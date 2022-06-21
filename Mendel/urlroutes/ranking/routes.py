#TARGET RANKING PAGE DISPLAYS THE SCATTER PLOT OF CLUSTER ANALYSIS OF THE ACCOUNTS UNDER A SALES REPRESENTATIVE 


#IMPORT ALL THE REQUIRED LIBRARIES
import pandas as pd
from Mendel import db
from sqlalchemy import text
from Mendel.models import User
from flask_login import  current_user    
from flask import render_template,  flash, redirect, url_for,jsonify, Blueprint
import Mendel.mlmodel.hcp_clustering_segmentation as clt
import Mendel.mlmodel.hcp_propensity_modeling as mdl



#CREATING THE BLUE PRINT VARIABLE FOR THE RANKING FOR ROUNTING 
ranking = Blueprint('ranking', __name__)





#READING THE REQUIRED FILES, CURRENTLY THE INTERGRATION IS NOT COMPLETE THEREFORE DISPLAYING THE KPIS USING FILES

master_km = pd.DataFrame(clt.master_km)
propensity_p=pd.DataFrame(mdl.propensity)
propensity = propensity_p.merge(master_km[['account_name','cluster_id']],on='account_name')


#propensity = pd.read_csv("Mendel/static/data/propensity.csv")
propensity['cluster_id']=propensity['cluster_id'].astype(str)
propensity['cluster_id'].replace('0','A',inplace=True)
propensity['cluster_id'].replace('1','B',inplace=True)
propensity['cluster_id'].replace('2','C',inplace=True)
propensity['cluster_id'].replace('3','D',inplace=True)






#ROUTE FOR TARGET RANKING HTML
@ranking.route("/targetranking")
def targetranking():
    #user authentication
    if current_user.is_authenticated==False:
        flash('User not logged in', 'info')
        return redirect(url_for('main.login'))
    
    #if the logged in user is manager, then loading the list of mapped sales reps
    replist=[]
    if(current_user.user_type=='admin'):
        reps=db.session.query(User).from_statement(text("SELECT * FROM user where manager_id="+str(current_user.id))).all()
        for rep in reps:
            replist.append(rep.username)
    
    #loading the html template as GET request 
    return render_template('targetranking.html',title='Target Ranking',reps=replist)




#ROUTE FOR CREATING JSON DATA FOR THE SCATTER PLOT
@ranking.route("/scatterplot_data")
def scatterplot_data():
    #multiline comment for scatterplot data using database
    '''
    accounts=db.session.query(Account).from_statement(text("SELECT * FROM account where user_id="+str(current_user.id))).all()
    jsonData = []
    for account in accounts:
        potvalue=0
        counter=0
        prob_score=0
        selling_drug=0
        competitor_drug=0
        account_vars=db.session.query(Account_Var).from_statement(text("SELECT * FROM account_var where npi_id="+str(account.id))).all()
        for account_var in account_vars:
            counter=counter+1
           potvalue=potvalue+account_var.Potential_Value
            prob_score=prob_score+account_var.Prob_Score
            selling_drug=selling_drug+account_var.Selling_Drug
            competitor_drug=competitor_drug+account_var.Competitor_Drug
        pscore=prob_score/counter
        m_share=(selling_drug/competitor_drug)*100    
        eachData = {}
        eachData['group'] = 'Account'
        eachData['name'] = account.Account_Name
        eachData['Probability_Score'] =  pscore
        eachData['Potential_Value'] = potvalue
        eachData['Market_Share'] = m_share
        jsonData.append(eachData)
    '''
    
    #converting data frame to json
    jsonData = []
    
    #loading dataframe line by line to dataframe
    for index,row in propensity.iterrows():
        if row['patients_treated_with_competitive_drug']>0:
            m_share=((row['patients_treated_with_selling_drug']/row['patients_treated_with_competitive_drug'])*100)
        else:
            m_share=100
        eachData = {}
        eachData['group'] = 'Account'
        eachData['name'] = row['account_name']
        eachData['Probability_Score'] =  round(m_share,2)
        eachData['Potential_Value'] = row['total_potential_value']
        eachData['Market_Share'] = round(m_share,2)
        eachData['Segment'] = 'Segment '+row['cluster_id']
        jsonData.append(eachData)
    
    #sending the data to the scatter plot d3.js
    return jsonify(jsonData)   



		