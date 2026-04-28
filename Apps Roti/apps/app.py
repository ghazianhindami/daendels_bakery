from urllib import response

import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Bakery Daendels")

st.title("🍞 Bakery Daendels POS")

if "logged_in" not in st.session_state:
    st.session_state.logged_in=False


def login_page():

    st.title("🔐 Login Bakery POS")

    id_employee = st.number_input(
   "Employee ID",
   min_value=1,
   step=1,
   format="%d"
    )


    if st.button("Login"):

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

                # st.rerun()

            else:
                st.error(
                    "Login gagal"
                )

        except Exception as e:
            st.error(e)
            # st.error(
            #     "API tidak dapat diakses"
            # )

# # -------------------------
# # Success Message Persist
# # -------------------------
def main_app():
    st.write(
        f"Selamat datang, {st.session_state.full_name} ({st.session_state.role})"
    )

    


    # -------------------------
    # Session Cart
    # -------------------------

    if "cart" not in st.session_state:
        st.session_state.cart = []


    # -------------------------
    # Cached Master Data
    # -------------------------

    @st.cache_data
    def load_products():
        return requests.get(
            "http://localhost:8000/products",
            timeout=5
        ).json()


    @st.cache_data
    def load_branches():
        return requests.get(
            "http://localhost:8000/branch",
            timeout=5
        ).json()


    products = load_products()


    product_map = {
        p["product_name"]: p
        for p in products
    }

    # -------------------------
    # Branch
    # -------------------------

    st.subheader("Nama Branches")

    cabang = st.write(st.session_state.branch_name)


    # -------------------------
    # Product Form
    # -------------------------

    st.subheader("Pilih Produk")

    produk = st.selectbox(
        "Pilih Produk",
        options=list(product_map.keys())
    )

    harga = product_map[produk]["unit_price"]

    st.write(
        f"Harga Unit: EUR {harga}"
    )

    qty = st.number_input(
        "Jumlah",
        min_value=1,
        value=1
    )

    # realtime update
    subtotal = harga * qty

    st.write(
        f"Subtotal: EUR {subtotal}"
    )


    if st.button("Tambah ke Keranjang"):

        st.session_state.cart.append({
            "product_id":
                product_map[produk]["product_id"],
            "produk":
                produk,
            "qty":
                qty,
            "harga":
                harga,
            "subtotal":
                subtotal
        })

        st.success(
            "Produk ditambahkan"
        )


    # -------------------------
    # Cart Display
    # -------------------------

    st.subheader("Keranjang")

    if len(st.session_state.cart) > 0:

        cart_df = pd.DataFrame(
            st.session_state.cart
        )

        st.dataframe(
            cart_df[
                ['produk',
                'qty',
                'harga',
                'subtotal']
            ]
        )

        grand_total = cart_df[
            "subtotal"
        ].sum()

        st.metric(
            "Grand Total",
            f"EUR {grand_total}"
        )


        # Payment Method
        pembayaran = st.selectbox(
            "Metode Pembayaran",
            [
                "Cash",
                "Debit Card",
                "Credit Card"
            ]
        )


        # -------------------------
        # Checkout
        # -------------------------

        if st.button("Checkout"):

            payload = {
                "payment_method": pembayaran,
                "branch_id":
                    st.session_state.branch_id,
                "items":[
                    {
                        "product_id":
                            item["product_id"],
                        "qty":
                            item["qty"]
                    }
                    for item in st.session_state.cart
                ]
            }

            try:

                with st.spinner(
                    "Menyimpan transaksi..."
                ):

                    response = requests.post(
                        "http://localhost:8000/sales",
                        json=payload,
                        timeout=10
                    )

                if response.status_code == 200:

                    result = response.json()

                    st.session_state.success_msg = (
                        f"Transaksi berhasil. "
                        f"Order #{result['order_id']}"
                    )

                    st.session_state.cart = []

                    st.rerun()

                else:
                    st.error(
                        "Gagal menyimpan transaksi"
                    )

            except requests.exceptions.RequestException:
                st.error(
                    "API tidak dapat diakses"
                )

    else:
        st.info(
            "Keranjang masih kosong"
        )

    if "success_msg" in st.session_state:
        st.success(st.session_state.success_msg)
        del st.session_state.success_msg
        

if st.session_state.logged_in:
    main_app()
else:
    login_page()