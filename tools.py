#Tom Lancaster (c) 2019
#Capstone Project - Fantasy Football Auction Draft Tool

#functions.py

#=================================================================
#Purpose: To consolidate all functions related to tasks for project
#=================================================================


import pandas as pd #Import Pandas Library and alias as pd
import math as mt #Imports Math library package for floor and ceiling functions

#======================================================================
#    Functions
#======================================================================

#Takes original QB stats and transforms the data into

def total_pts_qb(df, perc, settings):

    df1 = df.copy() #Preserves the original data by creating a new dataframe to be manipulated
    #Multiplies each statistic by their weighted value
    #Totals fantasy points of each category
    df1['yds'] = df1['yds'] * settings['pass_yds']
    df1['td'] = df1['td'] * settings['pass_tds']
    df1['int'] = df1['int'] * settings['interceptions']
    df1['rush_yds'] = df1['rush_yds'] * settings['rush_yds']
    df1['rush_td'] = df1['rush_td'] * settings['rush_tds']
    df1['fl'] = df1['fl'] * settings['fl']
    df1['fpts'] = df1.sum(1) - df1['g'] #Totals all the players fantasy point totals
    df1['PPG'] = df1['fpts'] / df1['g'] #Finds Fantasy Points Per Game (PPG)

    #Resets Dataframe Index in numerical order (1...n) of Total Fantasy Points
    df1 = df1.sort_values(by=['fpts'],ascending=False)
    index_arr = df1.index.values
    len_index_arr = len(index_arr)
    for i in range(len_index_arr):
        index_arr[i] = i+1

    #Sets Percentiles based on baseline levels which helps us find points to dollar ratio
    elite_star = perc['qb']['elite_starter']
    starter = perc['qb']['starter']
    top_res = perc['qb']['top_reserve']
    roster = perc['qb']['roster']
    df1['elite_starter'] = df1['fpts'] - df1.loc[elite_star]['fpts'] #Finds point value at that percentile
    df1['starter'] = df1['fpts'] - df1.loc[starter]['fpts']
    df1['top_reserve'] = df1['fpts'] - df1.loc[top_res]['fpts']
    df1['roster'] = df1['fpts'] - df1.loc[roster]['fpts']

    set_to_0(df1) #Resets certain columns negative values to 0

    df1['sum_pts'] = df1['elite_starter']+df1['starter']+df1['top_reserve']+df1['roster'] #Totals point differentials of each player compared to each baseline

    return df1

#Totals points for Running Backs
def total_pts_rb(df, perc, settings):

    df1 = df.copy()

    #Running Back specific categories are totaled by fantasy points
    df1['rush_yds'] = df1['rush_yds'] * settings['rush_yds']
    df1['td'] = df1['td'] * settings['rush_tds']
    df1['rec'] = df1['rec'] * settings['recs']
    df1['rec_yds'] = df1['rec_yds'] * settings['rec_yds']
    df1['rec_td'] = df1['rec_td'] * settings['rec_tds']
    df1['fl'] = df1['fl'] * settings['fl']
    df1['fpts'] = df1.sum(1) - df1['games'] #Totals all the players fantasy point totals
    df1['PPG'] = df1['fpts'] / df1['games']

    #Resets Dataframe Index in order of Total Fantasy Points
    df1 = df1.sort_values(by=['fpts'],ascending=False)
    index_arr = df1.index.values
    len_index_arr = len(index_arr)
    for i in range(len_index_arr):
        index_arr[i] = i+1

    #Sets Percentiles based on selection
    elite_star = perc['rb']['elite_starter']
    starter = perc['rb']['starter']
    top_res = perc['rb']['top_reserve']
    roster = perc['rb']['roster']
    df1['elite_starter'] = df1['fpts'] - df1.loc[elite_star]['fpts']
    df1['starter'] = df1['fpts'] - df1.loc[starter]['fpts']
    df1['top_reserve'] = df1['fpts'] - df1.loc[top_res]['fpts']
    df1['roster'] = df1['fpts'] - df1.loc[roster]['fpts']

    set_to_0(df1) #Resets certain columns negative values to 0

    df1['sum_pts'] = df1['elite_starter']+df1['starter']+df1['top_reserve']+df1['roster']

    return df1

#Totals points for Wide Receivers
def total_pts_wr(df, perc, settings):

    df1 = df.copy()
    df1['rec'] = df1['rec'] * settings['recs']
    df1['rec_yds'] = df1['rec_yds'] * settings['rec_yds']
    df1['rec_td'] = df1['rec_td'] * settings['rec_tds']
    df1['rush_yds'] = df1['rush_yds'] * settings['rush_yds']
    df1['rush_td'] = df1['rush_td'] * settings['rec_tds']
    df1['fl'] = df1['fl'] * settings['fl']
    df1['fpts'] = df1.sum(1) - df1['g'] #Totals all the players fantasy point totals
    df1['PPG'] = df1['fpts'] / df1['g']

    #Resets Dataframe Index in order of Total Fantasy Points
    df1 = df1.sort_values(by=['fpts'],ascending=False)
    index_arr = df1.index.values
    len_index_arr = len(index_arr)
    for i in range(len_index_arr):
        index_arr[i] = i+1

    #Sets Percentiles based on selection
    elite_star = perc['wr']['elite_starter']
    starter = perc['wr']['starter']
    top_res = perc['wr']['top_reserve']
    roster = perc['wr']['roster']
    df1['elite_starter'] = df1['fpts'] - df1.loc[elite_star]['fpts']
    df1['starter'] = df1['fpts'] - df1.loc[starter]['fpts']
    df1['top_reserve'] = df1['fpts'] - df1.loc[top_res]['fpts']
    df1['roster'] = df1['fpts'] - df1.loc[roster]['fpts']

    set_to_0(df1) #Resets certain columns negative values to 0

    df1['sum_pts'] = df1['elite_starter']+df1['starter']+df1['top_reserve']+df1['roster']

    return df1

#Totals fantasy points for Tight Ends
def total_pts_te(df, perc, settings):

    df1 = df.copy()
    df1['rec'] = df1['rec'] * settings['recs']
    df1['rec_yards'] = df1['rec_yards'] * settings['rec_yds']
    df1['rec_td'] = df1['rec_td'] * settings['rec_tds']
    df1['rush_yds'] = df1['rush_yds'] * settings['rush_yds']
    df1['rush_td'] = df1['rush_td'] * settings['rush_tds']
    df1['fl'] = df1['fl'] * settings['fl']
    df1['fpts'] = df1.sum(1) - df1['g'] #Totals all the players fantasy point totals
    df1['PPG'] = df1['fpts'] / df1['g']

    #Resets Dataframe Index in order of Total Fantasy Points
    df1 = df1.sort_values(by=['fpts'],ascending=False)
    index_arr = df1.index.values
    len_index_arr = len(index_arr)
    for i in range(len_index_arr):
        index_arr[i] = i+1

    #Sets Percentiles based on selection
    elite_star = perc['te']['elite_starter']
    starter = perc['te']['starter']
    top_res = perc['te']['top_reserve']
    roster = perc['te']['roster']
    df1['elite_starter'] = df1['fpts'] - df1.loc[elite_star]['fpts']
    df1['starter'] = df1['fpts'] - df1.loc[starter]['fpts']
    df1['top_reserve'] = df1['fpts'] - df1.loc[top_res]['fpts']
    df1['roster'] = df1['fpts'] - df1.loc[roster]['fpts']

    set_to_0(df1) #Resets certain columns negative values to 0

    df1['sum_pts'] = df1['elite_starter']+df1['starter']+df1['top_reserve']+df1['roster']

    return df1

#Totals fantasy points for Kickers
def total_pts_k(df, perc, settings):

    df1 = df.copy()
    df1['u20'] = df1['u20'] * settings['u20']
    df1['u30'] = df1['u30'] * settings['u30']
    df1['u40'] = df1['u40'] * settings['u40']
    df1['u50'] = df1['u50'] * settings['u50']
    df1['u70'] = df1['u70'] * settings['u70']
    df1['xpt'] = df1['xpt'] * settings['pat']
    df1['fpts'] = df1.sum(1) - df1['g'] #Totals all the players fantasy point totals
    df1['PPG'] = df1['fpts'] / df1['g']

    #Resets Dataframe Index in order of Total Fantasy Points
    df1 = df1.sort_values(by=['fpts'],ascending=False)
    index_arr = df1.index.values
    len_index_arr = len(index_arr)
    for i in range(len_index_arr):
        index_arr[i] = i+1

    #Sets Percentiles based on selection
    elite_star = perc['k']['elite_starter']
    starter = perc['k']['starter']
    top_res = perc['k']['top_reserve']
    roster = perc['k']['roster']
    df1['elite_starter'] = df1['fpts'] - df1.loc[elite_star]['fpts']
    df1['starter'] = df1['fpts'] - df1.loc[starter]['fpts']
    df1['top_reserve'] = df1['fpts'] - df1.loc[top_res]['fpts']
    df1['roster'] = df1['fpts'] - df1.loc[roster]['fpts']

    set_to_0(df1) #Resets certain columns negative values to 0

    df1['sum_pts'] = df1['elite_starter']+df1['starter']+df1['top_reserve']+df1['roster']

    return df1

#Totals fantasy points for Defense/Special Teams
def total_pts_def(df, perc, settings):

    df1 = df.copy()
    df1['sack'] = df1['sack'] * settings['sack']
    df1['int'] = df1['int'] * settings['int']
    df1['fr'] = df1['fr'] * settings['sfty']
    df1['def_td'] = df1['def_td'] * settings['def_td']
    df1['sfty'] = df1['sfty'] * settings['sfty']
    #df1['spc_td'] = df1['spc_td'] * settings['def_td']
    df1['fpts'] = df1.sum(1) - df1['g'] #Totals all the players fantasy point totals
    df1['PPG'] = df1['fpts'] / df1['g']

    #Resets Dataframe Index in order of Total Fantasy Points rank
    df1 = df1.sort_values(by=['fpts'],ascending=False)
    index_arr = df1.index.values
    len_index_arr = len(index_arr)
    for i in range(len_index_arr):
        index_arr[i] = i+1

    #Sets Percentiles based on selection
    elite_star = perc['defense']['elite_starter']
    starter = perc['defense']['starter']
    top_res = perc['defense']['top_reserve']
    roster = perc['defense']['roster']
    df1['elite_starter'] = df1['fpts'] - df1.loc[elite_star]['fpts']
    df1['starter'] = df1['fpts'] - df1.loc[starter]['fpts']
    df1['top_reserve'] = df1['fpts'] - df1.loc[top_res]['fpts']
    df1['roster'] = df1['fpts'] - df1.loc[roster]['fpts']

    set_to_0(df1) #Resets certain columns negative values to 0

    df1['sum_pts'] = df1['elite_starter']+df1['starter']+df1['top_reserve']+df1['roster']

    return df1

def percentiles(perc_dict, league_dict):
    for position, p_info in perc_dict.items():
        for key in p_info:
        #Computes percentile of an elite starter, starter, top_reserve, and roster baselines
        #at each  position. This depends on the number of starters for each position and
        #the number of teams in the league.
            if key == 'elite_starter':
                perc_dict[position][key] = mt.floor(league_dict[position]*league_dict['teams']*0.5)
            elif key == 'starter':
                perc_dict[position][key] = mt.floor(league_dict[position]*league_dict['teams'])

            #"Top reserve" percentile different for running backs and wide receivers
            elif key == 'top_reserve' and position == 'rb':
                perc_dict[position][key] = mt.floor(league_dict[position]*league_dict['teams']*1.3)
            elif key == 'top_reserve' and position == 'wr':
                perc_dict[position][key] = mt.floor(league_dict[position]*league_dict['teams']*1.3)
            elif key == 'top_reserve':
                perc_dict[position][key] = mt.floor(league_dict[position]*league_dict['teams']*1.5)

            #Quarterback 'Roster' percentile different than other positions
            elif key == 'roster' and position == 'qb':
                perc_dict[position][key] = mt.floor(league_dict[position]*league_dict['teams'] + (league_dict['teams']+3))
            elif key == 'roster':
                perc_dict[position][key] = mt.floor(league_dict[position]*league_dict['teams']*1.6)
            else:
                continue

    return perc_dict

#Baseline point subtraction leads to negative player values which is not possible so negative player values are reset to zero by this function
def set_to_0(df1):

    new_cols = ['elite_starter', 'starter', 'top_reserve', 'roster']

    for col in new_cols:
        df1.loc[df1[col] < 0, col] = 0.0

    return df1


#Prints the entire dataframe
def print_full_pts(df1):
    pd.set_option('display.max_rows', len(df1))
    cols = list(df1.columns.values)
    print(df1.loc[:][cols])
    pd.reset_option('display.max_rows')

    return 0

#Calculates total points in entire league and divides it by the total amount of usable money
# for points to dollar ratio that applied to each player
def points_to_dollar(qb, rb, wr, te, k, defense, settings_dict):

    qb_sum = qb['sum_pts'].sum()
    rb_sum = rb['sum_pts'].sum()
    wr_sum = wr['sum_pts'].sum()
    te_sum = te['sum_pts'].sum()
    k_sum = k['sum_pts'].sum()
    def_sum = defense['sum_pts'].sum()
    total_lg_pts = qb_sum + rb_sum + wr_sum + te_sum + k_sum + def_sum
    free_money = settings_dict['teams'] * settings_dict['auction_budget'] - (settings_dict['teams'] * settings_dict['total_roster'])
    pts_to_dollar = total_lg_pts / free_money
    result = round(pts_to_dollar,2)

    return result

#Calculates player values based Yahoo! league and scoring settings
#Calls on all supporting functions established in this file
def yahoo(qb, rb, wr, te, k, defense, perc1, settings_dict):
    qb = total_pts_qb(qb, perc1, settings_dict)
    rb = total_pts_rb(rb, perc1, settings_dict)
    wr = total_pts_wr(wr, perc1, settings_dict)
    te = total_pts_te(te, perc1, settings_dict)
    k = total_pts_k(k, perc1, settings_dict)
    defense = total_pts_def(defense, perc1, settings_dict)
    pts_dol = points_to_dollar(qb, rb, wr, te, k, defense, settings_dict)

    qb['Value'] = qb['sum_pts']/pts_dol
    qb.loc[qb['Value'] < 1.0, 'Value'] = 1.0
    rb['Value'] = rb['sum_pts']/pts_dol
    rb.loc[rb['Value'] < 1.0, 'Value'] = 1.0
    wr['Value'] = wr['sum_pts']/pts_dol
    wr.loc[wr['Value'] < 1.0, 'Value'] = 1.0
    te['Value'] = te['sum_pts']/pts_dol
    te.loc[te['Value'] < 1.0, 'Value'] = 1.0
    k['Value'] = k['sum_pts']/pts_dol
    k.loc[k['Value'] < 1.0, 'Value'] = 1.0
    defense['Value'] = defense['sum_pts']/pts_dol
    defense.loc[defense['Value'] < 1.0, 'Value'] = 1.0

    format_mapping={'PPG': '{:,.1f}','Value': '${:,.2f}'}
    for key, value in format_mapping.items():
        qb[key] = qb[key].apply(value.format)
        rb[key] = rb[key].apply(value.format)
        wr[key] = wr[key].apply(value.format)
        te[key] = te[key].apply(value.format)
        k[key] = k[key].apply(value.format)
        defense[key] = defense[key].apply(value.format)

    #Calculates the number of players to display in the final output
    num_qb = mt.ceil(perc1['qb']['roster']*1.25)
    num_rb = mt.ceil(perc1['rb']['roster']*1.40)
    num_wr = mt.ceil(perc1['wr']['roster']*1.40)
    num_te = mt.ceil(perc1['te']['roster']*1.25)
    num_k = mt.ceil(perc1['k']['roster']*1.25)
    num_def = mt.ceil(perc1['defense']['roster']*1.25)

    cols = ['Name','PPG','Value'] #Only show these columns

    qb_final=qb[:num_qb][cols]
    rb_final=rb[:num_rb][cols]
    wr_final=wr[:num_wr][cols]
    te_final=te[:num_te][cols]
    k_final=k[:num_k][cols]
    defense_final=defense[:num_def][cols]

    return qb_final, rb_final, wr_final, te_final, k_final, defense_final

#Calculates player values based ESPN league and scoring settings
def espn(qb, rb, wr, te, k, defense, perc1, settings_dict):
    qb = total_pts_qb(qb, perc1, settings_dict)
    rb = total_pts_rb(rb, perc1, settings_dict)
    wr = total_pts_wr(wr, perc1, settings_dict)
    te = total_pts_te(te, perc1, settings_dict)
    k = total_pts_k(k, perc1, settings_dict)
    defense = total_pts_def(defense, perc1, settings_dict)
    pts_dol = points_to_dollar(qb, rb, wr, te, k, defense, settings_dict)

    qb['Value'] = qb['sum_pts']/pts_dol
    qb.loc[qb['Value'] < 1.0, 'Value'] = 1.0
    rb['Value'] = rb['sum_pts']/pts_dol
    rb.loc[rb['Value'] < 1.0, 'Value'] = 1.0
    wr['Value'] = wr['sum_pts']/pts_dol
    wr.loc[wr['Value'] < 1.0, 'Value'] = 1.0
    te['Value'] = te['sum_pts']/pts_dol
    te.loc[te['Value'] < 1.0, 'Value'] = 1.0
    k['Value'] = k['sum_pts']/pts_dol
    k.loc[k['Value'] < 1.0, 'Value'] = 1.0
    defense['Value'] = defense['sum_pts']/pts_dol
    defense.loc[defense['Value'] < 1.0, 'Value'] = 1.0

    format_mapping={'PPG': '{:,.1f}','Value': '${:,.2f}'}
    for key, value in format_mapping.items():
        qb[key] = qb[key].apply(value.format)
        rb[key] = rb[key].apply(value.format)
        wr[key] = wr[key].apply(value.format)
        te[key] = te[key].apply(value.format)
        k[key] = k[key].apply(value.format)
        defense[key] = defense[key].apply(value.format)

    num_qb = mt.ceil(perc1['qb']['roster']*1.25)
    num_rb = mt.ceil(perc1['rb']['roster']*1.40)
    num_wr = mt.ceil(perc1['wr']['roster']*1.40)
    num_te = mt.ceil(perc1['te']['roster']*1.25)
    num_k = mt.ceil(perc1['k']['roster']*1.25)
    num_def = mt.ceil(perc1['defense']['roster']*1.25)

    cols = ['Name','PPG','Value']

    qb_final=qb[:num_qb][cols]
    rb_final=rb[:num_rb][cols]
    wr_final=wr[:num_wr][cols]
    te_final=te[:num_te][cols]
    k_final=k[:num_k][cols]
    defense_final=defense[:num_def][cols]

    return qb_final, rb_final, wr_final, te_final, k_final, defense_final

def ycup(qb, rb, wr, te, k, defense, perc1, settings_dict):
    qb = total_pts_qb(qb, perc1, settings_dict)
    rb = total_pts_rb(rb, perc1, settings_dict)
    wr = total_pts_wr(wr, perc1, settings_dict)
    te = total_pts_te(te, perc1, settings_dict)
    k = total_pts_k(k, perc1, settings_dict)
    defense = total_pts_def(defense, perc1, settings_dict)
    pts_dol = points_to_dollar(qb, rb, wr, te, k, defense, settings_dict)

    qb['Value'] = qb['sum_pts']/pts_dol
    qb.loc[qb['Value'] < 1.0, 'Value'] = 1.0
    rb['Value'] = rb['sum_pts']/pts_dol
    rb.loc[rb['Value'] < 1.0, 'Value'] = 1.0
    wr['Value'] = wr['sum_pts']/pts_dol
    wr.loc[wr['Value'] < 1.0, 'Value'] = 1.0
    te['Value'] = te['sum_pts']/pts_dol
    te.loc[te['Value'] < 1.0, 'Value'] = 1.0
    k['Value'] = k['sum_pts']/pts_dol
    k.loc[k['Value'] < 1.0, 'Value'] = 1.0
    defense['Value'] = defense['sum_pts']/pts_dol
    defense.loc[defense['Value'] < 1.0, 'Value'] = 1.0

    format_mapping={'PPG': '{:,.1f}','Value': '${:,.2f}'}
    for key, value in format_mapping.items():
        qb[key] = qb[key].apply(value.format)
        rb[key] = rb[key].apply(value.format)
        wr[key] = wr[key].apply(value.format)
        te[key] = te[key].apply(value.format)
        k[key] = k[key].apply(value.format)
        defense[key] = defense[key].apply(value.format)

    num_qb = mt.ceil(perc1['qb']['roster']*1.25)
    num_rb = mt.ceil(perc1['rb']['roster']*1.40)
    num_wr = mt.ceil(perc1['wr']['roster']*1.40)
    num_te = mt.ceil(perc1['te']['roster']*1.25)
    num_k = mt.ceil(perc1['k']['roster']*1.25)
    num_def = mt.ceil(perc1['defense']['roster']*1.25)

    cols = ['Name','PPG','Value']

    qb_final=qb[:num_qb][cols]
    rb_final=rb[:num_rb][cols]
    wr_final=wr[:num_wr][cols]
    te_final=te[:num_te][cols]
    k_final=k[:num_k][cols]
    defense_final=defense[:num_def][cols]

    return qb_final, rb_final, wr_final, te_final, k_final, defense_final

#Calculates player values based the user's inputted league and scoring settings
def custom(qb, rb, wr, te, k, defense, perc_dict, settings_dict):

   #Command Line interface for custom option; now deprecated.
    """
    #User Input for Custom Option
    print("\n------------LEAGUE SETTINGS---------------")
    settings_dict["teams"] = inputNumber('Teams in League: ')
    settings_dict["auction_budget"] = inputNumber('Auction Budget: ')
    settings_dict["qb"] = inputNumber('Starting Quarterback\'s: ')
    input_rb = inputNumber('Starting Running Back\'s: ')
    input_wr = inputNumber('Starting Wide Receivers\'s: ')
    input_flex = inputNumber('Starting FLEX Positions: ')
    settings_dict["rb"] = float(input_rb) + (float(input_flex)/2)
    settings_dict["wr"] = float(input_wr) + (float(input_flex)/2)
    settings_dict["te"] = inputNumber('Starting Tight End\'s: ')
    settings_dict["k"] = inputNumber('Starting Kicker\'s: ')
    settings_dict["defense"] = inputNumber('Starting Defenses: ')
    settings_dict["bench"] = inputNumber('Bench Size: ')
    #settings_dict["total_roster"] = float(settings_dict["qb"]) + float(input_rb) + float(input_wr) + int(input_flex) + float(settings_dict["te"]) \
    #+ float(settings_dict["k"]) + float(settings_dict["def"]) + float(settings_dict["bench"])
    print("\n----------POINT SETTINGS--------------")
    print("\n-- Skill Positions --")
    settings_dict["pass_yds"] = 1/inputNumber('Passing Yards Per Point: ')
    settings_dict["pass_tds"] = inputNumber('Passing Touchdowns: ')
    settings_dict["interceptions"] = inputNumber('Interceptions: ')
    settings_dict["rush_yds"] = 1/inputNumber('Rushing Yards Per Point: ')
    settings_dict["rush_tds"] = inputNumber('Rushing Touchdowns: ')
    settings_dict["recs"] = inputNumber('Receptions: ')
    settings_dict["rec_yds"] = 1/inputNumber('Receiving Yards Per Point: ')
    settings_dict["rec_tds"] = inputNumber('Receiving Touchdowns: ')
    settings_dict["two_point"] = inputNumber('Two Point Conversions: ')
    settings_dict["fl"] = inputNumber('Fumbles Lost: ')
    print("\n-- Kickers --")
    settings_dict["u20"] = inputNumber('Field Goals 0-19: ')
    settings_dict["u30"] = inputNumber('Field Goals 20-29: ')
    settings_dict["u40"] = inputNumber('Field Goals 30-39: ')
    settings_dict["u50"] = inputNumber('Field Goals 40-49: ')
    settings_dict["u70"] = inputNumber('Field Goals 50+: ')
    settings_dict["pat"] = inputNumber('Extra Point: ')
    print("\n-- Defense --")
    settings_dict["sack"] = inputNumber('Sacks: ')
    settings_dict["int"] = inputNumber('Defensive Interceptions: ')
    settings_dict["fr"] = inputNumber('Fumbles Recovered: ')
    settings_dict["def_tds"] = inputNumber('Defensive Touchdowns: ')
    settings_dict["spc_td"] = inputNumber('Special Team\'s Touchdowns: ')
    settings_dict["sfty"] = inputNumber('Safety: ')
    """

    new_perc_dict = percentiles(perc_dict, settings_dict)

    qb = total_pts_qb(qb, new_perc_dict, settings_dict)
    rb = total_pts_rb(rb, new_perc_dict, settings_dict)
    wr = total_pts_wr(wr, new_perc_dict, settings_dict)
    te = total_pts_te(te, new_perc_dict, settings_dict)
    k = total_pts_k(k, new_perc_dict, settings_dict)
    defense = total_pts_def(defense, new_perc_dict, settings_dict)
    pts_dol = points_to_dollar(qb, rb, wr, te, k, defense, settings_dict)

    #Resets all values less than $1 to $1 since that is the lowest possible bid
    qb['Value'] = qb['sum_pts']/pts_dol
    qb.loc[qb['Value'] < 1.0, 'Value'] = 1.0
    rb['Value'] = rb['sum_pts']/pts_dol
    rb.loc[rb['Value'] < 1.0, 'Value'] = 1.0
    wr['Value'] = wr['sum_pts']/pts_dol
    wr.loc[wr['Value'] < 1.0, 'Value'] = 1.0
    te['Value'] = te['sum_pts']/pts_dol
    te.loc[te['Value'] < 1.0, 'Value'] = 1.0
    k['Value'] = k['sum_pts']/pts_dol
    k.loc[k['Value'] < 1.0, 'Value'] = 1.0
    defense['Value'] = defense['sum_pts']/pts_dol
    defense.loc[defense['Value'] < 1.0, 'Value'] = 1.0

    format_mapping={'PPG': '{:,.1f}','Value': '${:,.2f}'} # Establish formats 'PPG' to near tenth
                                                         # decimal and 'Value' to nearest hundredth
                                                         # decimal since it is a monetary value

   #Applies formatting established right above to all dataframes
    for key, value in format_mapping.items():
        qb[key] = qb[key].apply(value.format)
        rb[key] = rb[key].apply(value.format)
        wr[key] = wr[key].apply(value.format)
        te[key] = te[key].apply(value.format)
        k[key] = k[key].apply(value.format)
        defense[key] = defense[key].apply(value.format)

    num_qb = mt.ceil(perc_dict['qb']['roster']*1.25)
    num_rb = mt.ceil(perc_dict['rb']['roster']*1.40)
    num_wr = mt.ceil(perc_dict['wr']['roster']*1.40)
    num_te = mt.ceil(perc_dict['te']['roster']*1.25)
    num_k = mt.ceil(perc_dict['k']['roster']*1.25)
    num_def = mt.ceil(perc_dict['defense']['roster']*1.25)

    cols = ['Name','PPG','Value']

    qb_final=qb[:num_qb][cols]
    rb_final=rb[:num_rb][cols]
    wr_final=wr[:num_wr][cols]
    te_final=te[:num_te][cols]
    k_final=k[:num_k][cols]
    defense_final=defense[:num_def][cols]

    return qb_final, rb_final, wr_final, te_final, k_final, defense_final


"""
#======================================================================
#   Deprecated Functions
#======================================================================

#def mk_df(list_in):
    #a = array(list_in)
    #rows = a.shape[0] #Finds the number of rows in the list
    #cols = a.shape[1] #Finds the number of columns in the list
    #df = pd.DataFrame(list_in)
    #print(df)


def open_xfile(data):

    workbook = xl.open_workbook("./player_stats.xlsx")

    sheet_names = workbook.sheet_names()
    print('Sheet Names ', sheet_names)
    sheet_cnt = len(sheet_names)

    #Assigns workbook sheet name to variable "xl_sheet"
    #xl_sheet = workbook.sheet_by_name(sheet_names[0])

    sheets = [None] * sheet_cnt
    data = [[]] * sheet_cnt
    for i in range(sheet_cnt):
        sheets[i] = workbook.sheet_by_index(i)
        cols = sheets[i].ncols
        #print("sheets["+str(i)+"].ncols="+str(cols))
        rows = sheets[i].nrows
        #print("sheets["+str(i)+"].nrows="+str(rows))
        data[i] = [[sheets[i].cell_value(r, c) for c in range(cols)] for r in range(rows)]

    return data

#Function takes in a 2D list as a parameter and prints out all the data
def print_2dlist(list_in):

    a = array(list_in)
    rows = a.shape[0]
    cols = a.shape[1]

    for c in range(cols):
        for r in range(rows):
            print(list_in[r][c])

def fnd_sheet_name(sht_num):
    xl_sheet = xl.sheet_by_index(sht_num)
    print('Sheet Name: %s' % xl_sheet.name)

def print_df(list_in):
    #a = array(list_in)
    #rows = a.shape[0] #Finds the number of rows in the list
    #cols = a.shape[1] #Finds the number of columns in the list
    df = pd.DataFrame(list_in)
    print(df)

#Function taken from: https://www.101computing.net/number-only/
def inputNumber(message):
  while True:
    try:
       userInput = float(input(message))
    except ValueError:
       print("Not a number! Try again.")
       continue
    else:
       return userInput
       break

"""
