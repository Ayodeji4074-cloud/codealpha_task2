#importing all necessary and required dependencies
import pytest
from flask import Flask
from app import create_app, db
from app.models import User, Menu, Order
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

#importing and getting access to the testing config class in app/config.py
@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create test users
        user1 = User(username='testuser1', email='test1@example.com', password=generate_password_hash('password1'), is_staff=False)
        user2 = User(username='testuser2', email='test2@example.com', password=generate_password_hash('password2'), is_staff=True)
        
        # Add users and commit to get IDs
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        # Print user IDs
        print(f"Created test users: {user1.id}, {user2.id}")

        # Create test menus
        menu1 = Menu(name='Pizza', description='Cheese Pizza', price=10.0, is_discounted=False, is_drink=False)
        menu2 = Menu(name='Cola', description='Soft Drink', price=2.0, is_discounted=True, is_drink=True)
        
        # Add menus and commit to get IDs
        db.session.add(menu1)
        db.session.add(menu2)
        db.session.commit()

        # Print menu IDs
        print(f"Created test menus: {menu1.id}, {menu2.id}")

        # Create test orders with correct user_id and menu_id
        order1 = Order(user_id=user1.id, menu_id=menu1.id, quantity=2)
        
        # Add orders and commit
        db.session.add(order1)
        db.session.commit()

        # Print order IDs
        print(f"Created test order: {order1.id}")

        yield

        # Teardown after tests
        db.session.remove()
        db.drop_all()

@pytest.fixture
def access_token_staff(client):
    user = User.query.filter_by(email='test2@example.com').first()
    print(f"Staff user: {user}")
    return create_access_token(identity={'id': user.id, 'is_staff': user.is_staff})

@pytest.fixture
def access_token_user(client):
    user = User.query.filter_by(email='test1@example.com').first()
    print(f"Regular user: {user}")
    return create_access_token(identity={'id': user.id, 'is_staff': user.is_staff})

#testing homepage endpoint
def test_homepage(client):
    response = client.get('/')
    print(f"Homepage response: {response.json}")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to Ore Restaurant"}

#testing register endpoint
def test_register(client):
    response = client.post('/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword',
        'is_staff': False
    })
    print(f"Register response: {response.json}")
    assert response.status_code == 201
    assert response.json == {"message": "User registered successfully"}

#testing if login is successful
def test_login_success(client, init_database):
    response = client.post('/login', json={
        'email': 'test1@example.com',
        'password': 'password1'
    })
    print(f"Login success response: {response.json}")
    assert response.status_code == 200
    assert 'access_token' in response.json

#testing login failure
def test_login_failure(client, init_database):
    response = client.post('/login', json={
        'email': 'test1@example.com',
        'password': 'wrongpassword'
    })
    print(f"Login failure response: {response.json}")
    assert response.status_code == 401
    assert response.json == {"message": "Invalid credentials"}

#testing the access to the dashboard endpoint
def test_dashboard_access_denied(client, access_token_user):
    response = client.get('/dashboard', headers={'Authorization': f'Bearer {access_token_user}'})
    print(f"Dashboard access denied response: {response.json}")
    assert response.status_code == 403
    assert response.json == {"message": "You do not have the permission to access this resource"}

#testing access granting to the dashboard endpoint
def test_dashboard_access_granted(client, access_token_staff):
    response = client.get('/dashboard', headers={'Authorization': f'Bearer {access_token_staff}'})
    print(f"Dashboard access granted response: {response.json}")
    assert response.status_code == 200
    data = response.json
    assert 'total_users' in data
    assert 'total_orders' in data
    assert 'total_revenue' in data

#testing the profile endpoint
def test_profile(client, access_token_user):
    response = client.get('/profile', headers={'Authorization': f'Bearer {access_token_user}'})
    print(f"Profile response: {response.json}")
    assert response.status_code == 200
    data = response.json
    assert 'username' in data
    assert 'email' in data
    assert 'registered_on' in data

#testing the updating profile endpoint
def test_update_profile(client, access_token_user):
    response = client.put('/profile', json={'username': 'updateduser'}, headers={'Authorization': f'Bearer {access_token_user}'})
    print(f"Update profile response: {response.json}")
    assert response.status_code == 200
    assert response.json == {"message": "Profile updated successfully"}

#testing the access denied endpoint to get all users 
def test_get_users_access_denied(client, access_token_user):
    response = client.get('/users', headers={'Authorization': f'Bearer {access_token_user}'})
    print(f"Get users access denied response: {response.json}")
    assert response.status_code == 403
    assert response.json == {"message": "You do not have the permission to access this resource"}

#testing the access granted endpoint to get all users 
def test_get_users_access_granted(client, access_token_staff):
    response = client.get('/users', headers={'Authorization': f'Bearer {access_token_staff}'})
    print(f"Get users access granted response: {response.json}")
    assert response.status_code == 200
    assert isinstance(response.json, list)

# testing the get user endpoint by id returning only username 
def test_get_user(client, access_token_staff):
    response = client.get('/users/1', headers={'Authorization': f'Bearer {access_token_staff}'})
    print(f"Get user response: {response.json}")
    assert response.status_code == 200
    assert 'id' in response.json
    assert 'username' in response.json
   
# # testing the get user endpoint by id returning email and username
def test_get_user(client, access_token_staff):
    response = client.get('/users/1', headers={'Authorization': f'Bearer {access_token_staff}'})
    print(f"Get user response: {response.json}")
    assert response.status_code == 200
    assert 'id' in response.json
    assert 'username' in response.json
    assert 'email' in response.json

# testing the manage menu endpoint
def test_manage_menus_get(client):
    response = client.get('/menus')
    print(f"Get menus response: {response.json}")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_manage_menus_post_access_denied(client, access_token_user):
    response = client.post('/menus', json={'name': 'Burger', 'description': 'Beef Burger', 'price': 5.0}, headers={'Authorization': f'Bearer {access_token_user}'})
    print(f"Post menu access denied response: {response.json}")
    assert response.status_code == 403
    assert response.json == {"message": "You do not have the permission to access this resource"}

def test_manage_menus_post_access_granted(client, access_token_staff):
    response = client.post('/menus', json={'name': 'Burger', 'description': 'Beef Burger', 'price': 5.0}, headers={'Authorization': f'Bearer {access_token_staff}'})
    print(f"Post menu access granted response: {response.json}")
    assert response.status_code == 201
    assert response.json == {"message": "Menu item created successfully"}

def test_manage_menu_get(client, init_database):
    response = client.get('/menus/1')
    print(f"Get menu response: {response.json}")
    assert response.status_code == 200
    data = response.json
    assert 'id' in data
    assert 'name' in data
    assert 'description' in data
    assert 'price' in data

def test_manage_menu_put_access_denied(client, access_token_user):
    response = client.put('/menus/1', json={'name': 'Updated Pizza'}, headers={'Authorization': f'Bearer {access_token_user}'})
    print(f"Put menu access denied response: {response.json}")
    assert response.status_code == 403
    assert response.json == {"message": "You do not have the permission to access this resource"}

def test_manage_menu_put_access_granted(client, access_token_staff):
    response = client.put('/menus/1', json={'name': 'Updated Pizza'}, headers={'Authorization': f'Bearer {access_token_staff}'})
    print(f"Put menu access granted response: {response.json}")
    assert response.status_code == 200
    assert response.json == {"message": "Menu item updated successfully"}

def test_manage_menu_delete_access_denied(client, access_token_user):
    response = client.delete('/menus/1', headers={'Authorization': f'Bearer {access_token_user}'})
    print(f"Delete menu access denied response: {response.json}")
    assert response.status_code == 403
    assert response.json == {"message": "You do not have the permission to access this resource"}

def test_manage_menu_delete_access_granted(client, access_token_staff):
    response = client.delete('/menus/1', headers={'Authorization': f'Bearer {access_token_staff}'})
    print(f"Delete menu access granted response: {response.json}")
    assert response.status_code == 200
    assert response.json == {"message": "Menu item deleted successfully"}

def test_manage_orders_post(client, access_token_user, init_database):
    response = client.post('/orders', json={'menu_id': 1, 'quantity': 1}, headers={'Authorization': f'Bearer {access_token_user}'})
    print(f"Post order response: {response.json}")
    assert response.status_code == 201
    assert response.json == {"message": "Order placed successfully"}

def test_get_all_orders_access_denied(client, access_token_user):
    response = client.get('/orders/all', headers={'Authorization': f'Bearer {access_token_user}'})
    print(f"Get all orders access denied response: {response.json}")
    assert response.status_code == 403
    assert response.json == {"message": "You do not have the permission to access this resource"}

def test_get_all_orders_access_granted(client, access_token_staff):
    response = client.get('/orders/all', headers={'Authorization': f'Bearer {access_token_staff}'})
    print(f"Get all orders access granted response: {response.json}")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_order_history(client, access_token_user, init_database):
    response = client.get('/orders/history', headers={'Authorization': f'Bearer {access_token_user}'})
    print(f"Order history response: {response.json}")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_discounted_menus(client, init_database):
    response = client.get('/menus/discounted')
    print(f"Get discounted menus response: {response.json}")
    assert response.status_code == 200
    assert isinstance(response.json, list)

#testing the get
def test_get_drink_menus(client, init_database):
    response = client.get('/menus/drinks')
    print(f"Get drink menus response: {response.json}")
    assert response.status_code == 200
    assert isinstance(response.json, list)
