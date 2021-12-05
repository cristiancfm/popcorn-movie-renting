from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 
    # if debugging is activated, changes to the code 
    # will rerun the webserver automatically