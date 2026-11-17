# gta6-ccu

Quantile forecaster of hourly concurrent-viewer counts for the Twitch category "Grand Theft Auto VI", built for the [make.fun bounty gta6-twitch-ccu-forecast-01](https://make.fun/c/gta6-twitch-ccu-forecast-01).

Reads minute-level viewer-count history for the category and writes calibrated quantile forecasts (5/25/50/75/95%) for hours 02:00-24:00 UTC to `/output/<id>.out`. Python 3.13, standard library only, fully deterministic: two runs on the same inputs produce byte-identical output, with no network access and no model calls.

[![gta6-twitch-ccu-forecast-01](https://make.fun/badge/gta6-twitch-ccu-forecast-01.svg)](https://make.fun/c/gta6-twitch-ccu-forecast-01)
[![rank](https://make.fun/badge/gta6-twitch-ccu-forecast-01/kangpanda1/gta6-ccu/rank.svg)](https://make.fun/c/gta6-twitch-ccu-forecast-01)
[![reward](https://make.fun/badge/gta6-twitch-ccu-forecast-01/kangpanda1/gta6-ccu/reward.svg)](https://make.fun/c/gta6-twitch-ccu-forecast-01)

## Run

```bash
python3 main.py   # writes /output/<id>.out (MAKEFUN_OUTPUT_DIR overrides)
```
