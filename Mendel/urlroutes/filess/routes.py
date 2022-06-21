import os
import math
import numpy as np
import pandas as pd
from flask_login import  current_user    
from flask import render_template, request, flash, redirect, url_for,jsonify, Blueprint,send_file
from Mendel import db,app
from Mendel.models import Call, Call_Sample,Affiliation
from werkzeug.utils import secure_filename
from sqlalchemy import text,create_engine
from dateutil.parser import parse
import datetime

files = Blueprint('files', __name__)

#VALIDATION FUNCTION FOR FILE INPUT IN THE DATAINPUT TAB

ALLOWED_EXTENSIONS = set(['txt','csv'])
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


sql_engine = create_engine('sqlite:///Mendel//site.db', echo=False)




#ROUTE FOR data_upload TAB
@files.route("/dataupload",methods=['GET'])
def dataupload():
    if current_user.is_authenticated==False:
        flash('User not logged in', 'info')
        return redirect(url_for('main.login'))
    filename=request.args.get('name', default="", type=str)
    columns=request.args.getlist('columns')
    
    return render_template('dataupload.html',title='Data Upload',filename=filename,columns=columns)







#ROUTE FOR data_upload TAB, FILE IMPORT FUNCTIONALITY
@files.route("/fileupload",methods=['GET','POST'])
def fileupload():
        if request.method == 'POST':
            filetype = request.form.get('filetype',default=None, type=str)
            print(filetype)
            #File import Validations
            if 'file' not in request.files:
               flash('No file Part!', 'danger')
               return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
               flash('No selected file', 'danger')
               return redirect(request.url)
            if file and allowed_file(file.filename):
               filename = secure_filename(file.filename)
               
               global file_path
               file_path=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
               file.save(file_path)
               data=pd.read_csv(file_path,nrows=10)
               columns=data.columns
               collist=[]
               for col in columns:   
                   collist.append(col.strip().replace(' ' , '_') )
               global file_data
               file_data=pd.read_csv(file_path,names=collist,dtype=str,skiprows=1)
               os.remove(file_path)
               print("File Removed!")        
               
               flash(f'File Added Successfully! Proceed to Mapping to complete the process', 'info')         
               return redirect(url_for('files.dataupload',name=filetype,columns=collist)) 
        return redirect(url_for('files.dataupload'))



#ROUTE FOR DATA INPUT, MANUAL INPUT CALCULATED FIELDS CALCULATIONS
@files.route('/input_account_process')
def input_account_process():
    try:
        FileType = request.args.get('FileType',default=None, type=str)
        print(FileType)
        
        if(FileType.strip()=='Call'):
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
            print(Call1)
            for index,row in file_data.iterrows():
                call = Call(activity_month=str(row[Call1]).strip(),display_brand_name=str(row[Call2]).strip(), display_franchise_name=str(row[Call3]).strip(), branded_unbranded=str(row[Call4]).strip(), call_identifier=str(row[Call5]).strip(), Customer_id=str(row[Call6]).strip(),parent_call_identifier=str(row[Call7]).strip(), call_detail=str(row[Call8]).strip(), account_type=str(row[Call9]).strip(), account_specialty=str(row[Call10]).strip(), rep_employee_code=str(row[Call11]).strip(), rep_territory_num=str(row[Call12]).strip(),call_detail_count=str(row[Call13]).strip(), market_detail_count=str(row[Call14]).strip(), rep_full_name=str(row[Call15]).strip())
                db.session.add(call)
                if index % 1000 == 0:
                    db.session.flush()
            db.session.flush()        
            db.session.commit()
        
        elif(FileType.strip()=='Call Sample'):
            CallSample1 = request.args.get('CallSample1',default=None, type=str)
            CallSample2 = request.args.get('CallSample2',default=None, type=str)
            CallSample3 = request.args.get('CallSample3',default=None, type=str)
            CallSample4 = request.args.get('CallSample4',default=None, type=str)
            CallSample5 = request.args.get('CallSample5',default=None, type=str)
            CallSample6 = request.args.get('CallSample6',default=None, type=str)
            for index,row in file_data.iterrows():
                callsample = Call_Sample(Customer_id=str(row[CallSample1]).strip(),sample_type=str(row[CallSample2]).strip(), derived_call_id=str(row[CallSample3]).strip(), date_period=str(row[CallSample4]).strip(), territory_id=str(row[CallSample5]).strip(), sample_quantity=str(row[CallSample6]).strip())
                db.session.add(callsample)
                if index % 1000 == 0:
                    db.session.flush()
            db.session.flush()        
            db.session.commit()
                
        elif(FileType.strip()=='Affiliation'):
            Affiliation1 = request.args.get('Affiliation1',default=None, type=str)
            Affiliation2 = request.args.get('Affiliation2',default=None, type=str)
            Affiliation3 = request.args.get('Affiliation3',default=None, type=str)
            Affiliation4 = request.args.get('Affiliation4',default=None, type=str)
            for index,row in file_data.iterrows():
                affiliation = Affiliation(parent_account_id=str(row[Affiliation1]).strip(),child_account_id=str(row[Affiliation2]).strip(), customer_id=str(row[Affiliation3]).strip(), affiliation_type=str(row[Affiliation4]).strip())
                db.session.add(affiliation)
                if index % 1000 == 0:
                    db.session.flush()
            db.session.flush()        
            db.session.commit()
                

        flash('File Loaded to the database', 'success')   
        return jsonify()
    except Exception as e:
        return str(e)
    

@files.route('/dataupload/download_call')
def download_call ():
    now = datetime.datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    filename='call_'+current_time+".csv"
    data_frame=pd.read_sql('select * from call',sql_engine)
    path=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
    data_frame.to_csv(path,index=False)
    return send_file(path, as_attachment=True)


@files.route('/dataupload/download_callsample')
def download_callsample ():
    now = datetime.datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    filename='call_sample_'+current_time+".csv"
    data_frame=pd.read_sql('select * from call_sample',sql_engine)
    path=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
    data_frame.to_csv(path,index=False)
    return send_file(path, as_attachment=True)


@files.route('/dataupload/download_affiliation')
def download_affiliation ():
    now = datetime.datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    filename='affiliation_'+current_time+".csv"
    data_frame=pd.read_sql('select * from affiliation',sql_engine)
    path=os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
    data_frame.to_csv(path,index=False)
    return send_file(path, as_attachment=True)