DROP DATABASE IF EXISTS LMS;
CREATE DATABASE LMS; -- Library Managemente System

USE LMS;

-- TASK 1: Create Tables

CREATE TABLE PUBLISHER ( 
	publisher_name VARCHAR(100) PRIMARY KEY, 
	phone VARCHAR(20),
	address VARCHAR(255) 
);

CREATE TABLE LIBRARY_BRANCH ( 
	branch_id INT PRIMARY KEY, 
	branch_name VARCHAR(100), 
	branch_address VARCHAR(255) 
);

CREATE TABLE BORROWER ( 
	card_no INT AUTO_INCREMENT PRIMARY KEY, 
	name VARCHAR(100), 
	address VARCHAR(255), 
	phone VARCHAR(20) 
);

CREATE TABLE BOOK ( 
	book_id INT PRIMARY KEY, 
	title VARCHAR(255), 
	book_publisher VARCHAR(100), 
	FOREIGN KEY (book_publisher) REFERENCES PUBLISHER(publisher_name) 
);

CREATE TABLE BOOK_AUTHORS ( 
	book_id INT, 
	author_name VARCHAR(100), 
	PRIMARY KEY (book_id, author_name), 
	FOREIGN KEY (book_id) REFERENCES BOOK(book_id) 
);

CREATE TABLE BOOK_COPIES ( 
	book_id INT, 
	branch_id INT, 
	no_of_copies INT, 
	PRIMARY KEY (book_id, branch_id), 
	FOREIGN KEY (book_id) REFERENCES BOOK(book_id), 
	FOREIGN KEY (branch_id) REFERENCES LIBRARY_BRANCH(branch_id) 
);

CREATE TABLE BOOK_LOANS ( 
	book_id INT, 
	branch_id INT, 
	card_no INT, 
	date_out DATE, 
	due_date DATE, 
	returned_date DATE, 
	PRIMARY KEY (book_id, branch_id, card_no, date_out), 
	FOREIGN KEY (book_id) REFERENCES BOOK(book_id), 
	FOREIGN KEY (branch_id) REFERENCES LIBRARY_BRANCH(branch_id), 
	FOREIGN KEY (card_no) REFERENCES BORROWER(card_no) 
);

-- TASK 2: Load Data

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Publisher.csv'  
INTO TABLE PUBLISHER 
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Library_Branch.csv'
INTO TABLE LIBRARY_BRANCH
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Borrower.csv'  
INTO TABLE BORROWER
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Book.csv'  
INTO TABLE BOOK
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Book_Loans.csv'  
INTO TABLE BOOK_LOANS
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Book_Copies.csv '  
INTO TABLE BOOK_COPIES
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Book_Authors.csv ' 
INTO TABLE BOOK_AUTHORS
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

SELECT * FROM PUBLISHER;
SELECT * FROM LIBRARY_BRANCH;
SELECT * FROM BORROWER;
SELECT * FROM BOOK;
SELECT * FROM BOOK_AUTHORS;
SELECT * FROM BOOK_COPIES;
SELECT * FROM BOOK_LOANS;

-- TASK 3: Count Records

SELECT 'BOOK' AS TableName, COUNT(*) AS Records FROM BOOK
UNION 
SELECT 'PUBLISHER', COUNT(*) FROM PUBLISHER  
UNION  
SELECT 'BORROWER', COUNT(*) FROM BORROWER  
UNION  
SELECT 'LIBRARY_BRANCH', COUNT(*) FROM LIBRARY_BRANCH  
UNION  
SELECT 'BOOK_LOANS', COUNT(*) FROM BOOK_LOANS  
UNION  
SELECT 'BOOK_COPIES', COUNT(*) FROM BOOK_COPIES  
UNION  
SELECT 'BOOK_AUTHORS', COUNT(*) FROM BOOK_AUTHORS;

-- TASK 4: Execute Queries

-- Q1: Insert Yourself as a New Borrower 
INSERT INTO BORROWER (name, address, phone) VALUES ('Alice Cooper', '999 Unity St, Plano, TX', '(999) 123-4567');
SELECT * FROM BORROWER;

-- Q2: Update Your Phone Number 
UPDATE BORROWER SET phone = '(837) 721-8965' WHERE name = 'Alice Cooper';
SELECT * FROM BORROWER;

-- Q3: Increase Number of Copies for East Branch 
UPDATE BOOK_COPIES SET no_of_copies = no_of_copies + 1 WHERE branch_id = (SELECT branch_id FROM LIBRARY_BRANCH WHERE branch_name = 'East Branch');
SELECT * FROM BOOK_COPIES;

-- Q4a: Insert New Book, Author, and Publisher 
INSERT INTO PUBLISHER (publisher_name, phone, address) VALUES ('Oxford Publishing', '(111) 222-3333', '123 Oxford St, UK'); 
INSERT INTO BOOK (book_id, title, book_publisher) VALUES (999, 'Harry Potter and the Sorcerer''s Stone', 'Oxford Publishing'); 
INSERT INTO BOOK_AUTHORS (book_id, author_name) VALUES (999, 'J.K. Rowling'); 

-- Q4b: Insert New Branches 
INSERT INTO LIBRARY_BRANCH (branch_id, branch_name, branch_address) VALUES (4, 'North Branch', '456 NW, Irving, TX 76100'); 
INSERT INTO LIBRARY_BRANCH (branch_id, branch_name, branch_address) VALUES (5, 'UTA Branch', '123 Cooper St, Arlington TX 76101');

-- Q5: Books Loaned Between March 5 and 23, 2022 
SELECT b.title, lb.branch_name, DATEDIFF(bl.returned_date, bl.date_out) AS days_borrowed 
FROM BOOK_LOANS bl 
JOIN BOOK b ON bl.book_id = b.book_id 
JOIN LIBRARY_BRANCH lb ON bl.branch_id = lb.branch_id 
WHERE bl.date_out BETWEEN '2022-03-05' AND '2022-03-23'; 

-- Q6: Borrowers With Books Not Returned 
SELECT br.name FROM BORROWER br 
JOIN BOOK_LOANS bl ON br.card_no = bl.card_no 
WHERE bl.returned_date IS NULL;

-- Q7: Borrowed Books Report by Return Status 
SELECT lb.branch_name, 
SUM(CASE WHEN bl.returned_date IS NOT NULL THEN 1 ELSE 0 END) AS returned, 
SUM(CASE WHEN bl.returned_date IS NULL AND bl.due_date >= CURDATE() THEN 1 ELSE 0 END) AS still_borrowed, 
SUM(CASE WHEN bl.returned_date IS NULL AND bl.due_date < CURDATE() THEN 1 ELSE 0 END) AS late 
FROM BOOK_LOANS bl 
JOIN LIBRARY_BRANCH lb ON bl.branch_id = lb.branch_id 
GROUP BY lb.branch_name; 

-- Q8: Books and Max Days Borrowed 
SELECT b.title, MAX(DATEDIFF(bl.returned_date, bl.date_out)) AS max_days 
FROM BOOK_LOANS bl 
JOIN BOOK b ON bl.book_id = b.book_id 
GROUP BY b.title; 

-- Q9: Report for Ethan Martinez 
SELECT b.title, ba.author_name, DATEDIFF(COALESCE(bl.returned_date, CURDATE()), bl.date_out) AS days_borrowed, 
CASE WHEN bl.returned_date IS NULL AND bl.due_date < CURDATE() THEN 'Late' ELSE 'On time' END AS status 
FROM BORROWER br 
JOIN BOOK_LOANS bl ON br.card_no = bl.card_no 
JOIN BOOK b ON bl.book_id = b.book_id 
JOIN BOOK_AUTHORS ba ON b.book_id = ba.book_id 
WHERE br.name = 'Ethan Martinez' 
ORDER BY bl.date_out; 

-- Q10: Borrowers from West Branch 
SELECT DISTINCT br.name, br.address 
FROM BORROWER br 
JOIN BOOK_LOANS bl ON br.card_no = bl.card_no 
JOIN LIBRARY_BRANCH lb ON bl.branch_id = lb.branch_id 
WHERE lb.branch_name = 'West Branch'; 
