CREATE DATABASE ARTGALLERY;
USE ARTGALLERY;

---creating tables and adding records into each

CREATE TABLE ARTADMIN
(
    admin_username VARCHAR(20),
    admin_email VARCHAR(50) UNIQUE,
    admin_password VARCHAR(20) CHECK (LENGTH(admin_password) >= 8 AND LENGTH(admin_password) <= 20),
    PRIMARY KEY (admin_username)
);

CREATE TABLE ARTIST (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    artist_name VARCHAR(25) NOT NULL,
    artist_dob DATE NOT NULL,
    artist_style VARCHAR(50) NOT NULL,
    artist_email VARCHAR(40) NOT NULL,
    artist_mobNum NUMERIC(10) NOT NULL,
    artist_place VARCHAR(20)
);
INSERT INTO ARTIST (artist_name, artist_dob, artist_style, artist_email, artist_mobNum, artist_place) 
VALUES 
('Amrita Sher-Gil', '1913-01-30', 'Modernism', 'amritasher@gmail.com', 9876543210, 'Delhi'),
('Raja Ravi', '1848-04-29', 'Realism', 'rrv@gmail.com', 8765432109, 'Trivandrum'),
('Bhupen Khakhar', '1934-03-10', 'Modern Indian Art', 'bhupenkhakhar@artstudio.com', 7654321098, 'Cochin'),
('Tyeb Mehta', '1925-07-25', 'Modernism', 'tyebmehta@example.com', 6543210987, 'Pune'),
('S.H. Raza', '1922-02-22', 'Abstract Expressionism', 'shraza@modernart.com', 5432109876, 'Mumbai'),
('Damien Hirst', '1965-06-07', 'Conceptual Art', 'damienhirst@example.com', 4321098765, 'Mumbai'),
('Yayoi Kusama', '1929-03-22', 'Contemporary Art', 'yayoikusama@artworld.com', 3210987654, 'Delhi'),
('Banksy', '2003-12-31', 'Street Art', 'banksy@anonymous.com', 2109876543, 'Jaipur'),
('JR', '2004-02-09', 'Street Photography', 'jr@photographer.com', 1098765432, 'Delhi');

CREATE TABLE CUSTOMER (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_name VARCHAR(50) NOT NULL,
    cust_aadhar_num numeric(12) NOT NULL,
    cust_email VARCHAR(100) UNIQUE NOT NULL,
    cust_mobNum numeric(10) NOT NULL,
    cust_place VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
('John Doe', 123456789012, 'john.doe@example.com', 9876543210, 'Mumbai'),
('Alice Smith', 234567890123, 'alice.smith@example.com', 8765432109, 'Delhi'),
('Bob Johnson', 345678901234, 'bob.johnson@example.com', 7654321098, 'Bangalore'),
('Emily Brown', 456789012345, 'emily.brown@example.com', 6543210987, 'Chennai'),
('Michael Davis', 567890123456, 'michael.davis@example.com', 5432109876, 'Kolkata');

CREATE TABLE ART (
    art_id VARCHAR(10) PRIMARY KEY,
    art_title VARCHAR(50) NOT NULL,
    art_artist VARCHAR(30),
    art_price DECIMAL(8,2),
    art_type VARCHAR(20),
    art_year DATE
);
INSERT INTO ART (art_id, art_title, art_artist, art_price, art_type, art_year)
VALUES 
('A001', 'Untitled', 'Amrita Sher-Gil', 5000.00, 'Oil Painting', '1950-01-01'),
('A002', 'Raja Ravi Varma Portrait', 'Raja Ravi', 10000.00, 'Oil Painting', '1870-01-01'),
('A003', 'Village Scene', 'Bhupen Khakhar', 15000.00, 'Oil Painting', '1960-01-01'),
('A004', 'Falling Figures', 'Tyeb Mehta', 7500.00, 'Oil Painting', '1980-01-01'),
('A005', 'Bindu', 'S.H. Raza', 8000.00, 'Oil Painting', '1970-01-01'),
('A006', 'The Physical Impossibility of Death', 'Damien Hirst', 7000.00, 'Sculpture', '1990-01-01'),
('A007', 'Infinity Mirror Room', 'Yayoi Kusama', 8500.00, 'Installation Art', '2000-01-01'),
('A008', 'Balloon Girl', 'Banksy', 6000.00, 'Stencil Art', '2010-01-01'),
('A009', 'The Wrinkles of the City', 'JR', 9000.00, 'Photography', '2020-01-01');

CREATE TABLE ORDERS (
    ord_num INT AUTO_INCREMENT PRIMARY KEY,
    cust_num INT NOT NULL,
	ord_date DATE,
    art_id VARCHAR(10) NOT NULL,
    ord_payment VARCHAR(15) NOT NULL
);
INSERT INTO ORDERS (cust_num, ord_date, art_id, ord_payment)
VALUES 
(1, '2024-04-13', 'A001', '5000'),
(2, '2024-04-13', 'A004', '7500'),
(3, '2024-04-13', 'A003', '15000'),
(4, '2024-04-13', 'A006', '7000');

ALTER TABLE ORDERS ADD FOREIGN KEY(cust_num) REFERENCES CUSTOMER(cust_id);
ALTER TABLE ORDERS ADD FOREIGN KEY(art_id) REFERENCES ART(art_id);
ALTER TABLE ORDERS AUTO_INCREMENT = 5001;

---trigger created to set date
DELIMITER //
CREATE TRIGGER SetOrderDate
BEFORE INSERT ON ORDERS
FOR EACH ROW
BEGIN
  SET NEW.ord_date = CURDATE();
END;
//
DELIMITER ;

---procedure to filter out artworks by an artist
CREATE PROCEDURE GetArtworksByArtist(IN artist_name VARCHAR(255))
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE art_id_val VARCHAR(10);
    DECLARE art_title_val VARCHAR(50);
    DECLARE art_artist_val VARCHAR(50);
    DECLARE art_price_val DECIMAL(8, 2);
    DECLARE art_type_val VARCHAR(20);
    DECLARE art_year_val DATE;

    DECLARE cursor_artworks CURSOR FOR
        SELECT art_id, art_title, art_artist, art_price, art_type, art_year FROM ART WHERE art_artist = artist_name;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cursor_artworks;
    cursor_loop: LOOP
        FETCH cursor_artworks INTO art_id_val, art_title_val, art_artist_val, art_price_val, art_type_val, art_year_val;
        IF done THEN
            LEAVE cursor_loop;
        END IF;
        SELECT art_id_val, art_title_val, art_artist_val, art_price_val, art_type_val, art_year_val;
    END LOOP;
    CLOSE cursor_artworks;
END;
//
DELIMITER ;

---procedure to place order by validating customerid and artid 
DELIMITER //
CREATE PROCEDURE PlaceOrder(
    IN customer_id INT,
    IN artist_id VARCHAR(10),
    IN order_payment VARCHAR(15),
    OUT success INT
)
BEGIN
    DECLARE cust_exists INT;
    DECLARE art_exists INT;

    -- Check if customer exists
    SELECT COUNT(*) INTO cust_exists FROM CUSTOMER WHERE cust_id = customer_id;

    -- Check if artwork exists
    SELECT COUNT(*) INTO art_exists FROM ART WHERE art_id = artist_id;

    -- Insert order if customer and artwork exist
    IF cust_exists = 1 AND art_exists = 1 THEN
        INSERT INTO ORDERS (cust_num, art_id,ord_payment) 
        VALUES (customer_id, artist_id, order_payment);
        SET success = 1;
    ELSE
        SET success = 0;
    END IF;
END //

DELIMITER //

---procedure to check if customer exist by checking email in customer side
DELIMITER //
CREATE PROCEDURE CheckCustomerEmailExists(
    IN p_cust_email VARCHAR(100),
    OUT email_exists INT
)
BEGIN
    DECLARE count_email INT;
    
    -- Check if the email exists
    SELECT COUNT(*) INTO count_email FROM CUSTOMER WHERE cust_email = p_cust_email;
    
    -- Set the output parameter based on the count
    IF count_email > 0 THEN
        SET email_exists = 1;
    ELSE
        SET email_exists = 0;
    END IF;
END//