 

aple=db.session.query(label('Act',func.sum(Account.Actual_Sales))).all()

for result in aple:
...     print(result.Act)


from Mendel import db

from Mendel.models import Mastertable

from Mendel.models import User,Account, Potential_Volume,Account_Var,Segment_Rank,Market_Share_Cat,Drivers_Rank,Drivers_Definition

db.session.query(User).delete()

from Mendel.models import Call, Call_Sample,Affiliation

db.create_all()

from sqlalchemy import text,update

user_d=Mastertable.query.all()


import pandas as pd #import pandas

header=['Rep_name',	'Rep_ID',	'Rep_Email',	'Health_Group',	'Account_Name',	'Targeting_Criteria_1',	'Targeting_Criteria_2',	'Targeting_Criteria_3',	'Targeting_Criteria_4',	'Targeting_Criteria_5',	'Targeting_Criteria_6',	'Targeting_Criteria_7',	'Targeting_Criteria_8',	'Targeting_Criteria_9',	'Targeting_Criteria_10',	'Targeting_Criteria_11',	'Targeting_Criteria_12',	'Targeting_Criteria_13',                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 	'Prob_Score',	'Total_Potential_Value',	                                                    'Actual_Sales',	'Target_Sales',	'Market_Share_in_Account',	'Territory_Potential_Sales',	                'Per_of_Territory_Actual_Sales',	'Segment',	                                                               'Territory_Quota',                                            		'Territory_Quota_Attainment',	'Target_Score_1',	'Target_Score_2',	'Target_Score_3',	'Target_Score_4',	'Target_Score_5',	'Target_Score_6',	'Target_Score_7',	'Target_Score_8',	'Target_Score_9',	'Target_Score_10',	'Target_Score_11',	'Target_Score_12',                                                                                                                                                                                                                                                                                                                                  	'DataInput_TimeStamp',	'DataInput_DataSerial']

mendel_data_log= pd.read_csv('D://Subhajit Code//import_file.csv',names=header,dtype=str,skiprows=1)

mendel_data_log.head()

for index,row in mendel_data_log.iterrows():
    call = Mastertable(Rep_name=str(Rep_name).strip(),Rep_ID=str(Rep_ID).strip(), Health_Group=str(Health_Group).strip(), Account_Name=str(Account_Name).strip(), Targeting_Criteria_1=str(Targeting_Criteria_1).strip(), Targeting_Criteria_2=str(Targeting_Criteria_2).strip(),Targeting_Criteria_3=str(Targeting_Criteria_3).strip(), Targeting_Criteria_4=str(Targeting_Criteria_4).strip(), Targeting_Criteria_5=str(Targeting_Criteria_5).strip(), Targeting_Criteria_6=str(Targeting_Criteria_6).strip(), Targeting_Criteria_7=str(Targeting_Criteria_7).strip(), Targeting_Criteria_8=str(Targeting_Criteria_8).strip(),Targeting_Criteria_9=str(Targeting_Criteria_9).strip(), Targeting_Criteria_10=str(Targeting_Criteria_10).strip(), Targeting_Criteria_11=str(Targeting_Criteria_11).strip(),Targeting_Criteria_12=str(Targeting_Criteria_12).strip(), Targeting_Criteria_13=str(Targeting_Criteria_13).strip(), Prob_Score=str(Prob_Score).strip(), Total_Potential_Value=str(Total_Potential_Value).strip(), Actual_Sales=str(Actual_Sales).strip(), Target_Sales=str(Target_Sales).strip(), Market_Share_in_Account=str(Market_Share_in_Account).strip(), Per_of_Territory_Actual_Sales=str(Per_of_Territory_Actual_Sales).strip(), Segment=str(Segment).strip(), Territory_Quota=str(Territory_Quota).strip(), Territory_Quota_Attainment=str(Territory_Quota_Attainment).strip(), Target_Score_1=str(Target_Score_1).strip(), Target_Score_2=str(Target_Score_2).strip(),Target_Score_3=str(Target_Score_3).strip(), Target_Score_4=str(Target_Score_4).strip(), Target_Score_5=str(Target_Score_5).strip(), Target_Score_6=str(Target_Score_6).strip(), Target_Score_7=str(Target_Score_7).strip(), Target_Score_8=str(Target_Score_8).strip(),Target_Score_9=str(Target_Score_9).strip(), Target_Score_10=str(Target_Score_10).strip(), Target_Score_11=str(Target_Score_11).strip(),Target_Score_12=str(Target_Score_12).strip(), DataInput_TimeStamp=str(DataInput_TimeStamp).strip(), DataInput_DataSerial=str(DataInput_DataSerial).strip())
    db.session.add(call)
    if index % 1000 == 0:
        db.session.flush()
    
#commiting to database
db.session.flush()        
db.session.commit()

db.session.query(Mastertable).delete()

mendel_data_log


x = db.session.query(Mastertable).get(1)


x

for index,row in mendel_data_log.iterrows():
    call = Mastertable(Rep_name=str(row['Rep_name']).strip())
    db.session.add(call)
    if index % 1000 == 0:
        db.session.flush()

mendel_data_log = pd.read_csv('D://Subhajit Code//import_file.csv')

print(user_d)

User.update().where(User.id==1).values(username='Harvey')

account_exist=User.query.filter_by(email=str('mike.ross@email.com').strip()).first()

account_exist.username
x = db.session.query(User).get(1)

x.username='Harvey Specter'


db.session.query(Affiliation).delete()
db.session.commit()

db.session.close()
    
user1=User(id=1,username='Harvey Specter',email='harvey.specter@email.com',password='admin',user_type='admin')
user2=User(id=2,username='Mike Ross', email='mike.ross@email.com',password='admin2',user_type='sales_rep',manager_id=1)
user3=User(id=3,username='Rachel Zane', email='rachel.zane@email.com',password='admin3',user_type='sales_rep',manager_id=1)

user4=User(id=4,username='Louis Litt', email='louis.litt@email.com',password='admin4',user_type='sales_rep',manager_id=1)

user5=User(id=5,username='Donna Paulson', email='donna.paulson@email.com',password='admin5',user_type='sales_rep')

    
db.session.add(user1)
db.session.add(user2)
db.session.add(user5)

db.session.commit()

db.session.close()

update(User).where(User.id==1).values(username='Harvey')


sd=db.session.query(Call).from_statement(text("SELECT * FROM call ")).all()

len(sd)


import pandas as pd

from sqlalchemy import create_engine

sql_engine = create_engine('sqlite:///Mendel//site.db', echo=False)
connection = sql_engine.raw_connection()
working_df.to_sql('data', connection,index=False, if_exists='append')


import datetime
from time import strftime


now = datetime.datetime.now()
current_time = now.strftime("%Y%m%d%H%M%S")
print("Current Time =", current_time)


datetime.datetime.now()
datetime.datetime(2009, 1, 6, 15, 8, 24, 78915)

print(datetime.datetime.now())
2018-07-29 09:17:13.812189

strftime("%Y-%m-%d %H:%M:%S", datetime.datetime.now())

data_frame=pd.read_sql("select * from account",sql_engine)
data_frame_var=pd.read_sql("select * from account_var",sql_engine)

data_frame
data_frame_var

df_merge_difkey = pd.merge(data_frame, data_frame_var, left_on='id', right_on='npi_id')

df_merge_difkey

Drivers_Definition.query.all()


db.session.query(Account_Var).from_statement(text("SELECT * FROM account_var where npi_id=1")).all()


users=db.session.query(User).from_statement(text("SELECT id FROM user where username='Searus Black'")).first()    

users.id

account=db.session.query(Account).from_statement(text("SELECT * FROM account where user_id="+str(users.id))).all()

from sqlalchemy import text

db.session.query(Drivers_Definition).from_statement(text("delete FROM Drivers_Definition"))


db.session.query(Drivers_Rank).from_statement(text("delete FROM Drivers_Rank")).all()

db.session.query(Account).delete()

db.session.query(Account_Var).delete()


db.session.query(Potential_Volume).delete()

db.session.query(Drivers_Rank).delete()

db.session.query(Drivers_Definition).delete()

db.session.query(Segment_Rank).delete()

db.session.query(Market_Share_Cat).delete()

Drivers_Rank.query.all()

from Mendel import models

models.query().delete()


account.Actual_Sales


users.id

act=0

for accounts in account:
    act=act+accounts.Actual_Sales
    
    
act    

User.query.all()

useremail="mike.ross@email.com"

user="\'"+useremail="\'"

str_append(useremail,"\'")

accounts=db.session.query(User).from_statement(text("SELECT * FROM user where email=\'"+str(useremail.strip())+"\'")).all()

len(accounts)
accounts[0]   

import pandas as pd

Calls_Data = pd.read_csv("Mendel/static/data/Calls_Data.csv")

Filtered_calls = Calls_Data[Calls_Data['REP_EMPLOYEE_EMAIL_ADDRESS']=='rachel.zane@email.com']

import datetime

Filtered_calls['DATA_DATE'] =  pd.to_datetime(Filtered_calls['DATA_DATE'], format='%m/%d/%Y')
Filtered_calls['count_column']=1
Filtered_calls['date_minus_time'] = Filtered_calls["DATA_DATE"].apply( lambda Filtered_calls : datetime.datetime(year=Filtered_calls.year, month=Filtered_calls.month, day=Filtered_calls.day))
Filtered_calls.set_index(Filtered_calls["date_minus_time"],inplace=True)
        
    
TS=Filtered_calls[['count_column']].resample('W').sum()
print(TS)

pd.get_dummies(Filtered_calls[['BRANDED_UNBRANDED','Decile']])

DF=Filtered_calls[['CALL_TYPE_DESCRIPTION','count_column']].groupby('CALL_TYPE_DESCRIPTION',as_index=False).sum()

DF


for index,row in DF.iterrows():
    print(row['CALL_TYPE_DESCRIPTION'])
    print (index)



Filtered_calls.columns

Filtered_calls.get_dummies(['Decile'])
Decile


TSData=[]

print(TSData)


TS.index.max()

date = TS.index.min()

while (date<=TS.index.max()):
    print(TS.loc[date,'count_column']) 
    date += datetime.timedelta(days=7)


pd.get_dummies(Filtered_calls['BRANDED_UNBRANDED'])