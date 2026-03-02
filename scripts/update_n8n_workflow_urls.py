#!/usr/bin/env python3
"""
n8n Workflow URL フィールドを一括更新
Supabase の canonical_json 内の n8nWorkflowUrl フィールドに Webhook URL を設定
"""

import os
import json
from supabase import create_client, Client

# Supabase 接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

# Webhook URL マッピング（Note フィールドから抽出したURL）
WEBHOOK_URLS = {
    "Task_N8N_CreateIssue": "https://kenken999-n8n-free.hf.space/webhook/google-form-to-issue",
    "Task_N8N_ClassifyIssue": "https://kenken999-n8n-free.hf.space/webhook/github-issue-classify",
    "Task_N8N_CreatePR": "https://kenken999-n8n-free.hf.space/webhook/github-branch-push",
    "Task_N8N_Deploy": "https://kenken999-n8n-free.hf.space/webhook/github-pr-approved"
}

def main():
    print("🚀 n8n Workflow URL フィールド一括更新")
    print("=" * 60)
    
    # Supabase クライアント作成
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # ワークフロー ID: 11 を取得
    print("\n📂 Supabase からワークフロー ID: 11 を取得中...")
    response = supabase.table('bpmn_workflows').select('*').eq('id', 11).execute()
    
    if not response.data:
        print("❌ ワークフロー ID: 11 が見つかりません")
        return
    
    workflow = response.data[0]
    print(f"✅ ワークフロー取得成功: {workflow['name']}")
    
    # canonical_json を取得
    canonical = workflow['canonical_json']
    updated_count = 0
    
    print(f"\n🔄 ノードの n8nWorkflowUrl フィールドを更新中...")
    print("=" * 60)
    
    # 各ノードを更新
    for node in canonical['nodes']:
        node_id = node.get('id', '')
        
        # Webhook URL が定義されているノードのみ更新
        if node_id in WEBHOOK_URLS:
            old_url = node.get('n8nWorkflowUrl', '')
            new_url = WEBHOOK_URLS[node_id]
            
            # n8nWorkflowUrl フィールドを更新
            node['n8nWorkflowUrl'] = new_url
            updated_count += 1
            
            print(f"\n【{node.get('label', 'Unknown')}】")
            print(f"   ID: {node_id}")
            print(f"   旧URL: {old_url if old_url else '(空)'}")
            print(f"   新URL: {new_url}")
            print(f"   ✅ 更新完了")
    
    if updated_count == 0:
        print("\n⚠️ 更新対象のノードが見つかりませんでした")
        return
    
    # Supabase に保存
    print(f"\n💾 Supabase に保存中...")
    print("=" * 60)
    
    update_data = {
        'canonical_json': canonical
    }
    
    response = supabase.table('bpmn_workflows').update(update_data).eq('id', 11).execute()
    
    if response.data:
        print(f"\n✅ 保存成功！")
        print(f"   更新ノード数: {updated_count}")
        print(f"   ワークフロー名: {workflow['name']}")
        print(f"\n📋 更新されたノード:")
        for node_id, url in WEBHOOK_URLS.items():
            print(f"   - {node_id}: {url}")
    else:
        print(f"\n❌ 保存失敗")
    
    print("\n" + "=" * 60)
    print("🎉 完了！BPMN Designer で確認してください")
    print("   手順: 🔄ボタン → ワークフロー選択 → n8nノードをクリック")

if __name__ == "__main__":
    main()
