/* ------------------------------------------------------
   FINALE AUTH-LOGIC.JS — SOVEREIGN FUSION
   Hält alle gesendeten Codes zusammen und aktiviert die Buttons.
   ------------------------------------------------------ */

window.isLoggedIn = false;
window.currentUser = null;
window.activeSection = 'chain'; 
const ADMIN_ID = "@RFOF-NETWORK";

/**
 * 1. UI-UPDATE & ADMIN-BRANDING
 * Sorgt dafür, dass @RFOF-NETWORK visuell verankert wird.
 */
window.updateView = function() {
    const headerTitle = document.querySelector("header > div");
    
    if (window.isLoggedIn && window.currentUser === ADMIN_ID) {
        headerTitle.style.color = "var(--accent-violet)";
        headerTitle.style.textShadow = "0 0 15px rgba(168, 107, 255, 0.8)";
        headerTitle.innerText = "AI-Chain — Sovereign: " + ADMIN_ID;
    } else {
        headerTitle.style.color = "var(--accent-blue)";
        headerTitle.innerText = "AI-Chain – RFOF System";
    }

    // Detail-Ansicht im Viewer aufräumen, wenn Sektion gewechselt wird
    if (window.activeSection !== 'chain') {
        const details = document.getElementById("block-details");
        if (details) details.innerHTML = "";
    }
};

/**
 * 2. BLOCK-DETAILS (ANKLICKBARKEIT)
 * Wird von deinem Python-Code (show_block_details) getriggert.
 */
window.show_block_details_js = function(blockData) {
    const detailsContainer = document.getElementById("block-details");
    if (!detailsContainer) return;

    detailsContainer.innerHTML = "";
    const pre = document.createElement("pre");
    pre.textContent = JSON.stringify(blockData, null, 2);
    detailsContainer.appendChild(pre);
    
    detailsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
};

/**
 * 3. SEKTIONS-STEUERUNG (NAVIGATION)
 * Regelt das Umschalten zwischen Chain, Wallet, Market und Settings.
 */
window.showSection = function(name) {
    window.activeSection = name;
    
    // Alle Sektionen verstecken
    document.querySelectorAll(".section").forEach(s => s.classList.add("hidden"));
    // Alle Nav-Links deaktivieren
    document.querySelectorAll("nav a").forEach(n => n.classList.remove("active"));

    // Ziel-Sektion anzeigen
    const activeEl = document.getElementById("section-" + name);
    const activeNav = document.getElementById("nav-" + name);
    
    if (activeEl) activeEl.classList.remove("hidden");
    if (activeNav) activeNav.classList.add("active");

    window.updateView();
};

/**
 * 4. AUTH-BRÜCKE (FÜR LOGIN & CREATE)
 * Diese Funktionen werden von deinen Python-Buttons aufgerufen.
 */
window.handleLoginSuccess = function(user, address) {
    window.isLoggedIn = true;
    window.currentUser = user;
    
    const addrEl = document.getElementById("wallet-address");
    if (addrEl) addrEl.innerHTML = `<strong>Address:</strong> ${address}`;
    
    window.updateView();
};

window.performLogout = function() {
    window.isLoggedIn = false;
    window.currentUser = null;
    
    const elementsToClear = ["wallet-address", "wallet-balances", "wallet-txs", "block-details"];
    elementsToClear.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = "";
    });

    window.showSection('chain');
};

// Initialisierung: Startpunkt ist immer die zentrale Blockchain
document.addEventListener("DOMContentLoaded", () => {
    window.showSection('chain');
});
