"""
עיצוב CSS מרכזי לאפליקציה
"""

MAIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');

* { font-family: 'Heebo', sans-serif !important; box-sizing: border-box; }
html, body { direction: rtl; background: #0a0e14; margin: 0; padding: 0; }
.stApp { background: #0a0e14 !important; }
[data-testid="stAppViewContainer"] { background: #0a0e14 !important; direction: rtl !important; }
[data-testid="stHeader"] { display: none !important; }
#MainMenu, footer, header { display: none !important; }
/* הסתרת כפתורי ניווט של streamlit */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

[data-testid="stMainBlockContainer"] {
    padding-top: 102px !important;
    padding-bottom: 70px !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
}
[data-testid="stHorizontalBlock"] { gap: 1.5rem !important; }

[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #2ea043, #3fb950) !important;
    border: 1px solid #2ea043 !important;
    color: #fff !important;
    box-shadow: 0 2px 12px rgba(63,185,80,0.35) !important;
    font-weight: 700 !important; border-radius: 10px !important;
}
[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, #3fb950, #56d364) !important;
    transform: translateY(-2px) !important;
}
[data-testid="baseButton-secondary"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #8b949e !important;
    font-weight: 700 !important; border-radius: 10px !important;
}
[data-testid="baseButton-secondary"]:hover {
    background: #1c2128 !important; border-color: #3fb950 !important; color: #e6edf3 !important;
}
[data-testid="stFileUploaderDropzone"] button { display: none !important; }
[data-testid="stFileUploaderDropzone"] small  { display: none !important; }

.card {
    background: linear-gradient(160deg, #161b22 0%, #13181f 100%);
    border: 1px solid #21262d; border-radius: 16px; padding: 26px 30px; margin-bottom: 18px;
    direction: rtl; text-align: right; box-shadow: 0 4px 16px rgba(0,0,0,0.5);
    transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
}
.card:hover { border-color: #2ea043; box-shadow: 0 8px 28px rgba(0,0,0,0.6); transform: translateY(-2px); }
.card-header {
    color: #e6edf3; font-size: 1.05em; font-weight: 700; margin: 0 0 16px; padding-bottom: 12px;
    border-bottom: 1px solid #21262d; display: flex; align-items: center; gap: 10px;
}
.card-header i { color: #3fb950; }
.card p, .card li { color: #8b949e; font-size: 0.95em; line-height: 1.8; margin: 0; }
.card ul { padding-right: 20px; margin: 10px 0 0; }

.page-header {
    background: linear-gradient(135deg, #161b22, #1c2128); border: 1px solid #21262d;
    border-radius: 14px; padding: 22px 28px; margin-bottom: 24px;
    display: flex; align-items: center; gap: 18px; direction: rtl;
}
.page-header-icon {
    width: 48px; height: 48px; background: linear-gradient(135deg, #0d2818, #1a4731);
    border: 1px solid #2ea043; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4em; color: #3fb950; flex-shrink: 0;
}
.page-header h2 { color: #e6edf3; font-size: 1.5em; font-weight: 800; margin: 0 0 4px; }
.page-header p  { color: #8b949e; font-size: 0.9em; margin: 0; }

.hero {
    background: linear-gradient(135deg, #0a1a0f 0%, #0d2318 40%, #0a1a0f 100%);
    border: 1px solid #1a3a24; border-radius: 24px; padding: 80px 56px;
    text-align: center; margin-bottom: 28px; position: relative; overflow: hidden;
    box-shadow: 0 8px 40px rgba(0,0,0,0.6);
}
.hero::before {
    content: ''; position: absolute; top: -100px; left: 50%; transform: translateX(-50%);
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(63,185,80,0.08) 0%, transparent 65%);
    pointer-events: none;
}
.hero-icon {
    width: 88px; height: 88px; background: linear-gradient(135deg, #0d2818, #1a4731);
    border: 1px solid #2ea043; border-radius: 22px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 2.4em; margin-bottom: 24px; color: #3fb950;
}
.hero h1 { color: #e6edf3; font-size: 3em; font-weight: 900; margin: 0 0 18px; line-height: 1.2; }
.hero h1 span { color: #3fb950; text-shadow: 0 0 30px rgba(63,185,80,0.3); }
.hero p  { color: #8b949e; font-size: 1.08em; margin: 0 auto; max-width: 540px; line-height: 1.85; }

.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
.stat-box {
    background: linear-gradient(160deg, #161b22, #13181f); border: 1px solid #21262d;
    border-radius: 16px; padding: 28px 24px; text-align: center;
    transition: border-color 0.25s, transform 0.25s; box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    position: relative; overflow: hidden;
}
.stat-box::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #3fb950, transparent); opacity: 0; transition: opacity 0.25s;
}
.stat-box:hover { border-color: #3fb950; transform: translateY(-4px); }
.stat-box:hover::before { opacity: 1; }
.stat-box .num { color: #3fb950; font-size: 2.4em; font-weight: 900; line-height: 1; }
.stat-box .lbl { color: #8b949e; font-size: 0.85em; margin-top: 10px; }

.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-bottom: 28px; }
.feature-card {
    background: linear-gradient(160deg, #161b22, #13181f); border: 1px solid #21262d;
    border-radius: 16px; padding: 30px 22px; text-align: center;
    transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4); position: relative; overflow: hidden;
}
.feature-card::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #3fb950, transparent); opacity: 0; transition: opacity 0.25s;
}
.feature-card:hover { border-color: #2ea043; transform: translateY(-5px); }
.feature-card:hover::after { opacity: 1; }
.feature-icon {
    width: 54px; height: 54px; background: linear-gradient(135deg, #0d2818, #1a4731);
    border: 1px solid #2ea043; border-radius: 14px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 1.4em; margin-bottom: 16px; color: #3fb950;
}
.feature-card h3 { color: #e6edf3; font-size: 1.02em; font-weight: 700; margin: 0 0 10px; }
.feature-card p  { color: #8b949e; font-size: 0.87em; margin: 0; line-height: 1.7; }

.metrics-container { background: #161b22; border: 1px solid #21262d; border-radius: 14px; padding: 20px 22px; margin: 16px 0; }
.metric-card { background: #0d1117; border: 1px solid #21262d; border-radius: 12px; padding: 20px 14px; text-align: center; }
.metric-card .label { color: #8b949e; font-size: 0.82em; margin-bottom: 8px; }
.metric-card .value { color: #e6edf3; font-size: 2em; font-weight: 900; line-height: 1; }
.metric-card .unit  { color: #3fb950; font-size: 0.8em; margin-top: 5px; }

.status-box {
    border-radius: 10px; padding: 14px 20px; margin: 10px 0; font-size: 0.95em; font-weight: 600;
    direction: rtl; text-align: right; border-right: 4px solid transparent;
    display: flex; align-items: center; gap: 12px;
}
.status-high    { background: #1a1f14; border-color: #3fb950; color: #7ee787; }
.status-normal  { background: #0d1f14; border-color: #3fb950; color: #7ee787; }
.status-low     { background: #0d1a2d; border-color: #58a6ff; color: #79c0ff; }
.status-warning { background: #1f1a0d; border-color: #d29922; color: #e3b341; }

.item-card {
    background: linear-gradient(160deg, #161b22, #13181f); border: 1px solid #21262d;
    border-radius: 16px; padding: 22px 26px; margin: 12px 0;
    border-right: 4px solid #3fb950; direction: rtl; text-align: right;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}
.item-stats { display: flex; gap: 12px; flex-wrap: wrap; }
.item-stat {
    background: #0a0e14; border: 1px solid #21262d; border-radius: 12px;
    padding: 12px 16px; text-align: center; flex: 1; min-width: 80px;
}
.item-stat .stat-label { color: #8b949e; font-size: 0.72em; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.8px; }
.item-stat .stat-value { color: #e3b341; font-size: 1.2em; font-weight: 800; }

.section-title {
    color: #8b949e; font-size: 0.75em; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; margin: 24px 0 10px; padding-bottom: 8px;
    border-bottom: 1px solid #21262d; direction: rtl; text-align: right;
}

.price-table-wrapper { background: #161b22; border: 1px solid #21262d; border-radius: 14px; overflow: hidden; }
.price-table { width: 100%; border-collapse: collapse; direction: rtl; }
.price-table th {
    background: #1c2128; color: #8b949e; font-size: 0.78em; font-weight: 700;
    text-transform: uppercase; padding: 14px 20px; border-bottom: 1px solid #21262d; text-align: right;
}
.price-table td { padding: 13px 20px; border-bottom: 1px solid #1c2128; color: #c9d1d9; font-size: 0.93em; text-align: right; }
.price-table tr:last-child td { border-bottom: none; }
.price-table tr:hover td { background: #1c2128; }
.price-badge {
    background: #0d2818; color: #3fb950; border: 1px solid #1a3a24;
    border-radius: 6px; padding: 3px 11px; font-size: 0.86em; font-weight: 700; display: inline-block;
}
.tech-tag {
    display: inline-block; background: #0d1a2d; color: #58a6ff; border: 1px solid #1a3050;
    border-radius: 6px; padding: 3px 11px; font-size: 0.83em; font-weight: 600; margin: 3px;
}

div[data-testid="stFileUploader"] {
    background: linear-gradient(160deg, #161b22, #13181f); border-radius: 16px; border: 2px dashed #30363d;
    transition: border-color 0.25s;
}
div[data-testid="stFileUploader"]:hover { border-color: #3fb950; }
.stSpinner > div { border-top-color: #3fb950 !important; }
[data-testid="stTextInput"] input { direction: rtl !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e14; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3fb950; }
[data-testid="stMainBlockContainer"] > div { animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
</style>
"""

HEADER_HTML = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@600;700;900&display=swap');
  #fscan-header {
    position: fixed; top: 0; left: 0; right: 0;
    height: 84px; background: #0d1117;
    border-bottom: 1px solid #21262d;
    box-shadow: 0 2px 20px rgba(0,0,0,0.6);
    z-index: 999999;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 32px;
    font-family: 'Heebo', sans-serif;
    direction: rtl;
  }
  #fscan-header .logo {
    display: flex; align-items: center; gap: 10px;
    font-size: 1.5em; font-weight: 900; color: #fff;
  }
  #fscan-header .logo-icon {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #2ea043, #3fb950);
    border-radius: 8px; display: inline-flex; align-items: center; justify-content: center;
    color: #fff; font-size: 1em;
  }
  #fscan-header .accent { color: #3fb950; }
  #fscan-header .nav { display: flex; align-items: center; gap: 4px; }
  #fscan-header .nav-btn {
    display: flex; align-items: center; gap: 6px;
    padding: 9px 18px; border-radius: 8px;
    border: 1px solid transparent; background: transparent;
    color: #8b949e; font-family: 'Heebo', sans-serif;
    font-size: 1.15em; font-weight: 600; cursor: pointer;
    transition: all 0.18s; direction: rtl; text-decoration: none;
  }
  #fscan-header .nav-btn:hover { background: #161b22; border-color: #30363d; color: #e6edf3; }
  #fscan-header .nav-btn.active { background: #0d2818; border-color: #1a3a24; color: #3fb950; }
</style>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<div id="fscan-header">
  <div class="nav">
    <a class="nav-btn" href="?page=home"><i class="bi bi-house-fill"></i>דף הבית</a>
    <a class="nav-btn" href="?page=detect"><i class="bi bi-camera-fill"></i>זיהוי</a>
    <a class="nav-btn" href="?page=price_list"><i class="bi bi-list-ul"></i>מחירון</a>
    <a class="nav-btn" href="?page=about"><i class="bi bi-info-circle-fill"></i>אודות</a>
  </div>
  <div class="logo">
    <span class="logo-icon"><i class="bi bi-flower1"></i></span>
    <span>Fresh<span class="accent">Scan</span></span>
  </div>
</div>
<script>
(function() {
  var p = window.parent;
  if (!p || !p.document.body) return;
  if (p.document.getElementById('fscan-header')) {
    p.document.querySelectorAll('#fscan-header .nav-btn').forEach(function(b) {
      b.classList.toggle('active', b.getAttribute('href') === '?page=CURRENT_PAGE');
      var newB = b.cloneNode(true);
      b.parentNode.replaceChild(newB, b);
      newB.addEventListener('click', function(e) {
        e.preventDefault();
        var page = this.getAttribute('href').replace('?page=', '');
        var target = 'nav:' + page;
        var found = false;
        p.document.querySelectorAll('[data-testid="stSidebar"] button').forEach(function(btn) {
          if (!found && btn.innerText.trim() === target) {
            btn.dispatchEvent(new MouseEvent('click', {bubbles:true}));
            found = true;
          }
        });
      });
    });
    return;
  }
  var link  = document.querySelector('link');
  var style = document.querySelector('style');
  var el    = document.getElementById('fscan-header');
  p.document.head.appendChild(link.cloneNode(true));
  p.document.head.insertAdjacentHTML('beforeend', '<style>' + style.textContent + '</style>');
  var clone = el.cloneNode(true);
  p.document.body.appendChild(clone);
  clone.querySelectorAll('.nav-btn').forEach(function(b) {
    b.classList.toggle('active', b.getAttribute('href') === '?page=CURRENT_PAGE');
    b.addEventListener('click', function(e) {
      e.preventDefault();
      var page = this.getAttribute('href').replace('?page=', '');
      var target = 'nav:' + page;
      var found = false;
      p.document.querySelectorAll('[data-testid="stSidebar"] button').forEach(function(btn) {
        if (!found && btn.innerText.trim() === target) {
          btn.dispatchEvent(new MouseEvent('click', {bubbles:true}));
          found = true;
        }
      });
    });
  });
})();
</script>
"""

FOOTER_HTML = """
<style>
  #fscan-footer {
    position: fixed; bottom: 0; left: 0; right: 0;
    height: 42px; background: #0d1117; border-top: 1px solid #21262d;
    z-index: 999999; display: flex; align-items: center; justify-content: center; gap: 10px;
    font-family: 'Heebo', sans-serif; color: #484f58; font-size: 0.82em; direction: rtl;
  }
  #fscan-footer .fb { color: #3fb950; font-weight: 700; }
  #fscan-footer .fd { color: #30363d; }
</style>
<div id="fscan-footer">
  <i class="bi bi-flower1" style="color:#3fb950"></i>
  <span class="fb">FreshScan</span>
  <span class="fd">&bull;</span>
  <span>2026</span>
  <span class="fd">&bull;</span>
  <span>מערכת זיהוי פירות וירקות בבינה מלאכותית</span>
</div>
<script>
  var footer = document.getElementById('fscan-footer');
  var style  = document.querySelector('style');
  if (window.parent && window.parent.document.body) {
    if (!window.parent.document.getElementById('fscan-footer')) {
      window.parent.document.head.insertAdjacentHTML('beforeend', '<style>' + style.textContent + '</style>');
      window.parent.document.body.appendChild(footer.cloneNode(true));
    }
  }
</script>
"""
