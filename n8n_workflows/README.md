# n8n Workflows - AI Automation Platform

AI Automation Platformで使用するn8nワークフローの定義と自動デプロイ設定。

## 📋 ワークフロー一覧

### 1️⃣ Workflow #1: Google Form → GitHub Issue
**ファイル**: `workflow-1-form-to-issue.json`  
**トリガー**: Google Form送信 (Webhook)  
**目的**: フォーム要件をGitHub Issueに自動変換

### 2️⃣ Workflow #2: Issue自動分類
**ファイル**: `workflow-2-classify-issue.json`  
**トリガー**: GitHub Issue作成 (Webhook)  
**目的**: AI/ルールベースでラベル・担当者を自動設定

### 3️⃣ Workflow #3: PR自動作成
**ファイル**: `workflow-3-auto-create-pr.json`  
**トリガー**: ブランチPush検知  
**目的**: feature/issue-XXX ブランチから自動PR作成

### 4️⃣ Workflow #4: マージ＆デプロイ
**ファイル**: `workflow-4-merge-and-deploy.json`  
**トリガー**: PR承認  
**目的**: 自動マージ→ビルド→本番デプロイ

## 🔧 セットアップ

### n8n接続情報

- **Server URL**: https://kenken999-n8n-free.hf.space
- **API Endpoint**: https://kenken999-n8n-free.hf.space/api/v1
- **MCP Server**: https://kenken999-n8n-free.hf.space/mcp-server/http
- **認証**: API Key (`N8N_API_KEY` in localProject/.env)

### 1. GitHub Secrets設定

リポジトリの Settings → Secrets and variables → Actions で以下を設定：

```
N8N_API_URL=https://your-n8n-instance.com/api/v1
N8N_API_KEY=your_n8n_api_key_here
GOOGLE_CHAT_WEBHOOK=https://chat.googleapis.com/v1/spaces/xxx/messages?key=xxx&token=xxx
```

### 2. n8n API キー取得方法

n8n管理画面：
1. Settings → API
2. "Create API Key" をクリック
3. 生成されたキーをコピー
4. GitHub Secretsに `N8N_API_KEY` として保存

### 3. デプロイ方法

#### 自動デプロイ
```bash
# n8n_workflows/内のJSONファイルを編集
git add n8n_workflows/
git commit -m "feat: ワークフロー更新"
git push origin main
```

→ 自動的にGitHub Actionsが起動してn8nにデプロイ

#### 手動デプロイ
GitHub Actions → "Deploy n8n Workflows" → "Run workflow"

## 📊 デプロイフロー

```
git push
   ↓
GitHub Actions起動
   ↓
n8n_workflows/*.json 検出
   ↓
n8n API経由でデプロイ (作成/更新)
   ↓
Google Chat通知
```

## 📁 ワークフロー管理

### 新規ワークフロー追加
```bash
# n8nでワークフローをエクスポート
# または手動でJSONファイル作成
cp my_workflow.json n8n_workflows/

git add n8n_workflows/my_workflow.json
git commit -m "feat: 新規ワークフロー追加 - My Workflow"
git push
```

### 既存ワークフロー更新
```bash
# n8n_workflows/内のJSONを編集
git add n8n_workflows/
git commit -m "fix: ワークフロー修正 - エラーハンドリング追加"
git push
```

---

## 🎯 ワークフロー詳細仕様

### Workflow #1: Google Form → GitHub Issue

**処理フロー**:
```
Google Form Webhook → データ検証 → GitHub API (Create Issue) → Google Chat通知
```

**入力データ**:
```json
{
  "title": "要件タイトル",
  "description": "詳細説明",
  "priority": "high|medium|low",
  "category": "feature|bug|enhancement",
  "requester": "要求者名"
}
```

**出力データ**:
```json
{
  "issue_url": "https://github.com/owner/repo/issues/123",
  "issue_number": 123,
  "created_at": "2026-03-02T10:00:00Z"
}
```

---

### Workflow #2: Issue自動分類

**処理フロー**:
```
GitHub Issue Webhook → AI分析 → ラベル設定 → 担当者アサイン
```

**分類ルール**:
| キーワード | ラベル | 優先度 | 担当者 |
|-----------|--------|--------|--------|
| "緊急", "ASAP" | `priority: high` | high | kenichimiyata |
| "バグ", "エラー" | `bug` | high | poe-dari-san |
| "機能追加" | `enhancement` | medium | kenichimiyata |
| "ドキュメント" | `documentation` | low | AI Agent |

---

### Workflow #3: PR自動作成

**処理フロー**:
```
Branch Push → ブランチ名解析 → コミット収集 → PRテンプレート適用 → PR作成
```

**PRテンプレート**:
```markdown
## 変更内容
[自動生成: コミットメッセージから抽出]

## 関連Issue
Closes #{issue_number}

## チェックリスト
- [ ] コードレビュー完了
- [ ] テスト実施
- [ ] ドキュメント更新
```

**レビュアー自動アサイン**:
- `feature/*` → kenichimiyata
- `bugfix/*` → poe-dari-san
- `docs/*` → AI Agent

---

### Workflow #4: マージ＆デプロイ

**処理フロー**:
```
PR Approved → 自動マージ → ビルド → デプロイ → ヘルスチェック → 完了通知
```

**デプロイ先**:
- shop11: `https://shop11.urlounge.co.jp`
- PhPRunner_11: `https://phprunner11.urlounge.co.jp`
- localProject: `https://localhost:7861`

**ヘルスチェック**:
```bash
curl -f https://{domain}/health || exit 1
```

**ロールバック条件**:
- ヘルスチェック失敗
- エラー率 > 5%
- レスポンスタイム > 3秒

---

## 📁 ワークフロー管理

### 新規ワークフロー追加
```bash
# n8nでワークフローをエクスポート
# または手動でJSONファイル作成
cp my_workflow.json n8n_workflows/

git add n8n_workflows/my_workflow.json
git commit -m "feat: 新規ワークフロー追加 - My Workflow"
git push
```

### 既存ワークフロー更新
```bash
# n8n_workflows/内のJSONを編集
git add n8n_workflows/
git commit -m "fix: ワークフロー修正 - エラーハンドリング追加"
git push
```

## 🔍 トラブルシューティング

### デプロイ失敗時
1. GitHub Actions のログ確認
2. n8n API URLが正しいか確認（末尾の`/api/v1`必須）
3. API Keyが有効か確認
4. ワークフローJSON形式が正しいか確認

### ワークフロー名の重複
同じ名前のワークフロー = 自動的に更新されます

### JSON形式エラー
```bash
# ローカルで検証
python -m json.tool n8n_workflows/my_workflow.json
```

## 📝 ワークフロー一覧

現在デプロイされているワークフロー：
- `github_issue_from_chat.json` - チャット→GitHub Issue作成
- `My workflow.json` - メインワークフロー
- `Supabase AI Chat Assistant.json` - Supabaseチャット連携
- `PhPRunner11 - Auto Issue Management.json` - Issue自動管理
- その他多数...

## 🔗 関連リンク

- [n8n API Documentation](https://docs.n8n.io/api/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
