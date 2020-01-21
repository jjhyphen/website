from flask import Flask, render_template, redirect, url_for, request,session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import MySQLdb

'''from models import Album, Artist
from tables import Results
from app import app
from db_setup import init_db, db_session
from forms import MusicSearchForm, AlbumForm'''


app = Flask(__name__)

app.secret_key = "allthelettersofthealphabet"


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'anki@123janvi'
app.config['MYSQL_DB'] = 'pythonregister'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql=MySQL(app)
#init_db()


mysql = MySQL()
conn = MySQLdb.connect("localhost","root","anki@123janvi","pythonregister" )
cursor = conn.cursor()
cursor2=cursor
'''@app.route('/insert/', methods=['GET', 'POST'])
def insert():
    if request.method == "POST":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        book = request.form['book']
        author = request.form['author']
        cursor.execute("INSERT INTO books (name, author) Values (%s, %s)", [book, author])
        conn.commit()
        return redirect("http://localhost:5000/search/", code=302)
    return render_template('insert.html')
'''
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
    
        conn = MySQLdb.connect("localhost","root","anki@123janvi","pythonregister" )
        cursor = conn.cursor()
        book = request.form['book']
        query= "SELECT name,author,id FROM books WHERE name = %s or author = %s"
        cursor.execute(query,[book,book])
        data = cursor.fetchall()
        conn.close()
        return render_template('search22.html',data=data)
    return render_template('search22.html')
    
@app.route('/userlogin/',methods=["GET","POST"])
def userlogin():
    msg= ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', [username,password])
        login = cursor.fetchone()
       
        if login:
            session['loggedin'] = True
            session['id'] = login['uid']
            session['username'] = login['username']
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        
        else:
             msg = 'Incorrect username/password!'
    elif 'loggedin' in session:
        msg = 'You have already logged in. PLease log out'
    return render_template('userlogin.html', msg=msg) 

@app.route('/adminlogin/',methods=["GET","POST"])
def adminlogin():
    msg= ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', [username,password])
        login = cursor.fetchone()
       
        if login:
            session['adminloggedin'] = True
            session['id'] = login['id']
            session['username'] = login['username']
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        
        else:
             msg = 'Incorrect username/password!'
    elif 'loggedin' in session or 'adminloggedin' in session:
        msg = 'You have already logged in. PLease log out'
    return render_template('adminlogin.html', msg=msg)

@app.route('/login/',methods=["GET","POST"])
def login():
    if 'loggedin' in session or 'adminloggedin' in session:
        return redirect(url_for('home'))
    return render_template('login.html')
@app.route('/logre/',methods=["GET","POST"])
def logre():
    return render_template('logre.html')
'''@app.route('/search/', methods=['GET', 'POST'])
def Search():
    search = MusicSearchForm(request.form) 
    if request.method == 'POST':
        return search_results(search)

    return render_template('Search.html', form=search)


@app.route('/results/')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Artist':
            qry = db_session.query(Album, Artist).filter(
                Artist.id==Album.artist_id).filter(
                    Artist.name.contains(search_string))
            results = [item[0] for item in qry.all()]
        elif search.data['select'] == 'Album':
            qry = db_session.query(Album).filter(
                Album.title.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'Publisher':
            qry = db_session.query(Album).filter(
                    Album.publisher.contains(search_string))
            results = qry.all()
        else:
            qry = db_session.query(Album)
            results = qry.all()
    else:
        qry = db_session.query(Album)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)


@app.route('/new_album/', methods=['GET', 'POST'])
def new_album():
    
    form = AlbumForm(request.form)

    if request.method == 'POST' and form.validate():
        
        album = Album()
        save_changes(album, form, new=True)
        flash('Album created successfully!')
        return redirect('/')

    return render_template('new_album.html', form=form)


def save_changes(album, form, new=False):
    
    artist = Artist()
    artist.name = form.artist.data

    album.artist = artist
    album.title = form.title.data
    album.release_date = form.release_date.data
    album.publisher = form.publisher.data
    album.media_type = form.media_type.data

    if new:
    
        db_session.add(album)

    
    db_session.commit()


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    qry = 'SELECT * FROM books WHERE id=%s'
    cursor.execute(qry,[id])
    data = cursor.fetchall()
    
    
    
    if request.method =='POST':
        qry = 'DELETE FROM books WHERE id=%s'
        cursor.execute(qry,[id])
        conn.commit()
        qry = 'SELECT * FROM books'
        cursor.execute(qry,)
        data=cursor.fetchall()
        return redirect(url_for('books', value=data))

    return render_template('example.html', value=data)

'''
@app.route('/deletebooks/<id>', methods=['GET', 'POST'])
def delete(id):
    qry = 'SELECT * FROM books WHERE id=%s'
    cursor.execute(qry,[id])
    data = cursor.fetchall()
    
    
    
    if request.method =='POST':
        qry = 'DELETE FROM books WHERE id=%s'
        cursor.execute(qry,[id])
        conn.commit()
        qry = 'SELECT * FROM books'
        cursor.execute(qry,)
        data=cursor.fetchall()
        return redirect(url_for('books', value=data))

    return render_template('deletebooks.html', value=data)

@app.route('/deletemovies/<id>', methods=['GET', 'POST'])
def deletemovies(id):
    qry = 'SELECT * FROM movies WHERE id=%s'
    cursor.execute(qry,[id])
    data = cursor.fetchall()
    
    
    
    if request.method =='POST':
        qry = 'DELETE FROM movies WHERE id=%s'
        cursor.execute(qry,[id])
        conn.commit()
        qry = 'SELECT * FROM movies'
        cursor.execute(qry,)
        data=cursor.fetchall()
        return redirect(url_for('movies', value=data))

    return render_template('deletemovies.html', value=data)

@app.route('/deletemusic/<id>', methods=['GET', 'POST'])
def deletemusic(id):
    qry = 'SELECT * FROM music WHERE id=%s'
    cursor.execute(qry,[id])
    data = cursor.fetchall()
    
    
    
    if request.method =='POST':
        qry = 'DELETE FROM music WHERE id=%s'
        cursor.execute(qry,[id])
        conn.commit()
        qry = 'SELECT * FROM music'
        cursor.execute(qry,)
        data=cursor.fetchall()
        return redirect(url_for('music', value=data))

    return render_template('deletemusic.html', value=data)


@app.route('/displaybooks/<id>')
def displaybooks(id):
    qry = 'SELECT * FROM books WHERE id=%s'
    cursor.execute(qry,[id])
    data = cursor.fetchall()
    conn.commit()
    return render_template('displaybooks.html', value=data)



@app.route('/profile/')
def profile():
    if 'loggedin' in session:
       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE uid = %s', [session['id']])
        account = cursor.fetchone()
       
        return render_template('profile.html',account=account)
   
    return redirect(url_for('home'))

    
@app.route('/admin/', methods=['GET','POST'])
def admin():
    if 'adminloggedin' in session:
            return render_template('elay.html')
    else:
        return redirect(url_for('home'))
        

@app.route('/books/', methods=['GET',"POST"])
def books():
    conn = MySQLdb.connect("localhost","root","anki@123janvi","pythonregister" )
    cursor = conn.cursor()
    query = "SELECT * from books"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return render_template('books.html',value=data)
@app.route('/addbooks/', methods=['GET',"POST"])
def addbooks():
   
    if request.method == 'POST' and 'name' in request.form and 'author' in request.form and 'publisher' in request.form and 'year' in request.form and 'description' in request.form:
        
       name = request.form['name']
      
       author = request.form['author']
       publisher = request.form['publisher']
       year = request.form['year']
       description = request.form['description']
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM books WHERE name = %s', [name])
       check=cursor.fetchone()
       if check:
           flash('This book has already been  added....')   
       else:
           
           cursor.execute('INSERT INTO books VALUES (%s, %s,%s,%s,%s,NULL)', [name, author,publisher, year,description])
           mysql.connection.commit()
           return redirect(url_for('books'))
    
    return render_template('addbooks.html')

    
    
@app.route('/music/', methods=['GET',"POST"])
def music():
    conn = MySQLdb.connect("localhost","root","anki@123janvi","pythonregister" )
    cursor = conn.cursor()
    query = "SELECT * from music"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return render_template('music.html',value=data)
@app.route('/addmusic/', methods=['GET',"POST"])
def addmusic():
    
    if request.method == 'POST' and 'name' in request.form and 'musicianband' in request.form and 'album' in request.form and 'year' in request.form and 'description' in request.form:
        
       name = request.form['name']
      
       musicianband = request.form['musicianband']
       album = request.form['album']
       year = request.form['year']
       description = request.form['description']
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM music WHERE name = %s', [name])
       check=cursor.fetchone()
       if check:
           flash('This piece has already been  added....')   
       else:
           
           cursor.execute('INSERT INTO music VALUES (%s, %s,%s,%s,%s,NULL)', [name, musicianband,album, year,description])
           mysql.connection.commit()
           return redirect(url_for('music'))
    
    return render_template('addmusic.html')



@app.route('/movies/', methods=['GET',"POST"])
def movies():

    conn = MySQLdb.connect("localhost","root","anki@123janvi","pythonregister" )
    cursor = conn.cursor()
    query = "SELECT * from movies"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return render_template('movies.html',value=data)
@app.route('/addmovies/', methods=['GET',"POST"])
def addmovies():
    
    if request.method == 'POST' and 'name' in request.form and 'director' in request.form and 'year' in request.form and 'description' in request.form:
        
       name = request.form['name']
      
       director = request.form['director']
       
       year = request.form['year']
       description = request.form['description']
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM movies WHERE name = %s', [name])
       check=cursor.fetchone()
       if check:
           flash('This film/movie has already been  added....')   
       else:
           
           cursor.execute('INSERT INTO movie VALUES (%s, %s,%s,%s,%s,NULL)', [name, director, year,description])
           mysql.connection.commit()
           return redirect(url_for('movies'))
    
    return render_template('addmovies.html')


@app.route('/logout/', methods = ['GET','POST'])
def logout():
    if 'loggedin' in session: 
        session.pop('loggedin')
        session.pop('id')
        session.pop('username')
        return redirect(url_for('home'))
    if 'adminloggedin'in session:
        session.pop('adminloggedin')
        session.pop('id')
        session.pop('username')
        
    return redirect(url_for('home'))


@app.route('/register/', methods=["GET","POST"])
def register():
    msg = ''
    if 'loggedin' in session:
       msg = 'You have logged in already. Why would you register again?'
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'confirm' in request.form and 'email' in request.form:
       username = request.form['username']
       password = request.form['password']
       confirm = request.form['confirm']
       email = request.form['email']
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM users WHERE username = %s', [username])
       register = cursor.fetchone()
       
       if register:
            msg = 'Account already exists!'
       elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
       elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
       elif not username or not password or not email:
            msg = 'Please fill out the form!'
       elif confirm!=password:
            msg = 'The passwords do not match ' 
       else:
         
            cursor.execute('INSERT INTO users VALUES (NULL,%s, %s, %s)', [username, password, email])
            mysql.connection.commit()
            flash('You have successfully registered! Thank you for registering.')
            return redirect(url_for('home'))
    elif request.method == 'POST':
            msg = 'Please fill out the form!'
   
    
    return render_template('REGISTER2.html', msg=msg)

		 
if __name__ == '__main__':
    app.run()