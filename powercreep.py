#!/usr/bin/python
import MySQLdb
import sys
import os
from datetime import datetime, timedelta
from pprint import PrettyPrinter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import data_lib


'''
scatter plot of pokemon by attack vs defense
'''
def attack_defense_scatter(df):
    f1 = df.plot.scatter(x='attack', y='defense', title='Pokemon Attack vs. Defense')
    f1.set(xlabel='Attack',ylabel='Defense')
    plt.show()

'''
scatter plot of pokemon by attack vs defense with sprites
'''
def attack_defense_scatter_sprites(df):
    # plot with sprites
    fig, ax = plt.subplots()

    #for x, y, image_path in zip(df['attack'], df['defense'], df['sprite']):
    for x, y, image_path in zip(df['attack'], df['defense'], df['sprite']):
        data_lib.imscatter(x, y, image_path, zoom=0.5, ax=ax)
        ax.scatter(x, y)

    plt.title('Pokemon Attack vs. Defense', fontsize=20)
    plt.xlabel("Attack", fontsize=20)
    plt.ylabel("Defense", fontsize=20)
    plt.show()

if __name__ == "__main__":

    csv = 'data/pokemon_complete.csv'

    # read csv
    print "[%s] read csv start" % (datetime.now())
    df = pd.read_csv(csv)
    print "[%s] read csv done" % (datetime.now())

    # overview
    print "[%s] overview" % (datetime.now())
    print "head:\n%s" % df.head()
    print "columns:\n%s" % list(df.columns.values)
    print "length: %s" % len(df)

    # plot attack & defense
    print "[%s] plot finish" % (datetime.now())
    attack_defense_scatter(df)
    attack_defense_scatter_sprites(df)
    print "[%s] plot done" % (datetime.now())

    # check legendary
    print "[%s] legendary" % (datetime.now())
    lf = df.loc[df['is_legendary'] == 1]
    print "head\n%s" % lf.head()
    print "length: %s" % len(lf)

    print "[%s] first gen" % (datetime.now())
    lf1 = lf.loc[df['generation'] == 1]

    # gen 1
    print "[%s] gen1" % (datetime.now())
    print "head\n%s" % lf1.head()
    lf1 = lf1[['name','attack','defense']]
    lf1.set_index('name', inplace=True)
    print "length: %s" % len(lf1)

    f2 = lf1.plot.bar(rot=0, stacked=True, title='1st Generation Legendary Pokemon Stats')
    f2.set(xlabel='Legendary Pokemon',ylabel='Stats')
    plt.show()

    # power creep check
    print "[%s] power creep" % (datetime.now())
    df_tot = df.groupby('generation')
    df_mean = df_tot.agg(np.mean)

    print "head\n%s" % df_mean.head

    df = df[['generation', 'attack','defense','sp_attack','sp_defense','hp','speed']]
    f3 = df_mean.plot.bar(y=['attack','defense','sp_attack','sp_defense','hp','speed'],stacked=True,title='Average Pokemon Statistics by Generation')
    f3.set(xlabel='Pokemon Generation',ylabel='Statistics')
    plt.show()










