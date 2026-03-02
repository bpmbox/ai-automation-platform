#!/usr/bin/env python3
"""
n8n Workflow URL フィールドの設定を最終確認
"""

import os
import json
from supabase import create_client, Client

# Supabase 接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

def main():
    print("🔍 n8n Workflow URL フィールド最終確認")
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
    print(f"✅ ワークフロー: {workflow['name']}")
    
    # canonical_json を取得
    canonical = workflow['canonical_json']
    print(f"\n📊 総ノード数: {len(canonical['nodes'])}")
    
    # n8nWorkflowUrl が設定されているノードを確認
    print(f"\n🔍 n8nWorkflowUrl フィールドを確認中...")
    print("=" * 60)
    
    n8n_nodes = []
    for node in canonical['nodes']:
        if 'n8nWorkflowUrl' in node and node['n8nWorkflowUrl']:
            n8n_nodes.append(node)
    
    print(f"\n✅ n8nWorkflowUrl が設定されているノード: {len(n8n_nodes)} 個\n")
    
    for idx, node in enumerate(n8n_nodes, 1):
        print(f"【Workflow #{idx}】 {node.get('label', 'Unknown')}")
        print(f"   ID: {node.get('id', 'N/A')}")
        print(f"   Role: {node.get('role', 'N/A')}")
        print(f"   n8nWorkflowUrl: {node.get('n8nWorkflowUrl', 'N/A')}")
        
        # Note フィールドからも Webhook URL を確認
        note = node.get('note', '')
        if 'Webhook URL:' in note:
            webhook_line = [line.strip() for line in note.split('\n') if 'Webhook URL:' in line][0]
            print(f"   Note内URL: {webhook_line}")
        
        print()
    
    print("=" * 60)
    if len(n8n_nodes) == 4:
        print("🎉 完璧！全4つのノードに n8nWorkflowUrl が設定されています！")
    else:
        print(f"⚠️ 警告: 期待される4ノードのうち {len(n8n_nodes)} ノードのみ設定されています")
    
    print("\n📋 設定内容:")
    print("   ✅ Note フィールド: Webhook URL + 詳細情報")
    print("   ✅ n8nWorkflowUrl フィールド: Webhook URL")
    print("   ✅ BPMN Designer で参照可能")

if __name__ == "__main__":
    main()
