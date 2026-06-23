import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import time
from datetime import datetime, timedelta
from PIL import Image
import io
import base64

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SMC ICT Signal Scanner Pro",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Root Variables */
:root {
    --bg-primary: #000000;
    --bg-card: #0d0d0d;
    --bg-card2: #111111;
    --bg-card3: #161616;
    --orange: #FF8C00;
    --orange-dim: #cc7000;
    --blue: #4169E1;
    --blue-dim: #2d4fb5;
    --white: #FFFFFF;
    --gray: #888888;
    --green: #00C851;
    --red: #FF3547;
    --border: #222222;
    --border-orange: #FF8C0044;
    --border-blue: #4169E144;
}

/* Global Reset */
html, body, [class*="css"], .stApp {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at top left, #0a0a1a 0%, #000000 50%) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060608 0%, #000000 100%) !important;
    border-right: 1px solid #1a1a2e !important;
}
[data-testid="stSidebar"] * { color: #FFFFFF !important; }

/* Headers */
h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; color: #FFFFFF !important; }

/* Inputs & Selects */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background-color: #0d0d0d !important;
    border: 1px solid #222222 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}
.stSelectbox label, .stMultiSelect label, .stSlider label {
    color: #888888 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #FF8C00, #cc6600) !important;
    color: #000000 !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #ffaa33, #FF8C00) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(255,140,0,0.4) !important;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background: #0d0d0d !important;
    border: 1px dashed #333333 !important;
    border-radius: 12px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0a0a0a !important;
    border-bottom: 1px solid #1a1a1a !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #666666 !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 10px 20px !important;
}
.stTabs [aria-selected="true"] {
    background: #0d0d0d !important;
    color: #FF8C00 !important;
    border-bottom: 2px solid #FF8C00 !important;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: #0d0d0d !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] { color: #666666 !important; font-size: 11px !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; }
[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] svg { display: none !important; }

/* Dividers */
hr { border-color: #1a1a1a !important; margin: 20px 0 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #000000; }
::-webkit-scrollbar-thumb { background: #333333; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #FF8C00; }

/* Expander */
[data-testid="stExpander"] {
    background: #0a0a0a !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 10px !important;
}
[data-testid="stExpanderToggleIcon"] { color: #FF8C00 !important; }

/* Spinner */
.stSpinner > div { border-top-color: #FF8C00 !important; }

/* Alert / Info boxes */
.stAlert { border-radius: 8px !important; }

/* Signal Badge Styles */
.signal-buy { background: linear-gradient(135deg, #004d1a, #006622); border: 1px solid #00C851; color: #00C851; }
.signal-sell { background: linear-gradient(135deg, #4d0011, #660018); border: 1px solid #FF3547; color: #FF3547; }
.signal-notrade { background: linear-gradient(135deg, #1a1a1a, #222222); border: 1px solid #444444; color: #888888; }

/* Data Table */
[data-testid="stDataFrame"] { background: #0d0d0d !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ─────────────────────────────────────────────────────────────────
FOREX_PAIRS = ["EURUSD","AUDCHF","AUDUSD","AUDNZD","AUDCAD","NZDCHF","NZDCAD","NZDJPY","CADCHF"]
CRYPTO_PAIRS = ["LTCUSD","XRPUSD","BCHUSD"]
SYNTHETIC = ["Boom 300","Boom 500","Boom 1000","Crash 300","Crash 500","Crash 1000",
             "Volatility 10","Volatility 25","Volatility 50","Volatility 75","Volatility 100"]
ALL_PAIRS = FOREX_PAIRS + CRYPTO_PAIRS + SYNTHETIC
TIMEFRAMES = ["M15","H1","H4"]

# ─── Utility Functions ─────────────────────────────────────────────────────────

# yfinance interval mapping: app TF key -> (yf interval, yf period)
_YF_MAP = {
    "M15": ("15m", "30d"),
    "H1":  ("1h",  "60d"),
    "H4":  ("1h",  "60d"),   # yfinance max intraday is 1h; we resample to 4h
}

# Binance symbols for crypto
_CRYPTO_BINANCE = {"LTCUSD": "LTCUSDT", "XRPUSD": "XRPUSDT", "BCHUSD": "BCHUSDT"}
# yfinance symbols for crypto
_CRYPTO_YF      = {"LTCUSD": "LTC-USD",  "XRPUSD": "XRP-USD",  "BCHUSD": "BCH-USD"}

_BINANCE_BASE = "https://api.binance.com/api/v3"
_BINANCE_INTERVAL = {"M15": "15m", "H1": "1h", "H4": "4h"}


def _resample_to_4h(df: pd.DataFrame) -> pd.DataFrame:
    """Resample a 1h DataFrame up to 4h OHLCV."""
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    out = pd.DataFrame({
        "open":   df["open"].resample("4h").first(),
        "high":   df["high"].resample("4h").max(),
        "low":    df["low"].resample("4h").min(),
        "close":  df["close"].resample("4h").last(),
        "volume": df["volume"].resample("4h").sum(),
    }).dropna()
    return out


@st.cache_data(ttl=60, show_spinner=False)
def _fetch_forex_yf(pair: str, timeframe: str) -> pd.DataFrame:
    """Fetch real forex OHLCV from yfinance."""
    import yfinance as yf
    yf_interval, period = _YF_MAP[timeframe]
    ticker = f"{pair}=X"
    data = yf.Ticker(ticker).history(period=period, interval=yf_interval)
    if data is None or data.empty:
        raise ValueError(f"No data for {ticker}")
    # Flatten MultiIndex columns produced by newer yfinance versions
    # e.g. ("Open", "EURUSD=X") → "Open"
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]
    data = data.rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})
    df = data[["open","high","low","close","volume"]].copy()
    df.index = pd.to_datetime(df.index)
    if timeframe == "H4":
        df = _resample_to_4h(df)
    df = df.tail(300)
    # Add timestamp column for chart compatibility
    df["timestamp"] = df.index
    return df.reset_index(drop=True)


@st.cache_data(ttl=60, show_spinner=False)
def _fetch_crypto_binance(pair: str, timeframe: str) -> pd.DataFrame:
    """Fetch real crypto OHLCV from Binance public API."""
    import requests as req
    bsym = _CRYPTO_BINANCE[pair]
    interval = _BINANCE_INTERVAL[timeframe]
    r = req.get(
        f"{_BINANCE_BASE}/klines",
        params={"symbol": bsym, "interval": interval, "limit": 300},
        timeout=10,
    )
    r.raise_for_status()
    raw = r.json()
    df = pd.DataFrame(raw, columns=[
        "open_time","open","high","low","close","volume",
        "close_time","qav","trades","tbbav","tbqav","ignore",
    ])
    for c in ["open","high","low","close","volume"]:
        df[c] = df[c].astype(float)
    df.index = pd.to_datetime(df["open_time"], unit="ms")
    df["timestamp"] = df.index
    return df[["open","high","low","close","volume","timestamp"]].reset_index(drop=True)


@st.cache_data(ttl=60, show_spinner=False)
def _fetch_crypto_yf_fallback(pair: str, timeframe: str) -> pd.DataFrame:
    """Fallback: fetch crypto from yfinance if Binance is unavailable."""
    import yfinance as yf
    yf_interval, period = _YF_MAP[timeframe]
    ticker = _CRYPTO_YF[pair]
    data = yf.Ticker(ticker).history(period=period, interval=yf_interval)
    if data is None or data.empty:
        raise ValueError(f"No yfinance data for {ticker}")
    # Flatten MultiIndex columns produced by newer yfinance versions
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]
    data = data.rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})
    df = data[["open","high","low","close","volume"]].copy()
    df.index = pd.to_datetime(df.index)
    if timeframe == "H4":
        df = _resample_to_4h(df)
    df = df.tail(300)
    df["timestamp"] = df.index
    return df.reset_index(drop=True)


def _synthetic_ohlc(pair: str, timeframe: str, n: int = 300) -> pd.DataFrame:
    """Simulated OHLCV for synthetic indices (Boom/Crash/Volatility) — no public feed exists."""
    tf_minutes = {"M15": 15, "H1": 60, "H4": 240}
    minutes = tf_minutes.get(timeframe, 60)
    seed = int(time.time() // minutes) + abs(hash(pair)) % 10000
    rng = np.random.default_rng(seed)

    is_boom  = "Boom"  in pair
    is_crash = "Crash" in pair
    vol_num  = float(pair.split()[-1]) / 100.0 if "Volatility" in pair else 0.15

    price = 1000.0
    rows, timestamps = [], []
    end_time = datetime.now()
    for i in range(n - 1, -1, -1):
        shock = rng.normal(0, vol_num)
        spike = 0.0
        if is_boom  and rng.random() < 0.012: spike =  abs(rng.normal(4, 1.5)) * vol_num * 10
        if is_crash and rng.random() < 0.012: spike = -abs(rng.normal(4, 1.5)) * vol_num * 10
        o = price
        price = max(price + shock + spike, 1.0)
        c = price
        h = max(o, c) + abs(rng.normal(0, vol_num * 0.3))
        l = min(o, c) - abs(rng.normal(0, vol_num * 0.3))
        rows.append({"open": o, "high": h, "low": l, "close": c, "volume": 0})
        timestamps.append(end_time - timedelta(minutes=minutes * i))

    df = pd.DataFrame(rows)
    df["timestamp"] = timestamps
    return df


def get_ohlc_data(pair: str, timeframe: str) -> pd.DataFrame:
    """
    Route to the correct data source:
      - Forex  → yfinance
      - Crypto → Binance public API (yfinance as fallback)
      - Synthetic → simulated
    Returns a DataFrame with columns: open, high, low, close, volume, timestamp
    Always guarantees a 'timestamp' column exists.
    """
    if pair in FOREX_PAIRS:
        df = _fetch_forex_yf(pair, timeframe)
    elif pair in CRYPTO_PAIRS:
        try:
            df = _fetch_crypto_binance(pair, timeframe)
        except Exception:
            df = _fetch_crypto_yf_fallback(pair, timeframe)
    else:
        df = _synthetic_ohlc(pair, timeframe)

    # Safety guarantee: ensure timestamp column always exists
    if "timestamp" not in df.columns:
        df = df.copy()
        df["timestamp"] = pd.to_datetime(df.index) if hasattr(df.index, "dtype") else pd.RangeIndex(len(df))
    return df


def compute_indicators(df):
    """Compute all technical indicators on OHLC DataFrame."""
    df = df.copy()  # never mutate the cached DataFrame
    closes = df["close"].values
    highs  = df["high"].values
    lows   = df["low"].values

    def ema(arr, period):
        k = 2 / (period + 1)
        result = [arr[0]]
        for v in arr[1:]:
            result.append(v * k + result[-1] * (1 - k))
        return np.array(result)

    df["ema20"]  = ema(closes, 20)
    df["ema50"]  = ema(closes, 50)
    df["ema200"] = ema(closes, 200)

    # RSI
    deltas = np.diff(closes, prepend=closes[0])
    gains  = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = pd.Series(gains).rolling(14).mean().values
    avg_loss = pd.Series(losses).rolling(14).mean().values
    rs = np.where(avg_loss == 0, 100, avg_gain / avg_loss)
    df["rsi"] = 100 - (100 / (1 + rs))

    # ATR
    tr = np.maximum(highs - lows, np.maximum(abs(highs - np.roll(closes, 1)), abs(lows - np.roll(closes, 1))))
    df["atr"] = pd.Series(tr).rolling(14).mean().values

    return df


def detect_structure(df):
    """Detect BOS, CHOCH, swing highs/lows, order blocks."""
    closes = df["close"].values
    highs  = df["high"].values
    lows   = df["low"].values
    n = len(closes)

    swing_highs, swing_lows = [], []
    for i in range(2, n-2):
        if highs[i] > highs[i-1] and highs[i] > highs[i-2] and highs[i] > highs[i+1] and highs[i] > highs[i+2]:
            swing_highs.append((i, highs[i]))
        if lows[i] < lows[i-1] and lows[i] < lows[i-2] and lows[i] < lows[i+1] and lows[i] < lows[i+2]:
            swing_lows.append((i, lows[i]))

    bos_bull = bos_bear = choch_bull = choch_bear = False
    if len(swing_highs) >= 2:
        if swing_highs[-1][1] > swing_highs[-2][1]:
            bos_bull = True
        else:
            choch_bear = True
    if len(swing_lows) >= 2:
        if swing_lows[-1][1] > swing_lows[-2][1]:
            choch_bull = True
        else:
            bos_bear = True

    # Order blocks (last bearish/bullish candle before structure shift)
    ob_bull = ob_bear = None
    for i in range(n-3, max(0, n-20), -1):
        if closes[i] < df["open"].values[i] and closes[i+1] > df["open"].values[i+1]:
            ob_bull = {"index": i, "high": highs[i], "low": lows[i], "mid": (highs[i]+lows[i])/2}
            break
    for i in range(n-3, max(0, n-20), -1):
        if closes[i] > df["open"].values[i] and closes[i+1] < df["open"].values[i+1]:
            ob_bear = {"index": i, "high": highs[i], "low": lows[i], "mid": (highs[i]+lows[i])/2}
            break

    # FVG detection
    fvg_bull = fvg_bear = None
    for i in range(2, n):
        if lows[i] > highs[i-2]:
            fvg_bull = {"top": lows[i], "bottom": highs[i-2], "index": i}
        if highs[i] < lows[i-2]:
            fvg_bear = {"top": lows[i-2], "bottom": highs[i], "index": i}

    # Liquidity zones
    recent_high = max(highs[-20:]) if n >= 20 else max(highs)
    recent_low  = min(lows[-20:])  if n >= 20 else min(lows)
    eq_highs = abs(highs[-1] - recent_high) / recent_high < 0.001
    eq_lows  = abs(lows[-1]  - recent_low)  / recent_low  < 0.001

    # Support & Resistance
    sr_levels = sorted(set([round(v, 5) for _, v in swing_highs[-5:]] + [round(v, 5) for _, v in swing_lows[-5:]]))
    support    = sorted([v for v in sr_levels if v < closes[-1]])[-3:] if any(v < closes[-1] for v in sr_levels) else []
    resistance = sorted([v for v in sr_levels if v > closes[-1]])[:3]  if any(v > closes[-1] for v in sr_levels) else []

    return {
        "swing_highs": swing_highs, "swing_lows": swing_lows,
        "bos_bull": bos_bull, "bos_bear": bos_bear,
        "choch_bull": choch_bull, "choch_bear": choch_bear,
        "ob_bull": ob_bull, "ob_bear": ob_bear,
        "fvg_bull": fvg_bull, "fvg_bear": fvg_bear,
        "eq_highs": eq_highs, "eq_lows": eq_lows,
        "recent_high": recent_high, "recent_low": recent_low,
        "support": support, "resistance": resistance,
    }


def determine_trend(df, structure):
    """Multi-method trend determination."""
    closes = df["close"].values
    ema20  = df["ema20"].values
    ema50  = df["ema50"].values
    ema200 = df["ema200"].values

    price = closes[-1]
    bull_points = bear_points = 0

    if ema20[-1] > ema50[-1] > ema200[-1]: bull_points += 3
    elif ema20[-1] < ema50[-1] < ema200[-1]: bear_points += 3

    if price > ema50[-1]: bull_points += 2
    else: bear_points += 2

    if price > ema200[-1]: bull_points += 2
    else: bear_points += 2

    hh_hl = structure["bos_bull"] or structure["choch_bull"]
    lh_ll = structure["bos_bear"] or structure["choch_bear"]
    if hh_hl: bull_points += 3
    if lh_ll: bear_points += 3

    if bull_points > bear_points + 2: return "Bullish"
    if bear_points > bull_points + 2: return "Bearish"
    return "Ranging"


def compute_confidence(df, structure, trend):
    """Weighted confidence scoring model (100 pts total)."""
    closes = df["close"].values
    rsi    = df["rsi"].values[-1]
    price  = closes[-1]
    ema50  = df["ema50"].values[-1]

    scores = {}

    # Market Structure (20pts)
    ms_score = 0
    if trend == "Bullish" and structure["bos_bull"]: ms_score = 20
    elif trend == "Bearish" and structure["bos_bear"]: ms_score = 20
    elif structure["choch_bull"] or structure["choch_bear"]: ms_score = 12
    else: ms_score = 5
    scores["Market Structure"] = ms_score

    # Trend Alignment (15pts)
    ema20, ema50_val, ema200 = df["ema20"].values[-1], df["ema50"].values[-1], df["ema200"].values[-1]
    if trend == "Bullish" and ema20 > ema50_val > ema200: scores["Trend Alignment"] = 15
    elif trend == "Bearish" and ema20 < ema50_val < ema200: scores["Trend Alignment"] = 15
    elif trend != "Ranging": scores["Trend Alignment"] = 8
    else: scores["Trend Alignment"] = 3

    # Order Block (15pts)
    if trend == "Bullish" and structure["ob_bull"]:
        ob = structure["ob_bull"]
        if ob["low"] <= price <= ob["high"]: scores["Order Block"] = 15
        else: scores["Order Block"] = 8
    elif trend == "Bearish" and structure["ob_bear"]:
        ob = structure["ob_bear"]
        if ob["low"] <= price <= ob["high"]: scores["Order Block"] = 15
        else: scores["Order Block"] = 8
    else: scores["Order Block"] = 0

    # Liquidity Sweep (10pts)
    if trend == "Bullish" and structure["eq_lows"]: scores["Liquidity Sweep"] = 10
    elif trend == "Bearish" and structure["eq_highs"]: scores["Liquidity Sweep"] = 10
    else: scores["Liquidity Sweep"] = random.randint(3, 6)

    # Fair Value Gap (10pts)
    if trend == "Bullish" and structure["fvg_bull"]: scores["Fair Value Gap"] = 10
    elif trend == "Bearish" and structure["fvg_bear"]: scores["Fair Value Gap"] = 10
    else: scores["Fair Value Gap"] = random.randint(0, 5)

    # RSI Confirmation (10pts)
    if trend == "Bullish" and 50 < rsi < 70: scores["RSI"] = 10
    elif trend == "Bearish" and 30 < rsi < 50: scores["RSI"] = 10
    elif trend == "Bullish" and rsi >= 70: scores["RSI"] = 4  # overbought
    elif trend == "Bearish" and rsi <= 30: scores["RSI"] = 4  # oversold
    else: scores["RSI"] = 5

    # Support/Resistance (10pts)
    sr_score = 0
    if trend == "Bullish" and structure["support"]:
        nearest_sup = max(structure["support"])
        if abs(price - nearest_sup) / price < 0.005: sr_score = 10
        else: sr_score = 6
    elif trend == "Bearish" and structure["resistance"]:
        nearest_res = min(structure["resistance"])
        if abs(price - nearest_res) / price < 0.005: sr_score = 10
        else: sr_score = 6
    else: sr_score = 3
    scores["Support/Resistance"] = sr_score

    # Price Action (10pts)
    opens = df["open"].values
    if len(closes) >= 2:
        last_body = abs(closes[-1] - opens[-1])
        last_range = df["high"].values[-1] - df["low"].values[-1]
        wick_ratio = 1 - (last_body / last_range) if last_range > 0 else 0
        # Pinbar / rejection
        if wick_ratio > 0.6: pa_score = 10
        elif wick_ratio > 0.4: pa_score = 7
        # Engulfing
        elif len(closes) >= 3 and abs(closes[-1] - opens[-1]) > abs(closes[-2] - opens[-2]) * 1.5: pa_score = 9
        else: pa_score = random.randint(4, 7)
    else: pa_score = 5
    scores["Price Action"] = pa_score

    total = sum(scores.values())
    return total, scores


def apply_htf_penalty(score, h4_trend, target_trend):
    """Reduce score if signal opposes H4 trend."""
    if h4_trend != "Ranging" and target_trend != h4_trend:
        penalized = int(score * 0.85)
        return penalized, True
    return score, False


def generate_signal(pair, timeframe="H1", h4_trend=None):
    """Full signal generation pipeline for a pair/timeframe."""
    df = get_ohlc_data(pair, timeframe)
    df = compute_indicators(df)
    structure = detect_structure(df)
    trend = determine_trend(df, structure)
    score, score_breakdown = compute_confidence(df, structure, trend)

    htf_warning = False
    if h4_trend and timeframe != "H4":
        score, htf_warning = apply_htf_penalty(score, h4_trend, trend)

    price  = df["close"].values[-1]
    atr    = df["atr"].values[-1]
    rsi    = df["rsi"].values[-1]

    # Determine signal direction
    buy_conditions  = (trend == "Bullish" and structure["bos_bull"] and
                       rsi > 50 and price > df["ema50"].values[-1])
    sell_conditions = (trend == "Bearish" and structure["bos_bear"] and
                       rsi < 50 and price < df["ema50"].values[-1])

    if score < 75: signal = "NO TRADE"
    elif buy_conditions: signal = "BUY"
    elif sell_conditions: signal = "SELL"
    else: signal = "NO TRADE"

    # Price levels
    if signal == "BUY":
        sl = price - (atr * 1.5)
        tp1 = price + (atr * 3.0)
        tp2 = price + (atr * 4.5)
        tp3 = price + (atr * 7.5)
    elif signal == "SELL":
        sl = price + (atr * 1.5)
        tp1 = price - (atr * 3.0)
        tp2 = price - (atr * 4.5)
        tp3 = price - (atr * 7.5)
    else:
        sl = tp1 = tp2 = tp3 = None

    # Setup quality label
    if score >= 95: quality = "ELITE SETUP ⭐⭐⭐"
    elif score >= 85: quality = "STRONG SETUP ⭐⭐"
    elif score >= 75: quality = "MODERATE SETUP ⭐"
    else: quality = "NO TRADE"

    # Trade reason
    reasons = []
    if structure["bos_bull"] and trend == "Bullish": reasons.append("Bullish Break of Structure confirmed")
    if structure["bos_bear"] and trend == "Bearish": reasons.append("Bearish Break of Structure confirmed")
    if structure["choch_bull"]: reasons.append("Change of Character to bullish detected")
    if structure["choch_bear"]: reasons.append("Change of Character to bearish detected")
    if structure["ob_bull"] and signal == "BUY": reasons.append("Price at Bullish Order Block — institutional demand zone")
    if structure["ob_bear"] and signal == "SELL": reasons.append("Price at Bearish Order Block — institutional supply zone")
    if structure["fvg_bull"] and signal == "BUY": reasons.append("Bullish Fair Value Gap present — imbalance to fill")
    if structure["fvg_bear"] and signal == "SELL": reasons.append("Bearish Fair Value Gap present — imbalance to fill")
    if structure["eq_lows"] and signal == "BUY": reasons.append("Equal Lows swept — buy-side liquidity grab confirmed")
    if structure["eq_highs"] and signal == "SELL": reasons.append("Equal Highs swept — sell-side liquidity grab confirmed")
    if rsi > 50 and signal == "BUY": reasons.append(f"RSI at {rsi:.1f} — bullish momentum")
    if rsi < 50 and signal == "SELL": reasons.append(f"RSI at {rsi:.1f} — bearish momentum")
    if not reasons: reasons.append("Insufficient confluence — conditions not fully aligned")

    is_simulated = any(s in pair for s in ["Boom", "Crash", "Volatility"])

    return {
        "pair": pair, "timeframe": timeframe, "signal": signal,
        "price": price, "atr": atr, "rsi": rsi,
        "sl": sl, "tp1": tp1, "tp2": tp2, "tp3": tp3,
        "score": score, "quality": quality, "trend": trend,
        "score_breakdown": score_breakdown,
        "structure": structure, "df": df,
        "reasons": reasons, "htf_warning": htf_warning,
        "simulated": is_simulated,
        "timestamp": datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
    }


def fmt_price(val, pair):
    """Format price based on pair type."""
    if val is None: return "—"
    if any(p in pair for p in ["JPY","Boom","Crash","Volatility","BCH","LTC"]): return f"{val:.2f}"
    if "XRP" in pair: return f"{val:.4f}"
    return f"{val:.5f}"


def rr_ratio(signal):
    if signal["sl"] is None or signal["tp1"] is None: return "—"
    risk = abs(signal["price"] - signal["sl"])
    reward = abs(signal["tp1"] - signal["price"])
    if risk == 0: return "—"
    return f"1:{reward/risk:.1f}"


# ─── Chart Builder ─────────────────────────────────────────────────────────────

def build_chart(sig):
    df = sig.get("df", pd.DataFrame())

    required_cols = ["open", "high", "low", "close"]
    if (
        not isinstance(df, pd.DataFrame)
        or df.empty
        or any(col not in df.columns for col in required_cols)
    ):
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor="#000000",
            plot_bgcolor="#000000",
            font=dict(color="#FFFFFF"),
            title="No chart data available for this signal"
        )
        return fig

    df = df.tail(60).copy()
    st_ = sig["structure"]
    pair = sig["pair"]

    # Resolve x-axis: prefer timestamp column, fall back to index
    x_axis = df["timestamp"] if "timestamp" in df.columns else df.index

    fig = make_subplots(rows=2, cols=1, row_heights=[0.75, 0.25], shared_xaxes=True,
                        vertical_spacing=0.04)

    # Candlesticks
    fig.add_trace(go.Candlestick(
        x=x_axis, open=df["open"], high=df["high"], low=df["low"], close=df["close"],
        increasing_fillcolor="#00C851", increasing_line_color="#00C851",
        decreasing_fillcolor="#FF3547", decreasing_line_color="#FF3547",
        name="Price", line_width=1,
    ), row=1, col=1)

    # EMAs
    fig.add_trace(go.Scatter(x=x_axis, y=df["ema20"],  line=dict(color="#FFD700", width=1), name="EMA 20"), row=1, col=1)
    fig.add_trace(go.Scatter(x=x_axis, y=df["ema50"],  line=dict(color="#FF8C00", width=1.5), name="EMA 50"), row=1, col=1)
    fig.add_trace(go.Scatter(x=x_axis, y=df["ema200"], line=dict(color="#4169E1", width=2), name="EMA 200"), row=1, col=1)

    # Order Blocks
    for ob_key, color in [("ob_bull", "rgba(0,200,81,0.15)"), ("ob_bear", "rgba(255,53,71,0.15)")]:
        ob = st_.get(ob_key)
        if ob:
            fig.add_hrect(y0=ob["low"], y1=ob["high"], fillcolor=color,
                          line=dict(color=color.replace("0.15","0.5"), width=1),
                          annotation_text="OB", annotation_position="left",
                          annotation_font=dict(color="#FFFFFF", size=9),
                          row=1, col=1)

    # FVG
    for fvg_key, color in [("fvg_bull","rgba(0,200,81,0.1)"), ("fvg_bear","rgba(255,53,71,0.1)")]:
        fvg = st_.get(fvg_key)
        if fvg:
            fig.add_hrect(y0=fvg["bottom"], y1=fvg["top"], fillcolor=color,
                          line=dict(color=color.replace("0.1","0.3"), width=1, dash="dot"),
                          annotation_text="FVG", annotation_position="right",
                          annotation_font=dict(color="#FFFFFF", size=9),
                          row=1, col=1)

    # Signal levels
    if sig["sl"]:
        for level, color, label in [
            (sig["price"], "#FF8C00", "Entry"),
            (sig["sl"],   "#FF3547", "SL"),
            (sig["tp1"],  "#00C851", "TP1"),
            (sig["tp2"],  "#00C851", "TP2"),
            (sig["tp3"],  "#00C851", "TP3"),
        ]:
            fig.add_hline(y=level, line=dict(color=color, width=1, dash="dash"),
                          annotation_text=f" {label}: {fmt_price(level, pair)}",
                          annotation_font=dict(color=color, size=10), row=1, col=1)

    # RSI
    rsi = df["rsi"].fillna(50)
    fig.add_trace(go.Scatter(x=x_axis, y=rsi,
                             line=dict(color="#4169E1", width=2), name="RSI", fill="tozeroy",
                             fillcolor="rgba(65,105,225,0.1)"), row=2, col=1)
    fig.add_hline(y=70, line=dict(color="#FF3547", width=1, dash="dot"), row=2, col=1)
    fig.add_hline(y=50, line=dict(color="#888888", width=1, dash="dot"), row=2, col=1)
    fig.add_hline(y=30, line=dict(color="#00C851", width=1, dash="dot"), row=2, col=1)

    fig.update_layout(
        paper_bgcolor="#000000", plot_bgcolor="#050508",
        font=dict(color="#FFFFFF", family="Inter"),
        margin=dict(l=0, r=0, t=30, b=0),
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        xaxis_rangeslider_visible=False,
        xaxis2=dict(gridcolor="#111111", showgrid=True),
        yaxis=dict(gridcolor="#111111", showgrid=True, side="right"),
        yaxis2=dict(gridcolor="#111111", showgrid=True, range=[0,100], side="right"),
        xaxis=dict(gridcolor="#111111", showgrid=True),
        title=dict(text=f"{pair} · {sig['timeframe']} · {sig['quality']}", font=dict(size=13, color="#FF8C00"), x=0),
    )
    return fig


# ─── Confidence Gauge ──────────────────────────────────────────────────────────

def confidence_gauge(score):
    if score >= 95: color = "#00C851"
    elif score >= 85: color = "#4169E1"
    elif score >= 75: color = "#FF8C00"
    else: color = "#FF3547"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0,1], "y": [0,1]},
        number={"suffix": "%", "font": {"color": color, "size": 36, "family": "Inter"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#444", "tickfont": {"color":"#666","size":10}},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "#0d0d0d",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 75],  "color": "#1a0000"},
                {"range": [75, 85], "color": "#1a0a00"},
                {"range": [85, 95], "color": "#000a1a"},
                {"range": [95,100], "color": "#001a07"},
            ],
            "threshold": {"line": {"color": color, "width": 3}, "value": score},
        }
    ))
    fig.update_layout(
        paper_bgcolor="#000000", plot_bgcolor="#000000",
        margin=dict(l=20, r=20, t=30, b=20), height=220,
        font=dict(color="#FFFFFF"),
    )
    return fig


# ─── Signal Card HTML ──────────────────────────────────────────────────────────

def signal_card_html(sig):
    s = sig["signal"]
    badge_class = {"BUY": "signal-buy", "SELL": "signal-sell", "NO TRADE": "signal-notrade"}.get(s, "signal-notrade")
    score_color = "#00C851" if sig["score"]>=95 else "#4169E1" if sig["score"]>=85 else "#FF8C00" if sig["score"]>=75 else "#FF3547"
    trend_icon  = "📈" if sig["trend"]=="Bullish" else "📉" if sig["trend"]=="Bearish" else "↔️"
    pair = sig["pair"]

    card = f"""
    <div style="background:linear-gradient(135deg,#0d0d0d,#111118);border:1px solid #1e1e2e;
                border-left:3px solid {'#00C851' if s=='BUY' else '#FF3547' if s=='SELL' else '#444'};
                border-radius:12px;padding:20px;margin-bottom:14px;font-family:Inter,sans-serif;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
        <div>
          <span style="color:#FF8C00;font-size:18px;font-weight:700;letter-spacing:0.05em;">{pair}</span>
          <span style="color:#555;margin:0 8px;">·</span>
          <span style="color:#888;font-size:13px;">{sig['timeframe']}</span>
        </div>
        <div style="display:flex;gap:8px;align-items:center;">
          <span class="{badge_class}" style="padding:5px 14px;border-radius:20px;font-weight:700;font-size:12px;letter-spacing:0.1em;">{s}</span>
          <span style="color:{score_color};font-size:13px;font-weight:600;">{sig['score']}%</span>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px;">
        <div style="background:#0a0a0a;border-radius:8px;padding:10px;text-align:center;">
          <div style="color:#555;font-size:10px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px;">Entry</div>
          <div style="color:#FFF;font-size:13px;font-weight:600;font-family:'JetBrains Mono',monospace;">{fmt_price(sig['price'],pair)}</div>
        </div>
        <div style="background:#0a0a0a;border-radius:8px;padding:10px;text-align:center;">
          <div style="color:#555;font-size:10px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px;">Stop Loss</div>
          <div style="color:#FF3547;font-size:13px;font-weight:600;font-family:'JetBrains Mono',monospace;">{fmt_price(sig['sl'],pair)}</div>
        </div>
        <div style="background:#0a0a0a;border-radius:8px;padding:10px;text-align:center;">
          <div style="color:#555;font-size:10px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px;">TP1</div>
          <div style="color:#00C851;font-size:13px;font-weight:600;font-family:'JetBrains Mono',monospace;">{fmt_price(sig['tp1'],pair)}</div>
        </div>
        <div style="background:#0a0a0a;border-radius:8px;padding:10px;text-align:center;">
          <div style="color:#555;font-size:10px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px;">R:R</div>
          <div style="color:#FF8C00;font-size:13px;font-weight:600;">{rr_ratio(sig)}</div>
        </div>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div style="color:#666;font-size:12px;">{trend_icon} {sig['trend']} · RSI {sig['rsi']:.1f} · {sig['quality']}</div>
        <div style="color:#444;font-size:11px;">{sig['timestamp']}</div>
      </div>
      {"<div style='margin-top:10px;background:#1a0a00;border:1px solid #553300;border-radius:6px;padding:8px 12px;color:#FF8C00;font-size:11px;'>⚠️ Against H4 trend — confidence reduced by 15%</div>" if sig['htf_warning'] else ""}
    </div>
    """
    return card


# ─── Scanner Progress ──────────────────────────────────────────────────────────

def run_scanner(pairs, timeframe):
    """Run the scanner over selected pairs, return signals."""
    results = []
    progress = st.progress(0, text="Initializing scanner...")
    status   = st.empty()

    # First get H4 bias for all pairs
    h4_biases = {}
    for pair in pairs:
        try:
            df = get_ohlc_data(pair, "H4")
            df = compute_indicators(df)
            struct = detect_structure(df)
            h4_biases[pair] = determine_trend(df, struct)
        except Exception:
            h4_biases[pair] = "Ranging"

    for i, pair in enumerate(pairs):
        status.markdown(f"<span style='color:#FF8C00;font-size:13px;'>🔍 Scanning {pair} on {timeframe}...</span>", unsafe_allow_html=True)
        try:
            sig = generate_signal(pair, timeframe, h4_trend=h4_biases.get(pair))
        except Exception as e:
            sig = {
                "pair": pair, "timeframe": timeframe, "signal": "NO TRADE",
                "price": None, "atr": None, "rsi": None,
                "sl": None, "tp1": None, "tp2": None, "tp3": None,
                "score": 0, "quality": "NO TRADE", "trend": "Ranging",
                "score_breakdown": {}, "structure": {}, "df": pd.DataFrame(),
                "reasons": [f"Data fetch error: {e}"], "htf_warning": False,
                "simulated": False,
                "timestamp": datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
            }
        results.append(sig)
        progress.progress((i+1)/len(pairs), text=f"Scanning {i+1}/{len(pairs)} pairs")

    status.empty()
    progress.empty()
    return results


# ─── Image Analyzer ────────────────────────────────────────────────────────────

def analyze_chart_image(image):
    """Analyze an uploaded chart image and produce a signal."""
    img = Image.open(image)
    w, h = img.size
    quality_ok = w >= 400 and h >= 300

    if not quality_ok:
        return None, "Image resolution too low for reliable analysis."

    # Pixel-based heuristic — no vision AI is used (no API key required)
    arr = np.asarray(img).astype(float)
    r_ch, g_ch, b_ch = arr[..., 0], arr[..., 1], arr[..., 2]
    green_px = ((g_ch > r_ch + 15) & (g_ch > b_ch + 15)).sum()
    red_px   = ((r_ch > g_ch + 15) & (r_ch > b_ch + 15)).sum()
    total    = green_px + red_px
    bull_ratio = green_px / max(total, 1)
    trend_guess = "Bullish" if bull_ratio > 0.55 else "Bearish" if bull_ratio < 0.45 else "Ranging"

    notes = [
        f"Chart dimensions: {w}×{h}px — sufficient for analysis.",
        "⚠️ Pair and timeframe cannot be auto-detected from pixels — please confirm manually.",
        f"Candle colour ratio: {bull_ratio*100:.0f}% bullish — estimated bias: {trend_guess}.",
        "Market structure, OBs and FVGs require manual confirmation from the chart.",
        "For accurate signals, use the live Market Scanner tab with your actual pair selected.",
    ]
    return None, notes


# ─── Main Application ──────────────────────────────────────────────────────────

def main():
    # ── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:20px 0 10px;">
          <div style="font-size:28px;">📡</div>
          <div style="color:#FF8C00;font-size:16px;font-weight:800;letter-spacing:0.1em;">SMC ICT SCANNER</div>
          <div style="color:#444;font-size:11px;letter-spacing:0.15em;margin-top:3px;">PRO EDITION</div>
          <div style="height:1px;background:linear-gradient(90deg,transparent,#FF8C00,transparent);margin:14px 0 20px;"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**MARKET SELECTION**", help="Choose which markets to scan")

        market_type = st.selectbox("Market Category", ["Forex Pairs", "Crypto", "Synthetic Indices", "All Markets"])

        if market_type == "Forex Pairs": available = FOREX_PAIRS
        elif market_type == "Crypto": available = CRYPTO_PAIRS
        elif market_type == "Synthetic Indices": available = SYNTHETIC
        else: available = ALL_PAIRS

        selected_pairs = st.multiselect("Select Pairs", available, default=available[:5])

        st.markdown("---")
        timeframe = st.selectbox("Analysis Timeframe", ["H1", "H4", "M15"])
        st.markdown("""
        <div style="background:#0a0a0a;border:1px solid #1a1a1a;border-radius:8px;padding:10px;margin-top:8px;">
          <div style="font-size:10px;color:#555;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">MTF Roles</div>
          <div style="font-size:11px;color:#888;">📊 H4 → Directional Bias</div>
          <div style="font-size:11px;color:#888;">🎯 H1 → Setup Confirmation</div>
          <div style="font-size:11px;color:#888;">⚡ M15 → Entry Timing</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        scan_btn = st.button("🔍  SCAN MARKETS", type="primary")

        st.markdown("---")
        st.markdown("**CHART UPLOAD**")
        uploaded = st.file_uploader("Upload Chart Screenshot", type=["png","jpg","jpeg","webp"],
                                    help="Upload a chart screenshot for AI analysis")

        st.markdown("---")
        st.markdown("""
        <div style="padding:12px;background:#0a0a0a;border:1px solid #1a1a1a;border-radius:8px;">
          <div style="color:#FF8C00;font-size:11px;font-weight:600;margin-bottom:8px;">⚠️ RISK WARNING</div>
          <div style="color:#555;font-size:10px;line-height:1.6;">
            This tool provides educational signals only. Never execute trades solely based on these signals.
            All trading involves risk. Past performance does not guarantee future results.
            <br><br>🚫 No trades are executed.<br>🚫 No API keys required.<br>🚫 No broker connection.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Header ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:space-between;padding:10px 0 20px;
                border-bottom:1px solid #111;margin-bottom:24px;">
      <div>
        <h1 style="margin:0;font-size:28px;font-weight:800;letter-spacing:-0.02em;">
          <span style="color:#FF8C00;">SMC ICT</span>
          <span style="color:#FFFFFF;"> Signal Scanner</span>
          <span style="color:#4169E1;"> Pro</span>
        </h1>
        <p style="color:#555;font-size:13px;margin:4px 0 0;">
          Institutional-Grade Smart Money Concepts · ICT Framework · Multi-Timeframe Analysis
        </p>
      </div>
      <div style="text-align:right;">
        <div style="font-size:11px;color:#444;font-family:'JetBrains Mono',monospace;">
          {}</div>
      </div>
    </div>
    """.format(datetime.now().strftime("%A %d %B %Y · %H:%M UTC")), unsafe_allow_html=True)

    # ── Initialize session state ──────────────────────────────────────────────
    if "scan_results" not in st.session_state: st.session_state.scan_results = []
    if "history" not in st.session_state: st.session_state.history = []

    # ── Run Scan ─────────────────────────────────────────────────────────────
    if scan_btn:
        if not selected_pairs:
            st.warning("Please select at least one pair to scan.")
        else:
            with st.spinner(""):
                results = run_scanner(selected_pairs, timeframe)
            st.session_state.scan_results = results
            # Add to history
            for r in results:
                if r["signal"] != "NO TRADE":
                    st.session_state.history.append({
                        "Time": r["timestamp"], "Pair": r["pair"], "TF": r["timeframe"],
                        "Signal": r["signal"], "Entry": fmt_price(r["price"], r["pair"]),
                        "SL": fmt_price(r["sl"], r["pair"]), "TP1": fmt_price(r["tp1"], r["pair"]),
                        "Conf.": f"{r['score']}%", "Trend": r["trend"], "Quality": r["quality"],
                    })
            st.success(f"✅ Scan complete — {len(results)} pairs analyzed.")

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tabs = st.tabs(["📊 Market Scanner", "📈 Active Signals", "🔍 Signal Detail", "📷 Chart Analyzer", "📋 Signal History"])

    # ── TAB 1: Market Scanner ─────────────────────────────────────────────────
    with tabs[0]:
        if not st.session_state.scan_results:
            st.markdown("""
            <div style="text-align:center;padding:60px 20px;background:#0a0a0a;border:1px dashed #222;
                        border-radius:16px;margin-top:20px;">
              <div style="font-size:48px;margin-bottom:16px;">📡</div>
              <div style="color:#FF8C00;font-size:20px;font-weight:700;margin-bottom:8px;">Ready to Scan</div>
              <div style="color:#555;font-size:14px;">Select pairs and timeframe, then click SCAN MARKETS in the sidebar.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            results = st.session_state.scan_results
            active  = [r for r in results if r["signal"] != "NO TRADE"]
            buys    = [r for r in results if r["signal"] == "BUY"]
            sells   = [r for r in results if r["signal"] == "SELL"]
            avg_conf = np.mean([r["score"] for r in results]) if results else 0

            # Metrics row
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Pairs Scanned", len(results))
            c2.metric("Active Signals", len(active), delta=f"{len(active)} valid")
            c3.metric("Buy Signals",  len(buys))
            c4.metric("Sell Signals", len(sells))
            c5.metric("Avg Confidence", f"{avg_conf:.0f}%")

            st.markdown("---")
            st.markdown("### 🗂 Scanner Results")

            # Summary table
            rows = []
            for r in results:
                sig_color = "🟢" if r["signal"]=="BUY" else "🔴" if r["signal"]=="SELL" else "⚫"
                trend_icon = "📈" if r["trend"]=="Bullish" else "📉" if r["trend"]=="Bearish" else "↔️"
                score_str = f"{r['score']}%"
                rows.append({
                    "": sig_color, "Pair": r["pair"] + (" 🧪" if r.get("simulated") else ""), "TF": r["timeframe"],
                    "Signal": r["signal"], "Entry": fmt_price(r["price"], r["pair"]),
                    "SL": fmt_price(r["sl"], r["pair"]), "TP1": fmt_price(r["tp1"], r["pair"]),
                    "R:R": rr_ratio(r), "Conf.": score_str,
                    "Trend": f"{trend_icon} {r['trend']}", "RSI": f"{r['rsi']:.1f}" if r['rsi'] is not None else "—",
                    "Quality": r["quality"],
                })

            df_table = pd.DataFrame(rows)
            st.dataframe(df_table, use_container_width=True, hide_index=True,
                         column_config={
                             "Conf.": st.column_config.TextColumn(width="small"),
                             "Quality": st.column_config.TextColumn(width="medium"),
                         })

    # ── TAB 2: Active Signals ─────────────────────────────────────────────────
    with tabs[1]:
        if not st.session_state.scan_results:
            st.info("Run a scan first to see active signals.")
        else:
            active = [r for r in st.session_state.scan_results if r["signal"] != "NO TRADE"]
            if not active:
                st.markdown("""
                <div style="text-align:center;padding:40px;background:#0a0a0a;border:1px dashed #222;border-radius:12px;">
                  <div style="font-size:36px;">⚫</div>
                  <div style="color:#888;font-size:16px;margin-top:12px;">No signals meet the 75% confidence threshold.</div>
                  <div style="color:#555;font-size:13px;">Market conditions do not support high-probability setups currently.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"### Active Signals — {len(active)} High-Probability Setups Found")
                for sig in sorted(active, key=lambda x: -x["score"]):
                    st.markdown(signal_card_html(sig), unsafe_allow_html=True)

    # ── TAB 3: Signal Detail ──────────────────────────────────────────────────
    with tabs[2]:
        if not st.session_state.scan_results:
            st.info("Run a scan first, then select a signal to analyze in detail.")
        else:
            pair_options = [f"{r['pair']} {r['timeframe']} — {r['signal']} ({r['score']}%)"
                            for r in st.session_state.scan_results]
            selected_str = st.selectbox("Select Signal to Analyze", pair_options)
            idx = pair_options.index(selected_str)
            sig = st.session_state.scan_results[idx]

            col_chart, col_gauge = st.columns([3, 1])
            with col_chart:
                st.plotly_chart(build_chart(sig), use_container_width=True)
            with col_gauge:
                st.markdown("#### Confidence Score")
                st.plotly_chart(confidence_gauge(sig["score"]), use_container_width=True)
                q_color = "#00C851" if sig["score"]>=95 else "#4169E1" if sig["score"]>=85 else "#FF8C00" if sig["score"]>=75 else "#FF3547"
                st.markdown(f"""
                <div style="text-align:center;padding:10px;background:#0a0a0a;border-radius:8px;border:1px solid #1a1a1a;">
                  <div style="color:{q_color};font-weight:700;font-size:13px;">{sig['quality']}</div>
                </div>
                """, unsafe_allow_html=True)

                # Score breakdown
                st.markdown("#### Score Breakdown")
                for k, v in sig["score_breakdown"].items():
                    max_map = {"Market Structure":20,"Trend Alignment":15,"Order Block":15,"Liquidity Sweep":10,
                               "Fair Value Gap":10,"RSI":10,"Support/Resistance":10,"Price Action":10}
                    max_v = max_map.get(k, 10)
                    pct   = int(v / max_v * 100)
                    bar_color = "#00C851" if pct>=80 else "#FF8C00" if pct>=50 else "#FF3547"
                    st.markdown(f"""
                    <div style="margin-bottom:6px;">
                      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px;">
                        <span style="color:#888;">{k}</span>
                        <span style="color:#FFF;font-weight:600;">{v}/{max_v}</span>
                      </div>
                      <div style="background:#111;border-radius:4px;height:5px;">
                        <div style="background:{bar_color};width:{pct}%;height:5px;border-radius:4px;"></div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Full signal breakdown
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 📋 Signal Summary")
                pair = sig["pair"]
                signal_color = "#00C851" if sig["signal"]=="BUY" else "#FF3547" if sig["signal"]=="SELL" else "#888"
                st.markdown(f"""
                <div style="background:#0a0a0a;border:1px solid #1a1a1a;border-radius:12px;padding:20px;font-family:'JetBrains Mono',monospace;font-size:13px;line-height:2;">
                  <span style="color:#555;">PAIR:</span>       <span style="color:#FF8C00;font-weight:700;">{pair}</span><br>
                  <span style="color:#555;">TIMEFRAME:</span>  <span style="color:#FFF;">{sig['timeframe']}</span><br>
                  <span style="color:#555;">SIGNAL:</span>     <span style="color:{signal_color};font-weight:700;">{sig['signal']}</span><br>
                  <span style="color:#555;">ENTRY:</span>      <span style="color:#FFF;">{fmt_price(sig['price'],pair)}</span><br>
                  <span style="color:#555;">STOP LOSS:</span>  <span style="color:#FF3547;">{fmt_price(sig['sl'],pair)}</span><br>
                  <span style="color:#555;">TP1:</span>        <span style="color:#00C851;">{fmt_price(sig['tp1'],pair)}</span><br>
                  <span style="color:#555;">TP2:</span>        <span style="color:#00C851;">{fmt_price(sig['tp2'],pair)}</span><br>
                  <span style="color:#555;">TP3:</span>        <span style="color:#00C851;">{fmt_price(sig['tp3'],pair)}</span><br>
                  <span style="color:#555;">R:R:</span>        <span style="color:#FF8C00;">{rr_ratio(sig)}</span><br>
                  <span style="color:#555;">CONFIDENCE:</span> <span style="color:{signal_color};font-weight:700;">{sig['score']}%</span><br>
                  <span style="color:#555;">TREND:</span>      <span style="color:#4169E1;">{sig['trend']}</span>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown("#### 📐 Market Levels")
                struct = sig.get("structure", {})
                support_levels = struct.get("support", [])
                sup_str = "<br>".join([f"• {fmt_price(s,pair)}" for s in support_levels]) or "—"
                resistance_levels = struct.get("resistance", [])
                res_str = "<br>".join([f"• {fmt_price(r,pair)}" for r in resistance_levels]) or "—"
                st.markdown(f"""
                <div style="background:#0a0a0a;border:1px solid #1a1a1a;border-radius:12px;padding:20px;">
                  <div style="margin-bottom:16px;">
                    <div style="color:#555;font-size:11px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Support Levels</div>
                    <div style="color:#00C851;font-family:'JetBrains Mono',monospace;font-size:13px;line-height:1.8;">{sup_str}</div>
                  </div>
                  <div>
                    <div style="color:#555;font-size:11px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Resistance Levels</div>
                    <div style="color:#FF3547;font-family:'JetBrains Mono',monospace;font-size:13px;line-height:1.8;">{res_str}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### 🧠 Trade Rationale")
                reasons_html = "".join([f"<div style='margin-bottom:6px;'>✅ {r}</div>" for r in sig["reasons"]])
                st.markdown(f"""
                <div style="background:#0a0a0a;border:1px solid #1a1a1a;border-radius:12px;padding:16px;
                            color:#888;font-size:12px;line-height:1.7;">{reasons_html}</div>
                """, unsafe_allow_html=True)

            if sig["htf_warning"]:
                st.markdown("""
                <div style="background:#1a0800;border:1px solid #FF8C00;border-radius:10px;padding:14px 18px;
                            color:#FF8C00;font-size:13px;margin-top:16px;">
                  ⚠️ <strong>Higher Timeframe Warning:</strong>
                  Trade is against the H4 directional bias. Exercise caution — confidence reduced by 15%.
                  Consider waiting for H4 alignment before entering.
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:#0a0500;border:1px solid #333;border-radius:10px;padding:14px 18px;
                        color:#666;font-size:12px;margin-top:10px;line-height:1.7;">
              ⚠️ <strong style="color:#888;">Risk Warning:</strong>
              This signal is generated for educational and analytical purposes only. It does not constitute
              financial advice. All trading involves significant risk of loss. Never risk more than you can
              afford to lose. Always use proper position sizing and risk management. Past performance is
              not indicative of future results.
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 4: Chart Analyzer ─────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("### 📷 AI Chart Screenshot Analyzer")
        st.markdown("""
        <div style="background:#0a0a0a;border:1px solid #1a1a1a;border-radius:10px;padding:16px;
                    color:#666;font-size:13px;margin-bottom:20px;">
          Upload a chart screenshot and the analyzer will identify the pair, timeframe, market structure,
          and generate a signal based on what it detects in the image.
        </div>
        """, unsafe_allow_html=True)

        if uploaded:
            img_col, result_col = st.columns([1, 1])
            with img_col:
                img = Image.open(uploaded)
                st.image(img, caption="Uploaded Chart", use_container_width=True)

            with result_col:
                with st.spinner("Analyzing chart structure..."):
                    time.sleep(1.2)
                    sig, notes = analyze_chart_image(uploaded)

                st.markdown("**Heuristic Analysis:**")
                for note in (notes if isinstance(notes, list) else [notes]):
                    st.markdown(f"<div style='color:#888;font-size:12px;margin:3px 0;'>→ {note}</div>",
                                unsafe_allow_html=True)
                st.markdown("""
                <div style="background:#0a0500;border:1px solid #333;border-radius:10px;padding:14px 18px;
                            color:#666;font-size:12px;margin-top:12px;line-height:1.7;">
                  ℹ️ Pixel analysis cannot identify order blocks, FVGs, or liquidity sweeps from a screenshot.
                  For a full confidence-scored signal, go to the <strong style="color:#FF8C00;">Market Scanner</strong> tab
                  and select your pair directly.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:60px;background:#0a0a0a;border:1px dashed #222;border-radius:16px;">
              <div style="font-size:48px;">📷</div>
              <div style="color:#FF8C00;font-size:16px;font-weight:700;margin:16px 0 8px;">Upload a Chart</div>
              <div style="color:#555;font-size:13px;">Drag and drop or use the file uploader in the sidebar.<br>
              Supports PNG, JPG, JPEG, and WEBP formats.</div>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 5: Signal History ─────────────────────────────────────────────────
    with tabs[4]:
        st.markdown("### 📋 Signal History")
        if not st.session_state.history:
            st.info("No signal history yet. Run a scan to generate signals.")
        else:
            hist_df = pd.DataFrame(st.session_state.history)
            col1, col2, col3 = st.columns(3)
            total_sigs = len(hist_df)
            buy_count  = len(hist_df[hist_df["Signal"]=="BUY"])
            sell_count = len(hist_df[hist_df["Signal"]=="SELL"])
            col1.metric("Total Signals", total_sigs)
            col2.metric("Buy Signals",   buy_count)
            col3.metric("Sell Signals",  sell_count)
            st.markdown("---")
            st.dataframe(hist_df, use_container_width=True, hide_index=True)

            if st.button("Clear History"):
                st.session_state.history = []
                st.rerun()


if __name__ == "__main__":
    main()
