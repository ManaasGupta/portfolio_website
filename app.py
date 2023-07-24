from sqlalchemy import create_engine,text
from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask,render_template,request,url_for,redirect
from datetime import date
import calendar
import logging

import hashlib
app = Flask(__name__,template_folder='templates')


lh_host=os.getenv("LOCAL_HOST")
lh_password=os.getenv("LOCAL_PASSWORD")
lh_database=os.getenv("LOCAL_DATABASE")
lh_port=os.getenv("LOCAL_PORT")
lh_user=os.getenv("LOCAL_USER")

connection_string=f"mysql+mysqlconnector://{lh_user}:{lh_password}@{lh_host}:{lh_port}/{lh_database}"
lh_engine=create_engine(connection_string,echo=True)

def get_database_page():
    return render_template("database.html")

@app.route('/',methods=['GET','POST'])
def entry_point():
    if request.method=='POST':
        fname=str(request.form['name'])
        email=str(request.form['email'])
        subject=str(request.form['subject'])
        message=str(request.form['message'])
        date_of_query=date.today()
        day=date_of_query.day
        month=date_of_query.month
        year=date_of_query.year
        month_name=calendar.month_abbr[month]
        month_name=month_name.upper()
        with lh_engine.connect() as conn:
            conn.execute(text("use query"))
            conn.execute(text("INSERT INTO user(fname, email, subject, msg, date_of_query, day, month, year, month_name) VALUES (:fname, :email, :subject, :msg, :date_of_query, :day, :month, :year, :month_name);"), {"fname":fname, "email": email, "subject": subject, "msg": message,'date_of_query':date_of_query,'day':day,'month':month,'year':year,'month_name':month_name})
            conn.commit()
            conn.close()
        
    return render_template("index.html")

@app.route('/admin',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=str(request.form['email'])
        password=str(request.form['password'])
        with lh_engine.connect() as conn:
                conn.execute(text("use query"))
                adminstring=os.getenv("ADMIN_STRING")
                login_deatils=conn.execute(text(adminstring))
                login_deatails_dict=login_deatils.mappings().all()
                conn.close()
                if (login_deatails_dict[0]['email']==email) and (login_deatails_dict[0]['password']==password):
                    return redirect(url_for('get_database'))
                else:
                    login_msg="Invalid Email or Password"
                    return render_template("login.html",login_msg=login_msg)
    return render_template("login.html")

@app.route("/admin/database",methods=['GET','POST'])
def get_database():
    if request.method=='POST':
        sql_query = request.form.get('query')
        if sql_query:
            lh_host=os.getenv("LOCAL_HOST")
            lh_password=os.getenv("LOCAL_PASSWORD")
            lh_database=os.getenv("LOCAL_DATABASE")
            lh_port=os.getenv("LOCAL_PORT")
            lh_user=os.getenv("LOCAL_USER")
            eng_string=f"mysql+mysqlconnector://{lh_user}:{lh_password}@{lh_host}:{lh_port}/{lh_database}"
            engine=create_engine(eng_string,echo=True)
            try:
                with engine.connect() as conn:
                    result = conn.execute(text(sql_query))
                    result_dict=result.mappings().all()
                    keys = list(result_dict[0].keys())
                    conn.close()
                    return render_template("database.html",data=result_dict,keys=keys)
            except Exception as e:
                error=e
                return render_template("database.html",data=error)
    return render_template("database.html")
            
@app.route("/login",methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        lh_host = os.getenv("LOCAL_HOST")
        lh_password = os.getenv("LOCAL_PASSWORD")
        lh_database = os.getenv("LOCAL_DATABASE")
        lh_port = os.getenv("LOCAL_PORT")
        lh_user = os.getenv("LOCAL_USER")
        connection_string = f"mysql+mysqlconnector://{lh_user}:{lh_password}@{lh_host}:{lh_port}/{lh_database}"
        email = str(request.form.get('user_email'))
        user_password = str(request.form.get('user_password'))
        lh_engine = create_engine(connection_string, echo=True)
        with lh_engine.connect() as conn:
            conn.execute(text("use query;"))
            login_details = conn.execute(text("SELECT * FROM valid_users;"))
            login_details_dict = login_details.mappings().all()

            login_successful = False  # Boolean flag to track login success

            for row in login_details_dict:
                try:
                    if (row["email"] == email) and (row['hashed_password'] == hashlib.md5(user_password.encode()).hexdigest()):
                        login_successful = True
                        print("Login Successful")
                        return render_template("index.html")
                except Exception as e:
                    logging.error(f"Error occurred during database insertion: {e}")
                    msg = "An error occurred while processing your sign-in request. Please try again later."
                    return render_template("register.html", msg=msg)

            if not login_successful:
                msg = "Credentials does not match our records"
                return render_template("user_login.html", msg=msg)
    return render_template("user_login.html")

@app.route("/register",methods=['GET','POST'])
def user_register():
    if request.method=='POST':
        lh_host=os.getenv("LOCAL_HOST")
        lh_password=os.getenv("LOCAL_PASSWORD")
        lh_database=os.getenv("LOCAL_DATABASE")
        lh_port=os.getenv("LOCAL_PORT")
        lh_user=os.getenv("LOCAL_USER")
        connection_string=f"mysql+mysqlconnector://{lh_user}:{lh_password}@{lh_host}:{lh_port}/{lh_database}"
        lh_engine=create_engine(connection_string,echo=True)
        first_name=str(request.form['first'])
        last_name=str(request.form['last'])
        email = str(request.form.get('user_email'))
        user_password = str(request.form.get('user_password'))
        confirm_password = str(request.form.get('confirm_password'))
        date_of_creation=date.today()
        day=date_of_creation.day
        month=date_of_creation.month
        year=date_of_creation.year
        month_name=calendar.month_abbr[month]
        month_name=month_name.upper()
        print("Email:", email)
        print("User Password:", user_password)
        print("Confirm Password:", confirm_password)
        if user_password == confirm_password:
            hashed_password = hashlib.md5(user_password.encode()).hexdigest()
            try:
                with lh_engine.connect() as conn:
                    conn.execute(text("use query;"))
                    conn.execute(text("INSERT INTO valid_users(first_name, last_name, email, hashed_password, date_of_creation, day, month, year, month_name) VALUES (:first_name, :last_name, :email, :hashed_password, :date_of_creation, :day, :month, :year, :month_name);"), {"first_name": first_name, "last_name": last_name, "email": email, "hashed_password": hashed_password, 'date_of_creation': date_of_creation, 'day': day, 'month': month, 'year': year, 'month_name': month_name})
                    conn.commit()
                return render_template("register.html")
            except Exception as e:
                logging.error(f"Error occurred during database insertion: {e}")
                msg = "An error occurred while processing your registration. Please try again later."
                return render_template("register.html", msg=msg)
        else:
            msg = "Passwords do not match"
            return render_template("register.html", msg=msg)

    return render_template("register.html")
if __name__ == '__main__':
    app.run(debug=True)