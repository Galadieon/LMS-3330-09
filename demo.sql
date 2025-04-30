DROP DATABASE IF EXISTS LMS;
CREATE DATABASE LMS; -- Library Managemente System

USE LMS;

-- TASK 1: Create Tables

CREATE TABLE Publisher ( 
	publisher_name VARCHAR(100) PRIMARY KEY, 
	phone VARCHAR(20),
	address VARCHAR(255) 
);

CREATE TABLE Library_Branch ( 
	branch_id INT PRIMARY KEY, 
	branch_name VARCHAR(100), 
	branch_address VARCHAR(255) 
);

CREATE TABLE Borrower ( 
	card_no INT AUTO_INCREMENT PRIMARY KEY, 
	name VARCHAR(100), 
	address VARCHAR(255), 
	phone VARCHAR(20) 
);

CREATE TABLE Book ( 
	book_id INT PRIMARY KEY AUTO_INCREMENT, 
	title VARCHAR(255), 
	book_publisher VARCHAR(100), 
	FOREIGN KEY (book_publisher) REFERENCES Publisher(publisher_name) 
);

CREATE TABLE Book_Authors ( 
	book_id INT, 
	author_name VARCHAR(100), 
	PRIMARY KEY (book_id, author_name), 
	FOREIGN KEY (book_id) REFERENCES Book(book_id) 
);

CREATE TABLE Book_Copies ( 
	book_id INT, 
	branch_id INT, 
	no_of_copies INT, 
	PRIMARY KEY (book_id, branch_id), 
	FOREIGN KEY (book_id) REFERENCES Book(book_id), 
	FOREIGN KEY (branch_id) REFERENCES Library_Branch(branch_id) 
);

CREATE TABLE Book_Loans ( 
	book_id INT, 
	branch_id INT, 
	card_no INT, 
	date_out DATE, 
	due_date DATE, 
	returned_date DATE, 
	PRIMARY KEY (book_id, branch_id, card_no, date_out), 
	FOREIGN KEY (book_id) REFERENCES Book(book_id), 
	FOREIGN KEY (branch_id) REFERENCES Library_Branch(branch_id), 
	FOREIGN KEY (card_no) REFERENCES Borrower(card_no) 
);

-- TASK 2: Load Data

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Publisher.csv'  
INTO TABLE Publisher 
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Library_Branch.csv'
INTO TABLE Library_Branch
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Borrower.csv'  
INTO TABLE Borrower
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Book.csv'  
INTO TABLE Book
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Book_Loans.csv'  
INTO TABLE Book_Loans
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Book_Copies.csv '  
INTO TABLE Book_Copies
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/LMS/Book_Authors.csv ' 
INTO TABLE Book_Authors
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

SELECT * FROM Publisher;
SELECT * FROM Library_Branch;
SELECT * FROM Borrower;
SELECT * FROM Book;
SELECT * FROM Book_Authors;
SELECT * FROM Book_Copies;
SELECT * FROM Book_Loans;

-- TASK 3: Count Records

SELECT 'Book' AS TableName, COUNT(*) AS Records FROM Book
UNION 
SELECT 'Publisher', COUNT(*) FROM Publisher  
UNION  
SELECT 'Borrower', COUNT(*) FROM Borrower  
UNION  
SELECT 'Library_Branch', COUNT(*) FROM Library_Branch  
UNION  
SELECT 'Book_Loans', COUNT(*) FROM Book_Loans  
UNION  
SELECT 'Book_Copies', COUNT(*) FROM Book_Copies  
UNION  
SELECT 'Book_Authors', COUNT(*) FROM Book_Authors;

-- TASK 4: Execute Queries

-- Q1: Insert Yourself as a New Borrower 
INSERT INTO Borrower (name, address, phone) VALUES ('Alice Cooper', '999 Unity St, Plano, TX', '(999) 123-4567');
SELECT * FROM Borrower;

-- Q2: Update Your Phone Number 
UPDATE Borrower SET phone = '(837) 721-8965' WHERE name = 'Alice Cooper';
SELECT * FROM Borrower;

-- Q3: Increase Number of Copies for East Branch 
UPDATE Book_Copies SET no_of_copies = no_of_copies + 1 WHERE branch_id = (SELECT branch_id FROM Library_Branch WHERE branch_name = 'East Branch');
SELECT * FROM Book_Copies;

-- Q4a: Insert New Book, Author, and Publisher 
INSERT INTO Publisher (publisher_name, phone, address) VALUES ('Oxford Publishing', '(111) 222-3333', '123 Oxford St, UK'); 
INSERT INTO Book (book_id, title, book_publisher) VALUES (999, 'Harry Potter and the Sorcerer''s Stone', 'Oxford Publishing'); 
INSERT INTO Book_Authors (book_id, author_name) VALUES (999, 'J.K. Rowling'); 

-- Q4b: Insert New Branches 
INSERT INTO Library_Branch (branch_id, branch_name, branch_address) VALUES (4, 'North Branch', '456 NW, Irving, TX 76100'); 
INSERT INTO Library_Branch (branch_id, branch_name, branch_address) VALUES (5, 'UTA Branch', '123 Cooper St, Arlington TX 76101');

-- Q5: Books Loaned Between March 5 and 23, 2022 
SELECT b.title, lb.branch_name, DATEDIFF(bl.returned_date, bl.date_out) AS days_borrowed 
FROM Book_Loans bl 
JOIN Book b ON bl.book_id = b.book_id 
JOIN Library_Branch lb ON bl.branch_id = lb.branch_id 
WHERE bl.date_out BETWEEN '2022-03-05' AND '2022-03-23'; 

-- Q6: Borrowers With Books Not Returned 
SELECT br.name FROM Borrower br 
JOIN Book_Loans bl ON br.card_no = bl.card_no 
WHERE bl.returned_date IS NULL;

-- Q7: Borrowed Books Report by Return Status 
SELECT lb.branch_name, 
SUM(CASE WHEN bl.returned_date IS NOT NULL THEN 1 ELSE 0 END) AS returned, 
SUM(CASE WHEN bl.returned_date IS NULL AND bl.due_date >= CURDATE() THEN 1 ELSE 0 END) AS still_borrowed, 
SUM(CASE WHEN bl.returned_date IS NULL AND bl.due_date < CURDATE() THEN 1 ELSE 0 END) AS late 
FROM Book_Loans bl 
JOIN Library_Branch lb ON bl.branch_id = lb.branch_id 
GROUP BY lb.branch_name; 

-- Q8: Books and Max Days Borrowed 
SELECT b.title, MAX(DATEDIFF(bl.returned_date, bl.date_out)) AS max_days 
FROM Book_Loans bl 
JOIN Book b ON bl.book_id = b.book_id 
GROUP BY b.title; 

-- Q9: Report for Ethan Martinez 
SELECT b.title, ba.author_name, DATEDIFF(COALESCE(bl.returned_date, CURDATE()), bl.date_out) AS days_borrowed, 
CASE WHEN bl.returned_date IS NULL AND bl.due_date < CURDATE() THEN 'Late' ELSE 'On time' END AS status 
FROM Borrower br 
JOIN Book_Loans bl ON br.card_no = bl.card_no 
JOIN Book b ON bl.book_id = b.book_id 
JOIN Book_Authors ba ON b.book_id = ba.book_id 
WHERE br.name = 'Ethan Martinez' 
ORDER BY bl.date_out; 

-- Q10: Borrowers from West Branch 
SELECT DISTINCT br.name, br.address 
FROM Borrower br 
JOIN Book_Loans bl ON br.card_no = bl.card_no 
JOIN Library_Branch lb ON bl.branch_id = lb.branch_id 
WHERE lb.branch_name = 'West Branch'; 









-- PHASE 3:

SELECT '' AS Message;
SELECT '' AS Message;
SELECT 'Database loaded!' AS Message;
SELECT '' AS Message;
SELECT '' AS Message;

-- TASK 1: Execute Queries

-- Q1: Add an extra column ‘Late’ to the Book_Loan table. Values will be 0-for non-late retuns, and 1-for late
-- returns. Then update the ‘Late’ column with '1' for all records that they have a return date later than the
-- due date and with '0' for those were returned on time
ALTER TABLE Book_Loans 
ADD Late INT;

UPDATE Book_Loans 
SET Late = (CASE 
    WHEN (Book_Loans.Returned_date BETWEEN 
    Book_Loans.date_out AND Book_Loans.due_date) THEN 0 
    ELSE 1 
    END); 
SELECT * FROM Book_Loans;

-- Q2: Add an extra column ‘LateFee’ to the Library_Branch table, decide late fee per day for each branch and
-- update that column.
ALTER TABLE Library_Branch  
ADD LateFee DECIMAL(10, 2);  
UPDATE Library_Branch  
SET LateFee = (CASE  
    WHEN (Library_Branch.branch_id = 1) THEN 1.20  
    WHEN (Library_Branch.branch_id = 2) THEN 0.75  
    WHEN (Library_Branch.branch_id = 3) THEN 2.30  
    ELSE 0.50  
    END);  
SELECT * FROM Library_Branch;

-- Q3: Create a view vBookLoanInfo that retrieves all information per book loan.
-- CREATE VIEW vBookLoanInfo
CREATE VIEW vBookLoanInfo AS
SELECT BW.card_no AS Card_No,
        BW.name AS 'Borrower Name',
        B_L.date_out AS Date_Out,
        B_L.due_date AS Due_Date,
        B_L.Returned_date,
        DATEDIFF(B_L.Returned_date, B_L.date_out) AS TotalDays,
        Bk.title AS 'Book Title',
        CASE
            WHEN (B_L.Returned_date BETWEEN B_L.date_out AND B_L.due_date) THEN 0
            ELSE DATEDIFF(B_L.Returned_date, B_L.due_date)
        END AS 'Number of days returned late',
        L_B.branch_id AS 'Branch ID',
        CASE
            WHEN (B_L.Returned_date BETWEEN B_L.date_out AND B_L.due_date) THEN 0
            ELSE L_B.LateFee * DATEDIFF(B_L.Returned_date, B_L.due_date)
        END AS LateFeeBalance
FROM Borrower AS BW
JOIN Book_Loans AS B_L ON BW.card_no = B_L.card_no
JOIN Book AS Bk ON B_L.book_id = Bk.book_id
JOIN Library_Branch AS L_B ON B_L.branch_id = L_B.branch_id;
SELECT * FROM vBookLoanInfo;