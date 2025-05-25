#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
需求單管理相關命令

提供需求單創建、查詢、提交、審核等功能。
"""

import click
import sys
from pathlib import Path
from datetime import datetime

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from database import (
    create_connection, create_requirement, get_user_requirements, 
    get_admin_dispatched_requirements, submit_requirement, approve_requirement,
    reject_requirement, get_user_by_username, get_all_staff
)
from cli.utils.session import require_auth, get_current_user
from cli.utils.formatter import format_output, success_message, error_message, warning_message

@click.group()
def requirement_group():
    """需求單管理相關命令"""
    pass

@requirement_group.command('list')
@click.option('--status', '-s',
              type=click.Choice(['all', 'pending', 'submitted', 'completed', 'rejected'], case_sensitive=False),
              default='all',
              help='篩選需求單狀態')
@click.option('--assignee', '-a',
              help='篩選指派給特定用戶的需求單 (用戶名)')
@click.pass_context
@require_auth
def list_requirements_command(ctx, status, assignee):
    """列出需求單
    
    顯示當前用戶相關的需求單。管理員可以看到所有發派的需求單，
    員工只能看到指派給自己的需求單。
    
    範例:
        reqmgr requirement list
        reqmgr requirement list --status pending
        reqmgr requirement list --assignee user1
    """
    try:
        current_user = get_current_user()
        if not current_user:
            error_message("請先登入")
            sys.exit(1)
        
        conn = create_connection()
        if not conn:
            error_message("無法連接到資料庫")
            sys.exit(1)
        
        # 根據用戶角色獲取需求單
        if current_user['role'] == 'admin':
            # 管理員可以看到所有發派的需求單
            requirements = get_admin_dispatched_requirements(conn, current_user['id'])
            title = "管理員發派的需求單"
        else:
            # 員工只能看到指派給自己的需求單
            requirements = get_user_requirements(conn, current_user['id'])
            title = "我的需求單"
        
        conn.close()
        
        if not requirements:
            warning_message("沒有找到任何需求單")
            return
        
        # 格式化需求單數據
        req_data = []
        for req in requirements:
            # 處理不同的數據結構
            if current_user['role'] == 'admin':  # 管理員視圖
                req_info = {
                    'id': req[0],
                    'title': req[1],
                    'status': req[3],
                    'priority': req[4],
                    'created_at': req[5][:19] if req[5] else '',
                    'assignee': req[6],
                    'comment': req[9] if len(req) > 9 and req[9] else ''
                }
            else:  # 員工視圖
                req_info = {
                    'id': req[0],
                    'title': req[1],
                    'status': req[3],
                    'priority': req[4],
                    'created_at': req[5][:19] if req[5] else '',
                    'assigner': req[6],
                    'comment': req[8] if len(req) > 8 and req[8] else ''
                }
            
            # 狀態篩選
            if status.lower() != 'all' and req_info['status'].lower() != status.lower():
                continue
            
            # 指派對象篩選（僅管理員）
            if assignee and current_user['role'] == 'admin':
                if req[6].lower() != assignee.lower():
                    continue
            
            req_data.append(req_info)
        
        if not req_data:
            warning_message(f"沒有找到符合條件的需求單")
            return
        
        # 選擇顯示的欄位
        if current_user['role'] == 'admin':
            columns = ['id', 'title', 'status', 'priority', 'created_at', 'assignee']
        else:
            columns = ['id', 'title', 'status', 'priority', 'created_at', 'assigner']
        
        # 顯示需求單列表
        format_output(req_data, columns, title=title, ctx=ctx)
        
    except Exception as e:
        error_message(f"獲取需求單列表時發生錯誤: {e}")
        sys.exit(1)

@requirement_group.command('show')
@click.argument('req_id', type=int)
@click.pass_context
@require_auth
def show_requirement_command(ctx, req_id):
    """顯示需求單詳細信息
    
    顯示指定需求單的詳細信息。
    
    參數:
        REQ_ID: 需求單ID
    
    範例:
        reqmgr requirement show 1
        reqmgr requirement show 5
    """
    try:
        current_user = get_current_user()
        if not current_user:
            error_message("請先登入")
            sys.exit(1)
        
        conn = create_connection()
        if not conn:
            error_message("無法連接到資料庫")
            sys.exit(1)
        
        # 獲取需求單詳情
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.id, r.title, r.description, r.status, r.priority, r.created_at,
                   u1.name as assigner_name, u2.name as assignee_name, r.comment, r.completed_at
            FROM requirements r
            JOIN users u1 ON r.assigner_id = u1.id
            JOIN users u2 ON r.assignee_id = u2.id
            WHERE r.id = ? AND r.is_deleted = 0
        ''', (req_id,))
        
        requirement = cursor.fetchone()
        conn.close()
        
        if not requirement:
            error_message(f"找不到ID為 {req_id} 的需求單")
            sys.exit(2)
        
        # 檢查權限：員工只能查看指派給自己的需求單
        if current_user['role'] == 'staff':
            if requirement[7] != current_user['name']:
                error_message("您沒有權限查看此需求單")
                sys.exit(3)
        
        # 格式化需求單詳細信息
        req_data = {
            'id': requirement[0],
            'title': requirement[1],
            'description': requirement[2][:100] + '...' if len(requirement[2]) > 100 else requirement[2],
            'status': requirement[3],
            'priority': requirement[4],
            'created_at': requirement[5][:19] if requirement[5] else '',
            'assigner': requirement[6],
            'assignee': requirement[7],
            'comment': requirement[8] if requirement[8] else '無',
            'completed_at': requirement[9][:19] if requirement[9] else '未完成'
        }
        
        # 顯示需求單詳情
        format_output([req_data], 
                     ['id', 'title', 'description', 'status', 'priority', 'created_at', 
                      'assigner', 'assignee', 'comment', 'completed_at'],
                     title=f"需求單詳細信息 (ID: {req_id})", ctx=ctx)
        
        # 如果是表格格式，額外顯示完整描述
        if ctx.obj.get('format', 'table') == 'table':
            click.echo(f"\n完整描述:")
            click.echo("=" * 50)
            click.echo(requirement[2])
        
    except Exception as e:
        error_message(f"獲取需求單詳情時發生錯誤: {e}")
        sys.exit(1)

@requirement_group.command('create')
@click.option('--title', '-t',
              required=True,
              help='需求單標題')
@click.option('--description', '-d',
              required=True,
              help='需求單描述')
@click.option('--assignee', '-a',
              required=True,
              help='指派給的用戶 (用戶名)')
@click.option('--priority', '-p',
              type=click.Choice(['normal', 'urgent'], case_sensitive=False),
              default='normal',
              help='優先級 (normal/urgent)')
@click.option('--scheduled', '-s',
              help='預約發派時間 (格式: YYYY-MM-DD HH:MM)')
@click.pass_context
@require_auth
def create_requirement_command(ctx, title, description, assignee, priority, scheduled):
    """創建新需求單
    
    創建一個新的需求單並指派給指定用戶。只有管理員可以執行此操作。
    
    範例:
        reqmgr requirement create -t "測試需求" -d "這是一個測試需求單" -a user1
        reqmgr requirement create -t "緊急任務" -d "緊急處理" -a staff1 -p urgent
        reqmgr requirement create -t "預約任務" -d "明天執行" -a user1 -s "2024-01-15 09:00"
    """
    try:
        current_user = get_current_user()
        if not current_user:
            error_message("請先登入")
            sys.exit(1)
        
        # 檢查權限
        if current_user['role'] != 'admin':
            error_message("只有管理員可以創建需求單")
            sys.exit(3)
        
        conn = create_connection()
        if not conn:
            error_message("無法連接到資料庫")
            sys.exit(1)
        
        # 檢查指派對象是否存在
        assignee_user = get_user_by_username(conn, assignee)
        if not assignee_user:
            error_message(f"找不到用戶 '{assignee}'")
            conn.close()
            sys.exit(2)
        
        assignee_id = assignee_user[0]
        
        # 處理預約時間
        scheduled_time = None
        if scheduled:
            try:
                scheduled_time = datetime.strptime(scheduled, '%Y-%m-%d %H:%M')
                if scheduled_time <= datetime.now():
                    error_message("預約時間必須是未來時間")
                    conn.close()
                    sys.exit(2)
            except ValueError:
                error_message("預約時間格式錯誤，請使用 YYYY-MM-DD HH:MM 格式")
                conn.close()
                sys.exit(2)
        
        # 創建需求單
        req_id = create_requirement(
            conn=conn,
            title=title,
            description=description,
            assigner_id=current_user['id'],
            assignee_id=assignee_id,
            priority=priority.lower(),
            scheduled_time=scheduled_time
        )
        
        conn.close()
        
        if req_id:
            if scheduled_time:
                success_message(f"成功創建預約需求單 (ID: {req_id})，將於 {scheduled} 發派")
            else:
                success_message(f"成功創建需求單 (ID: {req_id})，已立即發派")
            
            # 顯示創建的需求單信息
            req_data = {
                'id': req_id,
                'title': title,
                'description': description[:50] + '...' if len(description) > 50 else description,
                'assignee': assignee,
                'priority': priority.lower(),
                'status': 'not_dispatched' if scheduled_time else 'pending',
                'scheduled_time': scheduled if scheduled_time else '立即發派'
            }
            
            format_output([req_data], 
                         ['id', 'title', 'description', 'assignee', 'priority', 'status', 'scheduled_time'],
                         title="新創建的需求單", ctx=ctx)
        else:
            error_message("創建需求單失敗")
            sys.exit(1)
        
    except Exception as e:
        error_message(f"創建需求單時發生錯誤: {e}")
        sys.exit(1)

@requirement_group.command('submit')
@click.argument('req_id', type=int)
@click.option('--message', '-m',
              required=True,
              help='提交說明')
@click.pass_context
@require_auth
def submit_requirement_command(ctx, req_id, message):
    """提交需求單
    
    員工提交已完成的需求單，等待管理員審核。
    
    參數:
        REQ_ID: 需求單ID
    
    範例:
        reqmgr requirement submit 1 -m "已完成所有測試"
        reqmgr requirement submit 5 --message "任務已按要求完成"
    """
    try:
        current_user = get_current_user()
        if not current_user:
            error_message("請先登入")
            sys.exit(1)
        
        conn = create_connection()
        if not conn:
            error_message("無法連接到資料庫")
            sys.exit(1)
        
        # 檢查需求單是否存在且屬於當前用戶
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.id, r.title, r.status, u.name as assignee_name
            FROM requirements r
            JOIN users u ON r.assignee_id = u.id
            WHERE r.id = ? AND r.is_deleted = 0
        ''', (req_id,))
        
        requirement = cursor.fetchone()
        
        if not requirement:
            error_message(f"找不到ID為 {req_id} 的需求單")
            conn.close()
            sys.exit(2)
        
        # 檢查權限：只能提交指派給自己的需求單
        if requirement[3] != current_user['name']:
            error_message("您只能提交指派給自己的需求單")
            conn.close()
            sys.exit(3)
        
        # 檢查狀態：只能提交待處理的需求單
        if requirement[2] != 'pending':
            error_message(f"需求單狀態為 '{requirement[2]}'，無法提交")
            conn.close()
            sys.exit(2)
        
        # 提交需求單
        success = submit_requirement(conn, req_id, message)
        conn.close()
        
        if success:
            success_message(f"成功提交需求單 '{requirement[1]}' (ID: {req_id})")
            click.echo(f"提交說明: {message}")
        else:
            error_message("提交需求單失敗")
            sys.exit(1)
        
    except Exception as e:
        error_message(f"提交需求單時發生錯誤: {e}")
        sys.exit(1)

@requirement_group.command('approve')
@click.argument('req_id', type=int)
@click.pass_context
@require_auth
def approve_requirement_command(ctx, req_id):
    """審核通過需求單
    
    管理員審核通過員工提交的需求單。
    
    參數:
        REQ_ID: 需求單ID
    
    範例:
        reqmgr requirement approve 1
        reqmgr requirement approve 5
    """
    try:
        current_user = get_current_user()
        if not current_user:
            error_message("請先登入")
            sys.exit(1)
        
        # 檢查權限
        if current_user['role'] != 'admin':
            error_message("只有管理員可以審核需求單")
            sys.exit(3)
        
        conn = create_connection()
        if not conn:
            error_message("無法連接到資料庫")
            sys.exit(1)
        
        # 檢查需求單狀態
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.id, r.title, r.status, u.name as assignee_name
            FROM requirements r
            JOIN users u ON r.assignee_id = u.id
            WHERE r.id = ? AND r.assigner_id = ? AND r.is_deleted = 0
        ''', (req_id, current_user['id']))
        
        requirement = cursor.fetchone()
        
        if not requirement:
            error_message(f"找不到ID為 {req_id} 的需求單或您沒有權限審核")
            conn.close()
            sys.exit(2)
        
        # 檢查狀態：只能審核已提交的需求單
        if requirement[2] != 'submitted':
            error_message(f"需求單狀態為 '{requirement[2]}'，無法審核")
            conn.close()
            sys.exit(2)
        
        # 審核通過
        success = approve_requirement(conn, req_id)
        conn.close()
        
        if success:
            success_message(f"成功審核通過需求單 '{requirement[1]}' (ID: {req_id})")
            click.echo(f"執行者: {requirement[3]}")
        else:
            error_message("審核需求單失敗")
            sys.exit(1)
        
    except Exception as e:
        error_message(f"審核需求單時發生錯誤: {e}")
        sys.exit(1)

@requirement_group.command('reject')
@click.argument('req_id', type=int)
@click.pass_context
@require_auth
def reject_requirement_command(ctx, req_id):
    """審核拒絕需求單
    
    管理員審核拒絕員工提交的需求單。
    
    參數:
        REQ_ID: 需求單ID
    
    範例:
        reqmgr requirement reject 1
        reqmgr requirement reject 5
    """
    try:
        current_user = get_current_user()
        if not current_user:
            error_message("請先登入")
            sys.exit(1)
        
        # 檢查權限
        if current_user['role'] != 'admin':
            error_message("只有管理員可以審核需求單")
            sys.exit(3)
        
        conn = create_connection()
        if not conn:
            error_message("無法連接到資料庫")
            sys.exit(1)
        
        # 檢查需求單狀態
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.id, r.title, r.status, u.name as assignee_name
            FROM requirements r
            JOIN users u ON r.assignee_id = u.id
            WHERE r.id = ? AND r.assigner_id = ? AND r.is_deleted = 0
        ''', (req_id, current_user['id']))
        
        requirement = cursor.fetchone()
        
        if not requirement:
            error_message(f"找不到ID為 {req_id} 的需求單或您沒有權限審核")
            conn.close()
            sys.exit(2)
        
        # 檢查狀態：只能審核已提交的需求單
        if requirement[2] != 'submitted':
            error_message(f"需求單狀態為 '{requirement[2]}'，無法審核")
            conn.close()
            sys.exit(2)
        
        # 審核拒絕
        success = reject_requirement(conn, req_id)
        conn.close()
        
        if success:
            success_message(f"已拒絕需求單 '{requirement[1]}' (ID: {req_id})")
            click.echo(f"執行者: {requirement[3]}")
            click.echo("需求單狀態已重置為待處理，員工可重新提交")
        else:
            error_message("拒絕需求單失敗")
            sys.exit(1)
        
    except Exception as e:
        error_message(f"拒絕需求單時發生錯誤: {e}")
        sys.exit(1) 