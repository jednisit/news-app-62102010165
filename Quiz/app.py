from flask import Flask,render_template,request,redirect
from models import db,Books

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/')
def index():
    all_book = Books.query.all()
    return render_template('index.html',data = all_book,title="Index")
    

@app.route('/view/<int:id>')
def viewByID(id):
    book = Books.query.filter_by(id=id).first()
    if book :
        return render_template('view.html',data = book,title="View")
    return "Book with id = {0} Does not exits".format(id)


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    book = Books.query.filter_by(id=id).first()
    if request.method == 'POST':
        if book:
            db.session.delete(book)
            db.session.commit()

            title = request.form['title']
            author = request.form['author']
            genre = request.form['genre']
            heigh = request.form['heigh']
            publisher = request.form['publisher']

            book = Books(id=id,title=title,author=author,genre=genre,heigh=heigh,publisher=publisher)
            db.session.add(book)
            db.session.commit()
            return redirect(f'/view/{id}')
        else:
            return "Book with id = {0} Does not exits".format(id)
    return render_template('update.html', data = book,title="Update")

@app.route('/insert', methods=['GET','POST'])
def insert():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        heigh = request.form['heigh']
        publisher = request.form['publisher']

        book = Books(title=title,author=author,genre=genre,heigh=heigh,publisher=publisher)
        db.session.add(book)
        db.session.commit()
        return redirect(f'/')
    return render_template('insert.html',title="Insert")

@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    book = Books.query.filter_by(id=id).first()
    if request.method == 'POST':
        if book:
            if request.form['conf_yes'] == "YES":
                db.session.delete(book)
                db.session.commit()

                return redirect(f'/')

            return redirect(f'/view/{id}')

        return "Book with id = {0} Does not exits".format(id)

    return render_template('delete.html',data=id,title="Delete")




if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)