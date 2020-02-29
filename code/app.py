#lecture 51 - 55
#run this from virtual environment venv bcoz flask restful is installed in it

from flask import Flask,request
from flask_restful import Resource, Api,reqparse
#If our api returns and creates student ,then our Resource is student....
#using reqparse to parse the JSON data we(server) get from client
from security import authenticate,identity #importing from our security.py
from flask_jwt import JWT, jwt_required
#flask_JWT -> json web token -> used for encoding data
app = Flask(__name__)

app.secret_key = 'tripathi31'
api = Api(app)  #Api will allow us to very easily add resources to app

jwt = JWT(app,authenticate,identity)
""" How JWT works....
JWT creates a new endpoint '/auth'.
When we call '/auth' , we send it a username and a password.
JWT takes it and sends it to autheticate function.
The function then returns user -> the /auth endpoint returns a JWtoken
That jwtoken , we can send it to the next request we make
Then JWT takes that token and calls identity function and then gets the correct user from that token(payload)
If it find's the user from the token sent from browser, it means the user was autheticated previously
"""

items = []     #as always.. list of dictionaries

#every resource has to be a class in order to use Api for it
class Item(Resource):#inheriting class Resource into Item
    @jwt_required() #now we have to authenticate(\auth) before we call the get method i.e we cant get the item details before authorization
    def get(self,name):   #returns details of particular item
        item = next(filter(lambda x:x['name']==name,items),None)
        #next function gives the first matching item, if the list is empty returns None , hence we explicitely need to write next(filter(),None) to escape from error 
        return {'item': item},200 if item else 404 
        #return {'Item' : None },404 #### remember if u don't write this stmt then func returns None which is not a valid JSON and may cause error .... 
        #mentioned explicitelt 404 bcoz it would be 200 otherwise....

    def post(self, name):#this function also gets some JSON data(payload)
            if next(filter(lambda x:x['name']==name,items),None) is not None:  #preventing duplication
                return {'message':'An item with name {} already exists'.format(name)},400 #400 means bad request
            data = request.get_json() #if the payload does not have proper JSON or Content-type,this line gives error
            item = {'name': name,'price':data['price']}
            items.append(item)
            return item,201
        #status code 201 is for created the object, if not mentioned will be 200(default) if everything's ok
    def delete(self,name):
        global items
        items = list(filter(lambda x:x['name']!=name,items))
        return {'message':'Item deleted'}
    def put(self,name):
        parser = reqparse.RequestParser()#also looks in form payloads
        parser.add_argument('price',  #filtering out price from JSON payload we get from server
                            type = float,
                            required = True, #no request can come thru with no 'price'
                            help = "This feild can't be left blank!"
                            ) 
        data = parser.parse_args()#parses the arguments in payload #data = request.get_json()

        item = next(filter(lambda x:x['name'] == name,items),None)
        if item is None:
            item = { 'name' : name , 'price' : data['price'] }
            items.append(item)
        else :
            item.update(data)#item['price'] = data['price'] , part of item similar to data will update
        return item
class Itemlist(Resource):
    def get(self):
        return {'items':items} #returns item list
    
api.add_resource(Item,'/item/<string:name>')
api.add_resource(Itemlist,'/items') 

app.run(port=5000,debug = True)

