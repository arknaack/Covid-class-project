#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system(' pip install plotly')
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import os
os.getcwd()


# In[2]:


#Changing date into correct datatype and reading in the data. Backfilling total cases null value.
df = pd.read_csv('Coviddata.csv')
df=df.astype({"tot_cases": int})
df.Date = df.Date.astype("datetime64")
df.tot_cases.fillna(method="bfill")
df.info()


# In[3]:


#new_case will graph doing it with an individual state, but not the widget

co = df[(df.new_case > 0) & (df.State == "CO")]

plt.plot(co["Date"], co["new_case"])


# In[4]:


#checking to see if there are any null values in "new_case" but there aren't, trying to figure out why graph below won't work

#df2 = df["new_case"]
#mask = df2.isnull().any(axis=1)
#df2[mask]


# In[5]:


from ipywidgets import widgets, interactive, Layout

w_df = widgets.Dropdown(
    description='State',
    options=sorted(list(set(df.State))),
    value='AK',
    style = {"description_width": '50px'},
    layout = Layout(width="70%")
)

def view(state):
    if state == "All":
        df_tmp = df
    else:
        df_tmp = df[df.State == state]
        
    plt.style.use('seaborn-dark')
    fig, ax = plt.subplots(figsize=(15,7))
    ax.plot(df_tmp.Date, df_tmp.tot_cases, color=("purple"))
    ax.set(xlabel="Date", ylabel="Total Cases")
    ax2=ax.twinx()
    ax2.plot(df_tmp.Date, df_tmp["new_case"], color =("red"))
    ax2.plot(df_tmp.Date, df_tmp["tot_death"], color = ("green"))
    ax2.set_ylabel("Total Deaths and New Cases")
    ax2.legend(["New Cases", "Total Death"], loc=1)
    ax.legend(["Total Cases"], loc=0)
    
   
    plt.show()


i = interactive(view, state=w_df)
display(i)

