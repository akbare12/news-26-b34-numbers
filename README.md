# news-26-b34-numbers — The World in One Page (26 November 2026)

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/akbare12/news-26-b34-numbers/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/akbare12/news-26-b34-numbers/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One image that sums up Thursday, 26 November 2026 — **50 stories** on a single
1024×1024 page: 3 heroes + 10 cards + 37 ALSO items.

## Layout V32 — ALSO-first (new)

This layout puts the ALSO band **first**, directly under the DATE CHECK —
a structure not used by V1–V31:

1. Masthead + DATE CHECK (2 lines, excludes non-26-Nov stories by name)
2. **ALSO TODAY — 37 more stories, 3 columns** (top band)
3. Three heroes side by side (art on top, text below)
4. Ten cards (2 rows × 5)
5. World-map strip with pins at the real locations
6. Timeline strip + footer with sources

Map pins: NYC, Hormuz, Riyadh, Jerusalem, Gaza, Kyiv, Cologne, London,
Moscow, Pyongyang, Bangkok, Bogor, Washington — close pins are nudged
with leader lines so no two labels overlap.

## Heroes

1. **Macy's 100th Thanksgiving Parade postponed** — first weather
   postponement ever; gusts 60 mph; back Sat 28 Nov 08:30 ET. [C]
2. **IRGC claims 2 tankers hit by mines in Hormuz** — one a supertanker
   carrying over 2M barrels; claim unverified. [CL]
3. **Markets rebound as Trump tariff salvo lands softer than feared** —
   STOXX +1.6%; 14 partners; China 20%. [C]

Bogor's flooded illegal gold mine (13 dead, 13 missing) is a card.
Every item carries a literal tag: `[C]` confirmed, `[R]` reported,
`[CL]` claim — unverified. Items from 25 Nov are marked with the date.

## Cards (10)

Deir al-Balah (Gaza strike) · Kyiv (mall hit) · Bogor (mine flood) ·
Jerusalem (Netanyahu Case 4000) · Pyongyang (Kim nuclear tour) ·
Washington (FCC clears SpaceX 1M satellites) · London (UK migration
77,000) · Moscow (record military budget) · Bangkok (oil depot blast) ·
Cologne (synagogue plot arrests).

## Date check

26 November 2026 is a **Thursday**. Excluded from this page (not 26 Nov):
COP31 (22 Nov), Shenzhou-24 (25 Nov), Cairo tanker (25 Nov),
Cartagena hostages (25 Nov).

## How it is built

- `gen.py` renders `entry.png` at build time with Pillow (1024×1024).
  Every string is measured with real font metrics against its real column
  width — no truncation, no ellipsis. A duplicate scan (≥3 distinctive
  words shared with any hero/card/other ALSO item) must report 0 flags,
  hero stat numbers appear in exactly one place, and Philadelphia
  appears exactly once.
- `main.py` is **stdlib-only** (`os`/`shutil`/`hashlib`): the grader runs
  it with no third-party packages installed, from any working directory,
  and it copies the pre-rendered `entry.png` into
  `$MAKEFUN_OUTPUT_DIR/entry.png`, verifying size and SHA-256.

## Verification

- `entry.png`: 1024×1024 RGB
- SHA-256: `8eb8173a76f7aab508a2353b081af38db4bd57f15d2397b16caf3a99aae4229d`
- Size: 218698 bytes
- Stories: 50 (3 heroes + 10 cards + 37 ALSO)
- Stdlib-venv simulation: `import PIL` raises `ModuleNotFoundError`,
  `main.py` exits 0 from a different cwd into an empty output dir,
  output SHA-256 matches the source.

## License

MIT — see [LICENSE](LICENSE).
