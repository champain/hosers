from errbot import BotPlugin, botcmd
import requests


class Hosers(BotPlugin):
    """
    Hockey interaction plugin
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nhl_api_url = 'https://statsapi.web.nhl.com/api/v1'
        self.caps_id = 15

    def get_prev_game_id(self):
        previous_game_end = 'team.schedule.previous'
        game_id = requests.get("{}/teams/{}?expand={}".format(
            self.nhl_api_url, self.caps_id, previous_game_end)).json()
        prev_game_data = game_id['teams'][0]['previousGameSchedule']
        num_prev_games = int(len(prev_game_data['dates'])) - 1
        return prev_game_data['dates'][0]['games'][num_prev_games]['gamePk']

    def get_caps_score(self, game_id):
        game_data = requests.get("{}/game/{}/linescore".format(
            self.nhl_api_url, game_id)).json()
        home_team = game_data['teams']['home']
        away_team = game_data['teams']['away']
        home_team_name = home_team['team']['name']
        away_team_name = away_team['team']['name']
        home_team_score = home_team['goals']
        away_team_score = away_team['goals']
        if self.my_team_outcome(game_data):
            mood_string = ":fireworks:"
        else:
            mood_string = ":cry:"
        return_doc = 9*mood_string + "\n"
        return_doc += """
            The last Caps game score was:
            {} - {}
            {} - {}
            """.format(
                away_team_name,
                away_team_score,
                home_team_name,
                home_team_score).strip()
        return_doc += "\n{}".format(9*mood_string)
        return return_doc

    def my_team_outcome(self, game_data):
        if game_data['teams']['away']['team']['id'] == self.caps_id:
            my_team_key = 'away'
            bad_guys_key = 'home'
        else:
            my_team_key = 'home'
            bad_guys_key = 'away'
        my_team_score = int(game_data['teams'][my_team_key]['goals'])
        bad_guys_score = int(game_data['teams'][bad_guys_key]['goals'])
        if my_team_score < bad_guys_score:
            return False
        else:
            return True

    @botcmd()
    def caps_score(self, message, args):
        return self.get_caps_score(self.get_prev_game_id())
