import numpy as np 
import pandas as pd 
from sklearn.preprocessing import scale
from catboost import CatBoostClassifier
# from xgboost import XGBClassifier
import pickle

heart_disease_classifier = pickle.load(open('CatboostModel.pkl', 'rb'))

hepatitis_disease_classifier = pickle.load(open('hepatitis_classifier.pkl', 'rb'))

def hepatitisFunc(Age, Sex, ALB, ALP, ALT, AST, BIL, CHE, CHOL, CREA, GGT, PROT):
    result = hepatitis_disease_classifier.predict(scale(np.array([Age, sexTransform(Sex), ALB, 
                ALP, ALT, AST, BIL, CHE, CHOL, CREA, GGT, PROT])).reshape(1,-1))
    return result

def sexTransform(value):
    return 1 if value.lower() == 'male' else 0

def chestTransform(value):
    if value == 'ASY':
        return 0
    elif value == 'ATA':
        return 1
    elif value == 'NAP':
        return 2
    else:
        return 3

def resting_ecgTransform(value):
    if value == 'LVH':
        return 0
    elif value == 'Normal':
        return 1
    else:
        return 2

def exerciseTransform(value):
    return 1 if value == 'N' else 0
    
def st_slopeTransform(value):
    if value == 'Down':
        return 0
    elif value == 'Flat':
        return 1
    else:
        return 2

def heartFunc(Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS,RestingECG, MaxHR, 
                ExerciseAngina, Oldpeak, ST_Slope):

    result = heart_disease_classifier.predict(scale(np.array([sexTransform(Age), sexTransform(Sex), chestTransform(ChestPainType), 
                RestingBP, Cholesterol, FastingBS, resting_ecgTransform(RestingECG), MaxHR,
                exerciseTransform(ExerciseAngina), Oldpeak, st_slopeTransform(ST_Slope) ])).reshape(1,-1))
    return result



