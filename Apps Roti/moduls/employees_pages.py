import time as t

import streamlit as st

from .components.api_service import APIService
from .components.carts import Cart
from .components.session import SessionManager
from .components.header import HeaderComponent
from .components.components_page import pageComponents


def employee_service_app():

    # Init objects
    api = APIService()
    cart = Cart(st.session_state)
    session = SessionManager(st.session_state)

    header = HeaderComponent(session)
#     cart_ui = CartComponent(cart)

    st.subheader(f"Branch: {st.session_state.branch_name}")

    left, right = st.columns([3,3])

    with left:
        st.subheader(
            f"Selamat Bekerja, {st.session_state.full_name} ({st.session_state.role})"
        )
    # Render header
    with right:
        header.render()

#     # # Load data
    products = api.get_products()
    customers = api.get_customers()
    payments = api.get_payments()

    product_map = {
        p["product_name"]: p
        for p in products
    }

    customer_map = {
        c["customer_id"]: c
        for c in customers
    }

    payment_map = {
        p["method_name"]: p
        for p in payments
    }
#     # # UI
    final_channel = pageComponents.components_order_channel()

    customer_id = pageComponents.components_customer(customer_map)

    pageComponents.components_product(product_map)

    if len(st.session_state.cart) > 0:
        pageComponents.components_cart()
        pembayaran = pageComponents.components_pembayaran(payment_map)
        pageComponents.components_checkout(pembayaran=pembayaran,customer_id=customer_id)
    else:
        st.info("Silahkan pilih produk terlebih dahulu untuk melakukan checkout")

    if "success_msg" in st.session_state:
        st.success(st.session_state.success_msg)
        del st.session_state.success_msg

        t.sleep(3)  

        st.rerun()
