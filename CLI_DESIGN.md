# 需求管理系統 CLI 工具設計文檔

## 概述

本文檔描述了需求管理系統的命令行界面（CLI）工具設計，該工具將提供與現有 GUI 應用程序相同的功能，但通過命令行操作，適合自動化腳本、批量操作和遠程管理。

## 設計目標

1. **功能完整性**：提供與 GUI 版本相同的所有核心功能
2. **易用性**：直觀的命令結構和清晰的輸出格式
3. **可擴展性**：模塊化設計，便於添加新功能
4. **自動化友好**：支持腳本化操作和批量處理
5. **安全性**：適當的身份驗證和權限控制

## 技術架構

### 核心組件
- **CLI 框架**：使用 `argparse` 或 `click` 庫
- **數據庫層**：重用現有的 `database.py` 模組
- **認證模組**：重用現有的 `auth.py` 模組
- **配置管理**：支持配置文件和環境變量
- **輸出格式化**：支持表格、JSON、CSV 等多種輸出格式

### 項目結構
```
cli/
├── __init__.py
├── main.py              # CLI 主入口
├── commands/            # 命令模組
│   ├── __init__.py
│   ├── auth.py         # 認證相關命令
│   ├── user.py         # 用戶管理命令
│   ├── requirement.py  # 需求單管理命令
│   └── admin.py        # 管理員專用命令
├── utils/              # 工具模組
│   ├── __init__.py
│   ├── config.py       # 配置管理
│   ├── formatter.py    # 輸出格式化
│   └── session.py      # 會話管理
└── tests/              # 測試文件
    ├── __init__.py
    └── test_cli.py
```

## 命令結構設計

### 主命令
```bash
reqmgr [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS] [ARGS]
```

### 全局選項
- `--config, -c`：指定配置文件路徑
- `--format, -f`：輸出格式 (table, json, csv)
- `--verbose, -v`：詳細輸出
- `--quiet, -q`：靜默模式
- `--help, -h`：顯示幫助信息

## 命令分類

### 1. 認證命令 (auth)

#### 登入
```bash
reqmgr auth login [OPTIONS]
```
**選項：**
- `--username, -u`：用戶名
- `--password, -p`：密碼
- `--save-session`：保存會話信息

**範例：**
```bash
reqmgr auth login -u nicholas -p nicholas941013
reqmgr auth login --save-session
```

#### 登出
```bash
reqmgr auth logout
```

#### 查看當前用戶
```bash
reqmgr auth whoami
```

### 2. 用戶管理命令 (user)

#### 列出用戶
```bash
reqmgr user list [OPTIONS]
```
**選項：**
- `--role`：按角色篩選 (admin, staff)
- `--active`：只顯示活躍用戶

#### 創建用戶
```bash
reqmgr user create [OPTIONS]
```
**選項：**
- `--username, -u`：用戶名（必需）
- `--password, -p`：密碼（必需）
- `--name, -n`：真實姓名（必需）
- `--email, -e`：電子郵件（必需）
- `--role, -r`：角色 (admin, staff)

**範例：**
```bash
reqmgr user create -u newuser -p password123 -n "新用戶" -e newuser@example.com -r staff
```

#### 查看用戶詳情
```bash
reqmgr user show USER_ID
```

#### 更新用戶信息
```bash
reqmgr user update USER_ID [OPTIONS]
```

### 3. 需求單管理命令 (requirement)

#### 創建需求單
```bash
reqmgr requirement create [OPTIONS]
```
**選項：**
- `--title, -t`：標題（必需）
- `--description, -d`：描述（必需）
- `--assignee, -a`：指派給的用戶ID或用戶名（必需）
- `--priority, -p`：優先級 (normal, urgent)
- `--schedule, -s`：預約發派時間 (YYYY-MM-DD HH:MM)

**範例：**
```bash
reqmgr requirement create -t "系統維護" -d "進行服務器維護" -a user1 -p urgent
reqmgr requirement create -t "報告撰寫" -d "撰寫月度報告" -a 2 -s "2024-01-15 09:00"
```

#### 列出需求單
```bash
reqmgr requirement list [OPTIONS]
```
**選項：**
- `--status`：按狀態篩選 (pending, reviewing, completed, invalid)
- `--assignee`：按指派對象篩選
- `--priority`：按優先級篩選
- `--limit, -l`：限制顯示數量
- `--mine`：只顯示分配給當前用戶的需求單

#### 查看需求單詳情
```bash
reqmgr requirement show REQUIREMENT_ID
```

#### 提交需求單
```bash
reqmgr requirement submit REQUIREMENT_ID [OPTIONS]
```
**選項：**
- `--comment, -c`：完成說明

**範例：**
```bash
reqmgr requirement submit 123 -c "任務已完成，所有測試通過"
```

#### 審核需求單
```bash
reqmgr requirement review REQUIREMENT_ID ACTION [OPTIONS]
```
**動作：**
- `approve`：批准
- `reject`：拒絕
- `invalidate`：使失效

**範例：**
```bash
reqmgr requirement review 123 approve
reqmgr requirement review 124 reject
```

### 4. 管理員專用命令 (admin)

#### 查看系統統計
```bash
reqmgr admin stats [OPTIONS]
```
**選項：**
- `--period`：統計期間 (today, week, month, year)

#### 預約發派管理
```bash
reqmgr admin scheduled [SUBCOMMAND]
```
**子命令：**
- `list`：列出預約發派的需求單
- `cancel REQUIREMENT_ID`：取消預約發派

#### 垃圾桶管理
```bash
reqmgr admin trash [SUBCOMMAND]
```
**子命令：**
- `list`：列出已刪除的需求單
- `restore REQUIREMENT_ID`：恢復需求單
- `empty`：清空垃圾桶

#### 數據庫維護
```bash
reqmgr admin db [SUBCOMMAND]
```
**子命令：**
- `backup`：備份數據庫
- `restore FILE`：恢復數據庫
- `cleanup`：清理過期數據

## 輸出格式

### 表格格式 (預設)
```
ID  | 標題        | 狀態      | 優先級 | 指派對象 | 創建時間
----|------------|----------|--------|----------|------------------
1   | 系統維護    | pending  | urgent | 張三     | 2024-01-10 09:00
2   | 報告撰寫    | reviewing| normal | 李四     | 2024-01-09 14:30
```

### JSON 格式
```json
{
  "requirements": [
    {
      "id": 1,
      "title": "系統維護",
      "status": "pending",
      "priority": "urgent",
      "assignee": "張三",
      "created_at": "2024-01-10 09:00:00"
    }
  ],
  "total": 1
}
```

### CSV 格式
```csv
id,title,status,priority,assignee,created_at
1,系統維護,pending,urgent,張三,2024-01-10 09:00:00
```

## 配置管理

### 配置文件位置
- 系統級：`/etc/reqmgr/config.yaml`
- 用戶級：`~/.reqmgr/config.yaml`
- 項目級：`./reqmgr.yaml`

### 配置文件格式
```yaml
database:
  path: "./users.db"
  
auth:
  session_timeout: 3600
  save_session: true
  
output:
  default_format: "table"
  max_rows: 50
  
logging:
  level: "INFO"
  file: "~/.reqmgr/logs/cli.log"
```

### 環境變量
- `REQMGR_CONFIG`：配置文件路徑
- `REQMGR_DB_PATH`：數據庫路徑
- `REQMGR_FORMAT`：預設輸出格式

## 會話管理

### 會話存儲
- 位置：`~/.reqmgr/session`
- 格式：加密的 JSON 文件
- 內容：用戶ID、角色、登入時間、過期時間

### 自動登入
```bash
# 保存會話
reqmgr auth login --save-session

# 後續命令自動使用保存的會話
reqmgr requirement list
```

## 錯誤處理

### 錯誤代碼
- `0`：成功
- `1`：一般錯誤
- `2`：認證失敗
- `3`：權限不足
- `4`：資源不存在
- `5`：數據庫錯誤

### 錯誤輸出格式
```json
{
  "error": {
    "code": 2,
    "message": "認證失敗：用戶名或密碼錯誤",
    "details": "請檢查您的登入憑證"
  }
}
```

## 安全考慮

1. **密碼處理**：
   - 支持從標準輸入讀取密碼
   - 不在命令歷史中保存密碼
   - 支持密碼文件

2. **會話安全**：
   - 會話文件加密存儲
   - 自動過期機制
   - 安全的會話清理

3. **權限控制**：
   - 嚴格的角色權限檢查
   - 操作日誌記錄

## 批量操作支持

### 批量創建需求單
```bash
reqmgr requirement batch-create --file requirements.csv
```

### 批量更新狀態
```bash
reqmgr requirement batch-update --ids 1,2,3 --status completed
```

### 從模板創建
```bash
reqmgr requirement create --template maintenance.yaml
```

## 插件系統

### 插件接口
```python
class CLIPlugin:
    def register_commands(self, parser):
        """註冊命令"""
        pass
    
    def execute(self, args):
        """執行命令"""
        pass
```

### 插件目錄
- `~/.reqmgr/plugins/`
- 支持 Python 模組和可執行文件

## 測試策略

### 單元測試
- 每個命令模組的獨立測試
- 模擬數據庫操作
- 輸出格式驗證

### 集成測試
- 端到端命令執行測試
- 真實數據庫操作測試
- 會話管理測試

### 性能測試
- 大量數據處理性能
- 並發操作測試

## 部署和分發

### 安裝方式
```bash
# 從源碼安裝
pip install -e .

# 從 PyPI 安裝
pip install reqmgr-cli

# 獨立可執行文件
./reqmgr-cli-linux-x64
```

### 打包格式
- Python wheel 包
- 獨立可執行文件 (PyInstaller)
- Docker 鏡像

## 文檔和幫助

### 內建幫助
```bash
reqmgr --help
reqmgr requirement --help
reqmgr requirement create --help
```

### 手冊頁面
```bash
man reqmgr
```

### 在線文檔
- 完整的 API 文檔
- 使用範例
- 最佳實踐指南

## 未來擴展

1. **API 集成**：支持 REST API 操作
2. **多數據庫支持**：MySQL、PostgreSQL
3. **雲端同步**：支持雲端數據庫
4. **通知系統**：郵件、Slack 通知
5. **報表生成**：PDF、Excel 報表
6. **工作流程**：自定義審批流程

## 實施計劃

### 第一階段（基礎功能）
- [ ] CLI 框架搭建
- [ ] 基本認證功能
- [ ] 需求單 CRUD 操作
- [ ] 基本輸出格式

### 第二階段（進階功能）
- [ ] 管理員功能
- [ ] 批量操作
- [ ] 配置管理
- [ ] 會話管理

### 第三階段（完善功能）
- [ ] 插件系統
- [ ] 高級輸出格式
- [ ] 性能優化
- [ ] 完整測試覆蓋

### 第四階段（擴展功能）
- [ ] API 集成
- [ ] 通知系統
- [ ] 報表功能
- [ ] 工作流程

## 結論

這個 CLI 工具設計旨在提供一個功能完整、易於使用且可擴展的命令行界面，使用戶能夠高效地管理需求單系統。通過模塊化設計和標準化的命令結構，該工具將成為需求管理系統的重要補充，特別適合自動化和批量操作場景。 