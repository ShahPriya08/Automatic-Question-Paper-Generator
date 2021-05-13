from flask import render_template, url_for, flash, redirect,Flask,request,make_response,session
from requests.models import Response
import mysql.connector
from datetime import date 
import random
from flask import Response
import aqgFunction
from napkin import generate
import pdfkit as pdf
from xhtml2pdf import pisa
from io import BytesIO,StringIO
import re
import PyPDF2
import os
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = '/uploads/'
ALLOWED_EXTENSIONS = { 'pdf'}


date=date.today()
global q1a
global q1b
global q1c
global q2a
global q2b
global q2c
global q2cc
global q3a
global q3b
global q3c
global q3aa
global q3bb
global q3cc
global q4a
global q4b
global q4c
global q4aa
global q4bb
global q4cc
global q5a
global q5b
global q5c
global q5aa
global q5bb
global q5cc
global loggedIn
loggedIn = 0
global dat
dat = date.today()
global semester1
global subject1
global subjectCode
global duration
global totalMarks
totalMarks = 0
global marks1
marks1 = 0
global marks2
marks2=0
global marks3
marks3=0
global difficultyLevel1
global number_of_Ques1
global number_of_Ques2
global number_of_Ques3
global dataA
dataA = ''
global dataB
dataB = ''
global dataC
dataC = ''
global getPdf
getPdf = 0

app = Flask(__name__)

app.secret_key = 'any random string'
global COOKIE_TIME_OUT
#COOKIE_TIME_OUT = 60*60*24*7 #7 days
COOKIE_TIME_OUT = 60*5 #5 minutes
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="autoquest"
)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/<string:username>')
def dashboard(username):
    # print(username)
    if "username" in session:
        print("1",username)
        mycursor = mydb.cursor()
        mycursor.execute("select  COUNT( DISTINCT subject_code), COUNT(question) from add_questions ")
        data=mycursor.fetchall()
        print(data)
        return render_template('dashboard.html',show_subject=data,username=username)
    else:
        return redirect(url_for('home'))

@app.route('/adddata/<string:username>')
def add_question(username):
    if "username" in session:
        return render_template('adddata.html',username=username)
    else:
        return redirect(url_for('home'))

@app.route('/showQuestion/<string:username>')
def showQuestion(username):
    if "username" in session:
        mycursor = mydb.cursor()
        mycursor.execute("select * from add_questions")
        data=mycursor.fetchall()
        # print(data)
        # page=request.args.get('page')
        # if page and page.isdigit():
        #     page=int(page)
        # else:
        #     page=1
        # pages=data.paginate(page=page,per_page=1)
        return render_template('showQue.html',username=username,show_data=data)
    else:
        return redirect(url_for('home'))

@app.route('/paper/<string:username>')
def paper(username):
    if "username" in session:
        return render_template('paper.html',username="username")
    else:
        return redirect(url_for('home'))

@app.route('/contact/<string:username>')
def contact(username):
    return render_template('contact.html',username=username)

@app.route('/generatePaper/<string:username>')
def generatePaper(username):
    if "username" in session:
        return render_template('generatePaper.html',username=username)
    else:
        return redirect(url_for('home'))

@app.route('/subject/<string:username>')
def subject(username):
    if "username" in session:
        mycursor = mydb.cursor()
        mycursor.execute("select distinct subject_code from add_questions")
        data=mycursor.fetchall()
        print(data)
        return render_template('subject.html',subjectcode=data,username=username)
    else:
        return redirect(url_for('home')) 

@app.route('/showPapers/<string:username>')
def showPapers(username):
    if "username" in session:
        mycursor = mydb.cursor()
        mycursor.execute("select *from papers")
        data=mycursor.fetchall()
        
        print(data)
        return render_template('showPaper.html',papers=data,username=username)
    else:
        return redirect(url_for('home')) 

@app.route('/que//<string:username>/<string:subject_code>')
def que(username,subject_code):
    if "username" in session:
        mycursor=mydb.cursor()
        print(1)
        mycursor.execute("select * from add_questions where subject_code=%s",(subject_code,))
        data=mycursor.fetchall()
        print(data)
        return render_template("que.html",que=data,username=username)
    else:
        return redirect(url_for('home')) 

@app.route('/logout')
def logout():
    session.pop('username', None)
    # global loggedIn
    # loggedIn = 0
    # response = make_response()
    # response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    # Response().headers["Pragma"] = "no-cache"
    # Response().headers["Expires"] = "0"
    # Response().headers['Cache-Control'] = 'public, max-age=0'
    return render_template('home.html', title='Home')      

@app.route('/dashboard', methods=['POST','GET'])
def login_validation():
    mycursor = mydb.cursor()
    if request.method=='POST':
        signup=request.form
        username=signup['username']
        password=signup['password']
        remember=signup.getlist('remember')
        print(remember,"------")
        if remember:
            password=password.strip()
            print(password)
            username=username.strip()
            print(username)
            resp = make_response(redirect('/dashboard'))
            resp.set_cookie('username',username, max_age=COOKIE_TIME_OUT)
            resp.set_cookie('password',password, max_age=COOKIE_TIME_OUT)
            # resp.set_cookie('remember', 'checked', max_age=COOKIE_TIME_OUT)
            # return resp
        mycursor.execute("SELECT * FROM user")
        for row in mycursor.fetchall():
            if row[0]==username and row[1]==password:
                found=1
                break
            else:
                found=2
                flash('Login Unsuccessful. Please check username and password', 'danger')
                return redirect(url_for('login'))
        if found==1:
            session['username']=signup['username']
            if 'username' in session:
                s=session['username']
            mycursor.execute("select *from user where username='"+username+"' and password='"+password+"'" )
            r=mycursor.fetchall()
            count=mycursor.rowcount
            mycursor.execute("select  COUNT( DISTINCT subject_code), COUNT(question) from add_questions ")
            data=mycursor.fetchall()
            print(username,"+++++++")
            print(data)
            if count==1:
                return redirect(url_for("dashboard",show_subject=data,username=s))
            else:
                return render_template("login.html")
            mydb.commit()
            mycursor.close()

@app.route('/showUnit/<string:username>')
def showWeightage(username):
    if "username" in session:
        cur = mydb.cursor()
        cur.execute("SELECT * FROM units WHERE Username=%s",(username,))
        data = cur.fetchall()
        cur.close()
        print(data)
        return render_template('showUnit.html', weightage=data, username=username)
    else:
        return redirect(url_for('register'))


@app.route('/add/<string:username>',methods = ['POST'])
def addWeightage(username):

    if request.method == "POST":
        recordFound = 0
        
        subjectCode = int(request.form['subjectCode'])
        
        unit = int(request.form['unit'])

        weight = int(request.form['weightage'])
        weightage = float(weight/100)
        
        cur = mydb.cursor(buffered=True)
        cur.execute("SELECT * FROM units WHERE Username=%s AND subject_code=%s AND unit=%s",(username,subjectCode,unit))
        r=cur.fetchall()
        recordFound=cur.rowcount
        if recordFound==1:
            flash("Record already exists\n You might want to update it.",'danger')
            return redirect(url_for('showWeightage',username=username))
            

        elif recordFound==0:
            cur = mydb.cursor(buffered=True)
            cur.execute("INSERT INTO units (Username,subject_code,unit,weightage) VALUES (%s, %s, %s, %s)", (username,subjectCode,unit,weightage))
            mydb.commit()
            flash("Weightage Inserted Successfully","success")

            cur.execute("SELECT * FROM subjects WHERE  Username=%s AND Subject_code=%s",(username,subjectCode))
            r=cur.fetchall()
            found=cur.rowcount
            if found==1:
                cur.execute("UPDATE subjects SET Number_of_units=(SELECT COUNT(unit) FROM units WHERE Username=%s AND subject_code=%s) WHERE Subject_code=%s",(username,subjectCode,subjectCode))
                mydb.commit()
            else:
                cur.execute("INSERT INTO subjects (Username,Number_of_units,Subject_code) VALUES (%s,%s,%s)",(username,"1",subjectCode))
                mydb.commit()
            return redirect(url_for('showWeightage',username=username))

@app.route('/update_weightage/<string:username>',methods = ['POST','GET'])
def updateWeightage(username):

    if request.method == 'POST':
        id_data = request.form['id']
        subjectCode = int(request.form['subjectCode'])
        unit = int(request.form['unit'])
        weight = int(request.form['weightage'])
        weightage = float(weight/100)
        cur = mydb.cursor()
        cur.execute("""
               UPDATE units
               SET subject_code=%s, unit=%s, weightage=%s
               WHERE id=%s
            """, (subjectCode,unit,weightage, id_data))
        flash("Weightage Updated Successfully","success")
        mydb.commit()
        cur.execute("SELECT * FROM units WHERE  Username=%s AND subject_code=%s",(username,subjectCode))
        r=cur.fetchall()
        found=cur.rowcount
        print(found)
        if found==1:
            cur.execute("UPDATE subjects SET Number_of_units=(SELECT COUNT(unit) FROM units WHERE Username=%s AND subject_code=%s) WHERE Subject_code=%s",(username,subjectCode,subjectCode))
            mydb.commit()
        else:
            cur.execute("DELETE FROM subjects WHERE Subject_code=%s",(subjectCode,))
            mydb.commit()
        return redirect(url_for('showWeightage',username=username))


@app.route('/del_weightage/<string:id>/<string:username>/<string:subjectCode>',methods = ['POST','GET'])
def deleteWeightage(id,username,subjectCode):
    flash("Weightage Has Been Deleted Successfully","success")
    cur = mydb.cursor()
    cur.execute("DELETE FROM units WHERE id=%s", (id,))
    mydb.commit()
    cur.execute("SELECT * FROM units WHERE  Username=%s AND subject_code=%s",(username,subjectCode))
    r=cur.fetchall()
    found=cur.rowcount
    print(found)
    if found==1:
        cur.execute("UPDATE subjects SET Number_of_units=(SELECT COUNT(unit) FROM units WHERE Username=%s AND subject_code=%s) WHERE Subject_code=%s",(username,subjectCode,subjectCode))
        mydb.commit()
    else:
        cur.execute("DELETE FROM subjects WHERE Subject_code=%s",(subjectCode,))
        mydb.commit()
    return redirect(url_for('showWeightage',username=username))

@app.route('/add_user',methods=['POST'])
def add_user():
    mycursor = mydb.cursor()
    if request.method=='POST':
        signup=request.form
        found = 0
        username=signup['uname']
        email=signup['uemail']
        password=signup['upassword']
        mycursor.execute("SELECT * FROM user")
        for row in mycursor.fetchall():
                if row[0]==username:
                    found=1
                    flash('Username already exists', 'danger')
                    return redirect(url_for('register'))
                elif row[2]==email:
                    found=1
                    flash('Email already exists', 'danger')
                    return redirect(url_for('register'))
        if found==0:
            mycursor.execute("insert into user(username,email,password)values(%s,%s,%s)",(username,email,password))
            mydb.commit()
            mycursor.close()
            flash(f'Account created for {username} ! ', 'success')
            return render_template("login.html")

@app.route('/addQuestion/<string:username>',methods=['POST','GET'])
def addQuestion(username):
    if "username" in session:
        mycursor = mydb.cursor()
        
        # if request.method=='POST':
        recordFound=0
        signup=request.form
        subject_code=signup['subject_code']
        unit=signup['unit']
        # difficulty=signup['difficulty']
        marks=signup['marks']
        question=signup['question']
        print(username,subject_code,question)
        mycursor.execute("SELECT * FROM add_questions WHERE Username=%s AND subject_code=%s AND question=%s",(username,subject_code,question))
        # print("SELECT * FROM add_questions WHERE Username= AND subject_code=%s AND question=%s,(username,subject_code,question)")
        r=mycursor.fetchall()
        print(r,"!1111111111111")
        recordFound=mycursor.rowcount
        print(recordFound)
        if recordFound==1:
            flash("Record already exists",'danger')
            return redirect(url_for('showQuestion',username=username)) 
        elif recordFound==0:
            mycursor.execute("insert into add_questions(subject_code,unit,marks,question,Auto)values(%s,%s,%s,%s,%s)",(subject_code,unit,marks,question,"Manual"))
            mydb.commit()
            mycursor.close()
            flash("Question Inserted Successfully","success")
            return redirect(url_for('showQuestion',username=username))       
    else:
        return redirect(url_for('register'))

@app.route('/generate_paper/<string:username>', methods=['POST','GET'])
def generate_paper(username):
    if "username" not in session:
        return redirect(url_for('register'))
    signup=request.form
    sectionError = 0
    msg1 = ''
    msg2 = ''
    msg3 = ''
    msg=''
    global semester
    semester = signup['semester']
    global department
    department=signup['department']
    global subject
    subject = signup['subject']
    global subjectCode
    subjectCode = signup['subject code']
    durationHours = request.form['hours']
    durationMinutes = request.form['mins']
    global duration
    duration = durationHours+' hours '+durationMinutes+' minutes'
    #global marks1
    #marks1 = int(request.form['marks1'])
    #difficultyLevel1 = request.form.get('difficultyLevel1')
    #global number_of_Ques1
    #number_of_Ques1 = int(request.form['noOfQues1'])

    cur1 = mydb.cursor(buffered=True)
    cur1.execute("SELECT marks,question FROM add_questions WHERE Username=%s AND subject_code=%s AND marks='3' order by rand()",(username,subjectCode))
    
    if cur1.rowcount<8:
        sectionError+=1
        msg1+='\n3 Marks Questions:\nInsert desired questions in the AutoQuest system'

    #global dataA
    #dataA = cur1.fetchall()

    
        
    #global marks2
    #marks2 = int(request.form['marks2'])
    #difficultyLevel2 = request.form.get('difficultyLevel2')
    #global number_of_Ques2
    #number_of_Ques2 = int(request.form['noOfQues2'])
    cur2 = mydb.cursor(buffered=True)
    cur2.execute("SELECT marks,question FROM add_questions WHERE Username=%s AND subject_code=%s AND marks='4' order by rand()",(username,subjectCode))
    if cur2.rowcount<8:
        sectionError+=1
        msg2+='\n4 Marks Questions:\nInsert desired questions in the AutoQuest system'
    

    #global marks3
    #marks3 = int(request.form['marks3'])
    #difficultyLevel3 = request.form.get('difficultyLevel3')
    #global number_of_Ques3
    #number_of_Ques3 = int(request.form['noOfQues3'])
    cur3 = mydb.cursor(buffered=True)
    cur3.execute("SELECT marks,question FROM add_questions WHERE Username=%s AND subject_code=%s AND marks='7' order by rand()",(username,subjectCode))
    if cur3.rowcount<9:
        sectionError+=1
        msg3+='\n7 Marks Questions:\nInsert desired questions in the AutoQuest system'
    



    if sectionError==0:
        '''
        global totalMarks
        m1 = marks1*number_of_Ques1
        m2 = marks2*number_of_Ques2
        m3 = marks3*number_of_Ques3
        totalMarks=int(m1+m2+m3)
        '''





        '''
        cur1.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks='3' order by rand() limit 8",(username,semester1,subject1))
        global q1a
        q1a = cur1.fetchmany(1)
        global q2a
        q2a = cur1.fetchmany(1)
        global q3a
        q3a = cur1.fetchmany(1)
        global q3aa
        q3aa = cur1.fetchmany(1)
        global q4a
        q4a = cur1.fetchmany(1)
        global q4aa
        q4aa = cur1.fetchmany(1)
        global q5a
        q5a = cur1.fetchmany(1)
        global q5aa
        q5aa = cur1.fetchmany(1)
        cur2.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks='4' order by rand() limit 8",(username,semester1,subject1))
        global q1b
        q1b = cur2.fetchmany(1)
        global q2b
        q2b = cur2.fetchmany(1)
        global q3b
        q3b = cur2.fetchmany(1)
        global q3bb
        q3bb = cur2.fetchmany(1)
        global q4b
        q4b = cur2.fetchmany(1)
        global q4bb
        q4bb = cur2.fetchmany(1)
        global q5b
        q5b = cur2.fetchmany(1)
        global q5bb
        q5bb = cur2.fetchmany(1)
        
        cur3.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks='7' order by rand() limit 9",(username,semester1,subject1))
        global q1c
        q1c = cur3.fetchmany(1)
        global q2c
        q2c = cur3.fetchmany(1)
        global q2cc
        q2cc = cur3.fetchmany(1)
        global q3c
        q3c = cur3.fetchmany(1)
        global q3cc
        q3cc = cur3.fetchmany(1)
        global q4c
        q4c = cur3.fetchmany(1)
        global q4cc
        q4cc = cur3.fetchmany(1)
        global q5c
        q5c = cur3.fetchmany(1)
        global q5cc
        q5cc = cur3.fetchmany(1)
        cur3.close()
        '''



        cur = mydb.cursor(buffered=True)
        cur.execute("SELECT Number_of_units FROM subjects WHERE Subject_code=%s",(subjectCode,))
        for Device in cur.fetchmany(1):
            NoOfUnits=Device[0]
            print(NoOfUnits)
   
        finalAns=[]
        # subjectCode = '2170710'

    
        for i in range(1,int(NoOfUnits)+1):
            cur.execute("SELECT weightage FROM units WHERE subject_code=%s AND unit=%s",(subjectCode,i))
            for Device in cur.fetchmany(1):
                weightage=Device[0]
                print(weightage)
            finalWeightage=119*weightage
        #cur.execute("(SELECT  Unit,NULL as question, NULL as marks, NULL AS total FROM questions WHERE ((@total := 0)) UNION SELECT Unit,question,marks, @total := @total + marks AS total FROM questions WHERE Subject_code=%s AND Unit=%s AND marks=3 AND @total<119*0.1/5.5 ORDER BY RAND()) UNION (SELECT  Unit,NULL as question, NULL as marks, NULL AS total FROM questions WHERE ((@total := 0)) UNION SELECT Unit,question,marks, @total := @total + marks AS total FROM questions WHERE Subject_code=%s AND Unit=%s AND marks=4 AND @total<119*0.1/2 ORDER BY RAND()) UNION (SELECT  Unit,NULL as question, NULL as marks, NULL AS total FROM questions WHERE ((@total := 0)) UNION SELECT Unit,question,marks, @total := @total + marks AS total FROM questions WHERE Subject_code=%s AND Unit=%s AND marks=7 AND @total<119*0.1 ORDER BY RAND())",(subjectCode,i,subjectCode,i,subjectCode,i))
            cur.execute("(SELECT  unit,NULL as question, NULL as marks, NULL AS total FROM add_questions WHERE ((@total := 0)) UNION SELECT unit,question,marks, @total := @total + marks AS total FROM add_questions WHERE subject_code=%s AND unit=%s AND marks=3 AND @total<%s ORDER BY RAND()) UNION (SELECT  unit,NULL as question, NULL as marks, NULL AS total FROM add_questions WHERE ((@total := 0)) UNION SELECT unit,question,marks, @total := @total + marks AS total FROM add_questions WHERE subject_code=%s AND unit=%s AND marks=4 AND @total<%s ORDER BY RAND()) UNION (SELECT  unit,NULL as question, NULL as marks, NULL AS total FROM add_questions WHERE ((@total := 0)) UNION SELECT unit,question,marks, @total := @total + marks AS total FROM add_questions WHERE subject_code=%s AND unit=%s AND marks=7 AND @total<%s ORDER BY RAND())",(subjectCode,i,finalWeightage/5.5,subjectCode,i,finalWeightage/2,subjectCode,i,finalWeightage))
            cur2.execute("SELECT @total")
            tota = cur2.fetchone()
            tot = tota[0]
            print(tot)
            if float(tot) < finalWeightage:
                message1 = 'Unit '
                message2 = str(i)
                message3 = ': Insert desired questions in the AutoQuest system'
                msg+= message1+message2+message3
            tempAns=cur.fetchall()
            tempAns=list(tempAns)
            finalAns=finalAns+tempAns
            print(finalAns,"finalans")
        cur.execute("SELECT unit,question,marks FROM add_questions WHERE marks=1 AND subject_code=%s ORDER BY RAND()",(subjectCode,))
        aiOpt = cur.fetchall()
        random.shuffle(aiOpt)
        q1aOpt2=[item[1:3] for item in list(aiOpt[0:3])]
        random.shuffle(q1aOpt2)
        q2aOpt2=[item[1:3] for item in list(aiOpt[3:6])]
        random.shuffle(q2aOpt2)
        q3aaOpt2=[item[1:3] for item in list(aiOpt[6:9])]
        random.shuffle(q3aaOpt2)
        if msg!='':
                flash(msg, 'danger')
                return redirect(url_for('showQuestion',username=username))
        random.shuffle(finalAns)
        print("........................")
        # finalAns=list(finalAns)
        # print(finalAns)
        marks3 = [num for num in finalAns if num[2]==3]
        # print(marks3)
        marks4 = [num for num in finalAns if num[2]==4]
        print(marks4)
        marks7 = [num for num in finalAns if num[2]==7]
        marks3=list(marks3)
        marks4=list(marks4)
        # print(marks4)
        marks7=list(marks7)
        random.shuffle(marks3)
        random.shuffle(marks4)
        random.shuffle(marks7)
    #ques1a = marks3[0:1]
    #ques1a=list(ques1a)
        global q1a
        q1aOpt1=[item[1:3] for item in list(marks3[0:1])]
        if q1aOpt2!=[]:
        	q1a=random.choice([q1aOpt1,q1aOpt2])
        else:
        	q1a=[item[1:3] for item in list(marks3[0:1])]
        #q1a=[item[1:3] for item in list(q1aOpt[0:3])]
        q1a=list(q1a)
        q2aOpt1=[item[1:3] for item in list(marks3[1:2])]
        global q2a
        if q2aOpt2!=[]:
        	q2a=random.choice([q2aOpt1,q2aOpt2])
        else:
        	q2a=[item[1:3] for item in list(marks3[1:2])]
        q2a=list(q2a)
        global q3a
        q3a=[item[1:3] for item in list(marks3[2:3])]
        q3a=list(q3a)
        q3aaOpt1=[item[1:3] for item in list(marks3[3:4])]
        global q3aa
        if q3aaOpt2!=[]:
	        q3aa=random.choice([q3aaOpt1,q3aaOpt2])
        else:
        	q3aa=[item[1:3] for item in list(marks3[3:4])]
        q3aa=list(q3aa)
        global q4a
        q4a=[item[1:3] for item in list(marks3[4:5])]
        q4a=list(q4a)
        global q4aa
        q4aa=[item[1:3] for item in list(marks3[5:6])]
        q4aa=list(q4aa)
        global q5a
        q5a=[item[1:3] for item in list(marks3[6:7])]
        q5a=list(q5a)
        global q5aa
        q5aa=[item[1:3] for item in list(marks3[7:8])]
        q5aa=list(q5aa)

        global q1b
        q1b=[item[1:3] for item in list(marks4[0:1])]
        q1b=list(q1b)
        global q2b
        q2b=[item[1:3] for item in list(marks4[1:2])]
        q2b=list(q2b)
        global q3b
        q3b=[item[1:3] for item in list(marks4[2:3])]
        q3b=list(q3b)
        global q3bb
        q3bb=[item[1:3] for item in list(marks4[3:4])]
        q3bb=list(q3bb)
        global q4b
        q4b=[item[1:3] for item in list(marks4[4:5])]
        q4b=list(q4b)
        global q4bb
        q4bb=[item[1:3] for item in list(marks4[5:6])]
        q4bb=list(q4bb)
        global q5b
        q5b=[item[1:3] for item in list(marks4[6:7])]
        q5b=list(q5b)
        global q5bb
        q5bb=[item[1:3] for item in list(marks4[7:8])]
        q5bb=list(q5bb)
        print(q5bb)

        global q1c
        q1c=[item[1:3] for item in list(marks7[0:1])]
        q1c=list(q1c)
        global q2c
        q2c=[item[1:3] for item in list(marks7[1:2])]
        q2c=list(q2c)
        global q2cc
        q2cc=[item[1:3] for item in list(marks7[2:3])]
        q2cc=list(q2cc)
        global q3c
        q3c=[item[1:3] for item in list(marks7[3:4])]
        q3c=list(q3c)
        global q3cc
        q3cc=[item[1:3] for item in list(marks7[4:5])]
        q3cc=list(q3cc)
        global q4c
        q4c=[item[1:3] for item in list(marks7[5:6])]
        q4c=list(q4c)
        global q4cc
        q4cc=[item[1:3] for item in list(marks7[6:7])]
        q4cc=list(q4cc)
        global q5c
        q5c=[item[1:3] for item in list(marks7[7:8])]
        q5c=list(q5c)
        global q5cc
        q5cc=[item[1:3] for item in list(marks7[8:9])]
        q5cc=list(q5cc)
        flash("Question paper generated!","success")
        return render_template('paper.html', username=username,q1a=q1a,q1b=q1b,q1c=q1c,q2a=q2a,q2b=q2b,q2c=q2c,q2cc=q2cc,q3a=q3a,q3b=q3b,q3c=q3c,q3aa=q3aa,q3bb=q3bb,q3cc=q3cc,q4a=q4a,q4b=q4b,q4c=q4c,q4aa=q4aa,q4bb=q4bb,q4cc=q4cc,q5a=q5a,q5b=q5b,q5c=q5c,q5aa=q5aa,q5bb=q5bb,q5cc=q5cc, semester=semester,subject=subject,department=department,subjectCode=subjectCode,duration=duration,date=date,getPdf=getPdf)

    else:
        #root = tkinter.Tk()
        #root.withdraw()
        #messagebox.showinfo("Title", "Message")
        #win32api.MessageBox(0, 'hello', 'title')
        #pag.alert(text=msg, title="Couldn't generate question paper")
        if msg1!='' and msg2!='' and msg3!='':
            flash("Insert 3,4 and 7 marks Question", 'danger')
        elif msg1!='' and msg2!='' and msg3=='':
            flash("Insert 3 and 4 marks Question", 'danger')
        elif msg1!='' and msg2=='' and msg3!='':
            flash("Insert 3 and 7 marks Question", 'danger')
        elif msg1=='' and msg2!='' and msg3!='':
            flash("Insert 4 and 7 marks Question", 'danger')
        elif msg1=='' and msg2=='' and msg3!='':
            flash("Insert 7 marks Question", 'danger')
        elif msg1=='' and msg2!='' and msg3=='':
            flash("Insert 4 marks Question", 'danger')
        elif msg1!='' and msg2=='' and msg3=='':
            flash("Insert 3 marks Question", 'danger')
        
        return render_template("generatePaper.html",username=username)
    
"""

@app.route('/index/<string:username>/generate',methods=['POST','GET'])
def questionPaperB(username):
   # if request.method == 'POST':
        #semester = request.form.select['semester']
    
    global semester2
    global subject2
    global marks2
    global difficultyLevel2
    global number_of_Ques2
    global sectionB
    sectionB = 1
    semester2 = int(request.form.get('semester'))

    subject2 = request.form['subject']
    
    marks2 = request.form['marks2']
    difficultyLevel2 = request.form.get('difficultyLevel2')
    number_of_Ques2 = int(request.form['noOfQues2'])
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
    cur = db.cursor()
    cur.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks=%s AND Difficulty_level=%s order by rand() limit %s",(username,semester2,subject2,marks2,difficultyLevel2,number_of_Ques2))
    global dataB
    dataB = cur.fetchall()
    cur.close()
    dat = date.today()
    return redirect(url_for('generate',username=username))


@app.route('/index/<string:username>/generate',methods=['POST','GET'])
def questionPaperC(username):
   # if request.method == 'POST':
        #semester = request.form.select['semester']
    
    global sectionC
    sectionC = 1
    
    global semester3
    global subject3
    global marks3
    global difficultyLevel3
    global number_of_Ques3
    semester3 = int(request.form.get('semester'))

    subject3 = request.form['subject']
   
    marks3 = request.form['marks3']
    difficultyLevel3 = request.form.get('difficultyLevel3')
    number_of_Ques3 = int(request.form['noOfQues3'])
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
    cur = db.cursor()
    cur.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks=%s AND Difficulty_level=%s order by rand() limit %s",(username,semester3,subject3,marks3,difficultyLevel3,number_of_Ques3))
    global dataC
    dataC = cur.fetchall()
    cur.close()
    dat = date.today()
    return redirect(url_for('generate',username=username))
"""

        # return render_template("paper.html",date=date)
@app.route('/update/<string:username>',methods=['POST','GET'])
def update(username):
    if "username" in session:
        if request.method == 'POST':
            id_data = request.form['id']
            #semester = request.form.select['semester']
            subjectCode = int(request.form['subjectCode'])
            unit = int(request.form['unit'])
            marks = request.form['marks']
            difficultyLevel = request.form.get('difficultyLevel')
            question = request.form['question']
            cur = mydb.cursor()
            cur.execute("""
                UPDATE add_questions
                SET subject_code=%s, unit=%s, marks=%s, difficulty=%s, question=%s
                WHERE id=%s
                """, (subjectCode,unit,marks,difficultyLevel,question, id_data))
            flash("Question Updated Successfully","success")
            mydb.commit()
            return redirect(url_for('showQuestion',username=username))
    else:
        return redirect(url_for('register'))   
@app.route('/update/<string:username>/<string:subject_code>',methods=['POST','GET'])
def update1(username,subject_code):
    if "username" in session:
        if request.method == 'POST':
            id_data = request.form['id']
            #semester = request.form.select['semester']
            # subjectCode = int(request.form['subjectCode'])
            unit = int(request.form['unit'])
            marks = request.form['marks']
            # difficultyLevel = request.form.get('difficultyLevel')
            question = request.form['question']
            cur = mydb.cursor()
            cur.execute("""
                UPDATE add_questions
                SET unit=%s, marks=%s, question=%s
                WHERE id=%s
                """, (unit,marks,question, id_data))
            flash("Question Updated Successfully","success")
            mydb.commit()
            return redirect(url_for('que',username=username,subject_code=subject_code))
    else:
        return redirect(url_for('register')) 

@app.route('/<string:username>/generate_paper/pdf',methods=['POST'])
def PDFOfQuestionPaper(username,**args):
    if "username" not in session:
        return redirect(url_for('register'))
    # config = pdf.configuration(wkhtmltopdf="G:/AutoQuest/wkhtmltopdf.exe")
    config = pdf.configuration(wkhtmltopdf="G:/wkhtmltopdf/bin/wkhtmltopdf.exe")
 
    getPdf = 1
    html = render_template('paper.html',q1a=q1a,q1b=q1b,q1c=q1c,q2a=q2a,q2b=q2b,q2c=q2c,q2cc=q2cc,q3a=q3a,q3b=q3b,q3c=q3c,q3aa=q3aa,q3bb=q3bb,q3cc=q3cc,q4a=q4a,q4b=q4b,q4c=q4c,q4aa=q4aa,q4bb=q4bb,q4cc=q4cc,q5a=q5a,q5b=q5b,q5c=q5c,q5aa=q5aa,q5bb=q5bb,q5cc=q5cc, semester=semester,department=department,subject=subject,subjectCode=subjectCode,duration=duration,date=date,getPdf=getPdf)
    PDF = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode()),PDF)
    print(type(PDF))
    valueOfData =  PDF.getvalue()
    # print(valueOfData)
    headers = {
        'content-type': 'application.pdf',
        'content-disposition': 'attachment; filename=Question_Paper.pdf'}
    # print(headers)  
    # mycursor=mydb.cursor()
    # mycursor.execute("INSERT INTO papers (filename,data)values(%s,%s)",("filename.pdf",valueOfData))  
    # mydb.commit()
    return valueOfData, 200, headers



@app.route('/delete_data/<string:id>/<string:username>' ,methods=['POST','GET'])
def delete_data(id,username):
    if "username" not in session:
        return redirect(url_for('register'))
    mycursor = mydb.cursor()
    flash("Question Has Been Deleted Successfully","success")
    # if request.method=='POST':
    sql="delete from add_questions where id=%s"
    data=(id,)
    mycursor.execute(sql,data)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('showQuestion',username=username))

@app.route('/delete_data1/<string:id>/<string:username>/<string:subject_code>' ,methods=['POST'])
def delete_data1(id,username,subject_code):
    if "username" not in session:
        return redirect(url_for('register'))
    mycursor = mydb.cursor()
    flash("Question Has Been Deleted Successfully","success")
    if request.method=='POST':
        sql="delete from add_questions where id=%s"
        data=(id,)
        mycursor.execute(sql,data)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('que',username=username,subject_code=subject_code))

@app.route('/success/<string:username>', methods = ['POST','GET'])  
def success(username):
    if "username" not in session:
        return redirect(url_for('register'))
    mycursor = mydb.cursor()  
    if request.method == 'POST': 
        print("1") 
        f = request.files['file']  
        f.save(f.filename)  
        print("filetype",type(f))
        print(f)
        print(f.filename)
        subject_code=request.form['subject code']
        unit=request.form['unit']
        generate(output_format='plantuml', output_dir='C:/Users/asus/Downloads/AutoQuest/DB')
        aqg = aqgFunction
        inputTextPath =f.filename

        # inputTextPath = "E:/Project/sem7report/sql.txt"
        split_tup = os.path.splitext(inputTextPath)
        if split_tup[1] == '.pdf':
            readFile = open(inputTextPath, 'rb')
            inputText = PyPDF2.PdfFileReader(readFile)
            totalpage = inputText.numPages
            for i in range(totalpage):
                pageObject = inputText.getPage(i)
                textis = re.sub(r"\n", '', pageObject.extractText())
                questionList = aqg.aqgParse(textis, en_core_web_trf=textis)
                question=aqg.display(questionList)
                data=question.split('.')
                # print(data)
                for que in data:
                    if que!="":
                        mycursor.execute("SELECT * FROM add_questions WHERE Username=%s AND subject_code=%s AND question=%s",(username,subject_code,que))
                        # print(username,subject_code,question)
                        r=mycursor.fetchall()
                        # print(r,"!1111111111111")
                        recordFound=mycursor.rowcount
                        # print(recordFound)
                        if recordFound==1:
                            # flash("Record already exists",'danger')
                            return redirect(url_for('showQuestion',username=username)) 
                        elif recordFound==0:
                            # marks =[3, 4, 7]
                            # mark=random.choice(marks)
                            mycursor.execute("insert into add_questions(Username,subject_code,unit,marks,question,Auto)values(%s,%s,%s,%s,%s,%s)",(username,subject_code,unit,"1",que,'Automatic'))
                            mydb.commit()
                            # mycursor.close()
                            # flash("Question Inserted Successfully","success")
                        # return redirect(url_for('showQuestion',username=username))       
        else:
            readFile = open(inputTextPath, 'r+', encoding="utf8")
            inputText = readFile.read()
            questionList = aqg.aqgParse(inputText, en_core_web_trf=inputText)
            question=aqg.display(questionList)
            data=question.split('.')
            # print(data)
        
            for que in data:
                if que!="":
                    mycursor.execute("SELECT * FROM add_questions WHERE Username=%s AND subject_code=%s AND question=%s",(username,subject_code,que))
                    # print(username,subject_code,question)
                    r=mycursor.fetchall()
                    # print(r,"!1111111111111")
                    recordFound=mycursor.rowcount
                    # print(recordFound)
                    if recordFound==1:
                        # flash("Record already exists",'danger')
                        return redirect(url_for('showQuestion',username=username)) 
                    elif recordFound==0:
                        # import random
                        # marks =[3, 4, 7]
                        # mark=random.choice(marks)
                        mycursor.execute("insert into add_questions(Username,subject_code,unit,marks,question,Auto)values(%s,%s,%s,%s,%s,%s)",(username,subject_code,unit,"1",que,'Automatic'))
                        mydb.commit()
                        # mycursor.close()
                        # flash("Question Inserted Successfully","success")
                        # return redirect(url_for('showQuestion',username=username))       
                
        # # aqg.display(questionList)
        flash("Question Inserted Successfully","success")
        return redirect(url_for('showQuestion',username=username)) 




if __name__ == "__main__":
    app.run(debug=True)
