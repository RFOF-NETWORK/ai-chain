// scripts/dex.js
// DEX/Bridge-UI: Swaps AI/COIN/AIC_LP <-> externe Tokens

export function initDexUI() {
  const swapForm = document.getElementById('dex-swap-form');
  if (!swapForm) return;

  swapForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(swapForm);
    const fromToken = formData.get('from_token'); // AI, COIN, AIC_LP
    const toToken = formData.get('to_token');     // externes Symbol
    const amount = parseFloat(formData.get('amount'));

    const res = await fetch('/api/dex/swap', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ from_token: fromToken, to_token: toToken, amount })
    });

    const data = await res.json();
    console.log('DEX swap result:', data);
  });
}

