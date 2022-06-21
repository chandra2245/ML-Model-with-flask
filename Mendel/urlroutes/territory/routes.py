# ROUTING PAGE FOR THE TERRITORY ANALYSIS TAB, MANAGER IS REQUIRED SELECT A SALES REP TO VIEW KPIS
# SALES REP IS REQUIRED ONLY TO SELECT DATE FILTER FROM DROP DOWN

#IMPORTING THE REQUIRED LIBRARIES
import math
import datetime
import pandas as pd
from Mendel import db
from sqlalchemy import text
from Mendel.models import User
from flask_login import  current_user    
from flask import render_template, request, flash, redirect, url_for,jsonify, Blueprint
import Mendel.mlmodel.hcp_clustering_segmentation as clt
import Mendel.mlmodel.hcp_propensity_modeling as mdl



#CREATING THE BLUE PRINT VARIABLE FOR THE TERRITORY FOR ROUNTING 
territory = Blueprint('territory', __name__)






#LOADING THE REQUIRED FILES FOR SHOWING THE ANALYSIS
#FOR NOW ML MODEL IS NOT INTEGRATED THEREFORE KPIS SHOWN FROM FILES 
Account_data = pd.read_csv("Mendel/static/data/Account_data.csv")
rescale_clus_analysis = pd.DataFrame(clt.rescale_clus_analysis)
mendel_cluster_analysis =  pd.DataFrame(clt.mendel_cluster_analysis)
master_km = pd.read_csv("Mendel/static/data/master_km.csv")
timeseries = pd.read_csv("Mendel/static/data/timeseries.csv")

propensity_p=pd.DataFrame(mdl.propensity)
propensity = propensity_p.merge(master_km[['account_name','cluster_id']],on='account_name')

Calls_Data = pd.read_csv("Mendel/static/data/Calls_Data.csv")


Calls_Data['DATA_DATE'] =  pd.to_datetime(Calls_Data['DATA_DATE'], format='%m/%d/%Y')
Calls_Data['count_column']=1



rescale_clus_analysis['cluster_id']=rescale_clus_analysis['cluster_id'].astype(str)
rescale_clus_analysis['cluster_id'].replace('0','A',inplace=True)
rescale_clus_analysis['cluster_id'].replace('1','B',inplace=True)
rescale_clus_analysis['cluster_id'].replace('2','C',inplace=True)
rescale_clus_analysis['cluster_id'].replace('3','D',inplace=True)




mendel_cluster_analysis['cluster_id']=mendel_cluster_analysis['cluster_id'].astype(str)
mendel_cluster_analysis['cluster_id'].replace('0','A',inplace=True)
mendel_cluster_analysis['cluster_id'].replace('1','B',inplace=True)
mendel_cluster_analysis['cluster_id'].replace('2','C',inplace=True)
mendel_cluster_analysis['cluster_id'].replace('3','D',inplace=True)



propensity['cluster_id']=propensity['cluster_id'].astype(str)
propensity['cluster_id'].replace('0','A',inplace=True)
propensity['cluster_id'].replace('1','B',inplace=True)
propensity['cluster_id'].replace('2','C',inplace=True)
propensity['cluster_id'].replace('3','D',inplace=True)


master_km['cluster_id']=master_km['cluster_id'].astype(str)
master_km['cluster_id'].replace('0','A',inplace=True)
master_km['cluster_id'].replace('1','B',inplace=True)
master_km['cluster_id'].replace('2','C',inplace=True)
master_km['cluster_id'].replace('3','D',inplace=True)

Account_data['division']=pd.cut(Account_data['Total Potential Value'],5,labels=[5,4,3,2,1])
Data = Account_data.sort_values('Total Potential Value', ascending=False).reset_index()






#ROUTE FOR TERRITORY ANALYSIS PAGE
@territory.route("/territoryanalysis")
def territoryanalysis():
    #user authentication
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
    
    #sending the details to 'accountanalysis.html' template    
    return render_template('territoryanalysis.html',title='Territory Analysis',reps=replist)






#FUNCTIONALTY TO FILTER DATAFRAME WITH SELECTED SALES REP
@territory.route("/territoryanalysis_filter", methods=['GET', 'POST'])
def territoryanalysis_filter():
    try:
        #filtering the calls data
        global Filtered_calls
        #if the user type is manager then manager need to select a reporting rep
        if(current_user.user_type=='admin'):
            Rep_Names = request.args.get('Rep_Names', default="", type=str)
            if(Rep_Names=='All'):
                Filtered_calls = Calls_Data
            else:
                repemail=None
                reps=db.session.query(User).from_statement(text("SELECT * FROM user where manager_id="+str(current_user.id))).all()
                for rep in reps:
                    if(rep.username==Rep_Names):
                        repemail=rep.email
                        break
                Filtered_calls = Calls_Data[Calls_Data['REP_EMPLOYEE_EMAIL_ADDRESS']==repemail]                

        #if the user type is sales rep
        else:
            Filtered_calls = Calls_Data[Calls_Data['REP_EMPLOYEE_EMAIL_ADDRESS']==current_user.email]
            
        
        
        #parsing date column and creating it as index
        Filtered_calls['date_minus_time'] = Filtered_calls["DATA_DATE"].apply( lambda Filtered_calls : datetime.datetime(year=Filtered_calls.year, month=Filtered_calls.month, day=Filtered_calls.day))
        Filtered_calls.set_index(Filtered_calls["date_minus_time"],inplace=True)
        

        
        #date filters are currently not applied        
        Initial_date = request.args.get('Initial_date', default="", type=str)
        Final_date = request.args.get('Final_date', default="", type=str)
        options = request.args.get('options', default="", type=str)
        #dt = parse(Initial_date)


        #creating a global variables with filtered data        
        global Filtered_data
        Filtered_data = Account_data
        Score=int(math.ceil(len(Data.index)*3/4))
        global Pareto_Data
        Pareto_Data=Data.head(Score)
        
        #data type convertion for UI rendering        
        actual_sales=propensity['actual_sales'].mean()
        potential_value=propensity['total_potential_value'].mean()
        market_share=propensity['market_share_in_account'].mean()
        injection_potential=propensity['injection_potential'].mean()
        pal=propensity['pal'].mean()
        
        #sending the variables to UI        
        return jsonify(actual_sales=round(actual_sales,2),potential_value=round(potential_value,2),market_share=round(market_share,2),injection_potential=round(injection_potential,2),pal=round(pal,2))
    
    except Exception as e:
        return str(e)   







#TERRITORY ANALYSIS, PIE CHART DATA CREATION FUNCTIONALITY
@territory.route('/get_piechart_data_v2')
def get_piechart_data_v2():
    
    #data type conversion and computation variables creation
    df=master_km.groupby('cluster_id',as_index=False).size()
    Tot=Filtered_data['Account Name'].count()
    Group= Filtered_data[['Segment','Account Name']].groupby('Segment',as_index=False).count() 
    Group['Account Name']=Group[['Account Name']].apply(lambda x: (x/Tot)*100)
    Segments=['A','B','C','D']

    #Creating the json object with the data for 'd3.js' functions    
    pieChartData = []
    Segments
    i=0

    #json insertion segment wise 
    while(i<len(Segments)):    
        eachData = {}
        eachData['category'] = Segments[i]
        eachData['measure'] =  round(int(df.loc[df['cluster_id']==Segments[i],'size']))
        pieChartData.append(eachData)
        i=i+1  

    #sending the json object  
    return jsonify(pieChartData)







#TERRITORY ANALYSIS, BAR CHART DATA CREATION FUNCTIONALITY
@territory.route('/get_barchart_data_v2')
def get_barchart_data_v2():
    
    #data type conversion and computation variables creation
    df=master_km[['actual_sales', 'total_potential_value','market_share_in_account', 'injection_potential', 'pal',]].mean()
    Segments=['A','B','C','D','E']    
    Account_Relationship=['Actual Sales','Total Potential Value','Market Share','Injection Potential','Value Perception']    


    #Creating the json object with the data for 'd3.js' functions
    barChartData=[]

    #looping through the dataframe and loading the data to json
    for i in range(0,len(Account_Relationship)):
        eachData = {}
        #json insertion for overall
        eachData['group'] = 'All'
        eachData['category'] = Account_Relationship[i]
        eachData['measure'] =  round(4,2)
        eachData['value'] =  round(df[i],2)
        barChartData.append(eachData)
        
        
    #json insertion segment wise     
    for j in Segments:
        for x in range(0,len(Account_Relationship) ):
            if rescale_clus_analysis.loc[rescale_clus_analysis['cluster_id']==j,'cluster_id'].empty:
                eachData = {}
                eachData['group'] = j
                eachData['category'] = Account_Relationship[x]
                eachData['measure'] =  0.0
                eachData['value'] =  0.0
                barChartData.append(eachData)
            else:
                eachData = {}
                eachData['group'] = j
                eachData['category'] = Account_Relationship[x]
                temp=rescale_clus_analysis.loc[rescale_clus_analysis['cluster_id']==j,]
                eachData['measure'] =  round(float(temp.iloc[:,x+1]),2)
                temp2=mendel_cluster_analysis.loc[mendel_cluster_analysis['cluster_id']==j,]
                eachData['value'] =  round(float(temp2.iloc[:,x+1]),2)
                barChartData.append(eachData)
    
    #sending the json object    
    return jsonify(barChartData)







#PARETO CHART FITLER TO SELECT ALL ACCOUNT, TOP 75%, TOP 50% AND  25%
@territory.route('/Pareto_Division')
def Pareto_Division():
    try:
        #retrieve the user input for the pareto filter
        Pareto_Filter = request.args.get('Filter', default="All", type=str)
        
        #filtering the data according to selected filter
        Score=0.0
        if Pareto_Filter=='All':
            Score=int(math.ceil(len(Data.index)*90/100))
        elif Pareto_Filter=='75':
            Score=int(math.ceil(len(Data.index)*3/4))
        elif Pareto_Filter=='50':
            Score=int(math.ceil(len(Data.index)*1/2))
        elif Pareto_Filter=='25':
            Score=int(math.ceil(len(Data.index)*1/4))

        
        #creating the global dataframe for the filtered data
        global Pareto_Data
        Pareto_Data=Data.head(Score)
        return jsonify(Pareto_Filter=23)
    except Exception as e:
        return str(e)






#FUNCTIONALTY TO SEND FILTERED ACCOUNT SALES DATA  TO  D3.JS FUNCTION TO CREATE PARETO CHART 
@territory.route('/get_pareto_data')
def get_pareto_data():
    
    #create json object with the filtered data
    ParetoChartData = []
    i=0
    while i<len(Pareto_Data.index):
        eachData = {}
        eachData['Category'] = Pareto_Data.loc[i,'Account Name']
        eachData['Amount'] =  int(Pareto_Data.loc[i,'Total Potential Value'])
        eachData['Color'] = str(Pareto_Data.loc[i,'Segment'])
        ParetoChartData.append(eachData)
        i=i+1
    
    #sending the data to the d3.js pareto chart
    return jsonify(ParetoChartData)








#FUNCTIONALTY TO SEND TIME SERIES CALLS DATA TO CREATE CALLS LINE CHART
@territory.route('/get_timeseries_calls_data')
def get_timeseries_calls_data():
    
    #weekly aggregate calls
    TS=Filtered_calls[['count_column']].resample('W').sum()
    
    
    #json object with time series sales data
    TSData=[]
    date = TS.index.min()

    while (date<=TS.index.max()):
        eachData = {}
        eachData['date'] = date.strftime("%d-%b-%y")
        eachData['calls'] = int(TS.loc[date,'count_column'])
        TSData.append(eachData)
        date += datetime.timedelta(days=7)
    


    #sending the json object to line chart d3.js
    return jsonify(TSData)    



#FUNCTIONALTY TO SEND TIME SERIES CALLS DATA TO CREATE CALLS LINE CHART
@territory.route('/get_timeseries_callcat_data')
def get_timeseries_callcat_data():
    DF=pd.get_dummies(Filtered_calls['PLANNED_UNPLANNED'])
    DF2=pd.get_dummies(Filtered_calls['Decile'])
    DF3=pd.get_dummies(Filtered_calls['CALL_TYPE_DESCRIPTION'])

    #weekly aggregate calls
    TS=DF.resample('W').sum()
    TS2=DF2.resample('W').sum()
    TS3=DF3.resample('W').sum()
    
    L1=Filtered_calls['PLANNED_UNPLANNED'].unique()
    L2=Filtered_calls['Decile'].unique()
    L3=Filtered_calls['CALL_TYPE_DESCRIPTION'].unique()
    #json object with time series sales data
    TSData=[]
    date = TS.index.min()

    while (date<=TS.index.max()):
        eachData = {}
        eachData['date'] = date.strftime("%d-%b-%y")
        for cat in L1:
            eachData[str(cat)] = int(TS.loc[date,str(cat)])
        for cat in L2:
            eachData[str(cat)] = int(TS2.loc[date,str(cat)])
        for cat in L3:
            eachData[str(cat)] = int(TS3.loc[date,str(cat)])

        
        
        TSData.append(eachData)
        date += datetime.timedelta(days=7)
    

    #sending the json object to line chart d3.js
    return jsonify(TSData)   




#FUNCTIONALTY TO CREATE CALLS SEMESTER TO DATE BAR GRAPH
@territory.route('/get_bar_decile_data')
def get_bar_decile_data():
    
    DecileData=[]
   
    #creating group for decile
    DF=Filtered_calls[['Decile','count_column']].groupby('Decile',as_index=False).sum()
    for index,row in DF.iterrows():
        eachData = {}
        eachData['group']= 'Decile'
        eachData['type'] = str(row['Decile']) 
        eachData['value'] =  int(row['count_column']) 
        DecileData.append(eachData)

    #creating group for branded-unbranded
    DF2=Filtered_calls[['PLANNED_UNPLANNED','count_column']].groupby('PLANNED_UNPLANNED',as_index=False).sum()
    for index,row in DF2.iterrows():
        eachData = {}
        eachData['group']= 'PLANNED_UNPLANNED'
        eachData['type'] = str(row['PLANNED_UNPLANNED']) 
        eachData['value'] =  int(row['count_column'])
        DecileData.append(eachData)
    
    
    #creating group for call type
    DF3=Filtered_calls[['CALL_TYPE_DESCRIPTION','count_column']].groupby('CALL_TYPE_DESCRIPTION',as_index=False).sum()
    for index,row in DF3.iterrows():
        eachData = {}
        print(str(row['CALL_TYPE_DESCRIPTION']).replace("Call", ""))
        eachData['group']= 'CALL_TYPE_DESCRIPTION'
        eachData['type'] = str(row['CALL_TYPE_DESCRIPTION']).replace("Call", "") 
        eachData['value'] =  int(row['count_column'])
        DecileData.append(eachData)


    


    return jsonify(DecileData) 