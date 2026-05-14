# 部署指南 | Deployment Guide

## 🚀 快速部署 (5 分鐘)

### 第一步：建立 GitHub 帳號（如果還沒有）
1. 訪問 https://github.com/signup
2. 建立帳號並驗證郵箱

### 第二步：建立新的 GitHub 倉庫

1. 登入 GitHub
2. 點擊右上角 **"+"** → **"New repository"**
3. 填寫資訊：
   - **Repository name**: `steel-prices-streamlit`
   - **Description**: International Metal Prices Tracker
   - **Public**: ✅ 選中（讓別人能訪問）
   - **Initialize with**: 不勾選（我們已有代碼）
4. 點擊 **"Create repository"**

### 第三步：推送代碼到 GitHub

在終端運行（替換 `yourusername` 為你的 GitHub 用戶名）：

```bash
cd steel-prices-streamlit

# 設定 Git 用戶資訊（首次使用）
git config user.email "your.email@example.com"
git config user.name "Your Name"

# 提交第一個版本
git commit -m "Initial commit: Metal Prices Tracker with Streamlit"

# 重命名分支為 main（如果需要）
git branch -M main

# 新增遠端倉庫
git remote add origin https://github.com/yourusername/steel-prices-streamlit.git

# 推送代碼
git push -u origin main
```

### 第四步：在 Streamlit Cloud 部署

1. 訪問 https://streamlit.io/cloud
2. 點擊 **"Sign in with GitHub"** 並授權
3. 點擊 **"New app"**
4. 填寫部署資訊：
   - **Repository**: `yourusername/steel-prices-streamlit`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. 點擊 **"Deploy"** → 等待 1-2 分鐘

### 第五步：分享應用鏈接

部署完成後，你會得到公開 URL (例如)：
```
https://steel-prices-streamlit.streamlit.app
```

**分享這個鏈接給任何人，他們就能訪問你的應用！** 🎉

### 可選：設定真實鋼價 API Key

如果要啟用 Trading Economics 的 Steel HRC / 工業金屬資料：

1. 到 Streamlit Cloud 應用的 **Settings → Secrets**
2. 加入：

```toml
TRADING_ECONOMICS_API_KEY = "your_api_key_here"
```

3. 儲存後重新部署或重啟應用

---

## 📝 本地開發 (可選)

如果你想在本地測試修改：

```bash
# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt

# 執行應用
streamlit run app.py
```

應用會在 http://localhost:8501 打開

---

## 🔄 更新應用

每當你對代碼做修改：

```bash
# 1. 做修改...編輯任何 .py 文件

# 2. 提交並推送
git add .
git commit -m "描述你的修改"
git push origin main

# 3. Streamlit Cloud 會自動重新部署（1-2 分鐘）
```

---

## 🛠️ 常見問題

### Q: 部署失敗怎麼辦？
A: 
- 檢查 requirements.txt 是否在倉庫根目錄
- 查看 Streamlit Cloud 的部署日誌（Dashboard → 應用 → 日誌）
- 確保 app.py 在根目錄

### Q: 如何修改應用名稱？
A: Streamlit Cloud → 應用設定 → 修改名稱

### Q: 如何添加自定義域名？
A: Streamlit Cloud Pro plan（付費功能）

### Q: Database 文件會保留嗎？
A: 不會。Streamlit Cloud 會定期清理檔案系統。要持久化數據，考慮使用外部數據庫（如 Firebase）。

---

## 🚨 安全提示

⚠️ **不要提交敏感資訊:**
- API 密鑰
- 密碼
- 個人秘鑰

使用 `.env` 文件並添加到 `.gitignore`：

```bash
# .env 文件
API_KEY=your_secret_key

# config.py
import os
API_KEY = os.getenv('API_KEY')
```

在 Streamlit Cloud 中設置環境變數：
Secrets → 添加你的密鑰

---

## 需要幫助？

- Streamlit 文件: https://docs.streamlit.io
- Streamlit Cloud 文件: https://docs.streamlit.io/streamlit-enterprise/teams-and-organizations
- GitHub 文件: https://docs.github.com

祝部署順利！🚀
