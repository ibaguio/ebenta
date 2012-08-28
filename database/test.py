#!/usr/bin/env python
#test cases for db
import random,string
import datetime,logging
from dbModels import *
from privacy import *

exp_count = 0
not_exp_count = 0
not_yet_marked_as_expire = 0
names = ['Smih', 'Angelo', 'Jones', 'Boulstridge', 'Williams', 'Bungard', 'Brown', 'Bursnell', 'Taylor', 'Cabrera', 'Davies', 'Chaisty', 'Wilson', 'Clayworth', 'Evans', 'Denial', 'Thomas', 'Dissanayake', 'Johnson', 'Domville', 'Roberts', 'Dua', 'Walker', 'Edeson', 'Wright', 'Garrott', 'Robinson', 'Gaspar', 'Thompson', 'Gauge', 'White', 'Gelson', 'Hughes', 'Happer', 'Edwards', 'Hawa', 'Green', 'Helling', 'Hall', 'Hollingberry']

surnames = ['Abayari', 'Abeya', 'Abiad', 'Abinsay', 'Abiog', 'Ablang', 'Ablasa', 'Ablog', 'Abog', 'Abuan', 'Abucajo', 'Abucay', 'Abueg', 'Abut', 'Abuyen', 'Bagoyo', 'Bagsi', 'Bagsit', 'Bagtas', 'Bagu', 'Bagui', 'Bahaghar', 'Bahand', 'Bahena', 'Baiding', 'Baisac', 'Baita', 'Baje', 'Bakaranis', 'Balab', 'Balabagan', 'Balabis', 'Balaga', 'Balagot', 'Balagtas', 'Balamut', 'Datumanong', 'Dauz', 'Dawa', 'Dawi', 'Dawis', 'Daya', 'Dayag', 'Dayanan', 'Dayanghirang', 'Dayao', 'Dayap', 'Dayo', 'Dayoan', 'Mappala', 'Maquindang', 'Maquito', 'Maraan', 'Marahan', 'Maralit', 'Maramba', 'Maranan', 'Maranon', 'Marasigan', 'Marayag', 'Marigomon', 'Marikit', 'Marucut', 'Masaganda', 'Masakayan', 'Masangga', 'Masangkay', 'Masibay']

provider = ['yahoo.com','gmail.com','ymail.com','msn.com','rocketmail.com']

colleges = {"FA":"College of Fine Arts","Engg":"College of Engineering","Law":"College of Law","Educ":"College of Education","UPIS":"UP Integrated School","CBA":"College of Business Administration","Music":"College of Music","NCPAG":"National College of Public Administration and Governance","Stat":"School of Statistics","SOLAIR":"School of Labor and Industrial Relations","Asian":"Asian Center","Arki":"College of Architecture","CHE":"College of Home Economics","CSWCD":"College of Social Work and Community Development","SLIS":"School of Library and Information Studies","CMC":"College of Mass Communication","Econ":"School of Economics","SURP":"School of Urban and Regional Planning","ISSI":"Institute for Small Scale Industries","IIS":"Institute of Islamic Studies","AIT":"Asian Institute of Tourism","CHK":"College of Human Kinetics","KAL":"College of Arts and Letters","CS":"College of Science","CSSP":"College of Social Sciences and Philosophy","TMC":"Technology Management Center","ASP":"Archaeological Studies Program"}

books = [('A Tour of the Calculus', 'David Berlinski'), ('Advanced Euclidean Geometry', 'Alfred S Posamentier'), ('An Imaginary Tale', 'Paul J Nahin'), ('Arithmetic for Parents', 'Ron Aharoni'), ('Beyond Numbers A Practical Guide to Teaching Math Biblically', 'Katherine Loop'), ('Calculus A Liberal Art 2nd edition', 'William McGowen Priestley'), ('Calculus Gems Brief Lives and Memorable Mathematics', 'George F Simmons'), ('Calculus Made Easy revised 1998 edition', 'Silvanus P Thompson and Martin Gardner'), ('Culinary Math', 'Linda Blocker and Julia Hill'), ('Doing Simple Math in Your Head', 'W J Howard'), ('e The Story of a Number', 'Eli Maor'), ('Feynman s Lost Lecture The Motion of Planets Around the Sun', 'David L and Judith R'), ('Goodstein ', None), ('From Zero to Infinity What Makes Numbers Interesting ', None)]

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
    p = PrivacySetting.get_by_key_name("default")
    if not p:
        p = createDefault()
    test = []
    for i in range(4):
        user = getInfo()
        uname = str(user['user'].lower())
        logging.error("uname:"+uname)
        u = User(key_name=uname,username=uname,password=user['pass'],\
            firstName=user['first'],lastName=user['last'],email=user['email'],contactNum=user['con'],\
            admin=[True,False][random.randint(0,20)%2],privacy=p)
        u.put()
        test.append(u)
    return test

#generates a random expiry
def getRandomExpiry():
    global not_yet_marked_as_expire
    a = [True,False]
    add = a[random.randint(0,1)]
    if add:
        return datetime.datetime.now() + datetime.timedelta(days=5)    
    else:
        not_yet_marked_as_expire +=1
        return datetime.datetime.now() - datetime.timedelta(days=5)

def createTestSellOrder(users,max_=3):
    books = Library.all().fetch(20)
    a = [True,False,False]
    global exp_count, not_exp_count
    for book in books:
        for i in range(random.randint(1,max_)):
            #exp = a[random.randint(0,2)]
            #if exp: 
            #    exp_count += 1
            #    e = datetime.datetime.now() - datetime.timedelta(days=5)
            #if not exp: #not yet expired
            #    not_exp_count+=1
            #    e = getRandomExpiry()
            e = datetime.datetime.now() + datetime.timedelta(days=2)
            exp = False
            sale = SellBook(user=users[random.randint(0,len(users)-1)],expired=exp,\
                rating=random.randint(1,5), price=random.randint(20,70)*10.0,parent=book,expiry_date=e)
            sale.put()

    logging.info("EXPIRED COUNT:"+str(exp_count))
    logging.info("NOT EXPIRED COUNT:"+str(not_exp_count))
    logging.info("NOT YET MARKED AS EXP:"+str(not_yet_marked_as_expire))


#creates database of sample books
def createBookDb():
    for b in books:
        new = Library(title=b[0])
        if b[1]:
            new.author = b[1]
        new.generateSk()
        new.put()
    
def createMyAccount():
    privacy = PrivacySetting(key_name="default",showContact='admin',showCollege="admin")
    privacy.put()
    
    user = User(key_name="ibaguio",username="ibaguio",password="674cd0edf70ba1a76ad023a05f8cbd0b009d92b6b3d223a485448fe1deac041bQxbPFN",firstName="ivan", lastName="baguio",email="baguio.ivan@yahoo.com",contactNum="09228448858", privacy=privacy, admin=True)
    user.put()
    
def createColleges():
    for col in colleges:
        c = Colleges(abbr=col,college=colleges[col])
        c.put()

def generalTest():
    u = createTestAccounts()
    #createColleges()
    createMyAccount()
    createBookDb()
    createTestSellOrder(u)

def getAllUsers():
    users = User.all().fetch(15)
    u = []
    for user in users:
        u.append(user)
    return u

def generateMoreSellOrder():
    createTestSellOrder(getAllUsers(),7)

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

