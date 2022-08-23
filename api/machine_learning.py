import numpy as np 
import pandas as pd 
from sklearn.preprocessing import scale
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
import pickle

heart_disease_classifier = pickle.load(open('CatboostModel.pkl', 'rb'))

hepatitis_disease_classifier = pickle.load(open('voting_classifier.pkl', 'rb'))

def hepatitisFunc(Age, Sex, ALB, ALP, ALT, AST, BIL, CHE, CHOL, CREA, GGT, PROT):
    result = hepatitis_disease_classifier.predict(scale(np.array([Age, Sex, ALB, 
                ALP, ALT, AST, BIL, CHE, CHOL, CREA, GGT, PROT])).reshape(1,-1))
    return result

def heartFunc(Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS,RestingECG, MaxHR, 
                ExerciseAngina, Oldpeak, ST_Slope):

    result = heart_disease_classifier.predict(scale(np.array([Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS,RestingECG, MaxHR, 
                ExerciseAngina, Oldpeak, ST_Slope])).reshape(1,-1))
    return result



