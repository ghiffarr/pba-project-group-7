# Codebook: `data/player_seasons.csv`

**Source.** [transfermarkt-datasets](https://github.com/dcaribou/transfermarkt-datasets), a public, weekly-updated dataset built by scraping [transfermarkt.com](https://www.transfermarkt.com). Licensed CC0 1.0 (public domain), so the cleaned file can be shared in our public repository. Built by `01_build_data.R` from four raw tables: `players`, `player_valuations`, `appearances`, `games`.

**How the original data were collected.** Transfermarkt records match line-ups and events for professional football. Market values are estimates set by Transfermarkt's editors after community discussion; they are not actual transfer fees.

**Unit of observation.** One player in one season in one of the top-five European leagues.

**Period.** 2015/16 to 2025/26 seasons.

**Sample rules.** League matches only (no cups or European competitions). Players with at least 900 league minutes in the season. Players who changed between two top-five leagues mid-season are counted in the league where they played the most minutes. Market value is the last valuation recorded between 1 January and 31 July at the end of the season.

| Variable | Meaning | Unit / values |
|---|---|---|
| `player_id` | Transfermarkt player identifier | integer |
| `player_name` | Player name | text |
| `season` | Season start year (2023 = 2023/24) | year |
| `season_label` | Season as text | e.g. "2023/24" |
| `league` | League the player played in that season | Premier League, La Liga, Serie A, Bundesliga, Ligue 1 |
| `competition_id` | Transfermarkt league code | GB1, ES1, IT1, L1, FR1 |
| `premier_league` | Played in the Premier League (key explanatory variable) | 1 = yes, 0 = no |
| `position` | Main position | Goalkeeper, Defender, Midfield, Attack |
| `sub_position` | Detailed position | e.g. Centre-Back, Left Winger |
| `foot` | Preferred foot | left, right, both |
| `height_in_cm` | Height | centimetres |
| `citizenship` | Country of citizenship | text |
| `age` | Age on 1 January of the season | years |
| `games` | League appearances in the season | count |
| `minutes` | League minutes played | minutes |
| `goals` | League goals | count |
| `assists` | League assists | count |
| `goals_per90` | Goals per 90 minutes played | goals per 90 min |
| `assists_per90` | Assists per 90 minutes played | assists per 90 min |
| `market_value_eur` | End-of-season Transfermarkt market value (outcome) | euros |
| `value_m_eur` | Same, in millions | million euros |
| `log_value` | Natural log of `market_value_eur` | log euros |
| `value_date` | Date of the valuation used | date |
