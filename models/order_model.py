from . import customer_model
from . import employee_model
from . import shipper_model

class Order:
    def __init__(self, order_id=0, customer: customer_model.Customer = None, employee: employee_model.Employee = None, order_date='', shipper: shipper_model.Shipper = None):
        self.order_id = order_id
        self.customer = customer
        self.employee = employee
        self.order_date = order_date
        self.shipper = shipper
    
    def serialize(self):
        return{
            'order_id' : self.order_id,
            'order_date': self.order_date,
            'customer': self.customer.serialize(),
            'employee': self.employee.serialize(),
            'shipper': self.shipper.serialize()
        }