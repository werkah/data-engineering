#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import json
import pickle
import openpyxl
import re


# In[2]:


df = pd.read_csv('./lab1_ex01.csv')


# In[3]:


per_miss = df.isna().sum() / len(df)


# In[4]:


cols = []


# In[5]:


for c in df.columns:
    col = {'name': c, 'missing': per_miss[c],'type': 'other'}
    if df[c].dtype == 'int64':
        col['type'] = 'int'
    elif df[c].dtype == 'float64':
        col['type'] = 'float'
    cols.append(col)


# In[6]:


with open('ex01_fields.json', 'w') as f:
    json.dump(cols, f, indent=4)


# In[7]:


dict = {}
for col in df.columns:
    temp = df[col]
    if temp.dtype != 'object':
        nested = {
            'count':str(len(df[col])-df[col].isna().sum()),
            'mean':str(df[col].sum() / len(df[col])),
            'std':str(np.std(df[col], ddof=1)),
            'min':str(df[col].min()),
            '25%':str(df[col].quantile([0.25])),
            '50%':str(df[col].quantile([0.50])),
            '75%':str(df[col].quantile([0.75])),
            'max':str(df[col].max())
        }
        dict.update({col:temp.describe().to_dict()})
    else:
        nested = {
            'count': str(len(df[col])-df[col].isna().sum()),
            'unique':str(len(df[col].unique())),
            'top':str(df[col].value_counts().idxmax()),
            'freq':str(df[col].value_counts().max()),
        }
        dict.update({col:nested})


# In[8]:


with open('ex02_stats.json', 'w') as f:
    json.dump(dict, f)


# In[9]:


df = df.rename(columns=lambda x: re.sub(r'[^A-Za-z0-9_ ]', '', x))

df.columns = df.columns.str.replace(" ", "_")

df.columns = df.columns.str.lower()


# In[10]:


df.to_csv('ex03_columns.csv', index=False)


# In[11]:


df.to_excel("ex04_excel.xlsx", index = False)


# In[12]:


df.to_json("ex04_json.json", orient="records")


# In[13]:


rows = df.to_dict(orient = 'records')
with open('ex04_json.json', 'w') as f:
    json.dump(rows, f)


# In[14]:


with open('ex04_pickle.pkl', 'wb') as f:
    pickle.dump(df, f)


# In[15]:


df_2 = pd.read_pickle('lab1_ex05.pkl')
df_2 = df_2.fillna('')
res = df_2.iloc[df_2.index.str.startswith('v'), 1:3]
res.to_markdown('ex05_table.md')


# In[16]:


with open('lab1_ex06.json', 'r') as f:
    data = json.load(f)

df_3 = pd.json_normalize(data, sep='.')

df_3.to_pickle('ex06_pickle.pkl')

