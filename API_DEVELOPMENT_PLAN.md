# Requirement Management System API 開發計畫

## 專案概述

為現有的需求管理系統開發一套完整的 REST API，提供外部系統整合能力，使第三方應用可以透過標準的 HTTP 請求存取系統資料。

**專案倉庫**：[https://github.com/nicholaswang941013/python-project](https://github.com/nicholaswang941013/python-project)  
**分支**：`feature/api-development`  
**開發期程**：預計 4-6 週  

---

## 目錄
- [專案概述](#專案概述)
- [API 設計原則](#api-設計原則)
- [技術架構](#技術架構)
- [資料庫分析](#資料庫分析)
- [API 端點設計](#api-端點設計)
- [認證與授權](#認證與授權)
- [開發階段](#開發階段)
- [技術規格](#技術規格)
- [專案結構](#專案結構)
- [測試策略](#測試策略)
- [部署與監控](#部署與監控)
- [風險評估](#風險評估)
- [驗收標準](#驗收標準)

---

## API 設計原則

### 設計哲學
- **RESTful 設計**：遵循 REST 架構風格
- **資源導向**：以資源為核心的 URL 設計
- **版本控制**：支援 API 版本管理
- **統一回應格式**：標準化的 JSON 回應結構
- **錯誤處理**：明確的錯誤碼與訊息
- **安全性優先**：完整的認證與授權機制

### 核心特色
- 🔐 JWT Token 認證
- 📊 RESTful API 設計
- 🛡️ 權限分級控制
- 📝 Swagger 文檔自動生成
- ⚡ 快速回應與快取機制
- 🔄 版本管理支援
- 📈 API 使用統計與監控

---

## 技術架構

### 後端框架
- **主框架**：Flask (輕量級、靈活)
- **資料庫**：SQLite3 (現有資料庫)
- **ORM**：無 (直接使用現有 database.py)
- **認證**：Flask-JWT-Extended
- **文檔**：Flask-RESTX (Swagger)
- **CORS**：Flask-CORS

### 核心套件
```txt
Flask==2.3.3
Flask-JWT-Extended==4.5.3
Flask-RESTX==1.2.0
Flask-CORS==4.0.0
python-dotenv==1.0.0
```

### 回應格式標準
```json
{
  "success": true,
  "message": "操作成功",
  "data": {...},
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "v1"
}
```

---

## 資料庫分析

### 現有資料表結構

#### users 表
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 用戶ID |
| username | TEXT UNIQUE | 用戶名稱 |
| password | TEXT | 密碼 |
| name | TEXT | 真實姓名 |
| email | TEXT | 電子郵件 |
| role | TEXT | 角色 (admin/staff) |

#### requirements 表
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 需求單ID |
| title | TEXT | 標題 |
| description | TEXT | 描述 |
| assigner_id | INTEGER | 指派者ID |
| assignee_id | INTEGER | 接收者ID |
| status | TEXT | 狀態 |
| priority | TEXT | 優先級 |
| created_at | TIMESTAMP | 建立時間 |
| scheduled_time | TIMESTAMP | 預約時間 |
| is_dispatched | INTEGER | 是否已發派 |
| completed_at | TIMESTAMP | 完成時間 |
| comment | TEXT | 備註 |
| is_deleted | INTEGER | 是否已刪除 |
| deleted_at | TIMESTAMP | 刪除時間 |

### 資料關聯
- users.id → requirements.assigner_id (一對多)
- users.id → requirements.assignee_id (一對多)

---

## API 端點設計

### 基礎 URL
```
http://localhost:5000/api/v1
```

### 1. 認證模組 (/auth)

#### POST /auth/login
**登入取得 JWT Token**
```json
Request:
{
  "username": "nicholas",
  "password": "nicholas941013"
}

Response:
{
  "success": true,
  "message": "登入成功",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
      "id": 1,
      "username": "nicholas",
      "name": "王爺",
      "email": "yuxiangwang57@gmail.com",
      "role": "admin"
    }
  }
}
```

#### POST /auth/refresh
**刷新 Token**

#### POST /auth/logout
**登出**

#### GET /auth/profile
**取得當前用戶資料**

### 2. 用戶管理模組 (/users)

#### GET /users
**取得用戶列表** (限管理員)
- Query Parameters: `role`, `page`, `limit`

#### GET /users/{user_id}
**取得特定用戶資料**

#### POST /users
**建立新用戶** (限管理員)
```json
Request:
{
  "username": "newuser",
  "password": "password123",
  "name": "新用戶",
  "email": "newuser@example.com",
  "role": "staff"
}
```

#### PUT /users/{user_id}
**更新用戶資料**

#### DELETE /users/{user_id}
**刪除用戶** (限管理員)

### 3. 需求單管理模組 (/requirements)

#### GET /requirements
**取得需求單列表**
- Query Parameters: `status`, `priority`, `assignee_id`, `page`, `limit`
- 管理員：可查看所有需求單
- 員工：只能查看分配給自己的需求單

#### GET /requirements/{req_id}
**取得特定需求單詳情**

#### POST /requirements
**建立新需求單** (限管理員)
```json
Request:
{
  "title": "系統更新需求",
  "description": "更新用戶介面",
  "assignee_id": 2,
  "priority": "normal",
  "scheduled_time": "2024-01-20T09:00:00Z"
}
```

#### PUT /requirements/{req_id}
**更新需求單**

#### DELETE /requirements/{req_id}
**軟刪除需求單** (限管理員)

#### POST /requirements/{req_id}/submit
**提交需求單** (限員工)
```json
Request:
{
  "comment": "已完成系統更新"
}
```

#### POST /requirements/{req_id}/approve
**審核通過需求單** (限管理員)

#### POST /requirements/{req_id}/reject
**審核拒絕需求單** (限管理員)

#### POST /requirements/{req_id}/restore
**恢復已刪除需求單** (限管理員)

### 4. 統計與報表模組 (/statistics)

#### GET /statistics/overview
**系統概覽統計**
```json
Response:
{
  "success": true,
  "data": {
    "total_users": 15,
    "total_requirements": 128,
    "pending_requirements": 25,
    "completed_requirements": 98,
    "urgent_requirements": 5
  }
}
```

#### GET /statistics/users/{user_id}
**用戶工作統計**

#### GET /statistics/requirements
**需求單統計分析**
- Query Parameters: `period` (day/week/month/year)

### 5. 管理員專用模組 (/admin)

#### GET /admin/scheduled
**取得預約需求單列表**

#### POST /admin/dispatch
**手動觸發預約發派**

#### GET /admin/trash
**取得回收站需求單**

#### POST /admin/cleanup
**清空回收站**

#### GET /admin/logs
**取得系統日誌**

---

## 認證與授權

### JWT Token 設計
- **Header**: 包含 token 類型與加密算法
- **Payload**: 包含用戶 ID、角色、過期時間
- **Signature**: 使用密鑰簽名確保完整性

### 權限分級
1. **公開端點**: 不需認證
   - POST /auth/login
   - API 文檔頁面

2. **用戶端點**: 需要有效 Token
   - GET /auth/profile
   - GET/PUT /users/{自己的ID}
   - 自己的需求單相關操作

3. **管理員端點**: 需要管理員權限
   - 用戶管理相關
   - 所有需求單管理
   - 統計報表
   - 系統管理功能

### 安全機制
- 密碼加密存儲
- Token 自動過期 (2小時)
- Refresh Token 機制
- CORS 設定
- 請求頻率限制
- SQL 注入防護

---

## 開發階段

### 第一階段：基礎架構 (週 1-2)
- [x] 建立開發分支
- [ ] Flask 應用初始化
- [ ] 資料庫連接與模型建立
- [ ] JWT 認證系統
- [ ] 基礎 API 結構
- [ ] Swagger 文檔設定
- [ ] 基礎測試框架

**交付物**：
- API 基礎架構
- 認證系統
- Swagger 文檔頁面

### 第二階段：核心功能 (週 2-3)
- [ ] 用戶管理 API
- [ ] 需求單 CRUD API
- [ ] 權限控制實作
- [ ] 錯誤處理機制
- [ ] 資料驗證

**交付物**：
- 完整的用戶與需求單 API
- 權限控制系統
- 單元測試

### 第三階段：進階功能 (週 3-4)
- [ ] 統計報表 API
- [ ] 管理員專用功能
- [ ] 預約發派系統
- [ ] 批量操作 API
- [ ] API 使用監控

**交付物**：
- 統計與報表功能
- 管理員功能模組
- 監控儀表板

### 第四階段：優化與部署 (週 4-6)
- [ ] 性能優化
- [ ] 快取機制
- [ ] API 文檔完善
- [ ] 整合測試
- [ ] 部署準備

**交付物**：
- 完整的 API 系統
- 部署文檔
- 使用指南

---

## 技術規格

### 性能需求
- **回應時間**: < 200ms (標準請求)
- **並發用戶**: 支援 100+ 同時連線
- **資料量**: 支援 10,000+ 需求單
- **可用性**: 99.9% 運行時間

### 相容性需求
- **Python 版本**: 3.8+
- **瀏覽器**: Chrome 90+, Firefox 88+, Safari 14+
- **API 客戶端**: 支援標準 HTTP 請求庫

### 安全需求
- JWT Token 加密
- HTTPS 傳輸 (生產環境)
- SQL 注入防護
- XSS 攻擊防護
- CSRF 保護

---

## 專案結構

```
api/
├── app.py                    # Flask 應用入口
├── config.py                 # 配置設定
├── requirements-api.txt      # API 依賴套件
├── models/                   # 資料模型
│   ├── __init__.py
│   ├── user.py              # 用戶模型
│   └── requirement.py       # 需求單模型
├── resources/               # API 資源 (端點)
│   ├── __init__.py
│   ├── auth.py              # 認證相關 API
│   ├── users.py             # 用戶管理 API
│   ├── requirements.py      # 需求單管理 API
│   ├── statistics.py        # 統計報表 API
│   └── admin.py             # 管理員專用 API
├── utils/                   # 工具模組
│   ├── __init__.py
│   ├── decorators.py        # 裝飾器 (權限檢查等)
│   ├── validators.py        # 資料驗證
│   ├── helpers.py           # 輔助函數
│   └── database.py          # 資料庫操作 (使用現有)
├── tests/                   # 測試檔案
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_requirements.py
│   └── test_admin.py
├── docs/                    # 文檔
│   ├── API_USAGE.md         # API 使用指南
│   └── DEPLOYMENT.md        # 部署指南
└── .env.example             # 環境變數範例
```

---

## 測試策略

### 測試類型
1. **單元測試**: 每個 API 端點
2. **整合測試**: 完整業務流程
3. **性能測試**: 負載與壓力測試
4. **安全測試**: 認證與授權

### 測試工具
- **pytest**: 測試框架
- **pytest-flask**: Flask 測試支援
- **coverage**: 程式碼覆蓋率
- **postman**: API 功能測試

### 測試指令
```bash
# 執行所有測試
pytest

# 執行特定測試
pytest tests/test_auth.py

# 檢查覆蓋率
pytest --cov=api

# 執行性能測試
pytest tests/test_performance.py
```

---

## 部署與監控

### 本地開發
```bash
# 安裝依賴
pip install -r requirements-api.txt

# 設定環境變數
cp .env.example .env

# 啟動開發伺服器
python app.py
```

### 生產部署
- **WSGI 伺服器**: Gunicorn
- **反向代理**: Nginx
- **HTTPS**: Let's Encrypt
- **監控**: Flask-Monitor

### 監控指標
- API 請求數量與回應時間
- 錯誤率統計
- 系統資源使用率
- 用戶活躍度統計

---

## 風險評估

### 技術風險
| 風險 | 可能性 | 影響度 | 緩解措施 |
|------|--------|--------|----------|
| 資料庫效能問題 | 中 | 高 | 索引優化、查詢最佳化 |
| Token 安全性 | 低 | 高 | 強化加密、定期更新密鑰 |
| 併發處理問題 | 中 | 中 | 連接池、鎖機制 |

### 專案風險
| 風險 | 可能性 | 影響度 | 緩解措施 |
|------|--------|--------|----------|
| 開發時程延遲 | 中 | 中 | 分階段交付、優先級排序 |
| 需求變更 | 低 | 中 | 彈性架構設計 |
| 整合問題 | 低 | 高 | 早期整合測試 |

---

## 驗收標準

### 功能驗收
- [ ] 所有 API 端點正常運作
- [ ] 認證與授權機制完整
- [ ] 資料驗證與錯誤處理
- [ ] Swagger 文檔完整

### 性能驗收
- [ ] API 回應時間 < 200ms
- [ ] 支援 100+ 併發用戶
- [ ] 系統穩定運行 24 小時

### 安全驗收
- [ ] JWT Token 安全機制
- [ ] SQL 注入防護測試
- [ ] 權限控制驗證

### 文檔驗收
- [ ] API 使用指南
- [ ] 部署文檔
- [ ] 開發者文檔

---

## 總結

本計畫將為需求管理系統建立一套完整的 REST API，提供：

1. **標準化介面**: RESTful API 設計
2. **安全性**: JWT 認證與權限控制
3. **可擴展性**: 模組化架構設計
4. **文檔完整**: Swagger 自動文檔
5. **測試覆蓋**: 完整的測試策略

預計開發期程 4-6 週，分四個階段逐步交付，確保專案品質與進度控制。

---

**專案負責人**: [Your Name]  
**建立日期**: 2024-01-15  
**最後更新**: 2024-01-15  
**版本**: v1.0  

> 如有任何問題或建議，請聯繫開發團隊。 