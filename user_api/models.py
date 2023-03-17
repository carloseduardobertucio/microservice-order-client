from config import app, db



class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    cpf = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(255), unique=True)
    phone_number = db.Column(db.String(11))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
	        "name": self.name,
	        "cpf": self.cpf,
	        "email": self.email,
	        "phone_number": self.phone_number
        }
    
with app.app_context():
    db.create_all()