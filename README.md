# ☕ Coffee Shop POS System (Django + Clover Integration)

This project is a **Coffee Shop POS (Point of Sale)** application built with **Django** and integrated with the **Clover API**. It simulates real-world coffee shop operations — including menu management, order creation, and automatic syncing with Clover Merchant data.

---

## 🚀 Features

- 🍽️ Display and manage menu items  
- 🛒 Add items to the cart  
- 💳 Place orders through the POS interface  
- 🔗 Send order data to **Clover Merchant** using the Clover API  
- 🌐 Expose local Django server to the internet using **ngrok** for testing Clover webhooks and integrations  

---

## 🧠 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | Django (Python) |
| Database | PostgreSQL |
| API Integration | Clover REST API |
| Frontend | HTML, CSS, JavaScript |
| Local Tunneling | ngrok |
| ORM | Django ORM |
| Package Manager | pip + virtualenv |

---

## ⚙️ Project Setup

### 1. Clone Repository
```bash
git clone https://github.com/muhammad-ahmad-yousaf/coffee_shop.git
cd coffee_shop
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database
Create a PostgreSQL database and update your `.env` file:
```
DATABASE_URL=postgresql://username:password@localhost:5432/coffee_shop_pos
SECRET_KEY=your_secret_key
DEBUG=True
CLOVER_BASE_URL=https://sandbox.dev.clover.com
CLOVER_MERCHANT_ID=your_merchant_id
CLOVER_ACCESS_TOKEN=your_access_token
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

The app will be available at:  
👉 `http://127.0.0.1:8000/`

---

## 🌍 ngrok Setup (for Clover Webhooks)

Clover requires a public HTTPS endpoint to send data (e.g., webhooks, order syncs).  
Use **ngrok** to expose your local Django server.

### Start ngrok
```bash
ngrok http 8000
```

Copy the forwarding URL (e.g., `https://abcd1234.ngrok.io`) and update it in your Clover Developer Dashboard under:
> **App URL → Redirect / Webhook URLs**

---

## 🧩 Clover Integration

### Create Order Example

```python
order_url = f"{settings.CLOVER_BASE_URL}/v3/merchants/{merchant_id}/orders"
create_order_body = {"state": "OPEN"}
response = requests.post(order_url, headers=headers, json=create_order_body)
```

- `state: "OPEN"` means the order is currently active and editable.
- You can later update the order to `"CLOSED"` after payment or completion.

### Retrieve Orders

```python
orders_url = f"{settings.CLOVER_BASE_URL}/v3/merchants/{merchant_id}/orders"
response = requests.get(orders_url, headers=headers)
orders = response.json()
```

---

## 🧪 Testing the Flow

1. Add items to your cart from the **menu page**.  
2. Go to the **cart page** and click **Place Order**.  
3. Django creates an order locally and syncs it to **Clover Merchant**.  
4. Check your Clover Dashboard to confirm the order.

---

## 📁 Folder Structure

```
coffee-shop-pos/
├── clover_integration/
│   ├── views.py
│   ├── utils.py
│   └── urls.py
├── menu/
│   ├── templates/
│   ├── views.py
│   ├── models.py
│   └── urls.py
├── cart/
│   ├── views.py
│   ├── templates/
│   └── urls.py
├── orders/
│   ├── views.py
│   ├── models.py
│   ├── templates/
│   └── urls.py
├── coffee_shop/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env
├── requirements.txt
└── README.md
```

---

## 🧰 Useful Commands

| Command | Description |
|----------|--------------|
| `python manage.py runserver` | Start local development server |
| `python manage.py makemigrations` | Generate new migrations |
| `python manage.py migrate` | Apply migrations |
| `python manage.py createsuperuser` | Create Django admin user |
| `ngrok http 8000` | Expose local server for Clover API |
| `python manage.py collectstatic` | Collect static files |

---

## 📜 License

This project is licensed under the **MIT License**.  
Feel free to modify and use it for your own coffee shop or POS project.

---

**Developed by:** Muhammad Ahmad Yousaf  
☕ *Integrating real-world POS systems with modern web technology.*
