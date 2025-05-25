#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模組

處理 CLI 工具的配置文件載入和管理。
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

# 預設配置
DEFAULT_CONFIG = {
    'database': {
        'path': './users.db'
    },
    'auth': {
        'session_timeout': 3600,  # 1小時
        'save_session': True
    },
    'output': {
        'default_format': 'table',
        'max_rows': 50,
        'show_headers': True
    },
    'logging': {
        'level': 'INFO',
        'file': None  # None 表示不寫入文件
    }
}

def get_config_paths() -> list:
    """獲取配置文件搜索路徑
    
    Returns:
        list: 配置文件路徑列表，按優先級排序
    """
    paths = []
    
    # 1. 環境變量指定的配置文件
    env_config = os.getenv('REQMGR_CONFIG')
    if env_config:
        paths.append(Path(env_config))
    
    # 2. 當前目錄的配置文件
    paths.append(Path('./reqmgr.yaml'))
    paths.append(Path('./reqmgr.yml'))
    
    # 3. 用戶主目錄的配置文件
    home = Path.home()
    paths.append(home / '.reqmgr' / 'config.yaml')
    paths.append(home / '.reqmgr' / 'config.yml')
    
    # 4. 系統級配置文件 (僅限 Unix 系統)
    if os.name != 'nt':  # 不是 Windows
        paths.append(Path('/etc/reqmgr/config.yaml'))
        paths.append(Path('/etc/reqmgr/config.yml'))
    
    return paths

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """載入配置文件
    
    Args:
        config_path: 指定的配置文件路徑，如果為 None 則自動搜索
        
    Returns:
        dict: 配置字典
    """
    config = DEFAULT_CONFIG.copy()
    
    if config_path:
        # 使用指定的配置文件
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                    if user_config:
                        config = merge_config(config, user_config)
            except Exception as e:
                print(f"警告: 無法載入配置文件 {config_file}: {e}")
    else:
        # 自動搜索配置文件
        for config_file in get_config_paths():
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        user_config = yaml.safe_load(f)
                        if user_config:
                            config = merge_config(config, user_config)
                    break  # 找到第一個有效配置文件就停止
                except Exception as e:
                    print(f"警告: 無法載入配置文件 {config_file}: {e}")
                    continue
    
    # 處理環境變量覆蓋
    config = apply_env_overrides(config)
    
    return config

def merge_config(base_config: Dict[str, Any], user_config: Dict[str, Any]) -> Dict[str, Any]:
    """合併配置字典
    
    Args:
        base_config: 基礎配置
        user_config: 用戶配置
        
    Returns:
        dict: 合併後的配置
    """
    result = base_config.copy()
    
    for key, value in user_config.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value
    
    return result

def apply_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    """應用環境變量覆蓋
    
    Args:
        config: 配置字典
        
    Returns:
        dict: 應用環境變量後的配置
    """
    # 資料庫路徑
    db_path = os.getenv('REQMGR_DB_PATH')
    if db_path:
        config['database']['path'] = db_path
    
    # 輸出格式
    output_format = os.getenv('REQMGR_FORMAT')
    if output_format:
        config['output']['default_format'] = output_format
    
    # 日誌級別
    log_level = os.getenv('REQMGR_LOG_LEVEL')
    if log_level:
        config['logging']['level'] = log_level
    
    return config

def save_config(config: Dict[str, Any], config_path: Optional[str] = None) -> bool:
    """保存配置到文件
    
    Args:
        config: 要保存的配置
        config_path: 配置文件路徑，如果為 None 則保存到用戶目錄
        
    Returns:
        bool: 是否保存成功
    """
    try:
        if config_path:
            config_file = Path(config_path)
        else:
            # 預設保存到用戶目錄
            config_dir = Path.home() / '.reqmgr'
            config_dir.mkdir(exist_ok=True)
            config_file = config_dir / 'config.yaml'
        
        # 確保目錄存在
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        return True
        
    except Exception as e:
        print(f"錯誤: 無法保存配置文件: {e}")
        return False

def get_database_path(config: Dict[str, Any]) -> str:
    """獲取資料庫路徑
    
    Args:
        config: 配置字典
        
    Returns:
        str: 資料庫文件路徑
    """
    db_path = config.get('database', {}).get('path', './users.db')
    
    # 如果是相對路徑，轉換為絕對路徑
    if not os.path.isabs(db_path):
        # 相對於當前工作目錄
        db_path = os.path.abspath(db_path)
    
    return db_path 