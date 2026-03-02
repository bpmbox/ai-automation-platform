# -*- coding: utf-8 -*-
import os
import sys
import json
from supabase import create_client, Client
from dotenv import load_dotenv

# UTF-8 出力強制
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# .env読み込み
load_dotenv('c:/xampp/htdocs/localProject/.env')

# Supabase接続
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ID: 9 のワークフローを取得
response = supabase.table('bpmn_workflows').select('*').eq('id', 9).single().execute()

if response.data:
    workflow = response.data
    print(f"ID: {workflow['id']}")
    print(f"Name: {workflow['name']}")
    print(f"Created: {workflow['created_at']}")
    print("\nCanonical JSON Structure:")
    
    canonical = workflow.get('canonical_json')
    if canonical:
        print(f"Keys: {list(canonical.keys())}")
        
        if 'nodes' in canonical:
            print(f"\n[OK] 'nodes' key exists: {len(canonical['nodes'])} nodes")
            if canonical['nodes']:
                print(f"First node: {json.dumps(canonical['nodes'][0], indent=2)}")
        else:
            print(f"\n[ERROR] 'nodes' key not found!")
        
        if 'edges' in canonical:
            print(f"\n[OK] 'edges' key exists: {len(canonical['edges'])} edges")
            if canonical['edges']:
                print(f"First edge: {json.dumps(canonical['edges'][0], indent=2)}")
        else:
            print(f"\n[ERROR] 'edges' key not found!")
    else:
        print("[ERROR] No canonical_json!")
else:
    print("Workflow ID: 9 not found!")
