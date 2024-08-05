

# OreRestaurant

OreRestaurant is a Flask-based web application for managing a restaurant's menu, user accounts, and orders. It includes features for staff to manage menus and view customer information, as well as for customers to view menus and place orders and other features.

Language: PYTHON FLASK

DB: SQLITE

## Features

- **User Registration and Login**: Staff and customers can register and log in using JWT authentication.
- **Menu Management**: Staff can create, update, and delete menu items. Customers can view all menus and their details.
- **Order Management**: Customers can place orders, and staff can view all orders.
- **User Management**: Staff can view and manage user accounts.
- **Profile Management**: Users can update their profile information.

## Installation

To run the OreRestaurant project on your local machine, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ore_restaurant.git or fork and clone
cd ore_restaurant
```

### 2. Create and Activate a Virtual Environment

**For Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///instance/ore_restaurant.db
JWT_SECRET_KEY=your_jwt_secret_key
```

- Replace `your_secret_key` with a secret key for your Flask application.
- Replace `your_jwt_secret_key` with a secret key for JWT authentication.

### 5. Initialize the Database

Run the following commands to set up the database:

```bash
flask db upgrade
```

This will create the necessary tables in your SQLite database.

### 6. Run the Application

```bash
flask run
```

The application will be accessible at `http://127.0.0.1:5000/`.

## API Endpoints

### Authentication

- **POST /register**: Register a new user.
- **POST /login**: Log in and get a JWT access token.

### Menu Management 

- **GET /menus**: Get all menu items.
- **POST /menus**: Create a new menu item.
- **GET /menus/<menu_id>**: Get details of a specific menu item.
- **PUT /menus/<menu_id>**: Update a menu item.
- **DELETE /menus/<menu_id>**: Delete a menu item.
- **GET /menus/discounted**: Get all discounted menu items.
- **GET /menus/drinks**: Get all drink menu items.

### Order Management

- **GET /orders**: Get all orders for the current user.
- **POST /orders**: Place a new order.

### User Management (Staff Only)

- **GET /debug/users**: Get a list of all registered users.
- **GET /users/<user_id>**: Get details of a specific user.

### User Profile

- **GET /profile**: Get the profile of the current user.
- **PUT /profile**: Update the profile of the current user.

## Testing

To test the API endpoints, you can use tools like [Postman](https://www.postman.com/) or [cURL](https://curl.se/). 

### Example Requests

- **Register a User:**

```http
POST /register
Content-Type: application/json

{
  "username": "john_doe003",
  "email": "john003@example.com",
  "password": "securepassword003"
}
```

- **Login:**

```http
POST /login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}
```

- **Get All Menus:**

```http
GET /menus
Authorization: Bearer <your_jwt_token>
```

Flask
Flask-JWT-Extended
Flask-Migrate
Flask-SQLAlchemy
Werkzeug
 