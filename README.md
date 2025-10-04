# 🍵 FastDispatch POS Dashboard

This is a **FastDispatch POS Dashboard** built with **Django**, **PostgreSQL**, **Prisma ORM**, and **Clover API** integration.  
The project allows a coffee shop (or similar POS environment) to manage **menu items, cart, and order processing** — including **real-time Clover order synchronization** via webhooks and **ngrok** tunneling for local development.

---

## 🚀 Features

- **User authentication** (Admin & Employee roles)
- **Dynamic Menu Management**
- **Cart System** – Add, remove, or update items
- **Order Placement** – Orders sent to Clover API
- **Clover API Integration** for:
  - Creating and managing orders (`/v3/merchants/{merchant_id}/orders`)
  - Adding line items to Clover orders
  - Syncing order state (OPEN → CLOSED)
- **Webhooks** – Real-time updates from Clover
- **Ngrok Tunneling** – For secure local testing with external APIs
- **Prisma ORM** – For clean and efficient database schema management
- **PostgreSQL Database**

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend Framework** | Django (Python) |
| **Database** | PostgreSQL |
| **ORM** | Prisma |
| **API Integration** | Clover POS API |
| **Local Tunnel** | ngrok |
| **Frontend** | Django Templates (HTML/CSS/JS) |
| **Environment** | `.env` configuration |

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/muhammad-ahmad-yousaf/coffee_shop.git
cd coffee_shop
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and include:

```
DATABASE_URL="postgresql://postgres:yourpassword@localhost:5432/faastdispatch_pos"
CLOVER_BASE_URL="https://sandbox.dev.clover.com"
CLOVER_MERCHANT_ID="your_merchant_id"
CLOVER_ACCESS_TOKEN="your_access_token"
NGROK_AUTH_TOKEN="your_ngrok_token"
DJANGO_SECRET_KEY="your_django_secret_key"
DEBUG=True
```

### 5. Run Prisma Schema

```bash
npx prisma generate
npx prisma db push
```

### 6. Apply Django Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Start Django Server

```bash
python manage.py runserver
```

### 8. Start ngrok (for external API callbacks)

```bash
ngrok http 8000
```

Copy the **Forwarding URL** (e.g. `https://abcd1234.ngrok.io`) and update it in your Clover developer dashboard webhook URLs.

---

## ☕ Clover API Usage

Below are key API interactions in this project:

### ➤ Create a New Order

```python
order_url = f"{settings.CLOVER_BASE_URL}/v3/merchants/{merchant_id}/orders"
create_order_body = {"state": "OPEN"}
response = requests.post(order_url, json=create_order_body, headers=headers)
```

### ➤ Add Line Item to Order

```python
line_item_url = f"{order_url}/{order_id}/line_items"
line_item_body = {"name": "Latte", "price": 450}
requests.post(line_item_url, json=line_item_body, headers=headers)
```

### ➤ Close an Order

```python
update_order_url = f"{order_url}/{order_id}"
requests.post(update_order_url, json={"state": "CLOSED"}, headers=headers)
```

---

## 🧠 Common Prisma/Django Commands

```bash
npx prisma studio          # Open database GUI
npx prisma format           # Format schema
python manage.py createsuperuser  # Create admin user
python manage.py runserver        # Start project
```

---

## 🧪 Testing Locally

- Visit: [http://127.0.0.1:8000/menu/](http://127.0.0.1:8000/menu/)
- Add items to cart, then checkout
- Orders will be sent to Clover sandbox merchant dashboard
- Check real-time logs in Django console

---

## 📦 Folder Structure

```
faastdispatch_pos_dashboard/
│
├── core/                   # Main Django app (views, models, urls)
├── prisma/                 # Prisma schema & migration files
├── templates/              # HTML templates for UI
├── static/                 # CSS, JS, and images
├── manage.py               # Django management script
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

---

## 🧾 License

This project is open-source under the **MIT License**.

---

## 👨‍💻 Author

**Muhammad Ahmad Yousaf**  
Cybersecurity Expert | Developer | Tech Enthusiast  
📧 [ahmadjutt611@gmail.com](mailto:ahmadjutt611@gmail.com)

