let conversationId = null

window.onload = function() {
addMessage("أهلاً وسهلاً بيك! 👋\nأنا مساعد تواصل الذكي، موجود هنا عشان أساعدك تحدد متطلبات مشروعك البرمجي.\nقولي، إيه الفكرة اللي عندك؟ 😊", "ai")
}

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

addMessage("📋 Project Summary:", "ai")

addMessage(JSON.stringify(data.summary,null,2),"ai")

// Display Kano Analysis if available
if(data.kano_analysis && data.kano_analysis.features){
addMessage("📊 Kano Model Analysis:", "ai")

const categoryLabels = {
"must_be": "🔴 Must-Be (Basic/Expected)",
"performance": "🟡 Performance (One-Dimensional)",
"attractive": "🟢 Attractive (Delighters)",
"indifferent": "⚪ Indifferent",
"reverse": "🔵 Reverse"
}

// Group features by category
const grouped = {}
for(const feature of data.kano_analysis.features){
const cat = feature.category
if(!grouped[cat]) grouped[cat] = []
grouped[cat].push(feature)
}

// Display each category
for(const [category, label] of Object.entries(categoryLabels)){
if(grouped[category] && grouped[category].length > 0){
let text = label + "\n"
for(const f of grouped[category]){
text += `  • ${f.feature_en}\n    Reason: ${f.reason_en}\n`
}
addMessage(text, "ai")
}
}

// Display strategic recommendation
if(data.kano_analysis.strategic_recommendation_en){
addMessage("💡 Strategic Recommendation:\n" + data.kano_analysis.strategic_recommendation_en, "ai")
}
}

}