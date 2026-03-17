// core/static/core/js/dashboard.js

// Category filter — filters cards already rendered by Django
document.getElementById("category-filter").addEventListener("change", (e) => {
  const value = e.target.value;
  document.querySelectorAll(".deal-card").forEach((card) => {
    card.style.display =
      !value || card.dataset.category === value ? "" : "none";
  });
});

// Track history when View Deal is clicked
document.querySelectorAll(".deal-link").forEach((link) => {
  link.addEventListener("click", () => {
    fetch(`/deals/${link.dataset.dealId}/history/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/json",
      },
    });
  });
});

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}
