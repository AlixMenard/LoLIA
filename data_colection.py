import sqlite3
import json
import datetime
from copy import deepcopy
from importlib.metadata import metadata

from matplotlib.pyplot import connect

from lolesports_api import *
LOL = Lolesports_API()

def rfc4602datetime(rfc460):
    time_format = r'%Y-%m-%dT%H:%M:%SZ'
    time = datetime.datetime.strptime(rfc460.split('.')[0].split('Z')[0] + 'Z', time_format)
    return time

def datetime2rfc4602(date):
    time_format = r'%Y-%m-%dT%H:%M:%SZ'
    time = datetime.datetime.strftime(date, time_format)
    return time

def datetime2iso(date):
    time_format = r'%Y-%m-%d'
    time = datetime.datetime.strftime(date, time_format)
    return time


def create_table(league):
    connection = sqlite3.connect("matches.db")
    cursor = connection.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {league} (
        id INTEGER PRIMARY KEY,
        gameId INTEGER,
        date DATE,       -- format YYYY-MM-DD
        year INT,
        playoff BOOLEAN,
        
        time INT,         -- in seconds
        redInhib INT,
        redInhib_5 INT,
        redTowers INT,
        redTowers_5 INT,
        redBarons INT,
        redBarons_5 INT,
        redDragons INT,
        redDragons_5 INT,
        redInfernals INT,
        redClouds INT,
        redOceans INT,
        redMountains INT,
        redChemtechs INT,
        redHextechs INT,
        redElders INT,
        redElders_5 INT,
        blueInhib INT,
        blueInhib_5 INT,
        blueTowers INT,
        blueTowers_5 INT,
        blueBarons INT,
        blueBarons_5 INT,
        blueDragons INT,
        blueDragons_5 INT,
        blueInfernals INT,
        blueClouds INT,
        blueOceans INT,
        blueMountains INT,
        blueChemtechs INT,
        blueHextechs INT,
        blueElders INT,
        blueElders_5 INT,
        
        redTopKills INT,
        redTopKills_5 INT,
        redTopDeaths INT,
        redTopDeaths_5 INT,
        redTopAssists INT,
        redTopAssists_5 INT,
        redTopGolds INT,
        redTopGolds_5 INT,
        redTopLevel INT,
        redTopCS INT,
        redTopHealth INT,
        redTopMaxHealth INT,
        redTopKP REAL,
        redTopWardsPlaced INT,
        redTopWardsDestroyed INT,
        redTopAD INT,
        redTopAP INT,
        redTopCrit REAL,
        redTopAS INT,
        redTopLifeSteal INT,
        redTopMR INT,
        redTopArmor INT,
        redTopTenacity INT,
        redTopDamageShare REAL,
        
        redJungleKills INT,
        redJungleKills_5 INT,
        redJungleDeaths INT,
        redJungleDeaths_5 INT,
        redJungleAssists INT,
        redJungleAssists_5 INT,
        redJungleGolds INT,
        redJungleGolds_5 INT,
        redJungleLevel INT,
        redJungleCS INT,
        redJungleHealth INT,
        redJungleMaxHealth INT,
        redJungleKP REAL,
        redJungleWardsPlaced INT,
        redJungleWardsDestroyed INT,
        redJungleAD INT,
        redJungleAP INT,
        redJungleCrit REAL,
        redJungleAS INT,
        redJungleLifeSteal INT,
        redJungleMR INT,
        redJungleArmor INT,
        redJungleTenacity INT,
        redJungleDamageShare REAL,
        
        redMidKills INT,
        redMidKills_5 INT,
        redMidDeaths INT,
        redMidDeaths_5 INT,
        redMidAssists INT,
        redMidAssists_5 INT,
        redMidGolds INT,
        redMidGolds_5 INT,
        redMidLevel INT,
        redMidCS INT,
        redMidHealth INT,
        redMidMaxHealth INT,
        redMidKP REAL,
        redMidWardsPlaced INT,
        redMidWardsDestroyed INT,
        redMidAD INT,
        redMidAP INT,
        redMidCrit REAL,
        redMidAS INT,
        redMidLifeSteal INT,
        redMidMR INT,
        redMidArmor INT,
        redMidTenacity INT,
        redMidDamageShare REAL,
        
        redBotKills INT,
        redBotKills_5 INT,
        redBotDeaths INT,
        redBotDeaths_5 INT,
        redBotAssists INT,
        redBotAssists_5 INT,
        redBotGolds INT,
        redBotGolds_5 INT,
        redBotLevel INT,
        redBotCS INT,
        redBotHealth INT,
        redBotMaxHealth INT,
        redBotKP REAL,
        redBotWardsPlaced INT,
        redBotWardsDestroyed INT,
        redBotAD INT,
        redBotAP INT,
        redBotCrit REAL,
        redBotAS INT,
        redBotLifeSteal INT,
        redBotMR INT,
        redBotArmor INT,
        redBotTenacity INT,
        redBotDamageShare REAL,
        
        redSuppKills INT,
        redSuppKills_5 INT,
        redSuppDeaths INT,
        redSuppDeaths_5 INT,
        redSuppAssists INT,
        redSuppAssists_5 INT,
        redSuppGolds INT,
        redSuppGolds_5 INT,
        redSuppLevel INT,
        redSuppCS INT,
        redSuppHealth INT,
        redSuppMaxHealth INT,
        redSuppKP REAL,
        redSuppWardsPlaced INT,
        redSuppWardsDestroyed INT,
        redSuppAD INT,
        redSuppAP INT,
        redSuppCrit REAL,
        redSuppAS INT,
        redSuppLifeSteal INT,
        redSuppMR INT,
        redSuppArmor INT,
        redSuppTenacity INT,
        redSuppDamageShare REAL,
        
        blueTopKills INT,
        blueTopKills_5 INT,
        blueTopDeaths INT,
        blueTopDeaths_5 INT,
        blueTopAssists INT,
        blueTopAssists_5 INT,
        blueTopGolds INT,
        blueTopGolds_5 INT,
        blueTopLevel INT,
        blueTopCS INT,
        blueTopHealth INT,
        blueTopMaxHealth INT,
        blueTopKP REAL,
        blueTopWardsPlaced INT,
        blueTopWardsDestroyed INT,
        blueTopAD INT,
        blueTopAP INT,
        blueTopCrit REAL,
        blueTopAS INT,
        blueTopLifeSteal INT,
        blueTopMR INT,
        blueTopArmor INT,
        blueTopTenacity INT,
        blueTopDamageShare REAL,
        
        blueJungleKills INT,
        blueJungleKills_5 INT,
        blueJungleDeaths INT,
        blueJungleDeaths_5 INT,
        blueJungleAssists INT,
        blueJungleAssists_5 INT,
        blueJungleGolds INT,
        blueJungleGolds_5 INT,
        blueJungleLevel INT,
        blueJungleCS INT,
        blueJungleHealth INT,
        blueJungleMaxHealth INT,
        blueJungleKP REAL,
        blueJungleWardsPlaced INT,
        blueJungleWardsDestroyed INT,
        blueJungleAD INT,
        blueJungleAP INT,
        blueJungleCrit REAL,
        blueJungleAS INT,
        blueJungleLifeSteal INT,
        blueJungleMR INT,
        blueJungleArmor INT,
        blueJungleTenacity INT,
        blueJungleDamageShare REAL,
        
        blueMidKills INT,
        blueMidKills_5 INT,
        blueMidDeaths INT,
        blueMidDeaths_5 INT,
        blueMidAssists INT,
        blueMidAssists_5 INT,
        blueMidGolds INT,
        blueMidGolds_5 INT,
        blueMidLevel INT,
        blueMidCS INT,
        blueMidHealth INT,
        blueMidMaxHealth INT,
        blueMidKP REAL,
        blueMidWardsPlaced INT,
        blueMidWardsDestroyed INT,
        blueMidAD INT,
        blueMidAP INT,
        blueMidCrit REAL,
        blueMidAS INT,
        blueMidLifeSteal INT,
        blueMidMR INT,
        blueMidArmor INT,
        blueMidTenacity INT,
        blueMidDamageShare REAL,
        
        blueBotKills INT,
        blueBotKills_5 INT,
        blueBotDeaths INT,
        blueBotDeaths_5 INT,
        blueBotAssists INT,
        blueBotAssists_5 INT,
        blueBotGolds INT,
        blueBotGolds_5 INT,
        blueBotLevel INT,
        blueBotCS INT,
        blueBotHealth INT,
        blueBotMaxHealth INT,
        blueBotKP REAL,
        blueBotWardsPlaced INT,
        blueBotWardsDestroyed INT,
        blueBotAD INT,
        blueBotAP INT,
        blueBotCrit REAL,
        blueBotAS INT,
        blueBotLifeSteal INT,
        blueBotMR INT,
        blueBotArmor INT,
        blueBotTenacity INT,
        blueBotDamageShare REAL,
        
        blueSuppKills INT,
        blueSuppKills_5 INT,
        blueSuppDeaths INT,
        blueSuppDeaths_5 INT,
        blueSuppAssists INT,
        blueSuppAssists_5 INT,
        blueSuppGolds INT,
        blueSuppGolds_5 INT,
        blueSuppLevel INT,
        blueSuppCS INT,
        blueSuppHealth INT,
        blueSuppMaxHealth INT,
        blueSuppKP REAL,
        blueSuppWardsPlaced INT,
        blueSuppWardsDestroyed INT,
        blueSuppAD INT,
        blueSuppAP INT,
        blueSuppCrit REAL,
        blueSuppAS INT,
        blueSuppLifeSteal INT,
        blueSuppMR INT,
        blueSuppArmor INT,
        blueSuppTenacity INT,
        blueSuppDamageShare REAL
        
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()

def delete_table(league):
    connection = sqlite3.connect("matches.db")
    cursor = connection.cursor()

    delete_table_query = f"DROP TABLE IF EXISTS {league};"
    cursor.execute(delete_table_query)
    connection.commit()
    connection.close()

def get_match_ids(league, year): #!108176841597230181
    #print(league)
    l = [i['id'] for i in LOL.get_leagues()['leagues'] if i['slug'] == league][0]
    matches = []

    #print(year)
    start_year = f"{year}-01-01"
    end_year = f"{year}-12-31"
    tournaments = LOL.get_tournaments_for_league(league_id=l)['leagues'][0]['tournaments']
    tournaments = [t['id'] for t in tournaments if t['startDate']>=start_year and t['endDate']<=end_year]
    for t in tournaments:
        comp = LOL.get_completed_events(tournament_id=t)['schedule']['events']
        #input(comp[0])
        block = [i['blockName'] for i in comp]
        comp = [i['games'] for i in comp]
        for i,event in enumerate(comp):
            for match in event:
                matches.append((match['id'], block[i] in ['Playoffs', 'Finals', 'Knockouts', 'Quarterfinals', 'Semifinals']))
    #print("Done")
    return matches

def load_match(id):
    #print("Getting data")
    try:
        data = downloadDetails(id)
    except:
        #print(e)
        return
    #print("Parsing data")
    i = 0
    while int(data['frames'][i]['blueTeam']['totalGold']) == 0:
        i += 1
    data['frames'] = data['frames'][i:]

    start = data['frames'][0]["rfc460Timestamp"]
    start = rfc4602datetime(start)
    last_filter = deepcopy(start)
    filtered_frames = []
    for i in range(len(data['frames'])):
        frame_time = data['frames'][i]["rfc460Timestamp"]
        frame_time = rfc4602datetime(frame_time)
        delta = frame_time - start
        in_game_time = delta.total_seconds()
        data['frames'][i]["inGameTime"] = int(in_game_time)

        diff = int((frame_time - last_filter).total_seconds())
        if diff and diff % 10 == 0:
            filtered_frames.append(data['frames'][i])
            last_filter = frame_time
    data['frames'] = filtered_frames

    #print(data['frames'][-1]['blueTeam']['dragons'])
    #print(data['frames'][-1]['redTeam']['dragons'])

    """print("Saving data")
    with open("gametry.json", "w") as f:
        json.dump(data, f, indent = 3)"""

    return data


def save_match(id, is_PO, league):
    data = load_match(id)
    if data is None:
        connection = sqlite3.connect("matches.db")
        cursor = connection.cursor()
        sql = f"INSERT INTO game_ids (id) VALUES ({id})"
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return

    try:
        frames = data['frames']
    except:
        print(data)
    f0 = frames[0]

    metadata = {}
    metadata['date'] = datetime2iso(rfc4602datetime(f0['rfc460Timestamp']))
    metadata['year'] = int(metadata['date'][:4])
    metadata['playoff'] = is_PO
    #print(metadata['date'])

    new_frames = []
    start_index = 0
    while frames[start_index]['inGameTime'] < 10*60:
        start_index += 1

    for i, frame in enumerate(frames):
        if i<start_index:
            continue
        nf = {'gameId': id, 'date' : metadata['date'], 'year' : metadata['year'], 'playoff' : metadata['playoff'], 'time' : frame['inGameTime']}
        for c in ["red", "blue"]:
            nf[f'{c}Inhib'] = frame[f'{c}Team']['inhibitors']
            nf[f'{c}Inhib_5'] = frame[f'{c}Team']['inhibitors'] - frames[i-5*6][f'{c}Team']['inhibitors']
            nf[f'{c}Towers'] = frame[f'{c}Team']['towers']
            nf[f'{c}Towers_5'] = frame[f'{c}Team']['towers'] - frames[i-5*6][f'{c}Team']['towers']
            nf[f'{c}Barons'] = frame[f'{c}Team']['barons']
            nf[f'{c}Barons_5'] = frame[f'{c}Team']['barons'] - frames[i-5*6][f'{c}Team']['barons']
            nf[f'{c}Dragons'] = len(frame[f'{c}Team']['dragons'])
            nf[f'{c}Dragons_5'] = len(frame[f'{c}Team']['dragons']) - len(frames[i-5*6][f'{c}Team']['dragons'])
            nf[f'{c}Infernals'] = frame[f'{c}Team']['dragons'].count("infernal")
            nf[f'{c}Clouds'] = frame[f'{c}Team']['dragons'].count("cloud")
            nf[f'{c}Oceans'] = frame[f'{c}Team']['dragons'].count("ocean")
            nf[f'{c}Mountains'] = frame[f'{c}Team']['dragons'].count("mountain")
            nf[f'{c}Chemtechs'] = frame[f'{c}Team']['dragons'].count("chemtech")
            nf[f'{c}Hextechs'] = frame[f'{c}Team']['dragons'].count("hextech")
            nf[f'{c}Elders'] = frame[f'{c}Team']['dragons'].count("elder")
            nf[f'{c}Elders_5'] = frame[f'{c}Team']['dragons'].count("elder") - frames[i-5*6][f'{c}Team']['dragons'].count("elder")

            for pid, role in enumerate(["Top", "Jungle", "Mid", "Bot", "Supp"]):
                nf[f'{c}{role}Kills'] = frame[f'{c}Team']['participants'][pid]['kills']
                nf[f'{c}{role}Kills_5'] = frame[f'{c}Team']['participants'][pid]['kills'] - frames[i-5*6][f'{c}Team']['participants'][pid]['kills']
                nf[f'{c}{role}Deaths'] = frame[f'{c}Team']['participants'][pid]['deaths']
                nf[f'{c}{role}Deaths_5'] = frame[f'{c}Team']['participants'][pid]['deaths'] - frames[i-5*6][f'{c}Team']['participants'][pid]['deaths']
                nf[f'{c}{role}Assists'] = frame[f'{c}Team']['participants'][pid]['assists']
                nf[f'{c}{role}Assists_5'] = frame[f'{c}Team']['participants'][pid]['assists']- frames[i-5*6][f'{c}Team']['participants'][pid]['assists']
                nf[f'{c}{role}Golds'] = frame[f'{c}Team']['participants'][pid]['totalGold']
                nf[f'{c}{role}Golds_5'] = frame[f'{c}Team']['participants'][pid]['totalGold']- frames[i-5*6][f'{c}Team']['participants'][pid]['totalGold']
                nf[f'{c}{role}Level'] = frame[f'{c}Team']['participants'][pid]['level']
                nf[f'{c}{role}CS'] = frame[f'{c}Team']['participants'][pid]['creepScore']
                nf[f'{c}{role}Health'] = frame[f'{c}Team']['participants'][pid]['currentHealth']
                nf[f'{c}{role}MaxHealth'] = frame[f'{c}Team']['participants'][pid]['maxHealth']
                nf[f'{c}{role}KP'] = frame[f'{c}Team']['participants'][pid]['killParticipation']
                nf[f'{c}{role}WardsPlaced'] = frame[f'{c}Team']['participants'][pid]['wardsPlaced']
                nf[f'{c}{role}WardsDestroyed'] = frame[f'{c}Team']['participants'][pid]['wardsDestroyed']
                nf[f'{c}{role}AD'] = frame[f'{c}Team']['participants'][pid]['attackDamage']
                nf[f'{c}{role}AP'] = frame[f'{c}Team']['participants'][pid]['abilityPower']
                nf[f'{c}{role}Crit'] = frame[f'{c}Team']['participants'][pid]['criticalChance']
                nf[f'{c}{role}AS'] = frame[f'{c}Team']['participants'][pid]['attackSpeed']
                nf[f'{c}{role}LifeSteal'] = frame[f'{c}Team']['participants'][pid]['lifeSteal']
                nf[f'{c}{role}MR'] = frame[f'{c}Team']['participants'][pid]['magicResistance']
                nf[f'{c}{role}Armor'] = frame[f'{c}Team']['participants'][pid]['armor']
                nf[f'{c}{role}Tenacity'] = frame[f'{c}Team']['participants'][pid]['tenacity']
                nf[f'{c}{role}DamageShare'] = frame[f'{c}Team']['participants'][pid]['championDamageShare']

        new_frames.append(nf)

    connection = sqlite3.connect("matches.db")
    cursor = connection.cursor()

    columns = ", ".join(new_frames[0].keys())
    placeholders = ", ".join("?" * len(new_frames[0]))
    insert_sql = f"INSERT INTO {league} ({columns}) VALUES ({placeholders})"

    for frame in new_frames:
        for key in frame.keys():
            if type(frame[key]) == list:
                print(key, frame[key])
        values = tuple(frame.values())
        cursor.execute(insert_sql, values)

    connection.commit()
    connection.close()

    connection = sqlite3.connect("matches.db")
    cursor = connection.cursor()
    sql = f"INSERT INTO game_ids (id) VALUES ({id})"
    cursor.execute(sql)
    connection.commit()
    connection.close()

def found():
    connection = sqlite3.connect("matches.db")
    cursor = connection.cursor()
    sql = f"SELECT id FROM game_ids"
    cursor.execute(sql)
    results = cursor.fetchall()
    connection.close()
    return results

if __name__ == "__main__":
    leagues = ["worlds", "lec", "lcs", "lck", "lpl", "msi"]
    years = [2022, 2023, 2024]
    done_ids = found()
    done_ids = [i[0] for i in done_ids]
    print("Got saved.")

    for l in leagues:
        print(l, flush=True)
        create_table(l)
        for y in years:
            print(f"\t{y}... ", end = "", flush=True)
            m = get_match_ids(l, y)
            print("IDs retrieved... ", end = "", flush=True)
            skipped = done = 0
            nb_ids = len(m)
            for i in m:
                if not int(i[0]) in done_ids:
                    save_match(i[0], i[1], l)
                    done += 1
                else:
                    done += 1
                    skipped += 1
                    print(end="\r")
                    print(f"\t{y}... IDs retrieved... {done}/{nb_ids}, skipped {skipped}/{done}.", end = "", flush=True)
            print("Done", flush=True)

# 31/10 started LEC 2024