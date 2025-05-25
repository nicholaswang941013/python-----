BEGIN TRANSACTION;
CREATE TABLE requirements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT NOT NULL,
                        assigner_id INTEGER NOT NULL,
                        assignee_id INTEGER NOT NULL,
                        status TEXT NOT NULL DEFAULT 'pending',
                        priority TEXT NOT NULL DEFAULT 'normal',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        scheduled_time TIMESTAMP,
                        is_dispatched INTEGER DEFAULT 1,
                        completed_at TIMESTAMP,
                        comment TEXT,
                        is_deleted INTEGER DEFAULT 0,
                        deleted_at TIMESTAMP,
                        FOREIGN KEY (assigner_id) REFERENCES users (id),
                        FOREIGN KEY (assignee_id) REFERENCES users (id)
                    );
INSERT INTO "requirements" VALUES(10,'測試','測試',1,6,'pending','normal','2025-05-19 10:49:14',NULL,1,NULL,NULL,0,NULL);
INSERT INTO "requirements" VALUES(11,'測試定時','測試定時',1,6,'pending','normal','2025-05-19 19:40:38','2025-05-19 19:40:00',1,NULL,NULL,0,NULL);
INSERT INTO "requirements" VALUES(12,'開發需求管理系統 CLI 工具','## 需求概述
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
參考文檔：CLI_DESIGN.md, CLI_REQUIREMENT.md',1,2,'pending','urgent','2025-05-25 08:04:58',NULL,1,NULL,NULL,0,NULL);
INSERT INTO "requirements" VALUES(13,'實現 CLI 工具核心功能','## 需求概述
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
- 完成後需要進行完整的功能測試',1,2,'completed','urgent','2025-05-25 08:38:00',NULL,1,'2025-05-25 16:46:07','CLI工具核心功能已實現完成',0,NULL);
INSERT INTO "requirements" VALUES(14,'CLI測試需求','測試CLI工具的需求單創建功能',1,2,'reviewing','normal','2025-05-25 08:44:06',NULL,1,'2025-05-25 16:45:24','CLI測試需求已完成，功能正常運行',0,NULL);
CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        role TEXT NOT NULL DEFAULT 'staff'
                    );
INSERT INTO "users" VALUES(1,'nicholas','nicholas941013','王爺','yuxiangwang57@gmail.com','admin');
INSERT INTO "users" VALUES(2,'user1','user123','張三','user1@example.com','staff');
INSERT INTO "users" VALUES(3,'staff1','staff123','李四','staff1@example.com','staff');
INSERT INTO "users" VALUES(4,'staff2','staff123','王五','staff2@example.com','staff');
INSERT INTO "users" VALUES(6,'test','test123','助理','abc@gmail.com','admin');
INSERT INTO "users" VALUES(7,'testuser','password123','測試用戶','test@example.com','staff');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('users',7);
INSERT INTO "sqlite_sequence" VALUES('requirements',14);
COMMIT;
