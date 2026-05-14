# 金屬報價數據源指南

本應用已支援真實 API，會依序嘗試：

1. **Trading Economics**（需 API key，覆蓋 Steel、Iron Ore、Copper、Aluminum、Zinc、Nickel 等）
2. **Yahoo Finance futures**（免 key，使用 `yfinance`，可抓到 Steel HRC、Iron Ore、Copper、Aluminum、Zinc 與貴金屬期貨）
3. **Metals.live**（免 key，貴金屬）
4. **Demo Data**（所有 API 不可用時）

## 📊 推薦的免費 API 源

### 1️⃣ Metals.live API（貴金屬）✅ 推薦
**支持**: Gold, Silver, Platinum, Palladium
**官網**: https://metals.live
**API 文件**: https://metals.live/api
**成本**: 免費，無需 API Key
**限制**: 貴金屬只，無工業金屬

```python
# 使用方式（已在 api_client.py 實現）
import requests
url = "https://api.metals.live/v1/spot/metals"
response = requests.get(url)
data = response.json()
# 返回: {"gold": {"usd": 2145.50, ...}, "silver": {...}, ...}
```

### 2️⃣ Trading Economics（鋼鐵與工業金屬）✅ 推薦
**支持**: Steel、Iron Ore、Copper、Aluminum、Zinc、Nickel、Gold、Silver 等
**官網**: https://tradingeconomics.com
**API 文件**: https://docs.tradingeconomics.com/markets/snapshot/
**成本**: 需要 API Key（依方案限制）

Streamlit Cloud 設定：

```toml
TRADING_ECONOMICS_API_KEY = "your_api_key_here"
```

本地測試：

```bash
export TRADING_ECONOMICS_API_KEY="your_api_key_here"
streamlit run app.py
```

### 3️⃣ Commodity API（綜合商品）
**支持**: 油、天然氣、金屬、農產品等
**官網**: https://commodityapi.com
**成本**: 免費層（50 請求/月），付費方案
**限制**: 免費層流量較小

```python
curl "https://api.commodityapi.com/latest?base=USD&symbols=XAUUSD"
```

### 4️⃣ Python Package: `yfinance`（Yahoo Finance）
**支持**: 黃金 (GC), 白銀 (SI), 原油 (CL) 等期貨
**成本**: 免費，無需 API Key
**限制**: 非官方 API，可能不穩定

```python
import yfinance as yf

# 黃金期貨
gold = yf.Ticker("GC=F").history(period="1d")

# 白銀期貨
silver = yf.Ticker("SI=F").history(period="1d")

# 原油
oil = yf.Ticker("CL=F").history(period="1d")
```

---

## 🔧 如何更新應用

### 選項 A：使用 Alpha Vantage（推薦）

1. **申請 API Key**：https://www.alphavantage.co/support/#api-key

2. **修改 `config.py`**：
```python
ALPHA_VANTAGE_API_KEY = "your_api_key_here"
```

3. **新增 AlphaVantageClient**（在 `api_client.py` 中）：
```python
class AlphaVantageClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_commodity_price(self, symbol: str):
        # symbol: 'WTI' (油), 'COPPER' (銅), 'STEEL' (鋼) 等
        url = f"https://www.alphavantage.co/query?function={symbol}&apikey={self.api_key}"
        response = requests.get(url)
        return response.json()
```

### 選項 B：使用 yfinance（最快）

1. **安裝套件**：
```bash
pip install yfinance
```

2. **在 requirements.txt 添加**：
```
yfinance>=0.2.0
```

3. **修改 `api_client.py`**：
```python
import yfinance as yf

class YFinanceClient:
    def get_all_prices(self) -> list:
        metals = {
            'Gold': 'GC=F',
            'Silver': 'SI=F',
            'Copper': 'HG=F',
            'Steel': 'XX:US',  # Example, actual symbol varies
        }

        prices = []
        for name, symbol in metals.items():
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="1d")
                if not data.empty:
                    price = data['Close'].iloc[-1]
                    prices.append({
                        'metal': name,
                        'price': float(price),
                        'currency': 'USD'
                    })
            except:
                pass
        return prices
```

---

## 📌 當前應用狀態

**目前使用**: 自動資料源選擇
**金屬**: Steel HRC, Iron Ore, Copper, Aluminum, Zinc, Nickel, Gold, Silver, Platinum, Palladium
**更新頻率**: 手動刷新或自動（5 分鐘）

---

## 🚀 建議步驟

1. **短期方案**（現在）- 使用 Yahoo Finance + Metals.live 免 key 資料源
2. **正式方案** - 在 Streamlit Cloud Secrets 加入 `TRADING_ECONOMICS_API_KEY`
3. **進階方案** - 接交易所或付費授權資料源，提升 HRC steel 的穩定性與授權清晰度

---

## 💡 技巧

- **缺存策略**: 使用 SQLite 緩存數據，減少 API 調用
- **錯誤處理**: 實現 fallback 機制（API 故障 → 使用演示數據）
- **速率限制**: Metals.live 無限制，Alpha Vantage 5/min，yfinance 無官方限制
- **費用**: 全部免費方案都可用（除非大量使用）

有問題或需要幫助實裝？告訴我！
