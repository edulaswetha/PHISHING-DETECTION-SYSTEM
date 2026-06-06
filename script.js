/* ================================
   PHISHGUARD DETECTION ENGINE
================================ */

async function analyze() {
  const input = document.getElementById("inputBox").value.trim();
  if (!input) return;

  const loader = document.getElementById("loader");
  const resultBox = document.getElementById("result");
  const resultText = document.getElementById("resultText");

  loader.classList.remove("hidden");
  resultBox.classList.add("hidden");

  try {
    const res = await fetch("http://127.0.0.1:5000/analyze-chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input })
    });

    const data = await res.json();

    loader.classList.add("hidden");

    // Clean explanation formatting
    // Safe explanation handling
let explanation = data.explanation || "No explanation available.";

// Remove markdown symbols safely
explanation = explanation
  .replace(/###/g, "")
  .replace(/\*\*/g, "")
  .replace(/---/g, "");

// Split into lines
let lines = explanation.split("\n");

// Highlight numbered questions
let formatted = lines.map(line => {
  let trimmed = line.trim();

  if (/^\d+\./.test(trimmed)) {
    return `<br><br><strong style="font-size:16px;">${trimmed}</strong><br>`;
  }

  return trimmed + "<br>";
}).join("");

// Render result
resultText.innerHTML = `
  <div style="font-size:18px; font-weight:600; margin-bottom:20px;">
    ${data.prediction} (${data.confidence}% confidence)
  </div>
  <div style="line-height:1.8; font-size:15px; color:rgba(255,255,255,0.85); text-align:left;">
    ${formatted}
  </div>
`;

    resultBox.classList.remove("hidden");

  } catch (error) {
    loader.classList.add("hidden");
    console.error(error);
    alert("Frontend error. Check console.");
  }
}
/* ================================
   RESULT DISPLAY + TYPING EFFECT
================================ */

function showResult(prediction, confidence, explanation) {
  const resultBox = document.getElementById("result");
  const resultText = document.getElementById("resultText");
  const summaryText = document.getElementById("summaryText");

  resultBox.classList.remove("hidden");

  resultText.innerText =
    `${prediction} (${confidence}% confidence)`;

  // Clear old summary
  summaryText.innerText = "";

  // Typing effect
  let i = 0;
  function typeEffect() {
    if (i < explanation.length) {
      summaryText.innerText += explanation.charAt(i);
      i++;
      setTimeout(typeEffect, 15);
    }
  }

  typeEffect();
}


/* ================================
   SMOOTH TYPE EFFECT
================================ */

function typeEffect(text) {
  const el = document.getElementById("resultText");
  el.innerHTML = "";
  let i = 0;

  function typing() {
    if (i < text.length) {
      el.innerHTML += text.charAt(i);
      i++;
      setTimeout(typing, 15);
    }
  }

  typing();
}


/* ================================
   DRAG & DROP SUPPORT
================================ */

function handleDrop(event) {
  event.preventDefault();
  const text = event.dataTransfer.getData("text");
  document.getElementById("inputBox").value = text;
}


/* ================================
   VANTA FADE ON SCROLL
================================ */

window.addEventListener("scroll", function () {
  const canvas = document.querySelector("canvas");
  if (!canvas) return;

  const scrollY = window.scrollY;
  const fadeStart = 0;
  const fadeEnd = 400;

  let opacity = 1 - (scrollY - fadeStart) / (fadeEnd - fadeStart);

  if (opacity < 0) opacity = 0;
  if (opacity > 1) opacity = 1;

  canvas.style.transition = "opacity 0.3s ease";
  canvas.style.opacity = opacity;
});

async function loginUser() {
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value.trim();

  if (!email || !password) {
    alert("Please enter email and password");
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/login-user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (res.ok) {
      alert("Login successful!");
      window.location.href = "detect.html";
    } else {
      alert(data.error || "Login failed");
    }

  } catch (err) {
    alert("Server error");
  }
}

async function signupUser() {
  const username = document.getElementById("signupUsername").value.trim();
  const email = document.getElementById("signupEmail").value.trim();
  const password = document.getElementById("signupPassword").value.trim();

  if (!username || !email || !password) {
    alert("Please fill all fields");
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/signup-user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ username, email, password })
    });

    const data = await res.json();

    if (res.ok) {
      alert("Account created successfully! Redirecting to login...");
      setTimeout(() => {
        window.location.href = "login.html";
      }, 1000);
    } else {
      alert(data.error || "Signup failed");
    }

  } catch (err) {
    alert("Server error");
  }
}

async function checkLoginStatus() {
  try {
    const res = await fetch("http://127.0.0.1:5000/get-user", {
      credentials: "include"
    });
    const data = await res.json();

    if (data.logged_in) {
      document.getElementById("loginNav").style.display = "none";
      document.getElementById("signupNav").style.display = "none";
      document.getElementById("userNav").style.display = "flex";

      document.getElementById("usernameDisplay").innerText =
        "Hi, " + data.username;
    }
  } catch (err) {
    console.log("Login check failed");
  }
}

async function logoutUser() {
  await fetch("http://127.0.0.1:5000/logout-user", {
    credentials: "include"
  });
  window.location.reload();
}

document.addEventListener("DOMContentLoaded", checkLoginStatus);
