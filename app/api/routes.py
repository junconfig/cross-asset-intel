from fastapi import APIRouter, HTTPException

from app.api.schemas import RegimeResponse, HealthResponse
from app.cache import SimpleCache
from app.core.logger import get_logger
from app.services.data_fetcher import get_asset_data
from app.services.regime_engine import calculate_regime
from app.core.config import get_cache_ttl_seconds

router = APIRouter()
cache = SimpleCache()
logger = get_logger("api")


def fetch_all_data():
    logger.info("Fetching BTC...")
    btc = get_asset_data("BTC-USD")

    logger.info("Fetching SPY...")
    spy = get_asset_data("SPY")

    logger.info("Fetching VIX...")
    vix = get_asset_data("^VIX")

    logger.info("Fetching DXY...")
    dxy = get_asset_data("DX-Y.NYB")

    logger.info("Fetching TNX...")
    tnx = get_asset_data("^TNX")

    logger.info("Fetching GOLD...")
    gold = get_asset_data("GC=F")

    logger.info("Done fetching all data.")
    return {
        "BTC": btc,
        "SPY": spy,
        "VIX": vix,
        "DXY": dxy,
        "TNX": tnx,
        "GOLD": gold,
    }


@router.get("/regime", response_model=RegimeResponse)
def get_regime():
    try:
        key = "all_market_data"

        data = cache.get(key)

        if data is None:
            logger.info("Cache miss. Fetching fresh market data...")
            data = fetch_all_data()
            cache.set(key, data, ttl_seconds=get_cache_ttl_seconds())
        else:
            logger.info("Cache hit. Using cached market data.")

        result = calculate_regime(data)

        return {
            "score": result.score,
            "regime": result.regime,
            "confidence": result.confidence,
            "drivers": result.drivers,
        }

    except Exception as e:
        logger.exception("Error in /regime")
        raise HTTPException(status_code=500, detail=f"Regime calculation failed: {e}")


@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}