from flask import Flask, redirect, render_template, request, url_for
import MySQLdb

app = Flask(__name__)
app.config['DEBUG'] = True

hostname = 'localhost'
username = 'root'
password = 'root'
database = 'test'

students=[]

def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT reg_number, name FROM students" )
    del students[:]
    for reg_number, name in cur.fetchall() :
        student = [reg_number,name]
        students.append(student)





@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
		doQuery( myConnection )
		myConnection.close()

		return render_template('index.html', students = students)

	#return redirect(url_for('index'))

if __name__ == '__main__':
	app.run()