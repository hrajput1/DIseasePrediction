from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
import diseaseprediction
import csv

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin123'
app.config['MYSQL_DB'] = 'logindetail'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app) 

with open('templates/Testing.csv', newline='') as f:
        reader = csv.reader(f)
        symptoms = next(reader)
        symptoms = symptoms[:len(symptoms)-1]

@app.route('/')
def main():
	return render_template('main.html')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/home_page')
def home_page():
	return render_template('home_page.html')

@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/video')
def video():
	return render_template('video.html')

@app.route('/cure')
def cure():
	return render_template('cure.html')

@app.route('/medicine')
def medicine():
	return render_template('medicine.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        print(email, password)
        curl.execute("SELECT * FROM signup WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if user and len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['email'] = user['email']
                session['password'] = user['password']
                return render_template("home_page.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def singup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        name = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO signup (username, email, mobile, password) VALUES (%s,%s,%s,%s)",(name,email,mobile,hash_password))
        mysql.connection.commit()
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        return redirect(url_for('home_page'))
    

@app.route('/default', methods=['GET'])
def dropdown():
        return render_template('includes/default.html', symptoms=symptoms)
    
@app.route('/disease_predict', methods=['POST'])
def disease_predict():
    selected_symptoms = []
    if(request.form['Symptom1']!="") and (request.form['Symptom1'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom1'])
    if(request.form['Symptom2']!="") and (request.form['Symptom2'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom2'])
    if(request.form['Symptom3']!="") and (request.form['Symptom3'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom3'])
    if(request.form['Symptom4']!="") and (request.form['Symptom4'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom4'])
    if(request.form['Symptom5']!="") and (request.form['Symptom5'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom5'])

    disease = diseaseprediction.dosomething(selected_symptoms)
    return render_template('disease_predict.html',disease=disease,symptoms=symptoms)


@app.route('/find_doctor', methods=['POST'])
def get_location():
    location = request.form['doctor']
    return render_template('find_doctor.html',location=location,symptoms=symptoms)

@app.route("/appoint", methods=["GET", "POST"])
def appoint():
    if request.method == 'GET':
        return render_template("appoint.html")
    else:
        fullname = request.form['fullname']   
        phone_number = request.form['phone_number']
        dob = request.form['dob']
        email = request.form['email']
        appdate = request.form['appdate']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO appoint (fullname, phone_number, dob, email, appdate) VALUES (%s,%s,%s,%s,%s)",(fullname,phone_number,dob,email,appdate))
        mysql.connection.commit()
        session['fullname'] = request.form['fullname']
        session['phone_number'] = request.form['phone_number']
        session['dob'] = request.form['dob']
        session['email'] = request.form['email']
        session['appdate'] = request.form['appdate']
        print('Your appointment accepted we will connect with you soon.')
        return redirect(url_for('home_page'))

  
if __name__ =="__main__":  
    app.secret_key = "^A%DJAJU^JJ123"
    app.run()