// scripts/register.js
// Registrierung: erzeugt 24-Wort-Phrase + Wallet-Adresse, zeigt Phrase einmalig an

export function initRegisterForm() {
  const form = document.getElementById('register-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const username = formData.get('username');
    const password = formData.get('password');

    const res = await fetch('/api/register', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    console.log('Register result:', data);

    const errEl = document.getElementById('register-error');
    const phraseEl = document.getElementById('register-mnemonic');
    const addrEl = document.getElementById('register-address');

    if (data.status !== 'ok') {
      if (errEl) errEl.textContent = data.error || 'Registrierung fehlgeschlagen';
      return;
    }

    if (addrEl) addrEl.textContent = data.address;
    if (phraseEl) {
      phraseEl.textContent = data.mnemonic.join(' ');
      // Hinweis im UI: "Diese Phrase wird nur einmal angezeigt – jetzt sichern!"
    }
  });
}
