import requests
import streamlit as st

class APIService:

    BASE_URL = "http://localhost:8000"

    @st.cache_data
    def get_products(_self):
        return requests.get(f"{_self.BASE_URL}/products", timeout=5).json()

    @st.cache_data
    def get_customers(_self):
        return requests.get(f"{_self.BASE_URL}/customers", timeout=30).json()

    @st.cache_data
    def get_branches(_self):
        return requests.get(f"{_self.BASE_URL}/branch", timeout=30).json()
    
    @st.cache_data
    def get_payments(_self):
        return requests.get(
            f"{_self.BASE_URL}/payment",
            timeout=30
        ).json()

    def create_order(_self, payload):
        return requests.post(
            f"{_self.BASE_URL}/sales",
            json=payload,
            timeout=10
        )