## 🛒 Shopping Cart API (Multi-User + Idempotency)

A production-inspired REST API built with **FastAPI** that supports **multi-user shopping carts**, **idempotent operations**, and **clean separation of business logic**.

---

##  Why This Project?

This project goes beyond basic CRUD APIs and demonstrates **real-world backend engineering concepts** such as idempotency, user-isolated state, and strategy-based pricing logic.

---

##  Features

*  Multi-user carts using `cart_id`
*  Idempotent item addition using `Idempotency-Key`
*  Discount strategies (None / Percentage / Flat)
*  Stateless API design
*  Clean domain-driven structure
*  Swagger/OpenAPI documentation

---


##  Architecture Overview

```
Client → FastAPI → Idempotency Store → Cart Store → ShoppingCart
```

* **FastAPI**: HTTP handling & validation
* **ShoppingCart**: Core business/domain logic
* **cart_store**: User cart isolation
* **idempotency_store**: Safe retry handling

---

##  API Endpoints

###  Add Item (Idempotent)

```
POST /cart/{cart_id}/item
Headers:
  Idempotency-Key: <unique-key>
Body:
{
  "name": "iphone",
  "price": 10200
}
```

---

###  Get Cart Items

```
GET /cart/{cart_id}/items
```

---

###  Apply Discount

```
POST /cart/{cart_id}/discount
Body:
{
  "type": "percentage",
  "value": 10
}
```

---

###  Get Cart Total

```
GET /cart/{cart_id}/total
```

---

###  Reset Cart

```
POST /cart/{cart_id}/reset
```

---

## 🔐 Idempotency Explained

Using the same `Idempotency-Key` for retries ensures the request is processed **only once**, preventing duplicate item additions and ensuring safe retry behavior.

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🔮 Future Improvements

* Redis-backed cart store
* JWT authentication
* Cart expiration (TTL)
* Database persistence
* Async processing

> Note: In-memory storage is used for simplicity. In production, Redis or a database would be used.

---

## 🏁 Final Verdict

This project demonstrates **production-grade backend thinking** and is suitable for **technical interviews**, **portfolio showcasing**, and **real-world system design discussions**.

---


