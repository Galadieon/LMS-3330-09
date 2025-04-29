SOURCE demo-phase2.sql;

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