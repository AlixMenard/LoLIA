
from time import sleep
from lolesports_api import *

w = League('worlds')
w24 = w.getTournamentBySlug('worlds_2024')
w24.events = [e for e in w24.events if e['startTime']<'2024-09-28T18:00:00Z']
NA = w24.getEvent('112966697102367375')
NA1 = NA.getGame('112966697102367376')


while 1:
    data = NA1.get_window()
    print("\n"*50)
    meta = data["gameMetadata"]
    frame = data["frames"][-1]
    for i in range(5):
        print(meta['blueTeamMetadata']['participantMetadata'][i]['championId'], frame["blueTeam"]["participants"][i]['totalGold'], "golds  - ", meta['redTeamMetadata']['participantMetadata'][i]['championId'], frame["redTeam"]["participants"][i]['totalGold'], "golds")