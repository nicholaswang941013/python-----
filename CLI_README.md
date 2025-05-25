# 需求管理系統 CLI 工具使用指南

## 📖 概述

需求管理系統 CLI 工具 (`reqmgr`) 是一個命令行界面工具，為需求管理系統提供完整的命令行操作能力。您可以通過命令行進行用戶管理、需求單管理、認證等操作，非常適合自動化腳本、批量操作和遠程管理。

## 🚀 快速開始

### 系統需求
- Python 3.8+
- Windows/Linux/macOS

### 安裝依賴
```bash
# 安裝必要的依賴包
pip install -r requirements-cli.txt
```

### 驗證安裝
```bash
# 查看版本信息
python reqmgr.py --version

# 查看幫助信息
python reqmgr.py --help
```

## 📋 命令結構

### 基本語法
```bash
python reqmgr.py [全局選項] 命令組 子命令 [選項] [參數]
```

### 全局選項
| 選項 | 簡寫 | 說明 | 預設值 |
|------|------|------|--------|
| `--config` | `-c` | 指定配置文件路徑 | 自動搜索 |
| `--format` | `-f` | 輸出格式 (table/json/csv) | table |
| `--verbose` | `-v` | 詳細輸出 | false |
| `--quiet` | `-q` | 靜默模式 | false |
| `--version` | | 顯示版本信息 | |
| `--help` | `-h` | 顯示幫助信息 | |

## 🔐 認證命令 (auth)

認證命令組提供用戶登入、登出和會話管理功能。

### 可用命令
```bash
python reqmgr.py auth --help
```

#### 用戶登入
```bash
# 基本登入（會提示輸入密碼）
python reqmgr.py auth login -u nicholas

# 直接提供密碼登入
python reqmgr.py auth login -u nicholas -p nicholas941013

# 登入並保存會話（下次可自動登入）
python reqmgr.py auth login -u nicholas -p nicholas941013 --save-session
```

**選項說明:**
- `-u, --username`: 用戶名
- `-p, --password`: 密碼（可選，不提供會提示輸入）
- `--save-session`: 保存會話信息

#### 查看當前用戶
```bash
# 顯示當前登入的用戶信息
python reqmgr.py auth whoami
```

#### 用戶登出
```bash
# 登出並清除會話信息
python reqmgr.py auth logout
```

### 使用範例
```bash
# 完整的認證流程
python reqmgr.py auth login -u nicholas -p nicholas941013 --save-session
python reqmgr.py auth whoami
python reqmgr.py auth logout
```

## 👥 用戶管理命令 (user)

用戶管理命令組提供用戶的創建、查詢、更新等功能。

### 可用命令
```bash
python reqmgr.py user --help
```

#### 列出用戶
```bash
# 列出所有用戶
python reqmgr.py user list

# 以 JSON 格式顯示
python reqmgr.py --format json user list

# 以 CSV 格式顯示
python reqmgr.py --format csv user list
```

#### 創建用戶
```bash
# 創建新用戶
python reqmgr.py user create
```

### 使用範例
```bash
# 查看用戶列表（表格格式）
python reqmgr.py user list

# 查看用戶列表（JSON 格式）
python reqmgr.py --format json user list
```

## 📋 需求單管理命令 (requirement)

需求單管理命令組提供需求單的創建、查詢、提交等功能。

### 可用命令
```bash
python reqmgr.py requirement --help
```

#### 列出需求單
```bash
# 列出所有需求單
python reqmgr.py requirement list

# 以詳細模式顯示
python reqmgr.py --verbose requirement list

# 以 JSON 格式顯示
python reqmgr.py --format json requirement list
```

#### 創建需求單
```bash
# 創建新需求單
python reqmgr.py requirement create
```

### 使用範例
```bash
# 查看需求單列表
python reqmgr.py requirement list

# 創建新需求單
python reqmgr.py requirement create
```

## 👑 管理員命令 (admin)

管理員命令組提供系統管理員專用的功能。

### 可用命令
```bash
python reqmgr.py admin --help
```

#### 系統統計
```bash
# 顯示系統統計信息
python reqmgr.py admin stats

# 以 JSON 格式顯示統計
python reqmgr.py --format json admin stats
```

#### 資料庫備份
```bash
# 備份資料庫
python reqmgr.py admin backup
```

### 使用範例
```bash
# 查看系統統計
python reqmgr.py admin stats

# 備份資料庫
python reqmgr.py admin backup
```

## 📊 輸出格式

CLI 工具支持多種輸出格式，適合不同的使用場景。

### 表格格式 (預設)
```bash
python reqmgr.py user list
```
適合人類閱讀，提供清晰的表格顯示。

### JSON 格式
```bash
python reqmgr.py --format json user list
```
適合程式處理和 API 整合。

### CSV 格式
```bash
python reqmgr.py --format csv user list
```
適合數據分析和 Excel 處理。

## 🔧 配置管理

### 配置文件搜索順序
1. 環境變量 `REQMGR_CONFIG` 指定的文件
2. 當前目錄的 `reqmgr.yaml` 或 `reqmgr.yml`
3. 用戶主目錄的 `~/.reqmgr/config.yaml`
4. 系統級配置文件 `/etc/reqmgr/config.yaml` (僅 Unix 系統)

### 環境變量覆蓋
- `REQMGR_DB_PATH`: 資料庫路徑
- `REQMGR_FORMAT`: 預設輸出格式
- `REQMGR_LOG_LEVEL`: 日誌級別

### 配置文件範例
```yaml
# reqmgr.yaml
database:
  path: "./requirement.db"

auth:
  session_timeout: 3600
  save_session: true

output:
  default_format: "table"
  max_rows: 50
  show_headers: true

logging:
  level: "INFO"
  file: null
```

## 💡 使用技巧

### 1. 組合使用全局選項
```bash
# 靜默模式 + JSON 格式，適合腳本使用
python reqmgr.py --quiet --format json user list

# 詳細模式，適合除錯
python reqmgr.py --verbose user list
```

### 2. 管道和重定向
```bash
# 將輸出保存到文件
python reqmgr.py --format json user list > users.json

# 與其他命令組合使用
python reqmgr.py --format csv user list | grep "admin"
```

### 3. 批量操作腳本範例
```bash
#!/bin/bash
# 批量操作腳本

# 登入
python reqmgr.py auth login -u admin -p password --save-session

# 獲取用戶列表
python reqmgr.py --format json user list > users.json

# 獲取需求單列表
python reqmgr.py --format json requirement list > requirements.json

# 登出
python reqmgr.py auth logout
```

## 🚨 錯誤處理

### 常見錯誤和解決方法

#### 1. 模組導入錯誤
```
ModuleNotFoundError: No module named 'click'
```
**解決方法**: 安裝依賴
```bash
pip install -r requirements-cli.txt
```

#### 2. 資料庫連接錯誤
```
錯誤: 無法連接到資料庫
```
**解決方法**: 確保資料庫文件存在且有適當權限

#### 3. 認證失敗
```
❌ 登入失敗
```
**解決方法**: 檢查用戶名和密碼是否正確

### 除錯模式
```bash
# 使用詳細模式獲得更多信息
python reqmgr.py --verbose auth login -u username
```

## 📚 進階使用

### 1. 自動化腳本整合
```python
#!/usr/bin/env python3
import subprocess
import json

# 執行 CLI 命令並獲取 JSON 輸出
result = subprocess.run([
    'python', 'reqmgr.py', 
    '--format', 'json', 
    'user', 'list'
], capture_output=True, text=True)

if result.returncode == 0:
    data = json.loads(result.stdout)
    print(f"找到 {data['total']} 個用戶")
```

### 2. 配置文件自定義
```bash
# 使用自定義配置文件
python reqmgr.py --config /path/to/custom-config.yaml user list
```

### 3. 會話管理
```bash
# 登入並保存會話
python reqmgr.py auth login -u admin -p password --save-session

# 後續命令會自動使用保存的會話
python reqmgr.py user list
python reqmgr.py requirement list

# 清除會話
python reqmgr.py auth logout
```

## 🔄 開發狀態

### 當前版本: v0.1.0

#### ✅ 已實現功能
- CLI 框架和命令結構
- 配置管理系統
- 會話管理系統
- 多種輸出格式支持
- 完整的幫助系統

#### 🔄 開發中功能
- 認證功能實現
- 用戶管理 CRUD 操作
- 需求單管理功能
- 管理員統計功能

#### ⏳ 計劃功能
- 批量操作支持
- 模板系統
- 插件系統
- 完整的測試套件

## 🆘 獲得幫助

### 內建幫助
```bash
# 主要幫助
python reqmgr.py --help

# 特定命令幫助
python reqmgr.py auth --help
python reqmgr.py user --help
python reqmgr.py requirement --help
python reqmgr.py admin --help

# 子命令幫助
python reqmgr.py auth login --help
```

### 版本信息
```bash
python reqmgr.py --version
```

### 問題回報
如果遇到問題，請提供以下信息：
1. 使用的命令
2. 錯誤訊息
3. 系統環境 (OS, Python 版本)
4. 使用 `--verbose` 選項的詳細輸出

## 📄 許可證

本專案遵循 MIT 許可證。

---

**注意**: 這是一個開發中的工具，部分功能可能尚未完全實現。請參考開發狀態部分了解當前可用的功能。 