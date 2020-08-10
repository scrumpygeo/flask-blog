- pipenv shell

- pipenv install flask
- pipenv install email_validator
- pipenv install flask-wtf
- pipenv install flask-sqlalchemy

# 1. Start. Create flaskblog.py as the main app file and put this in it as basic:

```
      from flask import Flask, render_template

      @app.route('/')
      @app.route('/home')
      def home():
          return render_template('home.html')

      if __name__ == '__main__':
        app.run(debug=True)
```

- then make templates folder and put in home.html file with basic text for output.

- we run in debug mode so u don't have to keep stop/start the server every change.
  (-> set FLASK_DEBUG=1 in terminal doesnt work for me in pipenv but this does:)

```
            if __name__ == '__main__':
                app.run(debug=True)

```

    - NB to run, when u run pipenv shell and go to the url listed, usually localhost:5000

[
**Dummy Data**
Before getting to the db part we have dummy data to use for the forms.
This is in the main app and is like so:

```
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


```

]

# 2. Templates

- render_template
- url_for is so u can let flask decide where the path to the file is

next: https://www.youtube.com/watch?v=QnDWIZuWYW0&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=2

- template inheritance
  - block is a section child templates can overwrite.
    - `{% block content %} {% endblock %}`

```
jinja2 lets u put name of block in end as well so we do that to remind us what it's for. - here, content:

  {% extends "layout.html" % }
  {% block content %}
      {% for post in posts % }
      <h1>{{post.title}}</h1>
      <p>by {{post.author}} on {{post.date_posted}} </p></p>
      <p>{{post.content}} </p>
      {% endfor %}</p>
  {% endblock content %}

```

- add bootstrap
- any css etc go into static folder
- url_for function finds location of routes to static content like css for:
  `<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='main.css') }}" />`

snippets:
`https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog/snippets`

ch 3 `https://www.youtube.com/watch?v=UIJKdCIEXUQ`

# 3 FORMS AND USER INPUT

1. wt forms - flask-wtf - is most popular extension for working with forms in flask - handling validation etc.

- pipenv install flask-wtf
- pipenv install email_validator

2. create forms.py in root dir

- we will be writing python classes to represent the form and they will be automatically converted to html in the template.
- imported form fields will be classes too
- in `username = StringField('Username',`, the label is Username

- remember field lets people stay logged in even when browser shut via cookie
- secret key quards against modifying cookies, csrf etc: do in main app: flaskblog.py

  - good way of getting random chars is to go into python interpreter :

    ```
        import secrets
        secrets.token_hex(16)
         --> 92f27f2712769bfb901be18e43cbfa8e

      paste it into the SECRET_KEY thingy in flaskblog.py, the main app :
    ```

    - app.config['SECRET_KEY'] = '92f27f2712769bfb901be18e43cbfa8e'

  - import the forms into the main app: `from forms import RegistrationForm, LoginForm`

3. create routes for reg and login in main app

   - then create templates the routes refer to , eg registration.html & login.html
   - copy code from about page and paste it into the new pages to get started.
   - NB in form, if action="" then it posts to same route we are on
   - u can pass classes in via parent: `{{ form.username.label(class="form-control-label") }}`
     -NB in `<a href="{{ url-for('login')}}"` login refers to the function (the action) not the route

4. register form created. Ensure route has method=['GET', 'POST'] to allow those.
   - now we need to test if validation has occured ok & get and post requests working
   - in out app, at register route, after we create our form but b4 we create the template , check and return flash message if success:

```
            if form.validate_on_submit():
                    flash(f'Account created for {form.username.data}!', 'success')
                     return redirect((url_for('home'))

        NB 'success' is the bootstrap class u can add. This 2nd arg is called a category.
        -  then redirect user to different page

```

- then update layout.html template so flash messages appear on any page.- above block content part add:

```
            {% with messages = get_flashed_messages(with_categories=true) %}
              {% if messages %}
                {% for category, message in messages %}
                  <div class="alert alert-{{ category }}">
                    {{ message }}
                  </div>
                {% endfor %}
              {% endif %}
            {% endwith %}

```

5. above is flash for success. Now let em know when they screwed up.

- goto register.html template and within if block, if errors run field with class is-invalid:

```
                <div class="form-group">
                    {{ form.username.label(class="form-control-label") }}

                    {% if form.username.errors %}
                        {{ form.username(class="form-control form-control-lg is-invalid") }}
                        <div class="invalid-feedback">
                            {% for error in form.username.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>
                    {% else %}
                      {{ form.username(class="form-control form-control-lg") }}
                    {% endfor %}
                </div>
```

    - then copy above and paste over single line of each field below label then change field names to correct ones.

6. Login template: copy registration into it and modify.
   - add remember me field:

```
               <div class="form-check">
                    {{ form.remember(class="form-check-input") }}
                    {{ form.remember.label(class="form-check-label") }}
                </div>

```

    - add forgotten pwd link

- to test login page, add code to simulate user: goto login route in app add some fake data.

```
   form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.me' and form.password.data == '123456':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessfull', 'danger')
    return render_template('login.html', title="Login", form=form)

```

7. Change menu links to use url_for. in layout.html. eg `href="{{url_for('home')}}"`

`https://www.youtube.com/watch?v=cYWiDiIUxQc`

# 4. Database with Flask-SQLAlchemy

- to work with db in python we use sqlalchemy - a popular ORM, object relational mapper - lets us access db in an oo way, via classes aka models.
- this one lets u use many dbs and all u need to change is the db url you pass it.
- eg use sqlite for dev and for prod use postgresql
- pipenv install flask-sqlalchemy
- then in main app, `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'`
- 3 fwd slashes = relative path , ie in project dir we are in, here root.
- then create db instance: `db = SQLAlchemy(app)`
- classes (models) will later be put in separate files (next chapter) but for now we will keep em in the main app to avoid weird imports

- create User model via class User(db.Model), ie importing from db.Model

- dunder method aka magic method = how object is printed - we define what we want output to look like when we print out user object, eg:

```
      def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

Whole User model class is:

        class User(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(20), unique=True, nullable=False)
            email = db.Column(db.String(120), unique=True, nullable=False)
            image_file = db.Column(db.String(20), nullable=False,
                                  default='default.jpg')
            password = db.Column(db.String(60), nullable=False)
            posts = db.relationship('Post', backref='author', lazy=True)
                NB if  u have prob creating user change to lazy='dynamic'

            def __repr__(self):
                return f"User('{self.username}', '{self.email}', '{self.image_file}')"

```

    - next do Post class (Model)
    - NB with `default=datetime.utcnow` we don't have parentheses because we don't want time NOW but to pass in function to get the time when it's run

- Post and User models will have a 1 to many relationship

  - so in User model create a posts attribute:
    `posts = db.relationship('Post', backref='author', lazy=True)`

    - backref is like adding another column to Post model
    - lazy argument = when sqlalchemy loads data, True means load data as necessary in one go. Ths means that we can get all the posts created by a partic user.
    - this posts is not a physical column in db but an additional query running in background
    - then in Post model, add `user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)`

    - NB define relationhip with Post, capital P, because in User model we're referencing the Post class; while in foreign key in Post model the user.id has slower case u because we're referencing the table name & column name

- Now we have the strucs we can create the DB via cmd (within project dir and virtual thingy, ie in pipenv):

```
    >> from flaskblog import db
    >> db.create_all() # creates our db, visible in root dir

    Now add a user and a post via cmd & create instance

    >> from flaskblog import User, Post
    >> user1 = User(username='Fred', email='fred@blogs.me', password='123456')
    >> db.session.add(user1)    # this doesn't add to db but tells it we will. we can do several of these then do 1 add all at once
    >> db.session.commit()

    Now query db to check data in there:
    >> User.query.all()
          -->  [User('Fred', 'fred@blogs.me', 'default.jpg'), User('FWilmared', 'wilma@flintstone.me', 'default.jpg')]
    >> User.query.first()
    >> User.query.filter_by(username='Fred').all()     # [User('Fred', 'fred@blogs.me', 'default.jpg')]   nb in array
    >> User.query.filter_by(username='Fred').first()   # User('Fred', 'fred@blogs.me', 'default.jpg')  nb no array

    >> user = User('Fred', 'fred@blogs.me', 'default.jpg')   -put in var -> now we have access to extra attribs, eg type user.id

      user = User.query.get(1)  # gets same user

      user.posts    # returns []  ie empty

    Create some Posts
    -----------------

     post1 = Post(title='Blog1', content='This is an ordinary blog.', user_id=user.id)
     post2 = Post(title='Blog2', content='Here we go again.', user_id=user.id)
     - NB we created above post but not saved them yet (so no date posted for eg)

     db.session.add(post1)
     db.session.add(post2)
     db.session.commit()

     user.posts  should give array of posts for this user: `[Post('Blog1', '2020-08-08 14:39:15.613272'), Post('Blog2', '2020-08-08 14:39:15.616267')]`

    However since it's an array we can loop thru it:
    for post in user.posts:
      print(post.title)

    Directly query post table

    post = Post.query.first()
    post.user_id should then return user id

[ aside: to drop Posts table: `Post.__table__.drop(db.engine)`
        create single table: `Post.__table__.create(db.engine)`

]
  - backref="author" in the model lets us access it

  >> post.author    `returns this: User('Fred', 'fred@blogs.me', 'default.jpg')` ie the entire user object
```

Now lets delete all the data so in next chapter we start from scratch.

> > db.drop_all()
> > then create the db again
> > db.create_all()

So if you do User.query.all() and Post.query.all() then u should get [] back.

# -----

# 5. Package Structure

- restructure app as package instead of module
- usually start off all flask apps as packages; here he showed how to use module and how to convert.
- with packages imports can get weird.
- split model into separate file
- create models.py file in root & move models there; also add import of db and datetime
- import models into app from models.py
- -> error: when python imports something from a module it runs the entire module; at some point it doesn't know where something is due to **name** thing & referencing things another file hasn't imported yet.
- so we use packages to simplify the naming issues with imports
- to tell python st is a package create a `__init__.py` file:

- create new folder with same name as blog: flaskblog folder & in it create `__init__.py`
- move all of the files into the new folder except flashblog.py
- init file is where we initialize app and bring together different components:
  - from app, put the imports and where we instantiate db
  - put all the route info in the app file in their own module -> create routes.py in the package & put all the routes, relevant imports and dummy data there too.
- all that's left in main app is the app.run stuff; its only job is to run the app. So rename it to run.py and add `from flaskblog import app` which makes it import from the `__init__.py` file in the package.
- go into other files and clean up imports:
  - cut this `from flask import render_template, url_for, flash, redirect` into routes (from the init file, leaving just the import Flask on the top line)
  - move the `from forms import RegistrationForm, LoginForm` and `from models import User, Post` to the routes.py
  - prefix imports with flaskblog, eg `from flaskblog.models import User, Post` **which u do when importing from packages**
  - where using decorators, eg `@app.route` in routes, we need to `from flaskblog import app` to get @app in there
  - import routes into the `__init__.py` file, however u need to import it **AFTER** the initialization or u get circular import probs

**NB** where vscode automatically puts imports at top on save, add this `"python.formatting.autopep8Args": ["--ignore","E402"]` to editor settings, eg in `C:\Users\USERNAME\AppData\Roaming\Code\User\settings.json`

Next: `https://www.youtube.com/watch?v=CSHx6eCkmv0`

## 6. User Authentication

1. pipenv install flask-bcrypt

   - from flask_bcrypt import Bcrypt (in python shell)
   - bcrypt = Bcrypt() # instantiate
   - bcrypt.generate_password_hash('testing') --> `b'$2b$12$zCM4KJS8v8a3xw3UKusXsOXosfgNSe3CsD6VbiiPJiy1XqpxK9m.K'` where b means byte
   - to get it into string form, use:
     `hashed_pw = bcrypt.generate_password_hash('testing').decode('utf-8')` --> `$2b$12$hwXC9a0c2UhfUyrtQ/tbOuV5spx24n/4OA26n33th4pW7h5AIabe2`
   - NB these return different hashes even when repeated, so if stolen thief cant use
   - -> use a different method to check the pwd:
   - bcrypt.check_password_hash(hashed_pw, 'testing') ==> True

2. in `__init__.py`, `from flask_bcrypt import Bcrypt` then `bcrypt = Bcrypt(app)`
3. in routes.py, where flash says form valid on submit, create the a/c (make sure u import db, bcrypt)

   - `hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')`
   - `user = User(username=form.username.data, email=form.email.data, password=hashed_password)`
   - `db.session.add(user)`
   - `db.session.commit()`

4. We need to add front end validation so user doesnt register with existing name

   - go into forms.py
   - to RegistrationForm add:

```
  this is basic format of validation function:

      def validate_field(self, field):
        if True:
          raise ValidationError('Validation Message')

  actual eg:

      def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
          if user:
            raise ValidationError('That username is taken. Please choose another.')

```

    - and do same for email validation

5. Login
   - pipenv install flask-login # helps with user sessions
   - import into init: `from flask_login import LoginManager`
   - create instance: `login_manager = LoginManager(app)`
     - add functionality to our db model & manager handles all our sessions
   - goto models file
     - import login_manager: `from flaskblog import db, login_manager`
     - create function e decorator called user_loader

```
      @login_manager.user_loader
      def load_user(user_id):
          return User.query.get(int(user_id))


```

    - from flask_login import UserMixin   then passUserMixin to User class.
    - now the UserMixin & login_manager extensions can manage our sessions for us

6. modify login route (b4 we were checking hardcoded uname and pwd).

- in routes, import current_user extension so we can test if we logged in :

```
  add this to register & login routes:

    if current_user.is_authenticated:
        return redirect(url_for('home'))

```

7. create logout route

   - import logout_user
   - add logout to navigation template: layout.html

8. make it so if not logged in it takes u to login page if u try do something.

   - create account route: ``@app.route('/account')
   - create template for a/c: account.html
   - copy in the account template stuff to start
   - in navigation (in template) put menu link user will see if logged in, above the link for logout:
   - `<a class="nav-item nav-link" href="{{url_for('account')}}">Account</a>`
   - need to add a check to make sure user cant type /account in url otherwise he will not get the menu items:
   - use login_required decorator in routes:
     - add `@login_required` in line under `@app.route('/account')`
     - in init file, under login_manager line set login_manager route: `login_manager.login_view = 'login'`
       - if utype in /account, it will redirect u to login page if not logged it & to your page if u r
       - in init file add `login_manager.login_message_category = 'info'` which is bootstrap info alert blue color

9. if u try to access a page & ur not logged in it redirects u to login page. Then when u log in it takes u to account page. It would be nice for it to take u to the page uwanted to go to originally.

   - currently it has /login?next=%2Faccount in url when it tells u to log in. So access this query param & direct user there if it exists
   - `next_page = request.args.get('next')` - if u used args[0] it would throw an error if there were none, so instead use get() method - returns None if not exist

## 7. Edit User Account and Profile Picture

- finishing user account page for updating info & add ability to upload profile pic.

1. goto account.html template and add some jinja for username and email. then a link to the avatar imagewhich we set in routes
2. goto routes.py to account route at bottom & set image:
   - `image_file = url_for('static', filename='profile_pics/' + current_user.image_file )`
   - `return render_template('account.html', title="Account", image_file=image_file)`
   - now in template we can use image file as source: `<img class="rounded-circle account-img" src="{{ image_file }}">`
3. We want to allow update of info so we need forms: goto forms.py & copy registration form as a model.
   - nb wrt validation: if u check username is unique, it count's their current, so only check if they changed it
   - now add to route: in routes, create instance of the form, ie `form = UpdateAccountForm()` and pass it into the template via form=form, here:
   - `return render_template('account.html', title="Account", image_file=image_file, form=form)`
   - grab code from register.html template and use that modified into the account template
