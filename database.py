from sqlalchemy import create_engine,text
from dotenv import load_dotenv
load_dotenv()
import os
import hashlib
def get_data():
    lh_host=os.getenv("LOCAL_HOST")
    lh_password=os.getenv("LOCAL_PASSWORD")
    lh_database=os.getenv("LOCAL_DATABASE")
    lh_port=os.getenv("LOCAL_PORT")
    lh_user=os.getenv("LOCAL_USER")
    eng_string=f"mysql+mysqlconnector://{lh_user}:{lh_password}@{lh_host}:{lh_port}/{lh_database}"
    engine=create_engine(eng_string,echo=True)
    with engine.connect() as conn:
        conn.execute(text(""" CREATE TABLE valid_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(200) NOT NULL,
	date_of_creation DATE,
    day INT,
    month INT,
    year INT, -- Missing comma here
    month_name CHAR(30) -- Missing comma was added here
);"""))
        conn.commit()
        conn.close()
        
if __name__=="__main__":
    #Example SQL Query to fetch data from table 'users' where user id is 12
    # sql_string=str(input("Enter SQL Query: "))
    get_data()