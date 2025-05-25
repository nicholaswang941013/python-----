#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 功能實現需求單創建腳本

此腳本將創建一個用於實現 CLI 工具核心功能的需求單。
"""

import sys
import os
from datetime import datetime, timedelta

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import create_connection, create_requirement, get_all_staff, get_user_by_username

def create_cli_implementation_requirement():
    """創建 CLI 功能實現需求單"""
    
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
        
        admin_id = admin_user[0]
        print(f"✅ 找到管理員用戶: {admin_user[3]} (ID: {admin_id})")
        
        # 獲取所有員工
        staff_list = get_all_staff(conn)
        if not staff_list:
            print("❌ 找不到任何員工用戶")
            return False
        
        print(f"✅ 找到 {len(staff_list)} 個員工用戶")
        
        # 選擇指派對象（選擇第一個員工）
        assignee_id = staff_list[0][0]
        assignee_name = staff_list[0][1]
        print(f"📋 將需求單指派給: {assignee_name} (ID: {assignee_id})")
        
        # 需求單詳細內容
        title = "實現 CLI 工具核心功能"
        
        description = """
## 需求概述
根據需求單 REQ-CLI-001 的規劃，實現 CLI 工具的核心功能，包括認證、用戶管理、需求單管理等模組。

## 主要任務

### 1. 完善認證功能 (auth) 🔐
- 修復 auth.py 中的模組導入問題
- 實現與現有資料庫的整合
- 完善登入/登出/會話查詢功能
- 測試認證流程的完整性

**驗收標準:**
- 能夠成功登入管理員和員工帳號
- 會話管理正常運作
- 錯誤處理適當

**測試命令:**
```bash
python reqmgr.py auth login -u nicholas -p nicholas941013 --save-session
python reqmgr.py auth whoami
python reqmgr.py auth logout
```

### 2. 實現用戶管理功能 (user) 👥
- 實現用戶列表查詢功能
- 實現用戶創建功能
- 實現用戶詳情查看功能
- 支持多種輸出格式 (table/json/csv)

**功能需求:**
- `user list`: 列出所有用戶，支持角色篩選
- `user create`: 創建新用戶，包含完整的參數驗證
- `user show <id>`: 顯示特定用戶的詳細信息
- `user update <id>`: 更新用戶信息（可選）

**驗收標準:**
- 能夠正確顯示用戶列表
- 能夠創建新用戶並驗證
- 輸出格式正確且美觀

**測試命令:**
```bash
python reqmgr.py user list
python reqmgr.py --format json user list
python reqmgr.py user create -u testuser -p password123 -n "測試用戶" -e test@example.com
python reqmgr.py user show 1
```

### 3. 實現需求單管理功能 (requirement) 📋
- 實現需求單列表查詢功能
- 實現需求單創建功能
- 實現需求單詳情查看功能
- 實現需求單狀態更新功能

**功能需求:**
- `requirement list`: 列出需求單，支持狀態篩選
- `requirement create`: 創建新需求單
- `requirement show <id>`: 顯示需求單詳情
- `requirement submit <id>`: 提交需求單（員工功能）
- `requirement approve <id>`: 審核需求單（管理員功能）

**驗收標準:**
- 能夠正確顯示需求單列表
- 能夠創建新需求單
- 狀態更新功能正常
- 權限控制正確

**測試命令:**
```bash
python reqmgr.py requirement list
python reqmgr.py requirement create -t "測試需求" -d "這是一個測試需求單" -a user1
python reqmgr.py requirement show 1
python reqmgr.py requirement submit 1 -m "已完成測試"
```

### 4. 實現管理員功能 (admin) 👑
- 實現系統統計功能
- 實現資料庫備份功能
- 實現預約發派管理
- 實現垃圾桶管理

**功能需求:**
- `admin stats`: 顯示系統統計信息
- `admin backup`: 備份資料庫
- `admin scheduled`: 管理預約發派
- `admin trash`: 管理已刪除的需求單

**驗收標準:**
- 統計信息準確且完整
- 備份功能正常運作
- 管理員權限控制正確

**測試命令:**
```bash
python reqmgr.py admin stats
python reqmgr.py admin backup
python reqmgr.py admin scheduled list
python reqmgr.py admin trash list
```

## 技術要求

### 代碼質量
- 遵循 PEP 8 代碼規範
- 添加適當的錯誤處理
- 提供清晰的用戶反饋
- 支持詳細模式 (--verbose) 輸出

### 整合要求
- 與現有資料庫模組完全整合
- 重用現有的業務邏輯
- 保持與 GUI 版本的功能一致性
- 支持所有現有的資料庫操作

### 用戶體驗
- 提供清晰的幫助信息
- 錯誤訊息友好且具體
- 支持多種輸出格式
- 命令執行速度快 (< 2秒)

## 實施計劃

### 第一步: 修復認證功能 (1-2天)
- 修復模組導入問題
- 實現資料庫整合
- 測試認證流程

### 第二步: 實現用戶管理 (2-3天)
- 實現 user list 功能
- 實現 user create 功能
- 實現 user show 功能
- 添加輸出格式支持

### 第三步: 實現需求單管理 (3-4天)
- 實現 requirement list 功能
- 實現 requirement create 功能
- 實現 requirement show 功能
- 實現狀態更新功能

### 第四步: 實現管理員功能 (2-3天)
- 實現統計功能
- 實現備份功能
- 實現預約管理
- 實現垃圾桶管理

### 第五步: 測試和優化 (1-2天)
- 完整功能測試
- 性能優化
- 文檔更新
- 錯誤處理完善

## 交付物
- 完整實現的 CLI 工具
- 更新的測試用例
- 更新的使用文檔
- 功能演示視頻（可選）

## 驗收標準
- 所有命令功能正常運行
- 與現有系統完全整合
- 輸出格式正確且一致
- 錯誤處理適當
- 性能符合要求
- 文檔完整且準確

## 優先級
高 - 這是 CLI 工具的核心功能實現

## 預計完成時間
7-10 個工作天

## 備註
- 此需求單是 REQ-CLI-001 的具體實施階段
- 需要與現有的 GUI 系統保持功能一致性
- 實現過程中如遇到技術問題，及時溝通解決
- 完成後需要進行完整的功能測試
        """.strip()
        
        # 設定優先級為緊急
        priority = "urgent"
        
        # 創建需求單
        req_id = create_requirement(
            conn=conn,
            title=title,
            description=description,
            assigner_id=admin_id,
            assignee_id=assignee_id,
            priority=priority,
            scheduled_time=None
        )
        
        if req_id:
            print(f"✅ 成功創建 CLI 功能實現需求單！")
            print(f"   需求單ID: {req_id}")
            print(f"   標題: {title}")
            print(f"   指派者: {admin_user[3]} (ID: {admin_id})")
            print(f"   接收者: {assignee_name} (ID: {assignee_id})")
            print(f"   優先級: 緊急")
            print(f"   狀態: 已發派")
            print(f"   創建時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return req_id
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
    print("🚀 開始創建 CLI 功能實現需求單...")
    print("=" * 60)
    
    # 檢查資料庫文件是否存在
    if not os.path.exists("users.db"):
        print("❌ 找不到資料庫文件 'users.db'")
        print("   請確保您在正確的專案目錄中運行此腳本")
        return
    
    # 創建需求單
    req_id = create_cli_implementation_requirement()
    
    print("=" * 60)
    if req_id:
        print("🎉 CLI 功能實現需求單創建成功！")
        print(f"\n📋 需求單編號: REQ-CLI-IMPL-{req_id:03d}")
        print("\n📝 接下來的工作:")
        print("1. 修復認證功能")
        print("2. 實現用戶管理功能")
        print("3. 實現需求單管理功能")
        print("4. 實現管理員功能")
        print("5. 測試和優化")
        print("\n💡 提示：")
        print("- 需求單已設為緊急優先級")
        print("- 預計完成時間：7-10 個工作天")
        print("- 請按照實施計劃逐步完成")
    else:
        print("❌ 需求單創建失敗")

if __name__ == "__main__":
    main() 