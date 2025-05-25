# 需求管理系統

這是一個使用 Python/Tkinter 開發的需求管理系統，允許管理員創建和分派需求單給員工，員工可以查看和回應他們收到的需求單。

## 系統特點

- 使用 Python 3.x 和 Tkinter 開發的現代化 GUI 應用
- 採用 SQLite 數據庫進行數據持久化存儲
- 支持多線程處理預約發派功能
- 完整的用戶權限管理系統
- 即時通知系統
- 響應式界面設計

## 主要功能

1. **管理員功能**:
   - 發派需求單給特定員工
   - 預約發派需求單
   - 查看所有已發派的需求單
   - 審核員工提交的需求單
   - 管理刪除的需求單
   - 查看系統通知
   - 管理員工帳號

2. **員工功能**:
   - 查看收到的需求單
   - 提交完成的需求單
   - 查看需求單的詳細信息
   - 查看個人工作統計

## 技術架構

### 前端
- Tkinter GUI 框架
- ttk 主題化組件
- 自定義樣式和布局

### 後端
- Python 3.x
- SQLite3 數據庫
- 多線程處理
- 事件驅動架構

### 數據庫設計
- users 表：用戶管理
- requirements 表：需求單管理
- scheduled_requirements 表：預約發派管理

## 安裝和運行

### 系統需求
- Python 3.x
- SQLite3
- Tkinter (通常隨 Python 一起安裝)

### 安裝步驟
```bash
# 克隆專案
git clone [專案地址]

# 進入專案目錄
cd requirement-management-system

# 安裝依賴
pip install -r requirements.txt

# 運行程序
python main.py
```

## 預設用戶
- 管理員: username=`nicholas`, password=`nicholas941013`
- 員工1: username=`user1`, password=`user123`
- 員工2: username=`staff1`, password=`staff123`
- 員工3: username=`staff2`, password=`staff123`

## 使用指南

### 管理員操作
1. 登入系統
2. 在需求管理界面可以：
   - 創建新需求單
   - 選擇立即發派或預約發派
   - 設定需求單優先級
   - 查看所有需求單狀態
   - 審核員工提交的需求單

### 員工操作
1. 登入系統
2. 在個人界面可以：
   - 查看分配給自己的需求單
   - 提交完成的需求單
   - 查看需求單詳情
   - 查看個人工作統計

## 系統維護

### 數據庫備份
系統使用 SQLite 數據庫，建議定期備份 `requirement.db` 文件。

### 日誌管理
系統運行日誌保存在程序運行目錄下，可用於故障排查。

## 最近更新

### 1. 無法刪除需求單問題
- 問題: 錯誤信息 "TypeError: 'User' object is not subscriptable"
- 原因: 在 `requirement_manager.py` 中錯誤地使用 `self.current_user[0]` 而不是 `self.current_user.id`
- 解決方案: 添加 `self.user_id` 屬性，並正確處理不同格式的用戶對象

### 2. 無法發派需求單給新註冊員工問題
- 問題: 員工下拉選單在界面初始化時只加載一次，沒有刷新機制
- 解決方案: 添加刷新按鈕和 `refresh_staff_list` 方法，允許管理員手動更新員工列表

### 3. 註冊員工無法查看自己收到的需求單問題
- 問題: 新註冊的員工登錄後無法看到分配給他們的需求單
- 原因: 用戶ID處理邏輯不完善，可能在某些情況下無法正確獲取用戶ID
- 解決方案:
  - 增強 `RequirementManager.__init__` 中用戶ID的獲取邏輯，支持多種格式的用戶對象
  - 在 `load_user_requirements` 和 `submit_requirement` 方法中添加用戶ID檢查
  - 在 `RequirementApp.setup_staff_interface` 中添加用戶對象有效性檢查
  - 改進沒有需求單時的提示顯示方式

## 開發者信息

### 專案結構
```
requirement-management-system/
├── main.py              # 主程序入口
├── requirement_manager.py # 需求管理核心邏輯
├── database.py          # 數據庫操作
├── auth.py             # 用戶認證
├── models.py           # 數據模型
├── registration/       # 註冊相關功能
├── requirement.db           # SQLite數據庫文件
└── schema.sql         # 數據庫結構定義
```

### 代碼規範
- 遵循 PEP 8 編碼規範
- 使用類型提示
- 完整的文檔字符串
- 模塊化設計

## 貢獻指南
1. Fork 專案
2. 創建特性分支
3. 提交更改
4. 發起 Pull Request

## 授權協議
MIT License 