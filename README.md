# Ecommerce API

This README describes the **Ecommerce API** Django REST Project made by Tommaso Ticci for the "Progettazione e produzione multimediale" course.

---

## Live Hosting

The project runs live at:

```
https://ecommerceapi-production-8d69.up.railway.app/
```

_[ **Nota per il professore**: per testare un utente moderatore, utilizzare username TestModerator e come password la mia matricola (di Ticci Tommaso) ]_

---

## Local deployment

The repository contains the `settings.py` used for deployment. For **local development**, modify:

* Generate your own secret key and replace:

  ```python
  SECRET_KEY = "your_new_secret_key"
  ```
* Ensure:

  ```python
  DEBUG = True
  ```
  
* In the file `index.html`, don't forget to change at line 147:

    ```javascript
    const API_BASE = 'https://ecommerceapi-production-8d69.up.railway.app/api';
    ```
    
    to:
    
    ```javascript
    const API_BASE = 'http://127.0.0.1:8000/api';

* Run migrations:

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
* Create a superuser to access the admin:

  ```bash
  python manage.py createsuperuser
  ```
* Run:

  ```bash
  python manage.py runserver
  ```

---

## Structure

The **API is structured to handle users, products, carts and orders** in a RESTful manner.

### Main endpoints

| Endpoint                     | Method         | Description                                          |
|------------------------------| -------------- |------------------------------------------------------|
| `/api/users/register/`       | POST           | Register a user                                      |
| `/api/token/`                | POST           | Obtain JWT access and refresh token                  |
| `/api/token/refresh/`    | POST           | Refresh JWT access token                             |
| `/api/shop/products/`        | GET            | List all products                                    |
| `/api/shop/products/<id>/`   | GET/PUT/DELETE | Retrieve, update, delete product (moderators only)   |
| `/api/shop/cart/`            | GET/POST       | View or create user cart                             |
| `/api/shop/cart/<id>/add_item/` | POST           | Add item to cart                                     |
| `/api/shop/cart/<id>/remove_item/` | DELETE         | Remove item from cart                                |
| `/api/shop/orders/`          | POST           | Create an order from cart                            |
| `/api/shop/orders/user/`     | GET            | View user's own orders                               |
| `/api/shop/orders/admin/`    | GET            | View all orders (moderators only)                                     |
| `/api/shop/orders/<id>/`     | PATCH/DELETE   | Update order status / delete order (moderators only) |

---

## Authentication

The API uses **JWT authentication** via `rest_framework_simplejwt`.

1️⃣ Register:

```bash
http POST http://127.0.0.1:8000/api/users/register/ email="user@email.com" username="username" password="password" password2="password"
```

2️⃣ Obtain token:

```bash
http POST http://127.0.0.1:8000/api/token/ username="username" password="password"
```

This returns:

```json
{
  "refresh": "your_refresh_token",
  "access": "your_access_token"
}
```

3️⃣ Use the access token for authenticated requests:

```bash
http GET http://127.0.0.1:8000/api/shop/products/ "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Frontend

The project includes a **simple frontend** (`templates/index.html`) using **vanilla JavaScript** and fetch to interact with the REST API, supporting:

* User registration and login
* Product browsing
* Cart management
* Order placement
* User order history
* User profile management
* Moderator management interfaces

If logged in as a moderator, a **blue button** appears to access the moderator menu.

---

## Database Structure

### User

Extends Django's `AbstractUser`, with new fields:
* `is_moderator`: Boolean to check if the user is a moderator
* `is_active`: Boolean to check if the user is active; an inactive user cannot log in

### Product

* `name`, `description`, `quantity_available`, `price`, `discount`
* `is_purchasable`: Boolean to check if the product can be purchased
* `is_discounted`: Boolean to check if the product is discounted

### Cart & CartItem

* `Cart`: one-to-one with User
* `CartItem`: foreign keys to Cart and Product, with quantity

### Order & OrderItem

* `Order`: foreign key to User, amount, shipping address, status
* `OrderItem`: foreign keys to Order and Product, quantity, price

---

## Technologies

* **Django 5.2.3**
* **Django REST Framework**
* **JWT Authentication** (`rest_framework_simplejwt`)
* **Railway deployment ready**
* **SQLite**

---

## Cleaning Database (Development)

To reset your local database:

```bash
python manage.py flush
```

*(Be cautious: this will wipe all data)*

---

## License

This project is only for educational purposes under **University of Florence - PPM**.
