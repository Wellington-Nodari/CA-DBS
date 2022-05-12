from flask import Flask
from flask import request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change the HOST IP and Password to match your instance configurations
app.config['MYSQL_USER'] = 'web'
app.config['MYSQL_PASSWORD'] = 'webPass'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = 'localhost' #for now
mysql.init_app(app)

@app.route("/add") #Add Student
def add():
  name = request.args.get('name')
  email = request.args.get('email')
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email)
  cur.execute(s)
  mysql.connection.commit()
  return '{"Result":"Success"}'

@app.route("/update") #Delete Student
def update():
  name = request.args.get('name')
  email = request.args.get('email')
  id = int(request.args.get('id'))
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  s='''UPDATE students SET studentName='{}', email='{}' WHERE studentID='{}';'''.format(name,email,id)
  cur.execute(s)
  mysql.connection.commit()
#  s='''UPDATE students SET studentName=?, email=? WHERE studentID=?;'''
#  cur.execute(s, (name, email,id))
#  mysql.connection.commit()
  return '{"Result":"Success"}'

@app.route("/delete") #Delete Student
def delete():
  id = request.args.get('id')
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  s='''DELETE s.* FROM students s WHERE studentID='{}';'''.format(id)
  cur.execute(s)
  mysql.connection.commit()
  return '{"Result":"Success"}'

@app.route("/home") #Default - Show Data
def hello(): # Name of the method
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  cur.execute('''SELECT * FROM students''') # execute an SQL statment
  rv = cur.fetchall() #Retreive all rows returend by the SQL statment
  Results=[]
  for row in rv: #Format the Output Results and add to return string
    Result={}
    Result['Name']=row[0].replace('\n',' ')
    Result['Email']=row[1]
    Result['ID']=row[2]
    Results.append(Result)
  response={'Results':Results, 'count':len(Results)}
  ret=app.response_class(
    response=json.dumps(response),
    status=200,
    mimetype='application/json'
  )
  return ret #Return the data in a string format
if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080', ssl_context=('/home/well/cert.pem', '/home/well/privkey.pem')) #Run the flask app at port 8080
