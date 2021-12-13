from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Admin123@localhost/demo_db'

db = SQLAlchemy(app)

class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    def as_dict(self):return {i.name: getattr(self, i.name) for i in self.__table__.columns}
     
    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"

@app.route('/')
def index():
	return {"status": 200, "message": "The server is working"}

#Metodo GET

@app.route('/empleado/',methods=['GET'])
def get_all_empleado():
	data = []
	items = Empleado.query.all()
	for i in items:
		data.append({
			"id": i.id,
			"first_name": i.first_name,
			"last_name": i.last_name,
			"age": i.age
		})
	return {"status": 200, "data": data}

#Metodo GET buscando un id en especifico

@app.route('/empleado/<int:id>/', methods=['GET'])
def get_empleado_by_id(id):
	item = Empleado.query.get(id)
	if item:
		result = {
			"id": item.id,
			"first_name": item.first_name,
			"last_name": item.last_name,
			"age": item.age
		}
		return {"status": 200, "data": result}
	return {"status": 404, "data": {}}

##metodo POST

@app.route('/empleado/', methods=['POST'])
def create_empleado():
	data = request.json
	item = Empleado(
		first_name=data['first_name'],
		last_name=data['last_name'],
		age=data['age']
	)
	db.session.add(item)
	db.session.commit()
	db.session.refresh(item)
	return {"status": 201, "new_id": item.id}

#Metodo put

@app.route('/empleado/<int:id>/', methods=['PUT'])
def update_empleado(id):
	data = request.json
	item = Empleado.query.get(id)
	if item:
		if 'first_name' in data:
			item.first_name = data['first_name']
		if 'last_name' in data:
                        item.last_name = data['last_name']
		if 'age' in data:
                        item.age = data['age']
		db.session.commit()
		return {"status": 200, "message": "Updated successfully"}
	return {"status": 404, "message": "Not found Item"}

## Usando metodo DELETE

@app.route('/empleado/<int:id>/', methods=['DELETE'])
def delete_empleado(id):
	item = Empleado.query.get(id)
	if item:
		db.session.delete(item)
		db.session.commit()
		return {"status": 200, "message": "Item deleted"}
	return {"status": 404, "message": "Not found Item"}

if __name__ == '__name__':
        app.run()

