#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 工具開發需求單創建腳本

此腳本將 CLI 工具開發需求單直接寫入需求管理系統的資料庫中。
"""

import sys
import os
from datetime import datetime, timedelta

# 添加當前目錄到 Python 路徑，以便導入專案模組
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import create_connection, create_requirement, get_all_staff, get_user_by_username
from auth import login

def create_cli_requirement():
    """創建 CLI 工具開發需求單"""
    
    # 建立資料庫連接
    conn = create_connection()
    if not conn:
        print("❌ 無法連接到資料庫")
        return False
    
    try:
        # 獲取管理員用戶（nicholas）
        admin_user = get_user_by_username(conn, "nicholas")
        if not admin_user:
            print("❌ 找不到管理員用戶 'nicholas'")
            return False
        
        admin_id = admin_user[0]  # 用戶ID
        print(f"✅ 找到管理員用戶: {admin_user[3]} (ID: {admin_id})")
        
        # 獲取所有員工
        staff_list = get_all_staff(conn)
        if not staff_list:
            print("❌ 找不到任何員工用戶")
            return False
        
        print(f"✅ 找到 {len(staff_list)} 個員工用戶:")
        for staff in staff_list:
            print(f"   - {staff[1]} (ID: {staff[0]})")
        
        # 選擇指派對象（這裡選擇第一個員工，您可以修改）
        assignee_id = staff_list[0][0]
        assignee_name = staff_list[0][1]
        print(f"📋 將需求單指派給: {assignee_name} (ID: {assignee_id})")
        
        # 需求單詳細內容
        title = "開發需求管理系統 CLI 工具"
        
        description = """
## 需求概述
開發一個功能完整的命令行界面（CLI）工具，為現有的需求管理系統提供命令行操作能力。

## 主要功能需求

### 1. 認證功能 (auth)
- 登入功能：支持用戶名密碼登入
- 會話管理：支持會話保存和自動登入
- 登出功能：清理會話信息
- 身份查詢：查看當前登入用戶信息

### 2. 用戶管理功能 (user)
- 用戶列表：顯示所有用戶或按角色篩選
- 用戶創建：創建新用戶帳號
- 用戶查詢：查看特定用戶詳細信息
- 用戶更新：修改用戶信息

### 3. 需求單管理功能 (requirement)
- 創建需求單：支持立即發派和預約發派
- 需求單列表：支持多種篩選條件
- 需求單詳情：查看需求單完整信息
- 提交需求單：員工提交完成情況
- 審核需求單：管理員審核功能

### 4. 管理員功能 (admin)
- 系統統計：查看系統使用統計
- 預約管理：管理預約發派的需求單
- 垃圾桶管理：管理已刪除的需求單
- 數據庫維護：備份、恢復等維護功能

### 5. 批量操作功能
- 批量創建：從 CSV 文件批量創建需求單
- 批量更新：批量更新需求單狀態
- 模板支持：支持從模板創建需求單

## 技術需求

### 開發環境
- 程式語言：Python 3.8+
- CLI 框架：Click 或 argparse
- 數據庫：重用現有 SQLite 數據庫
- 配置管理：YAML 格式配置文件
- 日誌系統：標準 Python logging

### 架構要求
- 模塊化設計：按功能分離命令模組
- 可擴展性：支持插件系統
- 錯誤處理：完善的錯誤處理和用戶友好的錯誤信息
- 輸出格式：支持表格、JSON、CSV 多種輸出格式

### 性能要求
- 響應時間：單個命令執行時間 < 2秒
- 批量處理：支持處理 1000+ 條記錄
- 內存使用：正常操作內存使用 < 100MB

## 實施計劃

### 第一階段 (週 1-2): 基礎架構
- 設置項目結構和開發環境
- 實現 CLI 框架和基本命令結構
- 實現認證功能 (login, logout, whoami)
- 實現基本的輸出格式化 (table, json)
- 編寫基礎測試用例

### 第二階段 (週 3-4): 核心功能
- 實現需求單管理功能 (create, list, show)
- 實現用戶管理功能 (list, create, show)
- 實現需求單提交和審核功能
- 添加配置文件支持
- 實現會話管理

### 第三階段 (週 5): 管理員功能
- 實現管理員統計功能
- 實現預約發派管理
- 實現垃圾桶管理
- 實現數據庫維護功能
- 添加 CSV 輸出格式

### 第四階段 (週 6): 完善和測試
- 實現批量操作功能
- 完善錯誤處理和用戶體驗
- 編寫完整的測試套件
- 編寫用戶文檔和部署指南
- 性能優化和最終測試

## 驗收標準

### 功能驗收
- 所有命令功能正常運行
- 輸出格式正確且一致
- 錯誤處理適當且用戶友好
- 權限控制正確實施
- 批量操作功能正常

### 性能驗收
- 單個命令響應時間 < 2秒
- 批量處理 1000 條記錄 < 30秒
- 內存使用在合理範圍內

### 質量驗收
- 代碼通過所有測試用例
- 測試覆蓋率 > 80%
- 代碼符合 PEP 8 規範
- 文檔完整且準確

## 交付物
- 完整的 CLI 工具源代碼
- 單元測試和集成測試
- 用戶使用手冊
- 開發者文檔
- 部署指南

## 預計完成時間
4-6週

## 備註
此需求單編號：REQ-CLI-001
優先級：高
參考文檔：CLI_DESIGN.md, CLI_REQUIREMENT.md
        """.strip()
        
        # 設定優先級為緊急（因為是重要的系統擴展）
        priority = "urgent"
        
        # 設定預約發派時間（可選，這裡設為立即發派）
        scheduled_time = None  # None 表示立即發派
        
        # 創建需求單
        req_id = create_requirement(
            conn=conn,
            title=title,
            description=description,
            assigner_id=admin_id,
            assignee_id=assignee_id,
            priority=priority,
            scheduled_time=scheduled_time
        )
        
        if req_id:
            print(f"✅ 成功創建需求單！")
            print(f"   需求單ID: {req_id}")
            print(f"   標題: {title}")
            print(f"   指派者: {admin_user[3]} (ID: {admin_id})")
            print(f"   接收者: {assignee_name} (ID: {assignee_id})")
            print(f"   優先級: {'緊急' if priority == 'urgent' else '普通'}")
            print(f"   狀態: 已發派")
            print(f"   創建時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        else:
            print("❌ 創建需求單失敗")
            return False
            
    except Exception as e:
        print(f"❌ 創建需求單時發生錯誤: {e}")
        return False
    finally:
        conn.close()

def main():
    """主函數"""
    print("🚀 開始創建 CLI 工具開發需求單...")
    print("=" * 50)
    
    # 檢查資料庫文件是否存在
    if not os.path.exists("users.db"):
        print("❌ 找不到資料庫文件 'users.db'")
        print("   請確保您在正確的專案目錄中運行此腳本")
        return
    
    # 創建需求單
    success = create_cli_requirement()
    
    print("=" * 50)
    if success:
        print("🎉 CLI 工具開發需求單創建成功！")
        print("\n📝 您現在可以：")
        print("1. 運行 main.py 啟動需求管理系統")
        print("2. 使用管理員帳號 (nicholas/nicholas941013) 登入")
        print("3. 查看已發派的需求單")
        print("4. 或使用員工帳號查看收到的需求單")
        print("\n💡 提示：")
        print("- 需求單已設為緊急優先級")
        print("- 詳細的開發規格請參考 CLI_DESIGN.md 和 CLI_REQUIREMENT.md")
        print("- 可以根據實際情況調整需求單內容和指派對象")
    else:
        print("❌ 需求單創建失敗")
        print("請檢查錯誤信息並重試")

if __name__ == "__main__":
    main() 