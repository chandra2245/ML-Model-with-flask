#CODE FOR MANAGING APP,DATABASE CONFIGURATIONS AND ALL THE ROUTING


#IMPORTING THE REGQUIRED LIBRARIES
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy





#LOCAL PATH FOR THE DATA UPLOAD
UPLOAD_FOLDER = 'Mendel/uploads/'





#FLASK '__name__' VARIABLE INITIALIZATION 
app = Flask(__name__)




#APP CONFIGURATIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY']='5775df32c0f6472dae977b0c5625e030'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'




#DATABASE CONFIGURATIONS
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'





#IMPORT THE VARIOUS ROUTING PATHS
from Mendel.urlroutes.main.routes import main
from Mendel.urlroutes.targetdefinition.routes import targetdefinition
from Mendel.urlroutes.datainput.routes import datainput
from Mendel.urlroutes.ranking.routes import ranking
from Mendel.urlroutes.account.routes import account
from Mendel.urlroutes.territory.routes import territory
from Mendel.urlroutes.data.routes import data
from Mendel.urlroutes.hcp.routes import hcp




#REGISTERING THE ROUTES WITH THE APP
app.register_blueprint(main)
app.register_blueprint(targetdefinition)
app.register_blueprint(datainput)
app.register_blueprint(ranking)
app.register_blueprint(account)
app.register_blueprint(territory)
app.register_blueprint(data)
app.register_blueprint(hcp)