"""
price_list.py — Price List Page

Displays a searchable, sortable table of all supported fruits and vegetables
with their per-kg price and average unit weight.
"""
import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from src.config.settings import HEBREW_NAMES, EMOJI, PRICE_PER_KG, AVERAGE_WEIGHT_GRAMS


def render():
    """
    Render the price list page.

    Builds a list of all supported items from HEBREW_NAMES, applies
    the user's search filter (Hebrew or English), sorts by the selected
    criterion, and renders the result as an HTML table.
    """
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon"><i class="bi bi-list-ul"></i></div>
        <div>
            <h2>מחירון פירות וירקות</h2>
            <p>מחירים עדכניים לכל הפירות והירקות הנתמכים במערכת</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_search, col_sort = st.columns([3, 1])
    with col_search:
        search = st.text_input("חיפוש", placeholder="הקלידו שם פרי או ירק...")
    with col_sort:
        sort_by = st.selectbox("מיון לפי", ["שם", "מחיר נמוך", "מחיר גבוה"])

    rows = []
    for en_name, he_name in HEBREW_NAMES.items():
        # Filter: skip items that don't match the search query (case-insensitive)
        if search and search.lower() not in he_name and search.lower() not in en_name.lower():
            continue
        rows.append({
            "emoji":  EMOJI.get(en_name, "🔍"),
            "he":     he_name,
            "en":     en_name,
            "price":  PRICE_PER_KG.get(en_name, 0),
            "weight": AVERAGE_WEIGHT_GRAMS.get(en_name, 0),
        })

    # Sort the filtered rows according to the user's selection
    if sort_by == "מחיר נמוך":
        rows.sort(key=lambda x: x["price"])
    elif sort_by == "מחיר גבוה":
        rows.sort(key=lambda x: x["price"], reverse=True)
    else:
        rows.sort(key=lambda x: x["he"])  # Default: alphabetical by Hebrew name

    rows_html = ""
    for r in rows:
        rows_html += f"""
        <tr>
            <td>{r['he']}</td>
            <td style="color:#8b949e; font-size:0.85em">{r['en']}</td>
            <td><span class="price-badge">₪{r['price']}</span></td>
            <td style="color:#8b949e">{r['weight']}g</td>
        </tr>"""

    st.markdown(f"""
    <div class="price-table-wrapper">
    <table class="price-table">
        <thead>
            <tr>
                <th>פרי / ירק</th>
                <th>שם באנגלית</th>
                <th>מחיר לק"ג</th>
                <th>משקל ממוצע</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    </div>
    <div style='color:#484f58; font-size:0.82em; text-align:right; margin-top:10px'>סה"כ {len(rows)} פריטים</div>
    """, unsafe_allow_html=True)
