from flask import Flask
from flask import request
import json
import requests
from reccomendations import sample, reccomendations
app = Flask(__name__)

@app.route("/")
def hello_world():
    return {'data':[1,2,3]}


@app.route("/top10",methods=['GET'])

def top10():


    if request.method=='GET':
        with open("data.json",'r') as f:

            pref=json.load(f)

            likes=pref['liked']
            dislikes=pref['disliked'];
            choice=pref['choice']
            likes=[int(l) for l in likes]
            dislikes=[int(dl) for dl in dislikes]
            fileName='embeddings.csv'
            args={
                'fileName': fileName,
                'liked': likes,
                'disliked': dislikes,
                'choice': choice,
                'nBest':10
            }
            reccomendations(args)
            return "200"

@app.route("/preferences",methods=['GET','POST'])
def preferences():

    
    if (request.method=='GET'):
        with open("data.json",'r') as f:
            return json.load(f);

    if (request.method=='POST'):

        liked=request.args['liked']
        index=int(request.args['index'])
        data={}
        with open("data.json",'r') as f:
            data=json.load(f);
        
        data[liked].append(index);
        
        with open("data.json",'w') as f:
            json.dump(data,f)
    
        return "200"

@app.route("/sample", methods=["GET"])

def getSampleShow():

    args={
        'fileName': 'embeddings.csv'
    }

    return str(sample(args));
