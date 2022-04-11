
from Views.Serializer import serializeradmin, serializercompany, serializeremployer, serializerpost, serializeruser
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, Response, request, jsonify, make_response
from Models.model import *

main = Blueprint('main', __name__)





@main.route('/login3dwave',methods=["POST"])
def login3dwave():
    if request.method == 'POST':
        data = request.get_json()
        user = Admin3dwave.query.filter_by(email=data['email']).first()

        if user:
            if user.password == data['password']:
                return jsonify({"message":"correct",}),200

            else:
                return jsonify({"error_password":"Wrong password"})

        return jsonify({"error_email":"Email not found"})
    else:
        return jsonify({"error":"incorrect Method"})


@main.route('/add3dwave',methods=["POST"])
def add3dwave():
    if request.method == "POST":
        data = request.get_json()
        add3dwave = Admin3dwave.query.filter_by(email=data['email']).first()
        if add3dwave:
            return jsonify({"message":"Email already exist"})
        admin=Admin3dwave(firstName=data['firstName'], lastName=data['lastName'],gender=data['gender'],email=data['email'],password=data['password'],phoneNumber=data['phoneNumber'],age=data['age'])
        db.session.add(admin)
        db.session.commit()
        return jsonify({"message":"add"})
    else: 
        return jsonify({"message":"incorrect Method"})     

@main.route('/profile3dwave',methods=["POST"])
def profile3dwave():
    if request.method == "POST":
        data = request.get_json()
        admin3dwave = Admin3dwave.query.filter_by(email=data['email']).first()
        if admin3dwave:
            if data.get('pasword') is not None:
                if check_password_hash(admin3dwave.password, data['current_password']):
                    password=generate_password_hash(data['password'], method='sha256')
                    admin3dwave.password=password

                else:
                    return jsonify({"message":"verify your current password"})
                
            if data.get('firstName') is not None :
                admin3dwave.firstName = data["firstName"]
                
            if data.get('lastName') is not None :
                admin3dwave.lastName = data["lastName"]
                
            if data.get('gender') is not None :
                admin3dwave.gender = data["gender"]
                
            if data.get('phoneNumber') is not None :
                admin3dwave.phoneNumber = data["phoneNumber"]
                
            if data.get('age') is not None :
                admin3dwave.age = data["age"]
            
            db.session.commit()
            db.session.refresh(admin3dwave)
            
            return jsonify({"message":"data updated successfully", "data": serializeruser(admin3dwave)})
        else:
            return jsonify({"message":"verify your email"})

        
    else:
        jsonify({"message":"Incorrect Method"})


@main.route('/loginadmin',methods=["POST"])
def loginadmin():
    if request.method == 'POST':
        data=request.get_json()
        user = Admin.query.filter_by(email=data['email']).first()

        if user:
            if user.password == data['password']:
                return jsonify({"message":"correct",}),200

            else:
                return jsonify({"error":"Wrong password"})

        return jsonify({"error":"Email not found"})
    else:
        return jsonify({"error":"incorrect Method"})

@main.route('/adminpicture',methods=["POST"])
def adminpicture():
    if request.method == 'POST':
        data = dict(request.form)
        if( data.get("email") is not None):
            ad= Admin.query.filter_by(email=data["email"]).first()
            if ad is None:
                return jsonify({"error":"Incorrect Email"})
            if request.files.get("picture_admin") is not None :
                if ad.pictures != []:
                    pic =Picture_Admin.query.filter_by(picture_id=ad.pictures[0].picture_id).first()
                    pic_ad=request.files["picture_admin"]
                    pic.name = secure_filename(pic_ad.filename)
                    pic.mimetype = pic_ad.mimetype
                    pic.img=pic_ad.read()
                    db.session.commit()
                    return jsonify({"message":"success","img_id":ad.pictures[0].picture_id})
                else:
                    pic_ad=request.files["picture_admin"]
                    filename = secure_filename(pic_ad.filename)
                    mimetype = pic_ad.mimetype
                    picture = Picture_Admin(img=pic_ad.read(), name=filename, mimetype=mimetype,employees=ad)
                    db.session.add(picture)
                    db.session.commit()
                    db.session.refresh(picture)
                    return jsonify({"message":"success","img_id":picture.picture_id})
        else:
            return jsonify({"error":"incorect"})
            

@main.route('/companypicture',methods=["POST"])
def companypicture():
    if request.method == 'POST':
        data = dict(request.form)
        if( data.get("companyName") is not None):
            comp= Company.query.filter_by(companyName=data["companyName"]).first()
            if comp is None:
                return jsonify({"error":"Incorrect CompanyName"})
            if request.files.get("picture_company") is not None :
                if comp.logo != []:
                    pic =Logo.query.filter_by(picture_id=comp.logo[0].picture_id).first()
                    pic_ad=request.files["picture_company"]
                    pic.name = secure_filename(pic_ad.filename)
                    pic.mimetype = pic_ad.mimetype
                    pic.img=pic_ad.read()
                    db.session.commit()
                    return jsonify({"message":"success","img_id":comp.logo[0].picture_id})
                else:
                    pic_ad=request.files["picture_company"]
                    filename = secure_filename(pic_ad.filename)
                    mimetype = pic_ad.mimetype
                    picture = Logo(img=pic_ad.read(), name=filename, mimetype=mimetype,company=comp)
                    db.session.add(picture)
                    db.session.commit()
                    db.session.refresh(picture)
                    return jsonify({"message":"success","img_id":picture.picture_id})
        else:
            return jsonify({"error":"incorect"})
        
 
@main.route('/addadmin', methods=["POST"])
def addadmin():
    if request.method =="POST":
        data = dict(request.form)
        print(data)
        print(data["firstName"])
        print(request.files)
        # print(request.get_json())
        if(data.get('companyName') is not None):
            comp=Company.query.filter_by(companyName=data["companyName"]).first()
            if(comp):
                return jsonify({"error":"please choose another company name"})
        if( data.get("email") is not None):
            ad= Admin.query.filter_by(email=data["email"]).first()
            if(ad):
                print("*"*10)
                print(ad is None)
                return jsonify({"error":"email is used"})

        company=Company(companyName=data["companyName"])
        db.session.add(company)
        db.session.commit()
        db.session.refresh(company)
        admin=Admin(firstName=data["firstName"],lastName=data["lastName"],password=data["password"],gender=data["gender"],email=data["email"],phoneNumber=data["phoneNumber"],age=data["age"],company=company)
        db.session.add(admin)
        db.session.commit()
        if request.files.get("logo") is not None :
            pic=request.files["logo"]
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            logo = Logo(img=pic.read(), name=filename, mimetype=mimetype,company=company)
            db.session.add(logo)
            db.session.commit()
        if request.files.get("picture_admin") is not None :
            pic_ad=request.files["picture_admin"]
            filename = secure_filename(pic_ad.filename)
            mimetype = pic_ad.mimetype
            picture = Picture_Admin(img=pic_ad.read(), name=filename, mimetype=mimetype,admin=admin)
            db.session.add(picture)
            db.session.commit()

        return jsonify({"message":"success"})
    else:
        return jsonify({"message":"Incorrect Method"})


@main.route('/getadmin')
def getadmin():
    if request.method == "GET":
        admins=Admin.query.all()
        return jsonify({"data":serializeradmin(admins)})
    else:
        return jsonify({"message":"Wrong Method"})


@main.route('/search',methods=["POST"])
def getcompany():
    if request.method == "POST":
        data =request.get_json()
        print(data["email"])
        if data["email"].strip().lower() == "all" or data["email"].strip().lower() =="":
            admins=Admin.query.all()
            return jsonify({"data":serializeradmin(admins)})
        else:
            admins=Admin.query.filter_by(email=data["email"].strip().lower()).first()
            # admins=Admin.query.join(Company).filter(Company.companyName  == data["companyName"].strip().lower())
            # admins=Admin.query.filter( Admin.company.companyName == data["companyName"].strip().lower())
            return jsonify({"data":serializeradmin(admins)})

    else:
        return jsonify({"message":"Wrong Method"})
       


@main.route('/editadmin',methods=["POST"])
def editadmin():
    if request.method == "POST":
        data=request.get_json()
        print(data)

        admin=Admin.query.filter_by(email=data["owner_email"]).first()
        change={}
        if data.get("email") is not None:
            email_test=Admin.query.filter_by(email=data["email"].lower()).first()
            if email_test:
                return jsonify({"error":"Email is used by another admin"})
            change["email"]=data["email"]
            admin.email=data["email"]
        if data.get("password") is not None:
            change["password"]=data["password"]
            admin.password=data["password"]
        if data.get("firstName")   is not None:
            change["firstName"]=data["firstName"]
            admin.firstName=data["firstName"]
        if data.get("lastName") is not None:
            change["lastName"]=data["lastName"]
            admin.lastName=data["lastName"]
        if data.get("phoneNumber") is not None:
            change["phoneNumber"]=data["phoneNumber"]
            admin.phoneNumber=data["phoneNumber"]
        if data.get("description") is not None:
            change["description"]=data["description"]
            admin.description=data["description"]
        if data.get("age") is not None:
            change["age"]=data["age"]
            admin.age=data["age"]
        if data.get("gender") is not None:
            if data["gender"].lower() =="man" or data["gender"] .lower()=="whomen" :
                change["gender"]=data["gender"]
                admin.gender=data["gender"]
            else:
                return jsonify({"error":"Invalid gender type"})
        if data.get("NumberOfCarrot") is not None:
            if int(data["NumberOfCarrot"]) >= 0: 
                change["NumberOfCarrot"]=data["NumberOfCarrot"]
                admin.NumberOfCarrot=data["NumberOfCarrot"]
            else:
                return jsonify({"error":"Invalid number of carrot"})    
  
        if data.get("NumberOfGifts") is not None:
            if int(data["NumberOfGifts"]) >= 0: 
                change["NumberOfGifts"]=data["NumberOfGifts"]
                admin.NumberOfGifts=data["NumberOfGifts"]
            else:
                return jsonify({"error":"Invalid number of gifts"})    

        if data.get("companyName") is not None:
            comp=Company.query.filter_by(companyName=data["companyName"].strip().lower()).first()
            print(data.get("companyName"))
            print(comp)
            if comp :
                return jsonify({"error":"CompanyName Already Exists choose another company name"})
            change["companyName"]=data["companyName"]
            admin.company.companyName = data["companyName"]

        if data.get("numberOfEmployees") is not None:
            change["numberOfEmployees"]=data["numberOfEmployees"]
            admin.company.nbEmployee= data["numberOfEmployees"]
        db.session.commit()
        return jsonify({"message":change})
        
    else:
        return jsonify({"message":"Wrong Method"})
    



    
@main.route('/deletecompany',methods=["POST"])
def deladmin():
    if request.method == "POST":
        data=request.get_json()
        company=Company.query.filter_by(companyName=data["companyName"])
        if company.first() is None:
            return jsonify({"message":"Incorrect Company Name"})
        Logo.query.filter_by(company_id=company.first().id).delete()
        if company.first().admin[0].posts:
            for post in company.first().admin[0].posts:
                Comment.query.filter_by(post_id=post.id).delete()
                Picture_Post.query.filter_by(post_id=post.id).delete()
        Picture_Admin.query.filter_by(picture_id=company.first().admin[0].id).delete()
        Picture_Employees.query.filter(Picture_Employees.picture_id in list(map(lambda x: [i.picture_id for i in x.pictures] ,company.first().employees))).delete()  
        Post.query.filter_by(admin_id=company.first().admin[0].id).delete()
        Notification.query.filter_by(admin_id=company.first().admin[0].id).delete()
        Carote.query.filter_by(admin_id=company.first().admin[0].id).delete()
        Employees.query.filter_by(company_id=company.first().id).delete()
        Admin.query.filter_by(id=company.first().admin[0].id).delete()
        company.delete()
        db.session.commit()
        return jsonify({"message":"remove it"})
    else:
        return jsonify({"message":"Error"})
    
    
    

    
@main.route('/view/logo/<int:id>')
def get_logo(id):
    img = Logo.query.filter_by(picture_id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img , mimetype="image/jpeg")

@main.route('/view/admin/<int:id>')
def get_admin_picture(id):
    img = Picture_Admin.query.filter_by(picture_id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img , mimetype="image/jpeg")

@main.route('/view/employee/<int:id>')
def get_employee_picture(id):
    img = Picture_Employees.query.filter_by(picture_id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img , mimetype="image/jpeg")

@main.route('/view/post/<int:id>')
def get_post_picture(id):
    img = Picture_Post.query.filter_by(picture_id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img , mimetype="image/jpeg")

@main.route('/addemployee',methods=["POST"])
def add_employee():
    if request.method =="POST":
        data=request.get_json()
        if(data.get('owner_email') is not None):
            admin=Admin.query.filter_by(email=data["owner_email"]).first()
            comp=Company.query.filter_by(companyName= admin.company.companyName ).first()
            if(comp is None):
                return jsonify({"error":"Invalid Company Name"})
        else:
            return jsonify({"error":"Missing Company Name"})
        if( data.get("email") is not None):
            ad= Admin.query.filter_by(email=data["email"]).first()
            if(ad):
                return jsonify({"error":"email is used"})
            emp= Employees.query.filter_by(email=data["email"]).first()
            if (emp):
                return jsonify({"error":"email is Already used"})

        employees=Employees(firstName=data["firstName"],lastName=data["lastName"],password=data["password"],gender=data["gender"],email=data["email"],phoneNumber=data["phoneNumber"],age=data["age"],company=comp)
        comp.nbEmployee= str(int(comp.nbEmployee)+1)
        db.session.add(employees)
        db.session.commit()
        return jsonify({"message":"Employee add it successfully"})

@main.route('/deletemployee',methods=["POST"])
def deleteEmployee():
    if request.method == "POST":
        data=request.get_json()
        emp= Employees.query.filter_by(email=data["email"])
        print(emp.first() is  None)
        if emp.first() is  not None :
            emp.first().company.nbEmployee= str(int(emp.first().company.nbEmployee)-1)
            emp.delete()
            db.session.commit()
            return jsonify({"message":"Employee delete"})
        else :
            return jsonify({"error":"Infound Email"})
        


@main.route('/employeenpicture',methods=["POST"])
def employeenpicture():
    if request.method == 'POST':
        data = dict(request.form)
        if( data.get("email") is not None):
            ad= Employees.query.filter_by(email=data["email"]).first()
            if ad is None:
                return jsonify({"error":"Incorrect Email"})
            if request.files.get("picture_employee") is not None :
                if ad.pictures != []:
                    pic =Picture_Employees.query.filter_by(picture_id=ad.pictures[0].picture_id).first()
                    pic_ad=request.files["picture_employee"]
                    pic.name = secure_filename(pic_ad.filename)
                    pic.mimetype = pic_ad.mimetype
                    pic.img=pic_ad.read()
                    db.session.commit()
                    return jsonify({"message":"success","img_id":ad.pictures[0].picture_id})
                else:
                    pic_ad=request.files["picture_employee"]
                    filename = secure_filename(pic_ad.filename)
                    mimetype = pic_ad.mimetype
                    picture = Picture_Employees(img=pic_ad.read(), name=filename, mimetype=mimetype,employees=ad)
                    db.session.add(picture)
                    db.session.commit()
                    db.session.refresh(picture)
                    return jsonify({"message":"success","img_id":picture.picture_id})
        else:
            return jsonify({"error":"incorect"})
        
@main.route('/addemployeepicture', methods=['POST'])
def addemployeepicture():
    pic = request.files['pic']
    if pic is None:
                return jsonify({'message' :"picture none"})

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return jsonify({'message' : 'Bad upload!'})

    img = Picture_Employees(img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()
    db.session.refresh(img)

    return jsonify({'message' : 'Img Uploaded! '+str(img.picture_id)})




@main.route('/editemployee',methods=["POST"])
def editemployee():
    if request.method == "POST":
        data=request.get_json()
        print(data)

        employee=Employees.query.filter_by(email=data["owner_email"]).first()
        change={}
        if data.get("email") is not None:
            email_test=Employees.query.filter_by(email=data["email"].lower()).first()
            if email_test:
                return jsonify({"error":"Email is used by another employee"})
            change["email"]=data["email"]
            employee.email=data["email"]
        if data.get("password") is not None:
            change["password"]=data["password"]
            employee.password=data["password"]
        if data.get("firstName")   is not None:
            change["firstName"]=data["firstName"]
            employee.firstName=data["firstName"]
        if data.get("lastName") is not None:
            change["lastName"]=data["lastName"]
            employee.lastName=data["lastName"]
        if data.get("phoneNumber") is not None:
            change["phoneNumber"]=data["phoneNumber"]
            employee.phoneNumber=data["phoneNumber"]
        if data.get("description") is not None:
            change["description"]=data["description"]
            employee.description=data["description"]
        if data.get("age") is not None:
            change["age"]=data["age"]
            employee.age=data["age"]
        if data.get("gender") is not None:
            if data["gender"].lower() =="man" or data["gender"] .lower()=="whomen" :
                change["gender"]=data["gender"]
                employee.gender=data["gender"]
            else:
                return jsonify({"error":"Invalid gender type"})
        if data.get("NumberOfCarrot") is not None:
            if int(data["NumberOfCarrot"]) >= 0: 
                change["NumberOfCarrot"]=data["NumberOfCarrot"]
                employee.NumberOfCarrot=data["NumberOfCarrot"]
            else:
                return jsonify({"error":"Invalid number of carrot"})    
  
        if data.get("NumberOfGifts") is not None:
            if int(data["NumberOfGifts"]) >= 0: 
                change["NumberOfGifts"]=data["NumberOfGifts"]
                employee.NumberOfGifts=data["NumberOfGifts"]
            else:
                return jsonify({"error":"Invalid number of gifts"})    
        db.session.commit()
        return jsonify({"message":change})
         
    else:
        return jsonify({"message":"Wrong Method"})

@main.route('/loginemployee',methods=["POST"])
def loginEmployee():
    if request.method == "POST":
        data=request.get_json()
        print(data)
        user = Employees.query.filter_by(email=data['email']).first()

        if user:
            if user.password == data['password']:
                return jsonify({"message":"correct",}),200

            else:
                return jsonify({"error":"Wrong password"})

        return jsonify({"error":"Email not found"})
    else:
        return jsonify({"error":"incorrect Method"})

@main.route('/getemployee',methods=["POST"])
def getemployee():
    data =request.get_json()
    emp=Employees.query.filter_by(email=data["email"]).first()
    if emp is None:
        return jsonify({"error":"Incorrect Email"})
    return jsonify(serializeremployer(emp))

@main.route('/getemployeelist',methods=["POST"])
def getemployeelist():
    data =request.get_json()
    emp=Employees.query.filter_by(email=data["email"]).first()
    comp= Company.query.filter_by(companyName=emp.company.companyName).first()
    return jsonify(serializeremployer(comp.employees))

@main.route('/')
def home():
    return jsonify({"server":"server"})

@main.route('/addcarrot',methods=["POST"])
def addcarrot():
    if request.method == "POST":
        data =request.get_json()
        print(data)
        ad =Admin.query.filter_by(email=data["email"]).first()
        carrot=Carote(feedback =data["feedback"],admin=ad,sender_id=data["sender"],receiver_id=data["receiver"])
        db.session.add(carrot)
        db.session.commit()
        return jsonify({"message":"add it carrot"})

@main.route('/getcarrot',methods=["POST"])
def getcarrot():
    if request.method =="POST":
        data=request.get_json()
        ad =Admin.query.filter_by(email=data["email"]).first()
        if ad is None:
            return jsonify({"error":"Incorrect Admin"})
        Carrots = Carote.query.filter_by(admin_id=ad.id).all()
        output = []
        # if not( isinstance (Carrots, list )) :
        #     Carrots=[Carrots]
        for Carrot in Carrots:
            print(Employees.query.filter_by(email=Carrot.sender_id).first())
            Carrot_data={}
            Carrot_data['id'] = Carrot.id
            Carrot_data['feedback'] = Carrot.feedback
            Carrot_data['date_activities'] = Carrot.date_activities
            Carrot_data['accepted'] = Carrot.accepted
            Carrot_data['sender'] =serializeremployer(Employees.query.filter_by(email=Carrot.sender_id).first()) 
            Carrot_data['receiver'] = serializeremployer(Employees.query.filter_by(email=Carrot.receiver_id).first()) 
            Carrot_data['admin_id'] = serializeradmin(Carrot.admin,company=False,post=False)
            output.append(Carrot_data)
        return jsonify({"carrot":output})
    
    
@main.route('/editcarrot',methods=["POST"])
def editcarrot():
    if request.method =="POST":
        data=request.get_json()
        c=Carote.query.filter_by(id=data["id"]).first()
        if c is None:
            return jsonify({"error":"carrot not found"})
        c.accepted=data["accepted"]
        db.session.commit()
        return jsonify({"message":"Carrot updated"})
    

@main.route('/deletepost',methods=["POST"])
def deletepost():
    if request.method == "POST":
        data=request.get_json()
        post=Post.query.filter_by(id=data["id"])
        Comment.query.filter_by(post_id=post.first().id).delete()
        Picture_Post.query.filter_by(post_id=post.first().id).delete()
        post.delete()
        db.session.commit()
        return jsonify({"message":"delete it successfully"})
    
@main.route('/editpost',methods=["POST"])
def editpost():
    if request.method == "POST":
        data = dict(request.form)
        post=Post.query.filter_by(id=data["id"]).first()
        print(request.files.get("picture_post")is None)
        if post is None:
            return jsonify({"error":"Post not found"})
        if data.get("location") is not None:
            post.location=data["location"]
        if data.get("description") is not None:
            post.description=data["description"]
        if data.get("title") is not None:
            post.title=data["title"]
        db.session.commit()
        if request.files.get("picture_post") is not None :
            print("00000000")
            if post.pictures != []:
                print("111111")
                pic =Picture_Post.query.filter_by(picture_id=post.pictures[0].picture_id).first()
                pic_ad=request.files["picture_post"]
                pic.name = secure_filename(pic_ad.filename)
                pic.mimetype = pic_ad.mimetype
                pic.img=pic_ad.read()
                db.session.commit()
                return jsonify({"message":"success","img_id":post.pictures[0].picture_id})
            else:
                print("222222")
                pic_ad=request.files["picture_post"]
                filename = secure_filename(pic_ad.filename)
                mimetype = pic_ad.mimetype
                picture = Picture_Post(img=pic_ad.read(), name=filename, mimetype=mimetype,post=post)
                db.session.add(picture)
                db.session.commit()
                db.session.refresh(picture)
                return jsonify({"message":"success","img_id":picture.picture_id})

        return jsonify({"message":"Edit post successfully"})

@main.route('/addpost',methods=["POST"])
def addpost():
    if request.method == "POST":
        data = dict(request.form)
        print(data)
        if data.get("title") is not None and data.get("email") is not None:
            ad= Admin.query.filter_by(email=data["email"]).first()
            if ad is None:
                return jsonify({"error":"Incorrect email address"})
            post=Post(title=data["title"],admin=ad)
            if data.get("location") is not None:
                post.location=data["location"]
            if data.get("description") is not None:
                post.description=data["description"]
            db.session.add(post)
            db.session.commit()
            if request.files.get("picture_post") is not None :
                pic_ad=request.files["picture_post"]
                filename = secure_filename(pic_ad.filename)
                mimetype = pic_ad.mimetype
                picture = Picture_Post(img=pic_ad.read(), name=filename, mimetype=mimetype,post=post)
                db.session.add(picture)
                db.session.commit()
            return jsonify({"message":"Post Added"})
        else:
            return jsonify({"error":"Parametre Missing"})


#############################################Testing

@main.route('/test',methods=["POST"])
def test():
    if request.method == "POST":
        # data=request.files.get("logo")
        data=request.form["companyName"]
        print(data)
        print(type(data))

        company=Company(companyName=data)
        db.session.add(company)
        db.session.commit()
        db.session.refresh(company)

        if request.files.get("logo") is not None :
            pic=request.files.get("logo")
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            logo = Logo(img=pic.read(), name=filename, mimetype=mimetype,company=company)
            db.session.add(logo)
            db.session.commit()
            db.session.refresh(logo)

        return jsonify({"message":"gtt"})
    
    
@main.route('/pic', methods=['POST'])
def pic():
    pic = request.files['pic']
    if pic is None:
                return jsonify({'message' :"picture none"})

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return jsonify({'message' : 'Bad upload!'})

    img = Logo(img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()
    db.session.refresh(img)

    return jsonify({'message' : 'Img Uploaded! '+str(img.picture_id)})

@main.route('/')
def hello():
    return jsonify({'message' :"hellop"})

@main.route('/post')
def post():
    
    post=Post.query.filter_by(location="sousse").all()
    # print(post[0].comments[0].content)
    
    # ad=Admin.query.filter_by(id="1").first()
    # print(ad)
    # return jsonify({"ee":serializeradmin(ad)})
    
    return jsonify({'message' :serializerpost(post)})