# -*- coding: utf-8 -*-

# Import necessary modules from Flask
from flask import Flask, render_template, request

# Import pandas and numpy for data manipulation
import pandas as pd

# Import functions from mlxtend library for frequent itemsets and association rules
from mlxtend.frequent_patterns import apriori, association_rules

# Import create_engine function from SQLAlchemy for database connection
from sqlalchemy import create_engine
from urllib.parse import quote

# Create a Flask application instance
app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    # Render the index.html template
    return render_template('index.html')

# Define the route for the form submission
@app.route('/success', methods=['POST'])
def success():
    # Check if the request method is POST
    if request.method == 'POST':
        
        # Get the uploaded file from the request
        f = request.files['file']
        user = request.form['user']
        pw = quote(request.form['pw'])
        db = request.form['db']
        
        engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/{db}")
        
        df = pd.read_csv(f)
        
        ### 4. Model Building
        # converting binary data of data-frame to boolean values. zeros: False, 1: True.
            # given dataset doesn't require data to be one-hot encoded, as it already has vales in form of 0s and 1s
        bool_df = df.astype(bool)

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
        
        # Convert the DataFrame to an HTML table with Bootstrap styling
        html_table = top10_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_html(classes='table table-striped')
        
        # Render the new.html template with the HTML table
        return render_template("data.html", Y=f"<style>\
                    .table {{\
                        width: 50%;\
                        margin: 0 auto;\
                        border-collapse: collapse;\
                    }}\
                    .table thead {{\
                        background-color: #39648f;\
                    }}\
                    .table th, .table td {{\
                        border: 1px solid #ddd;\
                        padding: 8px;\
                        text-align: center;\
                    }}\
                    .table td {{\
                        background-color: #5e617d;\
                    }}\
                    .table tbody th {{\
                        background-color: #ab2c3f;\
                    }}\
                </style>\
                {html_table}") 

# Run the Flask application if this script is executed
if __name__ == '__main__':
    app.run(debug=True)

