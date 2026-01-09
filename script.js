const BACKEND_URL = "http://localhost:5000/analyze";
const HEADLINES_URL = "http://localhost:5000/headlines";

const headlinesList = document.getElementById("headlinesList");
const customHeadline = document.getElementById("customHeadline");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultDiv = document.getElementById("result");

let selectedHeadline = null;
let headlines = [];

async function fetchHeadlines() {
  try {
    const response = await fetch(HEADLINES_URL);
    if (!response.ok) throw new Error("Failed to fetch headlines");
    headlines = await response.json();
    renderHeadlines();
  } catch (error) {
    console.error("Error fetching headlines:", error);
    resultDiv.textContent = "❌ Failed to load headlines from backend.";
  }
}

function renderHeadlines() {
  headlinesList.innerHTML = "";
  headlines.forEach((headline, index) => {
    const div = document.createElement("div");
    div.className = "headline-item";
    div.textContent = headline;
    div.style.animationDelay = `${index * 0.1}s`;
    div.onclick = () => selectHeadline(headline, div);
    headlinesList.appendChild(div);
  });
}

function selectHeadline(headline, element) {
  document.querySelectorAll(".headline-item").forEach(el => el.classList.remove("selected"));
  element.classList.add("selected");
  selectedHeadline = headline;
  customHeadline.value = headline;
}

async function analyzeHeadline() {
  const headline = customHeadline.value.trim();
  if (!headline) {
    resultDiv.textContent = "⚠️ Please enter or select a headline.";
    return;
  }

  analyzeBtn.disabled = true;
  resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Analyzing with AI...</div>';

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ headline })
    });

    if (!response.ok) throw new Error("Backend error");

    const data = await response.json();
    resultDiv.textContent = data.result || data.explanation || JSON.stringify(data, null, 2);
  } catch (error) {
    resultDiv.innerHTML = `❌ <strong>Error:</strong> Could not connect to backend.\n\n` +
      `Make sure your Python server is running at:\n<code>${BACKEND_URL}</code>\n\n` +
      `Run: <code>python app.py</code>`;
  } finally {
    analyzeBtn.disabled = false;
  }
}

analyzeBtn.addEventListener("click", analyzeHeadline);

// Allow Enter key to analyze
customHeadline.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && e.ctrlKey) {
    analyzeHeadline();
  }
});

fetchHeadlines();
