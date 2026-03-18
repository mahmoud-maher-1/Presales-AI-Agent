let conversationId = null;
let currentLang = "ar";
let currentState = "insufficient_information";

// unique customer key per browser tab/session only
let customerKey = sessionStorage.getItem("customer_key");
if (!customerKey) {
  customerKey = "web_user_" + crypto.randomUUID();
  sessionStorage.setItem("customer_key", customerKey);
}

window.onload = function () {
  const chat = document.getElementById("chat");
  if (chat) {
    chat.innerHTML = "";
  }

  addMessage(
    "أهلاً وسهلاً بيك! 👋\nأنا مساعد تواصل الذكي، موجود هنا عشان أساعدك تحدد متطلبات مشروعك البرمجي.\nقولي، إيه الفكرة اللي عندك؟ 😊",
    "ai"
  );

  const input = document.getElementById("messageInput");
  if (input) {
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") sendMessage();
    });
  }

  // Restore dark mode preference
  if (localStorage.getItem("darkMode") === "true") {
    document.body.classList.add("dark");
    const darkToggle = document.getElementById("darkToggle");
    if (darkToggle) {
      darkToggle.textContent = "☀️";
    }
  }

  updateReadinessUI("insufficient_information");
};

function toggleDarkMode() {
  document.body.classList.toggle("dark");
  const isDark = document.body.classList.contains("dark");
  localStorage.setItem("darkMode", isDark);

  const darkToggle = document.getElementById("darkToggle");
  if (darkToggle) {
    darkToggle.textContent = isDark ? "☀️" : "🌙";
  }
}

// يبدأ جلسة جديدة تمامًا
function resetChat() {
  sessionStorage.removeItem("customer_key");
  sessionStorage.removeItem("conversation_id");
  location.reload();
}

// ─── Tab Switching ───

function showTab(tab) {
  const chatTab = document.getElementById("chatTab");
  const downloadsTab = document.getElementById("downloadsTab");
  const tabChat = document.getElementById("tabChat");
  const tabDownloads = document.getElementById("tabDownloads");

  if (!chatTab || !downloadsTab || !tabChat || !tabDownloads) return;

  if (tab === "chat") {
    chatTab.classList.add("active");
    downloadsTab.classList.remove("active");
    tabChat.classList.add("active");
    tabDownloads.classList.remove("active");
  } else {
    chatTab.classList.remove("active");
    downloadsTab.classList.add("active");
    tabChat.classList.remove("active");
    tabDownloads.classList.add("active");
  }
}

// ─── Readiness Gating ───

function updateReadinessUI(state) {
  currentState = state;

  const summaryBtn = document.getElementById("summaryBtn");
  const downloadsLocked = document.getElementById("downloadsLocked");
  const downloadsReady = document.getElementById("downloadsReady");

  const unlockedStates = ["ready_for_summary", "ready_for_closing"];

  if (summaryBtn) {
    if (unlockedStates.includes(state)) {
      summaryBtn.disabled = false;
      summaryBtn.classList.remove("locked");
    } else {
      summaryBtn.disabled = true;
      summaryBtn.classList.add("locked");
    }
  }

  if (downloadsLocked && downloadsReady) {
    if (unlockedStates.includes(state)) {
      downloadsLocked.style.display = "none";
      downloadsReady.style.display = "block";
    } else {
      downloadsLocked.style.display = "flex";
      downloadsReady.style.display = "none";
    }
  }
}

// ─── Messages ───

async function sendMessage() {
  const input = document.getElementById("messageInput");
  const text = input.value.trim();

  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  try {
    const response = await fetch("/api/message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        customer_key: customerKey,
        message: text,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("API error:", response.status, errorText);
      throw new Error(`Request failed: ${response.status}`);
    }

    const data = await response.json();

    conversationId = data.conversation_id;
    sessionStorage.setItem("conversation_id", String(conversationId));

    addMessage(data.reply, "ai");

    updateReadinessUI(data.state);

    if (typeof data.lead_score === "number" && data.lead_status) {
      addMessage(`📌 Lead Score: ${data.lead_score} (${data.lead_status})`, "ai");
    }
  } catch (error) {
    console.error(error);
    addMessage(`❌ حصلت مشكلة أثناء إرسال الرسالة: ${error.message}`, "ai");
  }
}

function addMessage(text, type) {
  const chat = document.getElementById("chat");
  if (!chat) return;

  const div = document.createElement("div");
  div.className = type;
  div.innerText = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

// ─── Language Toggle ───

function toggleLang() {
  currentLang = currentLang === "en" ? "ar" : "en";
  const btn = document.getElementById("langToggle");
  if (btn) {
    btn.textContent = currentLang === "en" ? "🌐 English" : "🌐 عربي";
  }
}

// ─── Summary Generation ───

async function getSummary() {
  if (!conversationId) {
    const storedConversationId = sessionStorage.getItem("conversation_id");
    if (storedConversationId) {
      conversationId = Number(storedConversationId);
    }
  }

  if (!conversationId) {
    alert("ابدأ محادثة أولاً");
    return;
  }

  const btn = document.getElementById("summaryBtn");
  if (btn) {
    btn.disabled = true;
    btn.textContent = "⏳ Preparing documents...";
  }

  try {
    const response = await fetch(
      `/api/conversation/${conversationId}/summary?lang=${currentLang}`
    );

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Summary error:", response.status, errorText);
      throw new Error("Summary generation failed");
    }

    await response.json();

    addMessage(
      "✅ تم تجهيز ملفات المشروع. تقدر تنزلها من تبويب Downloads.",
      "ai"
    );

    showTab("downloads");
  } catch (e) {
    console.error(e);
    addMessage("❌ حصل خطأ أثناء تجهيز الملفات.", "ai");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "Generate Project Summary";
    }
  }
}

// ─── PDF Downloads ───

function downloadPDF(type) {
  if (!conversationId) {
    const stored = sessionStorage.getItem("conversation_id");
    if (stored) {
      conversationId = stored;
    }
  }

  if (!conversationId) {
    alert("ابدأ محادثة أولاً");
    return;
  }

  let url = `/api/conversation/${conversationId}/pdf/${type}`;

  if (["summary", "swot", "activity", "kano"].includes(type)) {
    url += `?lang=${currentLang}`;
  }

  window.open(url, "_blank");
}