# 🤖 AI自動化プラットフォーム

**Supabase + GitHub Copilot + n8n 統合システム**

![Status](https://img.shields.io/badge/Status-Production-green)
![Platform](https://img.shields.io/badge/Platform-Multi--AI-blue)
![Integration](https://img.shields.io/badge/Integration-Supabase%20%7C%20GitHub%20%7C%20n8n-orange)

## 🎯 プロジェクト概要

AI開発を加速する自動化プラットフォームです。GitHub Issue、Supabase Realtime、VS Code Copilot を連携し、**質問するだけで自動開発**を実現します。

### ✨ 主要機能
- **🔄 GitHub Issue → Supabase → Copilot パイプライン** - Issue コメントが自動的に Copilot に転送
- **📡 Realtime 双方向通信** - Supabase Realtime による即座の情報共有
- **🤖 Multi-AI コラボレーション** - 複数の AI が協働して開発
- **🔧 n8n ワークフロー自動化** - ノーコードでの自動化フロー構築
- **📊 GitHub Actions 統合** - CI/CD パイプライン完備

## 🏗️ システムアーキテクチャ

```
┌──────────────────────────────────────────────────────────┐
│                  👥 GitHub Issue                         │
│              (質問・要求を投稿)                            │
└─────────────────┬────────────────────────────────────────┘
                  │ Webhook/Actions
┌─────────────────▼────────────────────────────────────────┐
│              🔄 n8n Workflow                             │
│         (GitHub → Supabase 変換)                         │
└─────────────────┬────────────────────────────────────────┘
                  │ INSERT
┌─────────────────▼────────────────────────────────────────┐
│            💾 Supabase Database                          │
│          (chat_history テーブル)                          │
│          📡 Realtime 有効化                               │
└────┬────────────────────────────────────────────┬────────┘
     │ Realtime Subscription                      │
     │                                            │
┌────▼───────────────────┐              ┌────────▼─────────┐
│  🖥️ VS Code Copilot   │              │  🌐 Web Client   │
│    (開発環境)          │              │  (ダッシュボード)  │
└───────────────────────┘              └──────────────────┘
```

## 📦 関連リポジトリ

### 🔧 コア実装
これらのリポジトリには実装の詳細があります（プライベート）：

- **shop11** - Laravel Blade + PHPRunner 統合システム
- **PhPRunner_11** - PHPRunner プロジェクトテンプレート
- **AUTOCREATE** - AI 統合開発環境
- **AUTOCREATER** - Supabase Bridge システム

### 🌐 公開情報
- **📚 [Wiki](https://github.com/kenichimiyata/ai-automation-platform/wiki)** - 詳細な技術ドキュメント
- **📖 [GitHub Pages](https://kenichimiyata.github.io/ai-automation-platform/)** - プロジェクト紹介サイト

## 🚀 クイックスタート

### 前提条件
- **Supabase アカウント** - データベース・Realtime 用
- **GitHub アカウント** - Issue・Actions 用
- **VS Code** - Copilot 拡張機能インストール済み
- **n8n** (オプション) - ワークフロー自動化用

### 基本セットアップ

#### 1. Supabase テーブル作成
```sql
CREATE TABLE chat_history (
  id BIGSERIAL PRIMARY KEY,
  ownerid VARCHAR(255),
  messages TEXT,
  送信日時 TIMESTAMP DEFAULT NOW()
);

-- Realtime 有効化
ALTER PUBLICATION supabase_realtime ADD TABLE chat_history;
```

#### 2. GitHub Actions ワークフロー
```yaml
name: Issue Comment to Supabase

on:
  issue_comment:
    types: [created]

jobs:
  send-to-supabase:
    runs-on: ubuntu-latest
    steps:
      - name: Send to Supabase
        run: |
          curl -X POST "${{ secrets.SUPABASE_URL }}/rest/v1/chat_history" \
            -H "apikey: ${{ secrets.SUPABASE_ANON_KEY }}" \
            -H "Content-Type: application/json" \
            -d "{
              \"ownerid\": \"${{ github.actor }}\",
              \"messages\": \"${{ github.event.comment.body }}\"
            }"
```

#### 3. VS Code 拡張機能設定
```json
{
  "supabase.url": "https://your-project.supabase.co",
  "supabase.anonKey": "your-anon-key"
}
```

## 📖 ドキュメント

### 📚 Wiki ページ
- [システムアーキテクチャ](https://github.com/kenichimiyata/ai-automation-platform/wiki/System-Architecture)
- [Supabase セットアップガイド](https://github.com/kenichimiyata/ai-automation-platform/wiki/Supabase-Setup)
- [GitHub Actions 設定](https://github.com/kenichimiyata/ai-automation-platform/wiki/GitHub-Actions)
- [n8n ワークフロー](https://github.com/kenichimiyata/ai-automation-platform/wiki/n8n-Workflows)
- [トラブルシューティング](https://github.com/kenichimiyata/ai-automation-platform/wiki/Troubleshooting)

### 🎓 チュートリアル
1. [はじめての Issue → Copilot 連携](https://github.com/kenichimiyata/ai-automation-platform/wiki/Tutorial-01-First-Integration)
2. [Realtime Subscription の設定](https://github.com/kenichimiyata/ai-automation-platform/wiki/Tutorial-02-Realtime-Setup)
3. [Multi-AI コラボレーション](https://github.com/kenichimiyata/ai-automation-platform/wiki/Tutorial-03-Multi-AI)

## 🎯 ユースケース

### 1. リモート開発支援
外出先から GitHub Issue にコメントするだけで、オフィスの VS Code Copilot が自動応答します。

### 2. チーム協働開発
複数の開発者が GitHub Issue 経由で AI に質問し、回答を共有できます。

### 3. AI エージェント会議室
複数の AI（Gemini、ChatGPT、Copilot）が Supabase を通じて会話・協働します。

## 🛠️ 技術スタック

| カテゴリ | 技術 | 用途 |
|---------|------|------|
| **Database** | Supabase | データ保存・Realtime |
| **AI** | GitHub Copilot | コード生成・質問応答 |
| **Automation** | n8n | ワークフロー自動化 |
| **CI/CD** | GitHub Actions | 自動デプロイ・テスト |
| **Frontend** | Gradio / noVNC | UI・リモートアクセス |
| **Backend** | FastAPI / Laravel | API・サーバーサイド |

## 🤝 コントリビューション

このプロジェクトは現在プライベート開発中ですが、公開可能な部分から順次オープンソース化を進めています。

### フィードバック・質問
GitHub Issue でお気軽にご質問ください：
- [💬 質問・議論](https://github.com/kenichimiyata/ai-automation-platform/issues/new?labels=question)
- [🐛 バグ報告](https://github.com/kenichimiyata/ai-automation-platform/issues/new?labels=bug)
- [✨ 機能要望](https://github.com/kenichimiyata/ai-automation-platform/issues/new?labels=enhancement)

## 🌍 GitHub Pages セットアップ

本プロジェクトは GitHub Pages で自動的にドキュメント化されます（Jekyll）。

### ページ有効化手順

1. **リポジトリの Settings へアクセス**
   ```
   https://github.com/bpmbox/ai-automation-platform/settings/pages
   ```

2. **Pages セクションで以下を設定**
   - **Source**: `Deploy from a branch`
   - **Branch**: `main`
   - **Folder**: `/docs`

3. **Save をクリック**

4. **デプロイ完了を待つ**（2-5分）

5. **公開 URL にアクセス**
   ```
   https://bpmbox.github.io/ai-automation-platform/
   ```

### ドキュメント構成

```
docs/
├── index.md              # ランディングページ
├── _config.yml           # Jekyll 設定
└── wiki/
    ├── Home.md           # Wiki ホーム
    └── System-Architecture.md  # アーキテクチャ解説
```

---

## 📜 ライセンス

このドキュメントは MIT License で公開されています。

## 🔗 リンク

- **📚 GitHub Pages**: https://bpmbox.github.io/ai-automation-platform/
- **📋 Project Board**: https://github.com/orgs/bpmbox/projects/6
- **📂 Repository**: https://github.com/bpmbox/ai-automation-platform
- **📧 Contact**: k.miyata@urlounge.co.jp
- **🏢 Organization**: urlounge-ds

---

**🌟 Star をつけていただけると励みになります！**
