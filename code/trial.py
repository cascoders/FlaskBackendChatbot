#run this from virtual environment venv
from flask import Flask
from flask_restful import Resource, Api
#If our api returns and creates student ,then our Resource is student....
app = Flask(__name__)
api = Api(app)  #Api will allow us to very easily add resources to app

#every resource has to be a class in order to use Api for it
class Student(Resource):#inheriting class Resource into Student
    #@app.route('/student/<string:name>') not needed 
    def get(self,name):   #adding/changing stuff
        return {'student': name}



api.add_resource(Student,'/student/<string:name>')
#http://127.0.0.1:5000/student/Rolf
#this name(e.g Rolf) will straight go into parameter name in get(self,name)

app.run(port=5000)

