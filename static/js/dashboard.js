// ── Global chart defaults ──────────────────────────────────
Chart.defaults.color       = '#5a6a7a';
Chart.defaults.font.family = 'DM Sans, sans-serif';
Chart.defaults.font.size   = 11;

const C = {
  yellow:  '#e8ff5a',
  cyan:    '#06b6d4',
  green:   '#10b981',
  purple:  '#a855f7',
  orange:  '#f97316',
  red:     '#f43f5e',
  blue:    '#3b82f6',
  teal:    '#14b8a6',
  grid:    'rgba(255,255,255,.05)',
  surface: '#0d1117'
};

const PALETTE = [C.yellow, C.cyan, C.green, C.purple, C.orange, C.red, C.blue, C.teal];

function gridOpts() {
  return { color: C.grid, drawBorder: false };
}

function tickOpts() {
  return { color: '#3a4a5a' };
}

// stored chart instances
const charts = {};

// ── Number formatter ──────────────────────────────────────
function fmt(n) {
  if (n >= 1e7) return (n / 1e7).toFixed(1) + 'Cr';
  if (n >= 1e5) return (n / 1e5).toFixed(1) + 'L';
  if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
  return String(Math.round(n));
}

// ── KPIs ──────────────────────────────────────────────────
async function loadKPIs() {
  const d = await fetch('/api/kpis').then(r => r.json());
  document.getElementById('kTotal').textContent = d.total.toLocaleString();
  document.getElementById('kAvg').textContent   = fmt(d.avg_price);
  document.getElementById('kMed').textContent   = fmt(d.med_price);
  document.getElementById('kCols').textContent  = d.columns;
  document.getElementById('kMiss').textContent  = d.missing.toLocaleString();
  document.getElementById('liveRec').textContent = d.total.toLocaleString() + ' records';
}

// ── Price Distribution ────────────────────────────────────
async function loadPriceDist() {
  const d = await fetch('/api/price_dist').then(r => r.json());
  if (d.error) return;
  if (charts.pd) charts.pd.destroy();
  charts.pd = new Chart(document.getElementById('cPriceDist'), {
    type: 'bar',
    data: {
      labels: d.labels,
      datasets: [{
        data: d.values,
        backgroundColor: C.yellow + '22',
        borderColor: C.yellow,
        borderWidth: 1.5,
        borderRadius: 4,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false },
        tooltip: { callbacks: { label: ctx => ' Count: ' + ctx.parsed.y } }
      },
      scales: {
        x: { grid: gridOpts(), ticks: { ...tickOpts(), maxRotation: 35, maxTicksLimit: 8 } },
        y: { grid: gridOpts(), ticks: tickOpts() }
      }
    }
  });
}

// ── Bedroom Doughnut ──────────────────────────────────────
async function loadBedroom() {
  const d = await fetch('/api/bedrooms').then(r => r.json());
  if (d.error) return;
  if (charts.bed) charts.bed.destroy();
  charts.bed = new Chart(document.getElementById('cBedroom'), {
    type: 'doughnut',
    data: {
      labels: d.labels,
      datasets: [{
        data: d.values,
        backgroundColor: PALETTE.map(c => c + '33'),
        borderColor: PALETTE,
        borderWidth: 2,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      cutout: '65%',
      plugins: {
        legend: { position: 'bottom', labels: { padding: 14, usePointStyle: true, pointStyleWidth: 8 } }
      }
    }
  });
}

// ── Avg by Category ───────────────────────────────────────
async function loadAvgCat() {
  const d = await fetch('/api/avg_by_cat').then(r => r.json());
  if (d.error) return;
  if (charts.ac) charts.ac.destroy();
  charts.ac = new Chart(document.getElementById('cAvgCat'), {
    type: 'bar',
    data: {
      labels: d.labels,
      datasets: [{
        data: d.values,
        backgroundColor: PALETTE.map(c => c + '33'),
        borderColor: PALETTE,
        borderWidth: 1.5,
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: { legend: { display: false },
        tooltip: { callbacks: { label: ctx => ' ' + fmt(ctx.parsed.x) } }
      },
      scales: {
        x: { grid: gridOpts(), ticks: { ...tickOpts(), callback: v => fmt(v) } },
        y: { grid: gridOpts(), ticks: tickOpts() }
      }
    }
  });
}

// ── Top Locations ─────────────────────────────────────────
async function loadLocations() {
  const d = await fetch('/api/top_locations').then(r => r.json());
  if (d.error) return;
  if (charts.loc) charts.loc.destroy();
  charts.loc = new Chart(document.getElementById('cLocations'), {
    type: 'bar',
    data: {
      labels: d.labels,
      datasets: [{
        data: d.values,
        backgroundColor: C.cyan + '22',
        borderColor: C.cyan,
        borderWidth: 1.5,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false },
        tooltip: { callbacks: { label: ctx => ' ' + fmt(ctx.parsed.y) } }
      },
      scales: {
        x: { grid: gridOpts(), ticks: { ...tickOpts(), maxRotation: 30 } },
        y: { grid: gridOpts(), ticks: { ...tickOpts(), callback: v => fmt(v) } }
      }
    }
  });
}

// ── Price Trend ───────────────────────────────────────────
async function loadTrend() {
  const d = await fetch('/api/trend').then(r => r.json());
  if (d.error) return;
  if (charts.tr) charts.tr.destroy();
  charts.tr = new Chart(document.getElementById('cTrend'), {
    type: 'line',
    data: {
      labels: d.labels,
      datasets: [{
        data: d.values,
        borderColor: C.green,
        backgroundColor: C.green + '12',
        fill: true,
        tension: 0.45,
        pointRadius: 0,
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false },
        tooltip: { callbacks: { label: ctx => ' ' + fmt(ctx.parsed.y) } }
      },
      scales: {
        x: { grid: gridOpts(), ticks: { ...tickOpts(), maxTicksLimit: 10 } },
        y: { grid: gridOpts(), ticks: { ...tickOpts(), callback: v => fmt(v) } }
      }
    }
  });
}

// ── Scatter ───────────────────────────────────────────────
async function loadScatter() {
  const d = await fetch('/api/scatter').then(r => r.json());
  if (d.error) return;
  const pts = d.x.map((x, i) => ({ x, y: d.y[i] }));
  if (charts.sc) charts.sc.destroy();
  charts.sc = new Chart(document.getElementById('cScatter'), {
    type: 'scatter',
    data: {
      datasets: [{
        label: 'Properties',
        data: pts,
        backgroundColor: C.purple + '55',
        borderColor: C.purple + 'aa',
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: {
          grid: gridOpts(),
          ticks: { ...tickOpts(), callback: v => fmt(v) },
          title: { display: true, text: 'Area', color: '#3a4a5a' }
        },
        y: {
          grid: gridOpts(),
          ticks: { ...tickOpts(), callback: v => fmt(v) },
          title: { display: true, text: 'Price', color: '#3a4a5a' }
        }
      }
    }
  });
}

// ── Table ─────────────────────────────────────────────────
let allRows = [];

async function loadTable() {
  const d = await fetch('/api/table').then(r => r.json());
  const head = document.getElementById('tHead');
  const body = document.getElementById('tBody');

  head.innerHTML = '<tr>' + d.columns.map(c =>
    `<th>${c.replace(/_/g,' ')}</th>`
  ).join('') + '</tr>';

  body.innerHTML = d.rows.map(row =>
    '<tr>' + row.map(cell => `<td>${cell}</td>`).join('') + '</tr>'
  ).join('');

  allRows = Array.from(body.querySelectorAll('tr'));
}

function filterTable() {
  const q = document.getElementById('searchBox').value.toLowerCase();
  allRows.forEach(tr => {
    tr.style.display = tr.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
}

// ── Price Filter ──────────────────────────────────────────
function applyFilter() {
  const min = parseFloat(document.getElementById('minP').value) || -Infinity;
  const max = parseFloat(document.getElementById('maxP').value) || Infinity;
  // Highlight KPI feedback
  document.getElementById('kAvg').style.color = '#e8ff5a';
  setTimeout(() => document.getElementById('kAvg').style.color = '', 600);
  console.log('Filter:', min, '–', max);
}

function resetFilter() {
  document.getElementById('minP').value = '';
  document.getElementById('maxP').value = '';
}

// ── Sidebar active on scroll ──────────────────────────────
window.addEventListener('scroll', () => {
  const sections = ['overview','charts','scatter','table-section'];
  const navItems = document.querySelectorAll('.nav-item');
  let current = sections[0];
  sections.forEach(id => {
    const el = document.getElementById(id);
    if (el && el.getBoundingClientRect().top < 120) current = id;
  });
  navItems.forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === '#' + current);
  });
});

// ── Init ──────────────────────────────────────────────────
(async function init() {
  await loadKPIs();
  loadPriceDist();
  loadBedroom();
  loadAvgCat();
  loadLocations();
  loadTrend();
  loadScatter();
  loadTable();
})();
