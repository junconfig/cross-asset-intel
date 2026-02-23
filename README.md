# Cross Asset Intel

Backend API that fetches cross-asset market data and computes a simple market regime score (risk-on / neutral / risk-off).

## Features
- FastAPI backend with `/regime` endpoint
- Cross-asset inputs (BTC, SPY, VIX, DXY, TNX, GOLD)
- Simple scoring model with drivers
- In-memory caching to reduce repeated downloads

## Tech Stack
- Python 3.11+
- FastAPI
- Uvicorn
- yfinance
- pandas

## Getting Started (Windows + VS Code)

### 1) Create and activate virtual environment
```powershell
python -m venv venv
venv\Scripts\Activate.ps1