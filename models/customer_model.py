class Customer:
    def __init__(self, customer_id=0,customer_name='', contact_name='',address='', city='', postal_code='', country=''):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.contact_name = contact_name
        self.address = address
        self.city = city
        self.postal_code = postal_code
        self.country = country
    

    def serialize(self):
        return {
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'contact_name': self.contact_name,
            'address': self.address,
            'city': self.city,
            'postal_code': self.postal_code,
            'country': self.country
        }