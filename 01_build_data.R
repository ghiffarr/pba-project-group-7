# Builds data/player_seasons.csv: one row per player per season,
# top five European leagues, 2015/16 to 2025/26.
# Source: transfermarkt-datasets (github.com/dcaribou/transfermarkt-datasets), CC0.

library(tidyverse)

# Settings
first_season <- 2015   # 2015/16 season
last_season  <- 2025   # 2025/26 season (last complete season)
min_minutes  <- 900    # keep players with at least 10 full games of league play

top5 <- tribble(
  ~competition_id, ~league,
  "GB1",           "Premier League",
  "ES1",           "La Liga",
  "IT1",           "Serie A",
  "L1",            "Bundesliga",
  "FR1",           "Ligue 1"
)

# download the raw tables
raw_dir  <- "data_raw"
base_url <- "https://pub-e682421888d945d684bcae8890b0ec20.r2.dev/data/"
tables   <- c("players", "player_valuations", "appearances", "games")

dir.create(raw_dir, showWarnings = FALSE)
dir.create("data",  showWarnings = FALSE)
options(timeout = 900)

for (t in tables) {
  dest <- file.path(raw_dir, paste0(t, ".csv.gz"))
  if (!file.exists(dest)) {
    download.file(paste0(base_url, t, ".csv.gz"), dest, mode = "wb")
  }
}

players     <- read_csv(file.path(raw_dir, "players.csv.gz"),           show_col_types = FALSE)
valuations  <- read_csv(file.path(raw_dir, "player_valuations.csv.gz"), show_col_types = FALSE)
appearances <- read_csv(file.path(raw_dir, "appearances.csv.gz"),       show_col_types = FALSE)
games       <- read_csv(file.path(raw_dir, "games.csv.gz"),             show_col_types = FALSE)

# league games in the top five leagues
league_games <- games |>
  filter(competition_id %in% top5$competition_id,
         season >= first_season, season <= last_season) |>
  select(game_id, season)

# each player's league performance per season
perf <- appearances |>
  select(game_id, player_id, competition_id, goals, assists, minutes_played) |>
  inner_join(league_games, by = "game_id") |>
  group_by(player_id, season, competition_id) |>
  summarise(
    games   = n(),
    minutes = sum(minutes_played, na.rm = TRUE),
    goals   = sum(goals,          na.rm = TRUE),
    assists = sum(assists,        na.rm = TRUE),
    .groups = "drop"
  ) |>
  
  # some players move between two top-five leagues mid-season so
  # we Keep the league where they played the most minutes.
  group_by(player_id, season) |>
  slice_max(minutes, n = 1, with_ties = FALSE) |>
  ungroup()

# End-of-season market value
# we use the last valuation recorded between 1 January and 31 July at the end of
# the season, so it reflects that season's performance.
# Example: valuations dated Jan-Jul 2024 belong to the 2023/24 season (= 2023).
end_values <- valuations |>
  mutate(date = as.Date(date)) |>
  filter(month(date) <= 7) |>
  mutate(season = year(date) - 1) |>
  group_by(player_id, season) |>
  slice_max(date, n = 1, with_ties = FALSE) |>
  ungroup() |>
  select(player_id, season, value_date = date, market_value_eur = market_value_in_eur)

# player characteristics
player_info <- players |>
  select(player_id,
         player_name   = name,
         date_of_birth,
         position,
         sub_position,
         foot,
         height_in_cm,
         citizenship   = country_of_citizenship) |>
  mutate(date_of_birth = as.Date(date_of_birth))

# combine it into one player_season table 
player_seasons <- perf |>
  inner_join(end_values, by = c("player_id", "season")) |>
  left_join(player_info, by = "player_id") |>
  left_join(top5,        by = "competition_id") |>
  mutate(
    season_label   = paste0(season, "/", str_sub(season + 1, 3, 4)),
    age            = as.numeric(make_date(season + 1, 1, 1) - date_of_birth) / 365.25,
    premier_league = as.integer(league == "Premier League"),
    goals_per90    = goals   / minutes * 90,
    assists_per90  = assists / minutes * 90,
    value_m_eur    = market_value_eur / 1e6,
    log_value      = log(market_value_eur)
  ) |>
  filter(
    minutes >= min_minutes,
    market_value_eur > 0,
    !is.na(age),
    !is.na(position), position != "Missing"
  ) |>
  select(player_id, player_name, season, season_label, league, competition_id,
         premier_league, position, sub_position, foot, height_in_cm, citizenship,
         age, games, minutes, goals, assists, goals_per90, assists_per90,
         market_value_eur, value_m_eur, log_value, value_date) |>
  arrange(season, league, desc(market_value_eur))

write_csv(player_seasons, "data/player_seasons.csv")

# check data overview for proposal use
cat("\ndata overview\n")
cat("Rows (player-seasons):", nrow(player_seasons), "\n")
cat("Distinct players:     ", n_distinct(player_seasons$player_id), "\n")
cat("Seasons:              ", min(player_seasons$season_label), "to",
                              max(player_seasons$season_label), "\n")
cat("File size (MB):       ",
    round(file.size("data/player_seasons.csv") / 1e6, 1), "\n\n")

cat("Rows by league:\n")
print(count(player_seasons, league))

cat("\nRows by position:\n")
print(count(player_seasons, position))

cat("\nMarket value (million EUR) by league:\n")
player_seasons |>
  group_by(league) |>
  summarise(n = n(),
            median_value = median(value_m_eur),
            mean_value   = mean(value_m_eur),
            mean_age     = mean(age)) |>
  arrange(desc(median_value)) |>
  print()

cat("\nMissing values in each column:\n")
player_seasons |>
  summarise(across(everything(), ~ sum(is.na(.x)))) |>
  pivot_longer(everything(), names_to = "column", values_to = "n_missing") |>
  filter(n_missing > 0) |>
  print(n = Inf)
