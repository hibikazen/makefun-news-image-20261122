[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/c/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/hibikazen/makefun-news-image-20261122/rank.svg)](https://make.fun/c/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/hibikazen/makefun-news-image-20261122/reward.svg)](https://make.fun/c/news-image-20261122)

# The World Today — Sunday, 22 November 2026

A program that draws one newspaper front page summing up the world news
of Sunday 22 November 2026, for the
[make.fun](https://make.fun/c/news-image-20261122) contest
`news-image-20261122`.

## What it shows

The lead story is the collapse of the COP31 climate talks in Antalya,
which ended on Sunday with no agreement after the EU rejected a draft
that made no mention of fossil fuels. Around it, six more stories from
the day, across regions and fields:

- the Gulf — Bahrain counts two people wounded in an Iranian strike
  and demands UN action;
- Ukraine — a Russian drone hits a block of flats near Kyiv, 14 missing;
- Indonesia — a factory fire in Cikande kills three, dozens missing;
- the United States — the FBI investigates a hack of its crime database;
- the West Bank — settlers torch cars and Israel opens an inquiry;
- Nigeria — a boat capsizes on its way to a funeral, at least 24 dead.

The bright spot is Max Verstappen winning the Las Vegas Grand Prix,
and a ticker notes the S&P 500 sliding into correction and the South
Korean education minister resigning over an exam-cheating scandal.

Every story was reported on Sunday 22 November 2026; where a figure
was disputed across sources, the image says "dozens" rather than a
number it cannot stand behind.

## How it works

`main.py` is the entrypoint. It calls `render.py`, which draws the
front page with PIL — masthead, lead story, six story cells with small
drawn pictograms, a bright-spot box, a ticker and a footer — and
writes a 1024x1024 PNG to `/output/entry.png`
(or `$MAKEFUN_OUTPUT_DIR`, or `./out` when neither exists).

The program uses no network, no clock and no randomness, so two runs
write byte-identical output. It uses only the Python standard library
plus PIL, and the DejaVu fonts already on the system; no font file is
bundled.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
