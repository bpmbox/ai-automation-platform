# n8n Workflows 自動デプロイ

n8n_workflows/内のJSONファイルをn8nサーバーに自動デプロイします。

## 🔧 セットアップ

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
