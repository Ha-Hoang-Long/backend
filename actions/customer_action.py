#connect to DB
#query and return result

from sqlite3.dbapi2 import Cursor
from ..models import customer_model
import sqlite3
class Customer_Action:
    def __init__(self, db_connection) -> None:
        self.db_connection = db_connection

    def get_all(self):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = 'SELECT * FROM tbl_customer'
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            customer = customer_model.Customer(
                customer_id=row[0],
                customer_name=row[1],
                contact_name=row[2],
                address=row[3],
                city=row[4],
                postal_code=row[5],
                country=row[6]
            )
            result.append(customer.serialize())
        return result

    def get_by_id(self, id):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            SELECT * FROM tbl_customer where customer_id = ?
        """
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row == None:
            return 'customer not found', 404
        customer = customer_model.Customer(
            customer_id=row[0],
            customer_name=row[1],
            contact_name=row[2],
            address=row[3],
            city=row[4],
            postal_code=row[5],
            country=row[6]
        )
        return customer, 200
    
    def add(self, customer: customer_model.Customer):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            INSERT INTO tbl_customer VALUES(null, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (customer.customer_name,customer.contact_name,customer.address,customer.city,customer.postal_code,customer.country))
        conn.commit()
        return 'Inserted successfully!'
    def delete(self, customer: customer_model.Customer):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            DELETE FROM tbl_customer WHERE customer_id = ?
        """
        cursor.execute(sql, (customer.customer_id, ))
        conn.commit()
        count = cursor.rowcount
        if count == 0:
            return 'customer not found', 404
        return 'delete successfully', 200
    def update_by_id(self, id, customer: customer_model.Customer):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            UPDATE tbl_customer SET customer_name = ?, contact_name = ?, address = ?, city = ?, postal_code = ?, country = ?
            WHERE customer_id = ?
        """
        cursor.execute(sql, (customer.customer_name, customer.contact_name, customer.address, customer.city, customer.postal_code, customer.country, id))
        conn.commit()
        row = cursor.rowcount
        if row == 0:
            return 'customer not found', 404
        return 'update successfully', 200