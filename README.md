# 🌍 International Metal Prices Tracker

Real-time commodity price tracking application built with Streamlit. Track steel, copper, zinc, aluminum, and more with historical price charts and analysis.

## Features

✨ **Core Features:**
- 📊 Real-time metal price tracking
- 📈 Interactive Plotly charts with 30+ days of history
- 💰 Multi-metal support (Steel, Copper, Zinc, Aluminum, Nickel, etc.)
- 🔄 Auto-refresh functionality
- 📱 Responsive web interface
- 💾 Local SQLite data persistence

## Tech Stack

- **Frontend**: Streamlit
- **Charts**: Plotly
- **Data**: Metals.live API (free, no API key required)
- **Database**: SQLite
- **Deployment**: Streamlit Cloud

## Installation

### Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/steel-prices-streamlit.git
cd steel-prices-streamlit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Usage

1. **Select Metals**: Choose metals to track from the sidebar
2. **Refresh Prices**: Click "🔄 Refresh Prices" to fetch latest data
3. **Auto-Refresh**: Enable auto-refresh for continuous updates (every 5 minutes)
4. **View Charts**: Click tabs to view price history and trends
5. **Adjust Range**: Use the slider to view different time periods

## Deployment to Streamlit Cloud

### Step 1: Prepare GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit: Metal Prices Tracker"
git branch -M main
git remote add origin https://github.com/yourusername/steel-prices-streamlit.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [Streamlit Cloud Dashboard](https://share.streamlit.io)
2. Click **"New app"**
3. Select your repository (`steel-prices-streamlit`)
4. Select **Main file** as `app.py`
5. Click **Deploy**

Your app will be live in ~2 minutes at:
```
https://steel-prices-streamlit.streamlit.app
```

Share this URL with anyone to let them track metal prices!

## Project Structure

```
steel-prices-streamlit/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration (metals, API URLs)
├── database.py           # SQLite operations
├── api_client.py         # External API client (Metals.live)
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── .gitignore           # Git ignore rules
└── .streamlit/
    └── config.toml      # Streamlit configuration
```

## Configuration

Edit `config.py` to customize:
- **METALS**: Add/remove metals to track
- **CURRENCY**: Change default currency (default: USD)
- **PRICE_UPDATE_INTERVAL**: Auto-refresh frequency in seconds
- **CHART_DAYS**: Default historical data range
- **TRADING_ECONOMICS_API_KEY**: Optional API key via environment variable or Streamlit Secrets

## API Data Sources

The app automatically uses the first working provider:

1. **Trading Economics**: best coverage for Steel HRC and industrial metals. Set `TRADING_ECONOMICS_API_KEY` in Streamlit Cloud Secrets.
2. **Yahoo Finance futures**: no API key; covers common futures such as HRC, iron ore, zinc, copper, gold, silver, platinum, and palladium when symbols are available.
3. **Metals.live**: no API key; fallback for precious metals.
4. **Demo Data**: keeps the app usable if all external providers are unavailable.

Streamlit Cloud secret example:

```toml
TRADING_ECONOMICS_API_KEY = "your_api_key_here"
```

## Database

Prices are cached locally in SQLite (`prices.db`):
- Stores every price update with timestamp
- Automatic cleanup of data older than 90 days
- Indexed for fast lookups
- Persists between app restarts

**Note**: `prices.db` is added to `.gitignore` to avoid committing data files.

## Development

### Adding a New Feature

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes
3. Test locally: `streamlit run app.py`
4. Commit: `git commit -m "Add feature: description"`
5. Push: `git push origin feature/your-feature`
6. Open Pull Request

### Testing Locally with Mock Data

Edit `api_client.py` to use `MockMetalsClient()` for testing without internet:

```python
# In app.py
api_client = MockMetalsClient()  # For testing
```

## Troubleshooting

### App won't connect to API
- Check internet connection
- Verify API is accessible: `curl https://api.metals.live/v1/spot/metals`
- App will use mock data as fallback

### Database errors
- Delete `prices.db` to reset database
- App will recreate it automatically

### Streamlit Cloud deployment fails
- Verify `requirements.txt` is present
- Check Python version compatibility (3.9+)
- Review deployment logs for errors

## License

MIT License - Feel free to use and modify!

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Submit Pull Request

## Support

For issues and questions, please open a GitHub Issue or check the FAQ above.

---

**Happy tracking!** 📊💰
