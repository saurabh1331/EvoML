'''
All the evaluation functions are inside this files.
Add new evalution functions in this file which will be according to the fitness function to be used.
'''
import random
from random import randint
import pandas as pd
from deap import base, creator, tools, algorithms
from sklearn import linear_model
import numpy as np
from sklearn.metrics import mean_squared_error
import math
from sklearn.cross_validation import train_test_split

def evalOneMax(individual, x_te, y_te, test_frac, test_frac_flag):
    '''
    It evaluates the whole ensemble as one. Predicting for each chromosome and then
    averaging the predictions.
    '''
    predict_vals = []
    y_te = pd.DataFrame(y_te)
    # Below is an experimental line. This was to change the test sample as well for each but 
    # later we found out that this is not going to work as we were thinking because of eaSimple's
    # inherent nature
    #x_te = x_te.sample(frac=test_frac, replace=test_frac_flag)
    #y_te = y_te.loc[list(x_te.index)]
    for i in range(0,len(individual)):
        chromosome = individual[i]
        predict_vals.append(get_predictions(x_te, chromosome))
    final_prediction = []
    for i in range(0,len(individual)):
        if(i==0):
            final_prediction = predict_vals[0]
        else:
            final_prediction = final_prediction+predict_vals[i]
    final_prediction = final_prediction/len(individual)
    return math.sqrt(mean_squared_error(y_te, final_prediction)),

def get_predictions(x_te, chrom):
    feat_chrom = list(chrom.X.columns.values)
    test_feat = x_te[feat_chrom]
    mod = chrom.estimator
    predicted = mod.predict(test_feat)
    return predicted

def evalOneMax2(individual, X_f, y_f):
    '''
    This function evaluates the whole ensemble by calculating error for each of the 
    individual and then averaging the errors for all the chromosomes.
    '''
    predict_rmses = []
    predict_vals = []
    ind_f = list(X_f.index)
    for i in range(0,len(individual)):
        chromosome = individual[i]
        ind_train = list(chromosome.X.index)        
        ind_test = list(set(ind_f)-set(ind_train))
        x_te = X_f.loc[ind_test]
        y_te = y_f.loc[ind_test]    
        predict_vals.append(get_predictions(x_te, chromosome))
        predict_rmses.append(mean_squared_error(y_te, predict_vals[i]))
    final_rmse = sum(predict_rmses)/len(predict_rmses)
    return final_rmse,