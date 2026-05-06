
import requests
import streamlit as st
import random

class pageComponents:
    def components_order_channel():
        order_channels = ["Auto (Random)", "Catering", "Online", "Telefoon", "Winkel"]
        
        selected_channel = st.selectbox(
            "Order Channel",
            options=order_channels
        )

        # Inisialisasi
        if "final_channel" not in st.session_state:
            st.session_state.final_channel = None

        if "last_selected_channel" not in st.session_state:
            st.session_state.last_selected_channel = None

        if selected_channel == "Auto (Random)":

            # jika user BARU pindah ke Auto → generate ulang
            if st.session_state.last_selected_channel != "Auto (Random)":
                st.session_state.final_channel = random.choices(
                    ["Online", "Winkel", "Telefoon", "Catering"],
                    weights=[0.5, 0.3, 0.15, 0.05]
                )[0]

        else:
            st.session_state.final_channel = selected_channel


        # simpan pilihan terakhir
        st.session_state.last_selected_channel = selected_channel

        st.write(f"Channel Penjualan: {st.session_state.final_channel}")
    
        
    def components_customer(customer_map):
        st.subheader("Informasi Customer")

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

        return customer_id
    
    def components_product(product_map):
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
        vat = subtotal * 0.09
        st.write(
            f"Subtotal: EUR {subtotal:.2f}"
        )


        if st.button("Tambah ke Keranjang"):

            product_id = product_map[produk]["product_id"]

            found = False

            for item in st.session_state.cart:
                if item["product_id"] == product_id:
                    item["qty"] += qty
                    item["subtotal"] = item["qty"] * item["harga"]
                    item["vat"] = item["subtotal"] * 0.09
                    found = True
                    break

            if not found:
                st.session_state.cart.append({
                    "product_id": product_id,
                    "produk": produk,
                    "qty": qty,
                    "harga": harga,
                    "subtotal": subtotal,
                    "vat": vat
                })

            st.success("Produk ditambahkan")


    def components_cart():
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

            grand_total_bfr_vat = sum(item["subtotal"] for item in st.session_state.cart) 
            grand_total_vat = grand_total_bfr_vat * 0.09  # Assuming 20% VAT
            grand_total = grand_total_bfr_vat + grand_total_vat 
            
            kol1, kol2, kol3 = st.columns(3)
            with kol1:
                st.metric("Grand Total", f"EUR {grand_total_bfr_vat:.2f}")
            with kol2:
                st.metric("VAT (9%)", f"EUR {grand_total_vat:.2f}")
            with kol3:
                st.metric("Total (incl. VAT)", f"EUR {grand_total:.2f}")

    def components_pembayaran(payment_map):
        pembayaran = st.selectbox(
                "Metode Pembayaran",
                options=list(payment_map.keys())
            )
        return pembayaran
        
    def components_checkout(pembayaran,customer_id):
        if st.button("Checkout"):

                payload = {
                    "payment_method": pembayaran,
                    "branch_id":
                        st.session_state.branch_id,
                    "customer_id": customer_id,
                    "employee_id": st.session_state.user,
                    "order_channel": st.session_state.final_channel,
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
                print(payload)
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

                        # st.rerun()
                    else:
                        error = response.json().get("detail", "Gagal menyimpan transaksi")
                        st.error(error)

                except requests.exceptions.RequestException:
                    st.error(
                        "API tidak dapat diakses"
                    )

    def components_branch(branch_map):
        st.subheader(f"Nama Branches")

        branches_options = list(branch_map.keys())
        pilih_branch = st.selectbox(
            "Pilih Branch",
            options=branches_options
        )

        selected_branch = branch_map[pilih_branch]

        if st.session_state.get("branch_id") != selected_branch["branch_id"]:
            st.session_state.branch_id = selected_branch["branch_id"]
            st.session_state.branch_name = selected_branch["branch_name"]

        return pilih_branch