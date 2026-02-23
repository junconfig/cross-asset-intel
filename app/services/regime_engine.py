from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


@dataclass
class RegimeResult:
    score: int
    regime: str
    confidence: float
    drivers: List[str]


def _get_last_close(df: pd.DataFrame) -> float:
    close_cols = [c for c in df.columns if c.startswith("close")]
    if not close_cols:
        raise ValueError("No close column found in dataframe.")
    return float(df[close_cols[0]].dropna().iloc[-1])


def _sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window).mean()


def _trend_up(series: pd.Series, window: int) -> bool:
    """
    Simple trend: last value is above the moving average.
    """
    ma = _sma(series, window)
    return bool(series.dropna().iloc[-1] > ma.dropna().iloc[-1])


def _pct_change(series: pd.Series, days: int) -> float:
    s = series.dropna()
    if len(s) < days + 1:
        return 0.0
    return float((s.iloc[-1] / s.iloc[-(days + 1)] - 1.0) * 100.0)


def calculate_regime(data: Dict[str, pd.DataFrame]) -> RegimeResult:
    """
    data keys expected:
      - "BTC"  (BTC-USD)
      - "SPY"  (SPY)
      - "VIX"  (^VIX)
      - "DXY"  (DX-Y.NYB)
      - "TNX"  (^TNX)  10Y yield index
      - "GOLD" (GC=F)

    Output:
      score 0-5, regime label, confidence 0-1, drivers list
    """

    # Extract close series for each asset
    def close_series(key: str) -> pd.Series:
        df = data[key].copy()
        close_cols = [c for c in df.columns if c.startswith("close")]
        if not close_cols:
            raise ValueError(f"{key}: no close column found.")
        return df[close_cols[0]].dropna()

    btc = close_series("BTC")
    spy = close_series("SPY")
    vix = close_series("VIX")
    dxy = close_series("DXY")
    tnx = close_series("TNX")
    gold = close_series("GOLD")

    score = 0
    drivers: List[str] = []
    checks: List[Tuple[bool, str]] = []

    # 1) Equities trend (SPY above 50-day MA)
    equities_up = _trend_up(spy, 50)
    checks.append((equities_up, "SPY above 50-day average (equities strong)"))

    # 2) Crypto trend (BTC above 50-day MA)
    btc_up = _trend_up(btc, 50)
    checks.append((btc_up, "BTC above 50-day average (crypto strong)"))

    # 3) Fear falling (VIX down over last 5 days)
    vix_change_5d = _pct_change(vix, 5)
    vix_falling = vix_change_5d < 0
    checks.append((vix_falling, f"VIX down over 5 days ({vix_change_5d:.2f}%)"))

    # 4) Dollar weakening (DXY down over last 10 days)
    dxy_change_10d = _pct_change(dxy, 10)
    dxy_falling = dxy_change_10d < 0
    checks.append((dxy_falling, f"DXY down over 10 days ({dxy_change_10d:.2f}%)"))

    # 5) Gold not spiking (gold down/flat over last 10 days can imply less fear)
    gold_change_10d = _pct_change(gold, 10)
    gold_not_spiking = gold_change_10d <= 1.0  # allow small up move
    checks.append((gold_not_spiking, f"Gold not spiking over 10 days ({gold_change_10d:.2f}%)"))

    for passed, reason in checks:
        if passed:
            score += 1
            drivers.append(reason)

    # Convert score into regime label
    if score <= 1:
        regime = "risk-off"
    elif score <= 3:
        regime = "neutral"
    else:
        regime = "risk-on"

    # Confidence: simple version = score / 5 (0.0 to 1.0)
    confidence = round(score / 5.0, 2)

    return RegimeResult(score=score, regime=regime, confidence=confidence, drivers=drivers)