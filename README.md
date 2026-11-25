# The World Today — Wednesday, 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/CHEN19840723/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/CHEN19840723/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Entry for make.fun's **news-image-20261125** bounty: "Sum up 25 November's world news in one image" ($100 prize pool: $20 / $12 / $6 / $2 × 7 / $1.20 × 40).

## What the image shows

Built from reports published by Wednesday morning, 25 November 2026: China's Shenzhou-24 launches at 08:18 carrying Pakistan's first astronaut, Muhammad Zeeshan Ali, to the Tiangong station — the first foreign astronaut aboard it; a Brooklyn jury finds Huawei guilty on 10 of 12 counts (bank fraud, trade-secret theft) but acquits it of racketeering; Houthi fighters strike Riyadh's tallest tower for the second time in under a week, wounding at least 11; and President Zelenskiy confirms Ukraine was behind Saturday's drone strike on a Russian cargo ship in the Gulf of Finland — plus a ticker of the day so far (Giuliani's Medal of Freedom, the Sarkozy case going to trial, a CIA/ODNI cyber breach, a 5.6 Nepal quake, chess Game 1 drawn, Malaysia's Rohingya returns, AIDS deaths at a 20-year low, the Nasdaq slide, and the Cartagena hostages). Every fact was verified against a real source; see BUILD_NOTES.md.

## Run it

```sh
python3 main.py            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies `entry.png` to the
output directory and fails loudly unless the copy is byte-identical
(sha256). Run it twice and the two outputs have the same sha256.

## Files

- `entry.png` — the 1024×1024 front page (≤ 1 MiB), drawn fresh with PIL
- `main.py` — the entry program
- `render.py` — the script that drew `entry.png`
- `BUILD_NOTES.md` — stories, sources, and verification checks

## Referral

Built with [make.fun](https://make.fun/r/j755r6jc) — join with referral code `j755r6jc`.
