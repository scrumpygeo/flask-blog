from flask import Flask, render_template
app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
