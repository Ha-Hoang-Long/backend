
from sqlite3.dbapi2 import connect
from flask import Flask
from flask import jsonify
from flask import Request
from flask.globals import request
from flask import send_file
from time import time

from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt_identity

from .models.shipper_model import Shipper
from .actions.employee_action import Employee_Action
from .models.employee_model import Employee
from .actions.customer_action import Customer_Action
from .models.customer_model import Customer
from .actions.order_action import Order_Action
from .models.order_model import Order
from .models import employee_model
from .actions.user_action import User_Action
from .models import user_model
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'sdf8sdfn303n2nkl'
jwt = JWTManager(app)

connection_data = './db.sqlite3'
"""
    1. GET
    2. POST
    3. PUT(PATCH)
    4. DELETE
"""
@app.route('/', methods=['GET'])
def home():
    result= {
        'message':'Hello World',
        'status':'Success'
    }
    return result
@app.route('/customer')
def get_customer():
    customer_action = Customer_Action(connection_data)
    result = customer_action.get_all()
    return jsonify(result)
@app.route('/customer/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_or_modify_customer(id):
    if request.method == 'GET':
        #get_customer_by_id
        customer_action = Customer_Action(connection_data)
        result, status_code = customer_action.get_by_id(id)
        if status_code == 200:
            return jsonify(result.serialize()), status_code
        return jsonify({
            'message': result
        }), status_code
    elif request.method == 'PUT':
        #update customer by id
        body = request.json
        customer_name = body.get('customer_name','')
        contact_name = body.get('contact_name','')
        address = body.get('address','')
        city = body.get('city','')
        postal_code = body.get('postal_code','')
        country = body.get('country','')

        customer = Customer(customer_name=customer_name,contact_name=contact_name,address=address,city=city,postal_code=postal_code,country=country)
        customer_action = Customer_Action(connection_data)
        message, status_code = customer_action.update_by_id(id,customer)
        return jsonify({
            'message': message
        }), status_code
    elif request.method == 'DELETE':
        #delete customer by id
        customer = Customer(customer_id=id)
        customer_action = Customer_Action(connection_data)
        message, status_code = customer_action.delete(customer)
        return jsonify({
            'message': message
        }), status_code
    else:
        # 405
        pass


@app.route('/customer', methods=['POST'])
def add_customer():
    #lay du lieu tu request body
    body = request.json
    customer_name = body.get('customer_name','')
    contact_name = body.get('contact_name','')
    address = body.get('address','')
    city = body.get('city','')
    postal_code = body.get('postal_code','')
    country = body.get('country','')

    customer = Customer(customer_name=customer_name,contact_name=contact_name,address=address,city=city,postal_code=postal_code,country=country)
    customer_action = Customer_Action(connection_data)
    result = customer_action.add(customer)
    return jsonify({
        'message': result
    }), 200

# ORDER
@app.route('/order')
def get_order():
    order_action = Order_Action(connection_data)
    order = order_action.get_all()
    return jsonify(order)
@app.route('/order/<int:id>')
def get_order_by_id(id):
    order_action = Order_Action(connection_data)
    result, status_code = order_action.get_by_id(id)
    if status_code == 200:
        return jsonify(result.serialize()), status_code
    return jsonify({
        'message': result
    }), status_code
@app.route('/order',methods=['POST'])
def add_order():
    #from_data = request.form
    data = request.json

    customer_id = data.get('customer_id', 0)
    employee_id = data.get('employee_id', 0)
    order_date = data.get('order_date', '')
    shipper_id = data.get('shipper_id', 0)

    customer = Customer(customer_id=customer_id)
    employee = Employee(employee_id=employee_id)
    shipper = Shipper(shipper_id=shipper_id)

    order = Order(customer=customer, employee=employee, order_date=order_date, shipper=shipper)
    action = Order_Action(connection_data)
    message = action.add(order)
    return jsonify({
        'message': message
    })

#EMPLOYEE

@app.route('/employee')
@jwt_required()
def get_employee():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        action = Employee_Action(connection_data)
        employee = action.get_all()
        return jsonify(employee)
    return jsonify({
        'message': 'you do not have permission'
    }), 403
    employee_action = Employee_Action(connection_data)
    employee = employee_action.get_all()
    return jsonify(employee)
@app.route('/employee', methods=['POST'])
def add_employee():
    form_data = request.form

    last_name = form_data.get('last_name','')
    first_name = form_data.get('first_name','')
    birth_date = form_data.get('birth_day','')
    note = form_data.get('note','')
    
    photo = request.files['photo']
    file_name = str(int(time())) + '.jpg'
    photo.save(f'uploads/{file_name}')

    employee = employee_model.Employee(
        last_name=last_name,
        first_name=first_name,
        birth_date=birth_date,
        note=note,
        photo=file_name
    )

    action = Employee_Action(connection_data)
    result = action.add(employee)
    return jsonify({
        'message': result
    })
@app.route('/image/<string:image_name>')
def get_image(image_name):
    return send_file(f'uploads/{image_name}', mimetype='image/jpeg')

#USER

@app.route('/login', methods=['POST'])
def login():
    user_name = request.json.get('user_name', None)
    user_password = request.json.get('user_password', None)
    if user_name == None or user_password is None:
        return jsonify({
            'message': 'Missing username or password'
        }), 400
    user_action = User_Action(connection_data)
    result,status_code = user_action.login(user_model.User(user_name=user_name, user_password=user_password))
    if status_code != 200:
        return jsonify({
            'message': result
        }), status_code
    #luu thong tin user vao token
    access_token = create_access_token(identity=result.serialize())
    return jsonify({
        'token': access_token
    })