const tabBtns = document.querySelectorAll(".tab-btn");
const tabPanels = document.querySelectorAll(".tab-panel");
const dealList = document.querySelector(".deal-list");

let allDeals = [];
let selectedCategories = [];

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

const deals = [
  new Deal(
    "Sony WH-1000XM5 Headphones",
    "Electronics",
    "£349.00",
    "£219.00",
    "https://example.com/images/sony-wh1000xm5.jpg",
    "https://amazon.co.uk/dp/sony-wh1000xm5",
  ),
  new Deal(
    "Nike Air Max 270",
    "Fashion",
    "£109.99",
    "£49.99",
    "https://example.com/images/nike-air-max.jpg",
    "https://nike.com/gb/t/air-max-270",
  ),
  new Deal(
    "Instant Pot Duo 7-in-1",
    "Home Appliances",
    "£99.99",
    "£59.99",
    "https://example.com/images/instant-pot.jpg",
    "https://amazon.co.uk/dp/instant-pot-duo",
  ),
  new Deal(
    "Dyson V11 Vacuum",
    "Home Appliances",
    "£599.00",
    "£349.00",
    "https://example.com/images/dyson-v11.jpg",
    "https://dyson.co.uk/vacuum-cleaners/dyson-v11",
  ),
  new Deal(
    "Apple AirPods Pro (2nd Gen)",
    "Electronics",
    "£279.00",
    "£189.00",
    "https://example.com/images/airpods-pro.jpg",
    "https://apple.com/uk/shop/airpods-pro",
  ),
];

function createDealCard(deal) {
  const card = document.createElement("div");
  card.className = "deal-card";

  const image = document.createElement("img");
  image.className = "deal-img";
  image.src = deal.img_url;
  image.alt = deal.name;

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

  card.appendChild(image);
  card.appendChild(dealName);
  card.appendChild(dealCurrentPrice);
  card.appendChild(dealOriginalPrice);
  card.appendChild(dealLink);

  return card;
}

function renderCard() {
  dealList.innerHTML = "";

  allDeals.forEach((deal) => {
    const card = createDealCard(deal);
    dealList.appendChild(card);
  });
}

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
