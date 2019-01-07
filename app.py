from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

app=Flask(__name__)
bcrypt=Bcrypt(app)
CORS(app)


#Hashing Testing
password='Akash123'
print('type of password',type(password))
gen_pass=bcrypt.generate_password_hash(password).decode('utf-8')
print('generated password hash',gen_pass)
print('type of hash',type(gen_pass))
candidate='secret'
check_pass=bcrypt.check_password_hash(gen_pass,password)
print('checking password',check_pass) 


client=MongoClient('127.0.0.1:27017')
db=client.Machinedata

@app.route('/machineDetails',methods=['GET'])
def home():
        machines=db.Machines.find()
        sendData=[]
        sendItem={}
        for machine in machines:            
            for dat in machine:
                if(dat!='_id'):                    
                    sendItem[dat]=machine[dat]            
            sendData.append(sendItem)
            sendItem={}       
        return jsonify(sendData)

@app.route('/addMachine',methods=['POST'])
def addMachine():
    try:
        print(request.json)
        json_data=request.json['info']
        print(json_data)
        deviceName = json_data['device']
        ipAddress = json_data['ip']
        userName = json_data['username']
        password = json_data['password']
        portNumber = json_data['port']

        password_hash=bcrypt.generate_password_hash(password).decode('utf-8')
        
        try:
            db.Machines.insert_one({
            'device':deviceName,
            'ipAddress':ipAddress,
            'username':userName,
            'password':password_hash,
            'port':portNumber
            })
            return jsonify(status='OK',message='inserted successfully')

        except Exception as e:
            print('Database Error',e)
            return jsonify(status='ERROR',message=str(e))     
        
    except Exception as e:
        print('Server error',e)
        return jsonify(status='ERROR',message=str(e))

@app.route('/deleteMachine',methods=['POST'])
def delete():   
    try:
        print(request.json)
        db.Machines.remove({'device':request.json['data']})
        return jsonify(status='OK',message='Delete successful')
    
    except Exception as e:
        print('Deletion error',e)
        return jsonify(status='ERROR',message=str(e))

# API for updation
@app.route('/updateMachine',methods=['PUT'])
def update():
    try:
        print('request.json',request.json)        
        db.Machines.update({'device':request.json['device']},{'$set':request.json['edit']})
        return jsonify(status='OK',message='Update successful')
    except Exception as e:
        print('Updation Error',e)
        return jsonify(status='ERROR',message=str(e))
    
   

if __name__=='__main__':
    app.run(debug=True,port=8080)


