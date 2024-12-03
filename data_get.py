import sqlite3 as sql
from random import random

import numpy as np
from copy import deepcopy


def smart_convert(x):
    # First convert to float
    num = float(x)
    # If it has no decimal part, convert to int
    if num.is_integer():
        return int(num)
    else:
        return num  # remains as float

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
    for i in range(len(ret_list)):
        ret_list[i] = np.array(ret_list[i])
        def smart_convert(x):
            # First convert to float
            num = float(x)
            # If it has no decimal part, convert to int
            if num.is_integer():
                return int(num)
            else:
                return num  # remains as float
        ret_list[i] = np.vectorize(smart_convert)(ret_list[i])
    return ret_list

def get_year(year, seq = False):
    leagues = ['lec', 'lcs', 'lck'] # , 'lpl'

    rw, pw = get_league_season("worlds", year, seq)
    #!rm, pm = get_league_season("msi", year, seq)
    p = np.vstack((rw, pw)) #!, rm, pm

    r = np.empty((0, 274))
    for l in leagues:
        rl, pl = get_league_season(l, year, seq)
        r = np.vstack((r, rl, pl))

    return r, p


def get_random_matches(n=1):
    con = sql.connect("matches.db")
    cur = con.cursor()
    sql_query = """SELECT name FROM sqlite_master  WHERE type='table';"""
    cur.execute(sql_query)
    tables = [t[0] for t in cur.fetchall() if t[0] != "game_ids"]

    matches = []
    for _ in range(n):
        table = np.random.choice(tables)
        cur.execute(f"SELECT gameId from {table}")
        games_ids = [id[0] for id in cur.fetchall()]
        id = np.random.choice(games_ids)
        cur.execute(f"SELECT * from {table} WHERE gameId={id} ORDER BY time")
        game = cur.fetchall()
        matches.append(game)
    matches = np.array(matches)[:,:,5:]
    matches = np.vectorize(smart_convert)(matches)
    return matches

def get_samples(size=2e4):
    con = sql.connect("matches.db")
    cur = con.cursor()
    n = size//3

    leagues = ["lec", "lcs", "lck"] #? LPL ?

    samples = []
    for l in leagues:
        cur.execute(f"SELECT * from {l} ORDER BY RANDOM() LIMIT {n}")
        s = cur.fetchall()
        samples += s
    samples = np.array(samples)[:,5:]
    samples = np.vectorize(smart_convert)(samples)
    return samples