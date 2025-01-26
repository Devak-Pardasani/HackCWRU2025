port=5000

async function fetchImage(id){



    var url="http://127.0.0.1:"+port+"/getID"
    var src="";
    const response=await fetch(url);
    const json=response.json();
    json.then(function(result){
        const url="https://api.themoviedb.org/3/find/" + result+ "?external_source=imdb_id"
        const options = {
            method: 'GET',
            headers: {
              accept: 'application/json',
              Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0ZWM2ZjNkMTc0Y2Y0NjgyNzBkZTE3NjE5YmVjMzEyZCIsIm5iZiI6MTczNzgyNzczNS42Nywic3ViIjoiNjc5NTI1OTc5YTMwYTg1YjI3MjM5MWQ3Iiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.cUtHclXqyB2xmgXz2yaZdKdmeIXw5RVC5gqbnNuTURQ'
            }
          };
          
          fetch(url, options)
          .then(res => res.json())
          .then(res =>{
            const poster_path=res['movie_results'][0].poster_path
       
            src="https://image.tmdb.org/t/p/w500/"+poster_path
            $('#imageDiv').empty();
            console.log(src);
            var image=document.createElement('img')
            image.src=src 
            image.alt="Imagine a poster here..."
            $("#imageDiv").append(image);
    })
          .catch(
            err => {console.error(err)
            const noImage=document.createElement('h1');
            noImage.textContent="No Image Found :("
            $("#imageDiv").append(noImage);
          });


        
            
    })


 


}
async function loadImage(){

    const url="http://127.0.0.1:"+port+"/sample"
    const response = await fetch(url);
    try{
    
    if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
    }

    const json = response.json();
    json.then(async function(result) {
    
        $("#movieTitle").remove();
        const element=document.createElement('h1');
        element.textContent=result[1]
        element.id="movieTitle"
        $(".image-area").prepend(element)
        
        await fetchImage();
    })
    

}
    catch (error) {
        console.error(error.message);
    }



}
const turnButtonsOn = (arr) => {

    console.log(arr);

    arr.forEach(element => {
        $(".icon-container").append(element)
    });
}

const turnButtonsOff = () => {
    const arr=Array.from($('.icon-container').children());
    $('.icon-container').empty();
    
    return arr;


    
}
async function processClick(){
    
    const iconId = event.target.id;
    const arr=turnButtonsOff();
    $("#movieTitle").remove();
    $("#imageDiv").empty();
    const waitingElement=document.createElement('h1')
    waitingElement.id="movieTitle"
    const imageWaiting=document.createElement('h1')
    imageWaiting.textContent="Image Uploading..."
    waitingElement.textContent="Title Uploading..."
    $('.image-area').prepend(waitingElement);
    $("#imageDiv").append(imageWaiting);
    if (iconId=="question"){
        loadImage()
        turnButtonsOn(arr)
        
        return;
    }
    const url = "http://127.0.0.1:" + port + "/preferences";
    console.log(url);
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ liked: iconId }),
    });

    if (response.status==200){
        loadImage().then(()=>{
            turnButtonsOn(arr)
        })
        const url2="http://127.0.0.1:" + port + "/top10";
        const response2=await fetch(url2);
        const json=response2.json();
        
        json.then(function(result) {
            
            $("#list").empty();
            
            for ( i=0;i<result.length;i++){
                element=document.createElement('li')
                element.textContent=result[i];
                $('#list').append(element)
            }
        
        })
        
        return;

        
    }

}
const clearData=()=>{
    
    const url = "http://127.0.0.1:" + port + "/clear";
    return fetch(url);
}
document.addEventListener("DOMContentLoaded",()=>{
    const icons = Array.from(document.getElementsByClassName('icon'));
    for (i=0;i<icons.length;i++){
        
        
        icons[i].addEventListener('click',processClick)
    }
})



window.onload = () => {
    loadImage();
    

    clearData();
}
