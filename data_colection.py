import sqlite3
import json
from lolesports_api import *
LOL = Lolesports_API()

def create_table(league):
    connection = sqlite3.connect("matches.db")
    cursor = connection.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {league} (
        id INTEGER PRIMARY KEY,
        date DATE,       -- format YYYY-MM-DD
        year INT,
        playoff BOOLEAN,
        
        time INT,         -- in seconds
        redInhib INT,
        redInhib_5 INT,
        redTowers INT,
        redTowers_5 INT,
        redBarons INT,
        redDragons INT,
        redInfernals INT,
        redClouds INT,
        redOceans INT,
        redMountains INT,
        redChemtechs INT,
        redHextechs INT
        blueInhib INT,
        blueInhib_5 INT,
        blueTowers INT,
        blueTowers_5 INT,
        blueBarons INT,
        blueDragons INT,
        blueInfernals INT,
        blueClouds INT,
        blueOceans INT,
        blueMountains INT,
        blueChemtechs INT,
        blueHextechs INT,
        
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
        redTopmaxHeath INT,
        redTopKP REAL
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
        redTopDamageShare REAL
        
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
        redJunglemaxHeath INT,
        redJungleKP REAL
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
        redJungleDamageShare REAL
        
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
        redMidmaxHeath INT,
        redMidKP REAL
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
        redMidDamageShare REAL
        
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
        redBotmaxHeath INT,
        redBotKP REAL
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
        redBotDamageShare REAL
        
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
        redSuppmaxHeath INT,
        redSuppKP REAL
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
        redSuppDamageShare REAL
        
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
        blueTopmaxHeath INT,
        blueTopKP REAL
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
        blueTopDamageShare REAL
        
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
        blueJunglemaxHeath INT,
        blueJungleKP REAL
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
        blueJungleDamageShare REAL
        
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
        blueMidmaxHeath INT,
        blueMidKP REAL
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
        blueMidDamageShare REAL
        
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
        blueBotmaxHeath INT,
        blueBotKP REAL
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
        blueBotDamageShare REAL
        
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
        blueSuppmaxHeath INT,
        blueSuppKP REAL
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

def get_match_ids(): #!108176841597230181
    leagues = ["worlds", "lec", "lcs", "lck", "lpl", "msi"]
    years = [2022, 2023, 2024]

    for league in leagues:
        print(league)
        l = [i['id'] for i in LOL.get_leagues()['leagues'] if i['slug'] == league][0]
        matches = []
        for year in years:
            #print(year)
            start_year = f"{year}-01-01"
            end_year = f"{year}-12-31"
            tournaments = LOL.get_tournaments_for_league(league_id=l)['leagues'][0]['tournaments']
            tournaments = [t['id'] for t in tournaments if t['startDate']>=start_year and t['endDate']<=end_year]
            for t in tournaments:
                comp = LOL.get_completed_events(tournament_id=t)['schedule']['events']
                input(comp[0])
                comp = [i['games'] for i in comp]
                for event in comp:
                    for match in event:
                        matches.append(match['id'])
        #print("Done")
    return matches

def get_match(id):
    print("Getting data")
    data = downloadDetails(id)
    i = 0
    while int(data['frames']['blueTeam'][totalGold]) == 0:
        i += 1
    data['frames'] = data['frames'][i:]
    print("Saving data")
    with open("gametry.json", "w") as f:
        json.dump(data, f)

get_match(108176841597230181)