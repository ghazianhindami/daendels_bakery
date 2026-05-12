import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh
from components.api_service import APIService

api = APIService()

st.title("Validator Orders")

# auto refresh tiap 3 detik
st_autorefresh(
    interval=3000,
    key="validator_refresh"
)

# ambil data order
orders = api.load_orders()

# filter pending
pending_orders = [
    o for o in orders
    if o["order_status"] == "In Behandeling"
]

st.subheader("Live Orders")

# jika kosong
if len(pending_orders) == 0:
    st.success("Tidak ada pembayaran pending")

# tampilkan order
for order in pending_orders:

    st.divider()

    col1, col2, col3 = st.columns([4, 2, 2])

    with col1:

        st.write(f"Order #{order['order_id']}")
        st.write(f"Channel: {order['order_channel']}")
        st.write(f"Payment: {order['payment_method']}")
        st.write(f"Total: EUR {order['total_amount']:.2f}")

    # tombol selesai
    with col2:

        if st.button(
            "✔ Voltooid",
            key=f"done_{order['order_id']}"
        ):

            response = requests.put(
                f"http://localhost:8000/orders/{order['order_id']}/complete"
            )

            if response.status_code == 200:
                st.success("Pembayaran berhasil divalidasi")
                st.rerun()

    # tombol cancel
    with col3:

        if st.button(
            "❌ Cancel",
            key=f"cancel_{order['order_id']}"
        ):

            response = requests.put(
                f"http://localhost:8000/orders/{order['order_id']}/cancel"
            )

            if response.status_code == 200:
                st.warning("Order dibatalkan")
                st.rerun()