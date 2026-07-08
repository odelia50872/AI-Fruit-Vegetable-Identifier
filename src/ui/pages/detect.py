"""
עמוד הזיהוי
"""
import streamlit as st
from PIL import Image
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from src.utils.image_utils import check_image_quality, analyze_image_results, estimate_weight, calculate_price
from src.utils.barcode_utils import generate_item_qr, image_to_base64
from src.ui.components import render_metrics, render_density_status, render_error_message, render_no_items_message
from src.config.settings import HEBREW_NAMES, EMOJI


def render(model):
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon"><i class="bi bi-camera-fill"></i></div>
        <div>
            <h2>זיהוי פירות וירקות</h2>
            <p>העלו תמונה וקבלו זיהוי, ספירה, משקל ומחיר תוך שניות</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("בחרו תמונה (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

    if uploaded_file is None:
        st.markdown("""
        <div class="status-box status-low" style="text-align:center; padding:32px;">
            <div style="font-size:2em; margin-bottom:8px"><i class="bi bi-camera" style="color:#58a6ff"></i></div>
            <div style="font-size:1.05em">העלו תמונה כדי להתחיל</div>
            <div style="font-weight:400; margin-top:6px; opacity:0.75">תומך בפורמטים: JPG, JPEG, PNG</div>
        </div>
        """, unsafe_allow_html=True)
        return

    _process(uploaded_file, model)


def _process(uploaded_file, model):
    image = Image.open(uploaded_file)

    # איפוס בחירות כשמועלת תמונה חדשה
    file_key = uploaded_file.name + str(uploaded_file.size)
    if st.session_state.get("_last_file") != file_key:
        for k in list(st.session_state.keys()):
            if k.startswith("chosen_"):
                del st.session_state[k]
        st.session_state["_last_file"] = file_key

    is_ok, err_title, err_desc = check_image_quality(image)
    if not is_ok:
        render_error_message(err_title, err_desc)
        return

    with st.spinner("מנתח את התמונה..."):
        results, topk_per_box = model.predict_topk(image, k=3)

    if not results:
        render_error_message("שגיאה בזיהוי", "לא ניתן לעבד את התמונה")
        return

    count, density, items, _, _ = analyze_image_results(results, model.model, topk_per_box)

    if results and len(results) > 0:
        annotated = Image.fromarray(results[0].plot()[..., ::-1])
        st.markdown('<div class="section-title">תמונה מסומנת</div>', unsafe_allow_html=True)
        _, col, _ = st.columns([1, 2, 1])
        col.image(annotated, use_container_width=True)

    if count == 0:
        render_no_items_message()
        return

    render_density_status(density)
    st.markdown('<div class="section-title">בחרו את הזיהוי הנכון לכל פריט</div>', unsafe_allow_html=True)
    _render_selection(items)
    _render_summary(items)


def _render_selection(items):
    for item_idx, (name, data) in enumerate(items.items()):
        cnt = len(data['weights'])
        avg_box_size = round(sum(data['weights']) / cnt)
        state_key = f"chosen_{item_idx}"

        topk_merged = data.get('topk_merged', {})
        candidates = sorted(
            [{"name": n, "conf": c} for n, c in topk_merged.items()],
            key=lambda x: x["conf"], reverse=True
        )[:3]
        if not candidates:
            candidates = [{"name": name, "conf": 1.0}]

        if state_key not in st.session_state:
            st.session_state[state_key] = name

        chosen_name = st.session_state[state_key]
        chosen_weight = estimate_weight(chosen_name, avg_box_size) * cnt
        chosen_price  = calculate_price(chosen_name, chosen_weight)
        qr_img, _     = generate_item_qr(chosen_name, cnt, chosen_weight, chosen_price)

        emoji_icon = EMOJI.get(chosen_name, '🍎')
        heb_chosen = HEBREW_NAMES.get(chosen_name, chosen_name)

        st.markdown(f"""
        <div class="item-card">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:16px;">
                <span style="font-size:1.6em">{emoji_icon}</span>
                <div>
                    <div style="color:#e6edf3; font-weight:700; font-size:1.05em">פריט {item_idx + 1}</div>
                    <div style="color:#8b949e; font-size:0.85em">{cnt} יחידות זוהו</div>
                </div>
            </div>
            <div style="color:#8b949e; font-size:0.8em; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px">בחרו את הזיהוי הנכון:</div>
        </div>
        """, unsafe_allow_html=True)

        # כפתורי בחירה צמודים
        btn_cols = st.columns(len(candidates))
        for col, candidate in zip(btn_cols, candidates):
            cname = candidate['name']
            heb   = HEBREW_NAMES.get(cname, cname)
            pct   = round(candidate['conf'] * 100)
            em    = EMOJI.get(cname, '🍎')
            is_active = chosen_name == cname
            if col.button(
                f"{em} {heb}\n{pct}%",
                key=f"btn_{item_idx}_{cname}",
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                st.session_state[state_key] = cname
                st.rerun()

        col_info, col_qr = st.columns([3, 1])
        with col_info:
            st.markdown(f"""
            <div style="margin-top:16px">
                <div class="item-stats">
                    <div class="item-stat"><div class="stat-label">פרי</div><div class="stat-value" style="font-size:1em">{heb_chosen}</div></div>
                    <div class="item-stat"><div class="stat-label">כמות</div><div class="stat-value">{cnt}</div></div>
                    <div class="item-stat"><div class="stat-label">משקל</div><div class="stat-value">{chosen_weight}g</div></div>
                    <div class="item-stat"><div class="stat-label">מחיר</div><div class="stat-value">₪{chosen_price:.2f}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_qr:
            st.image(f"data:image/png;base64,{image_to_base64(qr_img)}", width=160)

        st.markdown('</div>', unsafe_allow_html=True)


def _render_summary(items):
    total_weight = total_price = chosen_count = 0
    for item_idx, (name, data) in enumerate(items.items()):
        chosen_name = st.session_state.get(f"chosen_{item_idx}")
        if chosen_name:
            cnt = len(data['weights'])
            avg_box_size = round(sum(data['weights']) / cnt)
            w = estimate_weight(chosen_name, avg_box_size) * cnt
            total_weight += w
            total_price  += calculate_price(chosen_name, w)
            chosen_count += cnt

    if chosen_count > 0:
        st.markdown('<div class="section-title">סיכום כללי</div>', unsafe_allow_html=True)

        render_metrics(chosen_count, total_weight, total_price)
