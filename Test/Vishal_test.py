#!/usr/bin/env python
# coding: utf-8

# #### Insatll libs

# In[ ]:


# pip install fuzzywuzzy
# pip install python-Levenshtein


# #### Import necessary libs

# In[72]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import warnings
warnings.filterwarnings('ignore')


# #### Read csv data

# In[73]:


df = pd.read_csv("exploratory_data_analysis_dataset_1.csv")


# In[74]:


df.head()


# ### 1) number of rows in dataset

# In[75]:


# number of rows in dataset
msg = f'''Bank transaction dataset consists of {len(df)} rows.'''
print(msg)


# ### 2) Find missing value if there

# In[76]:


# Find missing value
df.isnull().sum()


# #### There is no missing value present in data

# ### 3) Here we are calculating outlier to identify fraudulent transection
# #### Assumption: 
# -  If amount is debited more than 75% of the total balance then we can say it as a fraudulent transection

# In[77]:


# We'll find outlier using IQR
df_bedit = df[df['type']=="DEBIT"]

# Find 25% and 75% of data
Q1 = np.percentile(df_bedit['amount'], 25)
Q3 = np.percentile(df_bedit['amount'], 75)

# Calculate IQR
IQR = Q3 - Q1


# In[78]:


# Find upper and lower bound
ul = Q3+1.5*IQR
ll = Q1-1.5*IQR


# In[79]:


# In roder to find outlier we'll take >upper limit
df_debit = df_bedit[(df_bedit['amount']>ul)]
df_debit.head()


# In[80]:


# Here we'll find how many percentage amount is debited from account, if it is more than 75% then we'll consider it as a fraud transection
df_debit['percentage'] = (df_debit["amount"] * 100) // (df_debit["amount"]+df_debit["currentBalance"])
df_fraud = df_debit[df_debit['percentage'].astype('int')>75]
df_fraud


# #### we are getting 4 fraudulent transections

# ### 4) Now we are going to check different payment methods used and how many time they used while transection

# In[93]:


transection_mode = df['mode'].value_counts()
modes = transection_mode.keys()
for mode in modes:
    msg = f''' {mode} has total {transection_mode[mode]} transections '''
    print(msg)


# In[98]:


# Lets see same in graphical manner
y = transection_mode.values
mylabels = transection_mode.keys()
myexplode = [0.2, 0, 0]

plt.pie(y, labels = mylabels, autopct='%1.1f%%', explode = myexplode, shadow = True, textprops={'color':"w"})
plt.legend(title = "Mode of transection")
plt.show() 
plt.show() 


# #### Here as we can see that UPI has max uses while FT has min uses

# ### 5) Now we are grouping the similar transactions id based on similar narration
# #### Assumption
# - Lets assume threshold value 80
# - if similarity_count > 80 then we'll assume that narration as a smiliar otherwise different

# In[234]:


index = list()
narration = list()
similar_narration = list()
amount = list()
txnId = list()
for i in df.index:
    for j in df.index:
        if fuzz.ratio(df['narration'][i],df['narration'][j]) > 80: 
            index.append(i)
            narration.append(df['narration'][i])
            similar_narration.append(df['narration'][j])
            amount.append(df['amount'][j])
            txnId.append(df['txnId'][j])


# In[235]:


new_df = pd.DataFrame({'index':index, 'txnId':txnId, 'narration':narration, 'similar_narration':similar_narration, 'amount':amount})


# In[236]:


new_df


# In[248]:


new_df.groupby('index').agg({'amount':'sum','txnId':', '.join})


# #### Based on fuzz logic we got similar narration and so similar transections id

# ### 6) Highest currentBalance and lowest currentBalance

# In[264]:


msg = f''' Max available amount is {df['currentBalance'].max()} '''
print(msg)


# In[265]:


msg = f''' Max available amount is {df['currentBalance'].min()} '''
print(msg)


# ### 7) Highest and lowest amount debited

# In[266]:


msg = f''' Max amount debited is {df[df['type']=='DEBIT']['amount'].max()} '''
print(msg)


# In[267]:


msg = f''' Min amount debited is {df[df['type']=='DEBIT']['amount'].min()} '''
print(msg)


# ### 8) Highest and lowest amount credited

# In[262]:


msg = f''' Max amount credited is {df[df['type']=='CREDIT']['amount'].max()} '''
print(msg)


# In[263]:


msg = f''' Min amount credited is {df[df['type']=='CREDIT']['amount'].min()} '''
print(msg)


# In[ ]:




