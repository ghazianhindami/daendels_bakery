import streamlit as st
import requests
import time

def login_page():

    st.title("🔐 Login Bakery POS")

    id_employee = st.number_input(
   "Employee ID",
   min_value=1,
   step=1,
   format="%d"
    )


    if st.button("Login"):
        with st.spinner(
                    "Sedang Login..."
                ):
            payload={
                "employee_id":id_employee
            }

            try:
                response = requests.post(
                    "http://localhost:8000/login",
                    json=payload,
                    timeout=5
                )

                if response.status_code==200:

                    user=response.json()
                    st.write(response.status_code)
                    st.write(response.json())

                    st.session_state.logged_in=True
                    st.session_state.user=user["user_id"]
                    st.session_state.full_name=user["username"]
                    st.session_state.role=user["role"]
                    st.session_state.branch_id=user["branch_id"]
                    st.session_state.branch_name=user["branch_name"]


                    st.success(
                        "Login berhasil")
                    
                    time.sleep(2)
                    st.rerun()

                else:
                    st.error(
                        "Login gagal"
                    )

            except Exception as e:
                st.error(e)

    if st.button("Logout"):
        st.session_state.show_login=False
        st.rerun()

            # st.error(
            #     "API tidak dapat diakses"
            # )
