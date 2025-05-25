#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
輸出格式化模組

處理 CLI 工具的輸出格式化，支持表格、JSON、CSV 等格式。
"""

import json
import csv
import io
import click
from typing import List, Dict, Any, Optional
from tabulate import tabulate

# 全局格式化設置
_output_format = 'table'
_verbose = False
_quiet = False

def setup_output_format(format_type: str, verbose: bool = False, quiet: bool = False):
    """設置全局輸出格式
    
    Args:
        format_type: 輸出格式 ('table', 'json', 'csv')
        verbose: 是否詳細輸出
        quiet: 是否靜默模式
    """
    global _output_format, _verbose, _quiet
    _output_format = format_type
    _verbose = verbose
    _quiet = quiet

def format_output(data: List[Dict[str, Any]], 
                 columns: List[str], 
                 title: Optional[str] = None,
                 ctx: Optional[click.Context] = None) -> None:
    """格式化輸出數據
    
    Args:
        data: 要輸出的數據列表
        columns: 要顯示的列名列表
        title: 輸出標題
        ctx: Click 上下文對象
    """
    if _quiet:
        return
    
    # 從上下文獲取格式設置
    format_type = _output_format
    if ctx and ctx.obj:
        format_type = ctx.obj.get('format', _output_format)
    
    if not data:
        if not _quiet:
            click.echo("沒有找到數據")
        return
    
    if format_type == 'json':
        _format_json(data, title)
    elif format_type == 'csv':
        _format_csv(data, columns, title)
    else:  # 預設為 table
        _format_table(data, columns, title)

def _format_table(data: List[Dict[str, Any]], 
                 columns: List[str], 
                 title: Optional[str] = None) -> None:
    """格式化為表格輸出"""
    if title and not _quiet:
        click.echo(f"\n{title}")
        click.echo("=" * len(title))
    
    # 準備表格數據
    table_data = []
    for item in data:
        row = [str(item.get(col, '')) for col in columns]
        table_data.append(row)
    
    # 格式化列標題
    headers = [col.replace('_', ' ').title() for col in columns]
    
    # 輸出表格
    table = tabulate(table_data, headers=headers, tablefmt='grid')
    click.echo(table)
    
    if not _quiet:
        click.echo(f"\n總計: {len(data)} 項")

def _format_json(data: List[Dict[str, Any]], 
                title: Optional[str] = None) -> None:
    """格式化為 JSON 輸出"""
    output = {
        'data': data,
        'total': len(data)
    }
    
    if title:
        output['title'] = title
    
    click.echo(json.dumps(output, ensure_ascii=False, indent=2))

def _format_csv(data: List[Dict[str, Any]], 
               columns: List[str], 
               title: Optional[str] = None) -> None:
    """格式化為 CSV 輸出"""
    if title and not _quiet:
        click.echo(f"# {title}")
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns)
    
    writer.writeheader()
    for item in data:
        # 只輸出指定的列
        filtered_item = {col: item.get(col, '') for col in columns}
        writer.writerow(filtered_item)
    
    click.echo(output.getvalue().strip())

def success_message(message: str) -> None:
    """顯示成功消息
    
    Args:
        message: 成功消息
    """
    if not _quiet:
        click.echo(click.style(f"✅ {message}", fg='green'))

def error_message(message: str) -> None:
    """顯示錯誤消息
    
    Args:
        message: 錯誤消息
    """
    click.echo(click.style(f"❌ {message}", fg='red'), err=True)

def warning_message(message: str) -> None:
    """顯示警告消息
    
    Args:
        message: 警告消息
    """
    if not _quiet:
        click.echo(click.style(f"⚠️  {message}", fg='yellow'))

def info_message(message: str) -> None:
    """顯示信息消息
    
    Args:
        message: 信息消息
    """
    if _verbose and not _quiet:
        click.echo(click.style(f"ℹ️  {message}", fg='blue'))

def progress_message(message: str) -> None:
    """顯示進度消息
    
    Args:
        message: 進度消息
    """
    if not _quiet:
        click.echo(f"🔄 {message}")

def format_error_response(error_code: int, message: str, details: Optional[str] = None) -> Dict[str, Any]:
    """格式化錯誤響應
    
    Args:
        error_code: 錯誤代碼
        message: 錯誤消息
        details: 錯誤詳情
        
    Returns:
        dict: 格式化的錯誤響應
    """
    error_response = {
        'error': {
            'code': error_code,
            'message': message
        }
    }
    
    if details:
        error_response['error']['details'] = details
    
    return error_response

def format_success_response(data: Any, message: Optional[str] = None) -> Dict[str, Any]:
    """格式化成功響應
    
    Args:
        data: 響應數據
        message: 成功消息
        
    Returns:
        dict: 格式化的成功響應
    """
    response = {
        'success': True,
        'data': data
    }
    
    if message:
        response['message'] = message
    
    return response

def print_separator(char: str = '-', length: int = 50) -> None:
    """打印分隔線
    
    Args:
        char: 分隔線字符
        length: 分隔線長度
    """
    if not _quiet:
        click.echo(char * length)

def format_datetime(dt_str: str) -> str:
    """格式化日期時間字符串
    
    Args:
        dt_str: 日期時間字符串
        
    Returns:
        str: 格式化後的日期時間
    """
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return dt_str

def truncate_text(text: str, max_length: int = 50) -> str:
    """截斷文本
    
    Args:
        text: 要截斷的文本
        max_length: 最大長度
        
    Returns:
        str: 截斷後的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...' 