import csv
import numpy as np
import json 
def parseToList(strArr):

    return json.loads(strArr);
def reccomendaitons(args):

    
    fileName=args['fileName']
    probs=[]
    allShows=[]
    with open(fileName,'r') as f:

        reader=csv.reader(f);
        header=[]
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
        liked=[]
        for i in range(100):
            n_samples=len(probs)
            choice=np.random.choice(n_samples,1,p=probs)[0];
            print(f"Have you watched {allShows[choice][0]} and did you like it? (0-Watched it and liked, 1-Watched and didn't like, 2-Never watched/I don't know)?")
            
            ans=int(input())
            
            
            if (ans==0):

                liked.append(choice)
            currentCandidates=[]
            
            for (candIdx, cand) in enumerate(allShows):
                if (candIdx in liked):
                    continue
                curr_dist=float('inf');

                for showIdx in liked:
                   
                    arr1=np.array(allShows[showIdx][3]);
                    arr2=np.array(cand[3]);
                    
                    curr_dist=min(curr_dist,np.linalg.norm(arr1-arr2)); 
                    
                 
                currentCandidates.append([curr_dist,candIdx])
            
            currentCandidates.sort(key=lambda x: x[0])
            topShows=currentCandidates[0:args["nBest"]]
            topShows=[allShows[x[1]][0] for x in topShows]
            print(f"Your top show reccomendations are: {topShows}")

            
                    





if __name__=="__main__":
    args={
        'fileName': 'embeddings.csv',
        'nBest': 10
    }
    reccomendaitons(args);



