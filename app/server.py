from app import app

from app.controllers import home, characters, items



if __name__=="__main__":   
    app.run(debug=True) 