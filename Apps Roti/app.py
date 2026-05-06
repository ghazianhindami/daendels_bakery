import streamlit as st
from moduls.login import login_page
from moduls.main_page import main_app
from moduls.self_service_page import self_service_app
from moduls.pages import employee_service_app
from moduls.login import login_page

st.set_page_config(page_title="Bakery Daendels", layout="centered")
st.title("🍞 Bakery Daendels POS")


if "self_service" not in st.session_state:
    st.session_state.self_service = False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_login" not in st.session_state:
    st.session_state.show_login = False


# tampilkan menu hanya jika belum masuk mode apapun
if (
    not st.session_state.self_service
    and not st.session_state.logged_in
    and not st.session_state.show_login
):

    left, right = st.columns(2)

    with left:
        if st.button("Self Service"):
            st.session_state.self_service = True
            st.rerun()

    with right:
        if st.button("Employee Login"):
            st.session_state.show_login = True
            st.rerun()


# routing
# 
if st.session_state.logged_in:
    employee_service_app()
elif st.session_state.self_service:
    self_service_app()

elif st.session_state.show_login:
    login_page()

