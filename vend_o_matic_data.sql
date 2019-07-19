-- CREATE AND LOAD TABLES QUERIES

CREATE TABLE Drinks ( id int NOT NULL, name VARCHAR(50) NOT NULL, quarters int NOT NULL, quantity int NOT NULL, vending_machine_id int NOT NULL, PRIMARY KEY (id));

INSERT INTO Drinks (id, name, quarters, quantity, vending_machine_id)
VAlUES(1, 'Coca-cola', 2, 5, 1);

INSERT INTO Drinks (id, name, quarters, quantity, vending_machine_id)
VAlUES(2, 'Sprite', 2, 5, 1);

INSERT INTO Drinks (id, name, quarters, quantity, vending_machine_id)
VAlUES(3, 'Pepsi', 2, 5, 1);


CREATE TABLE Vending_Machine (id int NOT NULL, coin_quantity int NOT NULL, temp_coin_quantity_id int NOT NULL, PRIMARY KEY (id));

INSERT INTO Vending_Machine (id, coin_quantity, temp_coin_quantity_id)
VALUES(1, 0, 1);


CREATE TABLE Temp_Coin_Quantity (id int NOT NULL, temp_coins int NOT NULL, PRIMARY KEY (id));

INSERT INTO Temp_Coin_Quantity (id, temp_coins)
VALUES(1, 0);

-- DROP TABLES QUERIES

drop table drinks;
drop table vending_machine;
drop table temp_coin_quantity;