from numpy import exp
from scipy.stats import norm

def get_SDNN(age):
    if age <= 15:
        result = norm(loc = 108, scale = 32)
        return result
    elif 15 < age <= 21:
        result = norm(loc = 101, scale = 57)
        return result
    elif 21 < age < 24:
        result = norm(loc = 127, scale = 51)
        return result
    else:
        result = norm(loc = 105, scale = 64)
        return result

def get_RMSSD(age):
    if age <= 15:
        result = norm(loc = 137, scale = 48)
        return result
    elif 15 < age <= 21:
        result = norm(loc = 134, scale = 83)
        return result
    elif 21 < age < 24:
        result = norm(loc = 168, scale = 79)
        return result
    else:
        result = norm(loc = 140, scale = 90)
        return result
    
def get_pNN50(age):
    if age <= 15:
        result = norm(loc = 47, scale = 46)
        return result
    elif 15 < age <= 21:
        result = norm(loc = 41, scale = 40)
        return result
    elif 21 < age < 24:
        result = norm(loc = 52, scale = 54)
        return result
    else:
        result = norm(loc = 43, scale = 43)
        return result

def get_LFHF(age):
    if age <= 15:
        result = norm(loc = 0.163, scale = 0.007)
        return result
    elif 15 < age <= 21:
        result = norm(loc = 0.012, scale = 0.06)
        return result
    elif 21 < age < 24:
        result = norm(loc = 0.015, scale = 0.08)
        return result
    else:
        result = norm(loc = 0.013, scale = 0.115)
        return result