let conversationId = null
let currentLang = "en"
let currentState = "insufficient_information"

window.onload = function() {
addMessage("أهلاً وسهلاً بيك! 👋\nأنا مساعد تواصل الذكي، موجود هنا عشان أساعدك تحدد متطلبات مشروعك البرمجي.\nقولي، إيه الفكرة اللي عندك؟ 😊", "ai")

document.getElementById("messageInput").addEventListener("keydown", function(e) {
  if(e.key === "Enter") sendMessage()
})

// Restore dark mode preference
if(localStorage.getItem("darkMode") === "true"){
  document.body.classList.add("dark")
  document.getElementById("darkToggle").textContent = "☀️"
}
}

function toggleDarkMode(){
document.body.classList.toggle("dark")
const isDark = document.body.classList.contains("dark")
localStorage.setItem("darkMode", isDark)
document.getElementById("darkToggle").textContent = isDark ? "☀️" : "🌙"
}

// ─── Tab Switching ───

function showTab(tab){
const chatTab = document.getElementById("chatTab")
const downloadsTab = document.getElementById("downloadsTab")
const tabChat = document.getElementById("tabChat")
const tabDownloads = document.getElementById("tabDownloads")

if(tab === "chat"){
  chatTab.classList.add("active")
  downloadsTab.classList.remove("active")
  tabChat.classList.add("active")
  tabDownloads.classList.remove("active")
} else {
  chatTab.classList.remove("active")
  downloadsTab.classList.add("active")
  tabChat.classList.remove("active")
  tabDownloads.classList.add("active")
}
}

// ─── Readiness Gating ───

function updateReadinessUI(state){
currentState = state
const summaryBtn = document.getElementById("summaryBtn")
const downloadsLocked = document.getElementById("downloadsLocked")
const downloadsReady = document.getElementById("downloadsReady")

if(state === "ready_for_summary"){
  summaryBtn.disabled = false
  summaryBtn.classList.remove("locked")
  downloadsLocked.style.display = "none"
  downloadsReady.style.display = "block"
} else {
  summaryBtn.disabled = true
  summaryBtn.classList.add("locked")
  downloadsLocked.style.display = "flex"
  downloadsReady.style.display = "none"
}
}

// ─── Messages ───

async function sendMessage(){
const input = document.getElementById("messageInput")
const text = input.value.trim()
if(!text) return

addMessage(text, "user")
input.value = ""

const response = await fetch("/api/message", {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify({ customer_key: "web_user", message: text })
})

const data = await response.json()
conversationId = data.conversation_id
addMessage(data.reply, "ai")

// Update readiness gate based on conversation state
updateReadinessUI(data.state)
}

function addMessage(text, type){
const chat = document.getElementById("chat")
const div = document.createElement("div")
div.className = type
div.innerText = text
chat.appendChild(div)
chat.scrollTop = chat.scrollHeight
}

function addHtmlMessage(html, type){
const chat = document.getElementById("chat")
const div = document.createElement("div")
div.className = type
div.innerHTML = html
chat.appendChild(div)
chat.scrollTop = chat.scrollHeight
}

// ─── Language Toggle ───

function toggleLang(){
currentLang = currentLang === "en" ? "ar" : "en"
const btn = document.getElementById("langToggle")
btn.textContent = currentLang === "en" ? "🌐 English" : "🌐 عربي"
}

// ─── Summary Generation ───

async function getSummary(){
if(!conversationId){
  alert("ابدأ محادثة أولا")
  return
}

const btn = document.getElementById("summaryBtn")
btn.disabled = true
btn.textContent = "⏳ Generating..."

try {
  const response = await fetch(`/api/conversation/${conversationId}/summary?lang=${currentLang}`)
  const data = await response.json()

  addMessage("📋 Project Summary:", "ai")
  addMessage(JSON.stringify(data.summary, null, 2), "ai")

  if(data.kano_analysis && data.kano_analysis.features){
    displayKano(data.kano_analysis)
  }

  if(data.srs_document){
    displaySRS(data.srs_document)
  }
} catch(e) {
  addMessage("❌ Failed to generate summary. Please try again.", "ai")
} finally {
  btn.disabled = false
  btn.textContent = "Generate Project Summary"
}
}

// ─── Kano Display ───

function displayKano(kano){
addMessage("📊 Kano Model Analysis:", "ai")

const categoryLabels = {
  "must_be": "🔴 Must-Be (Basic/Expected)",
  "performance": "🟡 Performance (One-Dimensional)",
  "attractive": "🟢 Attractive (Delighters)",
  "indifferent": "⚪ Indifferent",
  "reverse": "🔵 Reverse"
}

const grouped = {}
for(const feature of kano.features){
  const cat = feature.category
  if(!grouped[cat]) grouped[cat] = []
  grouped[cat].push(feature)
}

for(const [category, label] of Object.entries(categoryLabels)){
  if(grouped[category] && grouped[category].length > 0){
    let text = label + "\n"
    for(const f of grouped[category]){
      text += `  • ${f.feature}\n    Reason: ${f.reason}\n`
    }
    addMessage(text, "ai")
  }
}

if(kano.strategic_recommendation){
  addMessage("💡 Strategic Recommendation:\n" + kano.strategic_recommendation, "ai")
}
}

// ─── SRS Display ───

function displaySRS(srs){
const s = srs.sections
let html = `<div class="srs-document">`

html += `<div class="srs-header">`
html += `<h3>📄 ${escapeHtml(srs.title || "Software Requirements Specification")}</h3>`
html += `<span class="srs-meta">v${escapeHtml(srs.version || "1.0")} — ${escapeHtml(srs.date || "")}</span>`
html += `</div>`

if(s.introduction){
  html += `<div class="srs-section">`
  html += `<h4>1. Introduction</h4>`
  if(s.introduction.purpose){
    html += `<div class="srs-subsection"><strong>1.1 Purpose</strong><p>${escapeHtml(s.introduction.purpose)}</p></div>`
  }
  if(s.introduction.scope){
    html += `<div class="srs-subsection"><strong>1.2 Scope</strong><p>${escapeHtml(s.introduction.scope)}</p></div>`
  }
  if(s.introduction.definitions && s.introduction.definitions.length > 0){
    html += `<div class="srs-subsection"><strong>1.3 Definitions</strong><ul>`
    for(const d of s.introduction.definitions){
      html += `<li><strong>${escapeHtml(d.term || "")}</strong>: ${escapeHtml(d.definition || "")}</li>`
    }
    html += `</ul></div>`
  }
  html += `</div>`
}

if(s.overall_description){
  const od = s.overall_description
  html += `<div class="srs-section"><h4>2. Overall Description</h4>`
  if(od.product_perspective) html += `<div class="srs-subsection"><strong>2.1 Product Perspective</strong><p>${escapeHtml(od.product_perspective)}</p></div>`
  if(od.product_features && od.product_features.length > 0){
    html += `<div class="srs-subsection"><strong>2.2 Product Features</strong><ul>`
    for(const f of od.product_features) html += `<li>${escapeHtml(f)}</li>`
    html += `</ul></div>`
  }
  if(od.user_classes && od.user_classes.length > 0){
    html += `<div class="srs-subsection"><strong>2.3 User Classes</strong><ul>`
    for(const u of od.user_classes) html += `<li><strong>${escapeHtml(u.class || "")}</strong>: ${escapeHtml(u.description || "")}</li>`
    html += `</ul></div>`
  }
  if(od.operating_environment) html += `<div class="srs-subsection"><strong>2.4 Operating Environment</strong><p>${escapeHtml(od.operating_environment)}</p></div>`
  if(od.constraints && od.constraints.length > 0){
    html += `<div class="srs-subsection"><strong>2.5 Constraints</strong><ul>`
    for(const c of od.constraints) html += `<li>${escapeHtml(c)}</li>`
    html += `</ul></div>`
  }
  if(od.assumptions && od.assumptions.length > 0){
    html += `<div class="srs-subsection"><strong>2.6 Assumptions</strong><ul>`
    for(const a of od.assumptions) html += `<li>${escapeHtml(a)}</li>`
    html += `</ul></div>`
  }
  html += `</div>`
}

if(s.functional_requirements && s.functional_requirements.length > 0){
  html += `<div class="srs-section"><h4>3. Functional Requirements</h4>`
  for(const fr of s.functional_requirements){
    const priorityClass = (fr.priority || "P2").toLowerCase()
    html += `<div class="srs-requirement">`
    html += `<div class="srs-req-header"><span class="srs-req-id">${escapeHtml(fr.id || "")}</span><span class="srs-priority ${priorityClass}">${escapeHtml(fr.priority || "")}</span></div>`
    html += `<strong>${escapeHtml(fr.title || "")}</strong><p>${escapeHtml(fr.description || "")}</p>`
    if(fr.acceptance_criteria && fr.acceptance_criteria.length > 0){
      html += `<div class="srs-ac"><em>Acceptance Criteria:</em><ul>`
      for(const ac of fr.acceptance_criteria) html += `<li>${escapeHtml(ac)}</li>`
      html += `</ul></div>`
    }
    html += `</div>`
  }
  html += `</div>`
}

if(s.non_functional_requirements && s.non_functional_requirements.length > 0){
  html += `<div class="srs-section"><h4>4. Non-Functional Requirements</h4>`
  for(const nfr of s.non_functional_requirements){
    html += `<div class="srs-requirement">`
    html += `<div class="srs-req-header"><span class="srs-req-id">${escapeHtml(nfr.id || "")}</span><span class="srs-nfr-cat">${escapeHtml(nfr.category || "")}</span></div>`
    html += `<strong>${escapeHtml(nfr.title || "")}</strong><p>${escapeHtml(nfr.description || "")}</p>`
    html += `</div>`
  }
  html += `</div>`
}

if(s.constraints_and_assumptions && s.constraints_and_assumptions.length > 0){
  html += `<div class="srs-section"><h4>5. Constraints & Assumptions</h4><ul>`
  for(const item of s.constraints_and_assumptions) html += `<li>${escapeHtml(item)}</li>`
  html += `</ul></div>`
}

if(s.acceptance_criteria_summary){
  html += `<div class="srs-section"><h4>6. Acceptance Criteria Summary</h4><p>${escapeHtml(s.acceptance_criteria_summary)}</p></div>`
}

html += `</div>`
addHtmlMessage(html, "ai srs-wrapper")
}

// ─── PDF Downloads ───

function downloadPDF(type){
if(!conversationId){
  alert("No conversation to download")
  return
}
let url = `/api/conversation/${conversationId}/pdf/${type}`
if(type === "kano" || type === "srs"){
  url += `?lang=${currentLang}`
}
window.open(url, "_blank")
}

// ─── Utility ───

function escapeHtml(text){
if(!text) return ""
const div = document.createElement("div")
div.appendChild(document.createTextNode(String(text)))
return div.innerHTML
}