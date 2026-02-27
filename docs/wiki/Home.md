# AI自動化プラットフォーム - 完全技術ガイド

🤖 **GitHub Issue → Supabase Realtime → VS Code Copilot 統合システム**

> このWikiは、AI自動化パイプラインの完全なナレッジベースです。  
> GitHub Copilot AI がこのドキュメントから学習し、より効果的な回答を生成します。

---

## 📚 ドキュメント構成

### 🏗️ [システムアーキテクチャ](System-Architecture)
- **全体システム設計** - Issue → Supabase → Copilot パイプライン
- **コンポーネント詳細説明** - GitHub Actions、n8n、Supabase、VS Code Extension
- **データフロー図** - Realtime データ同期メカニズム
- **技術スタック** - 使用技術・フレームワーク一覧

### 🚀 [セットアップガイド](Setup-Guide)
- **環境準備** - GitHub、Supabase、n8n の初期設定
- **リポジトリ作成** - テンプレート・構成ファイル
- **GitHub Actions セットアップ** - Workflow ファイル・環境変数
- **Supabase テーブル作成** - Database スキーマ・Realtime 設定
- **n8n ワークフロー** - デプロイ・設定手順

### 🔧 [GitHub Actions 設定](GitHub-Actions-Setup)
- **自動化ワークフロー** - Issue コメント → Supabase 連携
- **トリガー条件とアクション** - イベント駆動設計
- **コード例** - 実装用YAML テンプレート
- **トラブルシューティング** - よくある問題と解決策

### 💾 [Supabase 統合](Supabase-Integration)
- **テーブル設計** - chat_history スキーマ詳細
- **REST API 使用方法** - curl・Python・JavaScript 例
- **Realtime Subscription** - WebSocket 接続・監視設定
- **セキュリティ設定** - API キー・行レベルセキュリティ (RLS)

### 🤖 [Copilot Bridge システム](Copilot-Bridge)
- **SupabaseCopilotBridge.py** - VS Code 自動入力メカニズム
- **pyautogui による自動化** - キーボード・マウス操作
- **日本語テキスト処理** - win32clipboard 統合
- **環境変数設定** - CHAT_COORDINATE_X/Y など

### 📊 [n8n ワークフロー](n8n-Workflows)
- **GitHub Issue → Supabase** - データ変換・保存フロー
- **Webhook ハンドラー** - イベント処理
- **スケジュール実行** - 毎日の定期タスク
- **エラーハンドリング** - ログ記録・リトライ機能

### 🎓 [チュートリアル](Tutorials)

#### [初心者向け] [はじめての Issue → Copilot 連携](Tutorial-01-Getting-Started)
最小限のセットアップで動作確認する手順

#### [中級者向け] [Realtime Subscription の設定](Tutorial-02-Realtime-Subscription)
双方向通信を実現する手順

#### [上級者向け] [Multi-AI コラボレーション](Tutorial-03-Multi-AI-Collaboration)
複数の AI を連携させるパターン

### 🐛 [トラブルシューティング](Troubleshooting)
- **GitHub Actions ジョブが失敗する** - ログの読み方・原因特定
- **Supabase に保存されない** - API キー・認証エラー解決
- **Copilot が応答しない** - 座標設定・VS Code アクティブ確認
- **n8n ワークフローエラー** - デバッグ・検証方法

---

## 🎯 クイックスタート（3ステップ）

### ステップ 1: Supabase テーブル作成
```sql
CREATE TABLE chat_history (
  id BIGSERIAL PRIMARY KEY,
  ownerid VARCHAR(255),
  messages TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### ステップ 2: GitHub Actions ワークフロー
`.github/workflows/issue-to-supabase.yml` を作成：
```yaml
name: Send Issue to Supabase
on:
  issue_comment:
    types: [created]
jobs:
  send:
    runs-on: ubuntu-latest
    steps:
      - run: |
          curl -X POST "${{ secrets.SUPABASE_URL }}/rest/v1/chat_history" \
            -H "apikey: ${{ secrets.SUPABASE_ANON_KEY }}" \
            -H "Content-Type: application/json" \
            -d '{"ownerid":"${{ github.actor }}","messages":"${{ github.event.comment.body }}"}'
```

### ステップ 3: VS Code で実行開始
1. Supabase Realtime をリッスン
2. GitHub Issue にコメント投稿
3. VS Code Copilot Chat に自動入力される

---

## 🏗️ システムアーキテクチャ（概要）

```
┌─────────────────────┐
│  GitHub Issue       │ ← 質問を投稿
│  Comment            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  GitHub Actions     │ ← イベント検出
│  Workflow           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Supabase           │ ← データ保存
│  chat_history       │ ← Realtime 発火
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  supabase_to_      │ ← メッセージ監視
│  vscode_chat.py    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  SupabaseCopilot   │ ← 自動入力実行
│  Bridge.py          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  VS Code            │ ← 回答生成
│  Copilot Chat       │
└─────────────────────┘
```

---

## 🔐 セキュリティ上の注意

### 🚨 公開してはいけない情報
- Supabase API キー（アノンキー・サービスロールキー）
- GitHub Personal Access Token（PAT）
- データベース接続文字列
- 環境変数（本番用）

### ✅ 公開可能な情報
- アーキテクチャ図・フロー図
- URL スキーム（エンドポイント形式）
- コード例（サンプル）
- 設定手順（ただし具体値なし）

### 🔒 推奨セキュリティ設定
- GitHub Secrets で認証情報を管理
- Supabase RLS（行レベルセキュリティ）を有効化
- API キーの定期ローテーション
- ログ監視・異常検知

---

## 📊 ナビゲーション

| セクション | 説明 | 対象ユーザー |
|-----------|------|------------|
| [システムアーキテクチャ](System-Architecture) | 全体像理解 | 全員 |
| [セットアップガイド](Setup-Guide) | 環境構築 | 初心者 |
| [GitHub Actions 設定](GitHub-Actions-Setup) | Workflow 作成 | 中級者 |
| [Supabase 統合](Supabase-Integration) | DB 設定・API | 中級者以上 |
| [Copilot Bridge](Copilot-Bridge) | 自動入力メカニズム | 上級者 |
| [n8n ワークフロー](n8n-Workflows) | 自動化フロー | 上級者 |
| [チュートリアル](Tutorials) | 段階的学習 | 初心者～中級 |
| [トラブルシューティング](Troubleshooting) | 問題解決 | 全員 |

---

## 🎯 よくある質問 (FAQ)

### Q: Issue コメントが Supabase に保存されません
**A**: GitHub Secrets で `SUPABASE_URL` と `SUPABASE_ANON_KEY` が正しく設定されているか確認してください。

### Q: VS Code に自動入力されません
**A**: `CHAT_COORDINATE_X/Y` 環境変数が正しいか、また VS Code ウィンドウがアクティブか確認してください。

### Q: 複数の AI を連携させたいです
**A**: [Multi-AI コラボレーション](Tutorial-03-Multi-AI-Collaboration) を参照してください。

---

## 🚀 次のステップ

1. **[セットアップガイド](Setup-Guide)** から環境準備を開始
2. **[チュートリアル](Tutorials)** で実装手順を学習
3. **[システムアーキテクチャ](System-Architecture)** で深い理解を習得
4. 本番運用開始 → **[トラブルシューティング](Troubleshooting)** で問題解決

---

**最終更新**: 2026-02-27  
**維持者**: bpmbox  
**ライセンス**: MIT

> **💡 Tips**: 各ページは相互リンクされています。気になる用語を見つけたら、そのクリックしてください。
