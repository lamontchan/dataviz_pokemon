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
    fig = df.plot.scatter(x='attack', y='defense', title='Pokemon Attack vs. Defense')
    fig.set(xlabel='Attack',ylabel='Defense')
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

def avg_stats_by_generation(df):
    df_tot = df.groupby('generation')
    df_mean = df_tot.agg(np.mean)

    df = df[['generation', 'attack','defense','sp_attack','sp_defense','hp','speed']]
    fig = df_mean.plot.bar(y=['attack','defense','sp_attack','sp_defense','hp','speed'],stacked=True,title='Average Pokemon Statistics by Generation')
    fig.set(xlabel='Pokemon Generation',ylabel='Statistics')
    plt.show()


def show_gen1_legendary_stats(df):

    # get first gen legendaries
    df = df.loc[df['is_legendary'] == 1]
    df = df.loc[df['generation'] == 1]

    # gen 1
    df = df[['name','attack','defense']]
    df.set_index('name', inplace=True)

    fig = df.plot.bar(rot=0, stacked=True, title='1st Generation Legendary Pokemon Stats')
    fig.set(xlabel='Legendary Pokemon',ylabel='Stats')
    plt.show()

def plot_stat_distribution(df):
    df['total_stats'] = df['attack'] + df['defense'] + df['sp_attack'] + df['sp_defense'] + df['hp'] + df['speed']
    fig = df['total_stats'].plot.hist(title='Statistic Distribution of Pokemon', bins=10)
    fig.set(xlabel='Total Statistics',ylabel='Number of Pokemon')
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
    print "[%s] attack/defense scatter start" % (datetime.now())
    attack_defense_scatter(df)
    attack_defense_scatter_sprites(df)
    print "[%s] attack/defense scatter done" % (datetime.now())

    # check legendary
    print "[%s] gen1 legendary start" % (datetime.now())
    show_gen1_legendary_stats(df)
    print "[%s] gen1 legendary done" % (datetime.now())

    # power creep check
    print "[%s] average pokemon statistics by generation start" % (datetime.now())
    avg_stats_by_generation(df)
    print "[%s] average pokemon statistics by generation end" % (datetime.now())

    # distribution
    print "[%s] plot statistics distribution start" % (datetime.now())
    plot_stat_distribution(df)
    print "[%s] plot statistics distribution end" % (datetime.now())








