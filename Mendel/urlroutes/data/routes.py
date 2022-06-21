# ROUTING PAGE FOR THE MANGER LEVEL DATA TAB, MANAGER IS REQUIRED MAP SALES REP TO HIMSELF, LOAD SOME DATA FILES I.E.SALES, CALL DETAILS ETC
# VIEW THE DATA ENTERED BY EACH SALES REP, FUNCTIONALITY TO DOWNLOAD THE FILES

#IMPORTING THE REQUIRED LIBRARIES
import os
import datetime
import pandas as pd
from Mendel import db,app
from flask_login import  current_user
from sqlalchemy import text,create_engine 
from werkzeug.utils import secure_filename
from Mendel.models import User,Call,Call_Sample,Affiliation, Prescription   
from flask import render_template, request, flash, redirect, url_for, Blueprint,jsonify,send_file




#CREATING THE BLUE PRINT VARIABLE FOR THE DATA FOR ROUNTING 
data = Blueprint('data', __name__)





#VALIDATION FOR ALLOWING ONLY txt and csv FILES
ALLOWED_EXTENSIONS = set(['txt','csv'])
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





#SQLALCHEMY ENGINE TO ACCESS THE DATABASE
sql_engine = create_engine('sqlite:///Mendel//site.db', echo=False)




#ROUTE FOR DATA HTML TAB, VISIBLE TO MANAGER ONLY     
@data.route("/data", methods=['GET', 'POST'])
def dataurl():
    #User authentication
    if current_user.is_authenticated==False:
        flash('User not logged in', 'info')
        return redirect(url_for('main.login'))
    
    #Retrieve the sales reps mapped to logged in Manger from the database
    reps=db.session.query(User).from_statement(text("SELECT * FROM user where manager_id="+str(current_user.id))).all()
    replist=[]
    for rep in reps:
        replist.append(rep.username)
    
    #Retrieve the file type uploaded from UI
    filetype=request.args.get('name', default="", type=str)
    
    #Retrieve the list of columns in the upload file sent by the GET request
    columns=request.args.getlist('columns')
    
    #Sending the details to the data.html template
    return render_template('data.html',title='Data Tab',reps=replist,filename=filetype,columns=columns)





#FUNCTIONALY TO MAP A SALES REPRESENTAIVE TO THE LOGGED IN MANAGER
@data.route('/repmap', methods=['GET', 'POST'])
def repmap():
    if request.method == 'POST':
        
        #manager filled email from UI
        repemail = request.form.get('repemail',default=None, type=str)
        
        #rep details from the database
        user=User.query.filter_by(email=str(repemail).strip()).first()
        
        #updating the rep manager id with current logged in manager
        user.manager_id=current_user.id
        
        #commiting the database
        db.session.commit()
        db.session.close()
        
        #Flashing the success message
        flash(f'Sales Representative now mapped to you!!!', 'success')         
        
        #redirecting back to data tab
        return redirect(url_for('data.dataurl')) 
    return redirect(url_for('data.dataurl'))






#FILE UPLOAD FUNCTIONALTY IN THE DATA TAB 
@data.route("/fileupload",methods=['GET','POST'])
def fileupload():
        if request.method == 'POST':
            #retrieving the file type i.e. call, call_sample etc 
            filetype = request.form.get('filetype',default=None, type=str)
            
            #retrieving the type of delimiter i.e ',', '\t' etc
            delimiter = request.form.get('delimiter',default=None, type=str)

            #retrieving the date format
            dateformat = request.form.get('dateformat',default=None, type=str)

            
            #file import Validations
            if 'file' not in request.files:
               flash('No file Part!', 'danger')
               return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
               flash('No selected file', 'danger')
               return redirect(request.url)
            if file and allowed_file(file.filename):
               filename = secure_filename(file.filename)
               
               #Saving the file temporarily to local
               global file_path
               file_path=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
               file.save(file_path)
               
               #Reading the file first 10 rows as data frame to get the column names
               data=pd.read_csv(file_path,nrows=10,sep=delimiter)
               columns=data.columns
               
               #Creating a list of the column names and also replacing space with underscore
               collist=[]
               for col in columns:   
                   collist.append(col.strip().replace(' ' , '_') )
               
               #reading the file to a global dataframe with all column as string  
               global file_data
               file_data=pd.read_csv(file_path,names=collist,dtype=str,sep=delimiter,skiprows=1)
               
               #deleting the file from local
               os.remove(file_path)
                
               #flashing the message to UI
               flash(f'File Added Successfully! Proceed to Mapping to complete the process', 'info')         
               
               #sending the file type and the column names to UI for further mapping functionality
               return redirect(url_for('data.datamap',name=filetype,columns=collist)) 
        return redirect(url_for('data.dataurl'))







@data.route("/datamap", methods=['GET', 'POST'])
def datamap():
    #User authentication
    if current_user.is_authenticated==False:
        flash('User not logged in', 'info')
        return redirect(url_for('main.login'))
    

    
    #Retrieve the file type uploaded from UI
    filetype=request.args.get('name', default="", type=str)
    
    #Retrieve the list of columns in the upload file sent by the GET request
    columns=request.args.getlist('columns')
    
    #Sending the details to the data.html template
    return render_template('datamap.html',title='Data Map',filename=filetype,columns=columns)




#FUNCTIONALTY TO MAP FILE COLUMNS TO DATABASE COLUMNS AND LOAD RECORDS TO DATABASE 
@data.route('/input_account_process')
def input_account_process():
    try:
        #retreving the file type from UI
        FileType = request.args.get('FileType',default=None, type=str)

        #If the file type is CALL
        if(FileType.strip()=='Call'):
            
            #retreving the mapped columns
            Call1 = request.args.get('Call1',default=None, type=str)
            Call2 = request.args.get('Call2',default=None, type=str)
            Call3 = request.args.get('Call3',default=None, type=str)
            Call4 = request.args.get('Call4',default=None, type=str)
            Call5 = request.args.get('Call5',default=None, type=str)
            Call6 = request.args.get('Call6',default=None, type=str)
            Call7 = request.args.get('Call7',default=None, type=str)
            Call8 = request.args.get('Call8',default=None, type=str)
            Call9 = request.args.get('Call9',default=None, type=str)
            Call10 = request.args.get('Call10',default=None, type=str)
            Call11 = request.args.get('Call11',default=None, type=str)
            Call12 = request.args.get('Call12',default=None, type=str)
            Call13 = request.args.get('Call13',default=None, type=str)
            Call14 = request.args.get('Call14',default=None, type=str)
            Call15 = request.args.get('Call15',default=None, type=str)
            
            #looping the file data frame and inserting into the call table
            for index,row in file_data.iterrows():
                call = Call(activity_month=str(row[Call1]).strip(),display_brand_name=str(row[Call2]).strip(), display_franchise_name=str(row[Call3]).strip(), branded_unbranded=str(row[Call4]).strip(), call_identifier=str(row[Call5]).strip(), Customer_id=str(row[Call6]).strip(),parent_call_identifier=str(row[Call7]).strip(), call_detail=str(row[Call8]).strip(), account_type=str(row[Call9]).strip(), account_specialty=str(row[Call10]).strip(), rep_employee_code=str(row[Call11]).strip(), rep_territory_num=str(row[Call12]).strip(),call_detail_count=str(row[Call13]).strip(), market_detail_count=str(row[Call14]).strip(), rep_full_name=str(row[Call15]).strip())
                db.session.add(call)
                if index % 1000 == 0:
                    db.session.flush()
            
            #commiting to database
            db.session.flush()        
            db.session.commit()
        
        #if the file type is CALL SAMPLE
        elif(FileType.strip()=='Call Sample'):
            #retreving the mapped columns
            CallSample1 = request.args.get('CallSample1',default=None, type=str)
            CallSample2 = request.args.get('CallSample2',default=None, type=str)
            CallSample3 = request.args.get('CallSample3',default=None, type=str)
            CallSample4 = request.args.get('CallSample4',default=None, type=str)
            CallSample5 = request.args.get('CallSample5',default=None, type=str)
            CallSample6 = request.args.get('CallSample6',default=None, type=str)
            
            #looping the file data frame and inserting into the call sample table
            for index,row in file_data.iterrows():
                callsample = Call_Sample(Customer_id=str(row[CallSample1]).strip(),sample_type=str(row[CallSample2]).strip(), derived_call_id=str(row[CallSample3]).strip(), date_period=str(row[CallSample4]).strip(), territory_id=str(row[CallSample5]).strip(), sample_quantity=str(row[CallSample6]).strip())
                db.session.add(callsample)
                if index % 1000 == 0:
                    db.session.flush()
            #commiting to database
            db.session.flush()        
            db.session.commit()
                
        #if the file type is AFFILATION
        elif(FileType.strip()=='Affiliation'):
            #retreving the mapped columns
            Affiliation1 = request.args.get('Affiliation1',default=None, type=str)
            Affiliation2 = request.args.get('Affiliation2',default=None, type=str)
            Affiliation3 = request.args.get('Affiliation3',default=None, type=str)
            Affiliation4 = request.args.get('Affiliation4',default=None, type=str)
            
            #looping the file data frame and inserting into the affiliation table
            for index,row in file_data.iterrows():
                affiliation = Affiliation(parent_account_id=str(row[Affiliation1]).strip(),child_account_id=str(row[Affiliation2]).strip(), customer_id=str(row[Affiliation3]).strip(), affiliation_type=str(row[Affiliation4]).strip())
                db.session.add(affiliation)
                if index % 1000 == 0:
                    db.session.flush()
            #commiting to database
            db.session.flush()        
            db.session.commit()
        
        #If the file type is Prescription
        elif(FileType.strip()=='Prescription'):
            
            #retreving the mapped columns
            P1 = request.args.get('P1',default=None, type=str)
            P2 = request.args.get('P2',default=None, type=str)
            P3 = request.args.get('P3',default=None, type=str)
            P4 = request.args.get('P4',default=None, type=str)
            P5 = request.args.get('P5',default=None, type=str)
            P6 = request.args.get('P6',default=None, type=str)
            P7 = request.args.get('P7',default=None, type=str)
            P8 = request.args.get('P8',default=None, type=str)
            P9 = request.args.get('P9',default=None, type=str)
            P10 = request.args.get('P10',default=None, type=str)
            P11 = request.args.get('P11',default=None, type=str)
            P12 = request.args.get('P12',default=None, type=str)
            P13 = request.args.get('P13',default=None, type=str)
            P14 = request.args.get('P14',default=None, type=str)
            P15 = request.args.get('P15',default=None, type=str)
            P16 = request.args.get('P16',default=None, type=str)
            P17 = request.args.get('P17',default=None, type=str)
            P18 = request.args.get('P18',default=None, type=str)
            print(P1)
            
            #looping the file data frame and inserting into the Prescription table
            for index,row in file_data.iterrows():
                prescription = Prescription(Customer_id=str(row[P1]).strip(),customer_type=str(row[P2]).strip(), specialty_code=str(row[P3]).strip(), product_group=str(row[P4]).strip(), product_brand=str(row[P5]).strip(), nrx_m1=str(row[P6]).strip(),nrx_m2=str(row[P7]).strip(), nrx_m3=str(row[P8]).strip(), nrx_m4=str(row[P9]).strip(), nrx_m5=str(row[P10]).strip(), nrx_m6=str(row[P11]).strip(), trx_m1=str(row[P12]).strip(),trx_m2=str(row[P13]).strip(), trx_m3=str(row[P14]).strip(), trx_m4=str(row[P15]).strip(), trx_m5=str(row[P16]).strip(), trx_m6=str(row[P17]).strip(), data_date=str(row[P18]).strip())
                db.session.add(prescription)
                if index % 1000 == 0:
                    db.session.flush()
            
            #commiting to database
            db.session.flush()        
            db.session.commit()

        elif(FileType.strip()=='Rep Mapping'):
            #retreving the mapped columns
            RepMapping1 = request.args.get('RepMapping1',default=None, type=str)
            RepMapping2 = request.args.get('RepMapping2',default=None, type=str)
            print(RepMapping1)

            
            #looping the file data frame and updating the User table
            for index,row in file_data.iterrows():
                print(row)
                user=User.query.filter_by(email=str(row[RepMapping2]).strip()).first()
                print(user)
                #updating the rep manager id with current logged in manager
                user.manager_id=current_user.id
        
                #commiting the database
                db.session.commit()
                db.session.close()
                


        #Flask load success message to UI
        flash('File Loaded to the database', 'success')   
        return redirect(url_for('data.dataurl'))
    except Exception as e:
        return str(e)
    




#DOWNLOAD CALL DATA FUNCTIONALTY
@data.route('/dataupload/download_call')
def download_call ():
    
    #file name with current timestamp
    now = datetime.datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    filename='call_'+current_time+".csv"
    
    #create data frame with call table
    data_frame=pd.read_sql('select * from call',sql_engine)
    
    #saving the file to local
    path=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
    data_frame.to_csv(path,index=False)
    
    #sending the download path to UI
    return send_file(path, as_attachment=True)





#DOWNLOAD CALLSAMPLE DATA FUNCTIONALTY
@data.route('/dataupload/download_callsample')
def download_callsample ():
    
    #file name with current timestamp
    now = datetime.datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    filename='call_sample_'+current_time+".csv"
    
    #create data frame with call_sample table
    data_frame=pd.read_sql('select * from call_sample',sql_engine)
    
    #saving the file to local
    path=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
    data_frame.to_csv(path,index=False)
    
    #sending the download path to UI    
    return send_file(path, as_attachment=True)





#DOWNLOAD AFFLIATION DATA FUNCTIONALTY
@data.route('/dataupload/download_affiliation')
def download_affiliation ():
    
    #file name with current timestamp    
    now = datetime.datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    filename='affiliation_'+current_time+".csv"
    
    #create data frame with affilation table    
    data_frame=pd.read_sql('select * from affiliation',sql_engine)
    
    #saving the file to local    
    path=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
    data_frame.to_csv(path,index=False)
    
    #sending the download path to UI      
    return send_file(path, as_attachment=True) 






#DOWNLOAD PRESCRIPTION DATA FUNCTIONALTY
@data.route('/dataupload/download_prescription')
def download_prescription ():
    
    #file name with current timestamp    
    now = datetime.datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    filename='prescription_'+current_time+".csv"
    
    #create data frame with affilation table    
    data_frame=pd.read_sql('select * from prescription',sql_engine)
    
    #saving the file to local    
    path=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
    data_frame.to_csv(path,index=False)
    
    #sending the download path to UI      
    return send_file(path, as_attachment=True) 





	
#VIEW SALES REP'S ENTERED DATA 
@data.route("/datatab_filter", methods=['GET', 'POST'])
def datatab_filter():
    try:
        #filters to data, currently date filters are not applied 
        Initial_date = request.args.get('Initial_date', default="", type=str)
        Final_date = request.args.get('Final_date', default="", type=str)
        #dt = parse(Initial_date)
        
        #retreving the rep name
        Rep_Names = request.args.get('Rep_Names', default="", type=str)
        
        #retrieve all users from the database
        users=pd.read_sql("select * from user ",sql_engine)
        
        #if filter is selected for all, then whole database is retrieved
        if (Rep_Names.strip()=='All'):
            account_df=pd.read_sql("select * from account ",sql_engine)
            account_var_df=pd.read_sql("select * from account_var",sql_engine)            
        
        #if 'All' option is not selected i.e. a sales rep is selected, then the data is retrieved for that rep 
        else:
            reps=db.session.query(User).from_statement(text("SELECT * FROM user where manager_id="+str(current_user.id))).all()
            for rep in reps:
                if(str(rep.username).strip()==Rep_Names.strip()):
                    account_df=pd.read_sql("select * from account where user_id="+str(rep.id),sql_engine)
                    account_var_df=pd.read_sql("select * from account_var",sql_engine)
        
        #joining the user, account, account_var dataframe to create a single global dataframe also the removing unwanted columns
        account_df.rename(index=str, columns={"id": "acc_id"},inplace=True)
        global merged_accounts
        merged_acc = pd.merge(account_df, account_var_df, left_on='acc_id', right_on='npi_id')
        merged_acc.drop(['id'], axis=1,inplace=True)
        merged_accounts=pd.merge(users, merged_acc, left_on='id', right_on='user_id')
        merged_accounts.drop(['id','user_id','acc_id','user_type','npi_id','password','manager_id'], axis=1,inplace=True)
        merged_accounts.rename(index=str, columns={"username": "RepName","email":"RepEmail"},inplace=True)
        
        #converting the dataframe to json format
        jsonData=merged_accounts.to_dict('records')      

        #Sending the json to UI for display
        return jsonify( jsonData)
    except Exception as e:
        return str(e)   	
    





#DOWNLOAD SALES REP'S ENTERED DATA 
@data.route('/data/download_file')
def download_file():
    #file name with current timestamp    
    now = datetime.datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    filename='data_'+current_time+".csv"
    
    #saving the global dataframe merged_accounts as csv to local      
    path=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
    merged_accounts.to_csv(path,index=False)
    
    #sending the download path to UI        
    return send_file(path, as_attachment=True)	   










