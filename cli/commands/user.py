#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用戶管理相關命令

提供用戶列表、創建、查詢等功能。
"""

import click
import sys
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from database import create_connection, get_all_users, get_all_staff, get_all_admins, get_user_by_id, create_user
from cli.utils.session import require_auth, get_current_user
from cli.utils.formatter import format_output, success_message, error_message, warning_message

@click.group()
def user_group():
    """用戶管理相關命令"""
    pass

@user_group.command('list')
@click.option('--role', '-r',
              type=click.Choice(['all', 'admin', 'staff'], case_sensitive=False),
              default='all',
              help='篩選用戶角色 (all/admin/staff)')
@click.pass_context
@require_auth
def list_users_command(ctx, role):
    """列出用戶
    
    顯示系統中的所有用戶或按角色篩選。
    
    範例:
        reqmgr user list
        reqmgr user list --role admin
        reqmgr user list -r staff
    """
    try:
        conn = create_connection()
        if not conn:
            error_message("無法連接到資料庫")
            sys.exit(1)
        
        # 根據角色篩選獲取用戶
        if role.lower() == 'admin':
            users = get_all_admins(conn)
            title = "管理員列表"
        elif role.lower() == 'staff':
            users = get_all_staff(conn)
            title = "員工列表"
        else:
            users = get_all_users(conn)
            title = "所有用戶列表"
        
        conn.close()
        
        if not users:
            warning_message(f"沒有找到任何{role}用戶")
            return
        
        # 格式化用戶數據
        user_data = []
        for user in users:
            user_data.append({
                'id': user[0],
                'username': user[1],
                'name': user[3],
                'email': user[4],
                'role': user[5]
            })
        
        # 顯示用戶列表
        format_output(user_data, ['id', 'username', 'name', 'email', 'role'], 
                     title=title, ctx=ctx)
        
    except Exception as e:
        error_message(f"獲取用戶列表時發生錯誤: {e}")
        sys.exit(1)

@user_group.command('show')
@click.argument('user_id', type=int)
@click.pass_context
@require_auth
def show_user_command(ctx, user_id):
    """顯示用戶詳細信息
    
    顯示指定用戶的詳細信息。
    
    參數:
        USER_ID: 用戶ID
    
    範例:
        reqmgr user show 1
        reqmgr user show 2
    """
    try:
        conn = create_connection()
        if not conn:
            error_message("無法連接到資料庫")
            sys.exit(1)
        
        user = get_user_by_id(conn, user_id)
        conn.close()
        
        if not user:
            error_message(f"找不到ID為 {user_id} 的用戶")
            sys.exit(2)
        
        # 格式化用戶詳細信息
        user_data = {
            'id': user[0],
            'username': user[1],
            'name': user[3],
            'email': user[4],
            'role': user[5],
            'created_at': user[6] if len(user) > 6 else '未知'
        }
        
        # 顯示用戶詳情
        format_output([user_data], ['id', 'username', 'name', 'email', 'role', 'created_at'],
                     title=f"用戶詳細信息 (ID: {user_id})", ctx=ctx)
        
    except Exception as e:
        error_message(f"獲取用戶信息時發生錯誤: {e}")
        sys.exit(1)

@user_group.command('create')
@click.option('--username', '-u',
              required=True,
              help='用戶名')
@click.option('--password', '-p',
              required=True,
              help='密碼')
@click.option('--name', '-n',
              required=True,
              help='真實姓名')
@click.option('--email', '-e',
              required=True,
              help='電子郵件地址')
@click.option('--role', '-r',
              type=click.Choice(['admin', 'staff'], case_sensitive=False),
              default='staff',
              help='用戶角色 (admin/staff)')
@click.pass_context
@require_auth
def create_user_command(ctx, username, password, name, email, role):
    """創建新用戶
    
    創建一個新的用戶帳號。只有管理員可以執行此操作。
    
    範例:
        reqmgr user create -u testuser -p password123 -n "測試用戶" -e test@example.com
        reqmgr user create -u admin2 -p admin123 -n "管理員2" -e admin2@example.com -r admin
    """
    try:
        # 檢查當前用戶是否為管理員
        current_user = get_current_user()
        if not current_user or current_user['role'] != 'admin':
            error_message("只有管理員可以創建新用戶")
            sys.exit(3)
        
        # 驗證輸入
        if len(username) < 3:
            error_message("用戶名至少需要3個字符")
            sys.exit(2)
        
        if len(password) < 6:
            error_message("密碼至少需要6個字符")
            sys.exit(2)
        
        if '@' not in email:
            error_message("請提供有效的電子郵件地址")
            sys.exit(2)
        
        conn = create_connection()
        if not conn:
            error_message("無法連接到資料庫")
            sys.exit(1)
        
        # 檢查用戶名是否已存在
        from database import get_user_by_username
        existing_user = get_user_by_username(conn, username)
        if existing_user:
            error_message(f"用戶名 '{username}' 已存在")
            conn.close()
            sys.exit(2)
        
        # 創建用戶
        user_id = create_user(conn, username, password, name, email, role.lower())
        conn.close()
        
        if user_id:
            success_message(f"成功創建用戶 '{username}' (ID: {user_id})")
            
            # 顯示創建的用戶信息
            user_data = {
                'id': user_id,
                'username': username,
                'name': name,
                'email': email,
                'role': role.lower()
            }
            
            format_output([user_data], ['id', 'username', 'name', 'email', 'role'],
                         title="新創建的用戶", ctx=ctx)
        else:
            error_message("創建用戶失敗")
            sys.exit(1)
        
    except Exception as e:
        error_message(f"創建用戶時發生錯誤: {e}")
        sys.exit(1)

@user_group.command('update')
@click.argument('user_id', type=int)
@click.option('--name', '-n',
              help='更新真實姓名')
@click.option('--email', '-e',
              help='更新電子郵件地址')
@click.option('--password', '-p',
              help='更新密碼')
@click.option('--role', '-r',
              type=click.Choice(['admin', 'staff'], case_sensitive=False),
              help='更新用戶角色 (admin/staff)')
@click.pass_context
@require_auth
def update_user_command(ctx, user_id, name, email, password, role):
    """更新用戶信息
    
    更新指定用戶的信息。只有管理員可以執行此操作。
    
    參數:
        USER_ID: 用戶ID
    
    範例:
        reqmgr user update 2 --name "新姓名"
        reqmgr user update 2 --email "newemail@example.com"
        reqmgr user update 2 --role admin
    """
    try:
        # 檢查當前用戶是否為管理員
        current_user = get_current_user()
        if not current_user or current_user['role'] != 'admin':
            error_message("只有管理員可以更新用戶信息")
            sys.exit(3)
        
        # 檢查是否提供了要更新的字段
        if not any([name, email, password, role]):
            error_message("請至少提供一個要更新的字段")
            sys.exit(2)
        
        conn = create_connection()
        if not conn:
            error_message("無法連接到資料庫")
            sys.exit(1)
        
        # 檢查用戶是否存在
        user = get_user_by_id(conn, user_id)
        if not user:
            error_message(f"找不到ID為 {user_id} 的用戶")
            conn.close()
            sys.exit(2)
        
        # 構建更新語句
        update_fields = []
        params = []
        
        if name:
            update_fields.append("name = ?")
            params.append(name)
        
        if email:
            if '@' not in email:
                error_message("請提供有效的電子郵件地址")
                conn.close()
                sys.exit(2)
            update_fields.append("email = ?")
            params.append(email)
        
        if password:
            if len(password) < 6:
                error_message("密碼至少需要6個字符")
                conn.close()
                sys.exit(2)
            update_fields.append("password = ?")
            params.append(password)
        
        if role:
            update_fields.append("role = ?")
            params.append(role.lower())
        
        params.append(user_id)
        
        # 執行更新
        cursor = conn.cursor()
        update_sql = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(update_sql, params)
        conn.commit()
        
        if cursor.rowcount > 0:
            success_message(f"成功更新用戶 ID {user_id} 的信息")
            
            # 顯示更新後的用戶信息
            updated_user = get_user_by_id(conn, user_id)
            user_data = {
                'id': updated_user[0],
                'username': updated_user[1],
                'name': updated_user[3],
                'email': updated_user[4],
                'role': updated_user[5]
            }
            
            format_output([user_data], ['id', 'username', 'name', 'email', 'role'],
                         title="更新後的用戶信息", ctx=ctx)
        else:
            error_message("更新用戶信息失敗")
            sys.exit(1)
        
        conn.close()
        
    except Exception as e:
        error_message(f"更新用戶信息時發生錯誤: {e}")
        sys.exit(1) 