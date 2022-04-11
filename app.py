from flask import request, Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import datetime
from werkzeug.utils import secure_filename
import re
# import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secerttodo'
CORS(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    roll = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True,)
    phoneNumber = db.Column(db.String(60))
    age = db.Column(db.Integer)

    def __repr__(self):
        return f"User('username {self.firstName}', 'email :{self.email}', 'password :{self.password}')"


class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(120), nullable=False, )
    developer_id = db.Column(db.String(120), nullable=False, )
    date_debut = db.Column(db.String(120), nullable=False,)
    date_fin = db.Column(db.String(120),)
    etat = db.Column(db.String(120), nullable=False, default="en_attente")
    tache_name = db.Column(db.String(120), nullable=False, default="no_name")


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(120), )
    scrum_master = db.Column(db.String(120), )
    description = db.Column(db.Text())
    date_debut = db.Column(db.String(120), nullable=False,)
    date_fin = db.Column(db.String(120), nullable=False,)
    client = db.Column(db.String(120), nullable=False,)


class Developerproject(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id mt3 developer
    project_name = db.Column(db.String(120), )
    project_id = db.Column(db.String(120), )


# def validate(date_text):
#     try:
#         datetime.datetime.strptime(date_text, '%Y-%m-%d')
#         return True
#     except ValueError:
#         return False

def valetat(r):
    return r.strip().lower() in ["en_cours", "en_attend", "terminee"]


def valroll(r):
    return r.strip().lower() in ["developer", "client", "scrum_master"]


def valename(g):
    match = re.match("^[a-zA-Z0-9]+$", g.strip())
    return bool(match) and len(g.strip()) > 3 and len(g.strip()) < 15


def valeprojectname(g):

    return len(g.strip()) > 3 and len(g.strip()) < 21


def valage(p):
    p = p.strip()
    return p.isdigit() and int(p) > 18 and int(p) < 100


def valnum(n):
    n = n.strip()
    return len(n) == 8 and n.isdigit()


def valpass(p):
    p = p.strip()
    return len(p) > 3 and len(p) < 20


def valemail(g):
    matched = re.match(
        "[a-zA-Z0-9_\.\+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+", g.strip())
    return bool(matched)


def usergetter(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return user.firstName
    else:
        return ""


def useremailtoid(email):
    user = User.query.filter_by(email=email).first()
    return user.id


def projectgetter(id):
    project = Project.query.filter_by(id=id).first()
    return project.project_name


def tachelist(id):
    taches = Tache.query.filter_by(project_id=id).all()
    output = []
    for tache in taches:
        tache_data = {}
        tache_data['tache_id'] = tache.id
        tache_data['project_name'] = projectgetter(tache.project_id)
        tache_data['developer'] = usergetter(tache.developer_id)
        tache_data['etat'] = tache.etat
        tache_data['date_debut'] = tache.date_debut
        tache_data['date_fin'] = tache.date_fin
        tache_data['tache_name'] = tache.tache_name
        output.append(tache_data)

    return output


def tachedeveloperserilizer(taches):
    output = []
    for tache in taches:
        tache_data = {}
        tache_data['tache_id'] = tache.id
        tache_data['project_name'] = projectgetter(tache.project_id)
        tache_data['developer'] = usergetter(tache.developer_id)
        tache_data['etat'] = tache.etat
        tache_data['date_debut'] = tache.date_debut
        tache_data['date_fin'] = tache.date_fin
        tache_data['tache_name'] = tache.tache_name
        output.append(tache_data)

    return output


def serializer(projects):
    output = []
    for project in projects:
        project_data = {}
        project_data['projectname'] = project.project_name
        project_data['id'] = project.id
        project_data['description'] = project.description
        project_data['date_debut'] = project.date_debut
        project_data['date_fin'] = project.date_fin
        project_data['client'] = usergetter(project.client)
        project_data['scrum_master'] = usergetter(project.scrum_master)
        project_data['tache'] = tachelist(project.id)
        output.append(project_data)

    return output


def serializeroneproject(project):

    project_data = {}
    project_data['projectname'] = project.project_name
    project_data['id'] = project.id
    project_data['description'] = project.description
    project_data['date_debut'] = project.date_debut
    project_data['date_fin'] = project.date_fin
    project_data['client'] = usergetter(project.client)
    project_data['scrum_master'] = usergetter(project.scrum_master)
    project_data['tache'] = tachelist(project.id)

    return project_data


def serializeronetache(tache):

    tache_data = {}
    tache_data['tache_id'] = tache.id
    tache_data['project_name'] = projectgetter(tache.project_id)
    tache_data['developer'] = usergetter(tache.developer_id)
    tache_data['etat'] = tache.etat
    tache_data['date_debut'] = tache.date_debut
    tache_data['date_fin'] = tache.date_fin
    tache_data['tache_name'] = tache.tache_name

    return tache_data


def serializeruser(users):
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.firstName
        user_data['lastname'] = user.lastname
        user_data['roll'] = user.roll
        user_data['email'] = user.email
        user_data['phoneNumber'] = user.phoneNumber
        user_data['age'] = user.age

        output.append(user_data)

    return output


def serializeroneuser(user):

    user_data = {}
    user_data['id'] = user.id
    user_data['username'] = user.firstName
    user_data['lastname'] = user.lastname
    user_data['roll'] = user.roll
    user_data['email'] = user.email
    user_data['phoneNumber'] = user.phoneNumber
    user_data['age'] = user.age

    return user_data


@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        data = request.get_json()

        user = User.query.filter_by(email=data['email']).first()

        if user:
            if check_password_hash(user.password, data['password']):

                return jsonify({"message": "correct", "roll": user.roll}), 200

            else:
                return jsonify({"message": "incorect"})

        return jsonify({"message": "user exist pas"})

    else:

        return jsonify({"message": "method incorrect"})


@app.route('/')
def home():

    return jsonify({"message": "home"})


@app.route('/singup', methods=["POST"])
def singup():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        if not valemail(data['email'].strip()):
            return jsonify({"message": "invalid email format"})

        user = User.query.filter_by(email=data['email'].strip()).first()
        if user:
            return jsonify({"message": "exist"})
        print(request.get_json())
        password = generate_password_hash(data['password'], method='sha256')

        if valename(data['firstName']) and valnum(data['phoneNumber']) and valename(data['lastName']) and valroll(data['roll']) and valemail(data['email']) and valage(data['age']):

            new_user = User(password=password, firstName=data['firstName'].strip(), roll=data['roll'].strip(), lastname=data['lastName'].strip(
            ), email=data['email'].strip(), age=data['age'].strip(), phoneNumber=data['phoneNumber'].strip(),)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User created {}".format(data['firstName'])})
        else:
            print(valename(data['roll']))
            print(valage(data['age']))
            return jsonify({"message": "invalid input format"})

    else:

        return jsonify({"message": "Invalid method "})


@app.route('/projectupdate', methods=["POST"])
def projectupdate():
    if request.method == 'POST':
        data = request.get_json()
        master = None
        if data.get('emailmaster'):
            master = User.query.filter_by(email=data['emailmaster']).first()

        if not valeprojectname(data['projectname']):
            return jsonify({"message": "invalid project name"})
        if data.get('emailclient'):
            client = User.query.filter_by(email=data['emailclient']).first()
        else:
            return jsonify({"message": "email client missing"})
        if master is not None and client:
            master_id = master.id
            client_id = client.id
            new_project = Project(project_name=data['projectname'], scrum_master=master_id, description=data['description'],
                                  date_debut=data['date_debut'], date_fin=data['date_fin'], client=client.id,)
            db.session.add(new_project)
            db.session.commit()
            db.session.refresh(new_project)
            return jsonify({"message": "project created", "project_id": new_project.id})
        elif client:
            client_id = client.id
            new_project = Project(project_name=data['projectname'], description=data['description'],
                                  date_debut=data['date_debut'], date_fin=data['date_fin'], client=client.id,)
            db.session.add(new_project)
            db.session.commit()
            db.session.refresh(new_project)
            return jsonify({"message": "project created", "project_id": new_project.id})

        else:
            return jsonify({"message": "user email note found"})
    else:

        return jsonify({"message": "Invalid method "})


@app.route('/projectedit', methods=["POST"])
def projectedit():
    if request.method == 'POST':
        data = request.get_json()
        project = Project.query.filter_by(id=data['project_id']).first()
        if data.get('projectname') is not None:
            if not valeprojectname(data.get('projectname').strip()):

                return jsonify({"message": "invalid project name"})

        if project:
           # new_project=Project(project_name=data['projectname'],scrum_master=master_id,description=data['description'],date_debut=data['date_debut'],date_fin=data['date_fin'],client=client.id,)
            project.project_name = data.get(
                'projectname', project.project_name).strip()
            project.date_debut = data.get('date_debut', project.date_debut)
            project.date_fin = data.get('date_fin', project.date_fin)
            project.description = data.get(
                'description', project.description).strip()

            if data.get('emailmaster'):
                master = User.query.filter_by(
                    email=data['emailmaster']).first()
                if master:
                    master_id = master.id
                    project.scrum_master = master_id
                else:
                    return jsonify({"message": "email not found for master"})
            if data.get('emailclient'):
                client = User.query.filter_by(
                    email=data['emailclient']).first()
                if client:
                    client_id = client.id
                    project.client = client_id
                else:
                    return jsonify({"message": "email not found for client"})

            db.session.commit()
            db.session.refresh(project)
            return jsonify({"message": "project modifiet", "new project": serializeroneproject(project)})
        else:
            return jsonify({"message": "project not found"})
    else:

        return jsonify({"message": "Invalid method "})


@app.route('/tacheupdate', methods=["POST"])
def tacheupdate():
    if request.method == 'POST':
        data = request.get_json()
        project = Project.query.filter_by(id=data['project_id']).first()
        devloper = User.query.filter_by(email=data['email']).first()
        if not valeprojectname(data.get('tache_name').strip()):

            return jsonify({"message": "invalid tache name"})

        if not valetat(data.get('etat').strip()):

            return jsonify({"message": "invalid etat name"})

        # if not validate(data.get('date_debut').strip()) :

        #     return jsonify({"message":"invalid date_debut"})

        if project and devloper:
            project_id = project.id
            print(data['project_id'])
            new_tache = Tache(tache_name=data['tache_name'], project_id=project_id, developer_id=devloper.id,
                              date_debut=data['date_debut'], date_fin=data['date_fin'], etat=data['etat'],)
            db.session.add(new_tache)
            db.session.commit()
            return jsonify({"message": "Tache created"})
        else:
            return jsonify({"message": "project id or email incorect"})

    else:

        return jsonify({"message": "Invalid method "})


@app.route('/getproject', methods=["GET"])
def getproject():
    if request.method == 'GET':
        project = Project.query.all()

        return jsonify({"data": serializer(project)})

    else:

        return jsonify({"message": "Invalid method "})


@app.route('/getuser', methods=["POST"])
def getuser():
    if request.method == 'POST':
        data = request.get_json()
        users = User.query.filter_by(roll=data['roll']).all()

        return jsonify({"data": serializeruser(users)})

    else:

        return jsonify({"message": "Invalid method "})


@app.route('/delluser', methods=["POST"])
def delluser():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user:
            print(user)
            id_user = user.id
            User.query.filter_by(email=data['email']).delete()
            Project.query.filter((Project.client == id_user) | (
                Project.scrum_master == id_user)).delete()
            Tache.query.filter_by(developer_id=id_user).delete()

            db.session.commit()

            return jsonify({"message": data['email']+" deleted "})
        else:
            return jsonify({"message": data['email']+" n exist pas"})

    else:

        return jsonify({"message": "Invalid method "})


@app.route('/dellproject', methods=["POST"])
def dellproject():
    if request.method == 'POST':
        data = request.get_json()
        project = Project.query.filter_by(id=data['id_project']).first()
        if project:
            Project.query.filter_by(id=data['id_project']).delete()
            Tache.query.filter_by(project_id=data['id_project']).delete()

            db.session.commit()

            return jsonify({"message": "project with id "+data['id_project']+" deleted "})
        else:
            return jsonify({"message": "project with id "+data['id_project']+" n exist pas"})

    else:

        return jsonify({"message": "Invalid method "})


@app.route('/delltache', methods=["POST"])
def delltache():
    if request.method == 'POST':
        data = request.get_json()
        if data.get('tache_id'):
            tache = Tache.query.filter_by(id=data['tache_id']).first()
        elif data.get('email'):
            tache = Tache.query.filter_by(
                developer_id=useremailtoid(data['email'])).first()
        else:
            return jsonify({"message": "please give us a correct attribut like tache_id or email"})

        if tache:
            if data.get('tache_id'):
                Tache.query.filter_by(id=data["tache_id"]).delete()
                db.session.commit()
                return jsonify({"message": "tache with id "+data['tache_id']+" deleted "})

            elif data.get('email'):
                Tache.query.filter_by(
                    developer_id=useremailtoid(data['email'])).delete()
                db.session.commit()
                return jsonify({"message": "tache with  "+data['email']+" deleted "})

            else:
                return jsonify({"message": "please give us a correct attribut like tache_id or email"})

        else:
            return jsonify({"message": "Tache n exist pas "})

    else:

        return jsonify({"message": "Invalid method "})


@app.route('/tacheedit', methods=["POST"])
def tacheedit():
    if request.method == 'POST':
        data = request.get_json()
        tache = Tache.query.filter_by(id=data['tache_id']).first()
        if data.get('tache_name') is not None:
            if not valeprojectname(data.get('tache_name').strip()):

                return jsonify({"message": "invalid tache name"})
        if data.get('etat') is not None:
            if not valetat(data.get('etat').strip()):

                return jsonify({"message": "invalid etat name"})

        if tache:
            tache.tache_name = data.get('tache_name', tache.tache_name)
            tache.date_debut = data.get('date_debut', tache.date_debut)
            tache.date_fin = data.get('date_fin', tache.date_fin)
            tache.etat = data.get('etat', tache.etat)
            tache.project_id = data.get('project_id', tache.project_id)

            if data.get('email'):
                developer = User.query.filter_by(email=data['email']).first()
                if developer:
                    developer_id = developer.id
                    tache.developer_id = developer_id
                else:
                    return jsonify({"message": "email not found for developer"})

            db.session.commit()
            db.session.refresh(tache)
            return jsonify({"message": "tache modifiet", "new tache": serializeronetache(tache)})
        else:
            return jsonify({"message": "tache not found"})
    else:

        return jsonify({"message": "Invalid method "})


@app.route('/useredit', methods=["POST"])
def useredit():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if data.get('firstName') is not None:
            if not valename(data.get('firstName').strip()):

                return jsonify({"message": "invalid first name"})

        if data.get('lastName') is not None:
            if not valename(data.get('lastName').strip()):

                return jsonify({"message": "invalid last name"})

        if data.get('roll') is not None:
            if not valroll(data.get('roll').strip()):

                return jsonify({"message": "invalid roll name"})

        if data.get('age') is not None:
            if not valage(data.get('age').strip()):

                return jsonify({"message": "invalid age "})

        if data.get('phoneNumber') is not None:
            if not valnum(data.get('phoneNumber').strip()):

                return jsonify({"message": "invalid phoneNumber "})

        if user:
            user.firstName = data.get('firstName', user.firstName)
            user.lastname = data.get('lastName', user.lastname)
            user.roll = data.get('roll', user.roll)
            user.age = data.get('age', user.age)
            user.phoneNumber = data.get('phoneNumber', user.phoneNumber)

            if data.get('password'):
                password = generate_password_hash(
                    data['password'], method='sha256')
                user.password = password

            db.session.commit()
            db.session.refresh(user)
            return jsonify({"message": "user modifiet", "new user": serializeroneuser(user)})
        else:
            return jsonify({"message": "user not found"})
    else:

        return jsonify({"message": "Invalid method "})


@app.route('/oneuser', methods=["POST"])
def oneuser():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if user:
            return jsonify({"data": serializeroneuser(user)})
        else:
            return jsonify({"message": "user not found"})

    else:

        return jsonify({"message": "Invalid method "})


@app.route('/oneproject', methods=["POST"])
def oneproject():
    if request.method == 'POST':
        data = request.get_json()
        project = Project.query.filter_by(id=data['project_id']).first()

        if project:
            return jsonify({"data": serializeroneproject(project)})
        else:
            return jsonify({"message": "project not found"})

    else:

        return jsonify({"message": "Invalid method "})


@app.route('/onetache', methods=["POST"])
def onetache():
    if request.method == 'POST':
        data = request.get_json()
        tache = Tache.query.filter_by(id=data['tache_id']).first()

        if tache:
            return jsonify({"data": serializeronetache(tache)})
        else:
            return jsonify({"message": "tache not found"})

    else:

        return jsonify({"message": "Invalid method "})


@app.route('/getprojectbyclient', methods=["POST"])
def getprojectbyclient():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        user_id = user.id
        project = Project.query.filter_by(client=user_id).all()

        if project:
            return jsonify({"data": serializer(project)})
        else:
            return jsonify({"message": "project not found"})

    else:

        return jsonify({"message": "Invalid method "})


@app.route('/getprojectbymaster', methods=["POST"])
def getprojectbymaster():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        user_id = user.id
        project = Project.query.filter_by(scrum_master=user_id).all()

        if project:
            return jsonify({"data": serializer(project)})
        else:
            return jsonify({"message": "project not found"})

    else:

        return jsonify({"message": "Invalid method "})


@app.route('/gettachebydeveloper', methods=["POST"])
def gettachebydeveloper():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        user_id = user.id
        taches = Tache.query.filter_by(developer_id=user_id).all()
        if taches:
            return jsonify({"data": tachedeveloperserilizer(taches)})
        else:
            return jsonify({"message": "tache not found"})

    else:

        return jsonify({"message": "Invalid method "})


if __name__ == '__main__':
    app.run()
