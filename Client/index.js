let DEBUG = false
document.addEventListener('DOMContentLoaded', ()=>{
    if (DEBUG) console.log('DOM Loaded')
    document.getElementById('searchbutton').addEventListener('click', activate)
    document.getElementById('ytURL').addEventListener("keyup", ({key}) => {
        if (key === "Enter") {
            activate()
        }
    })
})

let activate = async () => {
    if (DEBUG) console.log('clicked!')
    let ytURL = document.getElementById('ytURL').value
    let linkElement = document.getElementById('playlistLink')
    if(ytURL != undefined && ytURL != ""){
        if(ytURL.split(".com")[1] != "/" && ytURL.split(".be/")[1] != "/" && ytURL.split(".com")[1] != "" && ytURL.split(".be")[1] != ""){
            if(ytURL.substr(0,4) != "http"){
                ytURL = `https://${ytURL}`
            }
            if (DEBUG) console.log('exists!')
                if (DEBUG) console.log('valid!')
                let spinner = setTimeout(()=>{
                    document.getElementById('searchbutton').disabled = false
                    document.getElementById('playlistLink').innerText = 'Playlist could not be loaded. Please message @LastechLabs on Twitter if this problem persists!'
                    linkElement.onclick = ""
                    linkElement.href = "https://www.twitter.com/lastechlabs"
                }, 20000)   

                linkElement.href = "#"
                linkElement.onclick = ()=>{return false}
                document.getElementById('searchbutton').disabled = true
                linkElement.innerText = "LOADING..."
                try{
                    let a = await fetch('https://uploadsplaylist.herokuapp.com/grab', {
                        method: 'POST', 
                        headers:{
                            'Content-Type': 'application/json'
                        }, 
                        body: JSON.stringify({
                            'URL': ytURL
                        })
                    })
                    let b = await a.text()
                    if(document.getElementById('searchbutton').disabled == true){
                        clearTimeout(spinner)
                        document.getElementById('searchbutton').disabled = false
                    }
                    if (DEBUG) console.log(b)
                    if(b == "ERROR URL NOT FOUND"){
                        linkElement.href = "#"
                        linkElement.onclick = ()=>{return false}
                    }else{
                        linkElement.onclick = ""
                        linkElement.href = b
                    }
                    linkElement.innerText = b
                }catch(error){
                    console.log(error)
                }
        }else{
            document.getElementById('searchbutton').disabled = false
            document.getElementById('playlistLink').innerText = 'Please enter the URL of a youtube video, playlist or channel'
            linkElement.onclick = ()=>{return false}
            linkElement.href = "#"
        }
    }else{
        document.getElementById('searchbutton').disabled = false
        document.getElementById('playlistLink').innerText = 'Please enter the URL of a youtube video, playlist or channel'
        linkElement.onclick = ()=>{return false}
        linkElement.href = "#"
    }

}