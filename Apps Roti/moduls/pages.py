import streamlit as st
import requests

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

#     # Render header
#     header.render()

#     # # Load data
    products = api.get_products()
    customers = api.get_customers()
    branches = api.get_branches()
    payments = api.get_payments()

    product_map = {
        p["product_name"]: p
        for p in products
    }

    customer_map = {
        c["customer_id"]: c
        for c in customers
    }

    branch_map = {
        b["branch_name"]: b
        for b in branches
    }

    payment_map = {
        p["method_name"]: p
        for p in payments
    }
#     # # UI
    pageComponents.components_order()
    pageComponents.components_customer(customer_map)
    pageComponents.components_product(product_map)
    if len(st.session_state.cart) > 0:
        pageComponents.components_cart()
        pageComponents.components_pembayaran(payment_map)
        pageComponents.components_checkout(pembayaran=pembayaran,final_channel=final_channel,customer_id=customer_id)
    else:
        st.info("Silahkan pilih produk terlebih dahulu untuk melakukan checkout")

# employee_service_app()

