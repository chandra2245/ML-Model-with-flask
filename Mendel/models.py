#CODE FOR MANAGING THE SQLITE DATABASE

#IMPORTING THE REGQUIRED LIBRARIES
from datetime import datetime
from Mendel import db, login_manager
from flask_login import UserMixin




#LOGIN MANAGER TO LOAD THE USER
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))






#USER TABLE
class User(db.Model,UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(60), nullable=False)
    manager_id= db.Column(db.Integer, nullable=True)
    accounts = db.relationship('Account', backref='author', lazy=True)
    potentials = db.relationship('Potential_Volume', backref='author', lazy=True)
    ranks = db.relationship('Segment_Rank', backref='author', lazy=True)
    ms_cats= db.relationship('Market_Share_Cat', backref='author', lazy=True)
    drivers_ranks= db.relationship('Drivers_Rank', backref='author', lazy=True)
    drivers_defs= db.relationship('Drivers_Definition', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"






#ACCOUNT BASE TABLE
class Account(db.Model):
    __tablename__='account'
    id = db.Column(db.Integer, primary_key=True)
    NPI_ID = db.Column(db.String(15), unique=True, nullable=False)
    Health_Groups = db.Column(db.String(50), nullable=False)
    Account_ID = db.Column(db.String(50), nullable=False)
    Account_Name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_vars = db.relationship('Account_Var', backref='acc', lazy=True)

    def __repr__(self):
        return f"Account('{self.Account_ID}', '{self.Account_Name}')"







#ACCOUNT DATA WITH TARGET CRITERIAS TABLE
class Account_Var(db.Model):
    __tablename__='account_var'
    id = db.Column(db.Integer, primary_key=True)
    TargetingCriteria1 = db.Column(db.String(50), nullable=True)
    TargetingCriteria2 = db.Column(db.String(50), nullable=True)
    TargetingCriteria3 = db.Column(db.String(50), nullable=True)
    TargetingCriteria4 = db.Column(db.String(50), nullable=True)
    TargetingCriteria5 = db.Column(db.String(50), nullable=True)
    TargetingCriteria6 = db.Column(db.String(50), nullable=True)
    TargetingCriteria7 = db.Column(db.String(50), nullable=True)
    TargetingCriteria8 = db.Column(db.String(50), nullable=True)
    TargetingCriteria9 = db.Column(db.String(50), nullable=True)
    TargetingCriteria10 = db.Column(db.String(50), nullable=True)
    TargetingCriteria11 = db.Column(db.String(50), nullable=True)
    TargetingCriteria12 = db.Column(db.String(50), nullable=True)
    
    Potential_Value = db.Column(db.Integer, nullable=False)
    Selling_Drug = db.Column(db.Integer, nullable=False)
    Competitor_Drug = db.Column(db.Integer, nullable=False)
    Actual_Sales = db.Column(db.Integer, nullable=False)
    Target_Sales = db.Column(db.Integer, nullable=False)
    Prob_Score = db.Column(db.Integer, nullable=True)
    NBA_insights= db.Column(db.String(100), nullable=True)
    Goal_Strategy= db.Column(db.String(100), nullable=True)
    Date_Posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    npi_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    

    def __repr__(self):
        return f"Account_Var('{self.npi_id}', '{self.Date_Posted}')"


#class Account_Message(db.Model):
#    __tablename__='account_var'
#    id = db.Column(db.Integer, primary_key=True)
#
#
#    npi_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
#    
#
#    def __repr__(self):
#        return f"Account_Var('{self.npi_id}', '{self.Date_Posted}')"



#POTENTIAL VOLUME TABLE
class Potential_Volume(db.Model):
    __tablename__='potential_volume'
    id = db.Column(db.Integer, primary_key=True)
    Limit = db.Column(db.String(15))
    OA_Patients = db.Column(db.String(50))
       

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Potential_Volume('{self.Limit}', '{self.OA_Patients}')"    
    





#SEGMENT RANK TABLE
class Segment_Rank(db.Model):
    __tablename__='segment_rank'
    id = db.Column(db.Integer, primary_key=True)
    Rank = db.Column(db.String(15))
    Segment = db.Column(db.String(50))
       

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Segment_Rank('{self.Rank}', '{self.Segment}')"






#MARKET SHARE CATEGORIZATION TABLE
class Market_Share_Cat(db.Model):
    __tablename__='market_share_cat'
    id = db.Column(db.Integer, primary_key=True)
    Category = db.Column(db.String(15))
    Limits = db.Column(db.String(50))
       

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Market_Share_Cat('{self.Category}', '{self.Limits}')"   
 
    
    
    
    
    
#PROBABILITY DRIVERS RANKINGS TABLE
class Drivers_Rank(db.Model):
    __tablename__='drivers_rank'
    id = db.Column(db.Integer, primary_key=True)
    Value_Definition = db.Column(db.String(15))
    Value = db.Column(db.String(50))
       

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Drivers_Rank('{self.Value_Definition}', '{self.Value}')"     
    
    
    
    
    
    
#PROBABILITY DRIVERS DEFINITION TABLE
class Drivers_Definition(db.Model):
    __tablename__='drivers_definition'
    id = db.Column(db.Integer, primary_key=True)
    Targeting_Criteria = db.Column(db.String(15))
    Driver_1 = db.Column(db.String(50), nullable=True)
    Driver_2 = db.Column(db.String(50), nullable=True)
    Driver_3 = db.Column(db.String(50), nullable=True)
    Driver_4 = db.Column(db.String(50), nullable=True)
    Driver_5 = db.Column(db.String(50), nullable=True)
    Driver_6 = db.Column(db.String(50), nullable=True)
    Driver_7 = db.Column(db.String(50), nullable=True)
    
    Weight = db.Column(db.String(50))
       

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Drivers_Definition('{self.Targeting_Criteria}', '{self.Weight}')"        
    
    
    
    
    
    
    
#ISA CALL DATA TABLE 
class Call(db.Model):
    __tablename__='call'
    id = db.Column(db.Integer, primary_key=True)
    activity_month = db.Column(db.String(50), nullable=True)
    display_brand_name = db.Column(db.String(50), nullable=True)
    display_franchise_name = db.Column(db.String(50), nullable=True)
    branded_unbranded = db.Column(db.String(50), nullable=True)
    call_identifier = db.Column(db.String(50), nullable=True)
    Customer_id = db.Column(db.String(50), nullable=True)
    parent_call_identifier = db.Column(db.String(50), nullable=True)
    call_detail= db.Column(db.String(50), nullable=True )
    account_type= db.Column(db.String(50), nullable=True)
    account_specialty= db.Column(db.String(50), nullable=True)
    rep_employee_code= db.Column(db.String(50), nullable=True)
    rep_territory_num= db.Column(db.String(50), nullable=True)
    call_detail_count= db.Column(db.String(50), nullable=True)
    market_detail_count= db.Column(db.String(50), nullable=True)
    rep_full_name= db.Column(db.String(50), nullable=True)

       

    def __repr__(self):
        return f"Call('{self.call_identifier}', '{self.Customer_id}','{self.call_detail}')"    






#CALL SAMPLE DATA TABLE 
class Call_Sample(db.Model):
    __tablename__='call_sample'
    id = db.Column(db.Integer, primary_key=True)
    Customer_id = db.Column(db.String(50), nullable=True)
    sample_type = db.Column(db.String(50), nullable=True)
    derived_call_id= db.Column(db.String(50), nullable=True )
    date_period= db.Column(db.String(50), nullable=True)
    territory_id= db.Column(db.String(50), nullable=True)
    sample_quantity= db.Column(db.String(50), nullable=True)
      

    def __repr__(self):
        return f"Call_Sample('{self.Customer_id}', '{self.sample_type}','{self.sample_quantity}')"       
    




    
#AFFILIATION INPUT 
class Affiliation(db.Model):
    __tablename__='affiliation'
    id = db.Column(db.Integer, primary_key=True)
    parent_account_id = db.Column(db.String(50), nullable=True)
    child_account_id = db.Column(db.String(50), nullable=True)
    customer_id= db.Column(db.String(50), nullable=True )
    affiliation_type= db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"Affiliation('{self.parent_account_id}', '{self.child_account_id}','{self.affiliation_type}')"    
    
    
    
    
    
#PRESCRIPTION TABLE 
class Prescription(db.Model):
    __tablename__='prescription'
    id = db.Column(db.Integer, primary_key=True)
    Customer_id = db.Column(db.String(50), nullable=True)
    customer_type = db.Column(db.String(50), nullable=True)
    specialty_code = db.Column(db.String(50), nullable=True)
    product_group = db.Column(db.String(50), nullable=True)
    product_brand = db.Column(db.String(50), nullable=True)
    nrx_m1 = db.Column(db.String(50), nullable=True)
    nrx_m2 = db.Column(db.String(50), nullable=True)
    nrx_m3= db.Column(db.String(50), nullable=True )
    nrx_m4= db.Column(db.String(50), nullable=True)
    nrx_m5= db.Column(db.String(50), nullable=True)
    nrx_m6= db.Column(db.String(50), nullable=True)
    trx_m1 = db.Column(db.String(50), nullable=True)
    trx_m2 = db.Column(db.String(50), nullable=True)
    trx_m3= db.Column(db.String(50), nullable=True )
    trx_m4= db.Column(db.String(50), nullable=True)
    trx_m5= db.Column(db.String(50), nullable=True)
    trx_m6= db.Column(db.String(50), nullable=True)
    data_date= db.Column(db.String(50), nullable=True)


       

    def __repr__(self):
        return f"Call('{self.Customer_id}', '{self.product_group}','{self.product_brand}')"     
    
    
#MASTER ANALYSIS DATA TABLE
class Mastertable(db.Model):
    __tablename__='mastertable'
    id = db.Column(db.Integer, primary_key=True)
    Rep_name	= db.Column(db.String(50), nullable=True)
    Rep_ID	= db.Column(db.String(50), nullable=True)
    Rep_Email	= db.Column(db.String(50), nullable=True)
    Health_Group	= db.Column(db.String(50), nullable=True)
    Account_Name	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_1	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_2	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_3	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_4	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_5	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_6	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_7	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_8	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_9	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_10	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_11	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_12	= db.Column(db.String(50), nullable=True)
    Targeting_Criteria_13	= db.Column(db.String(50), nullable=True)
    Prob_Score	= db.Column(db.String(50), nullable=True)
    Total_Potential_Value	= db.Column(db.String(50), nullable=True)
    Actual_Sales	= db.Column(db.String(50), nullable=True)
    Target_Sales	= db.Column(db.String(50), nullable=True)
    Market_Share_in_Account	= db.Column(db.String(50), nullable=True)
    Territory_Potential_Sales	= db.Column(db.String(50), nullable=True)
    Per_of_Territory_Actual_Sales	= db.Column(db.String(50), nullable=True)
    Segment	= db.Column(db.String(50), nullable=True)
    Territory_Quota	= db.Column(db.String(50), nullable=True)
    Territory_Quota_Attainment	= db.Column(db.String(50), nullable=True)
    Target_Score_1	= db.Column(db.String(50), nullable=True)
    Target_Score_2	= db.Column(db.String(50), nullable=True)
    Target_Score_3	= db.Column(db.String(50), nullable=True)
    Target_Score_4	= db.Column(db.String(50), nullable=True)
    Target_Score_5	= db.Column(db.String(50), nullable=True)
    Target_Score_6	= db.Column(db.String(50), nullable=True)
    Target_Score_7	= db.Column(db.String(50), nullable=True)
    Target_Score_8	= db.Column(db.String(50), nullable=True)
    Target_Score_9	= db.Column(db.String(50), nullable=True)
    Target_Score_10	= db.Column(db.String(50), nullable=True)
    Target_Score_11	= db.Column(db.String(50), nullable=True)
    Target_Score_12	= db.Column(db.String(50), nullable=True)
    DataInput_TimeStamp	= db.Column(db.String(50), nullable=True)
    DataInput_DataSerial	= db.Column(db.String(50), nullable=True)
       

    def __repr__(self):
        return f"Mastertable('{self.Rep_name}', '{self.Account_Name}')"         
    