# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:47:12 2019
@author: 713538
"""

 
import numpy as np #linear algebra
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import Mendel.mlmodel.Model_data_prep as kda

########## creating master data set for clustering and  derived insightful variables for clustering ########################

mendel_df = pd.DataFrame(kda.mendel)
mendel_df.info()

###1.monetary_actual_sales <- sum of actual sales for each account
monetary_actual_sales =  pd.DataFrame(mendel_df.groupby("account_name").actual_sales.sum())
monetary_actual_sales = monetary_actual_sales.reset_index()

###2.monetary_total_potential_value <- sum of total potential value for each account
monetary_total_potential_value =  pd.DataFrame(mendel_df.groupby("account_name").total_potential_value.sum())
monetary_total_potential_value = monetary_total_potential_value.reset_index()
#mater dataframe for clustering
master = monetary_actual_sales.merge(monetary_total_potential_value, on = "account_name", how = "inner")

###3.total_market_share_in_account <-  sum of total market share for each account
total_market_share_in_account =  pd.DataFrame(mendel_df.groupby("account_name").market_share_in_account.sum())
total_market_share_in_account = total_market_share_in_account.reset_index()
#mater dataframe for clustering
master = master.merge(total_market_share_in_account, on = "account_name", how = "inner")

### 5 & 6. injection_potential & product_adoption_ladder <- Transsform the  those ordinal categorical variables into encoded numeric values

cat_seg_cols = ['account_name','injection_potential','value_perception']
obj_mendel = mendel_df.loc[:,cat_seg_cols]
cleanup_nums = {
                "injection_potential": {"goldmine": 0.24*4, "silvermine": 0.24*3, "bronzemine": 0.24*2, "abandonedmine": 0.24*1 },                
                "value_perception": {"strong":0.06*4, "medium" : 0.06*3, "low": 0.06*2, "weak" : 0.06*1}                
                }
obj_mendel.replace(cleanup_nums, inplace=True)
obj_mendel.info()
#converting to categorical values to account level
for column in obj_mendel.loc[:, obj_mendel.columns != 'account_name']:
     sum_total = pd.DataFrame(obj_mendel.groupby(['account_name'])[column].sum()).reset_index()
     master = master.merge(sum_total, on = "account_name", how = "inner") 


#cheking duplicated acount_names
if len(master['account_name'].unique()) < len(master.index):
    print("Duplicated Account Names Present")
else :
    print("Duplicated Account Names Not Present")

#standadizing with z-score     
final_df = master.drop("account_name", axis=1)
final_df = stats.zscore(final_df)

#===============================================================================
#determining K through : Elbow Method
range_n_clusters = list(range(2,21))
print(range_n_clusters)
# sum of squared distances
ssd = []
for num_clusters in range_n_clusters:
    model_clus = KMeans(n_clusters = num_clusters, max_iter= 63)
    model_clus.fit(final_df)
    ssd.append(model_clus.inertia_)
    
#plt.plot(ssd)   

#===============================================================================  
""" ####determining K through : Silhouette Score Method
===============================================================================
Selecting the number of clusters with silhouette analysis on KMeans clustering
===============================================================================
Silhouette analysis can be used to study the separation distance between the
resulting clusters. The silhouette plot displays a measure of how close each
point in one cluster is to points in the neighboring clusters and thus provides
a way to assess parameters like number of clusters visually. This measure has a
range of [-1, 1].
Silhouette coefficients (as these values are referred to as) near +1 indicate
that the sample is far away from the neighboring clusters. A value of 0
indicates that the sample is on or very close to the decision boundary between
two neighboring clusters and negative values indicate that those samples might
have been assigned to the wrong cluster.
In this example the silhouette analysis is used to choose an optimal value for
``n_clusters``. The silhouette plot shows that the ``n_clusters`` value of 3, 5
and 6 are a bad pick for the given data due to the presence of clusters with
below average silhouette scores and also due to wide fluctuations in the size
of the silhouette plots. Silhouette analysis is more ambivalent in deciding
between 4 and 6.
Also from the thickness of the silhouette plot the cluster size can be
visualized. The silhouette plot for cluster 0 when ``n_clusters`` is equal to
2, is bigger in size owing to the grouping of the 3 sub clusters into one big
cluster. However when the ``n_clusters`` is equal to 4, all the plots are more
or less of similar thickness and hence are of similar sizes as can be also
verified from the labelled scatter plot on the right.
""" 


for n_clusters in range_n_clusters:
    # Create a subplot with 1 row and 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18, 7)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(final_df) + (n_clusters + 1) * 10])

    # Initialize the clusterer with n_clusters value and a random generator
    # seed of 10 for reproducibility.
    clusterer = KMeans(n_clusters=n_clusters, random_state=10)
    cluster_labels = clusterer.fit_predict(final_df)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = silhouette_score(final_df, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(final_df, cluster_labels)

    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    # 2nd Plot showing the actual clusters formed
    colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
    ax2.scatter(final_df[:, 0], final_df[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                c=colors, edgecolor='k')

    # Labeling the clusters
    centers = clusterer.cluster_centers_
    # Draw white circles at cluster centers
    ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
                c="white", alpha=1, s=200, edgecolor='k')

    for i, c in enumerate(centers):
        ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
                    s=50, edgecolor='k')

    ax2.set_title("The visualization of the mendel clustered data.")
    ax2.set_xlabel("Feature space for the x-axis")
    ax2.set_ylabel("Feature space for the y-axis")

    plt.suptitle(("Silhouette analysis for KMeans clustering on mendel data "
                  "with n_clusters = %d" % n_clusters),
                 fontsize=14, fontweight='bold')

#plt.show()

#===============================================================================

#===============================================================================
nr_cltrs = 4
km_model = KMeans(n_clusters = nr_cltrs, max_iter=63)
km_model.fit(final_df)
# analysis of clusters formed
master.index = pd.RangeIndex(len(master.index))
master_km = pd.concat([master, pd.Series(km_model.labels_)], axis=1)
master_km.columns = ['account_name','actual_sales','value_perception','total_potential_value','market_share_in_account','injection_potential', 'cluster_id']

# intialise data of series. 
data = pd.Series(np.arange(0,nr_cltrs,1))  
# Create DataFrame 
mendel_cluster_analysis = pd.DataFrame(data) 
mendel_cluster_analysis.columns = ['cluster_id']
##taking the mean of each columns for each clusters
for column in master_km.iloc[:,1:6]:
     attribute_means = pd.DataFrame(master_km.groupby(['cluster_id'])[column].mean()).reset_index()
     mendel_cluster_analysis = mendel_cluster_analysis.merge(attribute_means, on = "cluster_id", how = "inner") 
    
mendel_cluster_analysis.columns= ['cluster_id','actual_sales_avg','total_potential_value_avg','market_share_in_account_avg','injection_potential_avg','value_perception_avg']
 
def plot_cat(cat_var):  
    sns.set_style("whitegrid")    
    plt.title('Mean Distribution Accros Clusters')
    sns.barplot(x = 'cluster_id', y= cat_var, data= mendel_cluster_analysis) 
    plt.show()


#plot_cat('actual_sales_avg')
#plot_cat('total_potential_value_avg')
#plot_cat('market_share_in_account_avg')
#plot_cat('injection_potential_avg')
#plot_cat('value_perception_avg')


#===============================================================================

#rescaling the medel_cluster_analysis  between 1 to 5 for spyder plot
rescale_clus_analysis = pd.DataFrame(mendel_cluster_analysis)
for column in rescale_clus_analysis.loc[:, rescale_clus_analysis.columns != 'cluster_id']:
     rescale_clus_analysis[column] =  1 + (rescale_clus_analysis[column] - rescale_clus_analysis[column].min()) * 4 / (rescale_clus_analysis[column].max() - rescale_clus_analysis[column].min())
    

#rescale_clus_analysis.to_csv("rescale_clus_analysis.csv", index = False)
#mendel_cluster_analysis.to_csv("mendel_cluster_analysis.csv", index = False)

#radar/spider chart for strength of each cluster     
labels=['actual_sales_avg', 'total_potential_value_avg', 'market_share_in_account_avg', 'injection_potential_avg', 'value_perception_avg']
markers = [0, 1, 2, 3, 4, 5]
str_markers = ["0", "1", "2", "3", "4", "5"]

def radar_graph(name, stats, attribute_labels = labels, plot_markers = markers, plot_str_markers = str_markers):

    labels = np.array(attribute_labels)

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    stats = np.concatenate((stats,[stats[0]]))
    angles = np.concatenate((angles,[angles[0]]))
    fig= plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2)
    ax.fill(angles, stats, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, labels)
    plt.yticks(markers)
    ax.set_title(name)
    ax.grid(True)
    gridlines = ax.yaxis.get_gridlines()
    for gl in gridlines:
        gl.get_path()._interpolation_steps = 5
#   fig.savefig("static/images/%s.png" % name)
    return plt.show()


#radar_graph("Segment One", rescale_clus_analysis.iloc[0,1:]) # cluster_id 0
#radar_graph("Segment Two", rescale_clus_analysis.iloc[1,1:]) # cluster_id 1
#radar_graph("Segment Three", rescale_clus_analysis.iloc[2,1:]) # cluster_id 2
#radar_graph("Segment Four", rescale_clus_analysis.iloc[3,1:]) # cluster_id 3

##===============================================================================  
#"""
#===============================================================================
#Selecting the number of clusters with silhouette analysis on KMeans clustering
#===============================================================================
#Silhouette analysis can be used to study the separation distance between the
#resulting clusters. The silhouette plot displays a measure of how close each
#point in one cluster is to points in the neighboring clusters and thus provides
#a way to assess parameters like number of clusters visually. This measure has a
#range of [-1, 1].
#Silhouette coefficients (as these values are referred to as) near +1 indicate
#that the sample is far away from the neighboring clusters. A value of 0
#indicates that the sample is on or very close to the decision boundary between
#two neighboring clusters and negative values indicate that those samples might
#have been assigned to the wrong cluster.
#In this example the silhouette analysis is used to choose an optimal value for
#``n_clusters``. The silhouette plot shows that the ``n_clusters`` value of 3, 5
#and 6 are a bad pick for the given data due to the presence of clusters with
#below average silhouette scores and also due to wide fluctuations in the size
#of the silhouette plots. Silhouette analysis is more ambivalent in deciding
#between 4 and 6.
#Also from the thickness of the silhouette plot the cluster size can be
#visualized. The silhouette plot for cluster 0 when ``n_clusters`` is equal to
#2, is bigger in size owing to the grouping of the 3 sub clusters into one big
#cluster. However when the ``n_clusters`` is equal to 4, all the plots are more
#or less of similar thickness and hence are of similar sizes as can be also
#verified from the labelled scatter plot on the right.
#""" 
#
#
#for n_clusters in range_n_clusters:
#    # Create a subplot with 1 row and 2 columns
#    fig, (ax1, ax2) = plt.subplots(1, 2)
#    fig.set_size_inches(18, 7)
#
#    # The 1st subplot is the silhouette plot
#    # The silhouette coefficient can range from -1, 1 but in this example all
#    # lie within [-0.1, 1]
#    ax1.set_xlim([-0.1, 1])
#    # The (n_clusters+1)*10 is for inserting blank space between silhouette
#    # plots of individual clusters, to demarcate them clearly.
#    ax1.set_ylim([0, len(final_df) + (n_clusters + 1) * 10])
#
#    # Initialize the clusterer with n_clusters value and a random generator
#    # seed of 10 for reproducibility.
#    clusterer = KMeans(n_clusters=n_clusters, random_state=10)
#    cluster_labels = clusterer.fit_predict(final_df)
#
#    # The silhouette_score gives the average value for all the samples.
#    # This gives a perspective into the density and separation of the formed
#    # clusters
#    silhouette_avg = silhouette_score(final_df, cluster_labels)
#    print("For n_clusters =", n_clusters,
#          "The average silhouette_score is :", silhouette_avg)
#
#    # Compute the silhouette scores for each sample
#    sample_silhouette_values = silhouette_samples(final_df, cluster_labels)
#
#    y_lower = 10
#    for i in range(n_clusters):
#        # Aggregate the silhouette scores for samples belonging to
#        # cluster i, and sort them
#        ith_cluster_silhouette_values = \
#            sample_silhouette_values[cluster_labels == i]
#
#        ith_cluster_silhouette_values.sort()
#
#        size_cluster_i = ith_cluster_silhouette_values.shape[0]
#        y_upper = y_lower + size_cluster_i
#
#        color = cm.nipy_spectral(float(i) / n_clusters)
#        ax1.fill_betweenx(np.arange(y_lower, y_upper),
#                          0, ith_cluster_silhouette_values,
#                          facecolor=color, edgecolor=color, alpha=0.7)
#
#        # Label the silhouette plots with their cluster numbers at the middle
#        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
#
#        # Compute the new y_lower for next plot
#        y_lower = y_upper + 10  # 10 for the 0 samples
#
#    ax1.set_title("The silhouette plot for the various clusters.")
#    ax1.set_xlabel("The silhouette coefficient values")
#    ax1.set_ylabel("Cluster label")
#
#    # The vertical line for average silhouette score of all the values
#    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
#
#    ax1.set_yticks([])  # Clear the yaxis labels / ticks
#    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
#    # 2nd Plot showing the actual clusters formed
#    colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
#    ax2.scatter(final_df[:, 0], final_df[:, 1], marker='.', s=30, lw=0, alpha=0.7,
#                c=colors, edgecolor='k')
#
#    # Labeling the clusters
#    centers = clusterer.cluster_centers_
#    # Draw white circles at cluster centers
#    ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
#                c="white", alpha=1, s=200, edgecolor='k')
#
#    for i, c in enumerate(centers):
#        ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
#                    s=50, edgecolor='k')
#
#    ax2.set_title("The visualization of the mendel clustered data.")
#    ax2.set_xlabel("Feature space for the x-axis")
#    ax2.set_ylabel("Feature space for the y-axis")
#
#    plt.suptitle(("Silhouette analysis for KMeans clustering on mendel data "
#                  "with n_clusters = %d" % n_clusters),
#                 fontsize=14, fontweight='bold')
#
#plt.show()
#
##===============================================================================

####determining K through : Silhouette Score Method
#for n_clusters in range_n_clusters:
#    #  Apply your clustering algorithm of choice to the reduced data 
#    clusterer = KMeans(n_clusters = n_clusters).fit(final_df)
#    #  Predict the cluster for each data point
#    preds = clusterer.predict(final_df)
#    #  Find the cluster centers
#    centers = clusterer.cluster_centers_
#    #  Calculate the mean silhouette coefficient for the number of clusters chosen
#    score = silhouette_score(final_df, preds, metric='euclidean')
#    print ("For n_clusters = {}. The average silhouette_score is : {}".format(n_clusters, score))    
#
#

#===============================================================================

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
###6.injection_potential <- get dummies then total count of each category for every account
#Transsform the categorical variables  to dummies
#col_cat_seg = ['account_name','account_relation','injection_potential','pal','competitive_situation']
#obj_mendel = mendel_df.loc[:,col_cat_seg]
#
#cleanup_nums = {"account_relation":     {"strong": 4, "medium": 3, "low":2 , "weak" : 1},
#                "injection_potential": {"gold mine": 4, "silver mine": 3, "bronze mine": 2, "abandoned mine": 1 },
#                "pal" : {"loyalist \n": 4, "mixed user": 3, "trialist" : 2, "pro-competitor " : 1},
#                "competitive_situation" : {"highly ethical" :4 , "somewhat ethical": 3 , "low ethics" : 2, "no ethics": 1}
#                }
#
#obj_mendel.replace(cleanup_nums, inplace=True)
#obj_mendel.head()
                
                
#cat_mendel_seg_dummy = pd.get_dummies(cat_mendel_seg,drop_first=True)
#cat_seg = pd.concat([mendel_df['account_name'],cat_mendel_seg_dummy],axis=1)


##converting to categorical values to account level
#for column in cat_seg.loc[:, cat_seg.columns != 'account_name']:
#     count_sum = pd.DataFrame(cat_seg.groupby(['account_name'])[column].sum()).reset_index()
#     master = master.merge(count_sum, on = "account_name", how = "inner") 

#master = master.merge(obj_mendel, on = "account_name", how = "inner") 
####4.competitive_drug_market_penitration_in_account <- patients_treated_with_competitive_drug/total_potential_value for each account
#competitive_drug_market_penitration_in_account = pd.DataFrame(mendel_df.groupby("account_name").competitive_drug_market_penitration.sum())
#competitive_drug_market_penitration_in_account =  competitive_drug_market_penitration_in_account.reset_index()
##mater dataframe for clustering
#master = master.merge(competitive_drug_market_penitration_in_account, on = "account_name", how = "inner")
#
####5.selling_drug_market_penitration_in_account <- patients_treated_with_selling_drug/total_potential_value for each account
#mendel_df['selling_drug_market_penitration'] = mendel_df['patients_treated_with_selling_drug']/mendel_df['total_potential_value']
#mendel_df['selling_drug_market_penitration'].isnull().sum() #185 Missing values
#
##outlier tratment and handeling missing values for selling_drug_market_penitration
#sns.boxplot(mendel_df['selling_drug_market_penitration']) 
#kda.centile(mendel_df,'selling_drug_market_penitration')
#kda.outlier_treatment('selling_drug_market_penitration',0.35)
#mendel_df["selling_drug_market_penitration"].describe()
#mendel_df["selling_drug_market_penitration"] = mendel_df["selling_drug_market_penitration"].ffill().bfill()
#mendel_df.isnull().sum()

##selling_drug_market_penitration_in_account
#selling_drug_market_penitration_in_account = pd.DataFrame(mendel_df.groupby("account_name").selling_drug_market_penitration.sum())
#selling_drug_market_penitration_in_account =  selling_drug_market_penitration_in_account.reset_index()
##mater dataframe for clustering
#master = master.merge(selling_drug_market_penitration_in_account, on = "account_name", how = "inner")
#features = ['actual_sales','total_potential_value','market_share_in_account','competitive_drug_market_penitration','selling_drug_market_penitration']
#final_df = master.loc[:,features]
#from math import pi
#from sklearn.preprocessing import StandardScaler
#standard_scaler = StandardScaler()
#final_df = standard_scaler.fit_transform(master) 
#def make_spider( row, title, color):
#     #number of variable
#     categories=list(df)[1:]
#     N = len(categories)
#     # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
#     angles = [n / float(N) * 2 * pi for n in range(N)]
#     angles += angles[:1]
#     # Initialise the spider plot
#     ax = plt.subplot(2,2,row+1, polar=True, ) 
#     #If you want the first axis to be on top:
#     ax.set_theta_offset(pi / 2)
#     ax.set_theta_direction(-1) 
#     #Draw one axe per variable + add labels labels yet
#     plt.xticks(angles[:-1], categories, color='grey', size=8)
#     # Draw ylabels
#     ax.set_rlabel_position(0)
#     plt.yticks([10,20,30], ["10","20","30"], color="grey", size=7)
#     plt.ylim(0,40)
#     # Ind1
#     values=df.loc[row].drop('group').values.flatten().tolist()
#     values += values[:1]
#     ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
#     ax.fill(angles, values, color=color, alpha=0.4)
#     #Add a title
#     plt.title(title, size=11, color=color, y=1.1)
#     # ------- PART 2: Apply to all individuals
#     # initialize the figure
#     my_dpi=96
#     plt.figure(figsize=(1000/my_dpi, 1000/my_dpi), dpi=my_dpi) 
#     # Create a color palette:
#     my_palette = plt.cm.get_cmap("Set2", len(df.index))
#     # Loop to plot
#     for row in range(0, len(df.index)):
#         make_spider( row=row, title='group '+df['group'][row], color= my_palette(row))
#         
#    
# 
#make_spider(2,"the spider","grey")

#
## Libraries
#import matplotlib.pyplot as plt
#import pandas as pd
#from math import pi
# 
## Set data
#df = pd.DataFrame({
#'group': ['Segment One','Segment Two','Segment Three','Segment Four'],
#'var1': [38, 1.5, 30, 4],
#'var2': [29, 10, 9, 34],
#'var3': [8, 39, 23, 24],
#'var4': [7, 31, 33, 14],
#'var5': [28, 15, 32, 14]
#})
# 
#cleanup_nums_prop = {"account_relation":{"strong": 0.14*4, "medium": 0.14*3, "low": 0.14*2 , "weak" : 0.14*1},
#                "injection_potential": {"goldmine": 0.24*4, "silvermine": 0.24*3, "bronzemine": 0.24*2, "abandonedmine": 0.24*1 },
#                "pal" : {"loyalist\n":  0.22*4, "mixeduser":  0.22*3, "trialist" :  0.22*2, "pro-competitor" :  0.22*1},
#                "competitive_situation" : {"highlyethical" : 0.28*4 , "somewhatethical":  0.28*3 , "lowethics" :  0.28*2, "noethics":  0.28*1},
#                "clinical_mindset" : { "advocate" : 0.06*4, "neutral" : 0.06*3, "skeptical" : 0.06*3, "pro-prp" : 0.06*1 },
#                "value_perception": {"strong":0.06*4, "medium" : 0.06*3, "low": 0.06*2, "weak" : 0.06*1}
#                }
#