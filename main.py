import json
import math
import os
from pathlib import Path

IN_DIR = Path(os.environ.get('MAKEFUN_INPUT_DIR', '/input'))
OUT_DIR = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
TAUS = (0.05, 0.25, 0.50, 0.75, 0.95)
ZS = (-1.645, -0.674, 0.0, 0.674, 1.645)


def logv(x):
    return math.log(max(1.0, float(x)))


def median(xs):
    a = sorted(xs)
    n = len(a)
    return a[n // 2] if n % 2 else (a[n // 2 - 1] + a[n // 2]) / 2


def robust_scale(xs):
    m = median(xs)
    return max(0.12, 1.4826 * median([abs(x - m) for x in xs]))


def is_rolling(c):
    return 'midnight local' in str(c.get('unlock', '')).lower() or 'rolling' in str(c.get('unlock', '')).lower()


def ratios(case):
    first = max(1.0, float(case['known'][0]['viewers']))
    rows = []
    for c in case.get('comparables', []):
        vals = c.get('hourly') or []
        d0 = case['day_start'][:10]
        same_day = [r for r in vals if r.get('from', '').startswith(d0)]
        if not same_day:
            continue
        base = max(1.0, float(same_day[0]['viewers']))
        # GTA VI's pre-release category curve is a uniquely direct signal; other launches
        # teach the shape, not the absolute Twitch audience.
        gta = 'grand theft auto vi' in c.get('name', '').lower()
        for r in same_day[1:24]:
            h = int(r['from'][11:13]) + 1
            if 2 <= h <= 24:
                ratio = math.log(max(1.0, float(r['viewers'])) / base)
                weight = 2.5 if gta else 1.0
                if 'early-access-contaminated' in str(c.get('source', '')).lower():
                    weight *= 0.55
                # Rolling console launches are closest to this worldwide staggered unlock.
                if is_rolling(c):
                    weight *= 1.35
                rows.append((h, ratio, weight))
    return first, rows


def forecast(case):
    p1, history_ratios = ratios(case)
    all_logs = [logv(r['viewers']) for r in case.get('history_hourly', []) if r.get('viewers') is not None]
    # Estimate launch-specific pre-hour trend from the last six hours; constrain noisy slopes.
    recent = all_logs[-7:]
    slope = median([recent[i] - recent[i - 1] for i in range(1, len(recent))]) if len(recent) > 1 else 0.0
    slope = max(-0.10, min(0.10, slope))
    # During hour one, a rise/fall is informative but not extrapolated indefinitely.
    known_reads = case['known'][0].get('reads', 60)
    read_count = max(1, int(known_reads))
    hour_shape = {}
    for h in range(2, 25):
        vals = [(x, w) for hh, x, w in history_ratios if hh == h]
        if vals:
            vals.sort(key=lambda pair: pair[0])
            # Weighted median by launch shape samples, with the direct GTA curve included.
            total = sum(w for _, w in vals)
            acc = 0.0
            shape = vals[-1][0]
            for x, w in vals:
                acc += w
                if acc >= total / 2:
                    shape = x
                    break
        else:
            shape = -0.015 * (h - 1)
        # Regularize the historical cross-title shape toward a mild decay, increasing with horizon.
        shape = 0.82 * shape + 0.18 * (-0.012 * (h - 1))
        center = logv(p1) + shape + slope * min(3.0, math.sqrt(h - 1))
        # Spread grows with horizon; empirical launch-to-launch residuals add honest tail width.
        hourly_resid = [x for hh, x, _ in history_ratios if hh == h]
        spread = max(0.20, 0.13 * math.sqrt(h - 1), robust_scale(hourly_resid) if len(hourly_resid) >= 8 else 0.0)
        # Minute aggregation makes the first-hour level more reliable when reads are complete.
        spread *= 1.0 + 0.12 * max(0, 60 - read_count) / 60
        q = [max(1.01, min(1e9, math.exp(center + z * spread))) for z in ZS]
        hour_shape[h] = [round(v, 4) for v in q]
    return {'hours': [{'hour': row['hour'], 'q': hour_shape[row['hour']]} for row in case['forecast']]}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(IN_DIR.glob('*.in')):
        case = json.loads(path.read_text(encoding='utf-8'))
        result = forecast(case)
        (OUT_DIR / (path.stem + '.out')).write_text(json.dumps(result, separators=(',', ':')) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
