# AI Automation Platform - Business Model

**Human + AI 協働による開発受託サービス**

## 📋 ビジネス概要

### コンセプト
AI自動化プラットフォームを活用した**低コスト・高速開発サービス**を提供し、その収益でシステム自体を成長させる自己増殖型ビジネスモデル。

### 核心価値
- ⚡ **高速開発**: AI が基礎実装、人間が品質保証
- 💰 **低コスト**: 自動化で工数削減 → 競争力ある価格
- 🔄 **再投資サイクル**: 収益でシステム強化 → さらに効率化

---

## 💵 料金体系（Price List）

### 🎨 画面開発（PHPRunner / Supabase）

| 項目 | 単価 | 納期 | 内容 |
|------|------|------|------|
| **CRUD画面作成** | ¥15,000 / 画面 | 2-3営業日 | 一覧・詳細・登録・編集・削除 |
| **検索機能追加** | ¥8,000 / 画面 | 1-2営業日 | フィルター、ページネーション |
| **カスタムフォーム** | ¥20,000 / 画面 | 3-5営業日 | バリデーション、動的項目 |
| **マスタ管理画面** | ¥12,000 / 画面 | 2-3営業日 | シンプルなマスタ管理 |
| **ダッシュボード** | ¥30,000 / 画面 | 5-7営業日 | グラフ、集計、KPI表示 |

### 🔧 機能開発（バックエンド / API）

| 項目 | 単価 | 納期 | 内容 |
|------|------|------|------|
| **REST API エンドポイント** | ¥10,000 / 本 | 1-2営業日 | CRUD操作 |
| **カスタムロジック** | ¥15,000 / 機能 | 2-4営業日 | 計算、変換、集計処理 |
| **外部API連携** | ¥25,000 / 連携 | 3-5営業日 | Webhook、OAuth、API統合 |
| **バッチ処理** | ¥20,000 / ジョブ | 3-5営業日 | 定期実行、データ同期 |
| **認証・権限機能** | ¥35,000 / システム | 5-7営業日 | Supabase RLS、ロール管理 |

### 🤖 AI ワークフロー（n8n / GitHub Actions）

| 項目 | 単価 | 納期 | 内容 |
|------|------|------|------|
| **シンプルワークフロー** | ¥18,000 / フロー | 2-3営業日 | 3-5ステップの自動化 |
| **複雑ワークフロー** | ¥40,000 / フロー | 5-7営業日 | 条件分岐、並列処理、エラーハンドリング |
| **GitHub Actions** | ¥15,000 / フロー | 2-3営業日 | CI/CD、Issue自動化 |
| **Supabase 連携** | ¥20,000 / フロー | 3-5営業日 | DB トリガー、Realtime |

### 📊 パッケージプラン

| プラン | 価格 | 内容 | 想定用途 |
|--------|------|------|----------|
| **スターター** | ¥80,000 | CRUD画面×5 + API×3 | 小規模管理システム |
| **ビジネス** | ¥180,000 | CRUD×10 + API×8 + ワークフロー×2 | 業務システム |
| **エンタープライズ** | ¥400,000 | CRUD×20 + API×15 + ワークフロー×5 + ダッシュボード | 基幹システム |

### 🔄 保守・運用

| 項目 | 単価 | 内容 |
|------|------|------|
| **月額保守** | ¥20,000 / 月 | 軽微な修正、相談対応 |
| **緊急対応** | ¥15,000 / 回 | 24時間以内の緊急対応 |
| **機能追加** | 個別見積 | 上記料金表に準じる |

---

## 🚪 Issue 受付窓口（Multi-Channel）

### 1. GAS BPMN Designer（優先）
- **URL**: https://script.google.com/.../exec?version=github
- **特徴**: 視覚的にワークフローを設計 → Issue自動作成
- **対象**: 技術者・非技術者両方

### 2. GitHub Issue フォーム
- **URL**: https://github.com/kenichimiyata/ai-automation-dashboard/issues/new/choose
- **テンプレート**:
  - 🎨 Screen Development Request
  - 🔧 Feature Development Request
  - 🤖 Workflow Automation Request
- **対象**: GitHub ユーザー、開発者

### 3. Google Form
- **作成予定**: Googleフォーム → GAS → GitHub Issue
- **特徴**: 一般ユーザー向け、見積もり自動計算
- **対象**: 非技術者、営業経由

### 4. Email → Webhook
- **作成予定**: 指定メールアドレス → n8n → GitHub Issue
- **特徴**: メール本文をパース、自動Issue化
- **対象**: 既存顧客、メール連絡希望者

### 5. Slack / Google Chat
- **作成予定**: チャット → Webhook → GitHub Issue
- **特徴**: 社内案件、リアルタイム相談
- **対象**: 社内メンバー、パートナー

---

## 🔄 業務フロー

### Phase 1: 受注（Intake）
```yaml
1. 顧客が窓口（GAS/GitHub/Form/Email）から Issue 登録
2. AI が Issue を解析
   - 必要な画面数、機能数を推定
   - 料金表から自動見積もり
3. Google Chat で人間に通知
4. 人間が見積もり確認・調整
5. 顧客に見積もり提示（GitHub Issue コメント / メール）
6. 承認 → 着手
```

### Phase 2: 開発（Execution）
```yaml
1. Issue に BPMN YAML / 仕様書を追加
2. AI Copilot が自動実装開始（PR作成）
3. 人間がコードレビュー
4. 修正指示 → AI が修正
5. 承認 → マージ
6. ステージング環境にデプロイ
```

### Phase 3: 納品（Delivery）
```yaml
1. 顧客にステージング URL 共有
2. 動作確認・フィードバック
3. 最終調整
4. 本番デプロイ
5. 請求書発行
6. Issue クローズ
```

---

## 📊 収益管理

### Supabase テーブル設計

#### `projects` テーブル
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  github_issue_number INTEGER NOT NULL,
  client_name TEXT NOT NULL,
  project_type TEXT NOT NULL, -- 'screen', 'api', 'workflow', 'package'
  status TEXT NOT NULL, -- 'estimate', 'approved', 'development', 'review', 'delivered', 'invoiced', 'paid'
  estimated_price INTEGER,
  final_price INTEGER,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now(),
  metadata JSONB
);
```

#### `project_items` テーブル
```sql
CREATE TABLE project_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id),
  item_type TEXT NOT NULL, -- 'screen', 'api', 'workflow', etc.
  item_name TEXT NOT NULL,
  quantity INTEGER DEFAULT 1,
  unit_price INTEGER NOT NULL,
  subtotal INTEGER NOT NULL,
  complexity TEXT, -- 'simple', 'medium', 'complex'
  created_at TIMESTAMPTZ DEFAULT now()
);
```

#### `invoices` テーブル
```sql
CREATE TABLE invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id),
  invoice_number TEXT UNIQUE NOT NULL,
  total_amount INTEGER NOT NULL,
  issued_at TIMESTAMPTZ DEFAULT now(),
  due_date TIMESTAMPTZ,
  paid_at TIMESTAMPTZ,
  status TEXT NOT NULL, -- 'draft', 'sent', 'paid', 'overdue'
  metadata JSONB
);
```

### ダッシュボード KPI
- 📈 **月次収益**: invoices テーブルから集計
- 📊 **案件ステータス**: projects.status 別カウント
- ⏱️ **平均納期**: completed_at - started_at
- 💰 **平均単価**: final_price の平均
- 🔄 **リピート率**: client_name の重複度

---

## 🎯 成長戦略

### Step 1: 実績づくり（0 → 30万円/月）
- ✅ 作ったシステムで自社案件を受注
- ✅ 友人・知人の小規模案件（スターター）
- ✅ 実績を GitHub Pages で公開
- ✅ 料金体系の最適化

### Step 2: 営業強化（30 → 100万円/月）
- 🔄 Google Form 営業窓口を公開
- 🔄 事例記事を量産（GitHub Pages）
- 🔄 SNS / ブログ での情報発信
- 🔄 パッケージプランで受注単価アップ

### Step 3: システム強化（100 → 300万円/月）
- 🔄 AI 精度向上（実案件データで学習）
- 🔄 テンプレート増強（よくあるパターン）
- 🔄 自動見積もり精度向上
- 🔄 納期短縮（ワークフロー最適化）

### Step 4: スケール（300万円/月 →）
- 🔄 開発者アサイン自動化
- 🔄 複数案件並行処理
- 🔄 サブスク型保守サービス
- 🔄 プラットフォーム化（他の開発者も使える）

---

## 📈 収益シミュレーション

### 月間 10案件の場合
| 案件タイプ | 件数 | 単価 | 小計 |
|------------|------|------|------|
| CRUD画面×5 | 3件 | ¥75,000 | ¥225,000 |
| API開発 | 4件 | ¥10,000 | ¥40,000 |
| ワークフロー | 2件 | ¥18,000 | ¥36,000 |
| カスタマイズ | 1件 | ¥50,000 | ¥50,000 |
| **合計** | **10件** | - | **¥351,000** |

**コスト**: 
- 人件費（レビュー・調整）: ¥100,000
- インフラ（Supabase/HF/GitHub）: ¥10,000
- **利益**: ¥241,000

### 月間 30案件の場合（スケール後）
| 案件タイプ | 件数 | 単価 | 小計 |
|------------|------|------|------|
| スターター | 10件 | ¥80,000 | ¥800,000 |
| ビジネス | 5件 | ¥180,000 | ¥900,000 |
| 個別開発 | 15件 | ¥30,000 | ¥450,000 |
| **合計** | **30件** | - | **¥2,150,000** |

**コスト**:
- 人件費（2名体制）: ¥600,000
- インフラ: ¥50,000
- **利益**: ¥1,500,000

---

## 🚀 次のアクション

### 1. システム整備（今週）
- [ ] 自動見積もり機能（BPMN → 料金計算）
- [ ] Google Form 受付窓口
- [ ] Supabase 収益管理テーブル作成
- [ ] 収益ダッシュボード（簡易版）

### 2. 営業準備（来週）
- [ ] サービス紹介ページ（GitHub Pages）
- [ ] 料金表ページ
- [ ] 事例ページ（まず自社案件）
- [ ] 問い合わせフォーム

### 3. 初受注（2週間後）
- [ ] 友人・知人に営業
- [ ] 実案件1件受注
- [ ] Issue → 開発 → 納品 フロー確認
- [ ] フィードバック収集

### 4. 改善サイクル（継続）
- [ ] 納期・品質・コストを最適化
- [ ] テンプレート・ライブラリ拡充
- [ ] AI 精度向上
- [ ] 収益データ分析

---

## 📝 契約・法務

### 利用規約（簡易版）
1. **納品物**: ソースコード + デプロイ済み環境
2. **著作権**: 納品後は顧客に譲渡
3. **保証**: 納品後30日間は無償修正
4. **支払い**: 着手金50% + 納品後50%
5. **キャンセル**: 着手後のキャンセルは50%チャージ

### 見積書 / 請求書テンプレート
- Google Docs テンプレート作成予定
- 自動生成機能（GAS）

---

## 🎉 まとめ

このシステムで**実案件を受けて稼ぎながらシステムを成長**させる好循環を作る。

**Key Success Factors**:
1. ✅ **高速開発**: AIで基礎実装、人間で品質保証
2. ✅ **低コスト**: 自動化でコスト削減
3. ✅ **再投資**: 収益でシステム強化
4. ✅ **スケール**: 案件増でもコスト線形増加しない

**Target**: 
- 3ヶ月後: 月商30万円
- 6ヶ月後: 月商100万円
- 1年後: 月商300万円

---

**Created**: 2026-03-02  
**Status**: Draft  
**Next Review**: 実案件1件完了後
