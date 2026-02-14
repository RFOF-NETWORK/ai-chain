// scripts/login.js
// Ein Login-Formular, ein Passwortfeld (Passwort ODER Phrase für Admin)

export function initLoginForm() {
  const form = document.getElementById('login-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const username = formData.get('username');
    const password = formData.get('password'); // kann Phrase sein (Admin) oder Passwort (User)

    const res = await fetch('/api/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    console.log('Login result:', data);

    if (data.status === 'ok') {
      // Hier kannst du Session/LocalStorage setzen
      // z.B. localStorage.setItem('address', data.address);
    } else {
      // Fehleranzeige im UI
      const errEl = document.getElementById('login-error');
      if (errEl) errEl.textContent = data.error || 'Login fehlgeschlagen';
    }
  });
}

