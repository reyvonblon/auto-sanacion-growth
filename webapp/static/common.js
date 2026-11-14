async function apiRequest(url, options = {}) {
  const opts = {
    headers: { "Content-Type": "application/json" },
    ...options,
  };
  const res = await fetch(url, opts);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error || `Error HTTP ${res.status}`);
  }
  return data;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function showToast(message) {
  let el = document.getElementById("global-toast");
  if (!el) {
    el = document.createElement("div");
    el.id = "global-toast";
    el.className = "toast";
    el.setAttribute("role", "status");
    document.body.appendChild(el);
  }
  el.textContent = message;
  el.hidden = false;
  clearTimeout(window.__toastTimer);
  window.__toastTimer = setTimeout(() => {
    el.hidden = true;
  }, 3400);
}

function toEmbedUrl(rawUrl) {
  const url = String(rawUrl || "").trim();
  if (!url) return "";
  try {
    const parsed = new URL(url);
    if (parsed.hostname.includes("youtube.com")) {
      const vid = parsed.searchParams.get("v");
      if (vid) return `https://www.youtube.com/embed/${vid}`;
    }
    if (parsed.hostname === "youtu.be") {
      const vid = parsed.pathname.replace("/", "");
      if (vid) return `https://www.youtube.com/embed/${vid}`;
    }
    if (parsed.hostname.includes("vimeo.com")) {
      const vid = parsed.pathname.split("/").filter(Boolean)[0];
      if (vid) return `https://player.vimeo.com/video/${vid}`;
    }
  } catch {
    return "";
  }
  return url;
}

function stageLabel(stage) {
  const labels = {
    nuevo_lead: "Nuevo interesado",
    leyendo_libro: "Leyendo el libro",
    en_escuela: "En la Escuela",
    comprador_verificado: "Compró / Reseñó",
  };
  return labels[stage] || stage;
}
