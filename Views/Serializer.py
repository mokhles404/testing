

def serializeruser(user):
    user_data = {}
    user_data['id'] = user.id
    user_data['firstName'] = user.firstName
    user_data['lastName'] = user.lastName
    user_data['gender'] = user.gender
    user_data['email'] = user.email
    user_data['phoneNumber'] = user.phoneNumber
    user_data['age'] = user.age

    return user_data

def serializercarrot(Carrots):
    output = []
    if not( isinstance (Carrots, list )) :
        Carrots=[Carrots]
    for Carrot in Carrots:
        
        Carrot_data={}
        Carrot_data['id'] = Carrot.id
        Carrot_data['feedback'] = Carrot.feedback
        Carrot_data['date_activities'] = Carrot.date_activities
        Carrot_data['accepted'] = Carrot.accepted
        Carrot_data['sender'] = Carrot.sender_id
        Carrot_data['receiver'] = Carrot.receiver_id
        Carrot_data['admin_id'] = serializeradmin(Carrot.admin)
        output.append(Carrot_data)
        
    return output

def serializerNotification(Notification,admin=True,employee=True):
    output = []
    if not( isinstance (Notification, list )) :
        Notification=[Notification]
    for note in Notification:
        note_data={}
        
        note_data['id'] = note.id
        note_data['description'] = note.description
        note_data['timestamp'] = note.timestamp
        if employee:
            note_data['employee']=serializeremployer(note.employees,notification=False,company=False)
        if admin:
            note_data['admin']=serializeradmin(note.admin,notification=False,company=False)
        output.append(note_data)
    return output

def serializeremployer(employees,notification=True,company=True):
    output=[]
    if not( isinstance (employees, list )) :
        employees=[employees]
    for employee in employees:
        employee_data={}
        employee_data['id'] = employee.id
        employee_data['firstName'] = employee.firstName
        employee_data['lastName'] = employee.lastName
        employee_data['gender'] = employee.gender
        employee_data['email'] = employee.email
        employee_data['phoneNumber'] = employee.phoneNumber
        employee_data['age'] = employee.age
        employee_data['NumberOfCarrot'] = employee.NumberOfCarrot
        employee_data['description'] = employee.description
        employee_data['NumberOfGifts'] = employee.NumberOfGifts
        if notification:
            employee_data['notification'] = serializerNotification(employee.notification,employee=False,admin=False)
        if company:
            employee_data['company'] =serializercompany(employee.company,employee=False,admin=False)
        # if employee.pictures != []:
        employee_data['picture']= list(map(lambda x: x.picture_id ,employee.pictures))
        output.append(employee_data)
    return output

def serializercompany(company,admin=True,employee=True):

    company_data = {}
    
    company_data['companyName'] = company.companyName
    company_data['nbEmployee'] = company.nbEmployee
    company_data['logo'] =  company.logo[0].picture_id if len(company.logo) != 0 else ""
    if admin:
        company_data['admin'] = serializeradmin(company.admin,company=False,notification=False)
    
    if employee:
        company_data['employee'] = serializeremployer(company.employees,company=False,notification=False)

    return company_data

def serializerpost(posts):
    output = []
    if not( isinstance (posts, list )) :
        posts=[posts]
    for post in posts:
        post_data={}
        post_data['id']=post.id
        post_data['location']=post.location
        post_data['timestamp']=post.timestamp
        post_data['description']=post.description
        post_data['likes_user']=post.likes_user
        post_data['title']=post.title
        post_data['admin_id']=post.admin_id
        post_data['pictures']=list(map(lambda x: x.picture_id ,post.pictures))
        post_data['comments']=serializercomment(post.comments)
        output.append(post_data)
     
    return output
def serializercomment(comments):
    output = []
    if not( isinstance (comments, list )) :
        comments=[comments]
    for comment in comments:
        comment_data={}
        comment_data['id']=comment.id
        comment_data['content']=comment.content
        comment_data['timestamp']=comment.timestamp
        comment_data['post_id']=comment.post_id
        comment_data['employee']=serializeremployer(comment.employees,notification=False) if comment.employees is not None else []
        comment_data['admin']=serializeradmin(comment.admin,notification=False,post=False) if comment.admin is not None else []
        output.append(comment_data)
     
    return output
def serializeradmin(admins,notification=True,company=True, post=True,employee=True):
    output = []
    # print(admins[0].id)
    if not( isinstance (admins, list ) )  :
        admins=[admins]
    # print(admins[0][0].id)
    for admin in admins:
        admin_data = {}
        admin_data['id'] = admin.id
        admin_data['firstName'] = admin.firstName
        admin_data['lastName'] = admin.lastName
        admin_data['gender'] = admin.gender
        admin_data['email'] = admin.email
        admin_data['phoneNumber'] = admin.phoneNumber
        admin_data['description'] = admin.description
        admin_data['age'] = admin.age
        admin_data['NumberOfCarrot'] = admin.NumberOfCarrot
        admin_data['NumberOfGifts'] = admin.NumberOfGifts
        if post:
            admin_data['posts'] = serializerpost(admin.posts)
        if notification:
            admin_data['notification'] = serializerNotification(admin.notification,employee=False,admin=False)
        if company:
        #    admin_data['company']=admin.company.companyName
            admin_data['company'] =serializercompany(admin.company,employee=employee,admin=False)
        if admin.pictures != []:
            admin_data['picture']= list(map(lambda x: x.picture_id ,admin.pictures))

        output.append(admin_data)
     
    return output