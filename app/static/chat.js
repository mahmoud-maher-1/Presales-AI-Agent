let conversationId = null

async function sendMessage(){

const input = document.getElementById("messageInput")
const text = input.value

addMessage(text,"user")

const response = await fetch("/api/message",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
customer_key:"web_user",
message:text
})
})

const data = await response.json()

conversationId = data.conversation_id

addMessage(data.reply,"ai")

input.value = ""
}

function addMessage(text,type){

const chat = document.getElementById("chat")

const div = document.createElement("div")
div.className = type

div.innerText = text

chat.appendChild(div)

chat.scrollTop = chat.scrollHeight
}

async function getSummary(){

if(!conversationId){
alert("ابدأ محادثة أولا")
return
}

const response = await fetch(`/api/conversation/${conversationId}/summary`)

const data = await response.json()

addMessage("Project Summary:", "ai")

addMessage(JSON.stringify(data.summary,null,2),"ai")

}