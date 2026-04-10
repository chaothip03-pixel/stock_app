from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="p@ssword",
        database="stockdb",
        port=3307
    )

# ---------------- LOGIN ----------------
@app.post("/login")
def login(data: dict):
    db = None
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (data.get("username"), data.get("password"))
        )

        user = cursor.fetchone()
        return {"success": True} if user else {"success": False}

    except Exception as e:
        print("❌ LOGIN ERROR:", e)
        return {"success": False, "error": str(e)}
    finally:
        if db:
            db.close()   # ← สำคัญมาก! ปิด connection ทุกครั้ง


# ---------------- PRODUCTS ----------------
@app.get("/products")
def get_products():
    db = None
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()
    finally:
        if db:
            db.close()


@app.post("/products")
def create_product(p: dict):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO products (name, quantity, min_quantity, image)
            VALUES (%s,%s,%s,%s)
        """, (p["name"], p["quantity"], p["min_quantity"], p["image"]))
        db.commit()
        return {"msg": "ok"}
    finally:
        if db:
            db.close()


@app.delete("/products/{id}")
def delete_product(id: int):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM products WHERE id=%s", (id,))
        db.commit()
        return {"msg": "deleted"}
    finally:
        if db:
            db.close()


# ---------------- TRANSACTION ----------------
@app.post("/transaction")
def transaction(data: dict):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        product_id = data.get("product_id")
        qty = int(data.get("quantity", 0))
        t = data.get("type")

        print(f"[DEBUG] Transaction → ID: {product_id} | Type: {t} | Qty: {qty}")

        cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = cursor.fetchone()

        if not product:
            return {"error": "ไม่พบสินค้า"}

        current = product["quantity"]
        new_qty = current + qty if t == "IN" else current - qty

        if t == "OUT" and new_qty < 0:
            return {"error": "ของไม่พอ"}

        # อัพเดทจำนวน
        cursor.execute("UPDATE products SET quantity = %s WHERE id = %s", (new_qty, product_id))

        # เพิ่ม history
        cursor.execute(
            "INSERT INTO history (product_id, type, quantity) VALUES (%s, %s, %s)",
            (product_id, t, qty)
        )

        conn.commit()
        print(f"✅ สำเร็จ: {t} {qty} ชิ้น | เหลือ {new_qty}")
        return {"success": True}

    except Exception as e:
        print("❌ TRANSACTION ERROR:", str(e))
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


# ---------------- HISTORY ----------------
@app.get("/history")
def get_history():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT h.*, p.name
            FROM history h
            JOIN products p ON h.product_id = p.id
            ORDER BY h.id DESC
        """)

        data = cursor.fetchall()
        return data
    finally:
        if conn:
            conn.close()


# ---------------- STATS ----------------
@app.get("/stats")
def stats():
    db = None
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) as total FROM products")
        total = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) as low FROM products WHERE quantity <= min_quantity")
        low = cursor.fetchone()["low"]

        return {"total": total, "low": low}
    finally:
        if db:
            db.close()