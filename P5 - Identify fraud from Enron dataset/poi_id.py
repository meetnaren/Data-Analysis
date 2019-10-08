#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")
import pprint
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

def explore_data(dataset):
    '''
    Explores the data to display a variety of characteristics of the input dataset
    Inputs: dataset in the form of dictionary with each key representing an executive from the Enron dataset
    returns: None
    '''
    n_records=len(dataset)
    n_poi=sum([int(dataset[person]['poi']) for person in dataset])
    all_features=dataset[dataset.keys()[0]].keys()
    n_features=len(all_features)

    NaNs=0
    for person in dataset:
        for feature in dataset[person]:
            if dataset[person][feature]=='NaN':
                NaNs+=1

    NaNcounts={}
    for person in dataset:
        temp_nan_count=0
        for feature in dataset[person]:
            if dataset[person][feature]=='NaN':
                temp_nan_count+=1
        NaNcounts[person]=temp_nan_count

    featureNaNs={}
    for person in dataset:
        for feature in dataset[person]:
            if dataset[person][feature]=='NaN':
                featureNaNs[feature]=featureNaNs.get(feature,0)+1

    for feature in featureNaNs:
        featureNaNs[feature] = featureNaNs[feature]*1./n_records
    
    print "No. of records in the dataset:",n_records
    print "No. of POIs in the dataset:", n_poi
    print "Proportion of POIs in the dataset:", n_poi * 1./n_records
    print "No. of features in the dataset:", n_features
    print "The features are:"
    pprint.pprint(all_features)

    print "Total number of data points in the dataset:", n_records * n_features 
    print "Total number of missing data points in the dataset:",NaNs
    print "Proportion of missing data in the dataset:", n_records * n_features *1. / NaNs
    print 'These are the top 10 persons with missing data:'
    pprint.pprint(sorted(NaNcounts.items(), key=lambda x:x[1], reverse=True)[:10])
    print 'These are the top 10 features with missing data:'
    pprint.pprint(sorted(featureNaNs.items(), key=lambda x:x[1], reverse=True)[:10])

    return None

def scatterPlot(x,y,dataset,plotfilename):
    '''
    Creates a scatterplot based on the dataset and the x and y variables passed. x and y must be numeric columns in the dataset.
    Inputs:
    x - The variable to plot on the X-axis
    y - The variable to plot on the Y-axis
    dataset - the dataset containing the X and Y variables
    returns: None
    '''
    
    names=dataset.keys()
    xlist=[]
    ylist=[]

    for person in dataset:
        xlist.append(my_dataset[person][x])
        ylist.append(my_dataset[person][y])

    nameSeries=pd.Series(names,name='name')
    xSeries=pd.to_numeric(pd.Series(xlist,name=x), errors='coerce')
    ySeries=pd.to_numeric(pd.Series(ylist,name=y), errors='coerce')

    trace=go.Scatter(
        x=xSeries,
        y=ySeries,
        text=nameSeries,
        mode='markers'
        )

    layout=go.Layout(
        title=x+' and '+y+' of key Enron executives',
        xaxis=dict(title=x),
        yaxis=dict(title=y)
        )

    fig = go.Figure(data=[trace], layout=layout)
    plot(fig, filename=plotfilename)
    return None

def remove_outliers(dataset):
    '''
    Takes as input the dataset and removes the following outlier records:
    1) TOTAL is an outlier as we deduced from the scatterplot
    2) EUGENE LOCKHART does not have any information in the dataset. All columns are NaN
    3) THE TRAVEL AGENCY IN THE PARK is not a real person and can be removed
    '''
    dataset.pop('TOTAL')
    dataset.pop('LOCKHART EUGENE E')
    dataset.pop('THE TRAVEL AGENCY IN THE PARK')
    return dataset

def create_new_features(dataset):
    '''
    Takes as input the dataset and creates 3 new features:
    1) Bonus-to-salary ratio
    2) Proportion of emails received from POIs
    3) Proportion of emails sent to POIs
    '''
    for person in dataset:
        record    = dataset[person]
        
        bonus     = record['bonus']
        salary    = record['salary']
        topoi     = record['from_this_person_to_poi']
        frompoi   = record['from_poi_to_this_person']
        fromcount = record['from_messages']
        tocount   = record['to_messages']

        if bonus!='NaN' and salary!='NaN':
            record['bonus_to_salary'] = bonus * 1. / salary
        else:
            record['bonus_to_salary']=0

        if fromcount!='NaN' and topoi!='NaN':
            record['to_poi_ratio'] = topoi * 1. / fromcount
        else:
            record['to_poi_ratio'] = 0

        if tocount!='NaN' and frompoi!='NaN':
            record['from_poi_ratio'] = frompoi * 1. / tocount
        else:
            record['from_poi_ratio'] = 0

    return dataset

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Store to my_dataset for easy export below.
my_dataset = data_dict

explore_data(my_dataset)

scatterPlot('salary', 'bonus', my_dataset, 'Bonus+Salary1.html')

my_dataset=remove_outliers(my_dataset)

scatterPlot('salary', 'bonus', my_dataset, 'Bonus+Salary2.html')

my_dataset=create_new_features(my_dataset)

### Extract features and labels from dataset for local testing
all_features=my_dataset[my_dataset.keys()[0]].keys()
all_features.pop(all_features.index('poi'))
all_features.pop(all_features.index('email_address'))
features_list=['poi'] + all_features[:]
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

#Building a pipeline and searching hyperparameters
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, make_scorer

'''
#Model Selection through exhaustive grid search
#Exhaustive grid search to find the best classifier and parameters
#The grid search took more than 14 hours to complete!
#The results from the grid search are available in 'GridSearch results.txt'

classifiers=[{'name'  :'Support Vector Machine',
              'model' :SVC(),
              'params': {'clf__C':[0.1, 1, 10, 100]}},
             {'name'  :'Decision Tree',
              'model' :DecisionTreeClassifier(),
              'params':{'clf__min_samples_split':[2, 5, 10, 15, 20]}},
             {'name'  :'Random Forest',
              'model' :RandomForestClassifier(),
              'params':{'clf__min_samples_split':[2, 5, 10, 15, 20], 'clf__n_estimators':range(2, 21, 2)}},
             {'name'  :'Naive Bayes',
              'model' :GaussianNB(),
              'params':{}},
             {'name'  :'Logistic Regression',
              'model' :LogisticRegression(),
              'params':{'clf__class_weight':['balanced']}},
             {'name'  :'K Nearest Neighbors',
              'model' :KNeighborsClassifier(),
              'params':{'clf__n_neighbors':range(2,11)}},
             {'name'  :'Neural Network',
              'model' :MLPClassifier(),
              'params':{'clf__hidden_layer_sizes':[(50, 25, 10, 5), (25, 10, 5), (10, 5)], 'clf__solver':['lbfgs', 'sgd', 'adam']}}]

KBest_params={'dim_reduction__k':range(5,16)}

scoring = {'Precision':make_scorer(precision_score),
           'Recall':make_scorer(recall_score),
           'F1':make_scorer(f1_score)}


for clf in classifiers:
    cv=StratifiedShuffleSplit(labels, 1000, random_state=42)
    
    pipe = Pipeline([('scaling', MinMaxScaler()),
                     ('dim_reduction', SelectKBest(score_func=chi2)),
                     ('clf', clf['model'])])
    params=clf['params']
    params.update(KBest_params)
    
    grid_search = GridSearchCV(pipe,
                               param_grid=params,
                               scoring=scoring,
                               cv=cv,
                               verbose=1,
                               refit='F1')

    grid_search.fit(features, labels)

    print 'Classifier:', clf['name']
    print 'Best score:', grid_search.best_score_
    print 'Best precision:', grid_search.cv_results_['mean_test_Precision'][grid_search.best_index_]
    print 'Best recall:', grid_search.cv_results_['mean_test_Recall'][grid_search.best_index_]
    print 'Best parameters:', grid_search.best_params_
'''

#The best algo was Logistic Regression with the parameters below
clf=Pipeline([('scaling', MinMaxScaler()),
               ('dim_reduction', SelectKBest(k=5,score_func=chi2)),
               ('classifier',LogisticRegression(class_weight='balanced'))])

clf.fit(features, labels)

#Extracting the 5 best features foud through SelectKBest
masks = clf.named_steps.dim_reduction.get_support()
pvalues = clf.named_steps.dim_reduction.pvalues_
scores = clf.named_steps.dim_reduction.scores_

featureattributes=zip(all_features, masks, pvalues, scores)

sortedfeatures=sorted(featureattributes, key=lambda a:a[2])

features, masks, pvalues, scores=[list(t) for t in zip(*sortedfeatures)]

#Printing the best features selected by SelectKBest
for feature, mask, pvalue, score in sortedfeatures:
    if mask:
        print 'Feature:',feature
        print 'P-value:', pvalue
        print 'chi2 score:', score
        print '-----------------'

#Plotting the p-values of the features
trace=go.Bar(x=features,
             y=pvalues,
             marker=dict(color=[int(mask) for mask in masks]))

layout=go.Layout(yaxis=dict(title='P-values'))

fig=go.Figure(data=[trace],layout=layout)

plot(fig, filename='Feature p-values.html')

dump_classifier_and_data(clf, my_dataset, features_list)
