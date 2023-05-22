#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


file_path="proj2_data.csv"


# In[3]:


df = pd.read_csv(file_path, sep='[|;]', decimal=',', thousands=None,header=0, engine="python", skip_blank_lines=True)


# In[4]:


print(df)


# In[5]:


df.to_pickle("proj2_ex01.pkl")


# In[6]:


df_cp=df.copy()


# In[7]:


with open('proj2_scale.txt', 'r') as f:
    scale = [s.rstrip('\n') for s in f.readlines()]


# In[8]:


print(scale)


# In[9]:


for col in df_cp.columns:
    if set(df_cp[col]).issubset(set(scale)):
        df_cp[col] = df_cp[col].map(lambda x: scale.index(str(x)) + 1)


# In[10]:


print(df_cp)


# In[11]:


df_cp.to_pickle("proj2_ex02.pkl")


# In[12]:


df_cp1=df.copy()


# In[13]:


for col in df_cp1.columns:
    if set(df_cp1[col]).issubset(set(scale)):
        df_cp1[col] = pd.Categorical(df_cp1[col], categories=scale)


# In[14]:


df_cp1.dtypes


# In[15]:


df_cp1.to_pickle("proj2_ex03.pkl")


# In[16]:


df.dtypes


# In[17]:


import re
df_cp2=df.copy()


# In[18]:


for col in df_cp2.select_dtypes(include=['object']):
    df_cp2[col] = df_cp2[col].str.replace(',', '.')


# In[19]:


print(df_cp2)


# In[20]:


num_df = pd.DataFrame()
num_pat = r'(-?\d+(?:[.,]\d+)?)'
for col in df_cp2.select_dtypes(include="object"):
    nums = df_cp2[col].str.extract(num_pat)
    if not nums.isna().all().item():
        num_df[col] = nums.astype(float)
df_num = pd.DataFrame(num_df)


# In[21]:


print(df_num)


# In[22]:


df_num.dtypes


# In[23]:


df_num.to_pickle("proj2_ex04.pkl")


# In[24]:


cols = []
for col in df.columns:
    if df[col].dtype == "object" and df[col].nunique() <= 10:
        if df[col].str.match(r"^[a-z]+$").all() and not df[col].isin(scale).any():
            cols.append(col)
print(cols)


# In[25]:


for i, col in enumerate(cols):
    oh = pd.get_dummies(df[col])
    print(oh)
    oh.to_pickle(f"proj2_ex05_{i+1}.pkl")

