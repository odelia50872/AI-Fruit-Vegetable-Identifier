"""
דף הבית
"""
import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))


def render():
    st.markdown("""
    <div class="hero">
        <div class="hero-icon"><i class="bi bi-flower1"></i></div>
        <h1>זיהוי פירות וירקות<br><span>בבינה מלאכותית</span></h1>
        <p>העלו תמונה וקבלו זיהוי מדויק, ספירה אוטומטית, הערכת משקל ומחיר — תוך שניות.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-row">
        <div class="stat-box"><div class="num">34+</div><div class="lbl">סוגי פירות וירקות</div></div>
        <div class="stat-box"><div class="num">95%</div><div class="lbl">דיוק זיהוי</div></div>
        <div class="stat-box"><div class="num">&lt;3s</div><div class="lbl">זמן עיבוד ממוצע</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon"><i class="bi bi-cpu-fill"></i></div>
            <h3>זיהוי חכם</h3>
            <p>מודל YOLO מתקדם מזהה עד 34 סוגי פירות וירקות בדיוק גבוה</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon"><i class="bi bi-speedometer2"></i></div>
            <h3>הערכת משקל</h3>
            <p>חישוב אוטומטי של משקל משוער לכל פריט על פי גודלו בתמונה</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon"><i class="bi bi-currency-exchange"></i></div>
            <h3>חישוב מחיר</h3>
            <p>מחירון עדכני לכל הפירות והירקות עם חישוב מחיר כולל מיידי</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon"><i class="bi bi-bar-chart-fill"></i></div>
            <h3>ניתוח צפיפות</h3>
            <p>זיהוי צפיפות הפריטים בתמונה והמלצות לסידור מחדש</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon"><i class="bi bi-qr-code"></i></div>
            <h3>ברקוד QR</h3>
            <p>יצירת QR code לכל פריט עם כל הפרטים לסריקה בקופה</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon"><i class="bi bi-list-check"></i></div>
            <h3>Top-3 זיהויים</h3>
            <p>הצגת 3 אפשרויות זיהוי לכל פריט לבחירה ידנית מדויקת</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="text-align:center; padding:24px 32px;">
        <div class="card-header" style="border:none; justify-content:center; font-size:1em;">
            <i class="bi bi-rocket-takeoff-fill"></i> מוכנים להתחיל?
        </div>
        <p style="margin-bottom:0">העלו תמונה של פירות או ירקות וקבלו תוצאות תוך שניות</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("התחל זיהוי", type="primary"):
            st.session_state["page"] = "detect"
            st.rerun()
