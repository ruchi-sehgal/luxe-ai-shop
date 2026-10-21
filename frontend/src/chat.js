const toggleBtn = document.getElementById("chat-toggle");
const closeBtn = document.getElementById("chat-close");
const panel = document.getElementById("chat-panel");
const messagesEl = document.getElementById("chat-messages");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");

let history = [];

toggleBtn.addEventListener("click", () => {
  panel.classList.remove("hidden");
  input.focus();
});

closeBtn.addEventListener("click", () => {
  panel.classList.add("hidden");
});

function addBubble(text, sender) {
  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${sender}`;
  bubble.textContent = text;
  messagesEl.appendChild(bubble);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return bubble;
}

function addProducts(products) {
  if (products.length === 0) return;
  const container = document.createElement("div");
  container.className = "chat-products";
  for (const p of products) {
    const card = document.createElement("div");
    card.className = "chat-product-card";
    card.innerHTML = `
      <img src="${p.image_url}" alt="${p.name}" />
      <div>
        <div class="name">${p.name}</div>
        <div class="price">₹${p.price}</div>
      </div>
    `;
    container.appendChild(card);
  }
  messagesEl.appendChild(container);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  addBubble(message, "user");
  input.value = "";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    history = data.history;
    addBubble(data.reply, "assistant");
    addProducts(data.products);
  } catch (err) {
    addBubble(`Something went wrong: ${err.message}`, "assistant");
  }
});