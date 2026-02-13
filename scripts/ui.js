// scripts/ui.js
//
// UI‑Steuerlogik für die ai_chain‑Weboberfläche.
// Aufgaben:
// - API‑Requests an server.py / api/*
// - DOM‑Updates für Portfolio, Chain‑Viewer, Liquidity‑Infos
// - Event‑Handler für Buttons, Inputs, Forms
//
// Hinweis:
// Diese Datei ist bewusst leichtgewichtig gehalten.
// charts.js übernimmt Visualisierungen, ui.js übernimmt Logik + DOM.

const API_BASE = "/api";

// -----------------------------------------------------------------------------
// Hilfsfunktionen
// -----------------------------------------------------------------------------

async function apiGet(path) {
    const res = await fetch(`${API_BASE}${path}`);
    return await res.json();
}

async function apiPost(path, data) {
    const res = await fetch(`${API_BASE}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    return await res.json();
}

function $(id) {
    return document.getElementById(id);
}

// -----------------------------------------------------------------------------
// Portfolio laden
// -----------------------------------------------------------------------------

async function loadPortfolio() {
    const address = $("address_input").value.trim();
    if (!address) {
        alert("Bitte Adresse eingeben.");
        return;
    }

    const data = await apiGet(`/portfolio?address=${address}`);

    $("portfolio_output").textContent = JSON.stringify(data, null, 2);

    // Charts aktualisieren
    if (window.updatePortfolioChart) {
        window.updatePortfolioChart(data.tokens);
    }
}

// -----------------------------------------------------------------------------
// Chain‑Viewer
// -----------------------------------------------------------------------------

async function loadLastBlocks() {
    const limit = parseInt($("block_limit").value) || 10;
    const data = await apiGet(`/chain/last?limit=${limit}`);

    $("chain_output").textContent = JSON.stringify(data, null, 2);
}

// -----------------------------------------------------------------------------
// Transaktion senden
// -----------------------------------------------------------------------------

async function sendTransaction() {
    const from = $("tx_from").value.trim();
    const to = $("tx_to").value.trim();
    const amount = parseFloat($("tx_amount").value);
    const token = $("tx_token").value.trim();

    if (!from || !to || !amount) {
        alert("Bitte alle Felder ausfüllen.");
        return;
    }

    const result = await apiPost("/tx/submit", {
        from,
        to,
        amount,
        token
    });

    $("tx_result").textContent = JSON.stringify(result, null, 2);
}

// -----------------------------------------------------------------------------
// Liquidity
// -----------------------------------------------------------------------------

async function addLiquidity() {
    const provider = $("lp_provider").value.trim();
    const ai = parseFloat($("lp_ai").value);
    const coin = parseFloat($("lp_coin").value);

    if (!provider || !ai || !coin) {
        alert("Bitte alle Felder ausfüllen.");
        return;
    }

    const result = await apiPost("/lp/add", {
        provider,
        amount_ai: ai,
        amount_coin: coin
    });

    $("lp_result").textContent = JSON.stringify(result, null, 2);
}

async function removeLiquidity() {
    const provider = $("lp_provider_remove").value.trim();
    const share = parseFloat($("lp_share").value);

    if (!provider || !share) {
        alert("Bitte alle Felder ausfüllen.");
        return;
    }

    const result = await apiPost("/lp/remove", {
        provider,
        share
    });

    $("lp_result_remove").textContent = JSON.stringify(result, null, 2);
}

// -----------------------------------------------------------------------------
// Login / Logout / Register
// -----------------------------------------------------------------------------

async function login() {
    const user = $("login_user").value.trim();
    const pw = $("login_pw").value.trim();

    const result = await apiPost("/auth/login", { user, pw });
    $("login_result").textContent = JSON.stringify(result, null, 2);
}

async function logout() {
    const result = await apiGet("/auth/logout");
    $("logout_result").textContent = JSON.stringify(result, null, 2);
}

async function registerUser() {
    const user = $("reg_user").value.trim();
    const pw = $("reg_pw").value.trim();

    const result = await apiPost("/auth/register", { user, pw });
    $("register_result").textContent = JSON.stringify(result, null, 2);
}

// -----------------------------------------------------------------------------
// Export für HTML
// -----------------------------------------------------------------------------

window.loadPortfolio = loadPortfolio;
window.loadLastBlocks = loadLastBlocks;
window.sendTransaction = sendTransaction;
window.addLiquidity = addLiquidity;
window.removeLiquidity = removeLiquidity;
window.login = login;
window.logout = logout;
window.registerUser = registerUser;
      
