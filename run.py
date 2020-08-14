from flaskblog import create_app

# u can pass any config in here (currently uses our default config)
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
