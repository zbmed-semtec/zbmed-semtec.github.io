// Lightweight interactivity for the site (no external deps).

function zbNormalize(s) {
  return (s || "")
    .toString()
    .toLowerCase()
    .normalize("NFKD")
    .replace(/\p{Diacritic}/gu, "");
}

// ── Card filtering ────────────────────────────────────────────────────────────
function setupZbCardFiltering() {
  const root = document.querySelector("[data-zb-filter-root]");
  if (!root) return;

  const input = root.querySelector("[data-zb-filter-input]");
  const cards = Array.from(root.querySelectorAll("[data-zb-card]"));
  const status = root.querySelector("[data-zb-filter-status]");
  if (!input || cards.length === 0) return;

  const index = cards.map((card) => ({
    card,
    haystack: zbNormalize(card.getAttribute("data-zb-haystack") || card.textContent || ""),
  }));

  function apply() {
    const q = zbNormalize(input.value).trim();
    let shown = 0;
    for (const item of index) {
      const ok = q === "" || item.haystack.includes(q);
      if (ok && item.card.style.display === "none") {
        item.card.style.display = "";
        item.card.animate(
          [{ opacity: 0, transform: "scale(0.93)" }, { opacity: 1, transform: "none" }],
          { duration: 220, easing: "cubic-bezier(0.22,1,0.36,1)", fill: "both" }
        );
      } else if (!ok) {
        item.card.style.display = "none";
      }
      if (ok) shown += 1;
    }
    if (status) status.textContent = q ? `${shown}/${cards.length} shown` : "";
  }

  input.addEventListener("input", apply, { passive: true });
  apply();
}

// ── Hero card mouse-glow ──────────────────────────────────────────────────────
function setupZbHeroCardGlow() {
  const cards = Array.from(document.querySelectorAll(".zb-card--hero"));
  if (cards.length === 0) return;

  for (const card of cards) {
    card.addEventListener(
      "pointermove",
      (e) => {
        const r = card.getBoundingClientRect();
        const x = ((e.clientX - r.left) / Math.max(1, r.width)) * 100;
        const y = ((e.clientY - r.top) / Math.max(1, r.height)) * 100;
        card.style.setProperty("--zb-x", `${x}%`);
        card.style.setProperty("--zb-y", `${y}%`);
      },
      { passive: true }
    );
  }
}

// ── Scroll progress bar ───────────────────────────────────────────────────────
function setupZbScrollProgress() {
  const bar = document.createElement("div");
  bar.className = "zb-progress";
  document.body.appendChild(bar);

  let ticking = false;
  window.addEventListener(
    "scroll",
    () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        const scrolled = window.scrollY;
        const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
        bar.style.width = Math.min(100, (scrolled / max) * 100) + "%";
        ticking = false;
      });
    },
    { passive: true }
  );
}

// ── Scroll reveal (IntersectionObserver) ─────────────────────────────────────
function setupZbScrollReveal() {
  const items = document.querySelectorAll(".zb-reveal");
  if (!items.length) return;

  const obs = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add("zb-visible");
          obs.unobserve(entry.target);
        }
      }
    },
    { threshold: 0.1 }
  );

  for (const item of items) obs.observe(item);
}

// ── Animated counters ─────────────────────────────────────────────────────────
function animateCount(el, target, duration) {
  const start = performance.now();
  const tick = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(eased * target);
    if (progress < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

function setupZbCounters() {
  const counters = document.querySelectorAll("[data-zb-counter]");
  if (!counters.length) return;

  const obs = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          const target = parseInt(entry.target.getAttribute("data-zb-counter"), 10);
          animateCount(entry.target, target, 1100);
          obs.unobserve(entry.target);
        }
      }
    },
    { threshold: 0.6 }
  );

  for (const counter of counters) obs.observe(counter);
}

// ── Cycling typing effect ─────────────────────────────────────────────────────
function setupZbTyping() {
  const el = document.querySelector("[data-zb-typing]");
  if (!el) return;

  const phrases = (el.getAttribute("data-zb-typing") || "").split("|").filter(Boolean);
  if (!phrases.length) return;

  let phraseIdx = 0;
  let charIdx = 0;
  let deleting = false;

  function tick() {
    const phrase = phrases[phraseIdx];
    if (!deleting) {
      charIdx++;
      el.textContent = phrase.slice(0, charIdx);
      if (charIdx === phrase.length) {
        deleting = true;
        setTimeout(tick, 2000);
        return;
      }
      setTimeout(tick, 80);
    } else {
      charIdx--;
      el.textContent = phrase.slice(0, charIdx);
      if (charIdx === 0) {
        deleting = false;
        phraseIdx = (phraseIdx + 1) % phrases.length;
        setTimeout(tick, 400);
        return;
      }
      setTimeout(tick, 45);
    }
  }

  setTimeout(tick, 800);
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  setupZbCardFiltering();
  setupZbHeroCardGlow();
  setupZbScrollProgress();
  setupZbScrollReveal();
  setupZbCounters();
  setupZbTyping();
});
