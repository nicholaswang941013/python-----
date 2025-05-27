# Requirement Management System 需求管理系統

一套以 Python/Tkinter 開發，支援多用戶、權限控管、需求單分派與追蹤的現代化需求管理系統，適用於中小企業或團隊。

專案倉庫：[https://github.com/nicholaswang941013/python-project](https://github.com/nicholaswang941013/python-project)

---

## 目錄
- [專案簡介](#專案簡介)
- [系統特點](#系統特點)
- [主要功能](#主要功能)
- [技術架構](#技術架構)
- [專案結構](#專案結構)
- [安裝與執行](#安裝與執行)
- [依賴說明](#依賴說明)
- [預設用戶](#預設用戶)
- [使用指南](#使用指南)
- [測試方式](#測試方式)
- [系統維護](#系統維護)
- [常見問題](#常見問題)
- [最近更新](#最近更新)
- [貢獻指南](#貢獻指南)
- [授權協議](#授權協議)

---

## 專案簡介
本系統提供管理員與員工兩種角色，支援需求單的建立、分派、追蹤、審核與統計，並具備即時通知與多線程處理能力。

## 系統特點
- Python 3.x + Tkinter GUI
- SQLite3 資料庫持久化
- 多線程預約發派
- 權限分級管理
- 即時通知
- CLI 與 GUI 雙模式（如有 CLI）
- 易於擴充與維護

## 主要功能
### 管理員
- 發派/預約需求單給員工
- 查看/審核/刪除需求單
- 員工帳號管理
- 系統通知

### 員工
- 查看/回應/提交需求單
- 查看個人工作統計

## 技術架構
- 前端：Tkinter、ttk、自定義樣式
- 後端：Python 3.x、SQLite3、多線程、事件驅動
- 數據庫：users、requirements、scheduled_requirements

## 專案結構
```
requirement-management-system/
├── main.py                  # 主程序入口 (GUI)
├── requirement_manager.py   # 需求管理核心邏輯
├── database.py              # 資料庫操作
├── auth.py                  # 用戶認證
├── models.py                # 數據模型
├── registration/            # 註冊功能模組
├── cli/                     # CLI 介面與指令
│   ├── main.py              # CLI 入口
│   └── commands/            # CLI 指令模組
├── utils/                   # 工具模組
├── requirement.db           # SQLite 資料庫
├── schema.sql               # 資料庫結構定義
├── requirements.txt         # 依賴套件清單
└── README.md                # 說明文件
```

## 安裝與執行
### 系統需求
- Python 3.8 以上
- SQLite3
- Tkinter（Python 內建）

### 安裝步驟
```bash
# 克隆專案
git clone https://github.com/nicholaswang941013/python-project.git

# 進入專案目錄
cd python-project

# 安裝依賴
pip install -r requirements.txt

# 啟動 GUI
python main.py

# 啟動 CLI（如有）
python cli/main.py
```

## 依賴說明
- Python 3.8+
- tkinter
- sqlite3
- 其他依賴請參考 requirements.txt

## 預設用戶
| 角色   | 帳號         | 密碼           |
|--------|--------------|----------------|
| 管理員 | nicholas     | nicholas941013 |
| 員工1  | user1        | user123        |
| 員工2  | staff1       | staff123       |
| 員工3  | staff2       | staff123       |

## 使用指南
### 管理員
1. 登入系統
2. 進入需求管理介面，創建/發派/預約需求單
3. 查看需求單狀態、審核員工提交
4. 管理員工帳號與系統通知

### 員工
1. 登入系統
2. 查看分配需求單、提交完成、查看統計

## 測試方式
- 若有自動化測試：
```bash
pytest
```
- 或手動測試 GUI/CLI 功能

## 系統維護
- 資料庫備份：定期備份 `requirement.db`
- 日誌管理：運行日誌保存在程式目錄下

## 常見問題
- 啟動失敗：請確認 Python 版本與依賴已安裝
- GUI 無法顯示：請確認 Tkinter 已安裝
- 權限問題：請用管理員帳號登入

## 最近更新
- 修正需求單刪除、分派、員工查詢等問題，詳見下方更新紀錄

## 貢獻指南
1. Fork 專案
2. 創建特性分支
3. 提交更改
4. 發起 Pull Request

## 授權協議
MIT License

---

> 本專案由 [yourname] 維護，歡迎貢獻與反饋。