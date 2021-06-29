#connect to DB
#query and return result

from sqlite3.dbapi2 import Cursor
from ..models import employee_model
import sqlite3
class Employee_Action:
    def __init__(self, db_connection) -> None:
        self.db_connection = db_connection

    def get_all(self):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = 'SELECT * FROM tbl_employee'
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            employee = employee_model.Employee(
                employee_id=row[0],
                last_name=row[1],
                first_name=row[2],
                birth_date=row[3],
                photo=row[4],
                note=row[5]
            )
            result.append(employee.serialize())
        return result

    def get_by_id(self, id):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            SELECT * FROM tbl_employee where employee_id = ?
        """
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row == None:
            return 'customer not found', 404
        employee = employee_model.Employee(
            employee_id=row[0],
            last_name=row[1],
            first_name=row[2],
            birth_date=row[3],
            photo=row[4],
            note=row[5]
        )
        return employee, 200
    
    def add(self, employee: employee_model.Employee):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            INSERT INTO tbl_employee VALUES(null, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (employee.employee_id, employee.last_name, employee.first_name, employee.photo, employee.note))
        conn.commit()
        return 'Inserted successfully!'
    def delete(self, employee: employee_model.Employee):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            DELETE FROM tbl_employee WHERE employee_id = ?
        """
        cursor.execute(sql, (employee.employee_id, ))
        conn.commit()
        count = cursor.rowcount
        if count == 0:
            return 'customer not found', 404
        return 'delete successfully', 200
    def update_by_id(self, id, customer: employee_model.Employee):
        # conn = sqlite3.connect(self.db_connection)
        # cursor = conn.cursor()
        # sql = """
        #     UPDATE tbl_customer SET customer_name = ?, contact_name = ?, address = ?, city = ?, postal_code = ?, country = ?
        #     WHERE customer_id = ?
        # """
        # cursor.execute(sql, (customer.customer_name, customer.contact_name, customer.address, customer.city, customer.postal_code, customer.country, id))
        # conn.commit()
        # row = cursor.rowcount
        # if row == 0:
        #     return 'customer not found', 404
        # return 'update successfully', 200
        pass