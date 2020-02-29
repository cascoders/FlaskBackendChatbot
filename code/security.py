from user import User #importing User class from user.py file we created
#OLD METHOD
''' 
users = [
    {
      'id':1,
      'username':'bob'
      'password': 'abcd'
    }
]
username_mapping = { 'bob':{
      'id':1,
      'username':'bob'
      'password': 'abcd'
    }
                     }

userid_mapping = { 1:{
      'id':1,
      'username':'bob'
      'password': 'abcd'
    }
                   }
'''
#NEW METHOD BELOW
users = [  User(1,'bob','abcd')  ] #users is a list of User objects
username_mapping = { u.username : u  for u in users }
userid_mapping = { u.id : u  for u in users }


def authenticate(username,password): #returns correct user data
    user =  username_mapping.get(username,None) #returns the value of passed key username #we don't get the benefit of using None if we use username_mapping[username]
    if user and user.password == password:
        return user


def identity(payload):#payload is the contents of the JWT token ,we extract the userid from that payload
    user_id = payload['identity']
    return userid_mapping.get(user_id,None)
