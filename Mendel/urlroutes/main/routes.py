#HOME PAGE AND LOGIN PAGE OF THE TOOL 


#IMPORT ALL THE REQUIRED LIBRARIES
from Mendel.models import User
from Mendel.urlroutes.main.forms import LoginForm
from flask_login import login_user, current_user, logout_user    
from flask import render_template,  flash, redirect, url_for, Blueprint





#CREATING THE BLUE PRINT VARIABLE FOR THE MAIN FOR ROUNTING 
main = Blueprint('main', __name__)




#ROUTE FOR THE HOME URL
@main.route("/")
@main.route("/home")
#ROUTE FOR HOME TAB                              
def home():
    return render_template('home.html')



#ROUTE FOR LOGIN PAGE
@main.route("/login", methods=['GET', 'POST'])
def login():
    #user authentication
    if current_user.is_authenticated:
        #if the user is already logged in then redirect
        flash('User already logged in', 'danger')
        
        #if the logged in user is a manager then redirect to target definition
        if current_user.user_type=='admin':
            return redirect(url_for('data.dataurl'))
        
        #if the logged in user is a sales rep then redirect to data input tab
        if current_user.user_type=='sales_rep':
            return redirect(url_for('datainput.datainputurl'))
        
    #if the user is not logged then POST request   
    form = LoginForm()
    
    #login username and password validations
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        #if the credentials were correct
        if user and (user.password== form.password.data):
            login_user(user)
            flash('Login Successfull', 'success')
            
            #if the logged in user is a manager then redirect to target definition
            if current_user.user_type=='admin':
                return redirect(url_for('data.dataurl'))
            
            #if the logged in user is a sales rep then redirect to data input tab
            if current_user.user_type=='sales_rep':
                return redirect(url_for('datainput.datainputurl'))
        
        #if the credentials were not correct
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    #rendering the html template as GET request 
    return render_template('login.html', title='Login', form=form)


#ROUTE FOR LOGOUT FUNCTIONALITY, WHEN THE LOGOUT BUTTON IS CLICKED
@main.route("/logout")
def logout():
    logout_user()
    flash('Logout Successfull', 'info')
    return redirect(url_for('main.login'))


	
	