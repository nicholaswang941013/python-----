#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
需求管理系統 CLI 工具主入口

使用方式:
    reqmgr [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS] [ARGS]

範例:
    reqmgr auth login -u nicholas -p nicholas941013
    reqmgr requirement list --status pending
    reqmgr user create -u newuser -p password123 -n "新用戶" -e user@example.com
"""

import sys
import os
import click
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cli.commands.auth import auth_group
from cli.commands.user import user_group
from cli.commands.requirement import requirement_group
from cli.commands.admin import admin_group
from cli.utils.config import load_config
from cli.utils.formatter import setup_output_format

# 全局配置
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--config', '-c', 
              type=click.Path(exists=True),
              help='指定配置文件路徑')
@click.option('--format', '-f', 
              type=click.Choice(['table', 'json', 'csv']),
              default='table',
              help='輸出格式 (預設: table)')
@click.option('--verbose', '-v', 
              is_flag=True,
              help='詳細輸出')
@click.option('--quiet', '-q', 
              is_flag=True,
              help='靜默模式')
@click.version_option(version='0.1.0', prog_name='reqmgr')
@click.pass_context
def cli(ctx, config, format, verbose, quiet):
    """需求管理系統命令行工具
    
    這個工具提供了完整的需求管理系統命令行操作能力，
    包括用戶管理、需求單管理、認證等功能。
    """
    # 確保 context 對象存在
    ctx.ensure_object(dict)
    
    # 載入配置
    if config:
        ctx.obj['config'] = load_config(config)
    else:
        ctx.obj['config'] = load_config()
    
    # 設置輸出格式
    ctx.obj['format'] = format
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet
    
    # 設置輸出格式化器
    setup_output_format(format, verbose, quiet)

# 註冊命令組
cli.add_command(auth_group, name='auth')
cli.add_command(user_group, name='user')
cli.add_command(requirement_group, name='requirement')
cli.add_command(admin_group, name='admin')

def main():
    """主函數入口"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n操作已取消", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"錯誤: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main() 