#importing all required dependencies
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db

bp = Blueprint('main', __name__)

#using bp instead of app to route all endpoints
#landing page endpoint
@bp.route('/', methods=['GET'])
def homepage():
    return jsonify({"message": "Welcome to Ore Restaurant"}), 200

#register page endpoint
@bp.route('/register', methods=['POST'])
def register():
    from app.models import User
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    is_staff = data.get('is_staff', False)

    user = User(username=username, email=email, password=password, is_staff=is_staff)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

#login endpoint
@bp.route('/login', methods=['POST'])
def login():
    from app.models import User
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={'id': user.id, 'is_staff': user.is_staff})
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid credentials"}), 401

#dashboard endpoint that displays some informations
@bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    from app.models import Order, User
    current_user = get_jwt_identity()
    if not current_user['is_staff']:
        return jsonify({"message": "You do not have the permission to access this resource"}), 403

    total_users = User.query.count()
    total_orders = Order.query.count()
    from app.models import Menu
    total_revenue = db.session.query(db.func.sum(Menu.price * Order.quantity)).scalar()

    return jsonify({
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue
    }), 200


#profile endpoint that displays users details
@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    from app.models import User
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    return jsonify({
        'username': user.username,
        'email': user.email,
        'registered_on': user.registered_on
    }), 200
    

#endpoint that allows users profile updating
@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    from app.models import User
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

#endpoint that returns all users
@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    from app.models import User
    current_user = get_jwt_identity()
    if not current_user['is_staff']:
        return jsonify({"message": "You do not have the permission to access this resource"}), 403

    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users]), 200

#endpoint that return a user in respect to its id
@bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    from app.models import User
    current_user = get_jwt_identity()
    if not current_user['is_staff']:
        return jsonify({"message": "You do not have the permission to access this resource"}), 403

    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200

# endpoint that returns all menu and also add a new menu
@bp.route('/menus', methods=['GET', 'POST'])
@jwt_required(optional=True)
def manage_menus():
    from app.models import Menu
    if request.method == 'GET':
        menus = Menu.query.all()
        return jsonify([{
            'id': menu.id,
            'name': menu.name,
            'description': menu.description,
            'price': menu.price,
            'is_discounted': menu.is_discounted,
            'is_drink': menu.is_drink
        } for menu in menus]), 200

    if request.method == 'POST':
        current_user = get_jwt_identity()
        if not current_user or not current_user['is_staff']:
            return jsonify({"message": "You do not have the permission to access this resource"}), 403

        data = request.get_json()
        menu = Menu(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            is_discounted=data.get('is_discounted', False),
            is_drink=data.get('is_drink', False)
        )
        db.session.add(menu)
        db.session.commit()
        return jsonify({"message": "Menu item created successfully"}), 201

#endpoint that returns a menu in respect to its id
@bp.route('/menus/<int:menu_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required(optional=True)
def manage_menu(menu_id):
    from app.models import Menu
    menu = Menu.query.get_or_404(menu_id)

    #get the menu
    if request.method == 'GET':
        return jsonify({
            'id': menu.id,
            'name': menu.name,
            'description': menu.description,
            'price': menu.price,
            'is_discounted': menu.is_discounted,
            'is_drink': menu.is_drink
        }), 200

    current_user = get_jwt_identity()
    if not current_user or not current_user['is_staff']:
        return jsonify({"message": "You do not have the permission to access this resource"}), 403
    #update a menu
    if request.method == 'PUT':
        data = request.get_json()
        menu.name = data.get('name', menu.name)
        menu.description = data.get('description', menu.description)
        menu.price = data.get('price', menu.price)
        menu.is_discounted = data.get('is_discounted', menu.is_discounted)
        menu.is_drink = data.get('is_drink', menu.is_drink)
        db.session.commit()
        return jsonify({"message": "Menu item updated successfully"}), 200
    #delete a menu
    if request.method == 'DELETE':
        db.session.delete(menu)
        db.session.commit()
        return jsonify({"message": "Menu item deleted successfully"}), 200

#endpoint that post a new order
@bp.route('/orders', methods=['POST'])
@jwt_required()
def manage_orders():
    from app.models import Order, Menu
    current_user = get_jwt_identity()
    if request.method == 'POST':
        data = request.get_json()
        menu_id = data.get('menu_id')
        quantity = data.get('quantity', 1)

        menu = Menu.query.get_or_404(menu_id)
        order = Order(user_id=current_user['id'], menu_id=menu.id, quantity=quantity)
        db.session.add(order)
        db.session.commit()
        return jsonify({"message": "Order placed successfully"}), 201

#endpoint that get and returns all orders
@bp.route('/orders/all', methods=['GET'])
@jwt_required()
def get_all_orders():
    from app.models import Order, Menu
    current_user = get_jwt_identity()
    if not current_user['is_staff']:
        return jsonify({"message": "You do not have the permission to access this resource"}), 403

    orders = Order.query.all()
    return jsonify([{
        'id': order.id,
        'menu': {
            'id': order.menu.id,
            'name': order.menu.name,
            'description': order.menu.description,
            'price': order.menu.price
        },
        'quantity': order.quantity,
        'created_on': order.created_on
    } for order in orders]), 200

#endpoint that get and retruns all past orders as orders history
@bp.route('/orders/history', methods=['GET'])
@jwt_required()
def order_history():
    from app.models import Order
    current_user = get_jwt_identity()
    orders = Order.query.filter_by(user_id=current_user['id']).all()
    return jsonify([{
        'id': order.id,
        'menu': {
            'id': order.menu.id,
            'name': order.menu.name,
            'description': order.menu.description,
            'price': order.menu.price
        },
        'quantity': order.quantity,
        'status': order.status,
        'created_on': order.created_on
    } for order in orders]), 200


#endpoint that returns all menus with discount on them
@bp.route('/menus/discounted', methods=['GET'])
@jwt_required(optional=True)
def get_discounted_menus():
    from app.models import Menu
    menus = Menu.query.filter_by(is_discounted=True).all()
    return jsonify([{
        'id': menu.id,
        'name': menu.name,
        'description': menu.description,
        'price': menu.price,
        'is_discounted': menu.is_discounted,
        'is_drink': menu.is_drink,
    } for menu in menus]), 200

#endpoint that returns all drinks present in the menu list
@bp.route('/menus/drinks', methods=['GET'])
@jwt_required(optional=True)
def get_drink_menus():
    from app.models import Menu
    menus = Menu.query.filter_by(is_drink=True).all()
    return jsonify([{
        'id': menu.id,
        'name': menu.name,
        'description': menu.description,
        'price': menu.price,
        'is_discounted': menu.is_discounted,
        'is_drink': menu.is_drink,
    } for menu in menus]), 200
