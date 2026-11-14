# Codebook
Unit: one player-season, assigned to one dominant top-five league.
Coverage: seasons starting 2015 through 2024; observations need 900 minutes in their assigned league.
Source: https://github.com/dcaribou/transfermarkt-datasets (CC0 collection; derived from Transfermarkt).
Downloaded 2026-11-13. Exact raw sources and checksums: source_manifest.json.

| Field | Meaning / unit |
|---|---|
| player_id | Source player identifier; repeated across seasons |
| season | Starting calendar year (2015 = 2015/16) |
| competition_id | GB1 England, ES1 Spain, IT1 Italy, L1 Germany, FR1 France |
| minutes | Sum of league minutes in assigned league and season |
| goals | Sum of league goals in assigned league and season |
| assists | Sum of league assists in assigned league and season |
| valuation_date | Latest valuation date in Jan-Jul of season+1 |
| market_value_eur | Positive Transfermarkt estimated value in nominal euros, not transfer fee |
| name | Player name from source profile |
| date_of_birth | Source date of birth |
| position | Profile category: Attack, Midfield, Defender, Goalkeeper; not historical position |
| age | Completed years on Jan 1 of season+1 |
| league | League name corresponding to competition_id |
| premier_league | 1 for GB1; 0 for other four leagues |
| log_value | Natural log of market_value_eur |
| goals_per90 | 90 * goals / minutes |
| assists_per90 | 90 * assists / minutes |

Preparation joins appearances to games by game_id, then aggregates by player/season/league.
Only league competition IDs above are retained. Select highest-minute league before imposing the 900-minute threshold.
Ties are broken by ascending competition code. Goals/minutes/assists from a second league are not included.
Match dates do not determine season: source game season labels are used, including pandemic-delayed games.
Valuations are joined by player and season, not current club; valuation club may differ following a transfer.
The Jan-Jul proxy need not be after a player's final game and can include summer transfers.
Keep latest valuation in the window, then discard missing/nonpositive values; do not fall back to an earlier positive value.
Drop missing birthdate/age and unrecognized position (including the source literal 'Missing').
Other leagues are pooled at observation level; players with more eligible seasons contribute more observations.
Figure 1 shows empirical 10th/25th/50th/75th/90th percentiles, with a log10 axis in EUR millions.
Figure 2 shows medians by position and Premier League indicator.
No missing-value imputation, inflation adjustment, fitted models, p-values or causal identification.

Attrition: 26,273 dominant-league player-seasons; 16,037 meet the minute rule;
82 removed for valuation; 10 for demographics/position; final 15,945, covering 4,976 players.
