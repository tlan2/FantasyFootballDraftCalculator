# Tom Lancaster (c) 2019
#
#Fantasy Football Auction Draft Calculator - Flask App
#


#======================================================================
#           Imported Packages
#======================================================================
from flask import Flask, render_template, request, flash #Flask web serving package with tools
from forms import CustomForm #Form created for custom setting
import pandas as pd #Library package that stores transformed data to be displayed
from tools import * #Imports all personally created functions

#======================================================================
#           Load Data
#======================================================================
excel_file = 'player_stats.xlsx' #Assigns a variable to the file being read in
qb_data = pd.read_excel(excel_file, sheet_name=0) #Assigns meaningful names to each spreadsheet
rb_data = pd.read_excel(excel_file, sheet_name=1)
wr_data = pd.read_excel(excel_file, sheet_name=2)
te_data = pd.read_excel(excel_file, sheet_name=3)
k_data = pd.read_excel(excel_file, sheet_name=4)
def_data = pd.read_excel(excel_file, sheet_name=5)

#======================================================================
#           League Settings Dictionaries
#======================================================================

#Each dictionary has the important elements to creating the created dataframes

yahoo_settings = {
    "auction_budget" : 200,
    "teams" : 10,
    "qb": 1,
    "rb": 2.5,
    "wr": 2.5,
    "te": 1,
    "flex": 1,
    "k": 1,
    "defense": 1,
    "bench": 6,
    "total_roster": 15,
    "pass_yds" : 0.04,
    "pass_tds" : 4.0,
    "interceptions" : -2.0,
    "rush_yds" : 0.1,
    "rush_tds" : 6,
    "recs" : 0.5,
    "rec_yds": 0.1,
    "rec_tds": 6.0,
    "two_point": 2.0,
    "fl" : -2.0,
    "u20" : 3.0,
    "u30" : 3.0,
    "u40" : 3.0,
    "u50" : 4.0,
    "u70" : 5.0,
    "pat" : 1.0,
    "sack": 1.0,
    "int" : 2.0,
    "fr" : 2.0,
    "def_td" : 6.0,
    "sfty": 2.0,
}

espn_settings = {
    "auction_budget" : 200,
    "teams" : 10,
    "qb": 1.0,
    "rb": 2.5,
    "wr": 2.5,
    "te": 1,
    "flex": 1,
    "k": 1,
    "defense": 1,
    "bench": 7,
    "total_roster": 16,
    "pass_yds" : 0.04,
    "pass_tds" : 4.0,
    "interceptions" : -2.0,
    "rush_yds" : 0.1,
    "rush_tds" : 6,
    "recs" : 1.0,
    "rec_yds": 0.1,
    "rec_tds": 6.0,
    "two_point": 2.0,
    "fl" : -2.0,
    "u20" : 3.0,
    "u30" : 3.0,
    "u40" : 3.0,
    "u50" : 4.0,
    "u70" : 5.0,
    "pat" : 1.0,
    "sack": 1.0,
    "int" : 2.0,
    "fr" : 2.0,
    "def_td" : 6.0,
    "sfty": 1.0,
}

ycup_settings = {
    "auction_budget" : 235,
    "teams" : 10,
    "qb": 2,
    "rb": 2.5,
    "wr": 2.5,
    "te": 1,
    "flex": 1,
    "k": 1,
    "defense": 1,
    "bench": 7,
    "total_roster": 18,
    "pass_yds" : 0.04,
    "pass_tds" : 4.0,
    "interceptions" : -2.0,
    "rush_yds" : 0.1,
    "rush_tds" : 6,
    "recs" : 0.25,
    "rec_yds": 0.1,
    "rec_tds": 6.0,
    "two_point": 2.0,
    "fl" : -2.0,
    "u20" : 1.0,
    "u30" : 1.0,
    "u40" : 1.0,
    "u50" : 3.0,
    "u70" : 4.0,
    "pat" : 0.5,
    "sack": 1.0,
    "int" : 2.0,
    "fr" : 2.0,
    "def_td" : 6.0,
    "sfty": 2.0,
}

#All custom settings initialized to zero which requires complete and accurate user input
custom_settings = {
    "auction_budget" : 0,
    "teams" : 0,
    "qb": 0,
    "rb": 0,
    "wr": 0,
    "te": 0,
    "flex": 0,
    "k": 0,
    "defense": 0,
    "bench": 0,
    "total_roster": 0,
    "pass_yds" : 0,
    "pass_tds" : 0,
    "interceptions" : 0,
    "rush_yds" : 0,
    "rush_tds" : 0,
    "recs" : 0,
    "rec_yds": 0,
    "rec_tds": 0,
    "two_point": 0,
    "fl" : 0,
    "u20" : 0,
    "u30" : 0,
    "u40" : 0,
    "u50" : 0,
    "u70" : 0,
    "pat" : 0,
    "sack": 0,
    "int" : 0,
    "fr" : 0,
    "def_td" : 0,
    "spc_td": 0,
    "sfty": 0
}

#This dictionary is used to establish various baselines which assist calculations
perc_dict = { "qb": {"elite_starter" : 0, "starter" : 0,"top_reserve" : 0, "roster" : 0},
                "rb": {"elite_starter" : 0, "starter" : 0,"top_reserve" : 0, "roster" : 0},
                "wr": {"elite_starter" : 0, "starter" : 0,"top_reserve" : 0, "roster" : 0},
                "te": {"elite_starter" : 0, "starter" : 0,"top_reserve" : 0, "roster" : 0},
                "k" : {"elite_starter" : 0, "starter" : 0,"top_reserve" : 0, "roster" : 0},
                "defense": {"elite_starter" : 0, "starter" : 0,"top_reserve" : 0, "roster" : 0}
}

#For the custom function
custom_percentiles = { "qb": {"elite_starter" : 0, "starter" : 0,"top_reserve" : 0, "roster" : 0},
                "rb": {"elite_starter" : 0, "starter" : 0,"top_reserve" : 0, "roster" : 0},
                "wr": {"elite_starter" : 0, "starter" : 0,"top_reserve" : 0, "roster" : 0},
                "te": {"elite_starter" : 0, "starter" : 0,"top_reserve" : 0, "roster" : 0},
                "k" : {"elite_starter" : 0, "starter" : 0,"top_reserve" : 0, "roster" : 0},
                "defense": {"elite_starter" : 0, "starter" : 0,"top_reserve" : 0, "roster" : 0}
}
#======================================================================
#           Transform Data
#======================================================================

#Provides the established percentiles based Yahoo! and ESPN settings
yahoo_percentiles = percentiles(perc_dict,yahoo_settings)
espn_percentiles = percentiles(perc_dict, espn_settings)
ycup_percentiles = percentiles(perc_dict, ycup_settings)

#ESPN Final Results called by function
qb_efinal, rb_efinal, wr_efinal, te_efinal, k_efinal, defense_efinal = espn(qb_data, rb_data, wr_data, te_data, k_data, def_data, espn_percentiles, espn_settings)

#Yahoo! Results
qb_yfinal, rb_yfinal, wr_yfinal, te_yfinal, k_yfinal, defense_yfinal = yahoo(qb_data, rb_data, wr_data, te_data, k_data, def_data, yahoo_percentiles, yahoo_settings)

#Hometown League Results
qb_ycup, rb_ycup, wr_ycup, te_ycup, k_ycup, defense_ycup = ycup(qb_data, rb_data, wr_data, te_data, k_data, def_data, ycup_percentiles, ycup_settings)

#======================================================================
#           Routers
#======================================================================
app = Flask(__name__) #Instantiates a Flask app
app.config.from_object(__name__) #Loads configuration from this file
app.config['SECRET_KEY'] = 'capstone_project' #Prevents a malicious attack from another request

@app.route('/') #Home Index Page Path
def home():
  return render_template('home.html') #Calls home.html template

@app.route('/espn') #ESPN Results index
def espn():

# Indexes into /espn page of website. render_template function calls on the html template for the ESPN results and translates each dataframe into an html table. All the tables are stored within a table list to be called within the espn_view.html template.
    return render_template('espn_view.html',tables=[qb_efinal.to_html(classes='espn'),\
                                               rb_efinal.to_html(classes='espn'),\
                                               wr_efinal.to_html(classes='espn'),\
                                               te_efinal.to_html(classes='espn'),\
                                               k_efinal.to_html(classes='espn'),\
                                               defense_efinal.to_html(classes='espn')],\
                                               titles = ['na', 'Quarterbacks', 'Running Backs',\
                                               'Wide Receivers', 'Tight Ends', 'Kickers',\
                                               'Defenses/Special Teams'])

# Indexes into /yahoo page of website. Does the same as ESPN page in translating table
@app.route('/yahoo')
def yahoo():
    return render_template('yahoo_view.html',tables=[qb_yfinal.to_html(classes='yahoo'),\
                                               rb_yfinal.to_html(classes='yahoo'),\
                                               wr_yfinal.to_html(classes='yahoo'),\
                                               te_yfinal.to_html(classes='yahoo'),\
                                               k_yfinal.to_html(classes='yahoo'),\
                                               defense_yfinal.to_html(classes='yahoo')],\
                                               titles = ['na', 'Quarterbacks', 'Running Backs',\
                                               'Wide Receivers', 'Tight Ends', 'Kickers',\
                                               'Defenses/Special Teams'])

@app.route('/twoqb')
def ycup():
    return render_template('ycup_view.html',tables=[qb_ycup.to_html(classes='ycup'),\
                                               rb_ycup.to_html(classes='ycup'),\
                                               wr_ycup.to_html(classes='ycup'),\
                                               te_ycup.to_html(classes='ycup'),\
                                               k_ycup.to_html(classes='ycup'),\
                                               defense_ycup.to_html(classes='ycup')],\
                                               titles = ['na', 'Quarterbacks', 'Running Backs',\
                                               'Wide Receivers', 'Tight Ends', 'Kickers',\
                                               'Defenses/Special Teams'])


# Indexes into /custom page of website. Uses Flask function 'GET' and 'POST' to communicate with user and receive input from said user.
@app.route('/custom', methods=['GET', 'POST'])
def custom_func():
  form = CustomForm(request.form) #Instatiates the form created in forms.py

  if request.method == 'POST':
    if form.validate() == False: #If any of the inputs are empty and therefore doesn't validate
      flash('All fields are required.') #Error message flashed to user
      return render_template('custom.html', form=form)#Resets page with error message
    else:
            #Adds user input values to custom dictionary
            #League Settings Input
            custom_settings['teams'] = int(request.form['teams']) #Converts string data into\
            #integer value; Form validates whether input is a whole number value

            custom_settings['auction_budget'] = int(request.form['auction_budget'])
            #Roster Composition
            custom_settings['qb'] = int(request.form['qb'])
            input_rb = float(request.form['input_rb']) #Also takes in float values
            input_wr = float(request.form['input_wr'])
            input_flex = float(request.form['input_flex'])
            custom_settings['rb'] = input_rb + (input_flex/2)
            custom_settings['wr'] = input_wr + (input_flex/2)
            custom_settings['te'] = int(request.form['te'])
            custom_settings['k'] = int(request.form['k'])
            custom_settings['defense'] = int(request.form['defense'])
            custom_settings['bench'] = int(request.form['bench'])
            #Point Values
            custom_settings['pass_yds'] = 1/float(request.form['pass_yds'])
            custom_settings['pass_tds'] = float(request.form['pass_tds'])
            custom_settings['interceptions'] = float(request.form['interceptions'])
            custom_settings['rush_yds'] = 1/float(request.form['rush_yds'])
            custom_settings['rush_tds'] = float(request.form['rush_tds'])
            custom_settings['recs'] = float(request.form['recs'])
            custom_settings['rec_yds'] = 1/float(request.form['rec_yds'])
            custom_settings['rec_tds'] = float(request.form['rec_tds'])
            custom_settings['two_point'] = float(request.form['two_point'])
            custom_settings['fl'] = float(request.form['fl'])
            #Kickers
            custom_settings['u20'] = float(request.form['u20'])
            custom_settings['u30'] = float(request.form['u30'])
            custom_settings['u40'] = float(request.form['u40'])
            custom_settings['u50'] = float(request.form['u50'])
            custom_settings['u70'] = float(request.form['u70'])
            custom_settings['pat'] = float(request.form['pat'])
            #Defense
            custom_settings['sack'] = float(request.form['sack'])
            custom_settings['def_int'] = float(request.form['def_int'])
            custom_settings['fr'] = float(request.form['fr'])
            custom_settings['def_td'] = float(request.form['def_td'])
            custom_settings['spc_td'] = float(request.form['spc_td'])
            custom_settings['sfty'] = float(request.form['sfty'])

            custom_qb,custom_rb,custom_wr,custom_te,custom_k,custom_def =\
            custom(qb_data, rb_data,wr_data, te_data, k_data, def_data,\
                    custom_percentiles, custom_settings) #Transforms data into custom results.

            tables = list() #Creates new list for dataframes and render_template function below
            titles = list() #Creates new list for dataframe titles

            return render_template('custom.html',tables=[custom_qb.to_html(classes='custom'),custom_rb.to_html(classes='custom'),custom_wr.to_html(classes='custom'),custom_te.to_html(classes='custom'),custom_k.to_html(classes='custom'),custom_def.to_html(classes='custom')],titles = ['na', 'Quarterbacks', 'Running Backs', 'Wide Receivers','Tight Ends','Kickers', 'Defenses/Special Teams'], success = True)

  elif request.method == 'GET': #Loads page information into web page index /custom
    return render_template('custom.html', form=form)

if __name__ == '__main__': #Hardcodes string name '__main__' to name value
    app.run(debug=True) #Runs app; debug=True gives feedback if website not working


"""
Deprecated Code

@app.route('/about') #Indexes
def about():
  return render_template('about.html')
"""
