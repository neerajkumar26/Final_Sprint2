from flask import Flask, request, render_template, jsonify, redirect, session, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'qwertyuio'

# Establish a connection to the database
mydb = pymysql.connect(
  host = "localhost",
  user = "root",
  password = "",
  database = "Interstellar Cargo Transportation"
)

# Same as others

@app.route('/cargo')
def cargo():
    try:
        # Call the get_cargo() function to retrieve data from the database
        cargo_data = get_cargo()
        # Render the cargo.html template with the retrieved data
        return render_template('cargo.html', cargo_data=cargo_data)
    except Exception as e:
        # Return an error message if there's any exception
        print("Error occurred: ", e)
        return jsonify({'error ': str(e)})
    
def get_cargo():
    try:
        # Open a cursor to execute SQL queries
        with mydb.cursor() as cursor:
            
            sql = "SELECT * FROM cargo ORDER BY ID"
            cursor.execute(sql)
            # Fetch all the rows returned by the query
            rows = cursor.fetchall()
            # Create a list of dictionaries where each dictionary represents a row
            cargo_data = []
            for row in rows:
                cargo_item = {
                    'id' : row[0],
                    'weight': row[1],
                    'cargotype': row[2],
                    'departure': row[3],
                    'arrival': row[4]
                }
                cargo_data.append(cargo_item)

        return cargo_data
    
    except Exception as e:
        # Return an error message if there's any exception
        print("Error occurred: ", e)
        return jsonify({'error ': str(e)})

def get_cargo_id(id):
    try:
        # Open a cursor to execute SQL queries
        with mydb.cursor() as cursor:
            # Execute a SELECT SQL query
            sql = ("SELECT * FROM cargo WHERE id = %s",id)
            cursor.execute(sql)
            rows = cursor.fetchall()
            cargo_data = []
            for row in rows:
                cargo_item = {
                    'id' : row[0],
                    'weight': row[1],
                    'cargotype': row[2],
                    'departure': row[3],
                    'arrival': row[4]
                }
                cargo_data.append(cargo_item)

        return cargo_data
    except:
        print('error occured.')

@app.route('/cargo/add', methods=['POST'])
def add_cargo():
    try:
    
        weight = request.form.get('weight')
        cargotype = request.form.get('cargo_type')
        departure = request.form.get('departure')
        arrival = request.form.get('arrival')
        shipid = request.form.get('shipid')

        # print(f"weight:{weight} cargotype:{cargotype} departure:{departure} arrival:{arrival} shipid:{shipid}")
        # Insert new cargo entry into 'cargo' table
        cursor = mydb.cursor()
        sql = f"INSERT INTO cargo (weight, cargotype, departure, arrival, shipid) VALUES ('{weight}', '{cargotype}', '{departure}', '{arrival}','{shipid}')"
        val = (weight, cargotype, departure, arrival, shipid)
        print("data requested 200")
        cursor.execute(sql)
        mydb.commit()
        return redirect(url_for('cargo'))
        # Return success message
        # return jsonify({'message': 'Cargo added successfully!'})

    except pymysql.Error as error:
        # Handle database errors
        return jsonify({'dtabase error': str(error)})
    
    except Exception as error:
        # Handle all other errors
        return jsonify({'error unknown ': str(error)})

    finally:
        # Close database connection
        if 'conn' in locals() and mydb.is_connected():
            cursor.close()
            mydb.close()
            print("Database connection closed.")

#update cargo items
@app.route('/cargo/update', methods=['GET','POST'])
def update_cargo():
    
    cursor = mydb.cursor()
    id = request.form['id']
    weight = request.form['weight']
    cargotype = request.form['cargotype']
    departure = request.form['departure']
    arrival = request.form['arrival']
    shipid = request.form['shipid']
    # Build the UPDATE query
    update_query = f"UPDATE cargo SET weight = '{weight}',cargotype = '{cargotype}',departure = '{departure}',arrival = '{arrival}',shipid= '{shipid}'"
    update_query += f" WHERE id = {id}"
    
    try:
        cursor.execute(update_query)
        mydb.commit()
        cursor.close()
        flash('Cargo details updated successfully.', 'success')
        return redirect('/cargo')
    except Exception as e:
        print(e)
        mydb.rollback()
        return {"error": "Cargo record update failed"}       

# Delete cargo by id
@app.route('/cargo/delete/<int:id>')
def delete_cargo(id):
    try:
        cur = mydb.cursor()
        cur.execute("DELETE FROM cargo WHERE id=%s", (id,))
        mydb.commit()
        cur.close()

        # Return success message
        # return jsonify({'message': 'Cargo with id {} deleted successfully.'.format(id)}), 200
        return redirect(url_for('cargo'))

    except Exception as e:
        # Roll back the transaction if there is an error
        mydb.rollback()
        cur.close()
        return jsonify({'message': str(e)}), 500

#CAPTAIN ROUTING DETAILS 
@app.route('/captain')
def captain():
    try:
        captain_data = get_captain()
        return render_template('captain.html', captain_data=captain_data)
    except Exception as e:
        print("Error occurred in displaying captain html file: ", e)
        return {'error ': str(e)}

def get_captain():
    try:
        # Open a cursor to execute SQL queries
        with mydb.cursor() as cursor:
            # Execute a SELECT SQL query
            sql = "SELECT * FROM captain ORDER BY ID"
            cursor.execute(sql)

            # Fetch all the rows returned by the query
            rows = cursor.fetchall()
             # Create a list of dictionaries where each dictionary represents a row
            captain_data = []
            for row in rows:
                captain_item = {
                    'firstname': row[1],
                    'lastname': row[2],
                    'rank': row[3],
                    'homeplanet': row[4]
                }
                captain_data.append(captain_item)
        return captain_data
        # return jsonify(rows)
    
    except Exception as e:
        # Return an error message if there's any exception
        print("Error occurred: ", e)
        return jsonify({'error ': str(e)})

# API to insert data into the 'captain' table
@app.route('/captain/add', methods=['POST'])
def add_captain():
    cursor = mydb.cursor()
    try:
        # Extracting data from the request body
        # data = request.get_json()
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        rank = request.form.get('rank')
        homeplanet = request.form.get('homeplanet')
        
        # Inserting the data into the 'captain' table
        query = f"INSERT INTO captain (firstname, lastname, rank, homeplanet) VALUES ('{firstname}', '{lastname}', '{rank}', '{homeplanet}')"
        # values = (firstname, lastname, rank, homeplanet)
        cursor.execute(query)
        mydb.commit()
        flash('Captain added successfully')
        return redirect(url_for('captain'))

    except Exception as e:
        print("Error occurred: ", e)
        return jsonify({"message": "Unable to add captain."}), 500

@app.route('/captain/update', methods=['POST'])
def update_captain():
    try:
        # request_data = request.json()
        cursor = mydb.cursor()
        id = request.form['id']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        rank = request.form['rank']
        home_planet = request.form['homeplanet']
        
        
        # Update the captain details
        update_query = f"UPDATE captain SET firstname = '{first_name}',lastname = '{last_name}',rank = '{rank}',homeplanet = '{home_planet}'"
        update_query += f" WHERE id = {id}"
        cursor.execute(update_query)
        mydb.commit()
        cursor.close()
        flash('Captain details updated successfully.', 'success')
        # Return success message
        return redirect(url_for('captain'))

    except Exception as e:
        # Rollback the transaction if any error occurs
        mydb.rollback()
        return {"error": f"An error occurred while updating the captain details: {str(e)}"}

# Delete captain by id
@app.route('/captain/delete/<int:id>')
def delete_captain(id):
    try:
        # Create a cursor object
        cur = mydb.cursor()
        cur.execute("DELETE FROM captain WHERE id=%s", (id,))
        mydb.commit()
        cur.close()

        # Return success message
        return redirect(url_for('captain'))

    except Exception as e:
        # Roll back the transaction if there is an error
        mydb.rollback()
        cur.close()

        # Return error message
        return jsonify({'message': str(e)}), 500

#SPACESHIP API ROUTING DETAILSSS>..... 
@app.route('/spaceship')
def spaceship():
    try:
        spaceship = get_spaceShip()
        return render_template('spaceship.html', spaceship = spaceship)
    except Exception as e:
        # Return an error message if there's any exception
        print("Error occurred: ", e)
        return jsonify({'error ': str(e)})

def get_spaceShip():
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT * FROM spaceship ORDER BY id"
            cursor.execute(sql)

            rows = cursor.fetchall()
            spaceship = []
                        
            for item in rows:
                spaceship_item = {
                    'maxweight': item[1],
                    'captainid':item[2]
                }
                spaceship.append(spaceship_item)
        return spaceship
    
    except Exception as e:
        return jsonify({'error ': str(e)})
    
@app.route('/spaceship/add', methods=['POST'])
def add_spaceship():
    cursor = mydb.cursor()
    maxweight = request.form.get('maxweight')
    captainid = request.form.get('captainid')
    sql = "INSERT INTO spaceship (maxweight, captainid) VALUES (%s, %s)"
    val = (maxweight, captainid)
    try:
        cursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('spaceship'))
    except pymysql.Error as err:
        mydb.rollback()
        return jsonify({"message": "Error creating spaceship: " + str(err)}), 400

@app.route('/spaceship/update', methods=['POST'])
def update_spaceship():
    try:
        cursor = mydb.cursor()
        id = request.form['id']
        maxweight = request.form['maxweight']
        captainid = request.form['captainid']
       
        # Update the spaceship details
        update_query = f"UPDATE spaceship SET maxweight = '{maxweight}', captainid='{captainid}"
        update_query += f" WHERE id = {id}"
        cursor.execute(update_query)
        mydb.commit()
        cursor.close()
        flash('Spaceship details updated successfully.', 'success')
        # Return success message
        return redirect(url_for('spaceship'))

    except Exception as e:
        # Rollback the transaction if any error occurs
        mydb.rollback()
        return {"error": f"An error occurred while updating the spaceship details: {str(e)}"}

# Delete spaceship by id
@app.route('/spaceship/delete/<int:id>')
def delete_spaceship(id):
    try:
        # Create a cursor object
        cur = mydb.cursor()
        cur.execute("DELETE FROM spaceship WHERE id=%s", (id,))
        mydb.commit()
        cur.close()

        # Return success message
        return redirect(url_for('spaceship'))

    except Exception as e:
        # Roll back the transaction if there is an error
        mydb.rollback()

        # Close the cursor and connection
        cur.close()

        # Return error message
        return jsonify({'message': str(e)}), 500

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login_post():
    # Hardcoded username and password
    USERNAME = "user"
    PASSWORD = "000"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            print('form filled')
            # Set the 'logged_in' flag in the session
            session['logged_in'] = True
            return redirect('/home')
        else:
            return render_template('login.html',error='Invalid username or password')
    
    print('not a post Request.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove the 'logged_in' flag from the session
    session.pop('logged_in', None)
    return redirect('/login')

if __name__ == '__main__':
  app.run(debug=True)
