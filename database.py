from sqlalchemy import create_engine,text
from dotenv import load_dotenv
load_dotenv()
import os
import hashlib
def get_data():
    lh_host=os.getenv("LOCAL_HOST")
    lh_password=os.getenv("LOCAL_USER")
    lh_database=os.getenv("LOCAL_DATABASE")
    lh_port=os.getenv("LOCAL_PORT")
    lh_user=os.getenv("LOCAL_USER")
    eng_string=f"mysql+mysqlconnector://{lh_user}:{lh_password}@{lh_host}:{lh_port}/{lh_database}"
    engine=create_engine(eng_string,echo=True)
    with engine.connect() as conn:
        conn.execute(text("use query;"))
        login_details=conn.execute(text("SELECT * FROM valid_users;"))
        login_details_dict=login_details.mappings().all()
        return login_details_dict
        
if __name__=="__main__":
    #Example SQL Query to fetch data from table 'users' where user id is 12
    # sql_string=str(input("Enter SQL Query: "))
    res=get_data()
    for row in res:
        print(row['email'])
        print(row['hashed_password'])
    email=str(input("Enter Email"))
    password=str(input("Enter Password"))
    for row in res:
        if (row["email"]==email) and (row['hashed_password']==hashlib.md5(password.encode()).hexdigest()):
            print("Login Sucessfull")
            break
    else:
        print("Invalid Credentials")