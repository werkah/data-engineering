#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import json
import numpy as np


# In[2]:


df1 = pd.read_json("proj3_data1.json")
df2 = pd.read_json("proj3_data2.json")
df3 = pd.read_json("proj3_data3.json")


# In[3]:


df = df1.append(df2, ignore_index=True)
df = df.append(df3, ignore_index=True)
df.to_json("ex01_all_data.json", orient = "records")


# In[4]:


csv = []
df_cp = df.copy()
for col in df_cp.columns:
    temp=[]
    missing_count = df_cp[col].isnull().sum()
    if missing_count > 0:
        temp.append(col)
        temp.append(missing_count)
        print(temp)
        csv.append(temp)
        print(csv)
        
with open("ex02_no_nulls.csv", "w") as f:
    for row in csv:
        f.write(",".join(map(str, row)) + "\n")


# In[5]:


with open("proj3_params.json") as f:
    params = json.load(f)
df_cp1 = df.copy()
concat_columns = params["concat_columns"]
df_cp1["description"] = df_cp1[concat_columns[0]]
for col in concat_columns[1:]:
    df_cp1["description"] += " " + df_cp1[col]
df_cp1.to_json("ex03_descriptions.json", orient = "records")


# In[6]:


with open("proj3_more_data.json") as f:
    data = json.load(f)
df_more = pd.DataFrame(data)
join_col = params["join_column"]
df_join = pd.merge(df_cp1, df_more, on=join_col, how="left")
df_join.to_json("ex04_joined.json", orient = "records")


# In[7]:


int_cols = params["int_columns"]

for _, row in df_join.iterrows():
    desc = row["description"].lower().replace(" ", "_")
    row[df_join.columns != "description"].to_json(f"ex05_{desc}.json")
    row.replace(np.nan, None, inplace=True)#wyrzucenie nan
    row[int_cols]=row[int_cols].astype('Int64')
    row[df_join.columns != "description"].to_json(f"ex05_int_{desc}.json")#poza desc

