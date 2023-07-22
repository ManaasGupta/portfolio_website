from sqlalchemy import create_engine,text
from dotenv import load_dotenv
load_dotenv()
import os
def get_data(sql_string:str):
    lh_host=os.getenv("LOCAL_HOST")
    lh_password=os.getenv("LOCAL_USER")
    lh_database=os.getenv("LOCAL_DATABASE")
    lh_port=os.getenv("LOCAL_PORT")
    lh_user=os.getenv("LOCAL_USER")
    eng_string=f"mysql+mysqlconnector://{lh_user}:{lh_password}@{lh_host}:{lh_port}/{lh_database}"
    engine=create_engine(eng_string,echo=True)

    email=str(input("Enter Email: "))
    password=str(input("Enter Password: "))

    with engine.connect() as connection:
        login_deatils=connection.execute(text("SELECT * FROM admin"))
    login_deatails_dict=login_deatils.mappings().all()
    connection.close()
    if (login_deatails_dict[0]['email']==email) and (login_deatails_dict[0]['password']==password):
        print("Login Sucessfull")
        sql_string=str(sql_string)
        with engine.connect() as conn:
            result = conn.execute(text(sql_string))
            print(type(result))
            result_dict=result.mappings().all()
            keys = list(result_dict[0].keys())      
            # for row in result_dict:
            #     print(row)
            #     print("\n")
        return result,result_dict,keys
    else:
        print('Invalid Login Details.')
        
if __name__=="__main__":
    #Example SQL Query to fetch data from table 'users' where user id is 12
    sql_string=str(input("Enter SQL Query: "))
    res,dict_res,keys=get_data(sql_string)
    for row in res:
        print(row)
    for row in dict_res:
        print(row)
    print(keys)