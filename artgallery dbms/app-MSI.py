#importing required libraries
from flask import Flask, render_template, request,url_for,session,redirect
import MySQLdb
from MySQLdb import Error as DBError
import MySQLdb.cursors

#flask
app = Flask(__name__)

#database connection
db = MySQLdb.connect("localhost","root","Menaswa18#","artgallery" )
cur = db.cursor()

app.secret_key = 'Menaswa18#'

#starting arrow to inside webpage 
@app.route('/')
def home():
	return render_template('index.html')

#directing to sign up page
@app.route('/front')
def front():
	return render_template('front.html')

#to logout and reach the signup page
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('password',None)
    session.pop('username',None)
    return redirect(url_for('front'))

#to go back to the home page
@app.route('/Home')
def home_page():
	return render_template('nav-bar.html')

#to view the gallery of artworks
@app.route('/gallery')
def gallery():
	return render_template('gallery.html')

'''ADMIN PART'''

#to display the customer details
@app.route('/customers',methods = ['POST','GET'])
def customers():
	cur.execute("SELECT cust_id, cust_name, cust_aadhar_num, cust_email, cust_mobNum, cust_place FROM CUSTOMER")
	customers_details= cur.fetchall()
	x = len(customers_details)
	return render_template('customers.html',c = customers_details,z = x)

#to enter new customer go to newcustomer.html
@app.route('/gonewcust')
def gonewcust():
	return render_template('newcustomer.html')

#to add new customer details
@app.route('/newcustomer',methods = ['POST', 'GET'])
def newcustomer():
    try:
        cname = request.form['cust_name']
        caadhaar = request.form['aadhaar_num']
        cmail = request.form['cust_email']
        cmob = request.form['cust_mobNum']
        cplace = request.form['cust_place']

        # SQL query to insert a new customer
        sql = """INSERT INTO CUSTOMER (cust_name, cust_aadhar_num, cust_email, cust_mobNum, cust_place) 
                 VALUES (%s, %s, %s, %s, %s)"""
        val = (cname, caadhaar, cmail, cmob, cplace)

        # Execute the SQL query
        cur.execute(sql, val)
        db.commit()

        # Successful insertion
        return render_template('newcustomer.html', msg="Successfully Registered")

    except MySQLdb.IntegrityError as e:
        # Handle integrity error (unique constraint violation)
        db.rollback()  # Rollback the transaction
        error_msg = f"Error: {str(e)}"
        print("Integrity Error:", error_msg)
        return render_template('newcustomer.html', msg="Email already exists. Please use a different email.")

    except Exception as e:
        # Handle other exceptions
        db.rollback()  # Rollback the transaction
        error_msg = "An error occurred: " + str(e)
        print("Error:", error_msg)
        return render_template('newcustomer.html', msg="An error occurred. Please try again later.")

#to delete a customer go to delete.html
@app.route('/godel')
def delecustomer():
	return render_template('del.html')

#to delete a customer
@app.route('/del',methods = ['POST', 'GET'])
def delcustomer():
	try:
		DID = (request.form['CID'])
		sql = "DELETE FROM CUSTOMER WHERE cust_id = %s"
		val = (DID,)
		cur.execute(sql,val)
		db.commit()
	except:
		return render_template('del.html',msg = "Cannot delete")
	return render_template('del.html',msg = "Successfully Deleted")


#to display the artist details
@app.route('/artist',methods = ['POST','GET'])
def artist():
	cur.execute("SELECT * FROM ARTIST")
	artist_details= cur.fetchall()
	x = len(artist_details)
	return render_template('artist.html',c = artist_details,z = x)

#to enter new artist go to newartist.html
@app.route('/gonewartist')
def gonewartist():
	return render_template('newartist.html')

#to enter a new artist
@app.route('/newartist',methods = ['POST', 'GET'])
def newartist():
	try:
		aname = (request.form['artist_name'])
		adob = (request.form['artist_dob'])
		astyle = (request.form['artist_style'])
		amail = (request.form['artist_email'])
		amob = (request.form['artist_mobNum'])
		aplace = (request.form['artist_place'])
		sql = """INSERT INTO ARTIST (artist_name,artist_dob,artist_style,artist_email,artist_mobNum,artist_place) VALUES(%s,%s,%s,%s,%s,%s)"""
		val = (aname,adob,astyle,amail,amob,aplace,)
		cur.execute(sql,val)
		db.commit()
	except:
		return render_template('newartist.html',msg = "Already Exists")
	return render_template('newartist.html',msg = "Successfully Registered")

#to delete an artist go to delartist.html
@app.route('/godelartist')
def deleartist():
	return render_template('delartist.html')

#to delete an artist
@app.route('/delartist',methods = ['POST', 'GET'])
def delartist():
	try:
		DID = (request.form['AID'])
		sql = "DELETE FROM ARTIST WHERE artist_id = %s"
		val = (DID,)
		cur.execute(sql,val)
		db.commit()
	except:
		return render_template('delartist.html',msg = "Cannot delete")
	return render_template('delartist.html',msg = "Successfully Deleted")


#to display the artworks details
@app.route('/artworks',methods=['POST','GET'])
def artworks():
	cur.execute("SELECT * FROM ART")
	artworks_details= cur.fetchall()
	x = len(artworks_details)
	return render_template('artworks.html',c = artworks_details,z = x)

#to enter new artworks go to newartworks.html
@app.route('/gonewartworks')
def gonewartwork():
	return render_template('newartworks.html')

#to enter a new artwork
@app.route('/newartworks',methods = ['POST', 'GET'])
def newartwork():
	try:
		aid = (request.form['art_id'])
		atitle = (request.form['art_title'])
		aartist = (request.form['art_artist'])
		aprice = (request.form['art_price'])
		atype = (request.form['art_type'])
		ayear = (request.form['art_year'])
		sql = """INSERT INTO ART (art_id,art_title,art_artist,art_price,art_type,art_year) VALUES(%s,%s,%s,%s,%s,%s)"""
		val = (aid,atitle,aartist,aprice,atype,ayear,)
		cur.execute(sql,val)
		db.commit()
	except:
		return render_template('newartworks.html',msg = "Already Exists")
	return render_template('newartworks.html',msg = "Successfully Registered")

#to search for an artwork by an artist 
@app.route('/search_artworks')
def search_artworks():
    return render_template('artistsearch.html')

#to filter out artists by artist name
@app.route('/by_artist', methods=['GET'])
def get_artworks_by_artist():
    artist_name = request.args.get('artist')
    try:
        # Call the stored procedure to get artworks by artist
        cur.callproc('GetArtworksByArtist', (artist_name,))
        artworks = cur.fetchall()
        print("Fetched Artworks:", artworks)
        return render_template('artist_artworks.html', artist_name=artist_name, artworks=artworks)
    except DBError as e:
        # Handle database errors
        print("Database Error:", e)
        return render_template('error.html', message="Database Error occurred.")

#to delete an artwork go to delartwork.html
@app.route('/godelartworks')
def deleartwork():
	return render_template('delartworks.html')

#to delete an artwork
@app.route('/delartworks',methods = ['POST', 'GET'])
def delartwork():
	try:
		ARTID = (request.form['AID'])
		sql = "DELETE FROM ART WHERE art_id = %s"
		val = (ARTID,)
		cur.execute(sql,val)
		db.commit()
	except:
		return render_template('delartworks.html',msg = "Cannot delete")
	return render_template('delartworks.html',msg = "Successfully Deleted")


#to display the orders details
@app.route('/orders',methods=['POST','GET'])
def orders():
    cur.execute("SELECT * FROM ORDERS")
    orders_details = cur.fetchall()
    x = len(orders_details)
    return render_template('orders.html', c=orders_details, z=x)

#to enter new orders go to neworders.html
@app.route('/goneworders')
def goneworder():
	return render_template('neworders.html')

#to place an order
@app.route('/neworders', methods=['POST', 'GET'])
def neworder():
    if request.method == 'POST':
        try:
            # Get form data
            cust_id = int(request.form['cust_id'])  # Ensure cust_id is an integer
            art_id = request.form['art_id']
            order_pay = request.form['order_pay']

            # Call the stored procedure to place the order
            cur.callproc('PlaceOrder', (cust_id, art_id, order_pay, 0))
            db.commit()

            # Get the result of the stored procedure
            cur.execute("SELECT @_PlaceOrder_3")
            result = cur.fetchone()[0]
            print(result)  # Check the result in your console

            if result == 1:
                msg1 = "Order placed successfully"
            else:
                msg1 = "Failed to place order. Please check customer and artwork IDs."

            return render_template('neworders.html', msg=msg1)

        except Exception as e:
            db.rollback()  # Rollback the transaction
            error_msg = "An error occurred: " + str(e)
            print("Error:", error_msg)
            return render_template('order_art.html', msg="An error occurred. Please try again later.")

    return render_template('neworders.html', msg="")

#to delete an order go to delorder.html
@app.route('/godelorders')
def deleorder():
	return render_template('delorders.html')

#to delete an order
@app.route('/delorders',methods = ['POST', 'GET'])
def delorder():
	try:
		OID = (request.form['OID'])
		sql = "DELETE FROM ORDERS WHERE ord_num = %s"
		val = (OID,)
		cur.execute(sql,val)
		db.commit()
	except:
		return render_template('delorders.html',msg = "Cannot delete")
	return render_template('delorders.html',msg = "Successfully Deleted")

#if admin it directs to admin signup page and there if username and password is correct it moves to nav-bar page
@app.route('/adminlogin/', methods=['GET', 'POST'])
def adminlogin():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # Print the username before the query
        print(f"Username from login form: {username}")

        cur.execute("SELECT admin_username, admin_password FROM artadmin WHERE admin_username = %s", (username,))
        admin_data = cur.fetchone()

        if admin_data:
            if admin_data[1] == password:
                session['loggedin'] = True
                msg = 'Logged in successfully'
                return render_template('nav-bar.html', msg=msg)
            else:
                msg = 'Incorrect password'
        else:
            msg = 'Admin username not found'

    return render_template('adminlogin.html', msg=msg)

'''CUSTOMER PART'''

#to customer login
@app.route('/clogin')
def cust_login():
	return render_template('customerlogin.html')

#to register new customer
@app.route('/newcust',methods = ['POST','GET'])
def newcust():
    try:
        cname = request.form['cust_name']
        caadhaar = request.form['aadhaar_num']
        cmail = request.form['cust_email']
        cmob = request.form['cust_mobNum']
        cplace = request.form['cust_place']

        # SQL query to insert a new customer
        sql = """INSERT INTO CUSTOMER (cust_name, cust_aadhar_num, cust_email, cust_mobNum, cust_place) 
                 VALUES (%s, %s, %s, %s, %s)"""
        val = (cname, caadhaar, cmail, cmob, cplace)

        # Execute the SQL query
        cur.execute(sql, val)
        db.commit()

        cur.execute("""
                    SELECT art_id, art_title, art_price, art_type, art_year, artist_name, artist_style 
                    FROM ART 
                    LEFT JOIN ARTIST 
                    ON ART.art_artist = ARTIST.artist_name
                """)
        art_details = cur.fetchall()
        x = len(art_details)
        return render_template('order_art.html', c=art_details, z=x)

        # Successful insertion

    except MySQLdb.IntegrityError as e:
        # Handle integrity error (unique constraint violation)
        db.rollback()  # Rollback the transaction
        error_msg = f"Error: {str(e)}"
        print("Integrity Error:", error_msg)
        return render_template('newcust.html', msg="Email already exists. Please use a different email.")

    except Exception as e:
        # Handle other exceptions
        db.rollback()  # Rollback the transaction
        error_msg = "An error occurred: " + str(e)
        print("Error:", error_msg)
        return render_template('newcust.html', msg="An error occurred. Please try again later.")

# Customer login for checking if email exists
@app.route('/exist_cust', methods=['POST', 'GET'])
def ex_cust():
    if request.method == 'POST':
        try:
            email = request.form['email']
            x = 0
            # Call the stored procedure to check if the email exists
            cur.callproc('CheckCustomerEmailExists', (email, x))

            # Fetch the result from the output parameter
            cur.execute("SELECT @_CheckCustomerEmailExists_1")
            result = cur.fetchone()[0]
            print(result)
            if result == 1:
                # If email exists, render the order_art.html template
                cur.execute("""
                    SELECT art_id, art_title, art_price, art_type, art_year, artist_name, artist_style 
                    FROM ART 
                    LEFT JOIN ARTIST 
                    ON ART.art_artist = ARTIST.artist_name
                """)
                art_details = cur.fetchall()
                x = len(art_details)
                return render_template('order_art.html', c=art_details, z=x)
            else:
                return render_template('exist_cust.html', msg="Email does not exist. Please register.")
        
        except Exception as e:
            # Handle exceptions
            print("Error:", e)
            return render_template('order_art.html', msg="An error occurred. Please try again later.")
    return render_template("exist_cust.html", msg="")

#to display the orders combining orders and art
@app.route('/orderdisplay',methods=['POST','GET'])
def ord_disp():
	cur.execute("SELECT O.cust_num,O.art_id,O.ord_num,O.ord_date,O.ord_payment,A.art_price FROM ORDERS O INNER JOIN ART A WHERE O.art_id = A.art_id")
	ord_details= cur.fetchall()
	x = len(ord_details)
	return render_template('orderdisplay.html',c = ord_details,z = x)

#to place new order
@app.route('/new_order', methods=['POST', 'GET'])
def new_order():
    if request.method == 'POST':
        try:
            # Get form data
            cust_id = int(request.form['cust_id'])  # Ensure cust_id is an integer
            art_id = request.form['art_id']
            order_pay = request.form['order_pay']

            # Call the stored procedure to place the order
            cur.callproc('PlaceOrder', (cust_id, art_id, order_pay, 0))
            db.commit()

            # Get the result of the stored procedure
            cur.execute("SELECT @_PlaceOrder_3")
            result = cur.fetchone()[0]
            print(result)  # Check the result in your console

            if result == 1:
                msg1 = "Order placed successfully"
            else:
                msg1 = "Failed to place order. Please check customer and artwork IDs."

            return render_template('new_order.html', msg=msg1)

        except Exception as e:
            db.rollback()  # Rollback the transaction
            error_msg = "An error occurred: " + str(e)
            print("Error:", error_msg)
            return render_template('order_art.html', msg="An error occurred. Please try again later.")

    return render_template('new_order.html', msg="")

#main begins
if __name__ == "__main__":
    app.run(debug = True, port = 8080)