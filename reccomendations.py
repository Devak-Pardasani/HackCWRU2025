import csv
import numpy as np
import json 
import pandas as pd;

def findIMDBID(args):
    fileName=args['fileName']
    choice=args['choice']

    df = pd.read_csv(fileName)
    id_value = df.loc[choice, 'ID']
    return json.dumps([id_value]);
def distanceMetric(cand,candIdx, allShows, liked,disliked):
    curr_dist=float('inf')

    for showIdx in liked:
        
        arr1=np.array(allShows[showIdx][4]);
        arr2=np.array(cand[4]);
        
        curr_dist=min(curr_dist,np.linalg.norm(arr1-arr2)); 
    return curr_dist

def sumMetric(cand,candIdx,allShows,liked,disliked,prioritization_factor=1,cachedSum=None):
    
    if len(disliked)+len(liked)==0:
        return float('inf')
    if (cachedSum==None):
        likedNames=[allShows[i][4] for i in liked]
        dislikedNames=[allShows[i][4] for i in disliked]
        
        cachedSum=(prioritization_factor*np.sum(np.array(likedNames),axis=0) - np.sum(np.array(disliked),axis=0))/(len(disliked)+len(liked))


    return np.linalg.norm(cand[3]-cachedSum);

    
def parseToList(strArr):

    return json.loads(strArr);




def sample(args):


    df = pd.read_csv(args['fileName'], header=None, skiprows=1)  # Skip the first row which is likely the header
    probs = pd.to_numeric(df[1], errors='coerce').values.astype(np.float32)  # Convert to numeric, coercing errors to NaN
    df[4] = df[4].apply(parseToList)
    probs_exp = np.exp(probs)
    probs_normalized = probs_exp / probs_exp.sum()
    choice = np.random.choice(len(probs), p=probs_normalized)
    return [str(choice), df.iloc[choice, 0]]

    

def reccomendations(args):
    fileName = args['fileName']
    nBest = args['nBest']
    liked = set(args['liked'])  
    disliked = set(args['disliked'])

    df = pd.read_csv(fileName)
    df.iloc[:, 4] = df.iloc[:, 4].apply(parseToList)  # Apply parseToList on the 4th column
    
    allShows = df.values  # Convert DataFrame to NumPy array for faster access
    currentCandidates = []
    
    for candIdx, cand in enumerate(allShows):
        if candIdx in liked:
            continue
        curr_dist = distanceMetric(cand, candIdx, allShows, liked, disliked)
        currentCandidates.append([curr_dist, candIdx])
    
    # Sort the candidates based on distance (distances are in the first element of the sublists)
    currentCandidates.sort(key=lambda x: x[0])
    
    # Get top N best shows
    topShows = [allShows[x[1]][0] for x in currentCandidates[:nBest]]
    
    return topShows
            
                    





if __name__=="__main__":
    args={
        'fileName': 'embeddings.csv',
        'nBest': 10
    }
    reccomendations(args);



