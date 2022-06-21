######################################################################
# Code for integration of ML Code with the Web App Code
######################################################################


#Importing the required libraries
import numpy as np #linear algebra
import pandas as pd #import pandas
import seaborn as sns # the commonly used alias for seaborn is sns
from sqlalchemy import create_engine 




####### Reading the data from the Database
sql_engine = create_engine('sqlite:///Mendel//site.db', echo=False)
data_frame=pd.read_sql('select * from mastertable',sql_engine)



####### data wrangling step for consistency
data_frame.replace("nan",np.nan,inplace=True)

#data_frame.info()
#data_frame.columns[19]

data_frame.drop(data_frame.columns[19], axis=1,inplace=True)
data_frame.drop(data_frame.columns[18], axis=1,inplace=True)
data_frame.drop(data_frame.columns[0], axis=1,inplace=True)

data_frame.drop(['Rep_name','Rep_Email','Targeting_Criteria_1','Targeting_Criteria_8','Targeting_Criteria_9',
                      'Segment','Target_Score_1','Target_Score_2','Target_Score_3',
                      'Target_Score_4','Target_Score_5','Target_Score_6','Target_Score_7',
                      'Target_Score_8','Target_Score_9','Target_Score_10','Target_Score_11','Target_Score_12','DataInput_DataSerial'], axis=1,inplace=True )

data_frame.rename(columns={"Rep_ID": "rep_id", "Health_Group": "health_grp","Account_Name" :"account_name",
                           "Targeting_Criteria_2" :"account_relation","Targeting_Criteria_3" :"injection_potential","Targeting_Criteria_4" :"pal",
                           "Targeting_Criteria_5" :"competitive_situation","Targeting_Criteria_6" :"clinical_mindset","Targeting_Criteria_7" :"value_perception",
                           "Targeting_Criteria_10" :"patients_treated_with_competitive_drug","Targeting_Criteria_11" :"patients_treated_with_selling_drug",
                           "Targeting_Criteria_12" :"competitive_drug_market_penitration","Total_Potential_Value":"total_potential_value",
                           "Actual_Sales":"actual_sales","Target_Sales":"target_sales","Market_Share_in_Account":"market_share_in_account",
                           "Territory_Potential_Sales":"percentage_territory_potential_sales","Per_of_Territory_Actual_Sales":"percentage_territory_actual_sales",
                           "Territory_Quota":"territory_quota","Territory_Quota_Attainment":"territory_quota_attainment","DataInput_TimeStamp":"input_timestamp"},inplace=True) 
 
#data_frame.head()    



###############################################
# 713538 Code start here 
###############################################   
mendel = pd.DataFrame(data_frame)
mendel.info()
mendel.head(5)
mendel.tail()
mendel.describe()    


#droping the row which has unneccesary value in all the columns
mendel = mendel[ (mendel['account_relation'] != 'Targeting Criteria_2') & (mendel['injection_potential'] != 'Targeting Criteria_3') 
                & ( mendel['pal'] != 'Targeting Criteria_4') & ( mendel['competitive_situation'] != 'Targeting Criteria_5' )
                & (mendel['clinical_mindset'] != 'Targeting Criteria_6') & (mendel['value_perception'] != 'Targeting Criteria_7') ]
#converting object/ character/ string  data type to numeric wherever required.
cols_num = ['patients_treated_with_competitive_drug','patients_treated_with_selling_drug',
                        'competitive_drug_market_penitration',
                           'total_potential_value','actual_sales','target_sales',
                           'market_share_in_account','percentage_territory_potential_sales',
                           'percentage_territory_actual_sales','territory_quota',
                           'territory_quota_attainment']

mendel[cols_num] = mendel[cols_num].apply(pd.to_numeric, errors='coerce', axis=1)

#cols_cat = ['rep_id','health_grp','account_name','account_relation','injection_potential','pal','competitive_situation','clinical_mindset','value_perception']
#converting to date time object and extracting month and weekdays
#mendel.input_timestamp =  pd.to_datetime(mendel.input_timestamp)
#mendel['month'] = mendel['input_timestamp'].dt.month
#mendel['month']= mendel['month'].apply(lambda x: calendar.month_abbr[x])
#mendel['day'] = mendel['input_timestamp'].dt.weekday_name

mendel.info()
#since strings data types have variable length, it is by default stored as object dtype. If you want to store them as string type, you can do something like this.
#cols_cat = ['account_relation','injection_potential','pal','competitive_situation','clinical_mindset','value_perception']

#converting all the categorical values in data frame to lower case
mendel = mendel.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)

#checking for duplicate observations and droping duplicates
dup_med = mendel.duplicated() #will return a sereis of boolean
mendel = mendel.drop_duplicates()

#removing a particular pattern of string in Product_Adoption_Ladder
mendel['pal'] = mendel['pal'].str.split('(').str[0]
mendel['pal'] = mendel['pal'].str.replace(' ', '')
mendel['injection_potential'] = mendel['injection_potential'].str.replace(' ', '')
mendel['competitive_situation'] = mendel['competitive_situation'].str.replace(' ', '')

# Total Number of missing values or NAN in each column & #percentage of missing values each column
mendel.isnull().sum()
round((mendel.isnull().sum()/len(mendel))*100,2)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#outlier treatment for numbneric values with a UDF centile
def centile(mendel,num_var):
    var_quantile =  mendel[num_var].quantile(np.arange(0,1.01,0.01))
    print(var_quantile)
    

def outlier_treatment(num_outlier_treat_var, value):
    mendel[num_outlier_treat_var] = np.where(mendel[num_outlier_treat_var] > value ,value ,mendel[num_outlier_treat_var])
    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#total_potential_value



#outlier treatment & handeling missing values
#set a seaborn style of your taste
sns.set_style("whitegrid")
sns.boxplot(mendel['total_potential_value'])
centile(mendel,'total_potential_value')
outlier_treatment('total_potential_value',600)

#handeling missing values of total_potential_value
mendel["total_potential_value"] = mendel["total_potential_value"].ffill().bfill()
mendel["total_potential_value"].describe()

#target_sales

#outlier treatment & handeling missing values
sns.boxplot(mendel['target_sales'])
centile(mendel,'target_sales')
outlier_treatment('target_sales',165)
mendel["target_sales"].describe()
mendel.isnull().sum()
mendel["target_sales"] = mendel["target_sales"].ffill().bfill()


#actual_sales
#outlier treatment & handeling missing values

sns.boxplot(mendel['actual_sales'])
centile(mendel,'actual_sales')
outlier_treatment('actual_sales',134.00)
mendel["actual_sales"].describe()
mendel["actual_sales"] = mendel["actual_sales"].ffill().bfill()
mendel.isnull().sum()


#competitive_drug_market_penitration
#outlier treatment & handeling missing values

sns.boxplot(mendel['competitive_drug_market_penitration']) #no outlier
centile(mendel,'competitive_drug_market_penitration') #no outlier
mendel["competitive_drug_market_penitration"].describe()
mendel["competitive_drug_market_penitration"] = mendel["competitive_drug_market_penitration"].ffill().bfill()
mendel.isnull().sum()

#patients_treated_with_competitive_drug
#outlier treatment & handeling missing values

sns.boxplot(mendel['patients_treated_with_competitive_drug']) 
centile(mendel,'patients_treated_with_competitive_drug') 
outlier_treatment('patients_treated_with_competitive_drug',225.20)
mendel["patients_treated_with_competitive_drug"].describe()
mendel["patients_treated_with_competitive_drug"] = mendel["patients_treated_with_competitive_drug"].ffill().bfill()
mendel.isnull().sum()

#patients_treated_with_selling_drug
#outlier treatment & handeling missing values

sns.boxplot(mendel['patients_treated_with_selling_drug']) 
centile(mendel,'patients_treated_with_selling_drug') 
outlier_treatment('patients_treated_with_selling_drug',85.60)
mendel["patients_treated_with_selling_drug"].describe()
mendel["patients_treated_with_selling_drug"] = mendel["patients_treated_with_selling_drug"].ffill().bfill()
mendel.isnull().sum()

#accout_relation
##handeling missing values  with mode.

sns.countplot(x= mendel['account_relation'], data = mendel)
((mendel['account_relation'].value_counts())/len(mendel))*100
mendel = mendel.fillna(mendel['account_relation'].value_counts().index[0])
mendel["account_relation"].describe()
#mendel['account_relation'] = mendel.fillna(mendel['account_relation'].ffill().bfill())
mendel.info()
mendel.isnull().sum()


#only outlier check
#market share in account
sns.boxplot(mendel['market_share_in_account']) 
outlier_treatment('market_share_in_account',0.88)
centile(mendel,'market_share_in_account') 
mendel["market_share_in_account"].describe()

#percentage_territory_potential_sales
#sns.boxplot(mendel['percentage_territory_potential_sales']) 
#centile(mendel,'percentage_territory_potential_sales') 
#outlier_treatment('percentage_territory_potential_sales',0.066)
#mendel.isnull().sum()

#percentage_territory_actual_sales
sns.boxplot(mendel['percentage_territory_actual_sales']) 
centile(mendel,'percentage_territory_actual_sales') 
outlier_treatment('percentage_territory_actual_sales',0.068966)
mendel.isnull().sum()

#territory_quota

sns.boxplot(mendel['territory_quota']) 
centile(mendel,'territory_quota') 
outlier_treatment('territory_quota',3200)
mendel.isnull().sum()



#territory_quota_attainment
sns.boxplot(mendel['territory_quota_attainment'])
centile(mendel,'territory_quota_attainment') 
outlier_treatment('territory_quota_attainment',1)
mendel.isnull().sum()

#derived metrics

###selling_drug_market_penitration_in_account <- patients_treated_with_selling_drug/total_potential_value for each account
mendel['selling_drug_market_penitration'] = mendel['patients_treated_with_selling_drug']/mendel['total_potential_value']
mendel['selling_drug_market_penitration'].isnull().sum() #185 Missing values

#outlier tratment and handeling missing values for selling_drug_market_penitration
sns.boxplot(mendel['selling_drug_market_penitration']) 
centile(mendel,'selling_drug_market_penitration')
outlier_treatment('selling_drug_market_penitration',0.397500)
mendel["selling_drug_market_penitration"].describe()
mendel["selling_drug_market_penitration"] = mendel["selling_drug_market_penitration"].ffill().bfill()
mendel.isnull().sum()

#mendel.info()

