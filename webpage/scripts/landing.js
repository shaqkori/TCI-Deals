const tabBtns = document.querySelectorAll(".tab-btn");
const tabPanels = document.querySelectorAll(".tab-panel");
const dealList = document.querySelector(".deal-list");
const categoryList = document.getElementById("category-filter");

let allDeals = [];
let selectedCategories = [];
let history = [];

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
  dealOriginalPrice.className = "price-original line-through text-gray-400";
  dealOriginalPrice.textContent = deal.originalPrice;

  const dealLink = document.createElement("a");
  dealLink.href = deal.src_url;
  dealLink.textContent = "View Deal";
  dealLink.className = "btn-sm";

  card.addEventListener("click", () => {
    if (!isHistory) {
      addToHistory(deal);

      console.log(history);
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

function renderHistory() {
  const historyList = document.querySelector("#tab-history");
  historyList.innerHTML = "";

  if (history.length === 0) {
    return;
  }

  history.forEach((deal) => {
    const card = createDealCard(deal, true);
    historyList.appendChild(card);
  });
}

function addToHistory(deal) {
  const exists = history.some((d) => d.src_url === deal.src_url);
  if (!exists) {
    history.push(deal);
    renderHistory();
  }
}

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

function getCategories() {
  categoryList.innerHTML = "";

  categories.forEach((category) => {
    const option = document.createElement("option");
    option.value = category.value;
    option.textContent = category.label;
    categoryList.appendChild(option);
    //selectedCategories.push(option.value);
  });

  console.log(selectedCategories);
}

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

allDeals = [...deals];
renderCard();
getCategories();
