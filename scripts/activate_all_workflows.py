# -*- coding: utf-8 -*-
"""
全ワークフローをアクティブ化
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv('c:/xampp/htdocs/localProject/.env')

N8N_API_KEY = os.getenv('N8N_API_KEY')
N8N_API_URL = os.getenv('N8N_API_URL')

workflow_ids = {
    'Workflow #1: Google Form → GitHub Issue': 'Smhynt7Gvp2Cfpu2',
    'Workflow #2: Issue自動分類': 'IRousr79doQJhyC5',
    'Workflow #3: PR自動作成': 'Luv7ZgygpznLnOrE',
    'Workflow #4: マージ＆デプロイ': 'Bbpmel4jLa8oeDCo'
}

print(f"🚀 全ワークフローをアクティブ化")
print(f"=" * 60)

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

for name, workflow_id in workflow_ids.items():
    print(f"📤 {name}")
    
    # まず現在のワークフロー取得
    get_response = requests.get(
        f"{N8N_API_URL}/workflows/{workflow_id}",
        headers=headers,
        timeout=30
    )
    
    if get_response.status_code != 200:
        print(f"   ❌ 取得失敗: {get_response.status_code}")
        continue
    
    workflow_data = get_response.json()
    
    # 許可されたフィールドのみ抽出
    allowed_fields = ['name', 'nodes', 'connections', 'settings', 'staticData', 'active']
    update_data = {k: v for k, v in workflow_data.items() if k in allowed_fields}
    
    # activeをTrueに設定
    update_data['active'] = True
    
    # PUT で更新
    response = requests.put(
        f"{N8N_API_URL}/workflows/{workflow_id}",
        headers=headers,
        json=update_data,
        timeout=30
    )
    
    if response.status_code == 200:
        print(f"   ✅ Active に変更完了")
    else:
        print(f"   ❌ エラー: {response.status_code}")
        print(f"   {response.text[:300]}")
    print()

print("=" * 60)
print("\n🎉 全ワークフローのアクティブ化完了！")
print("\n📋 Webhook URL:")
print("   Workflow #1: https://kenken999-n8n-free.hf.space/webhook/google-form-to-issue")
print("   Workflow #2: https://kenken999-n8n-free.hf.space/webhook/github-issue-classify")
print("   Workflow #3: https://kenken999-n8n-free.hf.space/webhook/github-branch-push")
print("   Workflow #4: https://kenken999-n8n-free.hf.space/webhook/github-pr-approved")
