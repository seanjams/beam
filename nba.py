from enum import Enum
from nba_api.stats.library.http import NBAStatsHTTP
from nba_api.stats.library.parameters import DayOffset, GameDate, LeagueID


# status values according to NBA Api
class GameStatus(Enum):
    tbd = 0
    pending = 1
    in_progress = 2
    complete = 3


class GameResult(Enum):
    pending = "pending"
    won = "won"
    lost = "lost"


def fetch_scoreboard(game_date=None):
    # Use today's date by default
    if not game_date:
        # game_date = pendulum.now("US/Pacific").format("YYYY-MM-DD")
        game_date = GameDate.default

    result = {
        "status": "error",
        "status_code": 500,
        "scoreboard": {}
    }

    # Fetch scoreboard for game date. Make custom NBAStatsHTTP request
    # to avoid a bunch of pandas stuff that the Scoreboard API performs.
    response = NBAStatsHTTP().send_api_request(
        endpoint="scoreboardV3",
        parameters={
            'DayOffset': DayOffset.default,
            'GameDate': game_date or GameDate.default,
            'LeagueID': LeagueID.default
        },
        timeout=30,
    )
    result["status_code"] = response._status_code

    # return scoreboard if successful
    if response._status_code == 200:
        result["status"] = "success"
        result["scoreboard"] = response.get_dict().get("scoreboard", {})

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
