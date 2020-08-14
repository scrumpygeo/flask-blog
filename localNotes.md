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
4. make it so editaccount form has data in it when it loads
   - go to routes.py : add `methods=['GET', 'POST']` account route
   - also add this to the route:

```
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
```

5. Changing profile picture

   - add new field to UpdateAccountForm
   - from flask_wtf.file import FileField, FileAllowed
   - picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) # where field label is in the ( )
   - then go to account.html template to add in the field:

```<div class="form-group">
                    {{ form.picture.label() }}
                    {{ form.picture(class="form-control-file") }}
                    {% if form.picture.errors %}
                        {% for error in form.picture.errors %}
                            <span class="text-danger">{{ error }}</span><br />
                        {% endfor %}
                    {% endif %}
                </div>

```

    - at top where we have `<form action="" method="POST">, ` **we need to add an encoding type** `enctype="multipart/form-data"`:
    - <form action="" method="POST" enctype="multipart/form-data">

    - NB with eg this, `f_name, f_ext = os.path.splitext(form_picture.filename)` we wont be using f_name so we can use `_` instead, (so editor won't complain about unused var): `_, f_ext = os.path.splitext(form_picture.filename)`
    - app.root_path gives us full path up to package dir (needs import os)

6. How to scale down image sizes automatically.

   - use package called Pillow pipenv install Pillow (capital P)
   - import into routes: `from PIL import Image`

## 8. Adding Posts

    - CRUD

1. Create route in routes file: /post/new, to render a template (which we create later). NB @login_required decorator
   - return render_template('create_post', title=New Post")
2. Create the template & to start paste in the about page code to extend layout.html etc., removing h1 tag text
   - template is to be a form for posting new posts
   - so create one in forms.py file called class PostForm(FlaskForm):
   - create instance of this form in the route via `form = PostForm()` & pass it into the create_post.html template via `form=form`
   - as we are letting a form post back to this route we need to accept a POST request: add `methods=['GET', 'POST']` to decorator
   - add usual conditionalsin routes to validate form when posted:`if form.validate_on_submit():` etc
   - add code to create_post.html template - copy across login template starting at 1st div that wraps the form
   - now add link in nav bar in layout.html
3. Now save posts to db and display on home page.
   - in routes, `post = Post(title=form.title.data, content=form.content.data, author=current_user)` - u can also use user_id instead of author, both acceptable; then do the db.session.add(post) and db.session.commit() -> post now added to db
   - now remove the dummy data we had at top of routes file
   - and at top, where we were passing dummy data to home template, add data from db: add this b4 render_template: `posts = Post.query.all()`
   - test it by making a post: turns out we were outputting user object instead of username. Also date is putting out time too. Also want to put user avatar next to post
   - home.html: we were printing out `{{ post.author }}` change to `{{ post.author.username }}`
   - to display just date (no time): as it's an object we can use strftime method: `{{ post.date_posted.strftime('%d-%m-%Y') }}`
   - to display user image: `<img class="rounded-circle article-img" src="{{ url_for('static', filename='profile_pics/' + post.author.image_file) }}" alt="">`

## At this it's working fine as a basic blog. There is always functionality to add tho' so we continue. Update and delete posts:

4. Create a route that takes us to a specific post page.

   - ie add id to route, eg `@app.route('/post/<int:post_id>')` where we specify the id as an integer
   - then function is def post(post_id):
   - then we can use this `post = Post.query.get(post_id)` **BUT** will instead use `get_or_404`: `post = Post.query.get_or_404(post_id)`
     - if u dont get post with that id u get 404: page doesnt exist.
     - `return render_template('post.html', title=post.title, post=post)`
   - now create the post.html template: copy from home.html and modify - get rid of for loop as there's only 1 post.
   - then on home.html, make sure link points to the post.html page: `<h2><a class="article-title" href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>`

5. Update Post

   - create route `@app.route('/post/<int:post_id>/update')` with def update_post(post_id):
   - needs @login_required
   - grab post as before and `if post.author != current_user:` then abort(403) : 403 is forbidden route - import from Flask
   - reuse form above: `form = PostForm()` and template similar to crate_post template.
   - we want title/content filled with existing data. Also form should say Update Post: pass in legend='Update Post' to the route (& add simlr to new post route: `legend="New Post"`)
   - and modify ceate_post.html to output legend above.
   - and under where we create the form add `form.title.data = post.title` and for content to populate the form

6. Add links to update and delete route to template (post.html)
   - for delete confirm use bootstrap modal
   - create delete_post route

## 9. PAGINATION &

- so we dont show too many posts at once => affecting performance; - Flask sqlalchemy has paginate method to help us do this
- also sort from newest to oldest

1. so add more posts from different users so we can see what pagination looks like
2. Flask sqlalchemy has paginate method to help us paginate.

   - Up to now query was like this:

```
          posts = Post.query.all()
          for post in posts:
            print(post)

    instead we can do:

          posts = Post.query.paginate()

          posts is now a pagination object with separate attributes & methods(do dir(posts) to see)

          posts.page tells u page ur currently on.
          posts.total - total nr pages in whole thing

          -- in cmd line in pipenv type python then >>> from flaskblog.models import Post
                                               then >>> posts = Post.query.paginate()
                                               then     dir(posts)
         - and u get  'has_next', 'has_prev', 'items', 'iter_pages', 'next', 'next_num', 'page', 'pages',
                      'per_page', 'prev', 'prev_num', 'query', 'total'

              then if u type >>> posts.per_page  u get 20, = default

    So to print out posts now u do

            for post in posts.items:
              print(post)

    for next page u do
          posts = Post.query.paginate(page=2)  & rerun the loop
```

    - if default of 20 is too much for page length, pass in per_page:
        - posts = Post.query.paginate(per_page=10)
        to get next page:
        - posts = Post.query.paginate(per_page=10, page=2)

3. in @app.route('/) for home page: replace `posts = Post.query.all()` with
   `posts = Post.query.paginate(per_page=5)`

   - we get the page nr we are at from the parameters (url):`page = request.args.get('page', 1, type=int)` where 1 is default page we set
   - type=int causes it to throw a value error if sb tries to put a non integer in.
   - now we pass the page into the query via page=page: `posts = Post.query.paginate(page=page, per_page=5)`

4. make change to home.html template & instead of `{% for post in posts %}` do `{% for post in posts.items %}`

   - now reload and we only have 5 posts on home page.
   - add `?page=2` to url to get page 2
   - update template so we can see links to other pages.
   - temporarily change per_page to =2 instead of 5 to give us more pages to play with.
   - for page in posts.iter_pages():
   - after the endfor, add another for loop then we check what page_num is, if it's a number put a link, if it says 'None' put an elipsis, ...
     - the elipsis is where u are not printing all the numbers (and correspond to 'None' in the code)
   - modify it so it shows fewer pages at bottom (hidden by elipses)
   - NB params to iter-pages: left_edge=1, right_edge=1 - how many pages show up on l and rhs
     - left_current=1, right_current=2 how many pages l and r of current show up
     - add another conditional to style current page differently: with filled in btn class: btn-info

5. put newer posts at top: goto routes, add `order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)` to Post.query line in home route

6. Build a route that will display posts from a partic user.
   - copy of home route with modifs
   - use home template as starting point to create user-posts template. Only diff is that it has heading saying whose page it is.
   - add this link to href in hom, post and user_posts templates `{{ url_for('post', post_id=post.id) }}` - make DRY in later video
   - in user_posts template we also need to change pagination links as they are no longer linking to home page. url_for() links to user_posts route; also pass in username.

## 10 - Email and Password Reset

    - generate secure time sensitive token for an individual
    - use itsdangerous
    - in idle:
        - `from itsdangerous import TimedJSONWebSignatureSerializer as Serializer`
        - s = Serializer('secret', 30)     # 30 sec expiration time
        - token = s.dumps({'user_id': 1}).decode('utf-8')
        - and run. if u type 'token' u get a big string back
        - to check if it's a valid method use loads() method as long as it's less thant 30" or whatever your exp time was:
        - s.loads(token)   # returns {'user_id': 1} ; wait too long and u get `Signature expired`

1. goto models.py and goto User model & `from itsdangerous import TimedJSONWebSignatureSerializer as Serializer`

   - we also need our app secret key so import `app`
   - create def get_reset_token(self, sec=1800):
   - create def verify_reset_token(token): but no expiry param; NB has @staticmethod to tell python not to expect self.

2. create route so user can reset pwd

   - need 2 new (v simple) forms:
     - i. class RequestResetForm(): ; also validate a/c exists for address
     - ii. class ResetPasswordForm(FlaskForm):

3. in routes.py, reset_password route

4. Create reset_request.html template & copy in login template code to start with and modify

5. create route where user actually resets pwd (as opposed to request to reset): def reset_token(token):

   - test token we get back is active
   - get this token from url

6. create reset_token.html template and paste in reset_request form stuff for modif.

7. What happens when we submit the above forms we've created (request for reset and actual reset.)

   - these forms return back to same route they submitted from.
   - -> add validate on submit conditional to our routes to handle form submission.

8. create empty function to create emails while he discusses what we need to do so: def send_reset_email(user):
   - install flask_mail: `pipenv install flask-mail`
   - in `__init__.py` add `from flask_mail import Mail` and also set some constants so app knows how to send mail:
     - this eg uses google mail but we can use any other :

```
  NB import os at top

      app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
      app.config['MAIL_PORT'] = 587
      app.config['MAIL_USE_TLS'] = True
      app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
      app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
      Mail(app)  # to initialize it

```

    - put email and password in environment variable to hide them - in windows env vars for eg.

    - now back to send_reset_email(user) method
    - `_external=True` is so we get an absolute url rather than a relative one.

9. add link to reset pwd page: login template

# 11 Blueprints

    - move config vars to their own files
    - create application factory: eg 1 app for prod and 1 for test

1. routes file too big with unrelated routes.

   - create new folder called users.
   - create another new folder called posts
   - create yetanother new folder called main as a catch all for the rest
   - make all the above 3 dirs to be **packages** as well, so each gets a `__init__.py` file, which can be empty.

2. within each of the above 3 packages we created we will makea routes.py file to only contain routes that deal with that package functionality

3. in users and posts packages we also want a forms.py file to keep forms separate.

4. in users package create utils.py file for odds and ends re users eg reset pwd stuff.

5. start adding stuff to users/route. No longer using global @ var to create the routes. Create it specifically for this blueprint and register it at a later time.

   - so instead of @app.route decorator in the users route, we have users instantiated at top and user @users.route instead.

   - repeat for post package routes decorator and again for main package.
   - all that's left in the old routes file are the imports which we will clean up later

6. repeat above for our forms. Most goes into users/form and one goes into posts/form. Then delete the old routes and forms files

7. goto application's `__init__.py` file, replace the old `from flaskblog import routes` with: `from flaskblog.users.routes import users`
   - then register with `app.register_blueprint(users)`
   - now repeat with the other blueprints: posts, main

```

```
