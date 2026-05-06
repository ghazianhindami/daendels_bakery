import streamlit as st

class CartComponent:

    def __init__(self, cart):
        self.cart = cart

    def render(self):

        if len(self.cart.items) == 0:
            st.info("Keranjang kosong")
            return None

        for i, item in enumerate(self.cart.items):

            col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])

            col1.write(item["produk"])
            col2.write(item["qty"])
            col3.write(f"EUR {item['harga']:.2f}")
            col4.write(f"EUR {item['subtotal']:.2f}")

            if col5.button("-", key=f"minus_{i}"):
                self.cart.remove_or_decrease(i)
                st.rerun()

        return self.cart.totals()