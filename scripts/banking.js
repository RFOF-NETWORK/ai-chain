// scripts/banking.js
// Fiat-Banking: EUR/USD <-> AI/COIN/AIC_LP

export function initBankingUI() {
  const depositForm = document.getElementById('fiat-deposit-form');
  const withdrawForm = document.getElementById('fiat-withdraw-form');

  if (depositForm) {
    depositForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(depositForm);
      const username = formData.get('username');
      const amount = parseFloat(formData.get('amount'));
      const currency = formData.get('currency');
      const token = formData.get('token'); // AI, COIN, AIC_LP

      const res = await fetch('/api/banking/deposit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ username, amount, currency, target_token: token })
      });

      const data = await res.json();
      console.log('Fiat deposit result:', data);
    });
  }

  if (withdrawForm) {
    withdrawForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(withdrawForm);
      const username = formData.get('username');
      const amount = parseFloat(formData.get('amount'));
      const currency = formData.get('currency');
      const token = formData.get('token'); // AI, COIN, AIC_LP

      const res = await fetch('/api/banking/withdraw', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ username, amount, currency, source_token: token })
      });

      const data = await res.json();
      console.log('Fiat withdraw result:', data);
    });
  }
}

