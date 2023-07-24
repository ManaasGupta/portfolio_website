use query;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS admin;
DROP TABLE IF exists valid_users;
CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT,
    fname VARCHAR(30),
    email VARCHAR(100),
    subject VARCHAR(200),
    msg VARCHAR(1000),
    date_of_query DATE,
    day INT,
    month INT,
    year INT, -- Missing comma here
    month_name CHAR(30), -- Missing comma was added here
    PRIMARY KEY(id)
);

CREATE TABLE admin (
    email VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL
);
insert into admin(email,password) values('manasgpt3@gmail.com','PalmS@0810');
INSERT INTO user(fname, email, subject, msg, date_of_query, day, month, year, month_name) VALUES ('Manas Gupta', 'manasgpt3@gmail.com', 'New Test', 'New test for localhost', '2023-07-18', 18, 7, 2023, 'JUL');


CREATE TABLE valid_users (
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
);

INSERT INTO valid_users(first_name,last_name,email,hashed_password,date_of_creation,day,month,year,month_name)VALUES ('Manas',' Gupta', 'manasgpt3@gmail.com', 'wefuewf;;sadqjwoidjwoidoqwiod', '2023-07-18', 18, 7, 2023, 'JUL');

show tables;

select * from user;
select * from admin;
describe admin;
describe user;
describe valid_users;

select * from valid_users;