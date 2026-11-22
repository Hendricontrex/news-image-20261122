[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Hendricontrex/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Hendricontrex/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

# The World in One Day — Sunday 22 November 2026

A make.fun entry for
[news-image-20261122](https://make.fun/bounty/news-image-20261122): one image
that sums up the world's news of Sunday 22 November 2026.

## The six stories

1. **COP31, Antalya** — climate talks spill into a second day of overtime;
   a new draft deal aims to avert collapse over fossil fuels and funding.
2. **Mexico** — top drug lord Fausto Isidro Meza Flores ("El Chapo Isidro")
   captured in a shoot-out; 11 killed in the operation.
3. **Gulf / Bahrain** — Iranian attack sets fire to a civilian industrial
   site; two oil tankers hit near the Strait of Hormuz.
4. **The Hague** — the ICJ rules 9-6 that Myanmar committed genocide
   against the Rohingya in 2017, a first for a state.
5. **Peru** — a magnitude 6.8 earthquake shakes the central Andean region.
6. **Gaza** — winter storms flood shelters for over a million displaced
   people; Australia, Canada, Italy and the UK call for aid access.

## How it is made

`compose.py` draws the front page with Pillow only (no network, no
downloaded images): masthead naming the day, a hero story, four panels and
a bottom strip, all text set from the script so it stays legible. `main.ts`
copies the finished `entry.png` to the output directory.

```sh
python3 compose.py        # regenerates entry.png (1024x1024, PNG)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Sources for the day's events: BBC, Reuters, Al Jazeera, Xinhua.
