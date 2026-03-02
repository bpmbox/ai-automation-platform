# -*- coding: utf-8 -*-
"""
全ワークフローのWebhook URLを取得
"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv('c:/xampp/htdocs/localProject/.env')

N8N_API_KEY = os.getenv('N8N_API_KEY')
N8N_API_URL = os.getenv('N8N_API_URL')
N8N_SERVER_URL = os.getenv('N8N_SERVER_URL')

print(f"🔗 Webhook URL 取得")
print(f"=" * 60)

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Accept': 'application/json'
}

# 全ワークフロー取得
response = requests.get(
    f"{N8N_API_URL}/workflows",
    headers=headers,
    timeout=30
)

if response.status_code != 200:
    print(f"❌ エラー: {response.status_code}")
    exit(1)

response_data = response.json()
# APIレスポンスが {data: []} 形式の場合に対応
if isinstance(response_data, dict) and 'data' in response_data:
    workflows = response_data['data']
else:
    workflows = response_data if isinstance(response_data, list) else []

# Workflow #1-#4 のみフィルタ
target_workflows = [
    'Workflow #1: Google Form → GitHub Issue',
    'Workflow #2: Issue自動分類',
    'Workflow #3: PR自動作成',
    'Workflow #4: マージ＆デプロイ'
]

print(f"📋 登録済みワークフロー: {len(workflows)} 件\n")

webhook_urls = {}

for workflow in workflows:
    name = workflow.get('name', '')
    
    if name in target_workflows:
        workflow_id = workflow.get('id')
        
        # ワークフロー詳細取得
        detail_response = requests.get(
            f"{N8N_API_URL}/workflows/{workflow_id}",
            headers=headers,
            timeout=30
        )
        
        if detail_response.status_code == 200:
            detail = detail_response.json()
            nodes = detail.get('nodes', [])
            
            # Webhookノードを検索
            webhook_node = None
            for node in nodes:
                if node.get('type') == 'n8n-nodes-base.webhook':
                    webhook_node = node
                    break
            
            if webhook_node:
                webhook_path = webhook_node.get('parameters', {}).get('path', '')
                webhook_url = f"{N8N_SERVER_URL}/webhook/{webhook_path}"
                
                webhook_urls[name] = {
                    'id': workflow_id,
                    'path': webhook_path,
                    'url': webhook_url,
                    'active': workflow.get('active', False)
                }
                
                status = "✅ Active" if workflow.get('active') else "⚠️ Inactive"
                print(f"【{name}】")
                print(f"   ID: {workflow_id}")
                print(f"   Webhook URL: {webhook_url}")
                print(f"   Status: {status}")
                print()

# 結果をファイルに保存
output_file = 'c:/xampp/htdocs/ai-automation-platform/n8n_workflows/webhook_urls.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(webhook_urls, f, indent=2, ensure_ascii=False)

print(f"💾 Webhook URL を保存: webhook_urls.json")
print()
print("次のステップ:")
print("1. 各ワークフローを Activate (有効化)")
print("2. GitHub Webhook 設定")
print("3. Google Form 作成")
