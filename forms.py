from wtforms import Form, TextField, IntegerField, FloatField, SubmitField, validators,\
                    ValidationError #wtforms package with input data types and input validation tools

class CustomForm(Form): #Called by routes.py
    #League Settings Input
    #Each variable takes a whole or fraction number input from the user
    #The input field validates the user input
    teams = IntegerField('Teams in League:', validators=[validators.required\
    ("Uh-oh! Only whole numbers only for 'Teams in League' field.")])
    auction_budget = IntegerField('Auction Budget:', validators=[validators.required\
    ("Out of money? Only whole numbers only for 'Auction Budget' field.")])
    #Roster Composition
    qb = IntegerField('Starting Quarterbacks:', validators=[validators.required\
    ("SACKED! Only whole numbers only for 'Starting Quarterbacks' field.")])
    input_rb = IntegerField('Starting Running Backs:', validators=[validators.required\
    ("TACKLE FOR A LOSS! Only whole numbers only for 'Starting Running Backs' field.")])
    input_wr = IntegerField('Starting Wide Receivers:', validators=[validators.required\
    ("THROUGH THE FINGERS! Only whole numbers only for 'Starting Wide Receivers' field.")])
    input_flex = IntegerField('Starting FLEX (RB/WR/TE) Positions:', validators=[validators.required\
    ("OUT OF BOUNDS! Only whole numbers only for 'Starting FLEX (RB/WR/TE) Positions' field.")])
    te = IntegerField('Starting Tight Ends:', validators=[validators.required\
    ("FUMBLE! Only whole numbers only for 'Starting Tight Ends' field.")])
    k = IntegerField('Starting Kickers:', validators=[validators.required\
    ("BLOCKED KICK! Only whole numbers only for 'Starting Kicker' field.")])
    defense = IntegerField('Starting Defense/Special Teams:', validators=[validators.required\
    ("MAN DOWN! Only whole numbers only for 'Starting Defense/Special Teams' field.")])
    bench = IntegerField('Bench Size:', validators=[validators.required\
    ("RIDING THE PINE! Only whole numbers only for 'Bench Size' field.")])
    #Point Values
    pass_yds = FloatField('Passing Yards Per Point:', validators=[validators.required\
    ("INTERCEPTED! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Passing Yards Per Point' field.")])
    pass_tds = FloatField('Passing Touchdowns:', validators=[validators.required\
    ("THROWING DUCKS! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Passing Touchdowns' field.")])
    interceptions = FloatField('Interceptions:', validators=[validators.required\
    ("BAD PASS! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Interceptions' field.")])
    rush_yds = FloatField('Rushing Yards Per Point:', validators=[validators.required\
    ("NO GAIN! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Rushing Yards Per Point' field.")])
    rush_tds = FloatField('Rushing Touchdowns:', validators=[validators.required\
    ("JUST SHORT! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Rushing Touchdowns' field.")])
    recs = FloatField('Receptions:', validators=[validators.required\
    ("BUTTERFINGERS! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Receptions' field.")])
    rec_yds = FloatField('Receiving Yards Per Point:', validators=[validators.required\
    ("OVERTHROWN! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Receiving Yards Per Point' field.")])
    rec_tds = FloatField('Receiving Touchdowns:', validators=[validators.required\
    ("PLAY BROKEN UP! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Receiving Touchdowns' field.")])
    two_point = FloatField('Two Point Conversions:', validators=[validators.required\
    ("NO GOOD! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Two Point Conversions' field.")])
    fl = FloatField('Fumbles Lost:', validators=[validators.required\
    ("TURNOVER! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Fumbles Lost' field.")])
    #Kickers
    u20 = FloatField('Field Goals 0-19 yards:', validators=[validators.required\
    ("WIDE LEFT! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Field Goals 0-19 yards' field.")])
    u30 = FloatField('Field Goals 20-29 yards:', validators=[validators.required\
    ("WIDE RIGHT! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Field Goals 20-29 yards' field.")])
    u40 = FloatField('Field Goals 30-39 yards:', validators=[validators.required\
    ("OFF THE GOALPOST! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Field Goals 30-39 yards' field.")])
    u50 = FloatField('Field Goals 40-49 yards:', validators=[validators.required\
    ("BLOCKED KICK! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Field Goals 40-49 yards' field.")])
    u70 = FloatField('Field Goals 50+ yards:', validators=[validators.required\
    ("Just short of the goal post! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Field Goals 50+ yards' field.")])
    pat = FloatField\
    ('Extra Point/PAT:', validators=[validators.required("KICK IS NO GOOD! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Extra Point/PAT' field.")])
    #Defense
    sack = FloatField('Sacks:', validators=[validators.required\
    ("FLAG! ROUGHING THE PASSER! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Sacks' field.")])
    def_int = FloatField\
    ('Interceptions:', validators=[validators.required("PASS INTERFERENCE! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Interceptions' field.")])
    fr = FloatField('Fumbles Recovered:', validators=[validators.required\
    ("OFFENSE RECOVERED! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Fumbles Recovered' field.")])
    def_td = FloatField('Defensive Touchdowns:', validators=[validators.required\
    ("INFRACTION! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Defensive Touchdowns' field.")])
    spc_td = FloatField('Special Team Touchdowns:', validators=[validators.required\
    ("MUFFED PUNT! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Special Teams Touchdowns' field.")])
    sfty = FloatField('Safeties:', validators=[validators.required\
    ("QB SCRAMBLE! Only whole or decimal/fractional numbers (Ex: 1, 0.5, 0.25, etc..) only for 'Safties' field.")])
    submit = SubmitField("Submit")

