# ROUTING PAGE FOR THE TARGET DEFINITION TAB, MANAGER IS REQUIRED TO DEFINE TARGET FOR THE REPS 
# TARGET DEFINITION IS SAVED IN THE FORM OF POTENTIAL VOLUME, SEGMENT RANK, MARKET SHARE CATEGORIZATION, DRIVERS RANK, DRIVERS DEFINITION

# IMPORTED THE REQUIRED LIBRARIES

from Mendel import db
from sqlalchemy import text
from flask_login import  current_user    
from flask import render_template, request, flash, redirect, url_for, jsonify, Blueprint
from Mendel.models import User, Potential_Volume,Segment_Rank,Market_Share_Cat,Drivers_Rank,Drivers_Definition


#CREATING THE targetdefinition BLUE PRINT VARIABLE
targetdefinition = Blueprint('targetdefinition', __name__)


#ROUTE FOR TARGET DEFINITION MANAGER TAB
@targetdefinition.route("/targetdefinition",methods=['GET', 'POST'])
def targetdefinitions():
    #User Authentication
    if current_user.is_authenticated==False:
        flash('User not logged in', 'info')
        return redirect(url_for('main.login')) 
    
    #Manager filled form mapping to the database
    if request.method == 'POST':
        #Potential Volume Size
        table1_size = request.form.get('table1_size',default=0, type=int)
        #Segment Rank Table Size
        table2_size = request.form.get('table2_size',default=0, type=int)
        #Market Share Table Size
        table3_size = request.form.get('table3_size',default=0, type=int)
        #Drivers Rank Table Size
        table4_size = request.form.get('table4_size',default=0, type=int)
        #Drivers Definition Table Size
        table5_size = request.form.get('table5_size',default=0, type=int)
        
        db.session.query(Potential_Volume).delete()
        db.session.query(Segment_Rank).delete()
        db.session.query(Market_Share_Cat).delete()
        db.session.query(Drivers_Rank).delete()
        db.session.query(Drivers_Definition).delete()
        db.session.commit()
        #Retriving Manager record by the email id
        users=db.session.query(User).from_statement(text("SELECT * FROM user where email=\'"+str(current_user.email.strip())+"\'")).all()

        #if the Rep record exists
        if len(users)>0 :
            
            #Inserting Potential Value details to database
            if table1_size>0:
                i=1
                while i<=table1_size:
                    Limit=request.form.get('txtboxt1c1['+str(i)+']',default="", type=str)
                    OA_Patients=request.form.get('txtboxt1c2['+str(i)+']',default="", type=str)
                    potential=Potential_Volume(Limit=Limit,OA_Patients=OA_Patients,author=users[0])
                    db.session.add(potential)
                    db.session.commit()
                    i=i+1
            
            #Inserting Segment Rank details to database
            if table2_size>0:
                i=1
                while i<=table2_size:
                    Rank=request.form.get('txtboxt2c1['+str(i)+']',default="", type=str)
                    Segment=request.form.get('txtboxt2c2['+str(i)+']',default="", type=str)
                    seg_rank=Segment_Rank(Rank=Rank,Segment=Segment,author=users[0])
                    db.session.add(seg_rank)
                    db.session.commit()
                    i=i+1
            
            #Insering Market Share Category details to database
            if table3_size>0:
                i=1
                while i<=table3_size:
                    Category=request.form.get('txtboxt3c1['+str(i)+']',default="", type=str)
                    Limits=request.form.get('txtboxt3c2['+str(i)+']',default="", type=str)
                    market_share=Market_Share_Cat(Category=Category,Limits=Limits,author=users[0])
                    db.session.add(market_share)
                    db.session.commit()
                    i=i+1
                    
            #Inserting Driver Definition details to database
            if table4_size>0:
                i=1
                while i<=table4_size:
                    Value_Definition=request.form.get('txtboxt4c1['+str(i)+']',default="", type=str)
                    Value=request.form.get('txtboxt4c2['+str(i)+']',default="", type=str)
                    drivers_rank=Drivers_Rank(Value_Definition=Value_Definition,Value=Value,author=users[0])
                    db.session.add(drivers_rank)
                    db.session.commit()
                    i=i+1
           
            #Inserting Target Definition details to database
            if table5_size>0:
                i=1
                while i<=table5_size:
                    Targeting_Criteria=request.form.get('txtboxt5c1['+str(i)+']',default="", type=str)
                    Weight=request.form.get('txtboxt5c'+str(table4_size+2)+'['+str(i)+']',default="", type=str)
                    j=2
                    Drivers=[None,None,None,None,None,None,None]  
                    while j<=(table4_size+1):
                        Drivers[j-2]=request.form.get('txtboxt5c'+str(j)+'['+str(i)+']',default="", type=str)
                        j=j+1
                    
                    drivers_def=Drivers_Definition(Targeting_Criteria=Targeting_Criteria,Weight=Weight,Driver_1=Drivers[0],Driver_2=Drivers[1],Driver_3=Drivers[2],Driver_4=Drivers[3],Driver_5=Drivers[4],Driver_6=Drivers[5],Driver_7=Drivers[6],author=users[0])
                    db.session.add(drivers_def)
                    db.session.commit()
                    i=i+1         
                
        #Insertion success notification to UI        
        flash(f'Target defined for Manager: {users[0].username} ', 'success')         
        
        #Redirect back to the Target definition manager page
        return redirect(url_for('targetdefinition.targetdefinitions'))
    
    #If the request is GET then render targetdefinition.html template
    return render_template('targetdefinition.html',title='Target definition')






#ROUTE FOR TARGET DEFINITION READ ONLY VIEW FOR SALES REPRESENTATIVE AS TARGET CAN ONLY BE DEFINED BY THE MANAGER
@targetdefinition.route("/targetdefinition_rep")
def targetdefinition_rep():
    #login user authentication
    if current_user.is_authenticated==False:
        flash('User not logged in', 'info')
        return redirect(url_for('main.login'))
    
    #Retriving the Potential Value details for the Logged in Sales Rep
    potential_volumes=db.session.query(Potential_Volume).from_statement(text("SELECT * FROM Potential_Volume where user_id="+str(current_user.manager_id))).all()
    
    #Retriving the Segment Rank details for the Rep
    segment_ranks=db.session.query(Segment_Rank).from_statement(text("SELECT * FROM Segment_Rank where user_id="+str(current_user.manager_id))).all()
    
    #Retriving the Market Share Category details for the Rep
    market_share_cats=db.session.query(Market_Share_Cat).from_statement(text("SELECT * FROM Market_Share_Cat where user_id="+str(current_user.manager_id))).all()
    
    #Retriving the Drivers Rank details for the Rep
    drivers_ranks=db.session.query(Drivers_Rank).from_statement(text("SELECT * FROM Drivers_Rank where user_id="+str(current_user.manager_id))).all()
    
    #Retriving the Target Definition details for the Rep
    drivers_definitions=db.session.query(Drivers_Definition).from_statement(text("SELECT * FROM drivers_definition where user_id="+str(current_user.manager_id))).all()
    
    #Sending the Sales Rep's defined target to html
    return render_template('targetdefinition_rep.html',title='Target definition',potential_volumes=potential_volumes,segment_ranks=segment_ranks,market_share_cats=market_share_cats,drivers_ranks=drivers_ranks,drivers_definitions=drivers_definitions)






#Function to check whether the Sales Rep email exists in the database
@targetdefinition.route('/user_exist')
def user_exist():
    try:
        #extracting the email entered in the user form
        useremail = request.args.get('useremail',default=None, type=str)
        
        #querying the user mail in the database
        users=db.session.query(User).from_statement(text("SELECT * FROM user where email=\'"+str(useremail.strip())+"\'")).all()
        output_text=None
        
        if len(users)>0 :
            output_text="<font color=\"blue\">Sales Representative User Exist!</font>"
        else:
            output_text="<font color=\"red\">Sales Representative User Not Exist!</font>"
        
        #Sending the response back to UI
        return jsonify(output_text=output_text)
    except Exception as e:
        return str(e)      	
	
	