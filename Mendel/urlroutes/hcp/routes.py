#ROUTES FOR ACTION PLAN AND HCP 360 VIEW


#IMPORT ALL THE REQUIRED LIBRARIES
import random
from Mendel import db,app
from sqlalchemy import text
from flask_login import login_user, current_user, logout_user    
from flask import render_template,  flash, redirect, url_for, Blueprint, request
from Mendel.models import User,Account,Account_Var, Potential_Volume,Segment_Rank,Market_Share_Cat,Drivers_Rank,Drivers_Definition




#CREATING THE BLUE PRINT VARIABLE FOR THE MAIN FOR ROUNTING 
hcp = Blueprint('hcp', __name__)











#ROUTE FOR THE ACTION PLAN TAB
@hcp.route("/actionplan")                            
def actionplan():
    #GET request 
    #retrieving the already loaded accounts for the given sales rep
    account_variables = Account_Var.query.all()
    accounts=db.session.query(Account).from_statement(text("SELECT * FROM account where user_id="+str(current_user.id))).all()
    
    #Static Insights generated for display purpose
    NBA_insight =['Past Touchpoint : Rep Call, Email<br />Next Touchpoint: ISA Call<br />Next Message: On Safety','Past Touchpoint : Rep Call<br />Next Touchpoint: MLO Call<br />Next Message: Latest Clinical Trial result<br />','Past Touchpoint : Rep Call, Helpdesk call<br />Next Touchpoint: Rep Call<br />Next Message: Provide Sample','Past Touchpoint : Rep Call<br />Next Touchpoint: ISA Call<br />Next Message: On Efficacy','Past Touchpoint : Rep Call, Email<br />Next Touchpoint: Rep Call<br />Next Message: Offer promotional discount','Past Touchpoint : Rep Call, ISA Call<br />Next Touchpoint: Rep Call<br />Next Message: Invite for Speaker Program','"Past Touchpoint : Rep Call, ISA Call, MLO Call<br />Next Touchpoint: Help Desk Call<br />Next Message: Reimbursement plans']
    print(len(NBA_insight))
    rand_numbers=[]
    pot=0
    #Generating Percentage of Potential Volume for each HCP at Territory Level
    for account in accounts:
        account_vars=db.session.query(Account_Var).from_statement(text("SELECT * FROM account_var where npi_id="+str(account.id))).all()
        for account_var in account_vars:
            rand_numbers.append(random.randrange(0,6))
            pot=pot+account_var.Potential_Value

    #Also generating the Market Share
    Per_Potential_Sales=[]
    Market_Share=[]
    for account in accounts:
        account_vars=db.session.query(Account_Var).from_statement(text("SELECT * FROM account_var where npi_id="+str(account.id))).all()
        for account_var in account_vars:
            Per_Potential_Sales.append(round((account_var.Potential_Value/pot)*100,2))
            Market_Share.append(round((account_var.Selling_Drug/(account_var.Selling_Drug+account_var.Competitor_Drug))*100,2))
    global tablelength
    tablelength=len(Per_Potential_Sales)  
    return render_template('actionplan.html',title='Action Plan',accounts=accounts,account_vars=account_variables,insights=NBA_insight,rand_numbers=rand_numbers,Per_Potential_Sales=Per_Potential_Sales,Market_Share=Market_Share)


#GOAL STRATEGY INPUT FORM RENDER
@hcp.route("/goalstrategyurl", methods=['GET', 'POST'])
def goalstrategyurl():
    if request.method == 'POST':
        
        strategy=[]
        for i in range(0,tablelength):
            strategy.append(request.form.get('StrategyInput_'+str(i+1),default=None, type=str))
            
        accounts=db.session.query(Account).from_statement(text("SELECT * FROM account where user_id="+str(current_user.id))).all()
          
        #looping the table and updating the account with the input goal strategy
        acc_var_ids=[]
        for account in accounts:
            account_vars=db.session.query(Account_Var).from_statement(text("SELECT * FROM account_var where npi_id="+str(account.id))).all()
            for account_var in account_vars:
                acc_var_ids.append(account_var.id)
        
        i=0 
        for var_id in   acc_var_ids:
            var=Account_Var.query.filter_by(id=var_id).first()
            var.Goal_Strategy=strategy[i]
            i=i+1
             #commiting the database
            db.session.commit()
            db.session.close()  
                  
        flash(f'Goal Strategy Updated', 'success') 
        return redirect(url_for('hcp.actionplan')) 
  












#ROUTE FOR THE HOME URL
@hcp.route("/hcp360")
#hcp FOR HOME TAB                              
def hcp360():
    return render_template('hcp360.html')











@hcp.route("/hcp360_form", methods=['GET', 'POST'])
#hcp FOR HOME TAB                              
def hcp360_form():
    if request.method == 'POST':
        return redirect(url_for('hcp.hcp360_form')) 
    return render_template('hcp360_2.html')










@hcp.route("/hcp360_2")
#hcp FOR HOME TAB                              
def hcp360_2():
    return render_template('hcp360_2.html')
	
	