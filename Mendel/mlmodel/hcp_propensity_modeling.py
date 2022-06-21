# -*- coding: utf-8 -*-
"""
Created on Thu May 16 11:24:22 2019
@author: 713538
"""

import numpy as np #linear algebra
import pandas as pd #import pandas
import matplotlib.pyplot as plt #eda
#import seaborn as sns # the commonly used alias for seaborn is sns
from sklearn.model_selection import train_test_split
from scipy import stats
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.feature_selection import RFECV
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
import Mendel.mlmodel.hcp_clustering_segmentation as cls


mendel_propensity = pd.DataFrame(cls.mendel_df)
mendel_propensity.info()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#outlier treatment for numbneric values with a UDF centile
def centile(mendel_propensity,num_var):
    var_quantile =  mendel_propensity[num_var].quantile(np.arange(0,1.01,0.01))
    #print(var_quantile)
    

def outlier_treatment(num_outlier_treat_var, value):
    mendel_propensity[num_outlier_treat_var] = np.where(mendel_propensity[num_outlier_treat_var] > value ,value ,mendel_propensity[num_outlier_treat_var])
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------


###1.monetary_actual_sales <- sum of actual sales for each account
monetary_actual_sales =  pd.DataFrame(mendel_propensity.groupby("account_name").actual_sales.sum()).reset_index()

###2.monetary_total_potential_value <- sum of total potential value for each account
monetary_total_potential_value =  pd.DataFrame(mendel_propensity.groupby("account_name").total_potential_value.sum()).reset_index()
#mater dataframe for clustering
propensity = monetary_actual_sales.merge(monetary_total_potential_value, on = "account_name", how = "inner")

###3.total_market_share_in_account <-  sum of total market share for each account
total_market_share_in_account =  pd.DataFrame(mendel_propensity.groupby("account_name").market_share_in_account.sum()).reset_index()
#mater dataframe for clustering
propensity = propensity.merge(total_market_share_in_account, on = "account_name", how = "inner")

####4.competitive_drug_market_penitration_in_account <- patients_treated_with_competitive_drug/total_potential_value for each account
competitive_drug_market_penitration_in_account = pd.DataFrame(mendel_propensity.groupby("account_name").competitive_drug_market_penitration.sum()).reset_index()
#mater dataframe for clustering
propensity = propensity.merge(competitive_drug_market_penitration_in_account, on = "account_name", how = "inner")

###5.selling_drug_market_penitration_in_account <- patients_treated_with_selling_drug/total_potential_value for each account
selling_drug_market_penitration_in_account = pd.DataFrame(mendel_propensity.groupby("account_name").selling_drug_market_penitration.sum())
selling_drug_market_penitration_in_account =  selling_drug_market_penitration_in_account.reset_index()
#mater dataframe for clustering
propensity = propensity.merge(selling_drug_market_penitration_in_account, on = "account_name", how = "inner")


###6.patients_treated_with_selling_drug <-  sum of total patients treated with selling drug for each account
patients_treated_with_selling_drug =  pd.DataFrame(mendel_propensity.groupby("account_name").patients_treated_with_selling_drug.sum()).reset_index()
#mater dataframe for clustering
propensity = propensity.merge(patients_treated_with_selling_drug, on = "account_name", how = "inner")


###7.patients_treated_with_competitive_drug <-  sum of total patients treated with competitive drug for each account
patients_treated_with_competitive_drug =  pd.DataFrame(mendel_propensity.groupby("account_name").patients_treated_with_competitive_drug.sum()).reset_index()
#mater dataframe for clustering
propensity = propensity.merge(patients_treated_with_competitive_drug, on = "account_name", how = "inner")


###8.monetary_target_sales <- sum of actual sales for each account
monetary_target_sales =  pd.DataFrame(mendel_propensity.groupby("account_name").target_sales.sum()).reset_index()
propensity = propensity.merge(monetary_target_sales, on = "account_name", how = "inner")



cleanup_nums_prop = {"account_relation":{"strong": 0.14*4, "medium": 0.14*3, "low": 0.14*2 , "weak" : 0.14*1},
                "injection_potential": {"goldmine": 0.24*4, "silvermine": 0.24*3, "bronzemine": 0.24*2, "abandonedmine": 0.24*1 },
                "pal" : {"loyalist\n":  0.22*4, "mixeduser":  0.22*3, "trialist" :  0.22*2, "pro-competitor" :  0.22*1},
                "competitive_situation" : {"highlyethical" : 0.28*4 , "somewhatethical":  0.28*3 , "lowethics" :  0.28*2, "noethics":  0.28*1},
                "clinical_mindset" : { "advocate" : 0.06*4, "neutral" : 0.06*3, "skeptical" : 0.06*3, "pro-prp" : 0.06*1 },
                "value_perception": {"strong":0.06*4, "medium" : 0.06*3, "low": 0.06*2, "weak" : 0.06*1}
                }

### 8. onwards. injection_potential & product_adoption_ladder <- Transsform the  those ordinal categorical variables into encoded numeric values
cat_prop_cols = ['account_name', 'account_relation','injection_potential','pal','competitive_situation','clinical_mindset','value_perception']

obj_mendel_prop = mendel_propensity.loc[:,cat_prop_cols]
obj_mendel_prop.replace(cleanup_nums_prop, inplace=True)

obj_mendel_prop.info()

#converting to categorical values to account level
for column in obj_mendel_prop.loc[:, obj_mendel_prop.columns != 'account_name']:
    df =  pd.DataFrame(obj_mendel_prop.groupby(['account_name'])[column].mean()).reset_index()
    propensity = propensity.merge(df, on = "account_name", how = "inner")

    
#######################
##propensity.to_csv("D://propensity.csv")

propensity_rescale= pd.DataFrame(propensity)

for column in propensity_rescale.loc[:, propensity_rescale.columns != 'account_name']:
     propensity_rescale[column] =  1 + (propensity_rescale[column] - propensity_rescale[column].min()) * 9 / (propensity_rescale[column].max() - propensity_rescale[column].min())


###### create  adependent variable response for propensity score #############    
def response_func(row):
    if row['actual_sales'] > 0.95*row['target_sales']:
        val = 1   
    else:
        val = 0
    return val    

propensity['response'] = propensity.apply(response_func, axis=1)
response_rate = propensity['response'].sum()/len(propensity.index)
#droping actual sales and target sales
score = propensity.drop(['actual_sales','target_sales','account_relation','injection_potential','pal',
                         'competitive_situation','clinical_mindset','value_perception'],axis = 1)

score.info()
score.isnull().sum()
#--------------------------------------------------------------

#9.acoount_relation
mode = mendel_propensity.groupby(['account_name'])['account_relation'].agg(
    lambda x: pd.Series.mode(x)[0]).to_frame().reset_index()
score = score.merge(mode, on = "account_name", how = "inner")

#10.injection_potential
mode = mendel_propensity.groupby(['account_name'])['injection_potential'].agg(
    lambda x: pd.Series.mode(x)[0]).to_frame().reset_index()
score = score.merge(mode, on = "account_name", how = "inner")

#11.pal
mode = mendel_propensity.groupby(['account_name'])['pal'].agg(
    lambda x: pd.Series.mode(x)[0]).to_frame().reset_index()
score = score.merge(mode, on = "account_name", how = "inner")

#12.competitive_situation
mode = mendel_propensity.groupby(['account_name'])['competitive_situation'].agg(
    lambda x: pd.Series.mode(x)[0]).to_frame().reset_index()
score = score.merge(mode, on = "account_name", how = "inner")

#13.clinical_mindset
mode = mendel_propensity.groupby(['account_name'])['clinical_mindset'].agg(
    lambda x: pd.Series.mode(x)[0]).to_frame().reset_index()
score = score.merge(mode, on = "account_name", how = "inner")

#14.value_perception
mode = mendel_propensity.groupby(['account_name'])['value_perception'].agg(
    lambda x: pd.Series.mode(x)[0]).to_frame().reset_index()
score = score.merge(mode, on = "account_name", how = "inner")

score.info()
score.isnull().sum()

#-------------------------------------------------------------------------------------------------------

############# Scaling , Sampling and Dummy variables creation and feature selection for model#####################################
#selecting numerics columns only after judging from EDA which are looks significant
cols_num_scaled = ['patients_treated_with_competitive_drug','patients_treated_with_selling_drug',
                        'competitive_drug_market_penitration','total_potential_value',
                    'market_share_in_account','selling_drug_market_penitration' ]

num_score = score.loc[:,cols_num_scaled]
# Normalizing and standadization of numeric variables
num_score = pd.DataFrame(stats.zscore(num_score))
num_score.columns = ['patients_treated_with_competitive_drug','patients_treated_with_selling_drug',
                        'competitive_drug_market_penitration','total_potential_value',
                    'market_share_in_account','selling_drug_market_penitration' ]
#selecting catgorical  variables
cols_cat = ['account_relation','injection_potential','pal','competitive_situation','clinical_mindset','value_perception']
cat_score = score.loc[:,cols_cat]
#Creating dummy varibles for categorical variables
# we can use drop_first = True to drop the first column from dummy dataframe.
cat_score_dummy = pd.get_dummies(cat_score,drop_first=True)

#creating the final data set which wre going to throw to the model
#adding dummy data frames of categorical varibles and normilized data frames of numeric varibles
score_final_df = pd.concat([cat_score_dummy,num_score,score['response']],axis=1)
score_final_df.info()

#spliting the data set into test and train
#random_state is the seed used by the random number generator, it can be any integer.
# Putting feature variables to X
X = score_final_df.loc[:, score_final_df.columns !='response' ]
# Putting dependent or response  variable to y
y = score_final_df['response']
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7 ,test_size = 0.3, random_state= 81)


###################### Model Building ############################
# Logistic regression model
##Adding a constant column to our dataframe
logm_1 = sm.GLM(y_train,(sm.add_constant(X_train)), family = sm.families.Binomial())
logm_1.fit().summary()

logr = LogisticRegression()
rfe_cv = RFECV(logr, step= 1 , cv = 5)
rfe_cv = rfe_cv.fit(X_train, y_train)

#print(rfe_cv.support_)                      # Printing the boolean results
#print(rfe_cv.ranking_)  
#print(rfe_cv.n_features_)
rfe_cv.grid_scores_


# Creating X_test dataframe with RFECV selected variables
col_rfe_cv = X_train.columns[rfe_cv.support_]
X_train_rfe_cv = X_train[col_rfe_cv]
#print(col_rfe_cv)


#Adding a constant column to our dataframe
X_train_rfe_cv = sm.add_constant(X_train_rfe_cv)   
# create a first fitted model
#model 1
logm_1 = sm.GLM(y_train,X_train_rfe_cv, family = sm.families.Binomial())
#Let's see the summary of our first linear model
logm_1.fit().summary()

#--------------------------------------------------------------------------------------------------
# UDF for calculating vif value
def vif_cal(input_data, dependent_col):
    vif_df = pd.DataFrame( columns = ['Var', 'Vif'])
    x_vars=input_data.drop([dependent_col], axis=1)
    xvar_names=x_vars.columns
    for i in range(0,xvar_names.shape[0]):
        y=x_vars[xvar_names[i]] 
        x=x_vars[xvar_names.drop(xvar_names[i])]
        rsq=sm.OLS(y,x).fit().rsquared  
        vif=round(1/(1-rsq),2)
        vif_df.loc[i] = [xvar_names[i], vif]
    return vif_df.sort_values(by = 'Vif', axis=0, ascending=False, inplace=False)



df_rfe_cv =  pd.concat([X_train_rfe_cv, y_train], axis = 1)
df_rfe_cv.info()

#----------------------------------------------------------------------------------------------------


#we are droping the constant bcz we have added constant for stat models.bcz stat models doesnot automatically add a consatnt.
vif_cal(input_data= df_rfe_cv.drop(["const"], axis=1) ,  dependent_col = "response")
# For all of the selected vaiables VIF is within 3 so no need to eliminate. based on VIF

logm_1.fit().summary()

#droping 'competitive_situation_noethics'
X_train_rfe_cv = X_train_rfe_cv.drop('competitive_situation_noethics', axis = 1)

#model 2
logm_2 = sm.GLM(y_train,X_train_rfe_cv, family = sm.families.Binomial())
logm_2.fit().summary()


#droping 'value_perception_strong'
X_train_rfe_cv = X_train_rfe_cv.drop('value_perception_strong', axis = 1)

#model 3
logm_3 = sm.GLM(y_train,X_train_rfe_cv, family = sm.families.Binomial())
logm_3.fit().summary()

#droping 'clinical_mindset_skeptical'
#X_train_rfe_cv = X_train_rfe_cv.drop('clinical_mindset_skeptical', axis = 1)

#model 4
logm_4 = sm.GLM(y_train,X_train_rfe_cv, family = sm.families.Binomial())
logm_4.fit().summary()

#droping 'pal_trialist'
X_train_rfe_cv = X_train_rfe_cv.drop('pal_trialist', axis = 1)

#model 5

logm_5 = sm.GLM(y_train,X_train_rfe_cv, family = sm.families.Binomial())
logm_5.fit().summary()

#droping 'account_relation_weak'
X_train_rfe_cv = X_train_rfe_cv.drop('account_relation_weak', axis = 1)

#model 6
logm_6 = sm.GLM(y_train,X_train_rfe_cv, family = sm.families.Binomial())
logm_6.fit().summary()


#droping 'injection_potential_goldmine'
X_train_rfe_cv = X_train_rfe_cv.drop('injection_potential_goldmine', axis = 1)
#model 7
logm_7 = sm.GLM(y_train,X_train_rfe_cv, family = sm.families.Binomial())
logm_7.fit().summary()


#droping 'clinical_mindset_pro-prp'
X_train_rfe_cv = X_train_rfe_cv.drop('clinical_mindset_pro-prp', axis = 1)
#model 8
logm_8 = sm.GLM(y_train,X_train_rfe_cv, family = sm.families.Binomial())
logm_8.fit().summary()


#droping 'patients_treated_with_competitive_drug'
X_train_rfe_cv = X_train_rfe_cv.drop('patients_treated_with_competitive_drug', axis = 1)
#model 9
final_model = sm.GLM(y_train,X_train_rfe_cv, family = sm.families.Binomial())
final_model.fit().summary()


############ Making Prediction ##################

# Now let's use our model to make predictions.
# Creating X_test_rfe_cv dataframe by dropping variables from X_test
# Let's run the model using the selected variables with sklearn
logsk = LogisticRegression()
X_train_rfe_cv = X_train_rfe_cv.drop('const', axis = 1)
logsk.fit(X_train_rfe_cv, y_train)

X_test_rfe_cv = X_test[col_rfe_cv]
X_test_rfe_cv = X_test_rfe_cv.drop(["competitive_situation_noethics","patients_treated_with_competitive_drug",
                                    "clinical_mindset_pro-prp","injection_potential_goldmine",
                                    "account_relation_weak","pal_trialist",
                                    
                                    "value_perception_strong"], axis = 1)

# Predicted probabilities
y_pred = logsk.predict_proba(X_test_rfe_cv)
#print(y_pred)

#y_pred.info()
# Converting y_pred to a dataframe which is an array
y_pred = pd.DataFrame(y_pred)
# Converting to column dataframe
y_pred_1 = y_pred.iloc[:,[1]]

# Let's see the head
y_pred_1.head()

# Converting y_test to dataframe
y_test = pd.DataFrame(y_test)

# Removing index for both dataframes to append them side by side 
y_pred_1.reset_index(drop=True, inplace=True)
y_test.reset_index(drop=True, inplace=True)
# Appending y_test and y_pred_1
y_pred_final = pd.concat([y_test,y_pred_1],axis=1)

# Renaming the column 
y_pred_final= y_pred_final.rename(columns={ 1 : 'response_prob'})

# Creating new column 'predicted' with 1 if response_prob>0.5 else 0
y_pred_final['predicted'] = y_pred_final.response_prob.map( lambda x: 1 if x > 0.5 else 0)

# Let's see the head
y_pred_final.head()




######################### Model Evaluation #########################
#help(metrics.confusion_matrix)
# Confusion matrix 
confusion = metrics.confusion_matrix( y_pred_final.response, y_pred_final.predicted )
confusion

                          #Predicted: not_responded   predicted : responded
# Actual :   # not_responded            59                  6                      precision:  TPR = TP/TP+FP
# Actual :   # responded                15                  10                      TNR = TN/TN+FN, FPR = 1 - TNR




#Let's check the overall accuracy.
metrics.accuracy_score( y_pred_final.response, y_pred_final.predicted)
TN = confusion[0,0] # true Negatives 
TP = confusion[1,1] # true positives
FP = confusion[0,1] # false positives
FN = confusion[1,0] # false negatives


# Let's see the sensitivity of our logistic regression model
TP / float(TP+FN) 

#  calculate specificity
TN / float(TN+FP) 

# positive predictive value : precision
#print (TP / float(TP+FP))

# Negative predictive value
#print (TN / float(TN+ FN))



###############ROC Curve #################################

#An ROC curve demonstrates several things:
#It shows the tradeoff between sensitivity and specificity (any increase in sensitivity will be accompanied by a decrease in specificity).
#The closer the curve follows the left-hand border and then the top border of the ROC space, the more accurate the test.
#The closer the curve comes to the 45-degree diagonal of the ROC space, the less accurate the test.

def draw_roc( actual, probs ):
    fpr, tpr, thresholds = metrics.roc_curve( actual, probs,
                                              drop_intermediate = False )
    auc_score = metrics.roc_auc_score( actual, probs )
    plt.figure(figsize=(6, 4))
    plt.plot( fpr, tpr, label='ROC curve (area = %0.2f)' % auc_score )
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate or [1 - True Negative Rate]')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

    return fpr, tpr, thresholds


#draw_roc(y_pred_final.response, y_pred_final.predicted)

#####Finding Optimal Cutoff Point################

######Optimal cutoff probability is that prob where we get balanced sensitivity and specificity


# Let's create columns with different probability cutoffs 
numbers = [float(x)/10 for x in range(10)]
for i in numbers:
    y_pred_final[i]= y_pred_final.response_prob.map( lambda x: 1 if x > i else 0)
y_pred_final.head()


# Now let's calculate accuracy sensitivity and specificity for various probability cutoffs.
cutoff_df = pd.DataFrame( columns = ['prob','accuracy','sensi','speci'])
num = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
for i in num:
    cm1 = metrics.confusion_matrix( y_pred_final.response, y_pred_final[i] )
    total1=sum(sum(cm1))
    accuracy = (cm1[0,0]+cm1[1,1])/total1
    speci = cm1[0,0]/(cm1[0,0]+cm1[0,1])
    sensi = cm1[1,1]/(cm1[1,0]+cm1[1,1])
    cutoff_df.loc[i] =[ i ,accuracy,sensi,speci]
#print(cutoff_df)



# Let's plot accuracy sensitivity and specificity for various probabilities.
#cutoff_df.plot.line(x='prob', y=['accuracy','sensi','speci'])

#from the curve above prob = 0.33 is the Optimal cutoff probability

y_pred_final['final_predicted'] = y_pred_final.response_prob.map( lambda x: 1 if x > 0.33 else 0)

y_pred_final.head()

#final accuracy
#Let's check the overall accuracy. #final accuracy 0.9033816425120773
metrics.accuracy_score( y_pred_final.response, y_pred_final.final_predicted) 
metrics.confusion_matrix( y_pred_final.response, y_pred_final.final_predicted)
#draw_roc(y_pred_final.response, y_pred_final.final_predicted)
roc_auc_score(y_pred_final.response, y_pred_final.final_predicted) 

auc = 0.7261538461538461 #getting from the auc curve
#print(2*auc -1) #gini score : 0.4523076923076923

#print(classification_report(y_pred_final.response, y_pred_final.final_predicted))

#             precision    recall  f1-score   support

#         0       0.88      0.69      0.78        65
#         1       0.49      0.76      0.59        25

#avg / total       0.77      0.71      0.73        90

#---------------------------------------------------------------------------------------------
##predict the propensity score for each HCP's for the selling drug
#-----------------------------------------------------------------------------------------------

score_rfe_cv = score_final_df[col_rfe_cv]
score_rfe_cv = score_rfe_cv.drop(["competitive_situation_noethics","patients_treated_with_competitive_drug",
                                    "clinical_mindset_pro-prp","injection_potential_goldmine",
                                    "account_relation_weak","pal_trialist",
                                 
                                    "value_perception_strong"], axis = 1)
# Predicted probabilities
response_score = logsk.predict_proba(score_rfe_cv)
#print(response_score)
# Converting hcp_score to a dataframe which is an array
response_score = pd.DataFrame(response_score)
# Converting to column dataframe
response_score_1 = response_score.iloc[:,[1]]
hcp_propensity_score = pd.concat([score['account_name'],response_score_1],axis=1)
hcp_propensity_score.columns = ['account_name', 'selling_drug_propensity_score']
hcp_propensity_score['selling_drug_propensity_score'] = hcp_propensity_score['selling_drug_propensity_score'] * 1000
#hcp_propensity_score.to_csv("Mendel/static/data/hcp_propensity_score.csv", index = False)

#-------------------------------------------------------------------------------------------------------------
########### GBM Classifier with Hyper parameters tuned by GridSearchCV #########
#--------------------------------------------------------------------------------------------------------------

#from sklearn.model_selection import GridSearchCV
#from sklearn.model_selection import cross_validate















