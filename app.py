import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import sys
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from src.models.yolo_model import YOLOModel
from src.ui.styles import MAIN_CSS, HEADER_HTML, FOOTER_HTML
from src.ui.pages import home, detect, price_list, about

st.set_page_config(page_title='FreshScan', page_icon='🌿', layout='wide', initial_sidebar_state='collapsed')
st.markdown(MAIN_CSS, unsafe_allow_html=True)
components.html(FOOTER_HTML, height=0)

@st.cache_resource
def load_model():
    return YOLOModel()

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'

    # כפתורי ניווט ב-sidebar מוסתר — ה-header לוחץ עליהם דרך JS
    with st.sidebar:
        if st.button('nav:home',       key='nav_home'):       st.session_state['page'] = 'home';       st.rerun()
        if st.button('nav:detect',     key='nav_detect'):     st.session_state['page'] = 'detect';     st.rerun()
        if st.button('nav:price_list', key='nav_price_list'): st.session_state['page'] = 'price_list'; st.rerun()
        if st.button('nav:about',      key='nav_about'):      st.session_state['page'] = 'about';      st.rerun()

    cur = st.session_state['page']
    components.html(HEADER_HTML.replace('CURRENT_PAGE', cur), height=0)

    if cur == 'home':
        home.render()
    elif cur == 'detect':
        model = load_model()
        if not model.model:
            st.error('לא ניתן לטעון את המודל!')
            st.stop()
        detect.render(model)
    elif cur == 'price_list':
        price_list.render()
    elif cur == 'about':
        about.render()

if __name__ == '__main__':
    main()
