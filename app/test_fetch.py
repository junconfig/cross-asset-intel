from app.services.data_fetcher import get_asset_data
from app.services.regime_engine import calculate_regime


def main():
    data = {
        "BTC": get_asset_data("BTC-USD"),
        "SPY": get_asset_data("SPY"),
        "VIX": get_asset_data("^VIX"),
        "DXY": get_asset_data("DX-Y.NYB"),
        "TNX": get_asset_data("^TNX"),
        "GOLD": get_asset_data("GC=F"),
    }

    result = calculate_regime(data)

    print("Score:", result.score)
    print("Regime:", result.regime)
    print("Confidence:", result.confidence)
    print("Drivers:")
    for d in result.drivers:
        print("-", d)


if __name__ == "__main__":
    main()