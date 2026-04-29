#nyalakan api uvicorn serviceapi:app --reload
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine,text
from typing import List
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")

app = FastAPI()

class SaleItem(BaseModel):
    product_id: int
    qty: int


class SaleRequest(BaseModel):
    payment_method: str
    branch_id: int
    customer_id: Optional[int] = None
    employee_id: Optional[int] = None
    items: List[SaleItem]

class LoginRequest(BaseModel):
    employee_id:int

@app.get("/customers")
def get_customers():

    sql="""
    select customer_id,
           CONCAT(first_name, ' ', last_name) AS full_name
    from customers
    """

    with engine.connect() as conn:
        rows = conn.execute(text(sql)).mappings().all()

    return rows
@app.get("/products")
def get_products():

    sql="""
    select product_id,
           product_name,
           unit_price
    from products
    """

    with engine.connect() as conn:
        rows = conn.execute(text(sql)).mappings().all()

    return rows

@app.get("/branch")
def get_branches():

    sql="""
    select branch_id,
           branch_name,
           address
    from branches
    """

    with engine.connect() as conn:
        rows = conn.execute(text(sql)).mappings().all()

    return rows

@app.post("/sales")
def create_sale(sale: SaleRequest):

    with engine.begin() as conn:

        grand_total = 0
        line_items = []

        # -------------------------
        # hitung seluruh item
        # -------------------------
        for item in sale.items:

            product = conn.execute(
                text("""
                select product_id,
                    product_name,
                    unit_price
                from products
                where product_id=:id
                """),
                {"id": item.product_id}
            ).fetchone()

            price = product.unit_price

            subtotal = price * item.qty

            grand_total += subtotal

            line_items.append({
                "product_id": item.product_id,
                "qty": item.qty,
                "price": price,
                "subtotal": subtotal,
                "grand_total": grand_total
            })

        # -------------------------
        # INSERT sales (header)
        # -------------------------

        sale_header = conn.execute(
            text("""
            insert into orders(
                order_datetime,
                payment_method,
                branch_id,
                customer_id,
                employee_id,
                subtotal,
                vat_amount,
                total_amount
            )
            values(
                CURRENT_DATE,
                :payment_method,
                :branch_id,
                :customer_id,
                :employee_id,
                :subtotal,
                0,
                :grand_total
            )
            returning order_id
            """),
            {
                "payment_method": sale.payment_method,
                "branch_id": sale.branch_id,
                "customer_id":sale.customer_id, # hardcode for now
                "employee_id":sale.employee_id, # hardcode for now
                "subtotal": grand_total,
                "grand_total": grand_total
            }
        ).fetchone()

        order_id = sale_header[0]


        # -------------------------
        # INSERT sales_item (detail)
        # -------------------------

        for row in line_items:

            conn.execute(
                text("""
                insert into order_items(
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    line_total
                )
                values(
                    :order_id,
                    :product_id,
                    :qty,
                    :price,
                    :subtotal
                )
                """),
                {
                    "order_id": order_id,
                    "product_id": row["product_id"],
                    "qty": row["qty"],
                    "price": row["price"],
                    "subtotal": row["subtotal"]
                }
            )

    return {
       "message":"saved",
       "order_id": order_id
    }

@app.post("/login")
def login(req: LoginRequest):

    with engine.connect() as conn:

        user = conn.execute(
            text("""
            SELECT employee_id,
                   CONCAT(first_name, ' ', last_name) AS full_name,
                   position_title,
                branch_id,
                 branch_name
            FROM employees
            LEFT JOIN branches USING(branch_id)
            WHERE employee_id=:u
            """),
            {
                "u": req.employee_id
            }
        ).mappings().first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid employee ID"
        )

    return {
        "user_id": user["employee_id"],
        "username": user["full_name"],
        "role": user["position_title"],
        "branch_id": user["branch_id"],
        "branch_name": user["branch_name"]
    }