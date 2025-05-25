#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
認證相關命令

提供用戶登入、登出、會話管理等功能。
"""

import click
import getpass
import sys
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from database import create_connection, get_user_by_username
from cli.utils.session import save_session as save_user_session, load_session, clear_session
from cli.utils.formatter import format_output, success_message, error_message

class UserInfo:
    """用戶信息類"""
    def __init__(self, user_data):
        self.id = user_data[0]
        self.username = user_data[1]
        self.password = user_data[2]  # 實際使用中不會暴露
        self.name = user_data[3]
        self.email = user_data[4]
        self.role = user_data[5]

def authenticate_user(username, password):
    """驗證用戶登入"""
    try:
        conn = create_connection()
        if not conn:
            return {'success': False, 'message': '無法連接到資料庫'}
        
        user_data = get_user_by_username(conn, username)
        conn.close()
        
        if not user_data:
            return {'success': False, 'message': '用戶不存在'}
        
        # 檢查密碼（這裡簡化處理，實際應該使用加密比較）
        if user_data[2] != password:
            return {'success': False, 'message': '密碼錯誤'}
        
        user_info = UserInfo(user_data)
        return {'success': True, 'user_info': user_info}
        
    except Exception as e:
        return {'success': False, 'message': f'認證過程中發生錯誤: {e}'}

@click.group()
def auth_group():
    """認證相關命令"""
    pass

@auth_group.command('login')
@click.option('--username', '-u', 
              prompt=True,
              help='用戶名')
@click.option('--password', '-p', 
              help='密碼 (如果不提供將會提示輸入)')
@click.option('--save-session', 
              is_flag=True,
              help='保存會話信息以便自動登入')
@click.pass_context
def login_command(ctx, username, password, save_session):
    """用戶登入
    
    範例:
        reqmgr auth login -u nicholas -p nicholas941013
        reqmgr auth login --save-session
    """
    try:
        # 如果沒有提供密碼，提示輸入
        if not password:
            password = getpass.getpass("密碼: ")
        
        # 嘗試登入
        result = authenticate_user(username, password)
        
        if result['success']:
            user_info = result['user_info']
            
            # 保存會話（如果需要）
            if save_session:
                save_session_result = save_user_session(user_info)
                if save_session_result:
                    success_message("登入成功，會話已保存")
                else:
                    success_message("登入成功，但會話保存失敗")
            else:
                success_message("登入成功")
            
            # 顯示用戶信息
            user_data = {
                'id': user_info.id,
                'username': user_info.username,
                'name': user_info.name,
                'email': user_info.email,
                'role': user_info.role
            }
            
            format_output([user_data], ['id', 'username', 'name', 'email', 'role'], 
                         title="用戶信息", ctx=ctx)
            
        else:
            error_message(result.get('message', '登入失敗'))
            sys.exit(2)
            
    except KeyboardInterrupt:
        click.echo("\n登入已取消")
        sys.exit(1)
    except Exception as e:
        error_message(f"登入過程中發生錯誤: {e}")
        sys.exit(1)

@auth_group.command('logout')
@click.pass_context
def logout_command(ctx):
    """用戶登出
    
    清除保存的會話信息。
    
    範例:
        reqmgr auth logout
    """
    try:
        if clear_session():
            success_message("已成功登出，會話信息已清除")
        else:
            click.echo("沒有找到活躍的會話")
            
    except Exception as e:
        error_message(f"登出過程中發生錯誤: {e}")
        sys.exit(1)

@auth_group.command('whoami')
@click.pass_context
def whoami_command(ctx):
    """查看當前登入用戶信息
    
    顯示當前保存的會話中的用戶信息。
    
    範例:
        reqmgr auth whoami
    """
    try:
        session = load_session()
        
        if session:
            user_data = {
                'id': session['user_id'],
                'username': session['username'],
                'name': session['name'],
                'email': session['email'],
                'role': session['role'],
                'login_time': session['login_time'],
                'expires_at': session['expires_at']
            }
            
            format_output([user_data], 
                         ['id', 'username', 'name', 'email', 'role', 'login_time', 'expires_at'],
                         title="當前用戶信息", ctx=ctx)
        else:
            click.echo("沒有找到活躍的會話，請先登入")
            sys.exit(2)
            
    except Exception as e:
        error_message(f"獲取用戶信息時發生錯誤: {e}")
        sys.exit(1) 