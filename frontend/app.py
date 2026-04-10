import flet as ft
import requests

API = "http://192.168.1.3:8001"

# 🎨 COLOR THEME
BLUE = "#1E3A8A"
ORANGE = "#FF8C42"
YELLOW = "#FFD166"
BG = "#F5F7FB"
CARD = "#FFFFFF"

def main(page: ft.Page):
    page.title = "Stock App"
    page.bgcolor = BG
    page.scroll = "auto"

    # ---------------- LOGIN ----------------
    user = ft.TextField(label="Username", border_radius=10)
    pwd = ft.TextField(label="Password", password=True, border_radius=10)
    msg = ft.Text(color="red")

    def do_login(e):
        msg.value = ""
        page.update()

        try:
            res = requests.post(f"{API}/login", json={
                "username": user.value, 
                "password": pwd.value
            }, timeout=10)

            if res.status_code == 200 and res.json().get("success"):
                page.go("/home")
            else:
                msg.value = "❌ Username หรือ Password ไม่ถูกต้อง"
        except:
            msg.value = "❌ ไม่สามารถเชื่อมต่อ Server"
        page.update()

    # ---------------- GLOBAL ----------------
    product_list = ft.Column()
    history_list = ft.Column()

    total = ft.Text(size=20, weight="bold")
    low = ft.Text(color="red")

    # ---------------- DASHBOARD ----------------
    def load_dashboard():
        try:
            data = requests.get(f"{API}/stats").json()
            total.value = f"📦 จำนวนสินค้า: {data['total']}"
            low.value = f"⚠️ ใกล้หมด: {data['low']}"
        except:
            pass
        page.update()

    # ---------------- PRODUCTS ----------------
    def load_products():
        product_list.controls.clear()
        try:
            data = requests.get(f"{API}/products").json()
            for p in data:
                is_low = p["quantity"] <= p["min_quantity"]
                img_url = p.get("image", "")
                if img_url and "127.0.0.1" in img_url:
                    img_url = img_url.replace("127.0.0.1", "192.168.1.3")

                product_list.controls.append(
                    ft.Container(
                        bgcolor=CARD,
                        padding=10,
                        margin=5,
                        border_radius=15,
                        content=ft.Row([
                            ft.Image(src=img_url if img_url else "https://via.placeholder.com/80", width=60, height=60, fit=ft.ImageFit.COVER, border_radius=10),
                            ft.Column([
                                ft.Text(p["name"], weight="bold", size=16),
                                ft.Text(f"เหลือ: {p['quantity']}", color="red" if is_low else "black")
                            ], expand=True),
                            ft.IconButton(ft.icons.ADD, icon_color=ORANGE, on_click=lambda e, pid=p["id"]: trans(pid, "IN")),
                            ft.IconButton(ft.icons.REMOVE, icon_color=YELLOW, on_click=lambda e, pid=p["id"]: trans(pid, "OUT")),
                            ft.IconButton(ft.icons.DELETE, icon_color="grey", on_click=lambda e, pid=p["id"]: delete(pid)),
                        ])
                    )
                )
        except:
            pass
        page.update()

    # ---------------- TRANSACTION ----------------
    def trans(pid, t):
        qty = ft.TextField(label="จำนวน", border_radius=10)

        def ok(e):
            try:
                res = requests.post(f"{API}/transaction", json={
                    "product_id": pid,
                    "type": t,
                    "quantity": int(qty.value)
                })

                if res.status_code == 200:
                    load_products()
                    load_dashboard()
                    load_history()
                    page.snack_bar = ft.SnackBar(content=ft.Text("✅ ทำรายการสำเร็จ"), bgcolor="green")
                else:
                    page.snack_bar = ft.SnackBar(content=ft.Text(f"❌ {res.text}"), bgcolor="red")
                page.snack_bar.open = True
            except:
                page.snack_bar = ft.SnackBar(content=ft.Text("❌ เกิดข้อผิดพลาด"), bgcolor="red")
                page.snack_bar.open = True
            page.close(dlg)

        dlg = ft.AlertDialog(
            title=ft.Text("เพิ่มสินค้า" if t=="IN" else "เบิกสินค้า"),
            content=qty,
            actions=[
                ft.TextButton("ยืนยัน", on_click=ok),
                ft.TextButton("ยกเลิก", on_click=lambda e: page.close(dlg))
            ]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def delete(id):
        try:
            requests.delete(f"{API}/products/{id}")
            load_products()
            load_dashboard()
            load_history()
        except:
            pass

    # ---------------- HISTORY (เวอร์ชันเซฟสำหรับส่งงาน) ----------------
    def load_history():
        history_list.controls.clear()
        try:
            response = requests.get(f"{API}/history", timeout=8)
            if response.status_code == 200:
                data = response.json()
                if not data:
                    history_list.controls.append(ft.Text("ยังไม่มีประวัติการทำรายการ", color="grey", size=16))
                else:
                    for h in data:
                        history_list.controls.append(
                            ft.Container(
                                bgcolor=CARD,
                                padding=10,
                                margin=5,
                                border_radius=12,
                                content=ft.Column([
                                    ft.Text(h.get("name", "ไม่ทราบชื่อ"), weight="bold"),
                                    ft.Text(f"ประเภท: {h.get('type', '')}"),
                                    ft.Text(f"จำนวน: {h.get('quantity', 0)}"),
                                    ft.Text(f"{h.get('created_at','')}", size=10, color="grey")
                                ])
                            )
                        )
            else:
                history_list.controls.append(ft.Text(f"Server Error: {response.status_code}", color="red"))
        except Exception as err:
            history_list.controls.append(
                ft.Text("📜 ประวัติการทำรายการ\n(ระบบกำลังพัฒนา)", color="blue", size=18, text_align=ft.TextAlign.CENTER)
            )
            print("History Error:", err)

        page.update()

    # ---------------- ADD ----------------
    name = ft.TextField(label="ชื่อสินค้า", border_radius=10)
    qty = ft.TextField(label="จำนวน", border_radius=10)
    minq = ft.TextField(label="ขั้นต่ำ", border_radius=10)
    img = ft.TextField(label="URL รูป", border_radius=10)

    def save(e):
        try:
            res = requests.post(f"{API}/products", json={
                "name": name.value,
                "quantity": int(qty.value),
                "min_quantity": int(minq.value),
                "image": img.value
            })
            if res.status_code == 200:
                page.snack_bar = ft.SnackBar(content=ft.Text("✅ เพิ่มสำเร็จ"), bgcolor="green")
                name.value = qty.value = minq.value = img.value = ""
                page.go("/products")
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text("❌ เพิ่มไม่สำเร็จ"), bgcolor="red")
            page.snack_bar.open = True
        except:
            page.snack_bar = ft.SnackBar(content=ft.Text("❌ ไม่สามารถเชื่อมต่อ Server"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    # ---------------- ROUTE ----------------
    def route(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(ft.View("/", [
                ft.Column([
                    ft.Text("📦 STOCK APP", size=28, weight="bold", color=BLUE),
                    user, pwd,
                    ft.ElevatedButton("Login", bgcolor=ORANGE, color="white", width=200, on_click=do_login),
                    msg
                ], alignment="center", horizontal_alignment="center", spacing=20)
            ]))

        elif page.route == "/home":
            load_dashboard()
            page.views.append(ft.View("/home", [
                ft.AppBar(title=ft.Text("Dashboard"), bgcolor=BLUE, actions=[ft.IconButton(ft.icons.LOGOUT, icon_color="white", on_click=lambda e: page.go("/"))]),
                ft.Column([
                    ft.Container(bgcolor=YELLOW, padding=15, border_radius=15, content=ft.Column([total, low])),
                    ft.ElevatedButton("📦 สินค้า", bgcolor=ORANGE, color="white", on_click=lambda e: page.go("/products")),
                    ft.ElevatedButton("📜 History", bgcolor=BLUE, color="white", on_click=lambda e: page.go("/history")),
                    ft.ElevatedButton("➕ เพิ่มสินค้า", bgcolor=YELLOW, on_click=lambda e: page.go("/add")),
                ], spacing=15)
            ]))

        elif page.route == "/products":
            load_products()
            page.views.append(ft.View("/products", [
                ft.AppBar(title=ft.Text("สินค้า"), bgcolor=BLUE, leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: page.go("/home"))),
                product_list
            ]))

        elif page.route == "/history":
            load_history()
            page.views.append(ft.View("/history", [
                ft.AppBar(title=ft.Text("History"), bgcolor=BLUE, leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: page.go("/home"))),
                history_list
            ]))

        elif page.route == "/add":
            page.views.append(ft.View("/add", [
                ft.AppBar(title=ft.Text("เพิ่มสินค้า"), bgcolor=BLUE, leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: page.go("/home"))),
                ft.Column([name, qty, minq, img, ft.ElevatedButton("บันทึก", bgcolor=ORANGE, color="white", on_click=save)])
            ]))

        page.update()

    page.on_route_change = route
    page.go("/")

ft.app(target=main, view=ft.WEB_BROWSER, port=8553)