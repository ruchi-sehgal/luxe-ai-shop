const grid = document.getElementById("product-grid");
const categoryButtons = document.querySelectorAll(".site-header nav button");
const priceButtons = document.querySelectorAll(".price-filters button");

let allProducts = [];
let activeCategory = "";
let activeMin = null;
let activeMax = null;

function renderProducts(products) {
  grid.innerHTML = "";
  if (products.length === 0) {
    grid.innerHTML = "<p class='empty'>No products found.</p>";
    return;
  }
  for (const p of products) {
    const card = document.createElement("article");
    card.className = "product-card";
    card.innerHTML = `
      <div class="product-image" style="background-image: url('${p.image_url}')"></div>
      <h3>${p.name}</h3>
      <p class="price">₹${p.price}</p>
      <p class="desc">${p.description}</p>
    `;
    grid.appendChild(card);
  }
}

function applyFilters() {
  const filtered = allProducts.filter((p) => {
    if (activeCategory && p.category !== activeCategory) return false;
    if (activeMin != null && p.price < activeMin) return false;
    if (activeMax != null && p.price > activeMax) return false;
    return true;
  });
  renderProducts(filtered);
}

for (const btn of categoryButtons) {
  btn.addEventListener("click", () => {
    categoryButtons.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    activeCategory = btn.dataset.category;
    applyFilters();
  });
}

for (const btn of priceButtons) {
  btn.addEventListener("click", () => {
    priceButtons.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    activeMin = btn.dataset.min ? Number(btn.dataset.min) : null;
    activeMax = btn.dataset.max ? Number(btn.dataset.max) : null;
    applyFilters();
  });
}

async function init() {
  try {
    const res = await fetch("/products");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    allProducts = await res.json();
    applyFilters();
  } catch (err) {
    grid.innerHTML = `<p class="empty">Could not reach the backend: ${err.message}</p>`;
  }
}

init();