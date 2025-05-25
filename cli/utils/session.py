#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
會話管理模組

處理用戶會話的保存、載入和管理。
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import base64

def get_session_file() -> Path:
    """獲取會話文件路徑
    
    Returns:
        Path: 會話文件路徑
    """
    # 創建用戶配置目錄
    config_dir = Path.home() / '.reqmgr'
    config_dir.mkdir(exist_ok=True)
    
    return config_dir / 'session'

def save_session(user_info, timeout: int = 3600) -> bool:
    """保存用戶會話
    
    Args:
        user_info: 用戶信息對象
        timeout: 會話超時時間（秒），預設 1 小時
        
    Returns:
        bool: 是否保存成功
    """
    try:
        session_file = get_session_file()
        
        # 計算過期時間
        login_time = datetime.now()
        expires_at = login_time + timedelta(seconds=timeout)
        
        # 準備會話數據
        session_data = {
            'user_id': user_info.id,
            'username': user_info.username,
            'name': user_info.name,
            'email': user_info.email,
            'role': user_info.role,
            'login_time': login_time.isoformat(),
            'expires_at': expires_at.isoformat(),
            'timeout': timeout
        }
        
        # 簡單的編碼（不是真正的加密，只是混淆）
        session_json = json.dumps(session_data)
        encoded_session = base64.b64encode(session_json.encode('utf-8')).decode('utf-8')
        
        # 保存到文件
        with open(session_file, 'w', encoding='utf-8') as f:
            f.write(encoded_session)
        
        # 設置文件權限（僅限 Unix 系統）
        if os.name != 'nt':  # 不是 Windows
            os.chmod(session_file, 0o600)  # 只有用戶可讀寫
        
        return True
        
    except Exception as e:
        print(f"保存會話失敗: {e}")
        return False

def load_session() -> Optional[Dict[str, Any]]:
    """載入用戶會話
    
    Returns:
        dict or None: 會話數據，如果沒有有效會話則返回 None
    """
    try:
        session_file = get_session_file()
        
        if not session_file.exists():
            return None
        
        # 讀取會話文件
        with open(session_file, 'r', encoding='utf-8') as f:
            encoded_session = f.read().strip()
        
        # 解碼會話數據
        session_json = base64.b64decode(encoded_session.encode('utf-8')).decode('utf-8')
        session_data = json.loads(session_json)
        
        # 檢查會話是否過期
        expires_at = datetime.fromisoformat(session_data['expires_at'])
        if datetime.now() > expires_at:
            # 會話已過期，刪除文件
            clear_session()
            return None
        
        return session_data
        
    except Exception as e:
        # 如果讀取失敗，清除可能損壞的會話文件
        clear_session()
        return None

def clear_session() -> bool:
    """清除用戶會話
    
    Returns:
        bool: 是否清除成功
    """
    try:
        session_file = get_session_file()
        
        if session_file.exists():
            session_file.unlink()
            return True
        
        return False
        
    except Exception as e:
        print(f"清除會話失敗: {e}")
        return False

def is_session_valid() -> bool:
    """檢查當前會話是否有效
    
    Returns:
        bool: 會話是否有效
    """
    session = load_session()
    return session is not None

def get_current_user() -> Optional[Dict[str, Any]]:
    """獲取當前登入用戶信息
    
    Returns:
        dict or None: 用戶信息，如果沒有有效會話則返回 None
    """
    session = load_session()
    if session:
        return {
            'id': session['user_id'],
            'username': session['username'],
            'name': session['name'],
            'email': session['email'],
            'role': session['role']
        }
    return None

def extend_session(additional_time: int = 3600) -> bool:
    """延長會話時間
    
    Args:
        additional_time: 要延長的時間（秒）
        
    Returns:
        bool: 是否延長成功
    """
    try:
        session = load_session()
        if not session:
            return False
        
        # 更新過期時間
        current_expires = datetime.fromisoformat(session['expires_at'])
        new_expires = current_expires + timedelta(seconds=additional_time)
        session['expires_at'] = new_expires.isoformat()
        
        # 重新保存會話
        session_file = get_session_file()
        session_json = json.dumps(session)
        encoded_session = base64.b64encode(session_json.encode('utf-8')).decode('utf-8')
        
        with open(session_file, 'w', encoding='utf-8') as f:
            f.write(encoded_session)
        
        return True
        
    except Exception as e:
        print(f"延長會話失敗: {e}")
        return False

def get_session_info() -> Optional[Dict[str, Any]]:
    """獲取會話詳細信息
    
    Returns:
        dict or None: 會話詳細信息
    """
    session = load_session()
    if session:
        login_time = datetime.fromisoformat(session['login_time'])
        expires_at = datetime.fromisoformat(session['expires_at'])
        now = datetime.now()
        
        return {
            'user_id': session['user_id'],
            'username': session['username'],
            'name': session['name'],
            'role': session['role'],
            'login_time': login_time.strftime('%Y-%m-%d %H:%M:%S'),
            'expires_at': expires_at.strftime('%Y-%m-%d %H:%M:%S'),
            'remaining_time': str(expires_at - now).split('.')[0],  # 移除微秒
            'is_valid': now < expires_at
        }
    return None

def require_auth(func):
    """裝飾器：要求用戶認證
    
    Args:
        func: 要裝飾的函數
        
    Returns:
        function: 裝飾後的函數
    """
    def wrapper(*args, **kwargs):
        if not is_session_valid():
            from cli.utils.formatter import error_message
            error_message("需要登入才能執行此操作，請先使用 'reqmgr auth login' 登入")
            import sys
            sys.exit(2)
        return func(*args, **kwargs)
    return wrapper

def require_admin(func):
    """裝飾器：要求管理員權限
    
    Args:
        func: 要裝飾的函數
        
    Returns:
        function: 裝飾後的函數
    """
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            from cli.utils.formatter import error_message
            error_message("需要登入才能執行此操作，請先使用 'reqmgr auth login' 登入")
            import sys
            sys.exit(2)
        
        if user['role'] != 'admin':
            from cli.utils.formatter import error_message
            error_message("此操作需要管理員權限")
            import sys
            sys.exit(3)
        
        return func(*args, **kwargs)
    return wrapper 