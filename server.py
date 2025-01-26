from flask import Flask
from flask import request
import json
import requests
from reccomendations import sample, reccomendations,findIMDBID
from flask_cors import CORS
app = Flask(__name__)


app = Flask(__name__)
CORS(app) 
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
            output=reccomendations(args);
            
            return json.dumps(output) ;

@app.route("/preferences",methods=['GET','POST'])
def preferences():

    
    if (request.method=='GET'):
        with open("data.json",'r') as f:
            return json.load(f);

    if (request.method=='POST'):

        res=request.get_json();
        liked=res.get('liked');
        data={}
        with open("data.json",'r') as f:
            data=json.load(f);
        index=int(data['choice'])
        data[liked].append(index);
        
        with open("data.json",'w') as f:
            json.dump(data,f)
    
        return "200"

@app.route("/sample", methods=["GET"])

def getSampleShow():

    args={
        'fileName': 'embeddings.csv'
    }
    id,title=sample(args)
    data={}
    with open("data.json",'r') as f:
        data=json.load(f);
    
    data['choice']=id;

    with open("data.json",'w') as f:
        json.dump(data,f)
    return json.dumps([id,title])


@app.route('/clear')

def clear():
    cleared={
        'liked':[],
        'disliked':[],
        'choice':""
    }
    with open('data.json','w') as f:
        
        json.dump(cleared,f) 
    
    return "200"

@app.route('/getID')

def getID():

    with open('data.json','r') as f:
        data=json.load(f)
        choice=int(data['choice'])
        args={
            'fileName': 'embeddings.csv',
            'choice':choice
        }
        return str(findIMDBID(args))