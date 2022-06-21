# ROUTING PAGE FOR THE DATA INPUT TAB, ONLY ACCESSIBLE FOR SALES REP, BASED ON TARGET CRITERIA SET BY MANAGER
# DATA INPUT CAN BE IN THE FORM OF FILE OR MANUAL RECORD ENTRY

#IMPORTING THE REQUIRED LIBRARIES
import os
import datetime
import random
import pandas as pd
from Mendel import db,app
from flask_login import current_user    
from sqlalchemy import text,create_engine
from werkzeug.utils import secure_filename
from flask import render_template, request, flash, redirect, url_for,jsonify, Blueprint,send_file
from Mendel.models import User,Account,Account_Var, Potential_Volume,Segment_Rank,Market_Share_Cat,Drivers_Rank,Drivers_Definition






#CREATING THE BLUE PRINT VARIABLE FOR THE DATAINPUT FOR ROUNTING 
datainput = Blueprint('datainput', __name__)





#VALIDATION FOR ALLOWING ONLY txt and csv FILES
ALLOWED_EXTENSIONS = set(['txt','csv'])
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
		   




#SQLALCHEMY ENGINE TO ACCESS THE DATABASE
sql_engine = create_engine('sqlite:///Mendel//site.db', echo=False)






#ROUTE FOR DATA INPUT TAB HTML TAB,ALSO FORM RENDERING MANUAL INPUT SAVE FUNCTIONALITY     
@datainput.route("/datainputurl", methods=['GET', 'POST'])
def datainputurl():
    #user authentication
    if current_user.is_authenticated==False:
        flash('User not logged in', 'info')
        return redirect(url_for('main.login'))
    
    #GET request 
    #retrieving the already loaded accounts
    account_variables = Account_Var.query.all()
    accounts=db.session.query(Account).from_statement(text("SELECT * FROM account where user_id="+str(current_user.id))).all()
    drivers_definitions=db.session.query(Drivers_Definition).from_statement(text("SELECT * FROM drivers_definition where user_id="+str(current_user.manager_id))).all()
    
    terr_target=3200
    tar=0
    for account in accounts:
        account_vars=db.session.query(Account_Var).from_statement(text("SELECT * FROM account_var where npi_id="+str(account.id))).all()
        for account_var in account_vars:
            tar=tar+account_var.Target_Sales
    
    #POST request for manual input form saving functionalty    
    if request.method == 'POST':
        
       #retrieving the data from UI 
       NPI_ID = request.form.get('NPI_ID') 
       Health_Groups = request.form.get('Health_Groups')
       Account_ID = request.form.get('Account_ID')
       Account_Name = request.form.get('Account_Name')
       TargetingCriteria1 = request.form.get('TargetingCriteria1',default=None, type=str)
       TargetingCriteria2 = request.form.get('TargetingCriteria2',default=None, type=str)
       TargetingCriteria3 = request.form.get('TargetingCriteria3',default=None, type=str)
       TargetingCriteria4 = request.form.get('TargetingCriteria4',default=None, type=str)
       TargetingCriteria5 = request.form.get('TargetingCriteria5',default=None, type=str)
       TargetingCriteria6 = request.form.get('TargetingCriteria6',default=None, type=str)
       TargetingCriteria7 = request.form.get('TargetingCriteria7',default=None, type=str)
       TargetingCriteria8 = request.form.get('TargetingCriteria8',default=None, type=str)
       TargetingCriteria9 = request.form.get('TargetingCriteria9',default=None, type=str)
       TargetingCriteria10 = request.form.get('TargetingCriteria10',default=None, type=str)
       TargetingCriteria11 = request.form.get('TargetingCriteria11',default=None, type=str)
       TargetingCriteria12 = request.form.get('TargetingCriteria12',default=None, type=str)
       
       Potential_Value = request.form.get('Potential_Value')
       Selling_Drug = request.form.get('Selling_Drug')
       Competitor_Drug = request.form.get('Competitor_Drug')
       Actual_Sales = request.form.get('Actual_Sales')
       Target_Sales = request.form.get('Target_Sales')
       Prob_Score = request.form.get('Prob_Score',default=None, type=float)
       Segments = request.form.get('Segments')
       
       #retrieve the account if exist, otherwise insert new record to database
       if Account.query.filter_by(NPI_ID=NPI_ID).first():
           flash('NPI id already exist!', 'info')
       else:    
           account = Account(NPI_ID=NPI_ID,Health_Groups=Health_Groups, Account_ID=Account_ID, Account_Name=Account_Name, author=current_user)
           db.session.add(account)
           db.session.commit()    
       
       #loading the record in the account var table 
       account_exist=Account.query.filter_by(NPI_ID=NPI_ID).first()
       account_var=Account_Var(NBA_insights=Segments,TargetingCriteria1=TargetingCriteria1,TargetingCriteria2=TargetingCriteria2,TargetingCriteria3=TargetingCriteria3,TargetingCriteria4=TargetingCriteria4,TargetingCriteria5=TargetingCriteria5,TargetingCriteria6=TargetingCriteria6,TargetingCriteria7=TargetingCriteria7,TargetingCriteria8=TargetingCriteria8,TargetingCriteria9=TargetingCriteria9,TargetingCriteria10=TargetingCriteria10,TargetingCriteria11=TargetingCriteria11,TargetingCriteria12=TargetingCriteria12,Potential_Value=Potential_Value,Selling_Drug=Selling_Drug,Competitor_Drug=Competitor_Drug,Actual_Sales=Actual_Sales,Target_Sales=Target_Sales,Prob_Score=Prob_Score,acc=account_exist)
       db.session.add(account_var)
       db.session.commit() 
       
       #displaying the success message to UI
       flash('Record Added Successfully!', 'success')    
       return redirect(url_for('datainput.datainputurl')) 
    
    #sending the loaded account data to UI as GET request
    return render_template('datainput.html',title='Data Input',accounts=accounts,drivers_definitions=drivers_definitions,account_vars=account_variables,territory_quota=terr_target,target_sale=tar,territory_quota_att=round(tar/terr_target,2))







#MANUAL INPUT CALCULATED FIELDS VALUE CALCULATION FUNCTIONALITY
@datainput.route('/background_process')
def background_process():
    try:
        #retrieving the data from UI
        TargetingCriteria =[None,None,None,None,None,None,None,None,None,None,None,None]
        TargetingCriteria[0] = request.args.get('TargetingCriteria1',default=None, type=str)
        TargetingCriteria[1] = request.args.get('TargetingCriteria2',default=None, type=str)
        TargetingCriteria[2] = request.args.get('TargetingCriteria3',default=None, type=str)
        TargetingCriteria[3] = request.args.get('TargetingCriteria4',default=None, type=str)
        TargetingCriteria[4] = request.args.get('TargetingCriteria5',default=None, type=str)
        TargetingCriteria[5] = request.args.get('TargetingCriteria6',default=None, type=str)
        TargetingCriteria[6] = request.args.get('TargetingCriteria7',default=None, type=str)
        TargetingCriteria[7] = request.args.get('TargetingCriteria8',default=None, type=str)
        TargetingCriteria[8] = request.args.get('TargetingCriteria9',default=None, type=str)
        TargetingCriteria[9] = request.args.get('TargetingCriteria10',default=None, type=str)
        TargetingCriteria[10] = request.args.get('TargetingCriteria11',default=None, type=str)
        TargetingCriteria[11] = request.args.get('TargetingCriteria12',default=None, type=str)
        Potential_Value = request.args.get('Potential_Value', default=0, type=int)
        Selling_Drug = request.args.get('Selling_Drug', default=0, type=int)
        Competitor_Drug = request.args.get('Competitor_Drug', default=0, type=int)
        Actual_Sales = request.args.get('Actual_Sales', default=0, type=int)
        Target_Sales = request.args.get('Target_Sales', default=0, type=int)
        
        #loading the drivers definition and target criterias set by the manager for the sales rep
        drivers_definitions=db.session.query(Drivers_Definition).from_statement(text("SELECT * FROM drivers_definition where user_id="+str(current_user.manager_id))).all()
        drivers_rank=db.session.query(Drivers_Rank).from_statement(text("SELECT * FROM Drivers_Rank where user_id="+str(current_user.manager_id))).all()
        
        
        #calculating the probability score for the record
        Score=0
        MaxScore=0
        for i in range(0,len(TargetingCriteria)):
            if TargetingCriteria[i] is not None:
                MaxScore=MaxScore+(int(drivers_definitions[i].Weight))*(int(drivers_rank[0].Value))
                if TargetingCriteria[i]==drivers_definitions[i].Driver_1:
                    Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[0].Value))
                elif TargetingCriteria[i]==drivers_definitions[i].Driver_2:
                    Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[1].Value))
                elif TargetingCriteria[i]==drivers_definitions[i].Driver_3:
                    Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[2].Value))   
                elif TargetingCriteria[i]==drivers_definitions[i].Driver_4:
                    Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[3].Value))
                elif TargetingCriteria[i]==drivers_definitions[i].Driver_5:
                    Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[4].Value))
                elif TargetingCriteria[i]==drivers_definitions[i].Driver_6:
                    Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[5].Value))
                elif TargetingCriteria[i]==drivers_definitions[i].Driver_7:
                    Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[6].Value))
         
        Prob_Score=round((Score/MaxScore)*100,1) 

        #calculating the competitive penetration
        Comp_Penitration=0
        if Potential_Value==0:
            Comp_Penitration=0
        elif Potential_Value>0:
            Comp_Penitration=(Competitor_Drug/Potential_Value)*100
        
        #calculating the market share
        M_Share=0
        if Competitor_Drug==0:
            M_Share=0
        elif Competitor_Drug>0:
            M_Share=(Selling_Drug/Competitor_Drug)*100
            
        #calculate the overall percentage actual and potential sale, at the rep level    
        Per_Actual_Sales=0
        accounts=db.session.query(Account).from_statement(text("SELECT * FROM account where user_id="+str(current_user.id))).all()
        
        act=Actual_Sales
        pot=Potential_Value
        for account in accounts:
            account_vars=db.session.query(Account_Var).from_statement(text("SELECT * FROM account_var where npi_id="+str(account.id))).all()
            for account_var in account_vars:
                act=act+account_var.Actual_Sales
                pot=pot+account_var.Potential_Value
        
        Per_Actual_Sales=(Actual_Sales/act)*100
        Per_Potential_Sales=(Potential_Value/pot)*100
        
        Segment=['A','B','C','D']
        call_segment=Segment[random.randrange(0,3)]
       
        #send all the calculations back to UI for display
        return jsonify(Prob_Score=round(Prob_Score,2),Competitive_Penitration=round(Comp_Penitration,2),Market_Share=round(M_Share,2),Percentage_Actual_Sales=round(Per_Actual_Sales,2),Percentage_Potential_Sales=round(Per_Potential_Sales,2),call_segment=call_segment)
    except Exception as e:
        return str(e)







#ROUTE FOR DATA INPUT TAB, FILE IMPORT FUNCTIONALITY
@datainput.route("/datainputfile",methods=['GET','POST'])
def datainputfile():
        #user authentication
        if current_user.is_authenticated==False:
            flash('User not logged in', 'info')
            return redirect(url_for('main.login'))
        
        if request.method == 'POST':
            
            #file import Validations
            if 'file' not in request.files:
               flash('No file Part!', 'danger')
               return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
               flash('No selected file', 'danger')
               return redirect(request.url)
            if file and allowed_file(file.filename):
               
               #if the file passes the validation 
               #reading the file name
               filename = secure_filename(file.filename)
               
               #loading the file in the local temporarily
               file.save(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename))
               
               #reading the file as data frame
               data=pd.read_csv(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename))
               num_rows=len(data.index)
               
               #retrieving the driver definition and driver rank set by the Manager for the logged in Sales Rep 
               drivers_definitions=db.session.query(Drivers_Definition).from_statement(text("SELECT * FROM drivers_definition where user_id="+str(current_user.manager_id))).all()
               drivers_rank=db.session.query(Drivers_Rank).from_statement(text("SELECT * FROM Drivers_Rank where user_id="+str(current_user.manager_id))).all()
                   
               #looping each record and checking if the account exist or not, if not exist then loading to database
               for index, row in data.iterrows():
                   if Account.query.filter_by(NPI_ID=str(row.iloc[0]).strip()).first():
                       #record already exists
                       num_rows=num_rows-1
                   else:    
                       account = Account(NPI_ID=str(row.iloc[0]).strip(),Health_Groups=row.iloc[1], Account_ID=row.iloc[2], Account_Name=row.iloc[3], author=current_user)
                       db.session.add(account)
                       db.session.commit()
                   account_exist=Account.query.filter_by(NPI_ID=str(row.iloc[0]).strip()).first()
                   
                   #looping for the levels set in the driver definition 
                   TargetingCriteria =[None,None,None,None,None,None,None,None,None,None,None,None]
                   for i in range(0,len(drivers_definitions)):
                       TargetingCriteria[i]=row.iloc[i+4]

                   #retrieving other values
                   Potential_Value=row.iloc[16]
                   Selling_Drug=row.iloc[17]
                   Competitor_Drug=row.iloc[18]
                   Actual_Sales=row.iloc[19]
                   Target_Sales=row.iloc[20]
                   
                   #Calculating the Probabilty Score
                   Score=0
                   MaxScore=0
                   for i in range(0,len(TargetingCriteria)):
                       if TargetingCriteria[i] is not None:
                           MaxScore=MaxScore+(int(drivers_definitions[i].Weight))*(int(drivers_rank[0].Value))
                           if TargetingCriteria[i]==drivers_definitions[i].Driver_1:
                               Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[0].Value))
                           elif TargetingCriteria[i]==drivers_definitions[i].Driver_2:
                               Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[1].Value))
                           elif TargetingCriteria[i]==drivers_definitions[i].Driver_3:
                               Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[2].Value))   
                           elif TargetingCriteria[i]==drivers_definitions[i].Driver_4:
                               Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[3].Value))
                           elif TargetingCriteria[i]==drivers_definitions[i].Driver_5:
                               Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[4].Value))
                           elif TargetingCriteria[i]==drivers_definitions[i].Driver_6:
                               Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[5].Value))
                           elif TargetingCriteria[i]==drivers_definitions[i].Driver_7:
                               Score=Score+(int(drivers_definitions[i].Weight))*(int(drivers_rank[6].Value))
                    
                   Prob_Score=round((Score/MaxScore)*100,1) 
                   
                   Segment=['A','B','C','D']
                   call_segment=Segment[random.randrange(0,3)]
                   
                   #finally loading the record to the database
                   account_var=Account_Var(NBA_insights=call_segment,TargetingCriteria1=TargetingCriteria[0],TargetingCriteria2=TargetingCriteria[1],TargetingCriteria3=TargetingCriteria[2],TargetingCriteria4=TargetingCriteria[3],TargetingCriteria5=TargetingCriteria[4],TargetingCriteria6=TargetingCriteria[5],TargetingCriteria7=TargetingCriteria[6],TargetingCriteria8=TargetingCriteria[7],TargetingCriteria9=TargetingCriteria[8],TargetingCriteria10=TargetingCriteria[9],TargetingCriteria11=TargetingCriteria[10],TargetingCriteria12=TargetingCriteria[11],Potential_Value=Potential_Value,Selling_Drug=Selling_Drug,Competitor_Drug=Competitor_Drug,Actual_Sales=Actual_Sales,Target_Sales=Target_Sales,Prob_Score=Prob_Score,acc=account_exist)
                   db.session.add(account_var)
                   db.session.commit() 
                   
               #flashing the success message on the UI    
               flash(f'File Added Successfully! {num_rows} new accounts out of {len(data.index)} records', 'success')         
               return redirect(url_for('datainput.datainputurl')) 
        return redirect(url_for('datainput.datainputurl'))		   



    


#FUNCTIONALTY TO DOWNLOAD LOADED ACCOUNTS
@datainput.route('/datainputurl/download_datainput')
def download_datainput():
    #file name with current timestamp 
    now = datetime.datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    filename='account_input_'+current_time+".csv"
    
    #loading the data from the database to dataframe
    account_df=pd.read_sql("select * from account where user_id="+str(current_user.id),sql_engine)
    account_var_df=pd.read_sql("select * from account_var",sql_engine)
    account_df.rename(index=str, columns={"id": "acc_id"},inplace=True)
    
    #joining all the dataframes to single 
    merged_accounts = pd.merge(account_df, account_var_df, left_on='acc_id', right_on='npi_id')
    
    #saving the dataframe as csv file temporarily to local
    path=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
    merged_accounts.drop(['acc_id', 'user_id','id','npi_id'], axis=1,inplace=True)
    merged_accounts.to_csv(path,index=False)
    
    #sending the download path to UI      
    return send_file(path, as_attachment=True)		



#FUNCTIONALTY TO DOWNLOAD LOADED ACCOUNTS
@datainput.route('/datainputurl/download_template')
def download_template():

    filename='DATA_INPUT_TEMPLATE.xlsx'

    
    #saving the dataframe as csv file temporarily to local
    path=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
    
    #sending the download path to UI      
    return send_file(path, as_attachment=True)	