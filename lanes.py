from flask import Flask, render_template, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lanes.db'
db = SQLAlchemy(app)

class Lanes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.String, unique=True, nullable=False)
    teller = db.Column(db.String, nullable=False)
    
    app.app_context().push()
    
    def __repr__(self):
        return f'Line {self.id}'
    
@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        lane = request.form["line"]
        said_by = request.form["owner"]
        new_line = Lanes(line=lane, teller=said_by)
        try:
            db.session.add(new_line)
            db.session.commit()
            return redirect ("/")
        except:
            flash("Unable to add the line")
    else:
        lines = Lanes.query.order_by(Lanes.id)
        return render_template('lines.html', lines=lines)

if __name__ == '__main__':
    app.run(debug=True)
    