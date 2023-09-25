#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json


# In[2]:


with open('proj5_params.json') as file:
    params = json.load(file)


# In[3]:


import pandas as pd
df = pd.read_csv('proj5_timeseries.csv')


# In[4]:


df


# In[5]:


dict.fromkeys(df.columns)


# In[6]:


df.columns = df.columns.str.lower()


# In[7]:


df.columns = df.columns.str.replace("[^a-z]", "_", regex=True)


# In[8]:


df


# In[9]:


dict.fromkeys(df.columns)


# In[10]:


df.dtypes


# In[11]:


name_column = df.columns[0]


# In[12]:


name_column


# In[13]:


pd.to_datetime(df[name_column])


# In[14]:


df[name_column] = pd.to_datetime(df[name_column])


# In[15]:


df


# In[16]:


df.dtypes


# In[17]:


df.set_index(name_column, inplace=True)


# In[18]:


df


# In[19]:


df.index


# In[20]:


len(df)


# In[21]:


df = df.asfreq(params['original_frequency'])


# In[22]:


df.index


# In[23]:


df


# In[24]:


df.to_pickle('proj5_ex01.pkl')


# In[25]:


dfw = df.copy()


# In[26]:


dfw = dfw.asfreq(params['target_frequency'])


# In[27]:


params['target_frequency']


# In[28]:


dfw


# In[29]:


dfw.dtypes


# In[30]:


dfw.index


# In[31]:


dfw.to_pickle('proj5_ex02.pkl')


# In[32]:


downsample_freq = str(params['downsample_periods']) + params['downsample_units']
downsample_freq
down = df.copy()


# In[33]:


down = down.resample(downsample_freq).sum(min_count=params['downsample_periods'])


# In[34]:


down


# In[35]:


down.to_pickle('proj5_ex03.pkl')


# In[36]:


df


# In[37]:


up = df.copy()
upsample_freq = str(params['upsample_periods']) + params['upsample_units']
up = up.resample(upsample_freq).interpolate(method=params['interpolation'], order=params['interpolation_order'])


# In[38]:


upsample_freq


# In[39]:


up


# In[40]:


original_freq = pd.Timedelta(1, unit=params['original_frequency'])
upsampled_freq = pd.Timedelta(upsample_freq)
scaling_factor = upsampled_freq / original_freq
up = up * scaling_factor


# In[41]:


upsampled_freq


# In[42]:


original_freq


# In[43]:


scaling_factor


# In[44]:


up


# In[45]:


up.to_pickle('proj5_ex04.pkl')


# In[46]:


df_sensors = pd.read_pickle('proj5_sensors.pkl')


# In[47]:


df_sensors


# In[48]:


df_sensors = df_sensors.pivot(columns='device_id', values='value')
df_sensors


# In[49]:


sensors_periods = params['sensors_periods']
sensors_units = params['sensors_units']
sensors_freq = str(params['sensors_periods']) + params['sensors_units']


# In[50]:


sensors_freq


# In[51]:


new_index = pd.date_range(start=df_sensors.index.min(), end=df_sensors.index.max(), freq=sensors_freq)


# In[52]:


new_index


# In[53]:


df_sensors.reindex(new_index)


# In[54]:


df_s = df_sensors.reindex(new_index.union(df_sensors.index)).interpolate()
df_s


# In[55]:


df_ss = df_s.reindex(new_index)
df_ss


# In[56]:


df_ss = df_ss.dropna()


# In[57]:


df_ss


# In[58]:


df_ss.to_pickle('proj5_ex05.pkl')

