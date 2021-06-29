class Employee:
    def __init__(self, employee_id=0, last_name='', first_name='', birth_date='', photo='', note=''):
        self.employee_id = employee_id
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.photo = photo
        self.note = note
    def serialize(self):
        return{
            'employee_id': self.employee_id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date,
            'photo': self.photo if self.photo == None else f'/image/{self.photo}',
            'note': self.note
        }