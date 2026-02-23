from fastapi import FastAPI

from app.cache import SimpleCache
from app.data_fetcher import get_asset_data
from app.regime_engine import calculate_regime

app = FastAPI(title="Cross Asset Intelligence API")

cache = SimpleCache()


def fetch_all_data():
    print("Fetching BTC...")
    btc = get_asset_data("BTC-USD")

    print("Fetching SPY...")
    spy = get_asset_data("SPY")

    print("Fetching VIX...")
    vix = get_asset_data("^VIX")

    print("Fetching DXY...")
    dxy = get_asset_data("DX-Y.NYB")

    print("Fetching TNX...")
    tnx = get_asset_data("^TNX")

    print("Fetching GOLD...")
    gold = get_asset_data("GC=F")

    print("Done fetching all data.")
    return {
        "BTC": btc,
        "SPY": spy,
        "VIX": vix,
        "DXY": dxy,
        "TNX": tnx,
        "GOLD": gold,
    }


@app.get("/regime")
def get_regime():
    key = "all_market_data"

    data = cache.get(key)

    if data is None:
        print("Fetching fresh market data...")
        data = fetch_all_data()
        cache.set(key, data, ttl_seconds=300)

    result = calculate_regime(data)

    return {
        "score": result.score,
        "regime": result.regime,
        "confidence": result.confidence,
        "drivers": result.drivers,
    }
@app.get("/health")
def health():
    return {"status": "ok"}