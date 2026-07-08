import streamlit as st
from src.config.settings import HEBREW_NAMES, EMOJI

def render_metrics(count, total_weight=0, total_price=0):
    st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, label, value, unit in [
        (c1, '<i class="bi bi-box-seam"></i> פריטים',    count,                'יחידות'),
        (c2, '<i class="bi bi-speedometer2"></i> משקל',  total_weight,         'גרם'),
        (c3, '<i class="bi bi-receipt"></i> מחיר כולל', f'₪{total_price:.2f}', 'שקלים'),
    ]:
        col.markdown(f'<div class="metric-card"><div class="label">{label}</div><div class="value">{value}</div><div class="unit">{unit}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_density_status(density):
    m = {
        'high':   ('status-high',   '<i class="bi bi-exclamation-triangle-fill"></i> צפיפות גבוהה', 'הפריטים צמודים מאוד.'),
        'normal': ('status-normal', '<i class="bi bi-check-circle-fill"></i> צפיפות תקינה',         'הפריטים מפוזרים נכון.'),
        'low':    ('status-low',    '<i class="bi bi-info-circle-fill"></i> צפיפות נמוכה',           'הפריטים מרווחים.'),
        'single': ('status-normal', '<i class="bi bi-check-circle-fill"></i> פריט בודד',             'זוהה פריט אחד.'),
    }
    cls, title, desc = m.get(density, m['normal'])
    st.markdown(f'<div class="status-box {cls}"><div>{title}</div><div style="font-weight:400;opacity:0.85">{desc}</div></div>', unsafe_allow_html=True)

def render_error_message(title, desc):
    st.markdown(f'<div class="status-box status-warning"><i class="bi bi-exclamation-circle-fill"></i> <div><div>{title}</div><div style="font-weight:400;opacity:0.85">{desc}</div></div></div>', unsafe_allow_html=True)

def render_no_items_message():
    st.markdown('<div class="status-box status-warning"><i class="bi bi-search"></i> לא זוהו פריטים בתמונה</div>', unsafe_allow_html=True)
