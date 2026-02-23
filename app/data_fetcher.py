import pandas as pd
import yfinance as yf


def get_asset_data(symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    Download historical price data for a given symbol.

    yfinance sometimes returns columns as tuples (multi-index).
    This function "flattens" them into normal strings and lowercases them.
    """
    try:
        data = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False)

        if data is None or data.empty:
            raise ValueError("No data returned. Check the symbol or your internet connection.")

        # If columns are multi-index (tuples), flatten them to strings
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = ["_".join([str(x) for x in col if x is not None]) for col in data.columns]
        else:
            data.columns = [str(col) for col in data.columns]

        # Lowercase column names
        data.columns = [col.lower() for col in data.columns]

        # Ensure datetime index
        data.index = pd.to_datetime(data.index)

        return data

    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()