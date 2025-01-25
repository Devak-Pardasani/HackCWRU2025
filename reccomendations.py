import csv
import numpy as np
import json 

def distanceMetric(cand,candIdx, allShows, liked):
    curr_dist=float('inf')

    for showIdx in liked:
        
        arr1=np.array(allShows[showIdx][3]);
        arr2=np.array(cand[3]);
        
        curr_dist=min(curr_dist,np.linalg.norm(arr1-arr2)); 
    return curr_dist

def sumMetric(cand,candIdx,allShows,liked,disliked,prioritization_factor=1,cachedSum=None):
    
    if len(disliked)+len(liked)==0:
        return float('inf')
    if (cachedSum==None):
        likedNames=[allShows[i][3] for i in liked]
        dislikedNames=[allShows[i][3] for i in disliked]
        
        cachedSum=(prioritization_factor*np.sum(np.array(likedNames),axis=0) - np.sum(np.array(disliked),axis=0))/(len(disliked)+len(liked))


    return np.linalg.norm(cand[3]-cachedSum);

    
def parseToList(strArr):

    return json.loads(strArr);


def sample(args):

    with open(args['fileName'],'r') as f:
        allShows=[]
        reader=csv.reader(f);
        header=[]
        probs=[]
        for (i,show) in enumerate(reader):

            if (i==0):
                header=show
            else:
                
                probs.append(float(show[1]))
                show[3]=parseToList(show[3])
                allShows.append(show);
        
        probs=np.array(probs)
        probs_exp=np.exp(probs);
        probs=probs_exp/np.sum(probs_exp)
        n_samples=len(probs);

        choice=np.random.choice(n_samples,1,p=probs)[0];

        return choice

    
def reccomendations(args):
    print("HELLO");
    
    fileName=args['fileName']
    
    allShows=[]
    with open(fileName,'r') as f:

        reader=csv.reader(f);
        header=[]
        for (i,show) in enumerate(reader):

            if (i==0):
                header=show
            else:
                
                show[3]=parseToList(show[3])
                allShows.append(show);
        
        choice=args['choice']
        liked=args['liked']
        disliked=args['disliked']

        
    
        currentCandidates=[]
        
        for (candIdx, cand) in enumerate(allShows):
            if (candIdx in liked):
                continue
            curr_dist=sumMetric(cand,candIdx,allShows,liked,disliked)

            
                
            currentCandidates.append([curr_dist,candIdx])
            print(candIdx)
        currentCandidates.sort(key=lambda x: x[0])
        topShows=currentCandidates[0:args["nBest"]]
        topShows=[allShows[x[1]][0] for x in topShows]
        print(f"Your top show reccomendations are: {topShows}")

            
                    





if __name__=="__main__":
    args={
        'fileName': 'embeddings.csv',
        'nBest': 10
    }
    reccomendations(args);



