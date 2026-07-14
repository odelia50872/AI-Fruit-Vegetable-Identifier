"""
app.py — FreshScan Application Entry Point

Main Streamlit application that handles page routing, model loading,
and rendering the custom navigation header/footer.
"""
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import sys

# Add project root to path so src modules are importable
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from src.models.yolo_model import YOLOModel
from src.ui.styles import MAIN_CSS, HEADER_HTML, FOOTER_HTML
from src.ui.pages import home, detect, price_list, about

# Configure Streamlit page settings
st.set_page_config(page_title='FreshScan', page_icon='🥦', layout='wide', initial_sidebar_state='collapsed')
st.markdown(MAIN_CSS, unsafe_allow_html=True)
components.html(FOOTER_HTML, height=0)


@st.cache_resource
def load_model():
    """Load and cache the YOLOv8 model. Cached across sessions to avoid reloading."""
    return YOLOModel()


def main():
    """
    Main application controller.

    Reads the current page from query params or session state,
    renders hidden sidebar nav buttons (triggered by the JS header),
    injects the custom header, and delegates rendering to the correct page module.
    """
    params = st.query_params

    # Initialize page state from URL query param on first load
    if 'page' not in st.session_state:
        st.session_state['page'] = params.get('page', 'home')
    elif params.get('page', st.session_state['page']) != st.session_state['page']:
        # Sync session state when URL param changes (e.g. browser back/forward)
        st.session_state['page'] = params.get('page')
        st.rerun()

    # Hidden sidebar buttons — the custom JS header clicks these to trigger Streamlit reruns
    with st.sidebar:
        if st.button('nav:home',       key='nav_home'):       st.session_state['page'] = 'home';       st.query_params['page'] = 'home';       st.rerun()
        if st.button('nav:detect',     key='nav_detect'):     st.session_state['page'] = 'detect';     st.query_params['page'] = 'detect';     st.rerun()
        if st.button('nav:price_list', key='nav_price_list'): st.session_state['page'] = 'price_list'; st.query_params['page'] = 'price_list'; st.rerun()
        if st.button('nav:about',      key='nav_about'):      st.session_state['page'] = 'about';      st.query_params['page'] = 'about';      st.rerun()

    cur = st.session_state['page']

    # Inject the fixed header with the active page highlighted
    components.html(HEADER_HTML.replace('CURRENT_PAGE', cur), height=0)

    # Route to the appropriate page renderer
    if cur == 'home':
        home.render()
    elif cur == 'detect':
        model = load_model()
        if not model.model:  # model.model is None when the weights file was not found
            st.error('לא ניתן לטעון את המודל!')
            st.stop()
        detect.render(model)
    elif cur == 'price_list':
        price_list.render()
    elif cur == 'about':
        about.render()


if __name__ == '__main__':
    main()
