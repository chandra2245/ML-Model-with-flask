# ROUTING PAGE FOR THE ACCOUNT ANALYSIS TAB, MANAGER IS REQUIRED SELECT A SALES REP AND ACCOUNTS UNDER LATTER TO VIEW KPIS
# SALES REP IS REQUIRED ONLY TO SELECT THE ACCOUNTS FROM DROP DOWN

#IMPORTING THE REQUIRED LIBRARIES
import math
import pandas as pd
from Mendel import db
from sqlalchemy import text
from Mendel.models import User
from flask_login import  current_user    
from flask import render_template, request, flash, redirect, url_for,jsonify, Blueprint
import Mendel.mlmodel.hcp_clustering_segmentation as clt
import Mendel.mlmodel.hcp_propensity_modeling as mdl





#CREATING THE BLUE PRINT VARIABLE FOR THE ACCOUNT FOR ROUNTING 
account = Blueprint('account', __name__)





#LOADING THE REQUIRED FILES FOR SHOWING THE ANALYSIS
#FOR NOW ML MODEL IS NOT INTEGRATED THEREFORE KPIS SHOWN FROM FILES 
timeseries = pd.read_csv("Mendel/static/data/timeseries.csv")
propensity_scaled = pd.DataFrame(mdl.propensity_rescale)
master_km = pd.DataFrame(clt.master_km)


propensity_p=pd.DataFrame(mdl.propensity)
propensity = propensity_p.merge(master_km[['account_name','cluster_id']],on='account_name')
#propensity = pd.read_csv("Mendel/static/data/propensity.csv")

propensity['cluster_id']=propensity['cluster_id'].astype(str)
propensity['cluster_id'].replace('0','A',inplace=True)
propensity['cluster_id'].replace('1','B',inplace=True)
propensity['cluster_id'].replace('2','C',inplace=True)
propensity['cluster_id'].replace('3','D',inplace=True)






#ROUTE FOR ACCOUNT ANALYSIS TAB
@account.route("/accountanalysis")
def accountanalysis():
    #user authetication
    if current_user.is_authenticated==False:
        flash('User not logged in', 'info')
        return redirect(url_for('main.login'))
    
    #if the logged in user is a sales rep then a dropdown of mapped sales reps is also displayed
    #retrieving reps mapped to manager
    replist=[]
    if(current_user.user_type=='admin'):
        reps=db.session.query(User).from_statement(text("SELECT * FROM user where manager_id="+str(current_user.id))).all()
        for rep in reps:
            replist.append(rep.username)
    
    #retrieving account names from file
    accounts=propensity['account_name']
    
    #sending the details to 'accountanalysis.html' template
    return render_template('accountanalysis.html',accounts=accounts,title='Account Analysis',reps=replist)







#FUNCTIONALTY TO FILTER DATAFRAME WITH SELECTED ACCOUNTS AND USER
@account.route("/accountanalysis_filter", methods=['GET', 'POST'])
def accountanalysis_filter():
    try:
        #date filters are currently not applied
        Initial_date = request.args.get('Initial_date', default="", type=str)
        Final_date = request.args.get('Final_date', default="", type=str)
        #dt = parse(Initial_date)
        
        #retrieving the selected account name
        Account_Names = request.args.get('Account_Names', default="", type=str)
        
        
        #creating a global variables with filtered data
        global Filtered_account
        global Scaled_account
        Filtered_account = propensity[propensity['account_name']==Account_Names]
        Scaled_account = propensity_scaled[propensity_scaled['account_name']==Account_Names]
        
        #data type convertion for UI rendering
        account_relation=float(Filtered_account['account_relation'])
        injection_potential=float(Filtered_account['injection_potential'])
        pal=float(Filtered_account['pal'])
        competitive_situation=float(Filtered_account['competitive_situation'])
        clinical_mindset=float(Filtered_account['clinical_mindset'])
        value_perception=float(Filtered_account['value_perception'])
        segment=(str(Filtered_account['cluster_id'])).split()
        
        #color codes for the heat map generation
        colors=['#cc0000','#ff3333','#ff8080','#d9f2e4','#9fdfbc','#66cc94','#40bf79','#39ac6d','#2d8655','#20603d']
        
        #variables with color codes for UI rendering        
        account_relation_c=colors[math.floor(float(Scaled_account['account_relation']))-1]
        injection_potential_c=colors[math.floor(float(Scaled_account['injection_potential']))-1]
        pal_c=colors[math.floor(float(Scaled_account['pal']))-1]
        competitive_situation_c=colors[math.floor(float(Scaled_account['competitive_situation']))-1]
        clinical_mindset_c=colors[math.floor(float(Scaled_account['clinical_mindset']))-1]
        value_perception_c=colors[math.floor(float(Scaled_account['value_perception']))-1]
        
        #sending the variables to UI
        return jsonify(account_relation=round(account_relation,2),injection_potential=round(injection_potential,2),pal=round(pal,2),competitive_situation=round(competitive_situation,2),clinical_mindset=round(clinical_mindset,2),value_perception=round(value_perception,2),account_relation_c=account_relation_c,injection_potential_c=injection_potential_c,pal_c=pal_c,competitive_situation_c=competitive_situation_c,clinical_mindset_c=clinical_mindset_c,value_perception_c=value_perception_c,segment=segment[1])
    except Exception as e:
        return str(e)   







    
#FUNCTIONALTY TO SEND SALES COMPARISON DATA TO  D3.JS FUNCTION TO CREATE RADIAL BAR CHART 
@account.route('/get_h_barchart_data')
def get_h_barchart_data():
    
    #data type conversion and computation variables creation
    actual_sales=int(Filtered_account['actual_sales'])
    target_sales=int(Filtered_account['target_sales'])
    patients_treated_with_selling_drug=int(Filtered_account['patients_treated_with_selling_drug'])
    patients_treated_with_competitive_drug=int(Filtered_account['patients_treated_with_competitive_drug'])
    act_color=None
    comp_color=None
    
    #competitor analysis score generation
    if patients_treated_with_competitive_drug>0:
            compdiv=patients_treated_with_selling_drug/patients_treated_with_competitive_drug
    else:
        compdiv=1

    #competitor analysis bar color coding
    if compdiv>0.2:
        comp_color='#ffff1a'
    else:
        comp_color='#ff471a'      
    
    #sales comparsion color coding
    if actual_sales<target_sales:
        act_color='#ff471a'
    else:
        act_color='#39ac6d'
    
    #Creating the json object with the data for 'd3.js' functions
    hbarData = []
    eachData = {}
    eachData['group'] = 'Sales'
    eachData['category'] = 'Target Sales'
    eachData['measure'] =  target_sales
    eachData['color'] = '#346DC3'
    hbarData.append(eachData)
    
    eachData = {}
    eachData['group'] = 'Sales'
    eachData['category'] = 'Actual Sales'
    eachData['measure'] =  actual_sales
    eachData['color'] = act_color
    hbarData.append(eachData)
    
    eachData = {}
    eachData['group'] = 'Comp_Analysis'
    eachData['category'] = 'Competitor'
    eachData['measure'] =  patients_treated_with_competitive_drug
    eachData['color'] = '#4d4dff'
    hbarData.append(eachData)
    
    eachData = {}
    eachData['group'] = 'Comp_Analysis'
    eachData['category'] = 'Own'
    eachData['measure'] =  patients_treated_with_selling_drug
    eachData['color'] = comp_color
    hbarData.append(eachData)
    
    #sending the json object
    return jsonify(hbarData)    






#FUNCTIONALTY TO SEND SALES MARKET SHARE DATA TO  D3.JS FUNCTION TO GAUGE CHART 
@account.route('/get_gauge_chart_data')
def get_gauge_chart_data():

    #data type conversion and computation variables creation
    patients_treated_with_selling_drug=int(Filtered_account['patients_treated_with_selling_drug'])
    patients_treated_with_competitive_drug=int(Filtered_account['patients_treated_with_competitive_drug'])
    
    #market share calculation
    if patients_treated_with_competitive_drug>0:
            compdiv=(patients_treated_with_selling_drug/patients_treated_with_competitive_drug)*100
    else:
        compdiv=100

    #creating the json data 
    hbarData = []
    eachData = {}
    eachData['measure'] =  round(compdiv,1)
    hbarData.append(eachData)
  
    #sending the json data to gauge chart d3.js
    return jsonify(hbarData)   






#FUNCTIONALTY TO SEND TIME SERIES SALES DATA TO CREATE SALES LINE CHART
@account.route('/get_timeseries_data')
def get_timeseries_data():
    
    #json object with time series sales data
    hbarData=[]
    for index, row in timeseries.iterrows():
        eachData = {}
        eachData['date'] = row['date']
        eachData['actual_sales'] =  row['actual_sales']
        eachData['target_sales'] =  row['target_sales']
        hbarData.append(eachData)

    #sending the json object to line chart d3.js
    return jsonify(hbarData)    



    
