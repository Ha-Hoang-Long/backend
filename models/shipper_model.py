class Shipper:
    def __init__(self,shipper_id=0,shipper_name='',phone=''):
        self.shipper_id = shipper_id
        self.shipper_name = shipper_name
        self.phone = phone
    
    def serialize(self):
        return{
            'shipper_id': self.shipper_id,
            'shipper_name': self.shipper_name,
            'phone': self.phone
        }