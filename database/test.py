#!/usr/bin/env python
#test cases for db
import random,string,math
import datetime,logging
from dbModels import *
from privacy import *

names = ['Smih', 'Angelo', 'Jones', 'Boulstridge', 'Williams', 'Bungard', 'Brown', 'Bursnell', 'Taylor', 'Cabrera', 'Davies', 'Chaisty', 'Wilson', 'Clayworth', 'Evans', 'Denial', 'Thomas', 'Dissanayake', 'Johnson', 'Domville', 'Roberts', 'Dua', 'Walker', 'Edeson', 'Wright', 'Garrott', 'Robinson', 'Gaspar', 'Thompson', 'Gauge', 'White', 'Gelson', 'Hughes', 'Happer', 'Edwards', 'Hawa', 'Green', 'Helling', 'Hall', 'Hollingberry']
surnames = ['Abayari', 'Abeya', 'Abiad', 'Abinsay', 'Abiog', 'Ablang', 'Ablasa', 'Ablog', 'Abog', 'Abuan', 'Abucajo', 'Abucay', 'Abueg', 'Abut', 'Abuyen', 'Bagoyo', 'Bagsi', 'Bagsit', 'Bagtas', 'Bagu', 'Bagui', 'Bahaghar', 'Bahand', 'Bahena', 'Baiding', 'Baisac', 'Baita', 'Baje', 'Bakaranis', 'Balab', 'Balabagan', 'Balabis', 'Balaga', 'Balagot', 'Balagtas', 'Balamut', 'Datumanong', 'Dauz', 'Dawa', 'Dawi', 'Dawis', 'Daya', 'Dayag', 'Dayanan', 'Dayanghirang', 'Dayao', 'Dayap', 'Dayo', 'Dayoan', 'Mappala', 'Maquindang', 'Maquito', 'Maraan', 'Marahan', 'Maralit', 'Maramba', 'Maranan', 'Maranon', 'Marasigan', 'Marayag', 'Marigomon', 'Marikit', 'Marucut', 'Masaganda', 'Masakayan', 'Masangga', 'Masangkay', 'Masibay']
provider = ['yahoo.com','gmail.com','ymail.com','msn.com','rocketmail.com']
colleges = {"FA":"College of Fine Arts","Engg":"College of Engineering","Law":"College of Law","Educ":"College of Education","UPIS":"UP Integrated School","CBA":"College of Business Administration","Music":"College of Music","NCPAG":"National College of Public Administration and Governance","Stat":"School of Statistics","SOLAIR":"School of Labor and Industrial Relations","Asian":"Asian Center","Arki":"College of Architecture","CHE":"College of Home Economics","CSWCD":"College of Social Work and Community Development","SLIS":"School of Library and Information Studies","CMC":"College of Mass Communication","Econ":"School of Economics","SURP":"School of Urban and Regional Planning","ISSI":"Institute for Small Scale Industries","IIS":"Institute of Islamic Studies","AIT":"Asian Institute of Tourism","CHK":"College of Human Kinetics","KAL":"College of Arts and Letters","CS":"College of Science","CSSP":"College of Social Sciences and Philosophy","TMC":"Technology Management Center","ASP":"Archaeological Studies Program"}
books = [('A Tour of the Calculus', 'David Berlinski','mathematics'), ('Advanced Euclidean Geometry', 'Alfred S Posamentier','mathematics'), ('An Imaginary Tale', 'Paul J Nahin','economics'), ('Arithmetic for Parents', 'Ron Aharoni','mathematics'), ('Beyond Numbers A Practical Guide to Teaching Math Biblically', 'Katherine Loop','mathematics'), ('Calculus A Liberal Art 2nd edition', 'William McGowen Priestley','science'),('Calculus Gems Brief Lives and Memorable Mathematics', 'George F Simmons','science'),('Calculus Made Easy revised 1998 edition', 'Silvanus P Thompson and Martin Gardner','engineering'),('Culinary Math', 'Linda Blocker and Julia Hill','history'), ('Doing Simple Math in Your Head', 'W J Howard','history'), ('e The Story of a Number', 'Eli Maor','filipino'), ('Feynman s Lost Lecture The Motion of Planets Around the Sun', 'David L and Judith R','filipino'),('Goodstein ', None,'other'), ('From Zero to Infinity What Makes Numbers Interesting ', None,'other')]

sysAdmin = None

def randNum():
    return ''.join(str(random.randint(0,9)))

#returns a random persons info
def getInfo():
    first = names[random.randint(0,len(names)-1)]
    last = surnames[random.randint(0,len(surnames)-1)]
    username = first[:len(first)/2 +1]+"_"+last[:len(first)/2 +1]
    cont = randNum()
    email = last+"_"+first+"@"+provider[random.randint(0,len(provider)-1)]
    password = ''.join(random.choice(string.letters) for x in xrange(random.randint(6,13)))
    return {'first':first,'last':last,'con':cont,'email':email,'pass':password,'user':username}

#creates random accounts    
def createTestAccounts():
    test = []
    for i in range(4):
        user = getInfo()
        uname = str(user['user'].lower())
        logging.error("uname:"+uname)
        u = User(key_name=uname,username=uname,password=user['pass'],\
            firstName=user['first'],lastName=user['last'],email=user['email'],contactNum=user['con'],\
            admin=[True,False][random.randint(0,20)%2])
        u.put()
        test.append(u)
    return test

def createTestConsign(users,max_=3):
    books = Library.all().fetch(20)
    for book in books:
        for i in range(random.randint(1,max_)):
            ask = random.randint(20,70)*10.0
            con = ConsignedBook(parent=book,consignee=users[random.randint(0,len(users)-1)],added_by=sysAdmin,\
                rating=random.randint(1,5), ask_price=ask,price=math.ceil(ask*1.1))
            con.put()

def createTestReqConsign(users,max_=3):
    books = Library.all().fetch(20)
    for book in books:
        for i in range(random.randint(0,max_)):
            con = ConsignRequest(book=book,user=users[random.randint(0,len(users)-1)])
            con.put()

def createTestRequest(users,max_=3):
    books = Library.all().fetch(20)
    for book in books:
        for i in range(random.randint(1,max_)):
            ask = str(random.randint(20,70)*10.0)
            new_req = RequestedBook(parent=book,user=users[random.randint(0,len(users)-1)],max_price=ask,\
                min_rating=random.randint(1,5))
            new_req.put()

#creates database of sample books
def createBookDb():
    for b in books:
        new = Library(title=b[0],category = b[2])
        if b[1]:
            new.author = b[1]
        new.generateSk()
        new.put()

def createMyAccount():
    global sysAdmin
    sysAdmin = User(key_name="system",username="system",password="674cd0edf70ba1a76ad023a05f8cbd0b009d92b6b3d223a485448fe1deac041bQxbPFN",\
        firstName="sys", lastName="sys",email="system@ebenta.com.ph",contactNum="09123456789", admin=True)
    sysAdmin.put()    
    user = User(key_name="ibaguio",username="ibaguio",password="674cd0edf70ba1a76ad023a05f8cbd0b009d92b6b3d223a485448fe1deac041bQxbPFN",\
        firstName="ivan", lastName="baguio",email="baguio.ivan@yahoo.com",contactNum="09228448858", admin=True)
    user.put()
    
def createColleges():
    for col in colleges:
        c = Colleges(abbr=col,college=colleges[col])
        c.put()

def generalTest():
    u = createTestAccounts()
    createMyAccount()
    createBookDb()
    createTestConsign(u,7)
    createTestReqConsign(u)
    createTestRequest(u)

def getAllUsers():
    users = User.all().fetch(15)
    u = []
    for user in users:
        u.append(user)
    return u

def loadOtherBooks():
    f = open("database/books.json")
    books_json = json.loads(f.read())
    #logging.info(type(books_json))
    for category in books_json:
        #logging.info(category)
        for book in books_json[category]:
            #logging.info(book)
            new = Library(title=book['title'],author=book['author'])
            try:
                new.isbn = book['isbn']
            except:
                pass
            new.generateSk()
            new.put()
    logging.info("other books loaded")