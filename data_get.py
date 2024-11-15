import sqlite3 as sql
import numpy as np
from copy import deepcopy

def get_league_season(league, year, seq = False):

    sql_regular = f"SELECT * from {league} WHERE year={year} AND playoff=0"
    sql_po = f"SELECT * from {league} WHERE year={year} AND playoff=1"

    con = sql.connect("matches.db")
    cur = con.cursor()
    cur.execute(sql_regular)
    regular = np.array(cur.fetchall())
    if not seq:
        regular = regular[:,5:]

    cur.execute(sql_po)
    po = np.array(cur.fetchall())
    if not seq:
        po = po[:,5:]

    con.close()

    if seq:
        return sequence(regular, po)

    def smart_convert(x):
        # First convert to float
        num = float(x)
        # If it has no decimal part, convert to int
        if num.is_integer():
            return int(num)
        else:
            return num  # remains as float

    regular = np.vectorize(smart_convert)(regular)
    po = np.vectorize(smart_convert)(po)

    np.random.shuffle(regular)
    np.random.shuffle(po)

    return regular, po

def sequence(*args):
    ret_list = []
    for list in args:
        games = {}
        ret_list.append([])
        for frame in list:
            if frame[1] in games.keys():
                games[frame[1]].append(frame)
            else:
                games[frame[1]] = [frame]
        for g in games:
            games[g].sort(key = lambda x: x[6])

            temp = []
            for i in range(len(games[g])-5):
                temp.append( [games[g][j] for j in range(i,i+5)] )
            temp = np.array(temp)
            temp = temp[:,:,5:]
            games[g] = deepcopy(temp)
            for seq in games[g]:
                ret_list[-1].append(seq)
    ret_list = np.array(ret_list)
    return ret_list

