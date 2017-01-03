from flask import render_template
from flask import Flask
from flask import session
from flask import request
import os
import random
import shelve

app = Flask(__name__)
app.secret_key= os.urandom(24)

@app.route('/registro.html',methods=['GET','POST'])
def registro():
	db = shelve.open('base_datos.bd', writeback=True) 
	if request.method== 'POST':		
		db[str(request.form['email'])]=[str(request.form['pass']),str(request.form['nombre'])]
		session['email']=str(request.form['email'])
		session['pass']=str(request.form['pass'])
		session['page']= []
		return render_template('index.html',loggedIn=True, email=session['email'],password=session['pass'],page=session['page'])
		db.close()
		
	return render_template('registro.html',loggedIn=False)
	
@app.route('/',methods=['GET','POST'])
def index():
	db = shelve.open('base_datos.bd', writeback=True) 
	if request.method== 'POST':
		flag = db.has_key(str(request.form['email']))
		if flag==True:
			if str(request.form['pass']) in db[str(request.form['email'])]:
				session['email']=str(request.form['email'])
				session['pass']=str(request.form['pass'])
				session['page']= []
				session['name']=db[str(request.form['email'])][1]
	
	if('email' in session)and('pass' in session):		
		session['page']=["index.html"]+ session['page'][0:]
		return render_template('index.html',loggedIn=True, email=session['email'],password=session['pass'],page=session['page'],name=session['name'])
	else:
		return render_template('index.html',loggedIn=False)

@app.route('/cerrar_sesion',methods=['GET'])	
def logout():
		session.pop('email',None)
		session.pop('pass',None)
		return render_template('index.html',loggedIn=False)
		
@app.route('/index.html')
def index2():
	if('email' in session)and('pass' in session):
		session['page']=["index.html"]+ session['page'][0:]
		return render_template('index.html',loggedIn=True, email=session['email'],password=session['pass'],page=session['page'],name=session['name'])
	else:
		return render_template('index.html')
	
@app.route('/burger.html')
def menu():
	if('email' in session)and('pass' in session):
		session['page']=["/burger.html"] + session['page'][0:]
		#session['page'].insert(0,str('/burger.html'))
		return render_template('burger.html',loggedIn=True, email=session['email'],password=session['pass'],page=session['page'],name=session['name'])
	else:
		return render_template('burger.html',loggedIn=False)
	
@app.route('/about.html')
def about():
	if('email' in session)and('pass' in session):
		session['page']=["about.html"]+ session['page'][0:]
		return render_template('about.html',loggedIn=True, email=session['email'],password=session['pass'],page=session['page'],name=session['name'])
	else:
		return render_template('about.html',loggedIn=False)	
	
@app.route('/blog.html')
def blog():
	if('email' in session)and('pass' in session):
		session['page']=["blog.html"]+ session['page'][0:]
		return render_template('blog.html',loggedIn=True, email=session['email'],password=session['pass'],page=session['page'],name=session['name'])
	else:
		return render_template('blog.html',loggedIn=False)

@app.route('/contact.html')
def contact():
	if('email' in session)and('pass' in session):
		session['page']=["/contact.html"] + session['page'][0:]
		return render_template('contact.html',loggedIn=True, email=session['email'],password=session['pass'],page=session['page'],name=session['name'])
	else:
		return render_template('contact.html',loggedIn=False)

@app.route('/datos_personales.html',methods=['GET','POST'])
def datos():
	db = shelve.open('base_datos.bd', writeback=True) 
	if request.method== 'POST':
		print ("hola")
		db[str(request.form['email'])]=[str(request.form['pass']),str(request.form['nombre'])]			
		session['email']=str(request.form['email'])
		session['pass']=str(request.form['pass'])
		session['name']=db[str(request.form['email'])][1]
		session['page'].insert(0,str('/datos_personales.html'))
		return render_template('datos_personales.html',loggedIn=True, email=session['email'],password=session['pass'],page=session['page'],name=session['name'])
		
	if('email' in session)and('pass' in session):
		session['page']=["datos_personales.html"]+ session['page'][0:]
		return render_template('datos_personales.html',loggedIn=True, email=session['email'],password=session['pass'],page=session['page'],name=session['name'])
				
	else:
		return render_template('datos_personales.html',loggedIn=False)
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
	
if __name__ == "__main__":
	#app.debug = false
	#app.run(host='0.0.0.0')
	#port=int(os.environ.get('PORT',5000))
	#app.run(host='0.0.0.0', port=port)

    	app.run(host='0.0.0.0', port='80')
