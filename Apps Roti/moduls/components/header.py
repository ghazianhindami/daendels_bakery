import streamlit as st

class HeaderComponent:

    def __init__(self, session_manager):
        self.session = session_manager

    def render(self):
        _, right = st.columns([3,1])

        with right:
            if st.button("Logout"):
                self.session.logout()
                st.success("Logout berhasil")
                st.rerun()