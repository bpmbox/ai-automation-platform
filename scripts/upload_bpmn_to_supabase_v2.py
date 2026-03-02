# -*- coding: utf-8 -*-
"""
AI Automation Platform - BPMN Workflow to Supabase Uploader V2

BPMN Designer の期待する形式 (nodes, edges) でアップロードします。
"""
import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# .env読み込み
load_dotenv('c:/xampp/htdocs/localProject/.env')

# Supabase接続
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ エラー: SUPABASE_URL または SUPABASE_ANON_KEY が設定されていません")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def parse_bpmn_xml_to_canonical(bpmn_file_path: str) -> dict:
    """
    BPMN XML → BPMN Designer Canonical JSON 変換
    """
    tree = ET.parse(bpmn_file_path)
    root = tree.getroot()
    ns = {'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'}
    
    process = root.find('.//bpmn:process', ns)
    if not process:
        raise ValueError("BPMN process not found")
    
    process_id = process.get('id')
    process_name = process.get('name', 'Unnamed Process')
    
    nodes = []
    edges = []
    
    # startEvent
    for idx, elem in enumerate(process.findall('.//bpmn:startEvent', ns)):
        node_id = elem.get('id')
        nodes.append({
            'id': node_id,
            'label': elem.get('name', 'Start'),
            'kind': 'Start',
            'role': 'Shared',
            'pos': {'x': 100, 'y': 200},
            'bpmn_type': 'startEvent'
        })
    
    # serviceTask (AI)
    for idx, elem in enumerate(process.findall('.//bpmn:serviceTask', ns)):
        node_id = elem.get('id')
        doc_elem = elem.find('.//bpmn:documentation', ns)
        doc_text = doc_elem.text if doc_elem is not None else ""
        nodes.append({
            'id': node_id,
            'label': elem.get('name', 'Service Task'),
            'kind': 'Task',
            'role': 'AI',
            'pos': {'x': 300 + idx * 200, 'y': 200},
            'note': doc_text.strip() if doc_text else "",
            'bpmn_type': 'serviceTask'
        })
    
    # userTask (Human)
    for idx, elem in enumerate(process.findall('.//bpmn:userTask', ns)):
        node_id = elem.get('id')
        doc_elem = elem.find('.//bpmn:documentation', ns)
        doc_text = doc_elem.text if doc_elem is not None else ""
        nodes.append({
            'id': node_id,
            'label': elem.get('name', 'User Task'),
            'kind': 'Task',
            'role': 'Human',
            'pos': {'x': 500 + idx * 200, 'y': 400},
            'note': doc_text.strip() if doc_text else "",
            'bpmn_type': 'userTask'
        })
    
    # exclusiveGateway
    for idx, elem in enumerate(process.findall('.//bpmn:exclusiveGateway', ns)):
        node_id = elem.get('id')
        nodes.append({
            'id': node_id,
            'label': elem.get('name', 'Gateway'),
            'kind': 'Gateway',
            'role': 'Shared',
            'pos': {'x': 700 + idx * 200, 'y': 300},
            'bpmn_type': 'exclusiveGateway'
        })
    
    # endEvent
    for idx, elem in enumerate(process.findall('.//bpmn:endEvent', ns)):
        node_id = elem.get('id')
        nodes.append({
            'id': node_id,
            'label': elem.get('name', 'End'),
            'kind': 'End',
            'role': 'Shared',
            'pos': {'x': 900, 'y': 200},
            'bpmn_type': 'endEvent'
        })
    
    # sequenceFlow
    for elem in process.findall('.//bpmn:sequenceFlow', ns):
        edges.append({
            'from': elem.get('sourceRef'),
            'to': elem.get('targetRef'),
            'label': elem.get('name', '')
        })
    
    canonical_json = {
        'nodes': nodes,
        'edges': edges
    }
    
    return {
        'process_id': process_id,
        'process_name': process_name,
        'canonical_json': canonical_json,
        'node_count': len(nodes),
        'edge_count': len(edges)
    }

def upload_bpmn_to_supabase(bpmn_file_path: str, workflow_name: str = None):
    """
    BPMNファイルをSupabaseにアップロード (BPMN Designer 形式)
    """
    print(f"📄 BPMNファイルを読み込んでいます: {os.path.basename(bpmn_file_path)}")
    
    # BPMNをパース
    result = parse_bpmn_xml_to_canonical(bpmn_file_path)
    
    if workflow_name is None:
        workflow_name = result['process_name']
    
    print(f"💾 Supabaseに保存中: {workflow_name}")
    print(f"   - ノード数: {result['node_count']}")
    print(f"   - エッジ数: {result['edge_count']}")
    
    # Supabaseに保存
    data = {
        'name': workflow_name,
        'description': f"{result['process_name']} - {result['process_id']}",
        'canonical_json': result['canonical_json'],
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    response = supabase.table('bpmn_workflows').insert(data).execute()
    
    if response.data:
        print(f"\n✅ 保存成功！")
        print(f"   ID: {response.data[0]['id']}")
        print(f"   名前: {response.data[0]['name']}")
        print(f"   ノード数: {result['node_count']}")
        print(f"   エッジ数: {result['edge_count']}")
        return response.data[0]
    else:
        print(f"❌ 保存失敗")
        return None

if __name__ == '__main__':
    print("🚀 AI Automation Platform - BPMN Uploader V2")
    print("=" * 60)
    
    # BPMNファイルのパス
    bpmn_file_path = 'c:/xampp/htdocs/ai-automation-platform/docs/bpmn/ai-automation-workflow.bpmn'
    
    if not os.path.exists(bpmn_file_path):
        print(f"❌ エラー: BPMNファイルが見つかりません: {bpmn_file_path}")
        exit(1)
    
    # アップロード実行
    result = upload_bpmn_to_supabase(
        bpmn_file_path,
        "AI Automation Workflow (Complete V2)"
    )
    
    if result:
        print(f"\n🎉 アップロード完了！")
        print(f"BPMN Designer で確認してください:")
        print(f"http://localhost/ai-automation-platform/docs/bpmn-designer.html")
    else:
        print(f"\n❌ アップロード失敗")
        exit(1)
