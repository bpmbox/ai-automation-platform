# -*- coding: utf-8 -*-
"""
Workflow #4 (ID: Bbpmel4jLa8oeDCo) の詳細確認
"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv('c:/xampp/htdocs/localProject/.env')

N8N_API_KEY = os.getenv('N8N_API_KEY')
N8N_API_URL = os.getenv('N8N_API_URL')
N8N_SERVER_URL = os.getenv('N8N_SERVER_URL')

workflow_id = 'Bbpmel4jLa8oeDCo'

print(f"🔍 Workflow #4 詳細確認")
print(f"=" * 60)

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Accept': 'application/json'
}

response = requests.get(
    f"{N8N_API_URL}/workflows/{workflow_id}",
    headers=headers,
    timeout=30
)

if response.status_code == 200:
    workflow = response.json()
    
    print(f"✅ Workflow 存在確認")
    print(f"   Name: {workflow.get('name')}")
    print(f"   ID: {workflow.get('id')}")
    print(f"   Active: {workflow.get('active')}")
    print(f"   Nodes: {len(workflow.get('nodes', []))}")
    print()
    
    # Webhookノード検索
    nodes = workflow.get('nodes', [])
    for node in nodes:
        if node.get('type') == 'n8n-nodes-base.webhook':
            webhook_path = node.get('parameters', {}).get('path', '')
            webhook_url = f"{N8N_SERVER_URL}/webhook/{webhook_path}"
            print(f"📌 Webhook URL: {webhook_url}")
else:
    print(f"❌ エラー: {response.status_code}")
    print(response.text)
