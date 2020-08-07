from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '92f27f2712769bfb901be18e43cbfa8e'

# Dummy data:
posts = [
    {
        'author': 'Fred Blogs',
        'title': 'Post 1',
        'content': 'first one',
        'date_posted': 'April 20, 2020'
    },
    {
        'author': 'Wilma Baggins',
        'title': 'Post 2',
        'content': 'first 2nd',
        'date_posted': 'April 22, 2020'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title="Register", form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title="Login", form=form)


if __name__ == '__main__':
    app.run(debug=True)
