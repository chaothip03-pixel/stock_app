#  ระบบจัดการสต็อกสินค้า (Stock Management App)

##  ผู้จัดทำ

* รหัสนักศึกษา: 641310394
* ชื่อ: (ช่อทิพย์ คงมาลัย)

---

##  รายละเอียดโปรเจค

แอปพลิเคชันสำหรับจัดการสต็อกสินค้า สามารถเพิ่มสินค้า เบิกสินค้า และดูประวัติการใช้งานได้ โดยพัฒนาในรูปแบบ Mobile Web Application

---

##  เทคโนโลยีที่ใช้

* Backend: FastAPI (Python)
* Database: MariaDB
* Frontend: Flet (Python)
* API: RESTful API

---

##  ฟีเจอร์ของระบบ

*  Login / Logout
*  Dashboard แสดงจำนวนสินค้า
*  จัดการสินค้า (เพิ่ม / ลบ)
*  เพิ่มสินค้าใหม่
*  เบิกสินค้า
*  แสดงประวัติการทำรายการ (History)
*  แจ้งเตือนสินค้าใกล้หมด
*  ใช้งานผ่านมือถือได้

---

##  โครงสร้างโปรเจค

```
stock_app/
│
├── backend/
│   ├── main.py
│   └── database.py
│
├── frontend/
│   └── app.py
│
└── README.md
```

---

##  วิธีรันระบบ

### 1. รัน Backend

```
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. รัน Frontend

```
cd frontend
python app.py
```

---

##  การใช้งานผ่านมือถือ

เปิด Browser ในมือถือ แล้วเข้า:

```
http://<IPเครื่องคอม>:8550
```

---

##  ตัวอย่างหน้าจอ

###  หน้า Login
![Login](images/login.png)

###  Dashboard
![Dashboard](images/dashboard.png)

###  Products
![Products](images/products.png)



---

##  หมายเหตุ

ระบบนี้พัฒนาเพื่อการศึกษา และสามารถใช้งานได้จริงในระดับพื้นฐาน

