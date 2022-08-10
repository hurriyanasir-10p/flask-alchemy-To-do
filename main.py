from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
import pytest
from datetime import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://username:password@localhost/todo"
db = SQLAlchemy(app)


class User_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    lists = db.relationship('List_model', cascade="all,delete",backref='user_model')

    def __repr__(self):
        return f"User name={self.name}, id= {self.id}"


class List_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_edit = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))

    tasks = db.relationship('Task_model', cascade="all,delete",backref='list_model')

    def __repr__(self):
        return f"List name={self.name}, last_edit= {self.last_edit}, start_date={self.start_date}"


class Task_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String, default='Normal')
    list_id = db.Column(db.Integer, db.ForeignKey("list_model.id"))

    def __repr__(self):
        return f"Task desc={self.description}, priority= {self.priority}"


########## classes start here ######################

db.create_all()

######### users
user_fields = {
    'id':fields.Integer,
    'name': fields.String,

}
user_parser = reqparse.RequestParser()
user_parser.add_argument('name')


class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        print("in get")
        result = User_model.query.filter_by(id=id).first()
        return result

    @marshal_with(user_fields)
    def put(self, id):
        result = User_model.query.filter_by(id=id).first()
        args = user_parser.parse_args()
        if args['name'] is not None:
            result.name = args['name']
        db.session.commit()
        return result

    @marshal_with(user_fields)
    def post(self):
        print("in post")
        args = user_parser.parse_args()
        user = User_model(name=args['name'])
        db.session.add(user)
        db.session.commit()

        return user

    @marshal_with(user_fields)
    def delete(self, id):
        user = User_model.query.filter_by(id=id).first()
        if user == None:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        return user


###### lists
list_fields = {
    'id':fields.Integer,
    'name': fields.String,
    'last_edit': fields.DateTime,
    'start_date': fields.DateTime,
    'user_id': fields.Integer
}
list_parser = reqparse.RequestParser()
list_parser.add_argument('name')
list_parser.add_argument('last_edit')
list_parser.add_argument('start_date')
list_parser.add_argument('user_id')


class List(Resource):
    @marshal_with(list_fields)
    def get(self, id):
        print("in get")
        result = List_model.query.filter_by(id=id).first()
        return result

    @marshal_with(list_fields)
    def put(self, id):
        result = List_model.query.filter_by(id=id).first()
        args = list_parser.parse_args()
        if args['name'] is not None:
            result.name = args['name']

        if args['user_id'] is not None:
            result.user_id = args['user_id']
        result.last_edit = datetime.utcnow()
        db.session.commit()
        return result
    @marshal_with(list_fields)
    def post(self):
        print("in post")

        args = list_parser.parse_args()
        list = List_model(name=args['name'], last_edit=datetime.utcnow(), user_id=args['user_id'])
        db.session.add(list)
        db.session.commit()
        return list

    @marshal_with(list_fields)
    def delete(self, id):
        list1 = List_model.query.filter_by(id=id).first()
        print("in delete ",list1)
        if list1 is not None:
            db.session.delete(list1)
            db.session.commit()

        # cascading delete
        return list1


############# Tasks
task_fields = {
    'id':fields.Integer,
    'description': fields.String,
    'priority': fields.String,
    'list_id': fields.Integer,
}
task_parser = reqparse.RequestParser()
task_parser.add_argument('description')
task_parser.add_argument('priority')
task_parser.add_argument('list_id')


class Task(Resource):
    @marshal_with(task_fields)
    def get(self, id):
        print("in get")
        result = Task_model.query.filter_by(id=id).first()
        return result

    @marshal_with(task_fields)
    def put(self, id):
        result = Task_model.query.filter_by(id=id).first()
        args = task_parser.parse_args()
        if args['description'] is not None:
            print("desc", args['description'], result.description)
            result.description = args['description']
            db.session.commit()
        if args['priority'] is not None:
            print("prior", args['priority'])
            result.priority = args['priority']
            db.session.commit()
        if args['list_id'] is not None:
            result.list_id = args['list_id']
            db.session.commit()
        list=List_model.query.filter_by(id=result.list_id ).first()
        return result
    @marshal_with(task_fields)
    def post(self):

        print("in post")
        args = task_parser.parse_args()
        task = Task_model(description=args['description'], priority=args['priority'], list_id=args['list_id'])
        db.session.add(task)
        db.session.commit()


        return task

    @marshal_with(task_fields)
    def delete(self, id):

        task = Task_model.query.filter_by(id=id).first()
        if task is not None:
            db.session.delete(task)
            db.session.commit()
        return task


# ######### JOINS

@app.route('/<id>') # here the id is of the user
@marshal_with(list_fields)
def getList(id):
    result = db.session.query(User_model.name,List_model).join(List_model). \
        filter(User_model.id== id)
    myLists=[]
    for u,l1 in result:
        print(l1)
        myLists.append(l1)

    return myLists

@app.route('/tasks/<id>') # here the id is of the list
@marshal_with(task_fields)
def getTasks(id):  # put application's code here
    result = db.session.query(List_model,Task_model).join(Task_model). \
        filter(List_model.id== id)
    # print(result.filter(List_model))
    # .query.filter_by(User_model.id=id)
    myTasks=[]
    for u,l1 in result:
        print(l1)
        myTasks.append(l1)

    return myTasks

#  Resources
api.add_resource(User, "/user/<int:id>", '/user')
api.add_resource(List, "/list/<int:id>","/list")
api.add_resource(Task, "/task/<int:id>","/task")
if __name__ == '__main__':
    app.run(debug=True)
