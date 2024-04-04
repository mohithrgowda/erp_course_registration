from flask import Flask, render_template,request,make_response,send_file,session
from flask_session import Session
from werkzeug.utils import secure_filename
import os
import mysql.connector
from mysql.connector import Error
from openpyxl import Workbook
from io import BytesIO
#from pymysql import *
#import xlwt
#import pandas.io.sql as sql
import json
import random
#Attendance Dates
from datetime import datetime
from datetime import date
import calendar
import pandas as pd
#import datetime

from datetime import date
import csv
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import base64

#install wkhtmltox-0.12.4_msvc2015-win64.exe,pip install pdfkit
import pdfkit
from num2words import num2words
#File upload
from werkzeug.utils import secure_filename

nhcount=0
userrole=''
rolename=''
app= Flask(__name__)
empcodelist=[]
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    return render_template('login1.html')

@app.route('/login')
def login():
    return render_template('login1.html')





#-------------------------------Admin START-----------------------------------------------------------------



@app.route('/aadminaddstu', methods =  ['GET','POST'])
def aadminaddstu():
    return render_template('aadminaddstu.html')


@app.route('/aadminaddhod', methods =  ['GET','POST'])
def aadminaddhod():
    return render_template('aadminaddhod.html')


@app.route('/aaddrounds', methods =  ['GET','POST'])
def aaddrounds():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
   
    sql_Query = "select * from rounddata"    
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    return render_template('aaddrounds.html',rdata=rdata)


#Add new round routing
@app.route('/addnewround')
def addnewround():
    sdate=request.args['sdate']
    edate=request.args['edate']
    round1=request.args['round']
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into rounddata (Sdate ,Edate ,Round) values('"+sdate+"','"+edate+"','"+round1+"')"
    cursor.execute(sql_Query)
    
    connection.commit()
    connection.close()
    cursor.close()
    resp = make_response(json.dumps("Success"))
    return resp


#Delete round routing
@app.route('/rounddelete')
def rounddelete():
    rid=request.args['id']

    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from rounddata where id='"+rid+"'"
    cursor.execute(sql_Query)    

    sql_Query = "select * from rounddata"    
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    
    return render_template('aaddrounds.html',rdata=rdata)


@app.route('/hmentorapplist')
def hmentorapplist():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')     
    cursor = connection.cursor()

    
    #sql_Query = "SELECT * from stuelectives where Stat='Approved'  and USN in (Select USN from studentdata where Dept ='"+session["dept"]+"')"
    sql_Query="Select Id,Uname from mentordata where Uname not in (Select Uname from stualloc where USN in (SELECT USN FROM `stupecelectives` where Stat='Pending')) and Stat='Pending'"
    cursor.execute(sql_Query)
    elecdata = cursor.fetchall()

    
    connection.close()
    cursor.close()
    return render_template('hmentorapplist.html',elecdata=elecdata)



@app.route('/uploadstudentdata', methods =  ['GET','POST'])
def uploadstudentdata():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')
        cursor = connection.cursor()
    
        prod_mas = request.files['prod_mas']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("D:/Upload/", filename))

        #csv reader
        fn = os.path.join("D:/Upload/", filename)

        # initializing the titles and rows list 
        fields = [] 
        rows = []
        
        with open(fn, 'r') as csvfile:
            # creating a csv reader object 
            csvreader = csv.reader(csvfile)  
  
            # extracting each data row one by one 
            for row in csvreader:
                rows.append(row)
                print(row)

        try:     
            #print(rows[1][1])       
            for row in rows[1:]: 
                # parsing each column of a row
                if row[0][0]!="":
                    i=0
                    query="";
                    query="insert into studentdata values (";
                    print(len(row))
                    #for col in row:
                    colval=len(row)+1
                    while (i <colval):
                        if i==3:
                            query =query+"'student@1234',"
                            i=i+1
                        else:
                            if i>3:
                                query =query+"'"+row[i-1]+"',"
                            else:
                                query =query+"'"+row[i]+"',"
                                
                            i=i+1
                        #print(query)
                        #print(i)
                    query =query[:-1]
                    query=query+");"
                print("query :"+str(query), flush=True)
                cursor.execute(query)
                connection.commit()
        except:
            print("An exception occurred")
        csvfile.close()
        
        print("Filename :"+str(prod_mas), flush=True)       
        
        
        connection.close()
        cursor.close()
        return render_template('aadminaddstu.html',data="Data loaded successfully")



@app.route('/cleardataset', methods = ['POST'])
def cleardataset():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')
    cursor = connection.cursor()
    query="delete from studentdata"
    cursor.execute(query)
    connection.commit()      
    connection.close()
    cursor.close()
    return render_template('aadminaddstu.html')


@app.route('/uploadhoddata', methods =  ['GET','POST'])
def uploadhoddata():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')
        cursor = connection.cursor()
    
        prod_mas = request.files['prod_mas']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("D:/Upload/", filename))

        #csv reader
        fn = os.path.join("D:/Upload/", filename)

        # initializing the titles and rows list 
        fields = [] 
        rows = []
        
        with open(fn, 'r') as csvfile:
            # creating a csv reader object 
            csvreader = csv.reader(csvfile)  
  
            # extracting each data row one by one 
            for row in csvreader:
                rows.append(row)
                print(row)

        try:     
            #print(rows[1][1])       
            for row in rows[1:]: 
                # parsing each column of a row
                if row[0][0]!="":                
                    query="";
                    query="insert into hoddata values (";
                    for col in row: 
                        query =query+"'"+col+"',"
                    query =query[:-1]
                    query=query+");"
                print("query :"+str(query), flush=True)
                cursor.execute(query)
                connection.commit()
        except:
            print("An exception occurred")
        csvfile.close()
        
        print("Filename :"+str(prod_mas), flush=True)       
        
        
        connection.close()
        cursor.close()
        return render_template('aadminaddhod.html',data="Data loaded successfully")



@app.route('/clearhoddataset', methods = ['POST'])
def clearhoddataset():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')
    cursor = connection.cursor()
    query="delete from hoddata"
    cursor.execute(query)
    connection.commit()      
    connection.close()
    cursor.close()
    return render_template('aadminaddhod.html')


#-------------------------------Mentor START-----------------------------------------------------------------

@app.route('/mentorhome')
def mentorhome():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')     
    cursor = connection.cursor()

    
    sql_Query = "SELECT count(*) from stualloc where Uname='"+session["uname"]+"'"
    cursor.execute(sql_Query)
    tile1data = cursor.fetchall()
    tile1data=tile1data[0][0]

    sql_Query = "SELECT * from stualloc where Uname='"+session["uname"]+"'"
    cursor.execute(sql_Query)
    studata = cursor.fetchall()

    
    connection.close()
    cursor.close()
    return render_template('mentorhome.html',tile1data=tile1data,studata=studata)

@app.route('/mapprovesub')
def mapprovesub():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')     
    cursor = connection.cursor()

    r1date=''
    r2date=''
    r3date=''
    sql_Query = "SELECT Sdate from rounddata where Round='1'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r1date=''
    try:
        r1date=rdata[0][0]
    except:
        r1date=''
    
    sql_Query = "SELECT Sdate from rounddata where Round='2'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r2date=''
    try:
        r2date=rdata[0][0]
    except:
        r2date=''
    
    sql_Query = "SELECT Sdate from rounddata where Round='3'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r3date=''
    try:
        r3date=rdata[0][0]
    except:
        r3date=''

    stucgpa=float(session["cgpa"])
    print(stucgpa)
    from datetime import date

    today = date.today()
    curdate = today.strftime("%Y-%m-%d")
    print(curdate)
    elecdata=[]
    if(r1date==curdate):
        elecdata=[]
    elif r2date==curdate:
        elecdata=[]
    elif (r3date==curdate):
        elecdata=[]
    else:        
        sql_Query = "SELECT * from stuelectives where Stat='Pending' and USN in (Select USN from stualloc where Uname='"+session["uname"]+"')"
        cursor.execute(sql_Query)
        elecdata = cursor.fetchall()

    sql_Query = "SELECT * from stupecelectives where Stat='Pending' and USN in (Select USN from stualloc where Uname='"+session["uname"]+"')"
    cursor.execute(sql_Query)
    pecdata = cursor.fetchall()
    connection.close()
    cursor.close()
    return render_template('mapprovesub.html',elecdata=elecdata,pecdata=pecdata)

@app.route('/mapprovesubval')
def mapprovesubval():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')     
    cursor = connection.cursor()
    rid=request.args['id']

    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "update stuelectives set Stat='Approved' where id='"+rid+"'"
    cursor.execute(sql_Query)   

    
    
    r1date=''
    r2date=''
    r3date=''
    sql_Query = "SELECT Sdate from rounddata where Round='1'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r1date=''
    try:
        r1date=rdata[0][0]
    except:
        r1date=''
    
    sql_Query = "SELECT Sdate from rounddata where Round='2'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r2date=''
    try:
        r2date=rdata[0][0]
    except:
        r2date=''
    
    sql_Query = "SELECT Sdate from rounddata where Round='3'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r3date=''
    try:
        r3date=rdata[0][0]
    except:
        r3date=''

    stucgpa=float(session["cgpa"])
    print(stucgpa)
    from datetime import date

    today = date.today()
    curdate = today.strftime("%Y-%m-%d")
    print(curdate)
    elecdata=[]
    if(r1date==curdate):
        elecdata=[]
    elif r2date==curdate:
        elecdata=[]
    elif (r3date==curdate):
        elecdata=[]
    else:        
        sql_Query = "SELECT * from stuelectives where Stat='Pending' and USN in (Select USN from stualloc where Uname='"+session["uname"]+"')"
        cursor.execute(sql_Query)
        elecdata = cursor.fetchall()

    sql_Query = "SELECT * from stupecelectives where Stat='Pending' and USN in (Select USN from stualloc where Uname='"+session["uname"]+"')"
    cursor.execute(sql_Query)
    pecdata = cursor.fetchall()
    connection.close()
    cursor.close()
    return render_template('mapprovesub.html',elecdata=elecdata,pecdata=pecdata)


@app.route('/approvementor')
def approvementor():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')     
    cursor = connection.cursor()
    rid=request.args['id']

    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "update mentordata set Stat='Approved' where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    
    
    #sql_Query = "SELECT * from stuelectives where Stat='Approved'  and USN in (Select USN from studentdata where Dept ='"+session["dept"]+"')"
    sql_Query="Select Id,Uname from mentordata where Uname not in (Select Uname from stualloc where USN in (SELECT USN FROM `stupecelectives` where Stat='Pending')) and Stat='Pending';"
    cursor.execute(sql_Query)
    elecdata = cursor.fetchall()

    
    connection.close()
    cursor.close()
    return render_template('hmentorapplist.html',elecdata=elecdata)

@app.route('/mapprovepecsubval')
def mapprovepecsubval():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')     
    cursor = connection.cursor()
    rid=request.args['id']
    
    sql_Query = "update stupecelectives set Stat='Approved' where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()

    
    
    r1date=''
    r2date=''
    r3date=''
    sql_Query = "SELECT Sdate from rounddata where Round='1'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r1date=''
    try:
        r1date=rdata[0][0]
    except:
        r1date=''
    
    sql_Query = "SELECT Sdate from rounddata where Round='2'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r2date=''
    try:
        r2date=rdata[0][0]
    except:
        r2date=''
    
    sql_Query = "SELECT Sdate from rounddata where Round='3'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r3date=''
    try:
        r3date=rdata[0][0]
    except:
        r3date=''

    stucgpa=float(session["cgpa"])
    print(stucgpa)
    from datetime import date

    today = date.today()
    curdate = today.strftime("%Y-%m-%d")
    print(curdate)
    elecdata=[]
    if(r1date==curdate):
        elecdata=[]
    elif r2date==curdate:
        elecdata=[]
    elif (r3date==curdate):
        elecdata=[]
    else:        
        sql_Query = "SELECT * from stuelectives where Stat='Pending' and USN in (Select USN from stualloc where Uname='"+session["uname"]+"')"
        cursor.execute(sql_Query)
        elecdata = cursor.fetchall()

    sql_Query = "SELECT * from stupecelectives where Stat='Pending' and USN in (Select USN from stualloc where Uname='"+session["uname"]+"')"
    cursor.execute(sql_Query)
    pecdata = cursor.fetchall()
    connection.close()
    cursor.close()
    return render_template('mapprovesub.html',elecdata=elecdata,pecdata=pecdata)

#-------------------------------Mentor END-----------------------------------------------------------------



@app.route('/sdownloadpdf')
def sdownloadpdf():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    
    
    sql_Query = "SELECT * from studentdata where USN='"+session["usn"]+"'"
    cursor.execute(sql_Query)
    studentdata = cursor.fetchall()

    sql_Query = "SELECT * from subjectdata where Course='"+session["dept"]+"' and (stype<>'PEC(Professional Elective Course)' and stype<>'OEC(Open Elective Course)')  and Sem='"+session["sem"]+"'"
    cursor.execute(sql_Query)
    subdata = cursor.fetchall()
    #print(subdata)
    selelecdata=[]
    
           
    sql_Query = "SELECT * from stuelectives where USN='"+session["usn"]+"'"
    cursor.execute(sql_Query)
    selelecdata = cursor.fetchall()
    
    sql_Query = "SELECT * from stupecelectives where USN='"+session["usn"]+"'"
    cursor.execute(sql_Query)
    selelecdata = cursor.fetchall()
    #print(selelecdata)

    sql_Query = "SELECT * from backlogdata where USN='"+session["usn"]+"'"
    cursor.execute(sql_Query)
    backlogdata = cursor.fetchall()

    
    
    connection.close()
    cursor.close()
    return render_template('sdownloadpdf.html',studentdata=studentdata,subdata=subdata,selelecdata=selelecdata,backlogdata=backlogdata)
@app.route('/schooseelectives')
def schooseelectives():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    elecdata=[]
    pecdata=[]
    subdata=[]
    oecdata=[]
    r1date=''
    r2date=''
    r3date=''
    sql_Query = "SELECT Sdate from rounddata where Round='1'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r1date=''
    try:
        r1date=rdata[0][0]
    except:
        r1date=''
    print(r1date)
    
    sql_Query = "SELECT Sdate from rounddata where Round='2'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r2date=''
    try:
        r2date=rdata[0][0]
    except:
        r2date=''
    print(r2date)
    
    sql_Query = "SELECT Sdate from rounddata where Round='3'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r3date=''
    try:
        r3date=rdata[0][0]
    except:
        r3date=''
    print(r3date)

    stucgpa=float(session["cgpa"])
    print(stucgpa)
    from datetime import date

    today = date.today()
    curdate = today.strftime("%Y-%m-%d")
    print(curdate)

    sql_Query = "SELECT * from stuelectives where USN='"+session["usn"]+"'"
    cursor.execute(sql_Query)
    elecdata = cursor.fetchall()
    print(elecdata)
    
    print('-----------------------')
    sql_Query = "SELECT * from stupecelectives where USN='"+session["usn"]+"'"
    cursor.execute(sql_Query)
    pecdata = cursor.fetchall()
    print(pecdata)

    if(r1date==curdate and stucgpa>7):       
        print('-----------R1------------')

        if(len(elecdata)==0):
            sql_Query = "SELECT * from subjectdata where Exclusion not like '%"+session["dept"]+"%' and  stype='OEC(Open Elective Course)' and Sem='"+session["sem"]+"'"
            cursor.execute(sql_Query)
            oecdata = cursor.fetchall()
            print(subdata)
        print(len(pecdata))
            
    
    if(r2date==curdate and stucgpa<=7):       
        print('-----------R2------------')

        if(len(elecdata)==0):
            sql_Query = "SELECT * from subjectdata where Exclusion not like '%"+session["dept"]+"%' and  stype='OEC(Open Elective Course)'  and Sem='"+session["sem"]+"'"
            cursor.execute(sql_Query)
            oecdata = cursor.fetchall()
            print(subdata)
        print(len(pecdata))
            
    
    if(r3date==curdate):       
        print('-----------R3------------')

        if(len(elecdata)==0):
            sql_Query = "SELECT * from subjectdata where Exclusion not like '%"+session["dept"]+"%' and  stype='OEC(Open Elective Course)' and Sem='"+session["sem"]+"'"
            cursor.execute(sql_Query)
            oecdata = cursor.fetchall()
            print(subdata)
        print(len(pecdata))
    if(len(pecdata)==0):
        sql_Query = "SELECT * from subjectdata where Course='"+session["dept"]+"' and  stype='PEC(Professional Elective Course)' and Sem='"+session["sem"]+"'"
        print(sql_Query)
        cursor.execute(sql_Query)
        pecdata = cursor.fetchall()
        print(pecdata)
    else:
        pecdata=[]

    connection.close()
    cursor.close()
    
    return render_template('schooseelectives.html',oecdata=oecdata,pecdata=pecdata)

@app.route('/uploadpref', methods = ['GET','POST'])
def uploadpref():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')
        cursor = connection.cursor()
        import random
        usn=session["usn"]
        val=random.randint(1,5)
        for i in range(1,10):
            if i==val:
                print(i)
                     
                checked=request.form.get(str(i))
                print(checked) 
                scode=request.form.get('scode'+str(i))
                print(scode)        
                sub=request.form.get('sub'+str(i))
                print(sub) 
                cred=request.form.get('cred'+str(i))
                print(cred)
                sem=request.form.get('sem'+str(i))
                print(sem)
                
                if(checked=='on'):
                    sql_Query = "insert into stuelectives(Scode,Subject,Sem,Credits,USN,Stat) values('"+str(scode)+"','"+str(sub)+"','"+str(sem)+"','"+str(cred)+"','"+str(usn)+"','Pending')"
                    print(sql_Query)
                    cursor.execute(sql_Query)
                '''
                sql_Query = "delete from stuelectives where Subject='None'"
                print(sql_Query)
                cursor.execute(sql_Query)
                '''
                connection.commit() 
        connection.close()
        cursor.close()
        #return render_template('schooseelectives.html')
        resp = make_response(json.dumps("Success"))
        return resp

@app.route('/uploadpref1', methods = ['GET','POST'])
def uploadpref1():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')
        cursor = connection.cursor()
        import random
        usn=session["usn"]
        for i in range(1,10):
            print(i)
                 
            checked=request.form.get(str(i))
            print(checked) 
            scode=request.form.get('scode'+str(i))
            print(scode)        
            sub=request.form.get('sub'+str(i))
            print(sub) 
            cred=request.form.get('cred'+str(i))
            print(cred)
            sem=request.form.get('sem'+str(i))
            print(sem)
            
            if(checked=='on'):
                sql_Query = "insert into stupecelectives(Scode,Subject,Sem,Credits,USN,Stat) values('"+str(scode)+"','"+str(sub)+"','"+str(sem)+"','"+str(cred)+"','"+str(usn)+"','Pending')"
                print(sql_Query)
                cursor.execute(sql_Query)
            '''
            sql_Query = "delete from stuelectives where Subject='None'"
            print(sql_Query)
            cursor.execute(sql_Query)
            '''
            connection.commit() 
        connection.close()
        cursor.close()
        #return render_template('schooseelectives.html')
        resp = make_response(json.dumps("Success"))
        return resp

@app.route('/sviewsub')
def sviewsub():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    
    
    sql_Query = "SELECT * from studentdata where USN='"+session["usn"]+"'"
    cursor.execute(sql_Query)
    studentdata = cursor.fetchall()

    sql_Query = "SELECT * from subjectdata where Course='"+session["dept"]+"' and (stype<>'PEC(Professional Elective Course)' and stype<>'OEC(Open Elective Course)')  and Sem='"+session["sem"]+"'"
    cursor.execute(sql_Query)
    subdata = cursor.fetchall()
    #print(subdata)
    selelecdata=[]
    
    
    r1date=''
    r2date=''
    r3date=''
    sql_Query = "SELECT Sdate from rounddata where Round='1'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r1date=''
    try:
        r1date=rdata[0][0]
    except:
        r1date=''
    
    sql_Query = "SELECT Sdate from rounddata where Round='2'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r2date=''
    try:
        r2date=rdata[0][0]
    except:
        r2date=''
    
    sql_Query = "SELECT Sdate from rounddata where Round='3'"
    cursor.execute(sql_Query)
    rdata = cursor.fetchall()
    r3date=''
    try:
        r3date=rdata[0][0]
    except:
        r3date=''

    stucgpa=float(session["cgpa"])
    print(stucgpa)
    from datetime import date

    today = date.today()
    curdate = today.strftime("%Y-%m-%d")
    print(curdate)
    elecdata=[]
    if(r1date==curdate):
        elecdata=[]
    elif r2date==curdate:
        elecdata=[]
    elif (r3date==curdate):
        elecdata=[]
    else:        
        sql_Query = "SELECT * from stuelectives where USN='"+session["usn"]+"'"
        cursor.execute(sql_Query)
        selelecdata = cursor.fetchall()
    
    sql_Query = "SELECT * from stupecelectives where USN='"+session["usn"]+"'"
    cursor.execute(sql_Query)
    selelecdata = cursor.fetchall()
    #print(selelecdata)

    sql_Query = "SELECT * from backlogdata where USN='"+session["usn"]+"'"
    cursor.execute(sql_Query)
    backlogdata = cursor.fetchall()

    
    connection.close()
    cursor.close()
    return render_template('sviewsub.html',studentdata=studentdata,subdata=subdata,selelecdata=selelecdata,backlogdata=backlogdata)


@app.route('/hmentors')
def hmentors():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    
    sql_Query = "select * from mentordata where Course='"+session["dept"]+"'" 
    cursor.execute(sql_Query)
    mentordata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    
    return render_template('hmentors1.html',mentordata=mentordata,dept=session["dept"])

@app.route('/studenthome')
def studenthome():    
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')     
    cursor = connection.cursor()

    
    sql_Query = "SELECT * from studentdata where USN='"+session["usn"]+"'"
    cursor.execute(sql_Query)
    studentdata = cursor.fetchall()
    
    connection.close()
    cursor.close()
    return render_template('studenthome.html',studentdata=studentdata)

@app.route('/hodhome')
def hodhome():
    '''
    dept=request.args['dept']
    if dept=="CS":
        dept="Computer Science"
    session["dept"]=dept
    '''
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')     
    cursor = connection.cursor()

    
    sql_Query = "SELECT count(*) from studentdata where Dept='"+session["dept"]+"'"
    cursor.execute(sql_Query)
    tile1data = cursor.fetchall()
    tile1data=tile1data[0][0]

    
    sql_Query = "SELECT count(*) from mentordata where Course='"+session["dept"]+"'"
    cursor.execute(sql_Query)
    tile2data = cursor.fetchall()
    tile2data=tile2data[0][0]

    
    connection.close()
    cursor.close()
    return render_template('hodhome.html',tile1data=tile1data,tile2data=tile2data)

@app.route('/hallocstudents')
def hallocstudents():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    
    sql_Query = "select USN from studentdata where Dept='"+session["dept"]+"'"   
    cursor.execute(sql_Query)
    studata = cursor.fetchall()
    
    sql_Query = "select Uname from mentordata where Course='"+session["dept"]+"'"    
    cursor.execute(sql_Query)
    mendata = cursor.fetchall()

    sql_Query = "select s.Id,s.USN, st.Name,s.Uname from stualloc s, studentdata st where st.Dept='"+session["dept"]+"' and s.USN=st.USN"    
    cursor.execute(sql_Query)
    stumendata = cursor.fetchall()
    
    
    connection.commit()
    connection.close()
    cursor.close()
    
    return render_template('hallocstudents.html',studata=studata,mendata=mendata,stumendata=stumendata)


#------------------------------------------------------------------------------------------------------------


@app.route('/asubjects')
def asubjects():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    
    sql_Query = "select * from subjectdata"    
    cursor.execute(sql_Query)
    subdata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    
    return render_template('asubjects.html',subdata=subdata)

#Add new subject routing
@app.route('/addnewsub')
def addnewsub():
    sub=request.args['sub']
    stype=request.args['stype']
    course=request.args['course']
    sem=request.args['sem']
    credit=request.args['credit']
    subcode=request.args['subcode']
    seats=request.args['seats']
    exclusion=request.args['exclusion']
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into subjectdata (Subject,Stype,Course,Sem,Credit,SubCode,Seats,Exclusion) values('"+sub+"','"+stype+"','"+course+"','"+sem+"','"+credit+"','"+subcode+"',"+seats+",'"+exclusion+"')"
    cursor.execute(sql_Query)
    
    connection.commit()
    connection.close()
    cursor.close()
    resp = make_response(json.dumps("Success"))
    return resp


#Delete subject routing
@app.route('/subdelete')
def qualdelete():
    rid=request.args['id']

    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from subjectdata where id='"+rid+"'"
    cursor.execute(sql_Query)    

    sql_Query = "select * from subjectdata"    
    cursor.execute(sql_Query)
    subdata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    
    return render_template('asubjects.html',subdata=subdata)

#------------------------------------------------------------------------------------------------------------


#Add add student mentor
@app.route('/addstumentor')
def addstumentor():
    mname=request.args['mname']
    usn=request.args['usn']
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into stualloc (Uname,USN) values('"+mname+"','"+usn+"')"
    cursor.execute(sql_Query)
    
    connection.commit()
    connection.close()
    cursor.close()
    resp = make_response(json.dumps("Success"))
    return resp


#Delete subject routing
@app.route('/stumentordelete')
def stumentordelete():
    rid=request.args['id']

    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from stualloc where id='"+rid+"'"
    cursor.execute(sql_Query)

    sql_Query = "select USN from studentdata where Dept='"+session["dept"]+"'"   
    cursor.execute(sql_Query)
    studata = cursor.fetchall()
    
    sql_Query = "select Uname from mentordata where Course='"+session["dept"]+"'"    
    cursor.execute(sql_Query)
    mendata = cursor.fetchall()

    
    sql_Query = "select s.Id,s.USN, st.Name,s.Uname from stualloc s, studentdata st where st.Dept='"+session["dept"]+"' and s.USN=st.USN"     
    cursor.execute(sql_Query)
    mentordata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()

    return render_template('hallocstudents.html',studata=studata,mendata=mendata,stumendata=mentordata)
#------------------------------------------------------------------------------------------------------------


#Add new mentor routing
@app.route('/addnewmentor')
def addnewmentor():
    mname=request.args['mname']
    course=request.args['course']
    uname=request.args['uname']
    sem=request.args['sem']
    pswd=request.args['pswd']
    email=request.args['email']
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into mentordata (Mname,Course,Sem,Uname,Pswd,Email) values('"+mname+"','"+course+"','"+sem+"','"+uname+"','"+pswd+"','"+email+"')"
    cursor.execute(sql_Query)
    
    connection.commit()
    connection.close()
    cursor.close()
    resp = make_response(json.dumps("Success"))
    return resp


#Delete subject routing
@app.route('/mentordelete')
def mentordelete():
    rid=request.args['id']

    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from mentordata where id='"+rid+"'"
    cursor.execute(sql_Query)    

    sql_Query = "select * from mentordata"    
    cursor.execute(sql_Query)
    mentordata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    dept=session["dept"]
    
    return render_template('hmentors1.html',mentordata=mentordata,dept=dept)

#-------------------------------------------------------------------------------------------------

#Add new subject routing
@app.route('/addnewblog')
def addnewblog():
    sub=request.args['sub']
    course=request.args['course']
    sem=request.args['sem']
    usn=request.args['usn']
    scode=request.args['scode']
    credits=request.args['credits']
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into backlogdata  (USN,Course,Sem,Subject,Scode,Credits) values('"+usn+"','"+course+"','"+sem+"','"+sub+"','"+scode+"','"+credits+"')"
    cursor.execute(sql_Query)
    
    connection.commit()
    connection.close()
    cursor.close()
    resp = make_response(json.dumps("Success"))
    return resp


#Delete subject routing
@app.route('/blogdelete')
def blogdelete():
    rid=request.args['id']

    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from backlogdata where id='"+rid+"'"
    cursor.execute(sql_Query)    

    sql_Query = "select * from backlogdata"    
    cursor.execute(sql_Query)
    blogdata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    
    return render_template('abacklogs.html',blogdata=blogdata)

@app.route('/abacklogs')
def abacklogs():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    
    sql_Query = "select * from backlogdata"    
    cursor.execute(sql_Query)
    bdata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    
    return render_template('abacklogs.html',blogdata=bdata)

@app.route('/aelectives')
def aelectives():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor(buffered=True)
    
    sql_Query = "select * from subjectdata where Stype='OEC(Open Elective Course)' or Stype='PEC(Professional Elective Course)' or Stype='PCC(Professional Core Course)'"    
    cursor.execute(sql_Query)
    subdata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    
    return render_template('aelectives.html',subdata=subdata)

@app.route('/adminhome')
def adminhome():
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')     
    cursor = connection.cursor()

    
    sql_Query = "SELECT count(*) from studentdata"
    cursor.execute(sql_Query)
    tile1data = cursor.fetchall()
    tile1data=tile1data[0][0]

    
    sql_Query = "SELECT count(*) from subjectdata "
    cursor.execute(sql_Query)
    tile2data = cursor.fetchall()
    tile2data=tile2data[0][0]

    
    sql_Query = "SELECT count(*) from mentordata"
    cursor.execute(sql_Query)
    tile3data = cursor.fetchall()
    tile3data=tile3data[0][0]

    
    connection.close()
    cursor.close()
    return render_template('adminhome.html',tile1data=tile1data,tile2data=tile2data,tile3data=tile3data)


@app.route('/logdata')
def logdata():
    usn=request.args['name']
    pswd=request.args['passwrd']
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor()
    sql_Query = "SELECT * from studentdata where USN='"+str(usn)+"' and Pswd='"+str(pswd)+"'"
    print(sql_Query)
    cursor.execute(sql_Query)
    studentdata = cursor.fetchall()
    print(len(studentdata))
    connection.close()
    cursor.close()
    if(len(studentdata)>0):
       session["usn"]=usn
       session["dept"]=studentdata[0][2]
       session["name"]=studentdata[0][1]
       session["cgpa"]=studentdata[0][4]
       session["sem"]=studentdata[0][5]
       session["phone"]=studentdata[0][6]
       resp = make_response(json.dumps("Student"))
       print('aaa')
       return resp
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor()
    sql_Query = "SELECT * from hoddata where Uname='"+str(usn)+"' and Pswd='"+str(pswd)+"'"
    print(sql_Query)
    cursor.execute(sql_Query)
    studentdata = cursor.fetchall()
    print(len(studentdata))
    connection.close()
    cursor.close()
    if(len(studentdata)>0):
       session["dept"]=studentdata[0][3]
       print(session["dept"])
       resp = make_response(json.dumps("HOD"))
       print('aaa')
       return resp
    
    connection = mysql.connector.connect(host='localhost',database='peserpdb',user='root',password='')    
    cursor = connection.cursor()
    sql_Query = "SELECT * from mentordata where Uname='"+str(usn)+"' and Pswd='"+str(pswd)+"'"
    print(sql_Query)
    cursor.execute(sql_Query)
    studentdata = cursor.fetchall()
    print(len(studentdata))
    connection.close()
    cursor.close()
    if(len(studentdata)>0):        
       session["course"]=studentdata[0][2]
       session["sem"]=studentdata[0][3]
       session["uname"]=usn
       session["email"]=studentdata[0][6]
       resp = make_response(json.dumps("Mentor"))
       print('aaa')
       return resp
    else:
       resp = make_response(json.dumps("Failure"))
       return resp


if __name__ == "__main__":
  #port = int(os.environ.get("PORT", 80))
  app.jinja_env.cache = {}
  app.run(debug=True)
