# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 17:33:24 2017

@author: shiwang
"""
# Import libraries
from ggplot import *
import seaborn as sns
import matplotlib.pyplot as plt
import urllib.parse
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import mysql.connector
import re
import pandas as pd
import numpy as np
from scipy import stats

# Settings
base_review_url_us = 'https://myanimelist.net/anime/'
base_search_url_jp = r'https://www.animesachi.com/visitor/search.php?sort=oastyle_up&key='
base_review_url_jp = r'https://www.animesachi.com/visitor/'
score_jp = re.compile(r'中央 ([0-9]+)点/平均')
MAX_REVIEW = 10000

# Function to connect to google cloud sql
def connect_to_cloudsql():
    db = mysql.connector.connect(
        user = 'root',
        passwd = 'hadoop',
        host='127.0.0.1',
        db = 'api_db')
    return db

# Function to get bsObj from given url
def getbsObj(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return(None)
    try:
        bsObj = BeautifulSoup(html.read())
    except AttributeError as e:
        return(None)
    return(bsObj)


# Extract rates from websites
def getReview():
    for index in range(1001,MAX_REVIEW):
        review_url = base_review_url_us + str(index)
        bsObj = getbsObj(review_url)
        
        if bsObj is not None:
            Name_US = bsObj.findAll("span", {"itemprop":"name"})[0].get_text()
            Score_US = float(bsObj.findAll("div", {"class":"fl-l score"})[0].get_text())
            Rating_US = bsObj.find(text= 'Rating:').parent.parent.get_text()[11:-3]
            Producer_US = bsObj.find(text= 'Studios:').parent.parent.get_text()[10:-1]
            sql = "insert into anime (id, name, us_score, us_rating, us_producer) values (%s,%s,%s,%s,%s)"
            c.execute(sql,(index,Name_US, Score_US, Rating_US, Producer_US))
            
            # one to many relationship, thus in another table
            Genres_US = bsObj.find(text= 'Genres:')
            for genre in Genres_US.parent.next_siblings:
                try:
                    genre_ = genre.attrs['title']
                    c.execute("insert into anime_genre (id, genre) values ('%s','%s')" % (index, genre_))
                except:
                    pass
                
            print('Finished US ID ' + str(index) + '---')
            conn.commit()
            
            # Extract japanese name and recode it
            Name_JP = bsObj.find(text= 'Japanese:').parent.parent.get_text()[12:-3]
            Name_JP = urllib.parse.quote(Name_JP)
            
            # Extract from jp webiste
            search_url_jp = base_search_url_jp + Name_JP
            bsObj = getbsObj(search_url_jp)
            try:
                Name_JP_link = bsObj.findAll("td", {"style":"text-align: left; padding-left: 7px;"})[0]
                Link = Name_JP_link.a.attrs['href']
                review_url_jp = base_review_url_jp + Link
                bsObj = getbsObj(review_url_jp)
                Score_JP = bsObj.find(text= score_jp)
                Score_JP = float(score_jp.findall(Score_JP)[0])
                c.execute("UPDATE anime SET jp_score = '%s' where id = '%s'" \
                          % (Score_JP, index))
                print('Finished JP ID ' + str(index) + '---')
                conn.commit()
            except:
                pass
        else:
            print('Skipped US/JP ID ' + str(index) + '---')

# Plot 1: Rating count plot
def CountPlot(dataset, column, label, s, a):
    orders = dataset[column].value_counts().keys()
    sns.set_style("darkgrid")
    sns_plot = sns.factorplot(y=column,data=dataset,kind='count',order = orders, 
                              palette="muted",size = s, aspect = a)
    plt.xlabel(label)
    plt.ylabel('Frequency')
    plt.tight_layout()
    sns_plot.savefig('./fig/'+ label + '_Count_Plot.png',dpi=100)

def TwoHist(dataset):
    sns.set_style("darkgrid")
    sns.distplot(dataset['us_score'], kde=True, rug=False, label = 'US Score')
    sns.distplot(dataset['jp_score'], kde=True, rug=False, label = 'JP Score')
    plt.legend()
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('./fig/Two_His_Plot.png',dpi=100)    

def TwoCorr(dataset):
    sns.set_style("darkgrid")
    sns.jointplot(x='us_score', y='jp_score', data=dataset).set_axis_labels('US Score','JP Score')
    plt.savefig('./fig/Two_Corr_Plot.png',dpi=100)
    
def ByColumnComparison(dataset,column):
    orders = dataset[column].value_counts().keys()
    df = dataset[['us_score', 'jp_score',column]]\
        .set_index(column)\
        .stack()\
        .reset_index()\
        .rename(columns={'level_1': 'Country', 0: 'Score'})
        
    df['Country'].replace(['us_score'], 'United States', inplace=True)
    df['Country'].replace(['jp_score'], 'Japan', inplace=True)
    
    sns.factorplot(y=column, x='Score', hue='Country', data=df, kind="bar", 
                   size = 4, aspect = 2, order=orders,ci =None)
    plt.savefig('./fig/By_'+ column +'_Comparison_Plot.png',dpi=100)
        

# Analyze the dataset
def Analyze():
    # Retrieve dataset
    c.execute('select * from anime')
    entries = c.fetchall()
    anime_reviews = pd.DataFrame(entries)

    c.execute('select * from anime_genre')
    entries = c.fetchall()
    anime_genres = pd.DataFrame(entries)
    
    # Manipulation
    anime_reviews.columns = ['id','name','us_score','jp_score','rating','producer']
    anime_reviews = anime_reviews.dropna(axis=0, how='any')
    anime_reviews.us_score = anime_reviews.us_score * 10
    anime_reviews['diff_score'] = anime_reviews.us_score - anime_reviews.jp_score 
    top_25_producers = anime_reviews.producer.value_counts().keys()[:25]
    
    anime_genres.columns = ['id','genre']
    anime_genres = pd.merge(anime_genres, anime_reviews, left_on=['id'], right_on = ['id'],\
                      how='left').dropna(axis=0, how='any')
    top_15_genres = anime_genres.genre.value_counts().keys()[:15]
    anime_genres = anime_genres[anime_genres.genre.isin(top_15_genres)]
    
    # Plots
    CountPlot(anime_reviews, 'rating', 'Rating',4,2)
    CountPlot(anime_reviews[anime_reviews.producer.isin(top_25_producers)], 'producer', 'Producer',4,2)
    TwoHist(anime_reviews)
    TwoCorr(anime_reviews)
    ByColumnComparison(anime_reviews,'rating')
    ByColumnComparison(anime_genres,'genre')

    # Summary Table
    # 1.paired t test
    stats.ttest_rel(anime_reviews.us_score,anime_reviews.jp_score)
    
    # 2.Group by rating & genre
    summary_rating = anime_reviews.groupby('rating').agg({'diff_score': [np.mean, np.std]})
    summary_genre = anime_genres.groupby('genre').agg({'diff_score': [np.mean, np.std]})
    summary_producer = anime_reviews[anime_reviews.producer.isin(top_25_producers)].groupby('producer').agg({'diff_score': [np.mean, np.std]})
        
    #g = sns.FacetGrid(anime_genres[anime_genres.genre.isin(top_15_genres)], row='genre',
    #                  size=1.7, aspect=4,)
    #g.map(sns.distplot, 'diff_score', hist=True, rug=False,kde=False);


if __name__ == '__main__':
    conn = connect_to_cloudsql()
    c = conn.cursor()
    #c.execute("TRUNCATE TABLE anime") 
    #c.execute("TRUNCATE TABLE anime_genre") 
    getReview()
    conn.commit()


