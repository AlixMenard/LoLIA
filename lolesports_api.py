import json, datetime
import requests
import requests as _requests
from datetime import datetime as _datetime, timedelta as _timedelta

def get_latest_date():
    now = datetime.datetime.now(datetime.timezone.utc)
    now = now - datetime.timedelta(
        seconds=now.second,
        microseconds=now.microsecond
    )
    now_string = now.isoformat()
    return str(now_string).replace('+00:00', 'Z')

class Lolesports_API:
    API_KEY = {'x-api-key': '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'}
    API_URL = 'https://esports-api.lolesports.com/persisted/gw'
    LIVESTATS_API = 'https://feed.lolesports.com/livestats/v1'
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.API_KEY)

    def get_leagues(self, hl='en-US'):
        response =  self.session.get(
            self.API_URL + '/getLeagues',
            params={'hl': hl}
        )

        return json.loads(response.text)['data']

    def get_tournaments_for_league(self, hl='en-US', league_id=None):
        response = self.session.get(
            self.API_URL + '/getTournamentsForLeague',
            params={
                'hl': hl,
                'leagueId': league_id
            }
        )

        return json.loads(response.text)['data']

    def get_standings(self, hl='en-US', tournament_id=None):
        response = self.session.get(
            self.API_URL + '/getStandings',
            params={
                'hl': hl,
                'tournamentId': tournament_id
            }
        )

        return json.loads(response.text)['data']
    
    def get_schedule(self, hl='en-US', league_id=None, pageToken=None):
        response = self.session.get(
            self.API_URL + '/getSchedule',
            params={
                'hl': hl,
                'leagueId': league_id,
                'pageToken': pageToken
            }
        )

        return json.loads(response.text)['data']

    def get_live(self, hl='en-US'):
        response = self.session.get(
            self.API_URL + '/getLive',
            params={'hl': hl}
        )

        return json.loads(response.text)['data']

    def get_completed_events(self, hl='en-US', tournament_id=None):
        response = self.session.get(
            self.API_URL + '/getCompletedEvents',
            params={
                'hl': hl,
                'tournamentId': tournament_id
            }
        )

        return json.loads(response.text)['data']

    def get_event_details(self, match_id, hl='en-US'):
        response = self.session.get(
            self.API_URL + '/getEventDetails',
            params={
                'hl': hl,
                'id': match_id
            }
        )

        return json.loads(response.text)['data']

    def get_games(self, hl='en-US', match_id=None):
        response = self.session.get(
            self.API_URL + '/getGames',
            params={
                'hl': hl,
                'id': match_id
            }
        )

        return json.loads(response.text)['data']

    def get_teams(self, hl='en-US', team_slug=None):
        response = self.session.get(
            self.API_URL + '/getTeams',
            params={
                'hl': hl,
                'id': team_slug
            }
        )

        return json.loads(response.text)['data']

    def get_window(self, game_id, starting_time=get_latest_date()):
        response = self.session.get(
            self.LIVESTATS_API + f'/window/{game_id}',
            params={
                'startingTime': starting_time
            }
        )

        return json.loads(response.text)

    def get_details(self, game_id, starting_time=get_latest_date(), participant_ids=None):
        response = self.session.get(
            self.LIVESTATS_API + f'/details/{game_id}',
            params={
                #'startingTime': starting_time,
                'participantIds': participant_ids
            }
        )

        return json.loads(response.text)


def downloadDetails(game_id):
    time_format = r'%Y-%m-%dT%H:%M:%SZ'
    windowApi = f'https://feed.lolesports.com/livestats/v1/window/{game_id}'
    detailApi = f'https://feed.lolesports.com/livestats/v1/details/{game_id}'
    windowData = _requests.get(windowApi).json()
    window_time = _datetime.strptime(windowData['frames'][-1]['rfc460Timestamp'].split('.')[0].split('Z')[0] + 'Z',
                                     time_format)
    # Round to the nearest 10 seconds per API requirements
    window_time = window_time - _timedelta(minutes=0,
                                           seconds=window_time.second % 10 - 10,
                                           microseconds=window_time.microsecond)

    frames = windowData['frames']
    while windowData['frames'][-1]['gameState'] != 'finished':
        params = {'startingTime': window_time.strftime(time_format)}
        windowData = _requests.get(windowApi, params=params).json()
        detailData = _requests.get(detailApi, params=params).json()
        if windowData['frames'][-1]['rfc460Timestamp'] != frames[-1]['rfc460Timestamp']:
            for fIdx in range(len(windowData['frames'])):
                assert windowData['frames'][fIdx]['rfc460Timestamp'] == detailData['frames'][fIdx]['rfc460Timestamp']
                for pIdx in range(0, 5):
                    windowParticipant = windowData['frames'][fIdx]['blueTeam']['participants'][pIdx]
                    detailParticipant = detailData['frames'][fIdx]['participants'][pIdx]
                    assert windowParticipant['participantId'] == detailParticipant['participantId']
                    windowParticipant.update(detailParticipant)

                    windowParticipant = windowData['frames'][fIdx]['redTeam']['participants'][pIdx]
                    detailParticipant = detailData['frames'][fIdx]['participants'][pIdx + 5]
                    assert windowParticipant['participantId'] == detailParticipant['participantId']
                    windowParticipant.update(detailParticipant)
            frames.extend(windowData['frames'])
        window_time = window_time + _timedelta(seconds=10)

    windowData['frames'] = frames
    return windowData