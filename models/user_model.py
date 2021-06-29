class User:
    def __init__(self, user_id=0, user_name='', user_password='', role='') -> None:
        self.user_id=user_id
        self.user_name=user_name
        self.user_password=user_password
        self.role=role
    
    def serialize(self):
        return{
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_password': self.user_password,
            'role': self.role
        }