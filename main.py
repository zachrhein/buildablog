from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buildablog:buildablog@localhost:8889/buildablog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'GET':
        blogs = Blog.query.all()

    return render_template('/blog.html', blogs=blogs)

@app.route('/viewblog')
def viewblog():
    blog_id = int(request.args.get('id'))
    blog = Blog.query.get(blog_id)
    return render_template('/viewblog.html',blog=blog)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method =='POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_post = Blog(blog_title, blog_body)
        db.session.add(new_post)
        db.session.commit()
        return render_template('/viewblog.html', blog=new_post)
        
    
    return render_template('/newpost.html')


if __name__ == '__main__':
    app.run()
