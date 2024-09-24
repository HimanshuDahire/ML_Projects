# -*- coding: utf-8 -*-
"""
> Name: Himanshu Dahire

> Batch_ID: Data_Science_05092024_10AM(PDS_23072024)
### 1. Business Problem

- Business Problem:

		The growth of the company was incremental year by year, but due to the online selling of books and widespread Internet access, its annual growth started to collapse.
		
- Business Objective:

		To help bookstore gain it's popularity by increasing the footfall of customers

- Business Constraints:

    	Minimize the marketing cost.
    
- Success Criteria: 

		Business Success Criteria: Improve business about 25% of the current growth and also increase the cross-selling of books.

		ML Success Criteria: Get acceptable `lift ratio`.

		Economic Success Criteria:  Increase the foot fall of customers and increase the sale of books.
"""
# import data

import pandas as pd
df = pd.read_csv('book.csv')
df.head()
from sqlalchemy import create_engine
from urllib.parse import quote

# data-base credentials
user = 'root'
pw = quote('xxxxxx')
db = 'datascience'

engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/{db}")

# exporting data to SQL
df.to_sql('books_tbl', con = engine, if_exists='replace', chunksize=1000, index=False)

# loading data from SQL
query = 'select * from books_tbl;'
df = pd.read_sql_query(query, con=engine)

"""
### 2. Data Dictionary

| Name of feature | Details                         | Type            | Relevance |
| --------------- | ------------------------------- | --------------- | --------- |
| ChildBks        | Book for Childerns              | Binary, Categorical | Na        |
| YouthBks        | Book for Youth                  | Binary, Categorical | Na        |
| CookBks         | Book for Cooking                | Binary, Categorical | Na        |
| DoItYBks        | Book for self help              | Binary, Categorical | Na        |
| RefBks          | Book for Reference to a subject | Binary, Categorical | Na        |
| ArtBks          | Book for Arts                   | Binary, Categorical | Na        |
| GeogBks         | Book on Geography               | Binary, Categorical | Na        |
| ItalCook        | Italian Cook book               | Binary, Categorical | Na        |
| ItalAtlas       | Atlas in Italina language       | Binary, Categorical | Na        |
| ItalArt         | Arts books in Italian language  | Binary, Categorical | Na        |
| Florence        | Book for Childerns              | Binary, Categorical | Na        |

"""

### 3. Data Pre-Processing
#### 3.1 Data Cleaning
# check for null values
df.isna().sum()

"""
- No null values are present.
- Not checked for duplicates because, all rows contain binary data, there is high chance that large number of rows can be similar.
"""

#### 3.2 EDA (Exploratory Data Analysis)
# count of books purchased of each category
count = df.loc[:,:].sum()
count

# taking top 6 most popular books category
popular_book_cat = count.sort_values(ascending=False).head(6)
popular_book_cat

# creating data-frame of the popular books
popular_book_cat_df = pd.DataFrame(popular_book_cat)

# resetting the index of data-frame
popular_book_cat_df.reset_index(inplace=True)

# renaming the columns of data-frame
popular_book_cat_df.rename(columns={'index':'books_cat', 0:'count'}, inplace=True)


# Visualization of the popular books category

import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize = (5,3)) # defining the size of plot

# creating scatter plot with seaborn
sns.barplot(orient='h', data=popular_book_cat_df,
            y = 'books_cat',
            x = 'count',
            hue='books_cat', 
            ax = ax
            ) 

plt.show()  


### 4. Model Building
# converting binary data of data-frame to boolean values. zeros: False, 1: True.
    # given dataset doesn't require data to be one-hot encoded, as it already has vales in form of 0s and 1s
bool_df = df.astype(bool)


# importing libraries for Association rules.


from mlxtend.frequent_patterns import apriori, association_rules  # Importing specific functions from mlxtend library.

# using Apriori Algorithm to calculate the support for each transactions
frequent_items = apriori(bool_df,
                         min_support=0.05, #at-least 5% probability of occurrence
                         max_len = 3,
                        use_colnames=True)

# sorting the frequent_items data-frame in descending order of support
frequent_items.sort_values(by='support', ascending=False, inplace=True)

# top 10 transactions with maximum support
frequent_items.head(10)

# calculating association rules metrics to get transaction with better lift ratio.
rules = association_rules(frequent_items, metric='lift', min_threshold=1)

# sorting rules in descending order of lift
rules.sort_values(by = 'lift', ascending=False, inplace=True)

# removing alternate rows of rules as they are repetitive
rules = rules.iloc[::2]

# top10 rules with highest lift value
top10_rules = rules.head(10)


# Visualization of rules by it's support, confidence and lift
top10_rules.plot(x="support", y="confidence", c=top10_rules.lift, 
             kind="scatter", s=50, cmap=plt.cm.coolwarm)

plt.show()
# defining a function to convert elements of frozenset to string
def to_string (element: frozenset)->str:
    """
    function to convert elements of frozenset to string

    Parameters:
    element (frozenset): input frozenset

    Return:
    element_str (str): elements of frozen set as string
    """
    element_str = ', '.join(f"'{i}'" for i in element)
    return element_str

top10_rules.loc[:,'antecedents'] = top10_rules.antecedents.apply(to_string)
top10_rules.loc[:,'consequents'] = top10_rules.consequents.apply(to_string)


# exporting this top10 to SQL
top10_rules.to_sql('top10_books_tbl', con=engine, if_exists='replace', chunksize=1000, index=False)
top10_rules