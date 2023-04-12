from enum import Enum
import pendulum
import requests


# status values according to NBA Api
class GameStatus(Enum):
    tbd = 0
    pending = 1
    in_progress = 2
    complete = 3


def scoreboard_request(game_date=None):
    # https://github.com/swar/nba_api/blob/05f91be1f3b66d44450a41e7ccb688d7337fa790/src/nba_api/stats/library/http.py#L100
    url = "https://stats.nba.com/stats/scoreboardV3"
    # https://github.com/swar/nba_api/blob/05f91be1f3b66d44450a41e7ccb688d7337fa790/src/nba_api/stats/library/http.py#L8
    headers = {
        'Host': 'stats.nba.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true',
        'Connection': 'keep-alive',
        'Referer': 'https://stats.nba.com/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    params = {
        # https://github.com/swar/nba_api/blob/05f91be1f3b66d44450a41e7ccb688d7337fa790/src/nba_api/stats/library/parameters.py#L172
        "DayOffset": "0",
        # https://github.com/swar/nba_api/blob/05f91be1f3b66d44450a41e7ccb688d7337fa790/src/nba_api/stats/library/parameters.py#L243
        "GameDate": game_date or str(pendulum.now("US/Pacific").date()),
        # https://github.com/swar/nba_api/blob/05f91be1f3b66d44450a41e7ccb688d7337fa790/src/nba_api/stats/library/parameters.py#L312
        "LeagueID": "00",
    }
    return requests.get(url=url, params=params, headers=headers, timeout=30)


def fetch_scoreboard(game_date=None):
    result = {
        "status": "error",
        "status_code": 500,
        "scoreboard": {}
    }

    # Fetch scoreboard for game date. Make custom NBAStatsHTTP request
    # to avoid a bunch of pandas stuff that the Scoreboard API performs.
    response = scoreboard_request(game_date)
    result["status_code"] = response.status_code

    # return scoreboard if successful
    if response.status_code == 200:
        result["status"] = "success"
        result["scoreboard"] = response.json().get("scoreboard", {})

    return result


def fetch_kings_game(game_date=None):
    # fetch scoreboard
    response = fetch_scoreboard(game_date)
    result = {
        "status": response["status"],
        "status_code": response["status_code"],
        "game": {}
    }

    # filter Kings games and return game if successful
    if result["status"] == "success":
        scoreboard = response.get("scoreboard", {})
        for game in scoreboard.get("games", []):
            home_team = game.get("homeTeam", {}).get("teamName")
            away_team = game.get("awayTeam", {}).get("teamName")
            if "Kings" in (home_team, away_team):
                result["game"] = game
                break

    return result


def game_winner(game):
    # if game status is complete, return name of team who won.
    # if game status is incomplete, return None.
    if game.get("gameStatus") == GameStatus.complete.value:
        home_team = game.get("homeTeam", {})
        away_team = game.get("awayTeam", {})
        if home_team.get("score", 0) > away_team.get("score", 0):
            return home_team.get("teamName")
        elif away_team.get("score", 0) > home_team.get("score", 0):
            return away_team.get("teamName")
        return "Tie"
    return None


# def test(game_date):
#     scoreboard = fetch_scoreboard(game_date)
#     games = scoreboard.get("scoreboard", {}).get("games", [])
#     num_completed = 0
#     for game in games:
#         winner = game_winner(game)
#         if winner:
#             num_completed += 1
#         print(winner)
#     print(f"NUM GAMES: {len(games)}")
#     print(f"NUM COMPLETED GAMES: {num_completed}")
