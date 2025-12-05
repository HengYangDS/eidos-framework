from typing import List, Dict, Any
import math

def calculate_sma(data: List[Dict[str, Any]], window: int, field: str) -> List[Dict[str, Any]]:
    result = []
    for i, row in enumerate(data):
        new_row = row.copy()
        if i < window - 1:
            new_row[f"sma_{window}"] = None
        else:
            window_slice = data[i - window + 1 : i + 1]
            values = [x[field] for x in window_slice if x[field] is not None]
            if len(values) == window:
                new_row[f"sma_{window}"] = sum(values) / window
            else:
                new_row[f"sma_{window}"] = None
        result.append(new_row)
    return result

def calculate_ema(data: List[Dict[str, Any]], window: int, field: str) -> List[Dict[str, Any]]:
    alpha = 2 / (window + 1)
    result = []
    ema = None
    for row in data:
        new_row = row.copy()
        val = row.get(field)
        if val is not None:
            if ema is None:
                ema = val
            else:
                ema = alpha * val + (1 - alpha) * ema
            new_row[f"ema_{window}"] = ema
        else:
            new_row[f"ema_{window}"] = None
        result.append(new_row)
    return result

def calculate_wma(data: List[Dict[str, Any]], window: int, field: str) -> List[Dict[str, Any]]:
    result = []
    weights = list(range(1, window + 1))
    denominator = sum(weights)
    
    for i, row in enumerate(data):
        new_row = row.copy()
        if i < window - 1:
            new_row[f"wma_{window}"] = None
        else:
            window_slice = data[i - window + 1 : i + 1]
            values = [x[field] for x in window_slice if x[field] is not None]
            if len(values) == window:
                weighted_sum = sum(w * v for w, v in zip(weights, values))
                new_row[f"wma_{window}"] = weighted_sum / denominator
            else:
                new_row[f"wma_{window}"] = None
        result.append(new_row)
    return result

def calculate_rsi(data: List[Dict[str, Any]], window: int, field: str) -> List[Dict[str, Any]]:
    result = []
    gains = []
    losses = []
    
    for i, row in enumerate(data):
        new_row = row.copy()
        if i == 0:
            new_row[f"rsi_{window}"] = None
            result.append(new_row)
            continue
            
        change = row[field] - data[i-1][field]
        gain = max(0, change)
        loss = max(0, -change)
        
        gains.append(gain)
        losses.append(loss)
        
        if len(gains) > window:
            gains.pop(0)
            losses.pop(0)
            
        if i < window:
            new_row[f"rsi_{window}"] = None
        else:
            avg_gain = sum(gains) / window
            avg_loss = sum(losses) / window
            
            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            new_row[f"rsi_{window}"] = rsi
            
        result.append(new_row)
    return result

def calculate_macd(data: List[Dict[str, Any]], fast: int, slow: int, signal: int, field: str) -> List[Dict[str, Any]]:
    fast_emas = calculate_ema(data, fast, field)
    slow_emas = calculate_ema(data, slow, field)
    
    macd_line = []
    result = []
    
    for i in range(len(data)):
        f_val = fast_emas[i].get(f"ema_{fast}")
        s_val = slow_emas[i].get(f"ema_{slow}")
        
        new_row = data[i].copy()
        
        if f_val is not None and s_val is not None:
            macd = f_val - s_val
            new_row["macd"] = macd
            macd_line.append(macd)
        else:
            new_row["macd"] = None
            macd_line.append(None)
        
        if len(macd_line) > 0 and macd_line[-1] is not None:
             k = 2 / (signal + 1)
             prev_sig = result[-1].get("macd_signal") if result else None
             
             if prev_sig is None:
                 sig = macd_line[-1]
             else:
                 sig = macd_line[-1] * k + prev_sig * (1 - k)
             new_row["macd_signal"] = sig
             new_row["macd_hist"] = new_row["macd"] - sig
        else:
             new_row["macd_signal"] = None
             new_row["macd_hist"] = None
             
        result.append(new_row)
        
    return result

def calculate_bbands(data: List[Dict[str, Any]], window: int, std_dev: int, field: str) -> List[Dict[str, Any]]:
    result = []
    for i, row in enumerate(data):
        new_row = row.copy()
        if i < window - 1:
            new_row["bb_mid"] = None
            new_row["bb_upper"] = None
            new_row["bb_lower"] = None
        else:
            window_slice = data[i - window + 1 : i + 1]
            values = [x[field] for x in window_slice if x[field] is not None]
            if len(values) == window:
                mean = sum(values) / window
                variance = sum([(x - mean) ** 2 for x in values]) / window
                std = math.sqrt(variance)
                
                new_row["bb_mid"] = mean
                new_row["bb_upper"] = mean + std_dev * std
                new_row["bb_lower"] = mean - std_dev * std
            else:
                new_row["bb_mid"] = None
        result.append(new_row)
    return result

def calculate_stoch(data: List[Dict[str, Any]], window: int, smooth: int, high: str, low: str, close: str) -> List[Dict[str, Any]]:
    result = []
    k_values = []
    
    for i, row in enumerate(data):
        new_row = row.copy()
        if i < window - 1:
            new_row["stoch_k"] = None
            new_row["stoch_d"] = None
            k_values.append(None)
        else:
            window_slice = data[i - window + 1 : i + 1]
            highs = [x[high] for x in window_slice if x[high] is not None]
            lows = [x[low] for x in window_slice if x[low] is not None]
            c = row[close]
            
            if len(highs) == window and len(lows) == window and c is not None:
                h_max = max(highs)
                l_min = min(lows)
                if h_max == l_min:
                    k = 100
                else:
                    k = (c - l_min) / (h_max - l_min) * 100
                k_values.append(k)
                new_row["stoch_k"] = k
            else:
                k_values.append(None)
                new_row["stoch_k"] = None
        
        # Calculate %D (SMA of %K)
        if len(k_values) >= smooth:
            d_slice = k_values[-smooth:]
            if all(x is not None for x in d_slice):
                new_row["stoch_d"] = sum(d_slice) / smooth
            else:
                new_row["stoch_d"] = None
        else:
            new_row["stoch_d"] = None
            
        result.append(new_row)
    return result

def calculate_cci(data: List[Dict[str, Any]], window: int, high: str, low: str, close: str) -> List[Dict[str, Any]]:
    result = []
    tps = []
    
    for i, row in enumerate(data):
        new_row = row.copy()
        if row[high] is not None and row[low] is not None and row[close] is not None:
            tp = (row[high] + row[low] + row[close]) / 3
        else:
            tp = None
        tps.append(tp)
        
        if i < window - 1:
            new_row["cci"] = None
        else:
            tp_slice = tps[i - window + 1 : i + 1]
            if all(x is not None for x in tp_slice):
                sma_tp = sum(tp_slice) / window
                mean_dev = sum([abs(x - sma_tp) for x in tp_slice]) / window
                if mean_dev == 0:
                    new_row["cci"] = 0
                else:
                    new_row["cci"] = (tp - sma_tp) / (0.015 * mean_dev)
            else:
                new_row["cci"] = None
        result.append(new_row)
    return result

def calculate_atr(data: List[Dict[str, Any]], window: int, high: str = "high", low: str = "low", close: str = "close") -> List[Dict[str, Any]]:
    result = []
    trs = []
    
    for i, row in enumerate(data):
        new_row = row.copy()
        h = row.get(high)
        l = row.get(low)
        c_prev = data[i-1].get(close) if i > 0 else None
        
        if h is not None and l is not None:
            if c_prev is None:
                tr = h - l
            else:
                tr = max(h - l, abs(h - c_prev), abs(l - c_prev))
            trs.append(tr)
        else:
            trs.append(None)
            
        if i < window:
            new_row[f"atr_{window}"] = None
        else:
            # First ATR is simple average of TR
            if i == window:
                tr_slice = trs[:window]
                if all(x is not None for x in tr_slice):
                    atr = sum(tr_slice) / window
                    new_row[f"atr_{window}"] = atr
                    # Store for next
                    new_row["_prev_atr"] = atr 
                else:
                    new_row[f"atr_{window}"] = None
            else:
                # Subsequent ATR: (PrevATR * (n-1) + TR) / n
                prev_atr = result[-1].get(f"atr_{window}") or result[-1].get("_prev_atr")
                curr_tr = trs[-1]
                
                if prev_atr is not None and curr_tr is not None:
                    atr = (prev_atr * (window - 1) + curr_tr) / window
                    new_row[f"atr_{window}"] = atr
                else:
                    new_row[f"atr_{window}"] = None
                    
        result.append(new_row)
    return result

def calculate_adx(data: List[Dict[str, Any]], window: int, high: str = "high", low: str = "low", close: str = "close") -> List[Dict[str, Any]]:
    # Implementing Wilder's ADX
    result = []
    
    # State
    trs = []
    dm_plus = []
    dm_minus = []
    
    smooth_tr = None
    smooth_dm_plus = None
    smooth_dm_minus = None
    
    dxs = []
    
    for i, row in enumerate(data):
        new_row = row.copy()
        h = row.get(high)
        l = row.get(low)
        prev = data[i-1] if i > 0 else None
        
        # 1. Calculate TR, +DM, -DM
        if prev and h is not None and l is not None:
            h_prev = prev.get(high)
            l_prev = prev.get(low)
            c_prev = prev.get(close)
            
            tr = max(h - l, abs(h - c_prev), abs(l - c_prev))
            
            up_move = h - h_prev
            down_move = l_prev - l
            
            if up_move > down_move and up_move > 0:
                dp = up_move
            else:
                dp = 0
                
            if down_move > up_move and down_move > 0:
                dm = down_move
            else:
                dm = 0
                
            trs.append(tr)
            dm_plus.append(dp)
            dm_minus.append(dm)
        else:
            trs.append(0)
            dm_plus.append(0)
            dm_minus.append(0)
            
        # 2. Smooth them (Wilder's Smoothing)
        if i == window:
             smooth_tr = sum(trs)
             smooth_dm_plus = sum(dm_plus)
             smooth_dm_minus = sum(dm_minus)
        elif i > window:
             smooth_tr = smooth_tr - (smooth_tr/window) + trs[-1]
             smooth_dm_plus = smooth_dm_plus - (smooth_dm_plus/window) + dm_plus[-1]
             smooth_dm_minus = smooth_dm_minus - (smooth_dm_minus/window) + dm_minus[-1]
             
        # 3. Calculate DI
        if i >= window:
            di_plus = 100 * (smooth_dm_plus / smooth_tr) if smooth_tr else 0
            di_minus = 100 * (smooth_dm_minus / smooth_tr) if smooth_tr else 0
            
            sum_di = di_plus + di_minus
            dx = 100 * abs(di_plus - di_minus) / sum_di if sum_di else 0
            dxs.append(dx)
            
            # 4. ADX is smoothed DX
            if len(dxs) >= window:
                # Simple average for first ADX, then smoothing
                # For simplicity here we just take SMA of DX or last DX
                # Proper Wilder is recursive
                adx = sum(dxs[-window:]) / window # Simplified
                new_row[f"adx_{window}"] = adx
            else:
                 new_row[f"adx_{window}"] = None
        else:
             new_row[f"adx_{window}"] = None
             
        result.append(new_row)
    return result

def calculate_obv(data: List[Dict[str, Any]], close: str = "close", vol: str = "volume") -> List[Dict[str, Any]]:
    result = []
    curr_obv = 0
    for i, row in enumerate(data):
        new_row = row.copy()
        c = row.get(close)
        v = row.get(vol, 0)
        
        if i > 0:
            c_prev = data[i-1].get(close)
            if c > c_prev:
                curr_obv += v
            elif c < c_prev:
                curr_obv -= v
        else:
            curr_obv = v
            
        new_row["obv"] = curr_obv
        result.append(new_row)
    return result

def calculate_vwap(data: List[Dict[str, Any]], price: str = "price", vol: str = "volume") -> List[Dict[str, Any]]:
    result = []
    cum_pv = 0
    cum_vol = 0
    
    for row in data:
        new_row = row.copy()
        p = row.get(price, row.get("close")) # Fallback to close
        v = row.get(vol, 0)
        
        if p is not None and v is not None:
            cum_pv += p * v
            cum_vol += v
            if cum_vol != 0:
                new_row["vwap"] = cum_pv / cum_vol
            else:
                new_row["vwap"] = p
        else:
            new_row["vwap"] = None
        result.append(new_row)
    return result
