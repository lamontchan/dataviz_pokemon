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
scatter plot with given x,y data
'''
def scatter_plot(df, x_data, y_data, x_label, y_label, title):
    fig = df.plot.scatter(x=x_data, y=y_data, title=title)
    fig.set(xlabel=x_label,ylabel=y_label)
    plt.show()

'''
scatter plot of given x,y data with pokemon sprites
'''
def scatter_plot_sprites(df, x_data, y_data, x_label, y_label, title):
    # plot with sprites
    fig, ax = plt.subplots()

    for x, y, image_path in zip(df[x_data], df[y_data], df['sprite']):
        data_lib.imscatter(x, y, image_path, zoom=0.5, ax=ax)
        ax.scatter(x, y)

    plt.title(title, fontsize=20)
    plt.xlabel(x_label, fontsize=20)
    plt.ylabel(y_label, fontsize=20)
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

def plot_stat_distribution(df, title):
    fig = df['total_stats'].plot.hist(title=title, bins=10)
    fig.set(xlabel='Total Statistics',ylabel='Number of Pokemon')
    plt.show()

def normalize_stats(df):
    df = normalize_column(df, 'attack')
    df = normalize_column(df, 'sp_attack')
    df = normalize_column(df, 'max_attack')
    df = normalize_column(df, 'defense')
    df = normalize_column(df, 'sp_defense')
    df = normalize_column(df, 'hp')
    df = normalize_column(df, 'speed')
    df = normalize_column(df, 'total_stats')
    return df

def normalize_column(df,column):
    df[column]=((df[column]-df[column].min())/(df[column].max()-df[column].min()))
    #print df.head()
    return df

'''
add max_attack as attack/sp_attack value; whichever is higher
    - pokemon most likely uses higher stat for attacking for more effectiveness
'''
def add_data(df):
    df['max_attack'] = df[['attack','sp_attack']].max(axis=1)
    df['total_stats'] = df['attack'] + df['defense'] + df['sp_attack'] + df['sp_defense'] + df['hp'] + df['speed']
    print df[['name','attack','sp_attack','max_attack','total_stats']].head()
    return df

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

    # check max attack/sp.attack
    print "[%s] add data to df start" % (datetime.now())
    df = add_data(df)
    print "[%s] add data to df end" % (datetime.now())

    # normalize data
    df = normalize_stats(df)

    # plot attack & defense
    print "[%s] attack/defense scatter start" % (datetime.now())
    scatter_plot(df, 'attack', 'defense', 'Attack', 'Defense', 'Pokemon Attack vs. Defense')
    scatter_plot_sprites(df, 'attack', 'defense', 'Attack', 'Defense', 'Pokemon Attack vs. Defense')
    print "[%s] attack/defense scatter done" % (datetime.now())

    # plot sp attack & sp defense
    print "[%s] sp.attack/sp.defense scatter start" % (datetime.now())
    scatter_plot_sprites(df.loc[df['is_fully_evolved'] == 1], 'sp_attack', 'sp_defense', 'Special Attack', 'Special Defense', 'Pokemon Sp. Attack vs. Sp. Defense')
    print "[%s] sp.attack/sp.defense scatter done" % (datetime.now())

    # check legendary
    print "[%s] gen1 legendary start" % (datetime.now())
    show_gen1_legendary_stats(df)
    print "[%s] gen1 legendary done" % (datetime.now())

    # power creep check
    print "[%s] average pokemon statistics by generation start" % (datetime.now())
    avg_stats_by_generation(df)
    avg_stats_by_generation(df.loc[df['is_fully_evolved'] == 1])
    print "[%s] average pokemon statistics by generation end" % (datetime.now())

    # distribution
    print "[%s] plot statistics distribution start" % (datetime.now())
    for i in range(1,7):
        plot_stat_distribution(df.loc[(df['is_fully_evolved'] == 1) & (df['generation'] == i)], 'Statistic Distribution of Pokemon - Generation %s' % (i))
        print df[['name','total_stats']].loc[(df['is_fully_evolved'] == 1) & (df['generation'] == i)].sort_values(by='total_stats',ascending=False).head()
    print "[%s] plot statistics distribution end" % (datetime.now())







