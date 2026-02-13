// scripts/admin.js
// Admin-Dashboard: Admin-Info + Admin-Portfolio

export async function initAdminDashboard() {
  const addrEl = document.getElementById('admin-address');
  const userEl = document.getElementById('admin-username');
  const roleEl = document.getElementById('admin-role');
  const ownerEl = document.getElementById('admin-owner-balance');
  const fundEl = document.getElementById('admin-fund-balance');
  const safeEl = document.getElementById('admin-safe-value');

  try {
    const infoRes = await fetch('/api/admin/info');
    const infoData = await infoRes.json();

    if (infoData.status === 'ok' && infoData.admin) {
      const admin = infoData.admin;
      if (addrEl) addrEl.textContent = admin.admin_address || '';
      if (userEl) userEl.textContent = admin.admin_username || '';
      if (roleEl) roleEl.textContent = admin.role || '';
    }

    const portRes = await fetch('/api/admin/portfolio');
    const portData = await portRes.json();

    if (portData.status === 'ok') {
      if (ownerEl) ownerEl.textContent = portData.owner_balance ?? '0';
      if (fundEl) fundEl.textContent = portData.fund_balance ?? '0';
      if (safeEl) safeEl.textContent = portData.safe_value ?? '0';
    }
  } catch (e) {
    console.error('Admin dashboard init failed', e);
  }
}
