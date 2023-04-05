from flask import Flask, render_template,request,redirect,session,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json



#--------------------------------------------------------------


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db';    #using sql-alchemy to connect to database.
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)
app.secret_key='super-secret-key'   

with open('config.json','r') as c:                         #just taken the variable which are constant in program in config file for simplicity. Opne config file in read mode.
    params=json.load(c)["params"]



#--------------------------------------------------------------


# Making a class to give configuration of database connection.To store the data in sqlite database.
class Todo(db.Model):
    sno= db.Column(db.Integer, primary_key="True")
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:                      #inbuit func to represent obj as string
        return f"{self.sno} - {self.title}"





#--------------------------------------------------------------
#Making the End points 

@app.route('/' , methods=['GET','POST'])
def hello_world():

    
    if request.method=='POST':                #CASE : 1 when we have a POST request to this method (ie to input todo and save it on database ).
       #print(request.form['title'])
      title=request.form['title']
      desc=request.form['desc']
                                              #Now making obj of todo to save on database
      todo=Todo(title=title,desc=desc)        #setting the form entered data into the Todo class.
      db.session.add(todo)                    #adding the the todo object to db and then commiting.
      db.session.commit()    
    #   flash("Todo added to the List ","success")
      return redirect("/")                    #used to redirect to home page of app

        

    #-----else condition for GET request.     # CASE 2 : when we have normal get request to fetch all the todo lists and just display them on html page.
                
    allTodo=Todo.query.all()                  #Fetching the all entries from database
    #print(allTodo)
    if( 'username' not in session ):          #Checking if user is logged in or Not  , if not redirect to login page
        return render_template('login.html',allTodo=allTodo)  
    
    
    return render_template('index.html' , allTodo=allTodo)   #render_template is used to show the html page and passed the allTodo objects to show in html page. 




#--------------------------------------------------------------
# Making the end points.  Login page url  

@app.route('/dashboard/',methods=['GET','POST'])
def dashboard():

    #if user is already login (username set in session) , directly give access inside website
    if ('username' in  session and session['username']== params['admin_user'] ) :
        allTodo=Todo.query.all()
        return redirect('/')
    

    if request.method=='POST':
        #redirect to Admin pannel / inside the project , if below code is successfull, Fetching values of Login Form to match with existing admin data in the config.json file.
        username=request.form.get('username')     
        password=request.form.get('password')
        
        if(username==params['admin_user'] and password== params['admin_password'] ):
               #set the session variable
               session['username']=username 
               allTodo=Todo.query.all()                   #Fetch all the Todos and send it as argument to display them in index.html
               return render_template('index.html',allTodo=allTodo)
    
    #GET Request :    
    #OTherwise- show the same login page again , if wrong request / wrong credentials
    allTodo=Todo.query.all()
    return render_template('login.html')

#_________________________________
@app.route('/logout/')
def logout():
    session.pop('username',None)                       #remove the username from session and show the login page again.
    return render_template('login.html')



#_________________________________

#--------------------------------------------------------------


@app.route('/show/')
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return 'Displays the List of todos only. We can make html page , and point it to this end point if required.'

#--------------------------------------------------------------
@app.route('/instruction/')
def instructionspage():
    return render_template('instruction.html')

#--------------------------------------------------------------
@app.route('/about/')
def aboutpage():
    return render_template('about.html')

#--------------------------------------------------------------
#UPDATE - End Point


@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':               #CASE 1 : when method is called with post request . We need to fetch the updated fields from the update form
        title=request.form['title']
        desc=request.form['desc']
                                             #setting the updated data in todo object.
        todo=Todo.query.filter_by(sno=sno).first()          #Fetching the current todo object. then setting its field with updated values.
        todo.title=title
        todo.desc=desc
        db.session.add(todo)                                  #adding the updated todo in database object and commit it to save the changes in file.
        db.session.commit()
        return redirect("/")                                  # redirect to home/index page , as get request so all the todos will be shown in index page. 


   #CASE 2 : If method is called by get request , just filter out the todo object and show the update.html page.
    #This is for showing the Update page , when the update button is clicked. Also fetching the current todo and sending it in argument .So we can old values in field of update form
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)


#--------------------------------------------------------------

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")                                               #redirect to index page (with get request by default).
    
#--------------------------------------------------------------



# TO run the app , and debug=True show errors if they come.
if __name__=="__main__":
    app.run(debug=True, port=8000)
   




#TO view the database file we can use the SQLite Viewer and opne our todo.db file in it. (Refer notes how to create the db file for Sqlite database)   