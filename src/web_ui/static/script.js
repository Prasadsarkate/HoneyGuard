async function loadAlerts() {
  const res = await fetch('/api/alerts');
  const data = await res.json();
  const tbody = document.querySelector('#alerts tbody');
  tbody.innerHTML = '';
  for (const item of data) {
    const tr = document.createElement('tr');
    const ts = item.ts || '';
    const level = item.level || '';
    const msg = item.message || item.text || '';
    const extra = JSON.stringify(item, null, 2);
    tr.innerHTML = `<td>${ts}</td><td>${level}</td><td>${msg}</td><td><code>${extra}</code></td>`;
    tbody.appendChild(tr);
  }
}
document.getElementById('refresh').addEventListener('click', loadAlerts);
loadAlerts();
