#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Wine Quality Investigation
# 
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# > This is a wine dataset containing 1599 rows and 12 columns displaying the wine's fixed acidity, residual sugar, citric acid and free sulphur dioxide which would be used to determine the quality of wine.
# ### Question(s) for Analysis
# <li>What chemical attribute are relevant in predicting the quality of wine.</li>
# <li>Do wines with higher alcoholic content receive better ratings?.</li>
# <li>What amount or level of acidity is associated with the highest quality.</li>
# <li>Do sweeter wines receive better ratings</li>
# <li>Is a certain type of wine associated with higher quality?</li>

# <a id='wrangling'></a>
# ## Data Wrangling

# ### Gathering Data

# In[117]:


#import statements
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
sns.set_style('darkgrid')
# load red and white wine datasets
red_df = pd.read_csv('winequality-red.csv', sep = ';') 
white_df =pd.read_csv('winequality-white.csv', sep = ';') 


# In[118]:


red_df


# In[119]:


white_df


# In[120]:


red_df.info()


# In[121]:


white_df.info()


# In[122]:


sum(white_df.duplicated())


# In[123]:


white_df.duplicated()


# In[124]:


white_df.nunique()


# In[125]:


red_df['density'].mean()


# In[126]:


# create color array for red dataframe
color_red = np.repeat('red', red_df.shape[0])

# create color array for white dataframe
color_white = np.repeat('white', white_df.shape[0])


# In[127]:


red_df['color'] = color_red
red_df.head()


# In[128]:


white_df['color']= color_white

white_df.head()


# In[129]:


# append dataframes
wine_df = red_df.append(white_df, sort = False)

# view dataframe to check for success

wine_df.head()


# In[130]:


wine_df.to_csv('winequality_edited.csv', index=False)


# In[131]:


wine_df.info()


# 
# ##### Data Cleaning

# In[132]:


red_df.rename(columns={'total_sulfur-dioxide':'total_sulfur_dioxide'}, inplace=True)


# <a id='eda'></a>
# ## Exploratory Data Analysis

# In[133]:


df_wine = pd.read_csv('winequality_edited.csv')
df_wine


# ## Scatterplot

# In[134]:


df_wine.plot(x ='quality', y = 'pH', kind = 'scatter' );


# In[135]:


df_wine.plot(x ='quality', y = 'residual_sugar', kind = 'scatter' );


# In[136]:


df_wine.plot(x ='quality', y = 'alcohol', kind = 'scatter' );


# In[137]:


df_wine.plot(x ='quality', y = 'volatile_acidity', kind = 'scatter' );


# ## Histogram

# In[138]:


df_wine.hist(figsize = (15, 15))


# In[139]:


df_wine['alcohol'].plot(kind = 'hist', figsize = (8, 8))


# In[140]:


df_wine['fixed_acidity'].plot(kind = 'hist', figsize = (8, 8), color = 'purple')


# In[141]:


df_wine['pH'].plot(kind = 'hist', figsize = (8, 8))


# In[142]:


df_wine['total_sulfur_dioxide'].plot(kind = 'hist', figsize = (8, 8))


# ### Drawing Conclusions Using Groupby

# ##### Is a certain type of wine associated with higher quality?

# In[143]:


# Find the mean quality of each wine type (red and white) with groupby
df_wine.groupby('color').mean().quality


# ##### What amount or level of acidity is associated with the highest quality?

# In[144]:


# View the min, 25%, 50%, 75%, max pH values with Pandas describe
df_wine['pH'].describe()


# In[145]:


# Bin edges that will be used to "cut" the data into groups
bin_edges = [2.72, 3.11, 3.21, 3.32, 4.01] # Fill in this list with five values you just found


# In[146]:


# Labels for the four acidity level groups
bin_names = bin_names = ['high', 'mod_high', 'medium', 'low'] # Name each acidity level category


# In[147]:


# Creates acidity_levels column
df_wine['acidity_levels'] = pd.cut(df_wine['pH'], bin_edges, labels=bin_names)

# Checks for successful creation of this column
df_wine.head()


# In[148]:


# Find the mean quality of each acidity level with groupby
acidity_level_quality_means = df_wine.groupby('acidity_levels').mean().quality


# In[149]:


locations = [2, 3, 4, 1]  # reorder values above to go from low to high
heights = acidity_level_quality_means

labels = ['Low', 'Medium', 'Moderately High', 'High']
#labels = acidity_level_quality_means.index.str.replace('_', ' ').str.title() # alternative to commented out line above

plt.bar(locations, heights, tick_label=labels)
plt.title('Average Quality Ratings by Acidity Level')
plt.xlabel('Acidity Level')
plt.ylabel('Average Quality Rating');


# In[150]:


# Save changes for the next section
df_wine.to_csv('winequality_edited.csv', index=False)


# ### Drawing Conclusions Using Groupby

# #### Que 3: Do wines with a higher alcoholic content receive better ratings?

# In[151]:


# get the median amount of alcohol content
df_wine['alcohol'].median()


# In[152]:


# select samples with alcohol content less than the median
low_alcohol = df_wine.query('alcohol < 10.300000000000001')

# select samples with alcohol content greater than or equal to the median
high_alcohol = df_wine.query('alcohol >= 10.300000000000001')

# ensure these queries included each sample exactly once
num_samples = df_wine.shape[0]
num_samples == low_alcohol['quality'].count() + high_alcohol['quality'].count() # should be True


# In[153]:


# get mean quality rating for the low alcohol and high alcohol groups
mean_quality_low = low_alcohol['quality'].mean()
mean_quality_low


# In[154]:


mean_quality_high = high_alcohol['quality'].mean()
mean_quality_high


# In[155]:


# Create a bar chart with proper labels
locations = [1, 2]
heights = [mean_quality_low, mean_quality_high]
labels = ['Low', 'High']
plt.bar(locations, heights, tick_label=labels)
plt.title('Average Quality Ratings by Alcohol Content')
plt.xlabel('Alcohol Content')
plt.ylabel('Average Quality Rating');


# #### Que 4: Do sweeter wines receive better ratings?

# In[156]:


# get the median amount of residual sugar
df_wine['residual_sugar'].median()


# In[157]:


# select samples with residual sugar less than the median
low_sugar = df_wine.query('residual_sugar < 3.0')

# select samples with residual sugar greater than or equal to the median
high_sugar =df_wine.query('residual_sugar >= 3.0')

# ensure these queries included each sample exactly once
num_samples == low_sugar['quality'].count() + high_sugar['quality'].count() # should be True


# In[158]:


# get mean quality rating for the low sugar and high sugar groups
low_sugar['residual_sugar'].mean()


# In[159]:


high_sugar['residual_sugar'].mean()


# In[160]:


mean= df_wine['residual_sugar'].mean()
low_sugar = df_wine.query('residual_sugar < {}'.format(mean))
high_sugar = df_wine.query('residual_sugar > {}'.format(mean))

mean_quality_low = low_sugar['quality'].mean()
mean_quality_low


# In[161]:


mean_quality_high = high_sugar['quality'].mean()
mean_quality_high


# In[162]:


# Create a bar chart 
location = [1, 2]
height = [mean_quality_low, mean_quality_high]
label = ['low', 'high']
plt.bar(location, height, tick_label = label);
plt.title('Average Quality Ratings by Residual Sugar')
plt.xlabel('Residual quality')
plt.ylabel('Average Quality Rating')


# ### Plotting Wine Type and Quality with Matplotlib

# #### Arrays for red bar heights white bar heights
# 1. Red bar proportions = counts for each quality rating / total # of red samples
# 2. White bar proportions = counts for each quality rating / total # of white samples

# In[163]:


# get counts for each rating and color
color_counts = wine_df.groupby(['color', 'quality']).count()['pH']
color_counts


# In[164]:


# get total counts for each color
color_totals = wine_df.groupby('color').count()['pH']
color_totals


# In[165]:


# get proportions by dividing red rating counts by total # of red samples
red_proportions = color_counts['red'] / color_totals['red']
red_proportions


# In[166]:


# get proportions by dividing white rating counts by total # of white samples
white_proportions = color_counts['white'] / color_totals['white']
white_proportions


# In[167]:


red_proportions['9'] = 0
red_proportions


# ### Plot proportions on a bar chart
# x axis = ratings
# y axis = width of each bar

# In[168]:


ind = np.arange(len(red_proportions)) #for x
width = 0.35                          #for y


# In[169]:


# plot bars
red_bars = plt.bar(ind, red_proportions, width, color='r', alpha=.7, label='Red Wine')
white_bars = plt.bar(ind + width, white_proportions, width, color='w', alpha=.7, label='White Wine')

# title and labels
plt.ylabel('Proportion')
plt.xlabel('Quality')
plt.title('Proportion by Wine Color and Quality')
locations = ind + width / 2  # xtick locations
labels = ['3', '4', '5', '6', '7', '8', '9']  # xtick labels
plt.xticks(locations, labels)

# legend
plt.legend()


# 

# <a id='conclusions'></a>
# ## Conclusions
# 
# In this analysis, i discovered the following:
# <li>A low level of acidity receives the highest mean quality rating.</li>
# <li>Wines with higher alcohol content receives better ratings</li>
# <li>The mean quality of red wine is less than that of white wine.</li>
# <li>Sweeter wines receive better ratings.</li>
# <li>The chemical attribute relevant in predicting a wines quality are mainly residual sugar, color, alcohol .</li>
# 
# 
# 

# In[171]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_Wine_Dataset.ipynb'])


# In[ ]:




