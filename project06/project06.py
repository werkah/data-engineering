#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd


# In[2]:


con = sqlite3.connect("proj6_readings.sqlite")
cur = con.cursor()


# In[3]:


result = cur.execute("SELECT COUNT(*) FROM readings;").fetchall()


# In[4]:


df = pd.DataFrame(result)


# In[5]:


df


# In[6]:


df = pd.read_sql("SELECT count(*) from readings;", con)
df


# In[7]:


query = "SELECT COUNT(DISTINCT detector_id) AS detector_count FROM readings;"
df = pd.read_sql(query, con)
df.to_pickle("proj6_ex01_detector_no.pkl")


# In[8]:


df


# In[9]:


query = """
SELECT
    detector_id,
    COUNT(*) AS meas_count,
    MIN(starttime) AS min_starttime,
    MAX(starttime) AS max_starttime
FROM
    readings
WHERE
    count IS NOT NULL
GROUP BY
    detector_id;
"""


# In[10]:


df = pd.read_sql(query, con)


# In[11]:


df.head(3)


# In[12]:


df.to_pickle("proj6_ex02_detector_stat.pkl")


# In[13]:


query = """
SELECT
    detector_id,
    count,
    LAG(count) OVER (PARTITION BY detector_id ORDER BY starttime) AS prev_count
FROM
    readings
WHERE
    detector_id = 146
LIMIT 500;
"""


# In[14]:


df = pd.read_sql(query, con)


# In[15]:


df.head(3)


# In[16]:


df.to_pickle("proj6_ex03_detector_146_lag.pkl")


# In[17]:


query = '''
SELECT
    detector_id,
    count,
    SUM(count) OVER (
        PARTITION BY detector_id
        ORDER BY starttime
        ROWS BETWEEN CURRENT ROW AND 10 FOLLOWING
    ) AS window_sum
FROM
    readings
WHERE
    detector_id = 146
LIMIT 500;
'''


# In[18]:


df = pd.read_sql(query, con)


# In[19]:


df.head(3)


# In[20]:


df.to_pickle("proj6_ex04_detector_146_sum.pkl")

