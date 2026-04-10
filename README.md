#  ระบบจัดการคลังสินค้า (Stock Management Mobile App)

---

##  ภาพรวมโครงงาน
โปรเจคนี้เป็นแอปพลิเคชันสำหรับจัดการสินค้าในคลัง โดยผู้ใช้สามารถเพิ่ม ลบ และปรับจำนวนสินค้าได้ รวมถึงสามารถดูประวัติการทำรายการต่าง ๆ ได้ และสามารถใช้งานผ่านมือถือได้

---

##  วัตถุประสงค์
- เพื่อพัฒนาระบบจัดการสินค้า
- เพื่อบันทึกการเคลื่อนไหวของสินค้า (เพิ่ม / เบิก)
- เพื่อพัฒนาแอปพลิเคชันที่สามารถใช้งานบนมือถือได้

---

##  เทคโนโลยีที่ใช้
- Python
- FastAPI (Backend)
- Flet (Frontend Mobile App)
- MariaDB (Database)

---

##  ฟีเจอร์ของระบบ
- 🔐 Login / Logout
- 📊 Dashboard (แสดงจำนวนสินค้า และสินค้าที่ใกล้หมด)
- 📦 เพิ่มสินค้า
- ❌ ลบสินค้า
- ➕ เพิ่มจำนวนสินค้า
- ➖ เบิกสินค้า
- 📜 แสดงประวัติการทำรายการ (History)

---

##  โครงสร้างฐานข้อมูล

###  users
- id (Primary Key)
- username
- password

###  products
- id (Primary Key)
- name
- quantity
- min_quantity
- image

###  transactions
- id (Primary Key)
- product_id (Foreign Key)
- type (IN / OUT)
- quantity
- created_at

---

##  API ที่ใช้
- `/login` → เข้าสู่ระบบ
- `/products` → จัดการสินค้า
- `/transaction` → เพิ่ม / เบิกสินค้า
- `/history` → ดูประวัติ
- `/stats` → ข้อมูล Dashboard

---

## วิธีการรันโปรแกรม

###  1. รัน Backend (FastAPI)
```bash
uvicorn main:app --reload


 2. รัน Frontend (Flet)
python app.py
