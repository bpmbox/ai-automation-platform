# システムアーキテクチャ

## 全体フロー図

```
GitHub Issue
    ↓
    └─→ GitHub Actions Workflow
            ↓
            └─→ Webhook / API Call
                    ↓
                    └─→ Supabase REST API
                            ↓
                            ├─→ INSERT into chat_history
                            └─→ Realtime Event Broadcast
                                    ↓
                                    ├─→ supabase_to_vscode_chat.py (Polling)
                                    │   ↓
                                    │   └─→新メッセージ検出
                                    │
                                    └─→ SupabaseCopilotBridge.py
                                        ↓
                                        └─→ VS Code 自動入力
                                            ↓
                                            └─→ Copilot Chat 実行
                                                ↓
                                                └─→ 回答生成
                                                    ↓
                                                    └─→ Supabase に結果保存
```

## コンポーネント詳細

### 1. GitHub Issue（入力層）

**役割**: ユーザーの質問・要求を受け取る入口

**内容**:
- Issue タイトル: 大まかな質問
- Issue コメント: 詳細説明・追加情報
- Issue ラベル: カテゴリ分類（bug, feature, question など）

**トリガーイベント**:
- `issues.opened` - 新規 Issue 作成時
- `issue_comment.created` - コメント追加時

### 2. GitHub Actions（オーケストレーション層）

**役割**: GitHub イベントを検出し、Supabase へ連携

**使用されるワークフロー**:
```yaml
name: Send Issue to Supabase
on:
  issue_comment:
    types: [created]

jobs:
  send-to-supabase:
    runs-on: ubuntu-latest
    steps:
      - name: Extract Issue Data
        run: |
          curl -X POST "${{ secrets.SUPABASE_URL }}/rest/v1/chat_history" \
            -H "Authorization: Bearer ${{ secrets.SUPABASE_ANON_KEY }}" \
            -H "Content-Type: application/json" \
            -d "{
              \"ownerid\": \"${{ github.actor }}\",
              \"messages\": \"${{ github.event.comment.body }}\",
              \"issue_number\": ${{ github.event.issue.number }},
              \"issue_title\": \"${{ github.event.issue.title }}\"
            }"
```

**特徴**:
- Official GitHub Secrets で認証情報を安全に管理
- 複数のワークフロー並列実行可能
- ログで実行履歴をトラッキング可能

### 3. Supabase（データ層）

**役割**: データの永続化・Realtime イベント管理

**テーブル構造**:
```sql
Table: chat_history
├── id (BIGSERIAL PRIMARY KEY)
├── ownerid (VARCHAR)
├── messages (TEXT)
├── issue_number (INT)
├── issue_title (VARCHAR)
├── response (TEXT)  -- Copilot の回答
└── created_at (TIMESTAMP DEFAULT NOW())
```

**Realtime 設定**:
```sql
-- Wiki で Realtime を有効化
ALTER PUBLICATION supabase_realtime ADD TABLE chat_history;
```

**API エンドポイント**:
- **GET** `/rest/v1/chat_history?limit=10&order=id.desc`
  → 最新 10 件のメッセージ取得

- **POST** `/rest/v1/chat_history`
  → 新規メッセージ追加

- **PATCH** `/rest/v1/chat_history?id=eq.123`
  → 既存レコード更新

**認証方式**:
- **アノンキー**: クライアント側（セキュアなAPI呼び出し）
- **サービスロールキー**: サーバー側（管理者権限）

### 4. supabase_to_vscode_chat.py（監視層）

**役割**: Supabase をポーリングして新メッセージを監視

**機能**:
```python
def get_new_messages():
    """Supabase から新着メッセージを取得"""
    result = run_curl(
        "GET",
        f"chat_history?order=id.desc&limit=5"
    )
    new_messages = [msg for msg in result if msg['id'] > last_message_id]
    return new_messages

def filter_messages(messages):
    """Copilot/GitHub メッセージをフィルタ（エコー防止）"""
    return [m for m in messages if 'copilot' not in m['ownerid'].lower()]

def create_chat_prompt(message):
    """メッセージを Copilot 入力フォーマットに変換"""
    return f"""
    ユーザー: {message['ownerid']}
    質問: {message['messages']}
    
    ※この回答を Supabase に保存してください
    """
```

**ポーリング間隔**: 2-5 秒（カスタマイズ可能）

**特徴**:
- curl ベースの HTTP API 呼び出し
- メモリ効率的なポーリング
- エコー防止（GitHub bot の循環参照防止）

### 5. SupabaseCopilotBridge.py（自動化層）

**役割**: VS Code に自動的にプロンプトを入力・実行

**主要機能**:

#### ① 日本語テキスト処理
```python
def send_japanese_text_via_clipboard(text):
    """日本語テキストをクリップボード経由で送信"""
    import win32clipboard
    import win32con
    
    win32clipboard.OpenClipboard()
    win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')  # ペースト
```

#### ② 座標ベースクリック
```python
chat_x = int(os.getenv('CHAT_COORDINATE_X', '1335'))
chat_y = int(os.getenv('CHAT_COORDINATE_Y', '1045'))
pyautogui.click(chat_x, chat_y)  # Chat 入力欄をクリック
```

**環境変数**:
- `CHAT_COORDINATE_X`: Chat 入力欄の X 座標
- `CHAT_COORDINATE_Y`: Chat 入力欄の Y 座標
- `SUPABASE_URL`: Supabase プロジェクト URL
- `SUPABASE_ANON_KEY`: 認証キー

**ポート**: 7872 (Gradio UI ホスト; 自動検出)

### 6. VS Code Copilot Chat（処理層）

**役割**: 入力されたプロンプトに対して回答を生成

**トリガー**: Enter キーが押下される

**出力**: 
- テキスト回答
- コード提案
- 質問した Issue へのコメント（オプション）

---

## データフロー詳細

### シーケンス図

```
ユーザー          GitHub           Actions          Supabase         Bridge          Copilot
  │                 │                 │                 │               │              │
  │──Issue Comment──→│                 │                 │               │              │
  │                 │                 │                 │               │              │
  │                 │──Webhook Trigger│                 │               │              │
  │                 │                 │                 │               │              │
  │                 │                 │──POST /rest/v1──→│               │              │
  │                 │                 │    chat_history  │               │              │
  │                 │                 │                 │               │              │
  │                 │                 │                 │   Realtime    │              │
  │                 │                 │                 │   Event───────→│              │
  │                 │                 │                 │               │              │
  │                 │                 │                 │               │─Ctrl+V───────→│
  │                 │                 │                 │               │  (自動入力)   │
  │                 │                 │                 │               │               │
  │                 │                 │                 │               │    Generate   │
  │                 │                 │                 │               │    Response   │
  │                 │                 │                 │               │               │
  │                 │                 │                 │     Copy       │
  │                 │                 │                 │←──Response─────│
  │                 │                 │                 │
  │                 │                PATCH (update)     │
  │                 │←─────────────────response──────────│
  │←─Comment Reply───│
  │(回答表示)        │
```

---

## 技術スタック

| レイヤー | 技術 | 用途 |
|---------|------|------|
| **入力** | GitHub Issues & Comments | ユーザーインタフェース |
| **オーケーション** | GitHub Actions YAML | イベント駆動 |
| **ネットワーク** | REST API / Webhooks | データ送受信 |
| **データ** | Supabase PostgreSQL | 永続化・同期 |
| **リアルタイム** | Supabase Realtime WebSocket | Push 更新 |
| **監視** | Python + curl | メッセージ監視 |
| **自動化** | Python pyautogui | キーボード・マウス |
| **入力補助** | win32clipboard | 日本語テキスト処理 |
| **AI** | GitHub Copilot API | 回答生成 |

---

## スケーラビリティ考慮

### 現在の制限
- **ポーリング間隔**: 2-5 秒（レイテンシ）
- **単一 Copilot インスタンス**: 並列処理なし
- **API レート制限**: GitHub Actions 1000 calls/hour

### スケールアップ戦略
1. **Realtime WebSocket subscribe** に移行（ポーリング廃止）
2. **Multi-Copilot**: 複数 VS Code インスタンス・複数ユーザー対応
3. **キューイング**: n8n で非同期処理化
4. **キャッシング**: 頻出質問への高速応答

---

## セキュリティアーキテクチャ

### 認証フロー

```
GitHub Actions
    ↓
使用秘密情報: GITHUB_TOKEN (自動提供)
    ↓
Request Supabase API
    ├─ Authorization Header: "Bearer SUPABASE_ANON_KEY"
    │
    ↓
Supabase RLS (Row Level Security)
    ├─ WHERE ownerid = auth.uid() (例)
    │
    ↓
Allow / Deny Access
```

### 推奨セキュリティ設定

1. **API キー管理**
   - 本番環境では サービスロールキー を使用しない
   - クライアント側は アノンキー のみ使用

2. **RLS ポリシー例**
```sql
CREATE POLICY chat_read ON chat_history
  FOR SELECT
  USING (ownerid = auth.uid());
```

3. **API レート制限**
   - GitHub Actions: built-in
   - Supabase: 管理画面で設定可能

---

## 監視・ロギング

### GitHub Actions ログ
- Actions タブで実行結果を確認
- ステップごとの実行時間・エラー情報

### Supabase ログ
- Logs エクスプローラーでクエリ監視
- API 呼び出し・エラー記録

### Python スクリプトログ
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"新規メッセージ検出: {message_id}")
logger.error(f"Supabase API エラー: {error}")
```

---

## 今後の拡張性

### 🔮 計画されている拡張
1. **Multi-AI サポート**: Gemini、ChatGPT との統合
2. **Web インタフェース**: Gradio ダッシュボード
3. **プロジェクト管理連携**: JIRA、Asana
4. **プロンプトカスタマイズ**: テンプレート機能
5. **履歴分析**: AI 回答品質の可視化

---

**最終更新**: 2026-02-27
