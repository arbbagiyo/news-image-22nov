[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/arbbagiyo/news-image-22nov/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/arbbagiyo/news-image-22nov/reward.svg)](https://make.fun/bounty/news-image-20261122)

# The World — Sunday 22 November 2026

Built for the [make.fun bounty "Sum up 22 November's world news in one image"](https://make.fun/bounty/news-image-20261122).

A newspaper front page drawn programmatically with Python + PIL (`render.py`),
1024×1024 PNG. Masthead "THE WORLD", red dateline "SUNDAY, 22 NOVEMBER 2026":

- **Main story:** Mexico captures 'El Chapo Isidro' — the FBI most-wanted
  drug lord seized in northern Mexico; 11 killed as the arrest sparks
  gunfights in Sinaloa.
- **Second story:** Gen Z protests, day two — 82,500 march in France,
  144 detained; Italy's transport strike halts trains.
- **Also:** COP31 deadlock drags into overtime, the IRGC targeting US radar
  in Bahrain, Trump vowing to cap credit-card interest at 10%, BepiColombo
  reaching Mercury — plus Brussels flight cancellations, the Gaza aid call,
  Seattle ICE arrests and the Nigeria boat toll.

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png` after checking its PNG signature and size; two runs are
byte-identical.
