"""
עמוד אודות
"""
import streamlit as st


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon"><i class="bi bi-info-circle-fill"></i></div>
        <div>
            <h2>אודות FreshScan</h2>
            <p>מידע על הפרויקט, הטכנולוגיה והצוות</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-header"><i class="bi bi-flower1"></i> מה זה FreshScan?</div>
            <p>FreshScan היא מערכת זיהוי פירות וירקות מבוססת בינה מלאכותית.
            המערכת מנתחת תמונות בזמן אמת, מזהה את הפריטים, מחשבת משקל משוער
            ומחיר כולל — ומייצרת ברקוד QR לכל פריט.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-header"><i class="bi bi-cpu-fill"></i> המודל</div>
            <ul>
                <li>ארכיטקטורה: YOLOv8</li>
                <li>34+ קטגוריות של פירות וירקות</li>
                <li>דיוק זיהוי: ~95%</li>
                <li>זמן עיבוד: פחות מ-3 שניות</li>
                <li>תמיכה ב-Top-K predictions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-header"><i class="bi bi-tools"></i> טכנולוגיות</div>
            <p>
                <span class="tech-tag">Python 3.10+</span>
                <span class="tech-tag">Streamlit</span>
                <span class="tech-tag">YOLOv8</span>
                <span class="tech-tag">Ultralytics</span>
                <span class="tech-tag">Pillow</span>
                <span class="tech-tag">qrcode</span>
                <span class="tech-tag">python-bidi</span>
                <span class="tech-tag">OpenCV</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-header"><i class="bi bi-folder2-open"></i> מבנה הפרויקט</div>
            <ul>
                <li><strong style="color:#c9d1d9">app.py</strong> — נקודת כניסה וניתוב</li>
                <li><strong style="color:#c9d1d9">src/models/</strong> — מודל YOLO</li>
                <li><strong style="color:#c9d1d9">src/ui/pages/</strong> — עמודי האפליקציה</li>
                <li><strong style="color:#c9d1d9">src/ui/</strong> — עיצוב ורכיבים</li>
                <li><strong style="color:#c9d1d9">src/utils/</strong> — כלי עזר</li>
                <li><strong style="color:#c9d1d9">src/config/</strong> — הגדרות</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-header"><i class="bi bi-play-circle-fill"></i> איך להשתמש?</div>
        <p>
            1. עברו לעמוד <strong style="color:#3fb950">זיהוי</strong> בסרגל הניווט<br>
            2. העלו תמונה של פירות או ירקות<br>
            3. המערכת תזהה אוטומטית את הפריטים<br>
            4. בחרו את הזיהוי הנכון לכל פריט מתוך 3 אפשרויות<br>
            5. קבלו סיכום מחיר וברקוד QR לכל פריט
        </p>
    </div>
    """, unsafe_allow_html=True)
