from flask import Flask,render_template, request, url_for, jsonify, json, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from hashids import Hashids
hash=Hashids()
padding=100000000
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB/database.db'
db = SQLAlchemy(app)
class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, unique=True)  
    def __init__(self, data):
        self.data = data  
    def __repr__(self):
        return '<data :{}>'.format(self.data)


def id_uid(id):    
    uid=hash.encrypt(id+padding)
    return uid
def uid_id(uid):
    id=hash.decrypt(uid)[0]-padding
    return id

@app.route('/gallery/<uid>')
def show(uid):
    id=uid_id(uid)
    data=Album.query.filter_by(id=id).first().data
    title,html=build_html(data)    
    return render_template('index.html',html=html,title=title)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data=request.get_json(force=True)
        album=Album(json.dumps(data['data']))
        db.session.add(album)
        db.session.commit()
        id=album.id
        uid=id_uid(id)
    return url_for('show',uid=uid,_external=True)

def template(active,link,index):
    return  """ <div class="item{0}">
                    <div class="cap">
                        <h3>image no.{2}</h3>                           
                        <p><a href="{1}">{1}</a></p>
                    </div>
                    <img src="{1}" alt="{1}" href={1}>

                </div>""".format(active,link,index)

def build_html(data):
    payload=json.loads(data)
    title=payload['title']
    links=payload['links']
    html=''.join((template(' active',link,index) if index==1 else template('',link,index) for index,link in enumerate(links,start=1)))
    return title,html


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')


