-- Active: 1712495201592@@127.0.0.1@3306@information_schema
DROP TABLE IF EXISTS Book, Reader, Borrow, Reserve;

CREATE DATABASE IF NOT EXISTS lab01;

USE lab01;
# 创建表
CREATE TABLE Book (
    bid CHAR(8) PRIMARY KEY, -- bid是主键
    bname VARCHAR(100) NOT NULL, #书名,不能为空
    author VARCHAR(50), -- 作者
    price FLOAT, #价格
    bstatus INT DEFAULT 0 CHECK (bstatus BETWEEN 0 AND 2), #0表示在架，1表示借出,2表示预约,默认值为0
    borrow_Times INT DEFAULT 0, #表示有史以来的总借阅次数，默认为0
    reserve_Times INT DEFAULT 0 #当前预约人数，默认值为0
);

CREATE TABLE Reader (
    rid CHAR(8) PRIMARY KEY, #读者号是主键
    rname VARCHAR(20), #读者姓名
    age INT, 
    address VARCHAR(100)
);

#主键为(book_ID,reader_ID,borrow_Date)
CREATE TABLE Borrow (
    book_ID CHAR(8), #图书号
    reader_ID CHAR(8), #读者号
    borrow_Date DATE, #借书日期
    return_Date DATE, #还书日期
    PRIMARY KEY (
        book_ID, reader_ID, borrow_Date
    ), #主键
    FOREIGN KEY (book_ID) REFERENCES Book (bid), #外键
    UNIQUE KEY (book_ID, return_Date), #一本书只能被一个人借出
    FOREIGN KEY (reader_ID) REFERENCES Reader (rid)
);

CREATE TABLE Reserve (
    book_ID CHAR(8), #图书号
    reader_ID CHAR(8), #读者号
    reserve_Date DATE DEFAULT(curdate()), #预约日期
    take_Date DATE, #取书日期
    PRIMARY KEY (
        book_ID, reader_ID, reserve_Date
    ), constraint chk_date CHECK (take_Date > reserve_Date)
);

-- 该测试样例是根据数据库规则设计好的
-- 不需要事先定义任何存储过程和触发器，定义好基本表后直接运行即可
-- 对测试样例有任何问题都可以联系yxy助教

-- 插入图书数据
INSERT INTO
    book (
        bid, bname, author, price, borrow_times, reserve_times, bstatus
    )
VALUES (
        'B001', 'The Hobbit', 'J.R.R. Tolkien', 18.99, 4, 1, 2
    ),
    (
        'B002', 'Harry Potter and the Chamber of Secrets', 'J.K. Rowling', 25.50, 3, 0, 1
    ),
    (
        'B003', 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 14.7, 2, 0, 1
    ),
    (
        'B004', 'To Kill a Mockingbird', 'Harper Lee', 12.99, 0, 0, 0
    ),
    (
        'B005', '1984', 'George Orwell', 10.50, 0, 1, 2
    ),
    (
        'B006', 'Learning MySQL: Get a Handle on Your Data', 'Seyed M.M. (Saied) Tahaghoghi, Hugh E. Williams', 29.99, 1, 0, 1
    ),
    (
        'B007', 'Pride and Prejudice', 'Jane Austen', 14.25, 1, 0, 1
    ),
    (
        'B008', 'The Catcher in the Rye', 'J.D. Salinger', 11.20, 0, 2, 2
    ),
    (
        'B009', 'Brave New World', 'Aldous Huxley', 13.80, 1, 0, 1
    ),
    (
        'B010', 'Animal Farm', 'George Orwell', 8.99, 1, 1, 1
    ),
    (
        'B011', 'MySQL Cookbook: Solutions for Database Developers and Administrators', 'Paul DuBois', 35.50, 1, 0, 0
    ),
    (
        'B012', 'Test your trigger here', 'TA', 10.4, 0, 0, 0
    );

-- 插入读者数据
INSERT INTO
    reader (rid, rname, age, address)
VALUES (
        'R001', 'John', 35, '456 Oak St, Othertown'
    ),
    (
        'R002', 'Rose', 35, '123 Main St, Anytown'
    ),
    (
        'R003', 'Emma', 30, '123 Elm St, Anytown'
    ),
    (
        'R004', 'Sophia', 28, '789 Maple St, Somewhere'
    ),
    (
        'R005', 'Emily', 28, '456 Elm St, Othertown'
    ),
    (
        'R006', 'Michael', 40, '789 Oak St, Somewhere'
    );

-- 插入借阅数据
INSERT INTO
    borrow (
        book_id, reader_id, borrow_date, return_date
    )
VALUES (
        'B001', 'R002', '2024-03-01', '2024-03-15'
    ),
    (
        'B003', 'R001', '2024-03-05', '2024-03-20'
    ),
    (
        'B002', 'R001', '2024-03-10', NULL
    ),
    (
        'B001', 'R004', '2024-03-15', '2024-03-16'
    ),
    (
        'B006', 'R005', '2024-03-03', NULL
    ),
    (
        'B003', 'R001', '2024-03-21', NULL
    ),
    (
        'B001', 'R005', '2024-03-17', '2024-03-18'
    ),
    (
        'B001', 'R006', '2024-03-19', '2024-03-20'
    ),
    (
        'B002', 'R001', '2024-03-08', '2024-03-09'
    ),
    (
        'B002', 'R005', '2024-03-09', '2024-03-10'
    ),
    (
        'B011', 'R005', '2024-03-11', '2024-03-25'
    ),
    (
        'B010', 'R002', '2024-03-12', NULL
    ),
    (
        'B007', 'R005', '2024-03-03', NULL
    ),
    (
        'B009', 'R005', '2024-03-03', NULL
    );

-- 插入预约数据
INSERT INTO
    reserve (book_id, reader_id, take_date) -- ver1将预约数据中4月改为6月
VALUES ('B001', 'R001', '2024-06-08'),
    ('B005', 'R004', '2024-06-08'),
    ('B008', 'R005', '2024-06-10'),
    ('B008', 'R002', '2024-06-10'),
    ('B010', 'R006', '2024-06-15');

#用SQL语言完成下面小题并测试运行结果
#查询读者rose借过的书（包括已还和未还）的图书号、书名和借期
SELECT bid, bname, borrow_Date
FROM Book, Borrow, Reader
WHERE
    Book.bid = Borrow.book_ID
    AND Reader.rid = Borrow.reader_ID
    AND Reader.rname = 'Rose';

#查询从没有借过图书也从没有预约过图书的读者号和读者姓名
SELECT rid, rname
FROM Reader
WHERE
    rid NOT IN(
        SELECT reader_ID
        FROM Borrow
        WHERE
            Borrow.reader_ID = Reader.rid
        UNION
        SELECT reader_ID
        FROM Reserve
        WHERE
            Reserve.reader_ID = Reader.rid
    )
    #查询被借阅次数最多的作者（注意一个作者可能写了多本书）
    #方法1：使用借阅表borrow中的借书记录

SELECT author, COUNT(*) #查询作者和借阅次数，然后按照借阅次数降序排序，取第一个
FROM Book, Borrow
WHERE
    Book.bid = Borrow.book_ID
GROUP BY
    author
ORDER BY COUNT(*) DESC
LIMIT 1;

#方法2：使用图书表book中的borrow_times
SELECT author, SUM(borrow_times) #思路和方法1类似，只是这里使用了SUM函数直接求借阅次数之和然后排序
FROM Book
GROUP BY
    author
ORDER BY SUM(borrow_times) DESC
LIMIT 1;

# 4.查询目前借阅未还的书名中包含“MySQL”的图书号和书名
SELECT bid, bname #bstatus=1表示借出，bname中包含MySQL
FROM Book
WHERE
    bstatus = 1
    AND bname LIKE '%MySQL%';

use lab01;
SELECT bid, bname
FROM borrow, book
WHERE
    book.bid = borrow.book_ID
    and borrow.return_date IS NULL
    and book.bname like '%MySQL%';

#5.查询目前借阅图书数目（多次借同一本需重复计入）超过3本的读者姓名
SELECT rname #查询读者姓名，然后按照读者号分组，统计借阅的书的数量，然后筛选出借阅的书的数量大于3的读者
FROM Reader, Borrow
WHERE
    Reader.rid = Borrow.reader_ID
GROUP BY
    Borrow.reader_ID
HAVING
    COUNT(*) > 3;

#6.查询没有借阅过任何一本 J.K. Rowling 所著的图书的读者号和姓名；
SELECT rid, rname #查询读者号和姓名，然后筛选出没有借阅过J.K. Rowling所著的图书的读者
FROM reader
WHERE
    rid NOT IN(
        SELECT DISTINCT
            Reader.rid
        FROM Reader, borrow, book
        WHERE
            reader.rid = borrow.reader_ID
            AND borrow.book_ID = book.bid
            AND book.author = 'J.K. Rowling'
    );

#7.查询2024年借阅图书数目排名前3名的读者号、姓名以及借阅图书数
SELECT rid, rname, COUNT(*) AS borrow_cnt #查询读者号、姓名和借阅图书数，然后按照借阅图书数降序排序，取前三名
FROM Reader, Borrow
WHERE
    Reader.rid = Borrow.reader_ID
    AND borrow_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY
    Borrow.reader_ID
ORDER BY COUNT(*) DESC
LIMIT 3;

#8.创建一个读者借书信息的视图，该视图包含读者号、姓名、所借图书号、
-- 图书名和借期（对于没有借过图书的读者，是否包含在该视图中均可）；
-- 并使用该视图查询2024年所有读者的读者号以及所借阅的不同图书数；
CREATE VIEW rb_view (
    rid, rname, bid, bname, borrow_Date
) AS
SELECT
    rid,
    rname,
    bid,
    bname,
    borrow_Date #创建视图，包含读者号、姓名、所借图书号、图书名和借期
FROM reader, borrow, book
WHERE
    reader.rid = borrow.reader_ID
    AND borrow.book_ID = book.bid;

SELECT rid, COUNT(DISTINCT bid) #查询2024年所有读者的读者号及借阅的不同图书数
FROM rb_view
WHERE
    borrow_Date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY
    rid;

-- 3. 设计一个存储过程updateReaderID，实现对读者表的ID的修改，
--  使用该存储过程将读者ID中 'R006' 改为 'R999'
DROP PROCEDURE IF EXISTS updateReaderID;

DELIMITER //

CREATE PROCEDURE updateReaderID(IN pre_ID CHAR(8), 
IN new_ID CHAR(8)) 
BEGIN 
	# 解除外键约束
	SET FOREIGN_KEY_CHECKS = 0;
	UPDATE borrow 
    SET reader_ID = new_ID 
        WHERE reader_ID = pre_ID;
	#创建存储过程updateReaderID，将借书记录中reader_ID中pre_ID改为new_ID
	UPDATE reserve 
    SET reader_ID = new_ID 
        WHERE reader_ID = pre_ID;
	#创建存储过程updateReaderID，将预约记录中reader_ID中pre_ID改为new_ID
	UPDATE Reader 
    SET rid = new_ID 
        WHERE rid = pre_ID;
	#创建存储过程updateReaderID，将读者ID中pre_ID改为new_ID
	SET FOREIGN_KEY_CHECKS = 1; # 恢复外键约束
END
// 
DELIMITER;

CALL updateReaderID ('R006', 'R999');
#调用存储过程updateReaderID
CALL updateReaderID ('R999', 'R006');

SELECT * FROM Reader;
# 展示变化
# 4、设计一个存储过程 borrowBook，当读者借书时调用该存储过程完成借书处理，要求：
# A. 一个读者最多只能借阅3本图书，意味着如果读者已经借阅了3本图书并且未归还则不允许再借书
# B.同一天不允许同一个读者重复借阅同一本书
# C. 如果该图书存在预约记录，而当前借阅者没有预约，则不许借阅；
#（思考：在实现时，处理借书请求的效率是否和 A、B、C 的实现顺序有关系？）
# D.如果借阅者已经预约了该图书，则允许借阅，但要求借阅完成后删除借阅者对该图书的预约记录；
# E.借阅成功后图书表中的 times 加 1，修改 bstatus，并在borrow表中插入相应借阅信息
USE lab01;
DROP PROCEDURE IF EXISTS BorrowBook;
DELIMITER //

CREATE PROCEDURE BorrowBook(IN bookID CHAR(8), IN readerID CHAR(8), IN borrowDate DATE)
BEGIN
    DECLARE borrowed_cnt INT;
    DECLARE reserved_cnt INT;
    DECLARE reserved_status INT;
    -- 查询读者是否已经借阅过这本书
    SELECT COUNT(*)
    INTO borrowed_cnt
    FROM borrow
    WHERE reader_ID = readerID
      AND book_ID = bookID
      AND borrow_Date = borrowDate;
    -- 如果已经借阅过这本书，则不允许再借
    IF borrowed_cnt > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The reader has already borrowed this book today.';
    END IF;
    -- 查询读者借阅的书的数量
    SELECT COUNT(*)
    FROM borrow
    WHERE 
        reader_ID = readerID 
        AND return_Date IS NULL INTO borrowed_cnt;  -- 注意，是未归还的书
    -- 如果借阅的书的数量大于等于3，则不允许再借书
    IF borrowed_cnt >= 3 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A reader can borrow at most 3 books';
    END IF;
    -- 查询该图书的预约人数
    SELECT reserve_Times
    INTO reserved_cnt
    FROM Book
    WHERE bookID = bid;
    -- 如果该图书存在预约记录，而当前借阅者没有预约，则不许借阅；
    IF reserved_cnt > 0 THEN
        SELECT COUNT(*)
        INTO reserved_status
        FROM reserve
        WHERE book_ID = bookID
          AND reader_ID = readerID;
-- 如果借阅者没有预约该图书，则不允许借阅，否则可以借阅，并在借阅后删除预约记录
        IF reserved_status = 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The book is reserved by others.';
        ELSE
            DELETE FROM reserve
            WHERE book_ID = bookID
              AND reader_ID = readerID;
        -- 借阅成功后图书表中的 times 加 1，修改 bstatus，并在 borrow 表中插入相应借阅信息
        INSERT INTO borrow (reader_ID, book_ID, borrow_Date, return_Date)
        VALUES (readerID, bookID, borrowDate, NULL);

        UPDATE Book SET borrow_Times = borrow_Times + 1, bstatus = 1
        WHERE bid = bookID;

        SELECT 'Book borrowed successfully.' AS message;
        END IF;
    ELSE  -- 如果该图书没有预约记录，则直接借阅
        INSERT INTO borrow (reader_ID, book_ID, borrow_Date, return_Date)
        VALUES (readerID, bookID, borrowDate, NULL);

        UPDATE Book SET borrow_Times = borrow_Times + 1, bstatus = 1
        WHERE bid = bookID;

        SELECT 'Book borrowed successfully.' AS message;
    END IF;
END//

DELIMITER ;

#ID为‘R001’的读者借阅ID为‘B008’的书的请求（未预约），显示借阅失败信息。
CALL BorrowBook('B008', 'R001', '2024-05-09');

#ID为‘R001’的读者借阅ID为‘B001’的书的请求（已预约），显示借阅成功信息，并展示预约表相关预约记录被删除，
-- 以及图书表对应书籍的borrow_times和bstatus属性的变化。
CALL BorrowBook('B001', 'R001', '2024-05-09');
SELECT * FROM Reserve WHERE book_ID = 'B001';
SELECT * FROM Book WHERE bid = 'B001';

#ID为‘R001’的读者再次借阅ID为‘B001’的书的请求（同一天已经借阅过），显示借阅失败信息。
CALL BorrowBook('B001', 'R001', '2024-05-09');

#ID为‘R005’的读者借阅ID为‘B008’的书的请求（已借三本书未还），显示借阅失败信息
CALL BorrowBook('B008', 'R005', '2024-05-09');

USE lab01;
DROP PROCEDURE IF EXISTS ReturnBook;
-- 参考 4，设计一个存储过程 returnBook，当读者还书时调用该存储过程完成还书处理。要求：
-- A. 还书后补上借阅表 borrow 中对应记录的 return_date;
-- B. 还书后将图书表 book 中对应记录的 bstatus 修改为 0（没有其他预约）或 2（有其他预约）
DELIMITER //
CREATE PROCEDURE ReturnBook(IN BookID CHAR(8), IN ReaderID CHAR(8), IN ReturnDate DATE)
BEGIN
    DECLARE bookstatus INT; # 用于记录是否被借出
    DECLARE reservecnt INT; # 用于记录预约人数
    SELECT COUNT(*)  # 查询是否被借出
    FROM borrow
    WHERE
        book_ID = BookID
        AND reader_ID = ReaderID
    INTO bookstatus;

    SELECT reserve_Times # 查询预约人数，存入reservecnt中
    FROM book
    WHERE bid = BookID
    INTO reservecnt;
    IF bookstatus = 0 THEN  # 如果没有被借出，则不允许还书
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The book has not been borrowed by the reader.';
    ELSE
        UPDATE borrow # 还书后补上借阅表 borrow 中对应记录的 return_date
        SET return_date = ReturnDate
        WHERE
            book_ID = BookID
            AND reader_ID = ReaderID;
        IF reservecnt = 0 THEN # 如果没有预约，则修改bstatus为0
            UPDATE book
            SET bstatus = 0
            WHERE bid = BookID;
        ELSE # 如果有预约，则修改bstatus为2
            UPDATE book
            SET bstatus = 2
            WHERE bid = BookID;
        END IF;
        SELECT 'Book returned successfully.' AS message;
    END IF;
END //
DELIMITER ;

# ID为‘R001’的读者归还ID为‘B008’的书的请求（未借阅），并展示还书失败信息
CALL returnBook('B008', 'R001', '2024-05-10');

#ID为‘R001’的读者归还ID为‘B001’的书的请求，并展示书籍在book表中的bstatus以及在borrow表中的return_date的变化
CALL returnBook('B001', 'R001', '2024-05-10');
SELECT bstatus FROM Book WHERE bid = 'B001';
SELECT return_Date FROM borrow WHERE book_ID = 'B001' AND reader_ID = 'R001';

#6.设计触发器，实现：
#A. 当一本书被预约时, 自动将图书表 book 中相应图书的 bstatus修改为 2，并增加 reserve_Times；
#B. 当某本预约的书被借出时或者读者取消预约时, 自动减少reserve_Times；
#C. 当某本书的最后一位预约者取消预约且该书未被借出（修改前bstatus 为 2）时， 将 bstatus 改为 0。
USE lab01;
DROP Trigger IF EXISTS auto_reserve;
DELIMITER //
CREATE TRIGGER auto_reserve   # 创建触发器auto_reserve，在预约表中插入记录时触发
AFTER INSERT ON reserve FOR each ROW
BEGIN
    UPDATE book
    SET bstatus = 2,  # 当一本书被预约时, 自动将图书表 book 中相应图书的 bstatus修改为 2并且增加reserve_Times
        reserve_Times = reserve_Times + 1
    WHERE bid = NEW.book_ID;
END
DELIMITER ;

DROP Trigger IF EXISTS auto_borrow;
DELIMITER //
CREATE TRIGGER auto_borrow
AFTER DELETE ON reserve FOR each ROW
BEGIN
    UPDATE book
    SET reserve_Times = reserve_Times - 1
    WHERE bid = OLD.book_ID;  # 当某本预约的书被借出时或者读者取消预约时, 自动减少reserve_Times
END //
DELIMITER ;

DROP Trigger IF EXISTS auto_cancel;
DELIMITER //
CREATE TRIGGER auto_cancel
AFTER DELETE ON reserve FOR each ROW
BEGIN
    UPDATE book
    SET bstatus = 0
    WHERE bid = old.book_ID
        AND bstatus = 2
        AND reserve_Times = 0;  # 当某本书的最后一位预约者取消预约且该书未被借出时， 将 bstatus 改为 0
END //
DELIMITER ;
use lab01;
#ID为‘R001’的读者预约ID为‘B012’的书，再取消预约的请求，展示过程中reserve_Times 和 bstatus 的变化
INSERT INTO reserve (book_ID, reader_ID, take_Date)
VALUES ('B012', 'R001', '2025-06-25');
SELECT reserve_Times, bstatus FROM book WHERE bid = 'B012';
DELETE FROM reserve WHERE book_ID = 'B012' AND reader_ID = 'R001';
SELECT reserve_Times, bstatus FROM book WHERE bid = 'B012';