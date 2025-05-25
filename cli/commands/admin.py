#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管理員功能相關命令

提供系統統計、預約管理、垃圾桶管理等管理員專用功能。
"""

import click
import sys
from pathlib import Path
from datetime import datetime

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from database import (
    create_connection, get_admin_scheduled_requirements, 
    cancel_scheduled_requirement, dispatch_scheduled_requirements,
    get_deleted_requirements, restore_requirement, get_all_users,
    get_admin_dispatched_requirements, clear_all_requirements
)
from cli.utils.session import require_admin, get_current_user
from cli.utils.formatter import format_output, success_message, error_message, warning_message

@click.group()
def admin_group():
    """管理員功能相關命令"""
    pass

@admin_group.command('stats')
@click.pass_context
@require_admin
def stats_command(ctx):
    """顯示系統統計信息
    
    顯示用戶數量、需求單統計等系統概況。
    
    範例:
        reqmgr admin stats
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
        
        cursor = conn.cursor()
        
        # 獲取用戶統計
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        admin_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'staff'")
        staff_count = cursor.fetchone()[0]
        
        # 獲取需求單統計
        cursor.execute("SELECT COUNT(*) FROM requirements WHERE is_deleted = 0")
        total_requirements = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM requirements WHERE status = 'pending' AND is_deleted = 0")
        pending_requirements = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM requirements WHERE status = 'submitted' AND is_deleted = 0")
        submitted_requirements = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM requirements WHERE status = 'completed' AND is_deleted = 0")
        completed_requirements = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM requirements WHERE is_dispatched = 0")
        scheduled_requirements = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM requirements WHERE is_deleted = 1")
        deleted_requirements = cursor.fetchone()[0]
        
        # 獲取當前管理員的需求單統計
        cursor.execute("SELECT COUNT(*) FROM requirements WHERE assigner_id = ? AND is_deleted = 0", (current_user['id'],))
        my_requirements = cursor.fetchone()[0]
        
        conn.close()
        
        # 準備統計數據
        stats_data = [
            {'category': '用戶統計', 'item': '管理員數量', 'count': admin_count},
            {'category': '用戶統計', 'item': '員工數量', 'count': staff_count},
            {'category': '用戶統計', 'item': '總用戶數', 'count': admin_count + staff_count},
            {'category': '需求單統計', 'item': '總需求單數', 'count': total_requirements},
            {'category': '需求單統計', 'item': '待處理', 'count': pending_requirements},
            {'category': '需求單統計', 'item': '已提交', 'count': submitted_requirements},
            {'category': '需求單統計', 'item': '已完成', 'count': completed_requirements},
            {'category': '需求單統計', 'item': '預約發派', 'count': scheduled_requirements},
            {'category': '需求單統計', 'item': '已刪除', 'count': deleted_requirements},
            {'category': '個人統計', 'item': '我發派的需求單', 'count': my_requirements}
        ]
        
        # 顯示統計信息
        format_output(stats_data, ['category', 'item', 'count'], 
                     title="系統統計信息", ctx=ctx)
        
    except Exception as e:
        error_message(f"獲取統計信息時發生錯誤: {e}")
        sys.exit(1)

@admin_group.command('scheduled')
@click.option('--dispatch', '-d',
              is_flag=True,
              help='立即發派所有到期的預約需求單')
@click.pass_context
@require_admin
def scheduled_command(ctx, dispatch):
    """管理預約發派的需求單
    
    顯示或管理預約發派的需求單。
    
    範例:
        reqmgr admin scheduled
        reqmgr admin scheduled --dispatch
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
        
        if dispatch:
            # 發派到期的預約需求單
            dispatched_count = dispatch_scheduled_requirements(conn)
            conn.close()
            
            if dispatched_count > 0:
                success_message(f"成功發派 {dispatched_count} 個到期的預約需求單")
            else:
                warning_message("沒有到期的預約需求單需要發派")
        else:
            # 顯示預約需求單列表
            scheduled_reqs = get_admin_scheduled_requirements(conn, current_user['id'])
            conn.close()
            
            if not scheduled_reqs:
                warning_message("沒有預約發派的需求單")
                return
            
            # 格式化預約需求單數據
            req_data = []
            for req in scheduled_reqs:
                req_data.append({
                    'id': req[0],
                    'title': req[1],
                    'priority': req[3],
                    'scheduled_time': req[4][:19] if req[4] else '',
                    'assignee': req[5],
                    'status': '待發派'
                })
            
            # 顯示預約需求單列表
            format_output(req_data, ['id', 'title', 'priority', 'scheduled_time', 'assignee', 'status'],
                         title="預約發派的需求單", ctx=ctx)
        
    except Exception as e:
        error_message(f"管理預約需求單時發生錯誤: {e}")
        sys.exit(1)

@admin_group.command('cancel')
@click.argument('req_id', type=int)
@click.pass_context
@require_admin
def cancel_command(ctx, req_id):
    """取消預約發派的需求單
    
    取消指定的預約發派需求單。
    
    參數:
        REQ_ID: 需求單ID
    
    範例:
        reqmgr admin cancel 5
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
        
        # 檢查需求單是否存在且為預約狀態
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.id, r.title, u.name as assignee_name
            FROM requirements r
            JOIN users u ON r.assignee_id = u.id
            WHERE r.id = ? AND r.assigner_id = ? AND r.is_dispatched = 0
        ''', (req_id, current_user['id']))
        
        requirement = cursor.fetchone()
        
        if not requirement:
            error_message(f"找不到ID為 {req_id} 的預約需求單或您沒有權限取消")
            conn.close()
            sys.exit(2)
        
        # 取消預約需求單
        success = cancel_scheduled_requirement(conn, req_id)
        conn.close()
        
        if success:
            success_message(f"成功取消預約需求單 '{requirement[1]}' (ID: {req_id})")
            click.echo(f"原指派對象: {requirement[2]}")
        else:
            error_message("取消預約需求單失敗")
            sys.exit(1)
        
    except Exception as e:
        error_message(f"取消預約需求單時發生錯誤: {e}")
        sys.exit(1)

@admin_group.command('trash')
@click.option('--restore', '-r',
              type=int,
              help='恢復指定ID的已刪除需求單')
@click.pass_context
@require_admin
def trash_command(ctx, restore):
    """管理垃圾桶中的需求單
    
    顯示或恢復已刪除的需求單。
    
    範例:
        reqmgr admin trash
        reqmgr admin trash --restore 5
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
        
        if restore:
            # 恢復指定的已刪除需求單
            success = restore_requirement(conn, restore)
            conn.close()
            
            if success:
                success_message(f"成功恢復需求單 (ID: {restore})")
            else:
                error_message(f"恢復需求單失敗，可能需求單不存在或未被刪除")
                sys.exit(1)
        else:
            # 顯示已刪除的需求單列表
            deleted_reqs = get_deleted_requirements(conn, current_user['id'])
            conn.close()
            
            if not deleted_reqs:
                warning_message("垃圾桶中沒有已刪除的需求單")
                return
            
            # 格式化已刪除需求單數據
            req_data = []
            for req in deleted_reqs:
                req_data.append({
                    'id': req[0],
                    'title': req[1],
                    'status': req[3],
                    'priority': req[4],
                    'assignee': req[7],
                    'deleted_at': req[8][:19] if req[8] else ''
                })
            
            # 顯示已刪除需求單列表
            format_output(req_data, ['id', 'title', 'status', 'priority', 'assignee', 'deleted_at'],
                         title="垃圾桶中的需求單", ctx=ctx)
            
            click.echo("\n💡 提示: 使用 'reqmgr admin trash --restore <ID>' 來恢復需求單")
        
    except Exception as e:
        error_message(f"管理垃圾桶時發生錯誤: {e}")
        sys.exit(1)

@admin_group.command('cleanup')
@click.option('--confirm', '-c',
              is_flag=True,
              help='確認執行清理操作')
@click.pass_context
@require_admin
def cleanup_command(ctx, confirm):
    """清理系統數據
    
    清空所有需求單數據。這是一個危險操作，需要確認。
    
    範例:
        reqmgr admin cleanup --confirm
    """
    try:
        if not confirm:
            error_message("此操作將清空所有需求單數據！")
            click.echo("如果確定要執行，請使用 --confirm 參數")
            sys.exit(2)
        
        # 再次確認
        click.echo("⚠️  警告：此操作將永久刪除所有需求單數據！")
        if not click.confirm("您確定要繼續嗎？"):
            click.echo("操作已取消")
            return
        
        success = clear_all_requirements()
        
        if success:
            success_message("系統數據清理完成")
        else:
            error_message("系統數據清理失敗")
            sys.exit(1)
        
    except Exception as e:
        error_message(f"清理系統數據時發生錯誤: {e}")
        sys.exit(1)

@admin_group.command('backup')
@click.option('--output', '-o',
              default='backup.sql',
              help='備份文件名')
@click.pass_context
@require_admin
def backup_command(ctx, output):
    """備份系統數據
    
    將系統數據備份到 SQL 文件。
    
    範例:
        reqmgr admin backup
        reqmgr admin backup --output my_backup.sql
    """
    try:
        import sqlite3
        import os
        
        # 檢查源數據庫是否存在
        if not os.path.exists('users.db'):
            error_message("找不到數據庫文件 users.db")
            sys.exit(1)
        
        # 連接到源數據庫
        source_conn = sqlite3.connect('users.db')
        
        # 創建備份
        with open(output, 'w', encoding='utf-8') as f:
            for line in source_conn.iterdump():
                f.write('%s\n' % line)
        
        source_conn.close()
        
        success_message(f"數據庫已備份到 {output}")
        
        # 顯示備份文件信息
        file_size = os.path.getsize(output)
        click.echo(f"備份文件大小: {file_size} 字節")
        click.echo(f"備份時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        error_message(f"備份數據庫時發生錯誤: {e}")
        sys.exit(1) 