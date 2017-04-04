from flask import Flask, redirect, render_template, request, url_for
import MySQLdb

app = Flask(__name__)
app.config['DEBUG'] = True

hostname = 'localhost'
username = 'root'
password = 'root'
database = 'test'

students=[]

def getStudents( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT reg_number, name FROM students" )
    del students[:]
    for reg_number, name in cur.fetchall() :
        student = (reg_number,name)
        students.append(student)

def insertStudent(conn, reg_number, name):
	cur = conn.cursor()
	cur.execute("insert into students (reg_number, name) values (%s, %s)", (reg_number, name))
	conn.commit()

def deleteStudent(conn, name):
	cur = conn.cursor()
	cur.execute("delete from students where name = %s", (name,))
	conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
	myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )

	if request.method == 'GET':
		getStudents( myConnection )
		myConnection.close()

		return render_template('index.html', students = students)
	else:
		reg_number = request.form['reg_number']
		name = request.form['name']
		if reg_number  and name:
			insertStudent(myConnection, reg_number, name)
			myConnection.close()

		return redirect(url_for('index'))

@app.route('/delete/<name>')
def delete(name):
	myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
	deleteStudent(myConnection, name)
	myConnection.close()

	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run()