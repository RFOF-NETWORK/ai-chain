// scripts/ui.js
//
// UI‑Steuerlogik für die ai_chain‑Weboberfläche.
// Aufgaben:
// - API‑Requests an server.py / api/*
// - DOM‑Updates für Portfolio, Chain‑Viewer (PZQQET-Brücke)
// - Modal-Handling (Pop-Ups für Block-Details)
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
    try {
        const res = await fetch(`${API_BASE}${path}`);
        if (!res.ok) throw new Error("API Offline");
        return await res.json();
    } catch (e) {
        console.warn(`PZQQET-Info: API-Pfad ${path} nicht erreichbar, nutze ggf. Fallback.`);
        return null;
    }
}

async function apiPost(path, data) {
    try {
        const res = await fetch(`${API_BASE}${path}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        return await res.json();
    } catch (e) {
        return { status: "error", reason: "connection_failed" };
    }
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

    if (data) {
        $("portfolio_output").textContent = JSON.stringify(data, null, 2);

        // Charts aktualisieren
        if (window.updatePortfolioChart) {
            window.updatePortfolioChart(data.tokens);
        }
    }
}

// -----------------------------------------------------------------------------
// Chain‑Viewer & Pop-Up Logik (Welle 1 & 2 Integration)
// -----------------------------------------------------------------------------

/**
 * Aktualisiert den Chain-Viewer im UI. 
 * Nutzt rfof_chain_data (Python-Brücke aus main.py) oder API /chain/last.
 */
async function update_chain_viewer() {
    const container = $("blocks-container") || $("chain_output");
    if (!container) return;

    // 1. Versuch: API Daten (für spätere Wellen)
    let chainData = await apiGet(`/chain/last?limit=10`);

    // 2. Fallback: Interne VM-Daten (Sofort-Anzeige für Welle 1 & 2)
    if (!chainData && window.rfof_chain_data) {
        chainData = window.rfof_chain_data.chain;
    }

    if (chainData) {
        if ($("blocks-container")) {
            $("blocks-container").innerHTML = ""; 
            chainData.forEach(block => {
                const blockEl = document.createElement("div");
                blockEl.className = "block-card"; 
                blockEl.innerHTML = `
                    <div class="block-header">Block #${block.index}</div>
                    <div class="block-hash">${block.hash.substring(0, 16)}...</div>
                `;
                blockEl.onclick = () => showBlockDetails(block);
                $("blocks-container").appendChild(blockEl);
            });
        } else if ($("chain_output")) {
            $("chain_output").textContent = JSON.stringify(chainData, null, 2);
        }
    }
}

/**
 * Zeigt das Pop-Up (Modal) mit Block-Details an.
 */
function showBlockDetails(block) {
    const modal = $("block-modal");
    if (!modal) {
        alert(`Block #${block.index}\nHash: ${block.hash}\nData: ${JSON.stringify(block.data)}`);
        return;
    }

    if ($("modal-title")) $("modal-title").textContent = `Details Block #${block.index}`;
    if ($("modal-content")) {
        $("modal-content").innerHTML = `
            <p><strong>Hash:</strong> ${block.hash}</p>
            <p><strong>Previous:</strong> ${block.previous_hash || '---'}</p>
            <p><strong>Timestamp:</strong> ${new Date(block.timestamp * 1000).toLocaleString()}</p>
            <hr>
            <pre style="background: #1a1a1a; padding: 10px; border-radius: 5px; color: #00ff00;">${JSON.stringify(block.data, null, 2)}</pre>
        `;
    }
    modal.style.display = "block";
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
    if ($("login_result")) $("login_result").textContent = JSON.stringify(result, null, 2);
}

async function logout() {
    const result = await apiGet("/auth/logout");
    if ($("logout_result")) $("logout_result").textContent = JSON.stringify(result, null, 2);
}

async function registerUser() {
    const user = $("reg_user").value.trim();
    const pw = $("reg_pw").value.trim();

    const result = await apiPost("/auth/register", { user, pw });
    if ($("register_result")) $("register_result").textContent = JSON.stringify(result, null, 2);
}

// -----------------------------------------------------------------------------
// Export für HTML & Initialisierung
// -----------------------------------------------------------------------------

// Modal schließen bei Klick außerhalb des Fensters
window.onclick = function(event) {
    const modal = $("block-modal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

// Globaler Export für HTML-Attribute (onclick)
Object.assign(window, {
    loadPortfolio,
    loadLastBlocks: update_chain_viewer,
    update_chain_viewer,
    sendTransaction,
    addLiquidity,
    removeLiquidity,
    login,
    logout,
    registerUser
});

// Automatischer Start beim Laden, um Genesis-Block zu zeigen
document.addEventListener("DOMContentLoaded", () => {
    setTimeout(update_chain_viewer, 500); // Delay für PyScript/VM-Initialisierung
});
