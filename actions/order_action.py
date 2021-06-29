from sqlite3.dbapi2 import Row
from ..models import customer_model
from ..models import employee_model
from ..models import shipper_model
from ..models import order_model
import sqlite3
class Order_Action:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def get_all(self):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            select tbl_order.order_id, tbl_order.order_date, tbl_customer.customer_id, tbl_customer.customer_name,
            tbl_customer.contact_name,tbl_customer.address, tbl_customer.city, tbl_customer.postal_code, tbl_customer.country,
            tbl_employee.employee_id, tbl_employee.last_name,tbl_employee.first_name, tbl_employee.birth_date, tbl_employee.photo,
            tbl_employee.note, tbl_shipper.shipper_id, tbl_shipper.shipper_name, tbl_shipper.phone 
            from tbl_order 
            inner join tbl_customer on tbl_order.customer_id == tbl_customer.customer_id
            inner join tbl_employee on tbl_order.emloyee_id == tbl_employee.employee_id
            inner join tbl_shipper on tbl_order.shipper_id == tbl_shipper.shipper_id
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            customer = customer_model.Customer(
                customer_id=row[2],
                customer_name=row[3],
                contact_name=row[4],
                address=row[5],
                city=row[6],
                postal_code=row[7],
                country=row[8]
            )
            employee = employee_model.Employee(
                employee_id=row[9],
                last_name=row[10],
                first_name=row[11],
                birth_date=row[12],
                photo=row[13],
                note=row[14]
            )
            shipper = shipper_model.Shipper(
                shipper_id=row[15],
                shipper_name=row[16],
                phone=row[17]
            )
            order = order_model.Order(
                order_id=row[0],
                order_date=row[1],
                customer=customer,
                employee=employee,
                shipper=shipper
            )
            result.append(order.serialize())
        return result
    def get_by_id(self, id):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            select tbl_order.order_id, tbl_order.order_date, tbl_customer.customer_id, tbl_customer.customer_name,
            tbl_customer.contact_name,tbl_customer.address, tbl_customer.city, tbl_customer.postal_code, tbl_customer.country,
            tbl_employee.employee_id, tbl_employee.last_name,tbl_employee.first_name, tbl_employee.birth_date, tbl_employee.photo,
            tbl_employee.note, tbl_shipper.shipper_id, tbl_shipper.shipper_name, tbl_shipper.phone 
            from tbl_order 
            inner join tbl_customer on tbl_order.customer_id == tbl_customer.customer_id
            inner join tbl_employee on tbl_order.emloyee_id == tbl_employee.employee_id
            inner join tbl_shipper on tbl_order.shipper_id == tbl_shipper.shipper_id
            WHERE tbl_order.order_id = ?
        """
        cursor.execute(sql,(id, ))
        row = cursor.fetchone()
        if row == None:
            return 'order not found!', 404
        customer = customer_model.Customer(
                customer_id=row[2],
                customer_name=row[3],
                contact_name=row[4],
                address=row[5],
                city=row[6],
                postal_code=row[7],
                country=row[8]
            )
        employee = employee_model.Employee(
            employee_id=row[9],
            last_name=row[10],
            first_name=row[11],
            birth_date=row[12],
            photo=row[13],
            note=row[14]
        )
        shipper = shipper_model.Shipper(
            shipper_id=row[15],
            shipper_name=row[16],
            phone=row[17]
        )
        order = order_model.Order(
            order_id=row[0],
            order_date=row[1],
            customer=customer,
            employee=employee,
            shipper=shipper
        )
        return order, 200
    def add(self, order: order_model.Order):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            INSERT INTO tbl_order VALUES(null, ?, ?, ?, ?)
        """
        cursor.execute(sql, (order.customer.customer_id, order.employee.employee_id, order.order_date, order.shipper.shipper_id))
        conn.commit()
        return 'Inserted successfully!'
    def update_by_id(self, id, order):
        pass
    def delete(self, order):
        pass