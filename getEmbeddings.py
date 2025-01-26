import csv
import ollama
def getEmbeddings(fileName):
    header=[]
    with open(fileName,'r') as f:
        csv_reader=csv.reader(f)
        
        
        shows=[] #[name,desc,popularity (for random sampling)]

        for (id,row) in enumerate(csv_reader):
            if (id==0):
                header=row 
                print(header)
            else:
                if (len(row[-1]) == 0):
                    print(f"No Description provided for {row[4]}. Show skipped");
                    continue
                shows.append([row[4],float(row[11]),row[-1],row[2]])
    
    embeddings=[]
    for i, d in enumerate(shows):
        response = ollama.embeddings(model="mxbai-embed-large", prompt=d[2]) #get embeddings for each description
        embedding = response["embedding"]
        embeddings.append(embedding)
    
    for i in range(len(shows)):
        shows[i].append(embeddings[i]);

    shows.insert(0,[header[4],header[11],header[-1],'ID','Embeddngs'])

    with open('embeddings.csv','w',newline="") as f:
        writer=csv.writer(f)
        writer.writerows(shows)



if __name__=="__main__":
    getEmbeddings("IMDB.csv")