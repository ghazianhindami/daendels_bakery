import streamlit as st
import requests

def self_service_app():
    left, right = st.columns([3, 1])
    with right:
        if st.button("Logout"):
            st.session_state.self_service=False
            st.session_state.user=None
            st.session_state.full_name=None
            st.session_state.role=None
            st.session_state.branch_id=None
            st.session_state.branch_name=None

            st.success(
                "Logout berhasil"
            )

            st.rerun()

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
    def load_customers():
        return requests.get(
            "http://localhost:8000/customers",
            timeout=30
        ).json()
    
    @st.cache_data
    def load_branches():
        return requests.get(
            "http://localhost:8000/branch",
            timeout=30
        ).json()

    products = load_products()
    customer = load_customers()
    branches = load_branches()


    product_map = {
        p["product_name"]: p
        for p in products
    }

    customer_map = {
        c["customer_id"]: c
        for c in customer
    }

    branch_map = {
        b["branch_name"]: b
        for b in branches
    }

    # -------------------------
    # Branch
    # -------------------------

    st.subheader("Nama Branches")

    branches_options = list(branch_map.keys())
    pilih_branch = st.selectbox(
        "Pilih Branch",
        options=branches_options
    )
    st.write(branch_map[pilih_branch]["branch_name"])


    # -------------------------
    # Customer List
    # -------------------------

    customer_options = ["Walk-in Customer"] + list(customer_map.keys())

    pilih_customer = st.selectbox(
        "Pilih Customer",
        options=customer_options
    )

    if pilih_customer == "Walk-in Customer":
        customer_id = None
        pelanggan = None
        st.write("Pelanggan walk-in")
    else:
        customer_id = customer_map[pilih_customer]["customer_id"]
        pelanggan = customer_map[pilih_customer]["full_name"]

        st.write(
            f"Selamat berbelanja, {pelanggan}!"
        )
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
        f"Subtotal: EUR {subtotal:.2f}"
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

        for i in range(len(st.session_state.cart)):

            item = st.session_state.cart[i]

            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

            col1.write("Produk")
            col2.write("Qty")
            col3.write("Harga")
            col4.write("Subtotal")
            col5.write("Action")

            col1.write(item["produk"])
            col2.write(item["qty"])
            col3.write(f"EUR {item['harga']:.2f}")
            col4.write(f"EUR {item['subtotal']:.2f}")

            if col5.button("-", key=f"minus_{i}"):

                if item["qty"] > 1:
                    st.session_state.cart[i]["qty"] -= 1
                    st.session_state.cart[i]["subtotal"] = (
                        st.session_state.cart[i]["qty"] *
                        st.session_state.cart[i]["harga"]
                    )
                else:
                    st.session_state.cart.pop(i)

                st.rerun()

        grand_total = sum(item["subtotal"] for item in st.session_state.cart)

        st.metric("Grand Total", f"EUR {grand_total:.2f}")


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
                    branch_map[pilih_branch]["branch_id"],
                "customer_id": customer_id,
                "employee_id": st.session_state.user,
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

            st.write(payload)

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

                    st.write(result) 

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