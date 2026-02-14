// hash-generator.js
// Autarkes Modul, das sich selbst in Login/Register einklinkt
// ohne bestehende Dateien zu verändern.

(function() {

  // -------------------------------
  // 1. Double SHA-256 (Browser)
  // -------------------------------
  async function doubleSHA256(input) {
    const encoder = new TextEncoder();
    const data = encoder.encode(input);

    const h1 = await crypto.subtle.digest("SHA-256", data);
    const h2 = await crypto.subtle.digest("SHA-256", h1);

    return Array.from(new Uint8Array(h2))
      .map(b => b.toString(16).padStart(2, "0"))
      .join("");
  }

  // -------------------------------
  // 2. Screenshot-Blocker (best effort)
  // -------------------------------
  function enableScreenshotBlocker() {
    document.addEventListener("keydown", (e) => {
      if (e.key === "PrintScreen") {
        navigator.clipboard.writeText("");
        alert("Screenshots sind deaktiviert.");
      }
    });

    document.addEventListener("keyup", () => {
      navigator.clipboard.writeText("");
    });
  }

  // -------------------------------
  // 3. Phrase-Datei erzeugen
  // -------------------------------
  function downloadPhraseFile(username, address, phrase, hash) {
    const content =
`AI-CHAIN / RFOF-GOLDEN PHRASE FILE

Username: ${username}
Address: ${address}

Phrase (24 words):
${phrase}

Phrase-Hash (double SHA-256):
${hash}

Hinweis:
Diese Datei wurde lokal erzeugt.
Der Server hat die Phrase niemals gesehen.
`;

    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `ai-chain-phrase-${username}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // -------------------------------
  // 4. Register-Hook (autark)
  // -------------------------------
  async function hookRegister() {
    const phraseEl = document.getElementById("register-mnemonic");
    const addrEl = document.getElementById("register-address");
    const userEl = document.querySelector("#register-form input[name='username']");

    if (!phraseEl || !addrEl || !userEl) return;

    // Wenn Phrase sichtbar wird → Hash erzeugen + Datei anbieten
    const observer = new MutationObserver(async () => {
      const phrase = phraseEl.textContent.trim();
      const address = addrEl.textContent.trim();
      const username = userEl.value.trim();

      if (phrase.split(" ").length >= 24 && address.length > 0) {
        const hash = await doubleSHA256(phrase);
        downloadPhraseFile(username, address, phrase, hash);
      }
    });

    observer.observe(phraseEl, { childList: true });
  }

  // -------------------------------
  // 5. Login-Hook (Admin-Phrase-Check)
  // -------------------------------
  function hookLogin() {
    const loginForm = document.getElementById("login-form");
    if (!loginForm) return;

    loginForm.addEventListener("submit", async (e) => {
      const pwd = loginForm.querySelector("input[name='password']").value;
      if (pwd.split(" ").length >= 24) {
        console.log("Admin-Phrase erkannt → Hash wird erzeugt.");
        const hash = await doubleSHA256(pwd);
        console.log("Admin-Phrase-Hash:", hash);
      }
    });
  }

  // -------------------------------
  // 6. Autostart
  // -------------------------------
  window.addEventListener("load", () => {
    enableScreenshotBlocker();
    hookRegister();
    hookLogin();
  });

})();

