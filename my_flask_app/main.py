import json
from app import app
from flask import Flask, jsonify, abort, flash, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ujnikmol,'
app.config['MYSQL_DB'] = 'Testing'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# This function returns the amount of coins in the temp_coin_quantity table.
@app.route('/', methods=['GET'])
def check_coins():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT temp_coins FROM Temp_Coin_Quantity''')
    rv = list(cur.fetchall())
    return str(rv[0]['temp_coins'])


#Increments the number of coins in the temp_coin_quantity table
# by 1 and returns the most updated value.
@app.route('/', methods=['PUT'])
def insert_coin():
    cur = mysql.connection.cursor()
    coins = int(check_coins())
    new_value = coins + 1
    cur.execute(
        '''
        UPDATE Temp_Coin_Quantity
        SET temp_coins = {}
        WHERE id = 1
        '''.format(new_value))
    mysql.connection.commit()
    cur.execute('''SELECT temp_coins FROM Temp_Coin_Quantity''')
    rv = list(cur.fetchall())
    rv_json = jsonify(cur.fetchall())
    rv_json.headers.set('X-Coins', coins)
    return jsonify(rv[0]['temp_coins'])
    
# Decrements one coin from temp_coin_quantity table.
# Returns quantity of coins in machine.   
@app.route('/subtract', methods=['PUT'])
def return_one_coin():
    cur = mysql.connection.cursor()
    coins = int(check_coins())
    if coins > 0:
        new_value = coins - 1
    else:
        new_value = 0
    cur.execute(
        '''
        UPDATE Temp_Coin_Quantity
        SET temp_coins = {}
        WHERE id = 1
        '''.format(new_value))
    mysql.connection.commit()
    cur.execute('''SELECT temp_coins FROM Temp_Coin_Quantity''')
    rv = list(cur.fetchall())
    return str(rv[0]['temp_coins'])

# Returns array of all drink objects.
@app.route('/inventory', methods=['GET'])
def get_all_inventory():
    cur = mysql.connection.cursor()
    cur.execute(
        '''
        SELECT * FROM Drinks
        ''')
    rv = jsonify(cur.fetchall())
    return rv

# Returns one drink, based on id, in JSON format.
@app.route('/inventory/<id>', methods=['GET'])
def get_single_drink(id):
    cur = mysql.connection.cursor()
    cur.execute(
        '''
        SELECT * FROM Drinks
        WHERE id = {}
        '''.format(id))
    rv = jsonify(cur.fetchall())
    return rv

# Returns the quantity of one drink, based on it's id, as an string.
def get_single_drink_quantity(id):
    cur = mysql.connection.cursor()
    cur.execute(
        '''
        SELECT quantity FROM Drinks
        WHERE id = {0}
        '''.format(id))
    rv = str(cur.fetchall()[0]['quantity'])
    return rv

# Returns the name of one drink, based on it's id, as an string.
def get_single_drink_name(id):
    cur = mysql.connection.cursor()
    cur.execute(
        '''
        SELECT name FROM Drinks
        WHERE id = {0}
        '''.format(id))
    rv = str(cur.fetchall()[0]['name'])
    return rv

def set_coins_to_zero():
    cur = mysql.connection.cursor()
    cur.execute(
        '''
        UPDATE temp_coin_quantity
        SET temp_coins = {0}
        Where id = 1
        '''.format('0'))
    mysql.connection.commit()

def return_change():
    coins = int(check_coins())
    if coins > 2:
        change_to_return = coins - 2
        for _ in range(change_to_return):
            return_one_coin()
        set_coins_to_zero()
        return change_to_return


def get_vm_coins():
    cur = mysql.connection.cursor()
    cur.execute(
        '''
        SELECT coin_quantity
        FROM vending_machine
        ''')
    rv = str(cur.fetchall()[0]['coin_quantity'])
    return rv

def add_coins_to_vm():
    cur = mysql.connection.cursor()
    coins = int(get_vm_coins()) + 2
    cur.execute(
        '''
        UPDATE Vending_Machine
        SET coin_quantity = {0}
        Where id = 1
        '''.format(coins))

# Decrements drink quantity by 1 based on drink id.
@app.route('/inventory/<id>', methods=['PUT'])
def update_inventory(id):
    cur = mysql.connection.cursor()
    coins = int(check_coins())
    soda_count = int(get_single_drink_quantity(id))
    soda_name = get_single_drink_name(id)

    if coins == 0:
        abort(403, 
        '''
        Insufficient funds. You must enter 2 coins to get a drink.
        ''')

    if coins == 1:
        abort(403, 
        '''
        Insufficient funds. You must enter 1 more coin to get a drink.
        ''')

    if soda_count < 1:
        abort(404, 'Sorry, but {0} is sold out!'.format(soda_name))

    new_soda_count = soda_count - 1
    cur.execute(
        '''
        UPDATE Drinks
        SET Quantity = {0}
        WHERE id = {1}
        '''.format(new_soda_count, id))
    add_coins_to_vm()
    mysql.connection.commit()
    rv = jsonify(cur.fetchall())
    rv.headers.set('Coins Returned', return_change())
    return rv

if __name__ == '__main__':
    app.run(debug=True)
		