const tabBtns = document.querySelectorAll(".tab-btn");
const tabPanels = document.querySelectorAll(".tab-panel");
const dealList = document.querySelector(".deal-list");
const categoryList = document.getElementById("category-filter");

let allDeals = [];
let selectedCategories = [];
let userCategories = [];

// ── CONSTRUCTORS ────────────────────────────────────────────

function Deal(name, category, originalPrice, currentPrice, img_url, src_url) {
  this.name = name;
  this.category = category;
  this.originalPrice = originalPrice.startsWith("£")
    ? originalPrice
    : "£" + originalPrice;
  this.currentPrice = currentPrice.startsWith("£")
    ? currentPrice
    : "£" + currentPrice;
  this.img_url = img_url;
  this.src_url = src_url;
}

class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
    this.trackedCategories = [];
    this.dealHistory = [];
  }

  trackCategory(categoryValue) {
    if (!this.trackedCategories.includes(categoryValue)) {
      this.trackedCategories.push(categoryValue);
    }
  }

  untrackCategory(categoryValue) {
    this.trackedCategories = this.trackedCategories.filter(
      (c) => c !== categoryValue,
    );
  }

  addToHistory(deal) {
    const exists = this.dealHistory.some((d) => d.src_url === deal.src_url);
    if (!exists) {
      this.dealHistory.push(deal);
    }
  }
}

// Mock logged in user — swap this out for a DB fetch later
const currentUser = new User("carl", "john@example.com");
currentUser.trackedCategories = [
  "electronics-photo",
  "clothing",
  "home-garden",
];

// ── MOCK DATA ───────────────────────────────────────────────

const categories = [
  { label: "Automotive", value: "automotive" },
  { label: "Baby Products", value: "baby-products" },
  { label: "Beauty", value: "beauty" },
  { label: "Books", value: "books" },
  { label: "Clothing", value: "clothing" },
  { label: "Computers & Accessories", value: "computers-accessories" },
  { label: "DIY & Tools", value: "diy-tools" },
  { label: "Electronics & Photo", value: "electronics-photo" },
  { label: "Grocery", value: "grocery" },
  { label: "Health & Personal Care", value: "health-personal-care" },
  { label: "Home & Garden", value: "home-garden" },
  { label: "Jewellery", value: "jewellery" },
  { label: "Kindle Store", value: "kindle-store" },
  { label: "Large Appliances", value: "large-appliances" },
  { label: "Lighting", value: "lighting" },
  { label: "Luggage", value: "luggage" },
  { label: "Music", value: "music" },
  { label: "Musical Instruments & DJ", value: "musical-instruments-dj" },
  { label: "Other", value: "other" },
  { label: "PC & Video Games", value: "pc-video-games" },
  { label: "Pet Supplies", value: "pet-supplies" },
  { label: "Shoes & Bags", value: "shoes-bags" },
  { label: "Shops", value: "shops" },
  { label: "Software", value: "software" },
  { label: "Sports & Outdoors", value: "sports-outdoors" },
  {
    label: "Stationery & Office Supplies",
    value: "stationery-office-supplies",
  },
  { label: "Toys & Games", value: "toys-games" },
  { label: "Video", value: "video" },
];

const deals = [
  new Deal(
    "Sony WH-1000XM5 Headphones",
    "electronics-photo",
    "£349.00",
    "£219.00",
    "https://placehold.co/400x300",
    "https://amazon.co.uk",
  ),
  new Deal(
    "Nike Air Max 270",
    "clothing",
    "£109.99",
    "£49.99",
    "https://placehold.co/400x300",
    "https://nike.com",
  ),
  new Deal(
    "Instant Pot Duo 7-in-1",
    "home-garden",
    "£99.99",
    "£59.99",
    "https://placehold.co/400x300",
    "https://amazon.co.uk",
  ),
  new Deal(
    "Dyson V11 Vacuum",
    "home-garden",
    "£599.00",
    "£349.00",
    "https://placehold.co/400x300",
    "https://dyson.co.uk",
  ),
  new Deal(
    "Apple AirPods Pro (2nd Gen)",
    "electronics-photo",
    "£279.00",
    "£189.00",
    "https://placehold.co/400x300",
    "https://apple.com",
  ),
];

// ── CARDS ───────────────────────────────────────────────────

function createDealCard(deal, isHistory = false) {
  const card = document.createElement("div");
  card.className = "deal-card";

  const image = document.createElement("img");
  image.className = "deal-img";
  image.src = deal.img_url;
  image.alt = deal.name;

  const category = document.createElement("div");
  category.className = "badge-outline";
  category.textContent = deal.category;

  const dealName = document.createElement("div");
  dealName.className = "deal-title";
  dealName.textContent = deal.name;

  const dealCurrentPrice = document.createElement("div");
  dealCurrentPrice.className = "price-current";
  dealCurrentPrice.textContent = deal.currentPrice;

  const dealOriginalPrice = document.createElement("div");
  dealOriginalPrice.className = "price-original";
  dealOriginalPrice.textContent = deal.originalPrice;

  const dealLink = document.createElement("a");
  dealLink.href = deal.src_url;
  dealLink.textContent = "View Deal";
  dealLink.className = "btn-sm";

  dealLink.addEventListener("click", () => {
    if (!isHistory) {
      currentUser.addToHistory(deal);
      renderHistory();
    }
  });

  card.appendChild(image);
  card.appendChild(category);
  card.appendChild(dealName);
  card.appendChild(dealCurrentPrice);
  card.appendChild(dealOriginalPrice);
  card.appendChild(dealLink);

  return card;
}

// ── RENDER ──────────────────────────────────────────────────

function renderCard() {
  dealList.innerHTML = "";

  const cardsToRender =
    selectedCategories.length > 0
      ? allDeals.filter((deal) => selectedCategories.includes(deal.category))
      : allDeals;

  cardsToRender.forEach((deal) => {
    dealList.appendChild(createDealCard(deal));
  });
}

function renderHistory() {
  const historyList = document.querySelector("#tab-history");
  historyList.innerHTML = "";

  if (currentUser.dealHistory.length === 0) {
    historyList.innerHTML = "<p>No deals viewed yet.</p>";
    return;
  }

  currentUser.dealHistory.forEach((deal) => {
    const card = createDealCard(deal, true);
    historyList.appendChild(card);
  });
}

function getCategories() {
  categoryList.innerHTML = '<option value="">All Categories</option>';

  categories.forEach((category) => {
    const option = document.createElement("option");
    option.value = category.value;
    option.textContent = category.label;
    categoryList.appendChild(option);
  });
}

function renderName(user) {
  const opening = document.querySelector(".welcome");
  opening.innerHTML = `
    <h1>Welcome back, ${user.name}</h1>
    <p>You have 4 new deals waiting for you today</p>
  `;
  console.log(user.name);
}

function renderTrackedCategories(user) {
  const categoriesTrack = document.querySelector(".category-list");
  categoriesTrack.innerHTML = "";

  user.trackedCategories.forEach((categoryValue) => {
    const match = categories.find((c) => c.value === categoryValue);

    const categoryCard = document.createElement("div");
    categoryCard.className = "category-item";
    categoryCard.textContent = match ? match.label : categoryValue;

    categoriesTrack.appendChild(categoryCard);
  });
}

// ── EVENTS ──────────────────────────────────────────────────

categoryList.addEventListener("change", (e) => {
  const value = e.target.value;
  selectedCategories = value ? [value] : [];
  renderCard();
});

tabBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const target = btn.dataset.tab;

    tabBtns.forEach((b) => {
      b.classList.remove("active");
      b.setAttribute("aria-selected", "false");
    });
    tabPanels.forEach((p) => p.classList.remove("active"));

    btn.classList.add("active");
    btn.setAttribute("aria-selected", "true");
    document.getElementById("tab-" + target).classList.add("active");
  });
});

// ── INIT ────────────────────────────────────────────────────

allDeals = [...deals];
getCategories();
renderCard();
renderName(currentUser);
renderTrackedCategories(currentUser);
