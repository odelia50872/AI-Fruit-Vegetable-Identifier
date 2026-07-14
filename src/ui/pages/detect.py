"""
detect.py — Detection Page

Handles the full detection workflow:
  1. Image input via file upload or live camera
  2. Quality validation
  3. YOLOv8 inference with Top-K candidates
  4. Interactive per-item class selection
  5. Results display with weight, price, and QR code per item
  6. Overall summary metrics
"""
import streamlit as st
from PIL import Image
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from src.utils.image_utils import check_image_quality, analyze_image_results, calculate_price
from src.utils.barcode_utils import generate_item_qr, image_to_base64
from src.ui.components import render_metrics, render_density_status, render_error_message, render_no_items_message
from src.config.settings import HEBREW_NAMES, EMOJI, AVERAGE_WEIGHT_GRAMS


def render(model):
    """
    Render the detection page.

    Displays two input tabs (file upload and live camera). Once the user
    provides an image via either tab, delegates processing to _process().

    Args:
        model: Loaded YOLOModel instance passed from app.py.
    """
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon"><i class="bi bi-camera-fill"></i></div>
        <div>
            <h2>זיהוי פירות וירקות</h2>
            <p>העלו תמונה וקבלו זיהוי, ספירה, משקל ומחיר תוך שניות</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Two input methods: file upload or live camera capture
    tab_upload, tab_camera = st.tabs(["📁 העלאת תמונה", "📷 צילום מהמצלמה"])

    source_file = None

    with tab_upload:
        uploaded_file = st.file_uploader("בחרו תמונה (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            source_file = uploaded_file
        else:
            # Show a placeholder prompt when no file has been uploaded yet
            st.markdown("""
            <div class="status-box status-low" style="text-align:center; padding:32px;">
                <div style="font-size:2em; margin-bottom:8px"><i class="bi bi-camera" style="color:#58a6ff"></i></div>
                <div style="font-size:1.05em">העלו תמונה כדי להתחיל</div>
                <div style="font-weight:400; margin-top:6px; opacity:0.75">תומך בפורמטים: JPG, JPEG, PNG</div>
            </div>
            """, unsafe_allow_html=True)

    with tab_camera:
        camera_file = st.camera_input("צלמו תמונה")
        if camera_file is not None:
            source_file = camera_file  # Camera capture overrides file upload

    # Only proceed if the user has provided an image from either tab
    if source_file is not None:
        _process(source_file, model)


def _process(uploaded_file, model):
    """
    Run the full detection pipeline on the provided image file.

    Steps:
      1. Open the image with PIL.
      2. Detect a new file by hashing name+size; reset per-item selections if changed.
      3. Validate image quality — abort with an error banner if it fails.
      4. Run YOLOv8 Top-K inference.
      5. Analyze results to get item counts, density, and per-class data.
      6. Route to the selection view or the results view depending on
         whether the user has confirmed all item classes.

    Args:
        uploaded_file: Streamlit UploadedFile object (from uploader or camera).
        model:         Loaded YOLOModel instance.
    """
    image = Image.open(uploaded_file)

    # Build a unique key for this file to detect when the user uploads a new image
    file_key = uploaded_file.name + str(uploaded_file.size)

    if st.session_state.get("_last_file") != file_key:
        # New image uploaded — clear all previously confirmed item selections
        for k in list(st.session_state.keys()):
            if k.startswith("chosen_"):
                del st.session_state[k]
        st.session_state["_last_file"] = file_key

    # Validate image quality before running the model
    is_ok, err_title, err_desc = check_image_quality(image)
    if not is_ok:
        render_error_message(err_title, err_desc)
        return

    # Run inference — returns primary results and Top-K candidates per box
    with st.spinner("מנתח את התמונה..."):
        results, topk_per_box = model.predict_topk(image, k=3)

    if not results:
        render_error_message("שגיאה בזיהוי", "לא ניתן לעבד את התמונה")
        return

    # Parse detection results into structured per-class item data
    count, density, items, _, _ = analyze_image_results(results, model.model, topk_per_box)

    # Generate the annotated image (bounding boxes drawn by YOLO)
    # results[0].plot() returns BGR numpy array — convert to RGB for PIL/Streamlit
    annotated = Image.fromarray(results[0].plot()[..., ::-1]) if results and len(results) > 0 else None

    if count == 0:
        # Show the annotated image centered, then a "no items" warning
        if annotated:
            _, col, _ = st.columns([1, 2, 1])
            col.image(annotated, use_container_width=True)
        render_no_items_message()
        return

    # Check whether the user has confirmed a class for every detected item group
    all_chosen = all(st.session_state.get(f"chosen_{i}") for i in range(len(items)))

    if not all_chosen:
        # --- Selection view: annotated image + per-item class buttons side by side ---
        render_density_status(density)
        col_img, col_sel = st.columns([1, 1], gap="large")
        with col_img:
            st.markdown('<div class="section-title">תמונה מסומנת</div>', unsafe_allow_html=True)
            if annotated:
                st.image(annotated, use_container_width=True)
        with col_sel:
            st.markdown('<div class="section-title">בחרו את הזיהוי הנכון לכל פריט</div>', unsafe_allow_html=True)
            _render_selection(items)
    else:
        # --- Results view: smaller annotated image + confirmed results side by side ---
        col_img, col_results = st.columns([1, 2], gap="large")
        with col_img:
            st.markdown('<div class="section-title">תמונה מסומנת</div>', unsafe_allow_html=True)
            if annotated:
                st.image(annotated, use_container_width=True)
        with col_results:
            _render_results(items)
            _render_summary(items)


def _render_selection(items):
    """
    Render Top-K candidate selection buttons for each detected item group.

    For each item group, displays a card with the item index and unit count,
    then renders one button per Top-K candidate. Clicking a button stores
    the chosen class name in session_state['chosen_{item_idx}'] and reruns
    the app to advance to the results view once all items are confirmed.

    Args:
        items: Dict of {class_name: data} from analyze_image_results().
    """
    for item_idx, (name, data) in enumerate(items.items()):
        cnt       = len(data['weights'])
        state_key = f"chosen_{item_idx}"

        # Build sorted candidate list from the merged Top-K scores
        topk_merged = data.get('topk_merged', {})
        candidates = sorted(
            [{"name": n, "conf": c} for n, c in topk_merged.items()],
            key=lambda x: x["conf"], reverse=True
        )[:3]

        # Fallback: if no candidates exist, use the primary detection at 100%
        if not candidates:
            candidates = [{"name": name, "conf": 1.0}]

        chosen_name = st.session_state.get(state_key)

        # Show the emoji of the currently chosen class (or the top candidate)
        em = EMOJI.get(chosen_name or candidates[0]['name'], '🍎')

        st.markdown(f"""
        <div style="background:#161b22; border:1px solid #21262d; border-radius:14px; padding:18px 20px; margin-bottom:14px; border-right:4px solid #3fb950;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
                <span style="font-size:1.8em">{em}</span>
                <div>
                    <div style="color:#e6edf3; font-weight:700; font-size:1.05em">פריט {item_idx + 1}</div>
                    <div style="color:#8b949e; font-size:0.85em">{cnt} יחידות זוהו</div>
                </div>
            </div>
            <div style="color:#8b949e; font-size:0.78em; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;">בחרו את הזיהוי הנכון:</div>
        </div>
        """, unsafe_allow_html=True)

        # Render one button per candidate in equal-width columns
        btn_cols = st.columns(len(candidates))
        for col, candidate in zip(btn_cols, candidates):
            cname     = candidate['name']
            heb       = HEBREW_NAMES.get(cname, cname)
            pct       = round(candidate['conf'] * 100)
            em        = EMOJI.get(cname, '🍎')
            is_active = chosen_name == cname  # Highlight the currently selected candidate

            if col.button(
                f"{em} {heb}\n{pct}%",
                key=f"btn_{item_idx}_{cname}",
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                # Store the user's choice and rerun to refresh the UI
                st.session_state[state_key] = cname
                st.rerun()


def _render_results(items):
    """
    Render the confirmed detection result card and QR code for each item group.

    For each item group where the user has confirmed a class:
      - If the confirmed class matches the primary detection, use the
        estimated weights from analyze_image_results().
      - If the user selected a different class, recalculate weight using
        the average weight for that class multiplied by the unit count.
      - Generates a QR code image and displays it alongside the item card.

    Args:
        items: Dict of {class_name: data} from analyze_image_results().
    """
    for item_idx, (name, data) in enumerate(items.items()):
        chosen_name = st.session_state.get(f"chosen_{item_idx}")
        if not chosen_name:
            continue  # Skip items not yet confirmed

        cnt = len(data['weights'])

        # Recalculate weight if the user chose a different class than detected
        if chosen_name == name:
            chosen_weight = sum(data['weights'])
        else:
            chosen_weight = AVERAGE_WEIGHT_GRAMS.get(chosen_name, 150) * cnt

        chosen_price = calculate_price(chosen_name, chosen_weight)

        # Generate QR code image for this item
        qr_img, _  = generate_item_qr(chosen_name, cnt, chosen_weight, chosen_price)
        heb_chosen = HEBREW_NAMES.get(chosen_name, chosen_name)
        em         = EMOJI.get(chosen_name, '🍎')

        col_info, col_qr = st.columns([2, 1])
        with col_info:
            # Show per-unit weight breakdown in parentheses (e.g. "120g + 135g")
            weight_breakdown = ' + '.join(str(w) + 'g' for w in data['weights'])
            st.markdown(f"""
            <div style="background:#161b22; border:1px solid #21262d; border-radius:14px; padding:18px 20px; margin-bottom:14px; border-right:4px solid #3fb950;">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
                    <span style="font-size:1.6em">{em}</span>
                    <div style="color:#e6edf3; font-weight:700; font-size:1.05em">{heb_chosen}</div>
                </div>
                <div class="item-stats">
                    <div class="item-stat"><div class="stat-label">כמות</div><div class="stat-value">{cnt}</div></div>
                    <div class="item-stat"><div class="stat-label">משקל</div><div class="stat-value">{chosen_weight}g</div><div style="color:#8b949e; font-size:0.75em; margin-top:4px">({weight_breakdown})</div></div>
                    <div class="item-stat"><div class="stat-label">מחיר</div><div class="stat-value">₪{chosen_price:.2f}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_qr:
            # Embed QR image as base64 to avoid writing temp files
            st.image(f"data:image/png;base64,{image_to_base64(qr_img)}", width=130)


def _render_summary(items):
    """
    Render the overall summary metrics across all confirmed item groups.

    Aggregates total item count, total weight, and total price from all
    groups where the user has confirmed a class, then calls render_metrics()
    to display the three summary cards.

    Args:
        items: Dict of {class_name: data} from analyze_image_results().
    """
    total_weight = total_price = chosen_count = 0

    for item_idx, (name, data) in enumerate(items.items()):
        chosen_name = st.session_state.get(f"chosen_{item_idx}")
        if not chosen_name:
            continue  # Skip unconfirmed items

        cnt = len(data['weights'])

        # Use estimated weights if class matches, otherwise use class average
        w = sum(data['weights']) if chosen_name == name else AVERAGE_WEIGHT_GRAMS.get(chosen_name, 150) * cnt

        total_weight += w
        total_price  += calculate_price(chosen_name, w)
        chosen_count += cnt

    if chosen_count > 0:
        st.markdown('<div class="section-title">סיכום כללי</div>', unsafe_allow_html=True)
        render_metrics(chosen_count, total_weight, total_price)
