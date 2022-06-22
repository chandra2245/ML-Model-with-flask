#FILE TO RUN TO LAUNCH THE APPLICATION

#IMPORTING THE APP
from Mendel import app

#CALLING THE APP IN DEBUGGING MODE
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
