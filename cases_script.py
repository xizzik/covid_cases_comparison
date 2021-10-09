# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 22:00:14 2021

@author: xizik
"""
import pandas as pd
import numpy as np
from TwitterAPI import TwitterAPI
import os
os.chdir('C:\\Users\\xizik\\Desktop\\data science\\cases\\covid_cases_comparison')
from credentials import Credentials

def output_preparer(is_bot : bool):
    data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv', header = 0, 
                       usecols = ['date', 'location','new_cases','new_deaths']) #TO DO in december add vaccinations 28-12-2021
    mask = data['location'] == 'Poland'
    data = data.loc[mask,:].drop('location', axis = 1).copy()
    data.loc[:,'date'] = pd.to_datetime(data.loc[:,'date'])
    year_td = pd.Timedelta(days = 365 if pd.Timestamp.today().year % 4 != 0 else 366)
    today = pd.Timestamp.today().normalize() - pd.Timedelta(days = 1)
    today_yearago = (today - year_td).normalize()
    mask = (data['date'].isin({today,today_yearago}))
    if is_bot: 
        features = ['new_cases','new_deaths'] 
        data_arr = np.array(data.loc[mask, features], dtype = int)
        return np.diff(data_arr, axis = 0).flatten()
    else:
        pass
def main():
    cds = Credentials()
    api = TwitterAPI(consumer_key = cds.ck, 
                     consumer_secret = cds.cs, 
                     access_token_key = cds.atk, 
                     access_token_secret = cds.ats)
    try:
        values_to_post = output_preparer(is_bot = True)
        if np.isnan(values_to_post).sum() > 0:
            raise ValueError()
    except ValueError:
        values_to_post = [False, False]
    
    if values_to_post.all():
        tweet = f"""Dzisiaj odnotowano {values_to_post[0]} nowych przypadków w stosunku do rok temu
         oraz {values_to_post[1]} zgonów w stosunku do rok temu."""
    else:
        tweet = 'Niestety nie posiadamy danych na dzis.'
        
    api.request('statuses/update', {'status':tweet})
    
if __name__ == "__main__":
    main()
    

