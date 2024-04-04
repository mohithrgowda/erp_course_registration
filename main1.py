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
#Master Page
from masterpage import maddsow,mfetchsow,mdeletesow,mupdatesow
from masterpage import maddempcat,mfetchempcat,mupdateempcat,mdeleteempcat
from masterpage import mupdatepayroll,mfetchpayroll,mfetchmgrpersonaldata
from masterpage import mfetchprocdata,mfetchemplist,mfetchempproclist,mfetchtimedata
from masterpage import mfetchroles,mfetchmenus,mfetchroleusers,mfetchuserswithempcode
from masterpage import mfetchlanguages,mfetchidproofs,mfetchdepartments,mfetchpositions,mfetchqualifications,mfetchbanks,mfetchholidays,mfetchipvals,mfetchweblogins,mfetchprocsalrange
from masterpage import mfetchproc,maddproc,mupdateproc,mdeleteproc,mfetchmgr_amgr,mfetchrec_procdata
from masterpage import mfetchpaytypes,mfetchshifttimings
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

def monthname(monnum):
    month = date(1900, int(monnum), 1).strftime('%b')
    return month

def monthnum(monname):
       month_number = datetime.strptime(monname, '%b').month
       return month_number

def convertsectotime(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)

#*****************************************Master Pages Start*******************************************************
@app.route('/chngpswd')
def chngpswd():
    return render_template('chngpswd.html')

@app.route('/changepswd')
def changepswd():
    ru_email=request.args['ru_email']
    ru_cpswd=request.args['ru_cpswd']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "update lkpmapuserrole set pswd='"+ru_cpswd+"' where email='"+ru_email+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps("Success"))
    return resp

#--------------------------------------------------------------------
#Process Salary Range creation page
@app.route('/processsal')
def processsal():
    procsalrangedata=mfetchprocsalrange()
    return render_template('processsalrange.html',procsalrangedata=procsalrangedata)


#Language creation page
@app.route('/languages')
def languages():
    languagesdata=mfetchlanguages()
    return render_template('languages.html',languagesdata=languagesdata)

#Add new language routing
@app.route('/addnewlang')
def addnewlang():
    lang=request.args['lang']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into lkplanguages(lang) values('"+lang+"')"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    languagesdata=mfetchlanguages()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps("Success"))
    return resp


#Delete language routing
@app.route('/langdelete')
def langdelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkplanguages where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    languagesdata=mfetchlanguages()
    return render_template('languages.html',languagesdata=languagesdata)


#------------------------------------------------------------------------------------------------------------

#weblogins creation page
@app.route('/weblogins')
def weblogins():
    weblogindata=mfetchweblogins()
    return render_template('weblogins.html',weblogindata=weblogindata)

#Add new language routing
@app.route('/addnewweblogin')
def addnewweblogin():
    ru_email=request.args['ru_email']
    ru_pswd=request.args['ru_pswd']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into lkpweblogins(email,pswd) values('"+ru_email+"','"+ru_pswd+"')"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    weblogindata=mfetchweblogins()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps("Success"))
    return resp


#Delete language routing
@app.route('/weblogindelete')
def weblogindelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkpweblogins where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    weblogindata=mfetchweblogins()
    return render_template('weblogins.html',weblogindata=weblogindata)


#------------------------------------------------------------------------------------------------------------

#Holiday creation page
@app.route('/holidaycal')
def holidaycal():
    holidaydata=mfetchholidays()
    return render_template('holidaycal.html',holidaydata=holidaydata)

#Add new language routing
@app.route('/addnewhdate')
def addnewhdate():
    hname=request.args['hname']
    dated=request.args['dated']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into lkpholidays(holidayname,holidaydate) values('"+hname+"','"+dated+"')"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    holidaydata=mfetchholidays()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps("Success"))
    return resp


#Delete language routing
@app.route('/hdatadelete')
def hdatadelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkpholidays where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    holidaydata=mfetchholidays()
    return render_template('holidaycal.html',holidaydata=holidaydata)


#------------------------------------------------------------------------------------------------------------

#IP creation page
@app.route('/ipaddrs')
def ipaddrs():
    ipaddressdata=mfetchipvals()
    return render_template('ipaddrs.html',ipaddressdata=ipaddressdata)

#Add new IP routing
@app.route('/addnewip')
def addnewip():
    ipaddr=request.args['ipaddr']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into lkpipvals(ipaddr) values('"+ipaddr+"')"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    ipaddressdata=mfetchipvals()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps("Success"))
    return resp


#Delete IP routing
@app.route('/ipaddrdelete')
def ipaddrdelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkpipvals where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    ipaddressdata=mfetchipvals()
    return render_template('ipaddrs.html',ipaddressdata=ipaddressdata)


#------------------------------------------------------------------------------------------------------------
#Bank creation page
@app.route('/banks')
def banks():
    banksdata=mfetchbanks()
    return render_template('banks.html',banksdata=banksdata)

#Add new Bank routing
@app.route('/addnewbank')
def addnewbank():
    bank=request.args['bank']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into lkpbanks(bankname) values('"+bank+"')"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    banksdata=mfetchbanks()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps("Success"))
    return resp


#Delete Bank routing
@app.route('/bankdelete')
def bankdelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkpbanks where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    banksdata=mfetchbanks()
    return render_template('banks.html',banksdata=banksdata)


#------------------------------------------------------------------------------------------------------------

#Qualification creation page
@app.route('/qualifications')
def qualifications():
    qualdata=mfetchqualifications()
    return render_template('qualifications.html',qualdata=qualdata)

#Add new qualification routing
@app.route('/addnewqual')
def addnewqual():
    qual=request.args['qual']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into lkpqualifications(qualification) values('"+qual+"')"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    qualdata=mfetchqualifications()
    resp = make_response(json.dumps("Success"))
    return resp


#Delete qualification routing
@app.route('/qualdelete')
def qualdelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkpqualifications where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    qualdata=mfetchqualifications()
    return render_template('qualifications.html',qualdata=qualdata)


#------------------------------------------------------------------------------------------------------------
#Language creation page
@app.route('/shifttiming')
def shifttiming():
    shifttimingdata=mfetchshifttimings()
    return render_template('shifttiming.html',shifttimingdata=shifttimingdata)

#Add new shift routing
@app.route('/addnewshift')
def addnewshift():
    sname=request.args['sname']
    intime=request.args['intime']
    outtime=request.args['outtime']
    hdhour=request.args['hdhour']
    fdhour=request.args['fdhour']
    nshift=request.args['nshift']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into lkpshifttimings(sname,intime,outtime,hdhour,fdhour,nshift) values('"+sname+"','"+intime+"','"+outtime+"','"+hdhour+"','"+fdhour+"','"+nshift+"')"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    languagesdata=mfetchlanguages()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps("Success"))
    return resp


#Delete shift routing
@app.route('/shiftdelete')
def shiftdelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkpshifttimings where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    shifttimingdata=mfetchshifttimings()
    return render_template('shifttiming.html',shifttimingdata=shifttimingdata)


#------------------------------------------------------------------------------------------------------------
#Paytype creation page
@app.route('/paytype')
def paytypes():
    paytypesdata=mfetchpaytypes()
    return render_template('paytypes.html',paytypesdata=paytypesdata)

#Add new language routing
@app.route('/addnewpaytype')
def addnewpaytype():
    paytype=request.args['paytype']
    paycode=request.args['paycode']
    color=request.args['color']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into lkppaytypes(paytype,paycode,color) values('"+paytype+"','"+paycode+"','"+color+"')"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    resp = make_response(json.dumps("Success"))
    return resp


#Delete language routing
@app.route('/paytypedelete')
def paytypedelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkppaytypes where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    paytypesdata=mfetchpaytypes()
    return render_template('paytypes.html',paytypesdata=paytypesdata)

#------------------------------------------------------------------------------------------------------------

#Department creation page
@app.route('/departments')
def departments():
    departmentsdata=mfetchdepartments()
    return render_template('departments.html',departmentsdata=departmentsdata)

#Add new language routing
@app.route('/addnewdept')
def addnewdept():
    dept=request.args['dept']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into lkpdepartments(dept) values('"+str(dept)+"')"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps("Success"))
    return resp


#Delete department routing
@app.route('/deptdelete')
def deptdelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkpdepartments where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    departmentsdata=mfetchdepartments()
    return render_template('departments.html',departmentsdata=departmentsdata)

#------------------------------------------------------------------------------------------------------------

#Position creation page
@app.route('/positions')
def positions():
    positionsdata=mfetchpositions()
    return render_template('positions.html',positionsdata=positionsdata)

#Add new language routing
@app.route('/addnewposition')
def addnewposition():
    position=request.args['position']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into lkppositions(position) values('"+str(position)+"')"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps("Success"))
    return resp


#Delete department routing
@app.route('/positiondelete')
def positiondelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkppositions where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    positionsdata=mfetchpositions()
    return render_template('positions.html',positionsdata=positionsdata)

#-------------------------------------------------------------------------------------------------------------

#Idproof creation page
@app.route('/idproofs')
def idproof():
    idproofdata=mfetchidproofs()
    return render_template('idproofs.html',idproofdata=idproofdata)

#Add new id proof routing
@app.route('/addnewidproof')
def addnewidproof():
    idproof=request.args['idproof']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into lkpidproof(idproof) values('"+idproof+"')"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    idproofdata=mfetchidproofs()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps("Success"))
    return resp

#Delete idproof routing
@app.route('/idproofdelete')
def idproofdelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkpidproof where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    idproofdata=mfetchidproofs()
    return render_template('idproofs.html',idproofdata=idproofdata)

#Role creation page
@app.route('/rolecreation')
def rolecreation():
    rolesdata=mfetchroles()
    return render_template('rolecreation.html',rolesdata=rolesdata)

#Role menu mapping page
@app.route('/rolemenumap')
def rolemenumap():
    rolesdata=mfetchroles()
    print(rolesdata)
    menudata=mfetchmenus()
    return render_template('rolemenumap.html',rolesdata=rolesdata,menudata=menudata)

#Role user management 
@app.route('/roleuseraccount')
def roleuseraccount():
    rolesdata=mfetchroles()
    roleusersdata=mfetchroleusers()
    print(roleusersdata)
    return render_template('roleuseraccount.html',rolesdata=rolesdata,roleusersdata=roleusersdata)

#Fetch Email on User Id 
@app.route('/fetchmgrpersonaldata')
def fetchmgrpersonaldata():
    empid=request.args['empid']
    detailsdata=mfetchmgrpersonaldata(empid)
    print(detailsdata)
    msg=detailsdata[0][0]+","+detailsdata[0][1]
    resp = make_response(json.dumps(msg))
    return resp

#Fetch Email from role for change password on User Id 
@app.route('/fetchroledata')
def fetchroledata():
    empid=request.args['empid']
    detailsdata=mfetchmgrpersonaldata(empid)
    print(detailsdata)
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()

    sql_Query = "select pswd from lkpmapuserrole where email='"+detailsdata[0][1]+"'"  
    cursor.execute(sql_Query)
    pswddata = cursor.fetchall()
    connection.commit()
    connection.close()
    cursor.close()
    msg=detailsdata[0][0]+","+detailsdata[0][1]+","+pswddata[0][0]
    resp = make_response(json.dumps(msg))
    return resp    

#Add new role routing
@app.route('/mapnewuserrole')
def mapnewuserrole():
    ru_uname=request.args['ru_uname']
    ru_pswd=request.args['ru_pswd']
    ru_roleddl=request.args['ru_roleddl']
    ru_email=request.args['ru_email']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "select count(*) from lkpmapuserrole where email='"+ru_email+"'"
    print(sql_Query)
    cursor.execute(sql_Query)
    dataval = cursor.fetchall()
    print(dataval)
    msg=''
    if int(dataval[0][0])==0:    
        sql_Query = "insert into lkpmapuserrole(username,pswd,rolename,email) values('"+ru_uname+"','"+ru_pswd+"','"+ru_roleddl+"','"+ru_email+"')"
        cursor.execute(sql_Query)
        msg="Role to user mapped successfully"
    else:
        msg="Role has been already assigned for the user"
    connection.commit()
    connection.close()
    cursor.close()
    rolesdata=mfetchroles()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps(msg))
    return resp

#Delete role user mapping route
@app.route('/roleuserdelete')
def roleuserdelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkpmapuserrole where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    rolesdata=mfetchroles()
    roleusersdata=mfetchroleusers()
    print(roleusersdata)
    return render_template('roleuseraccount.html',rolesdata=rolesdata,roleusersdata=roleusersdata)

#Add new role routing
@app.route('/addnewrole')
def addnewrole():
    rolename=request.args['rolename']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into lkproles(rolename) values('"+rolename+"')"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    rolesdata=mfetchroles()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps("Success"))
    return resp

#Delete role routing
@app.route('/roledelete')
def roledelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkproles where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    rolesdata=mfetchroles()
    return render_template('rolecreation.html',rolesdata=rolesdata)



#Rostering page
@app.route('/rostering')
def rostering():
    #procdata=mfetchprocdata()
    
    process_name_data=mfetchrec_procdata()
    emplist=mfetchemplist()
    timelist=mfetchtimedata()
    return render_template('rostering.html',process_name_data=process_name_data,emplist=emplist,timelist=timelist)


#Rostering page
@app.route('/fetchemponproc')
def fetchemponproc():
    procname=request.args['procname']
    emplist=mfetchempproclist(procname)
    msg=""
    for i in range(len(emplist)):
        msg=msg+str(emplist[i][0])+","
        msg=msg+str(emplist[i][1])+"#"
    resp = make_response(json.dumps(msg))
    return resp

'''
# To check counts in quarter
SELECT YEAR(STR_TO_DATE(DateFor, '%d-%b-%y')) AS year, QUARTER(STR_TO_DATE(DateFor, '%d-%b-%y')) AS quarter, COUNT(*) AS jobcount
  FROM tblEmpTotalHoursSimp
 WHERE Empcode = '101' and Atype='NH'
 GROUP BY YEAR(STR_TO_DATE(DateFor, '%d-%b-%y')), QUARTER(STR_TO_DATE(DateFor, '%d-%b-%y'))
 ORDER BY YEAR(STR_TO_DATE(DateFor, '%d-%b-%y')), QUARTER(STR_TO_DATE(DateFor, '%d-%b-%y'))
'''





#old Rostering Code
'''


    
   
    empdl=[101,1347,9486,9708,11695,106,164,1347,2046,2333,3954,4170,4947,4965,1347]
    msg=""
    
    global nhcount
    for i in range(len(selectedemplist)):
        print(selectedemplist[i])
        empval=selectedemplist[i].split('-')
        print(empval)
        if ltype=="NH":
            nhcount=nhcount+1
        empid=empval[0]
        empname=empval[1]
        if (int(empid) in empdl) and ltype=="CL":
            for j in range(len(selecteddateslist)):
                print(selecteddateslist[j])
                dtval=selecteddateslist[j].split('/')
                
                monthname=getMonthName(str(dtval[0]))
                yearval=int(dtval[2])-2000
                datefor=""
                if int(dtval[1])<10:
                    datefor="0"+str(dtval[1])+"-"+monthname+"-"+str(yearval)
                else:                
                    datefor=str(dtval[1])+"-"+monthname+"-"+str(yearval)
                idval=random.randint(111111, 999999)
                connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
                cursor = connection.cursor()
                sql_Query=""
                if ltype!="0":
                    sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,OffTypes,Atype) values('"+str(empid)+"','"+datefor+"',"+str(idval)+",'"+ltype+"','"+ltype+"')"
                if ltype!="0":
                    sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,ShiftId,Atype,ShiftStartTime,ShiftEndTime) values('"+str(empid)+"','"+datefor+"',"+str(idval)+",'"+stype+"','.')"
                print(sql_Query)
                cursor.execute(sql_Query)    
                connection.commit()        
                connection.close()
                cursor.close()
        else:
            msg=msg+"CL is not accumulated"

        
        if int(empid)!=12920 and ltype=="WO":
            for j in range(len(selecteddateslist)):
                print(selecteddateslist[j])
                dtval=selecteddateslist[j].split('/')
                
                monthname=getMonthName(str(dtval[0]))
                yearval=int(dtval[2])-2000
                datefor=""
                if int(dtval[1])<10:
                    datefor="0"+str(dtval[1])+"-"+monthname+"-"+str(yearval)
                else:                
                    datefor=str(dtval[1])+"-"+monthname+"-"+str(yearval)
                idval=random.randint(111111, 999999)
                connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
                cursor = connection.cursor()
                sql_Query=""
                if ltype!="0":
                    sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,OffTypes,Atype) values('"+str(empid)+"','"+datefor+"',"+str(idval)+",'"+ltype+"','"+ltype+"')"
                if stype!="0":
                    sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,ShiftId,Atype,ShiftStartTime,ShiftEndTime) values('"+str(empid)+"','"+datefor+"',"+str(idval)+",'"+stype+"','.')"
                print(sql_Query)
                cursor.execute(sql_Query)    
                connection.commit()        
                connection.close()
                cursor.close()
        else:
            if int(empid)==12920:
                msg="WO cannot be assigned as the employee as there are 4 LOP in last week"

        
        if int(empid)!=12922 and ltype=="SL":
            for j in range(len(selecteddateslist)):
                print(selecteddateslist[j])
                dtval=selecteddateslist[j].split('/')
                
                monthname=getMonthName(str(dtval[0]))
                yearval=int(dtval[2])-2000
                datefor=""
                if int(dtval[1])<10:
                    datefor="0"+str(dtval[1])+"-"+monthname+"-"+str(yearval)
                else:                
                    datefor=str(dtval[1])+"-"+monthname+"-"+str(yearval)
                idval=random.randint(111111, 999999)
                connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
                cursor = connection.cursor()
                sql_Query=""
                if ltype!="0":
                    sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,OffTypes,Atype) values('"+str(empid)+"','"+datefor+"',"+str(idval)+",'"+ltype+"','"+ltype+"')"
                if stype!="0":
                    sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,ShiftId,Atype,ShiftStartTime,ShiftEndTime) values('"+str(empid)+"','"+datefor+"',"+str(idval)+",'"+stype+"','.')"
                print(sql_Query)
                cursor.execute(sql_Query)    
                connection.commit()        
                connection.close()
                cursor.close()
        else:
            if int(empid)==12922:
                msg="SL cannot be assigned as the employee as there are 4 LOP in last week"

        
        if int(empid)!=12927 and ltype=="AL":
            for j in range(len(selecteddateslist)):
                print(selecteddateslist[j])
                dtval=selecteddateslist[j].split('/')
                
                monthname=getMonthName(str(dtval[0]))
                yearval=int(dtval[2])-2000
                datefor=""
                if int(dtval[1])<10:
                    datefor="0"+str(dtval[1])+"-"+monthname+"-"+str(yearval)
                else:                
                    datefor=str(dtval[1])+"-"+monthname+"-"+str(yearval)
                idval=random.randint(111111, 999999)
                connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
                cursor = connection.cursor()
                sql_Query=""
                if ltype!="0":
                    sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,OffTypes,Atype) values('"+str(empid)+"','"+datefor+"',"+str(idval)+",'"+ltype+"','"+ltype+"')"
                if stype!="0":
                    sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,ShiftId,Atype,ShiftStartTime,ShiftEndTime) values('"+str(empid)+"','"+datefor+"',"+str(idval)+",'"+stype+"','.')"
                print(sql_Query)
                cursor.execute(sql_Query)    
                connection.commit()        
                connection.close()
                cursor.close()
        else:
            if int(empid)==12927:
                msg="AL cannot be assigned as the employee joining is less than 3 years"
'''
@app.route('/setuprostering')
def setuprostering():
    monnum=4
    year=22
    selectedemp=request.args['selectedemp']
    selecteddates=request.args['selecteddates']
    ltype=request.args['ltype']
    stype=request.args['stype']
    print("aaa"+ltype)
    print(stype)
    msg=""
    selectedemp=selectedemp[0:len(selectedemp)-1]
    selecteddates=selecteddates[0:len(selecteddates)-1]
    selectedemplist=selectedemp.split(',')
    selecteddateslist=selecteddates.split(',')
    print(selectedemplist)

    leavedatescount=len(selecteddateslist)
    datesfinallist=[]
    isempeligible=0
    if ltype!='0':
        if ltype=="CL":
            
            if leavedatescount>1:
                msg="CL is not accumulated to apply for these days. There is only 1 CL per month"
            else:
                for i in range(len(selectedemplist)):
                    for j in range(leavedatescount):                        
                        sql_Query=""
                        listeddate=selecteddateslist[j]
                        datevalues=listeddate.split('/')
                        
                        day=''
                        month=''
                        year=''
                        if int(datevalues[1])<10:
                            day='0'+str(datevalues[1])
                        else:
                            day=str(datevalues[1])
                            
                        month=monthname(int(datevalues[0]))


                        #fetching dates based on the date
                        
                        if int(datevalues[1])>=16:
                            startdate=str(datevalues[2])+"-"+str(datevalues[0])+"-16"
                            nmonth=int(datevalues[0])+1
                            startmon=int(datevalues[0])
                            endmon=nmonth     
                            enddate=str(datevalues[2])+"-"+str(nmonth)+"-15"
                        else:                            
                            startmon=int(datevalues[0])-1
                            endmon=int(datevalues[0])    
                            startdate=str(datevalues[2])+"-"+str(startmon)+"-16"    
                            enddate=str(datevalues[2])+"-"+str(endmon)+"-15"

                        dateslist=pd.date_range(start=startdate,end=enddate)
                        for n in range(len(dateslist)):                        
                            dt=str(dateslist[n])[0:10]
                            dtval=dt.split('-')
                            dtval[1]=getMonthName(str(dtval[1]))
                            dtval[0]=int(dtval[0])-2000
                            findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
                            
                            datesfinallist.append(findate)    
                        '''
                        print(startdate)
                        print(enddate)
                        print('----------------------------------------')
                        print(datesfinallist)
                        print('----------------------------------------')
                        '''
                        year=int(datevalues[2])-2000
                        findate='-'+str(month)+'-'+str(year)
                        print(findate)
                        empval=selectedemplist[i].split('-')
                        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
                        cursor = connection.cursor(buffered=True)
                        sql_Query = "select DateofJoin from tblEmpMgrMap where Empcode='"+empval[0]+"'"
                        cursor.execute(sql_Query)
                        dojval = cursor.fetchall()
                        monname=monthname(monnum)                       
                        
                        dojvals=str(dojval[0][0]).split('-')
                        dojmonnum=0
                        try:
                            dojmonnum=monthnum(dojvals[1])
                        except:
                            dojmonnum=int(dojvals[1])
                        year=int(dojvals[2])+2000                        

                        d0 = date(int(year), int(dojmonnum), int(dojvals[0]))
                        d1 = date(int(datevalues[2]), int(datevalues[0]), int(day))
                        delta = d1 - d0                        
                       
                        if delta.days<30:
                            msg="Employee "+empval[0]+" not eligible for Casual Leave"
                            break
                        sql_Query = "select count(*) from tblEmpTotalHoursSimp where Empcode='"+empval[0]+"' and Atype='CL' and ("#DateFor like '%"+findate+"' "                        
                        for m in range(len(datesfinallist)):
                            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[m])+"' or "
                        sql_Query=sql_Query[0:len(sql_Query)-3]
                        sql_Query=sql_Query+")"
                        print(sql_Query)
                        cursor.execute(sql_Query)
                        leavecount = cursor.fetchall()
                        lc=0
                        try:
                            lc=leavecount[0][0]
                        except:
                            lc=0

                        print("Leave Count : "+str(lc))
                        if int(lc)==0:
                            findate1=str(day)+findate
                            sql_Query = "select count(*) from tblEmpTotalHoursSimp where Empcode='"+empval[0]+"' and DateFor like '"+findate1+"'"
                            print(sql_Query)
                            cursor.execute(sql_Query)
                            datecount = cursor.fetchall()
                            if int(datecount[0][0])==0:
                                idval=random.randint(111111, 999999)
                                sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,OffTypes,Atype) values('"+str(empval[0])+"','"+findate1+"',"+str(idval)+",'"+ltype+"','"+ltype+"')"
                                print(sql_Query)
                                cursor.execute(sql_Query)
                                connection.commit()
                            else:
                                sql_Query = "update tblEmpTotalHoursSimp set OffTypes='"+ltype+"',Atype='"+ltype+"' where Empcode='"+str(empval[0])+"' and DateFor='"+findate1+"'"
                                print(sql_Query)
                                cursor.execute(sql_Query)
                                connection.commit()                            
                        else:
                            msg=msg+"Casual Leave is not possible for "+selectedemplist[i]+" as it is consumed for this month"
                                
                        connection.close()
                        cursor.close()
                    
        if ltype=="NH":                
            extradaysflagger=0
            if leavedatescount>3:
                msg="NH canot exceed more than 3 days in a quarter"
            else:
                for i in range(len(selectedemplist)):
                    for j in range(leavedatescount):                        
                        sql_Query=""
                        listeddate=selecteddateslist[j]
                        datevalues=listeddate.split('/')
                        
                        day=''
                        month=''
                        year=''
                        if int(datevalues[1])<10:
                            day='0'+str(datevalues[1])
                        else:
                            day=str(datevalues[1])
                            
                        month=monthname(int(datevalues[0]))
                        
                        year=int(datevalues[2])-2000
                        findate='-'+str(month)+'-'+str(year)
                        print(findate)
                        empval=selectedemplist[i].split('-')
                        dtverifymonth=''
                        if int(datevalues[0])<10:
                            dtverifymonth='0'+str(datevalues[0])
                        else:
                            dtverifymonth=str(datevalues[0])
                        
                        datetoverify=str(datevalues[2])+'-'+str(dtverifymonth)+'-'+str(day)
                        
                        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
                        cursor = connection.cursor(buffered=True)
                        sql_Query = "select DateofJoin from tblEmpMgrMap where Empcode='"+empval[0]+"'"
                        cursor.execute(sql_Query)
                        dojval = cursor.fetchall()
                        monname=monthname(monnum)                       
                        
                        dojvals=str(dojval[0][0]).split('-')
                        dojmonnum=monthnum(dojvals[1])
                        year=int(dojvals[2])+2000                        

                        d0 = date(int(year), int(dojmonnum), int(dojvals[0]))
                        d1 = date(int(datevalues[2]), int(datevalues[0]), int(day))
                        delta = d1 - d0                        
                       
                        if delta.days<90:
                            msg="Employee "+empval[0]+" not eligible for National Holiday"
                            break
                        sql_Query = "select count(*) from lkpholidays where holidaydate='"+datetoverify+"'"
                        print(sql_Query)
                        cursor.execute(sql_Query)
                        isdateinholidays = cursor.fetchall()
                        if int(isdateinholidays[0][0])<=0:
                            msg="National Holiday is not available for this date "+str(listeddate)
                            break
                        sql_Query = "SELECT COUNT(*) AS leavecount FROM tblEmpTotalHoursSimp where Empcode='"+empval[0]+"' and Atype='NH' GROUP BY YEAR(STR_TO_DATE(DateFor, '%d-%b-%y')), QUARTER(STR_TO_DATE(DateFor, '%d-%b-%y')) ORDER BY YEAR(STR_TO_DATE(DateFor, '%d-%b-%y')), QUARTER(STR_TO_DATE(DateFor, '%d-%b-%y'))"
                        print(sql_Query)
                        cursor.execute(sql_Query)
                        leavecount = cursor.fetchall()
                        lc=0
                        try:
                            lc=leavecount[0][0]
                        except:
                            lc=0
                        
                        sumleaves=lc+leavedatescount
                        if sumleaves<=10:
                            print("Leave Count : "+str(lc))
                            if int(lc)<3:
                                findate1=str(day)+findate
                                sql_Query = "select count(*) from tblEmpTotalHoursSimp where Empcode='"+empval[0]+"' and DateFor like '"+findate1+"'"
                                cursor.execute(sql_Query)
                                datecount = cursor.fetchall()
                                if int(datecount[0][0])==0:
                                    idval=random.randint(111111, 999999)
                                    sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,OffTypes,Atype) values('"+str(empval[0])+"','"+findate1+"',"+str(idval)+",'"+ltype+"','"+ltype+"')"
                                    print(sql_Query)
                                    cursor.execute(sql_Query)
                                    connection.commit()
                                else:
                                    sql_Query = "update tblEmpTotalHoursSimp set OffTypes='"+ltype+"',Atype='"+ltype+"' where Empcode='"+str(empval[0])+"' and DateFor='"+findate1+"'"
                                    print(sql_Query)
                                    cursor.execute(sql_Query)
                                    connection.commit()                            
                            else:
                                msg=msg+"National holiday is not possible for "+selectedemplist[i]+" as it has exceeded 3days"
                        else:
                            extradaysflagger=1
                            
                    if extradaysflagger==1:
                        msg=msg+"Reduce dates count as it exceeds max NH allowed for "+selectedemplist[i]+" \n"
                        extradaysflagger=0
                                    
                        connection.close()
                        cursor.close()
                    
        if ltype=="SL":
            extradaysflagger=0
            if leavedatescount>6:
                msg="Sick Leave cannot exceed more than 6 days in a Year"
            else:
                for i in range(len(selectedemplist)):
                    for j in range(leavedatescount):                        
                        sql_Query=""
                        listeddate=selecteddateslist[j]
                        datevalues=listeddate.split('/')
                        
                        day=''
                        month=''
                        year=''
                        if int(datevalues[1])<10:
                            day='0'+str(datevalues[1])
                        else:
                            day=str(datevalues[1])
                            
                        month=monthname(int(datevalues[0]))

                        year=int(datevalues[2])-2000
                        findate='-'+str(month)+'-'+str(year)
                        print(findate)
                        empval=selectedemplist[i].split('-')
                        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
                        cursor = connection.cursor()
                        sql_Query = "SELECT COUNT(*) AS leavecount FROM tblEmpTotalHoursSimp where Empcode='"+empval[0]+"' and Atype='SL' and DateFor like '%-"+str(year)+"'"
                        print(sql_Query)
                        cursor.execute(sql_Query)
                        leavecount = cursor.fetchall()
                        lc=0
                        try:
                            lc=leavecount[0][0]
                        except:
                            lc=0
                        
                        sumleaves=lc+leavedatescount
                        if sumleaves<=6:
                            print("Leave Count : "+str(lc))
                            if int(lc)<6:
                                findate1=str(day)+findate
                                sql_Query = "select count(*) from tblEmpTotalHoursSimp where Empcode='"+empval[0]+"' and DateFor like '"+findate1+"'"
                                cursor.execute(sql_Query)
                                datecount = cursor.fetchall()
                                if int(datecount[0][0])==0:
                                    idval=random.randint(111111, 999999)
                                    sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,OffTypes,Atype) values('"+str(empval[0])+"','"+findate1+"',"+str(idval)+",'"+ltype+"','"+ltype+"')"
                                    print(sql_Query)
                                    cursor.execute(sql_Query)
                                    connection.commit()
                                else:
                                    sql_Query = "update tblEmpTotalHoursSimp set OffTypes='"+ltype+"',Atype='"+ltype+"' where Empcode='"+str(empval[0])+"' and DateFor='"+findate1+"'"
                                    print(sql_Query)
                                    cursor.execute(sql_Query)
                                    connection.commit()                            
                            else:
                                msg=msg+"Sick leave is not possible for "+selectedemplist[i]+" as it has exceeded 6days"
                        else:
                            extradaysflagger=1
                            
                    if extradaysflagger==1:
                        msg=msg+"Reduce dates count as it exceeds max SL allowed for "+selectedemplist[i]+" \n"
                        extradaysflagger=0
                                    
                        connection.close()
                        cursor.close()
                    
        if ltype=="AL":

                
            extradaysflagger=0
            if leavedatescount>5:
                print('I reached')
                msg="Annual Leave cannot exceed more than 5 days in a Year"
            else:
                for i in range(len(selectedemplist)):
                    for j in range(leavedatescount):                        
                        sql_Query=""
                        
                        listeddate=selecteddateslist[j]
                        datevalues=listeddate.split('/')
                        
                        day=''
                        month=''
                        year=''
                        if int(datevalues[1])<10:
                            day='0'+str(datevalues[1])
                        else:
                            day=str(datevalues[1])
                            
                        month=monthname(int(datevalues[0]))

                        year=int(datevalues[2])-2000
                        findate='-'+str(month)+'-'+str(year)
                        print(findate)
                        empval=selectedemplist[i].split('-')
                        
                        
                        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
                        cursor = connection.cursor(buffered=True)
                        sql_Query = "select DateofJoin from tblEmpMgrMap where Empcode='"+empval[0]+"'"
                        cursor.execute(sql_Query)
                        dojval = cursor.fetchall()
                        monname=monthname(monnum)                       
                        
                        dojvals=str(dojval[0][0]).split('-')
                        dojmonnum=0
                        try:
                            dojmonnum=monthnum(dojvals[1])
                        except:
                            dojmonnum=int(dojvals[1])
                        year=int(dojvals[2])+2000                        

                        d0 = date(int(year), int(dojmonnum), int(dojvals[0]))
                        d1 = date(int(datevalues[2]), int(datevalues[0]), int(day))
                        delta = d1 - d0                        
                       
                        if delta.days<1095:
                            msg="Employee "+empval[0]+" not eligible for Annual Leave"
                            break
                        sql_Query = "SELECT COUNT(*) AS leavecount FROM tblEmpTotalHoursSimp where Empcode='"+empval[0]+"' and Atype='AL' and DateFor like '%-"+str(year)+"'"
                        print(sql_Query)
                        cursor.execute(sql_Query)
                        leavecount = cursor.fetchall()
                        lc=0
                        try:
                            lc=leavecount[0][0]
                        except:
                            lc=0
                        
                        sumleaves=lc+leavedatescount
                        if sumleaves<=5:
                            print("Leave Count : "+str(lc))
                            if int(lc)<5:
                                findate1=str(day)+findate
                                sql_Query = "select count(*) from tblEmpTotalHoursSimp where Empcode='"+empval[0]+"' and DateFor like '"+findate1+"'"
                                cursor.execute(sql_Query)
                                datecount = cursor.fetchall()
                                if int(datecount[0][0])==0:
                                    idval=random.randint(111111, 999999)
                                    sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,OffTypes,Atype) values('"+str(empval[0])+"','"+findate1+"',"+str(idval)+",'"+ltype+"','"+ltype+"')"
                                    print(sql_Query)
                                    cursor.execute(sql_Query)
                                    connection.commit()
                                else:
                                    sql_Query = "update tblEmpTotalHoursSimp set OffTypes='"+ltype+"',Atype='"+ltype+"' where Empcode='"+str(empval[0])+"' and DateFor='"+findate1+"'"
                                    print(sql_Query)
                                    cursor.execute(sql_Query)
                                    connection.commit()                            
                            else:
                                msg=msg+"Annual Leave is not possible for "+selectedemplist[i]+" as it has exceeded 5days"
                        else:
                            extradaysflagger=1
                            
                    if extradaysflagger==1:
                        msg=msg+"Reduce dates count as it exceeds max AL allowed for "+selectedemplist[i]+" \n"
                        extradaysflagger=0
                                    
                        connection.close()
                        cursor.close()
                    
        if ltype=="WO":
            extradaysflagger=0
            if leavedatescount>1:
                msg="Week off cannot exceed more than 1 in a week"
            else:
                for i in range(len(selectedemplist)):
                    for j in range(leavedatescount):                        
                        sql_Query=""
                        listeddate=selecteddateslist[j]
                        datevalues=listeddate.split('/')
                        
                        day=''
                        month=''
                        year=''
                        if int(datevalues[1])<10:
                            day='0'+str(datevalues[1])
                        else:
                            day=str(datevalues[1])
                            
                        month=monthname(int(datevalues[0]))

                        year=int(datevalues[2])-2000
                        findate=str(day)+'-'+str(month)+'-'+str(year)
                        print(findate)
                        empval=selectedemplist[i].split('-')
                        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
                        cursor = connection.cursor()
                        sql_Query = "SELECT COUNT(*) AS leavecount FROM tblEmpTotalHoursSimp where Empcode='"+empval[0]+"' and Atype='WO' and DateFor like '"+str(findate)+"'"
                        print(sql_Query)
                        cursor.execute(sql_Query)
                        leavecount = cursor.fetchall()
                        lc=0
                        try:
                            lc=leavecount[0][0]
                        except:
                            lc=0
                        
                        sumleaves=lc+leavedatescount
                        if sumleaves<=1:
                            print("Leave Count : "+str(lc))
                            if int(lc)<1:
                                findate1=findate
                                sql_Query = "select count(*) from tblEmpTotalHoursSimp where Empcode='"+empval[0]+"' and DateFor like '"+findate+"'"
                                cursor.execute(sql_Query)
                                datecount = cursor.fetchall()
                                if int(datecount[0][0])==0:
                                    idval=random.randint(111111, 999999)
                                    sql_Query = "insert into  tblEmpTotalHoursSimp(Empcode,DateFor,id,OffTypes,Atype) values('"+str(empval[0])+"','"+findate1+"',"+str(idval)+",'"+ltype+"','"+ltype+"')"
                                    print(sql_Query)
                                    cursor.execute(sql_Query)
                                    connection.commit()
                                else:
                                    sql_Query = "update tblEmpTotalHoursSimp set OffTypes='"+ltype+"',Atype='"+ltype+"' where Empcode='"+str(empval[0])+"' and DateFor='"+findate1+"'"
                                    print(sql_Query)
                                    cursor.execute(sql_Query)
                                    connection.commit()                            
                            else:
                                msg=msg+"Week Off is not possible for "+selectedemplist[i]+" as it has exceeded WO count in that week"
                        else:
                            extradaysflagger=1
                            
                    if extradaysflagger==1:
                        msg=msg+"Reduce dates count as it exceeds max WO allowed for "+selectedemplist[i]+" \n"
                        extradaysflagger=0
                                    
                        connection.close()
                        cursor.close()
        
    if stype!='0':
        print("STYPE:"+str(stype))
        for i in range(len(selectedemplist)):
            for j in range(leavedatescount):
                sql_Query=""
                listeddate=selecteddateslist[j]
                datevalues=listeddate.split('/')

                day=''
                month=''
                year=''
                if int(datevalues[1])<10:
                    day='0'+str(datevalues[1])
                else:
                    day=str(datevalues[1])
                    
                month=monthname(int(datevalues[0]))
                
                empval=selectedemplist[i].split('-')
                year=int(datevalues[2])-2000
                checkdate=str(day)+"-"+str(month)+"-"+str(year)
                connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
                cursor = connection.cursor()
                sql_Query = "SELECT COUNT(*) FROM tblEmpTotalHoursSimp where Empcode='"+empval[0]+"' and DateFor like '%"+str(checkdate)+"%'"
                print(sql_Query)
                cursor.execute(sql_Query)
                datescount = cursor.fetchall()
                dc=0
                try:
                    dc=datescount[0][0]
                except:
                    dc=0
                print(dc)
                if dc>0:
                    atype=''
                    sql_Query = "SELECT * FROM lkpshifttimings where id='"+stype+"'"
                    cursor.execute(sql_Query)
                    shiftlkpdata = cursor.fetchall()
                    shift_schedule_stime=shiftlkpdata[0][2]
                    ssstime_split=shift_schedule_stime.split(':')
                    sssthrs=ssstime_split[0]
                    ssstmins=ssstime_split[1]
                    ssstsecs=ssstime_split[2]
                    ssst_totsecs=int(sssthrs)*60*60
                    ssst_totsecs=ssst_totsecs+int(ssstmins)*60
                    ssst_totsecs=ssst_totsecs+int(ssstsecs)
                    
                    shift_schedule_etime=shiftlkpdata[0][3]
                    ssetime_split=shift_schedule_etime.split(':')
                    ssethrs=ssetime_split[0]
                    ssetmins=ssetime_split[1]
                    ssetsecs=ssetime_split[2]
                    sset_totsecs=int(ssethrs)*60*60
                    sset_totsecs=sset_totsecs+int(ssetmins)*60
                    sset_totsecs=sset_totsecs+int(ssetsecs)

                    
                    sql_Query = "SELECT * FROM tblEmpTotalHoursSimp where Empcode='"+empval[0]+"' and DateFor like '%"+str(checkdate)+"%'"
                    graceperiodsecs=600
                    print(sql_Query)
                    cursor.execute(sql_Query)
                    attdata = cursor.fetchall()
                    lgtotsecs=0
                    #print(attdata[0][11])
                    try:
                        logintimeval=attdata[0][10].split(' ')
                        if logintimeval[2].lower()=='am':
                            logtime=logintimeval[1]
                            logtimesplit=logtime.split(':')
                            lghrs=logtimesplit[0]
                            lgmins=logtimesplit[1]
                            lgsecs=logtimesplit[2]
                            lgtotsecs=int(lghrs)*60*60
                            lgtotsecs=lgtotsecs+int(lgmins)*60
                            lgtotsecs=lgtotsecs+int(lgsecs)
                        elif logintimeval[2].lower()=='pm':
                            logtime=logintimeval[1]
                            logtimesplit=logtime.split(':')
                            lghrs=logtimesplit[0]
                            lgmins=logtimesplit[1]
                            lgsecs=logtimesplit[2]
                            lgtotsecs=(int(lghrs)+12)*60*60
                            lgtotsecs=lgtotsecs+int(lgmins)*60
                            lgtotsecs=lgtotsecs+int(lgsecs)
                    except:
                        lgtotsecs=0
                    #print(lgtotsecs)

                    lgouttotsecs=0
                    try:
                        logouttimeval=attdata[0][11].split(' ')
                        if logouttimeval[2].lower()=='am':
                            logouttime=logouttimeval[1]
                            logouttimesplit=logouttime.split(':')
                            lgouthrs=logouttimesplit[0]
                            lgoutmins=logouttimesplit[1]
                            lgoutsecs=logouttimesplit[2]
                            lgouttotsecs=int(lgouthrs)*60*60
                            lgouttotsecs=lgouttotsecs+int(lgoutmins)*60
                            lgouttotsecs=lgouttotsecs+int(lgoutsecs)
                        elif logouttimeval[2].lower()=='pm':
                            logouttime=logouttimeval[1]
                            logouttimesplit=logouttime.split(':')
                            lgouthrs=logouttimesplit[0]
                            lgoutmins=logouttimesplit[1]
                            lgoutsecs=logouttimesplit[2]
                            lgouttotsecs=(int(lgouthrs)+12)*60*60
                            lgouttotsecs=lgouttotsecs+int(lgoutmins)*60
                            lgouttotsecs=lgouttotsecs+int(lgoutsecs)
                    except:
                        lgouttotsecs=0
                    #print(lgouttotsecs)
                    tottimesecs=lgouttotsecs-lgtotsecs
                    lgdtime=convertsectotime(tottimesecs)
                    #print(lgdtime)
                    lgdtimesplit=lgdtime.split(':')
                    tothrs=lgdtimesplit[0]
                    addupmin=0
                    if int(lgdtimesplit[2])>30:
                        addupmin=1
                    tothrs=tothrs+"."+str(int(lgdtimesplit[1])+addupmin)
                    print(tothrs)
                    login_allow_time=ssst_totsecs+graceperiodsecs
                    total_shift_secs=sset_totsecs-ssst_totsecs
                    half_shift_secs=total_shift_secs/2
                    
                    if lgouttotsecs==0 and lgtotsecs==0:
                        atype="A"
                    elif int(tottimesecs)<=int(half_shift_secs+120) and int(tottimesecs)>=int(half_shift_secs-120):
                        atype="HD"
                    elif lgouttotsecs<sset_totsecs:
                        atype="HD"
                    elif lgtotsecs>login_allow_time:
                        atype="LHD"
                    else:
                        atype="P"

                    sql_Query = "update tblEmpTotalHoursSimp set Atype='"+str(atype)+"',ShiftStartTime='"+str(shift_schedule_stime)+"',ShiftEndTime='"+str(shift_schedule_etime)+"' where Empcode='"+empval[0]+"' and DateFor like '%"+str(checkdate)+"%'"
                    graceperiodsecs=600
                    print(sql_Query)
                    cursor.execute(sql_Query)

                else:
                    vv=0
                    #insert into rostering
                    
                    
                    
                
                    
                    
                               

    print(msg)
    resp = make_response(json.dumps(msg))
    return resp




#----------------------------------------------------------------------------------
#Employee Category page
@app.route('/empcat')
def empcategory():
    empcatdata=mfetchempcat()
    return render_template('empcat.html',empcatdata=empcatdata)

#Perks & Expenses
@app.route('/perksexpenses')
def perksexpenses():
    return render_template('perksnexpenses.html')


@app.route('/uploadperksajax', methods = ['POST'])
def upldfile():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')
        cursor = connection.cursor()
    
        prod_mas = request.files['prod_mas']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("./static/PerksExpenses/", filename))

        #csv reader
        fn = os.path.join("./static/PerksExpenses/", filename)

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
            counter=0
            for row in rows:
                print(counter)
                empid=0
                ta=0
                mb=0
                ot=0
                sla=0
                othinc=0
                arr=0
                paymonth=0

                it=0
                idcar=0
                qualdeduc=0
                adv=0
                oth=0
                if counter>0:                        
                    print(row[0])
                    # parsing each column of a row
                    if row[0]!="":
                        empid=row[0]
                        paymonth=row[1]
                        ta=row[2]
                        mb=row[3]
                        ot=row[4]
                        sla=row[5]
                        othinc=row[6]
                        arr=row[7]

                        it=row[8]
                        idcar=row[9]
                        qualdeduc=row[10]
                        adv=row[11]
                        oth=row[12]
                        grossdeduc=float(it)+float(idcar)+float(qualdeduc)+float(adv)+float(oth)+200
                        query="";
                        query="update `TABLE 18` set `Travel Allowance`='"+str(ta)+"',`Mobile Bill`='"+str(mb)+"',`Over Time`='"+str(ot)+"',`SLA Adherence`='"+str(sla)+"',`Other Incentives`='"+str(othinc)+"',`Arrears`='"+str(arr)+"',`Income TAX`='"+str(it)+"',`ID Card`='"+str(idcar)+"',`Quality Deductions`='"+str(qualdeduc)+"',`Advance`='"+str(adv)+"',`Others`='"+str(oth)+"',`Gross Deduction`='"+str(grossdeduc)+"' where Empcode='"+str(empid)+"' and PMonth='"+str(paymonth)+"'";
                        '''
                        for col in row: 
                            query =query+"'"+col+"',"
                        query =query[:-1]
                        query=query+");"
                        '''
                    print("query :"+str(query), flush=True)
                    cursor.execute(query)
                    connection.commit()
                counter=counter+1
        except Exception as e:
            print('Failed to upload to ftp: '+ str(e))
            print("An exception occurred")
            
        csvfile.close()
        
        print("Filename :"+str(prod_mas), flush=True)       
        
        
        connection.close()
        cursor.close()
        return render_template('perksnexpenses.html',data="Data loaded successfully")

#Employee Category  add data
@app.route('/addempcat')
def addempcat():
    empcat=request.args['empcat']
    catid=request.args['catid']
    stype=request.args['type']
    acolor=request.args['acolor']
    hdtime=request.args['hdtime']
    hdcolor=request.args['hdcolor']
    fdtime=request.args['fdtime']
    fdcolor=request.args['fdcolor']
    if stype=="New":
        msg=maddempcat(empcat,acolor,hdtime,hdcolor,fdtime,fdcolor)
    if stype=="Update":
        msg=mupdateempcat(empcat,catid,acolor,hdtime,hdcolor,fdtime,fdcolor)
    resp = make_response(json.dumps(msg))
    return resp


#Employee Category  delete data
@app.route('/deleteempcat')
def deleteempcat():
    catid=request.args['id']
    empcatdata=mdeleteempcat(catid)
    return render_template('empcat.html',empcatdata=empcatdata)

#--------------------------------------------------------------------------------------------------------------

#Process - Mgr Amgr page
@app.route('/process')
def process():
    process_name_data=mfetchrec_procdata()
    print(process_name_data)
    amgrdata=mfetchmgr_amgr()
    procdata=mfetchproc()
    #print(walkindata)
    return render_template('process.html',process_name_data=process_name_data,amgrdata=amgrdata,procdata=procdata)


@app.route('/fetchprocmgr')
def fetchprocmgr():
    proc=request.args['proc']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()    
    sql_Query = "select distinct OPSManager from tblproc_setup where ProcessName='"+proc+"'"
    print(sql_Query)
    cursor.execute(sql_Query)
    mgrname = cursor.fetchall()
    connection.commit()
    mgrname=mgrname[0][0]
    print(mgrname)
    
    connection.close()
    cursor.close()
    msg=mgrname
    resp = make_response(json.dumps(msg))
    return resp


#Process page add data
@app.route('/addproc')
def addproc():
    proc=request.args['proc']
    procid=request.args['procid']
    mgr=request.args['mgr']
    amgr=request.args['amgr']
    teval=request.args['teval']
    icval=request.args['icval']
    stype=request.args['type']
    if stype=="New":
        msg=maddproc(proc,mgr,amgr,teval,icval)
    if stype=="Update":
        msg=mupdateproc(procid,proc,mgr,amgr,teval,icval)
    resp = make_response(json.dumps(msg))
    return resp

#Process page delete data
@app.route('/deleteproc')
def deleteproc():
    procid=request.args['id']
    procdata=mdeleteproc(procid)
    return render_template('process.html',procdata=procdata)


#Sourceofwalkin page
@app.route('/sourceofwalkin')
def sourceofwalkin():
    walkindata=mfetchsow()
    #print(walkindata)
    return render_template('sourceofwalkin.html',walkindata=walkindata)

#Sourceofwalkin page add data
@app.route('/addsow')
def addsow():
    sow=request.args['sow']
    sowid=request.args['sowid']
    stype=request.args['type']
    if stype=="New":
        msg=maddsow(sow)
    if stype=="Update":
        msg=mupdatesow(sow,sowid)
    resp = make_response(json.dumps(msg))
    return resp


#Sourceofwalkin page delete data
@app.route('/deletesrc')
def deletesrc():
    sowid=request.args['id']
    walkindata=mdeletesow(sowid)
    #print(walkindata)
    return render_template('sourceofwalkin.html',walkindata=walkindata)

#------------------------------------------------------------------------------
#Payroll  page
@app.route('/payrollsetup')
def payrollsetup():
    payrolldata=mfetchpayroll()
    #print(walkindata)
    return render_template('payrollsetup.html',payrolldata=payrolldata)

#Payroll update page
@app.route('/payrollupdate')
def payrollupdate():
    emplyrpf=request.args['emplyrpf']
    emppf=request.args['emppf']
    emplyresic=request.args['emplyresic']
    empesic=request.args['empesic']
    pt=request.args['pt']
    smon=request.args['smon']
    syear=request.args['syear']
    sdate=str(smon)+"-"+str(syear)
    odeduc=request.args['odeduc']
    payrolldata=mupdatepayroll(emplyrpf,emppf,emplyresic,empesic,pt,sdate,odeduc)
    #print(walkindata)
    return render_template('payrollsetup.html',payrolldata=payrolldata)

#Delete payroll routing
@app.route('/payrolldelete')
def payrolldelete():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from lkppayrollsetup where id='"+rid+"'"
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    payrolldata=mfetchpayroll()
    return render_template('payrollsetup.html',payrolldata=payrolldata)

#Payslip mail trigger
@app.route('/triggerpayslips')
def triggerpayslips():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "select * from lkppayrollsetup where id='"+str(rid)+"'"
    cursor.execute(sql_Query)
    payrollmaildata = cursor.fetchall()



    sql_Query = "select * from tblonboarding where estatus='Working' or estatus='Training'"
    print(sql_Query)
    cursor.execute(sql_Query)
    empdata = cursor.fetchall()
    paymonnum=4
    for i in range(len(empdata)):
             
        #variable list
        pmonth=''
        ename=''
        eid=''
        designation=''
        dept=''
        payabledays=''
        #month same as paymonth
        uan=''
        esi=''
        bname=''
        baccno=''
        
        retearn=''
        overtime=''
        moballow=''
        travallow=''
        salarrear=''
        othincen=''
        totearn=''
        
        pt=''
        tds=''
        emplyrpf=''
        emplyresi=''
        saladvance=''
        totdeduc=''
        netpay=''
        amtwords=''

        emppf=''
        empesi=''
        totempcontrib=''
        
        #-------------------------Mail Attachment Start----------------------
        pmonth=payrollmaildata[0][6]
        pt=payrollmaildata[0][5]
        ename=str(empdata[i][2])
        eid=str(empdata[i][1])
        designation=str(empdata[i][34])
        dept=str(empdata[i][32])
        #month same as paymonth
        uan=str(empdata[i][56])
        esi=str(empdata[i][57])
        bname=str(empdata[i][44])
        baccno=str(empdata[i][49])
        
        sql_Query = "select * from `TABLE 18` where Pmonth='"+str(paymonnum)+"' and Empcode='"+str(eid)+"'"
        print(sql_Query)
        cursor.execute(sql_Query)
        payrolldata = cursor.fetchall()

        
        payabledays=payrolldata[0][19]
        retearn='--'
        overtime=payrolldata[0][25]
        payrolldata[0][24]
        travallow=payrolldata[0][23]
        salarrear=payrolldata[0][28]
        othincen=payrolldata[0][27]
        totearn=payrolldata[0][29]
        
        pt=payrolldata[0][35]
        tds=payrolldata[0][36]
        emppf=payrolldata[0][33]
        empesi=payrolldata[0][34]
        saladvance=''
        totdeduc=payrolldata[0][41]
        netpay=payrolldata[0][42]
        amtwords=num2words(int(netpay))
        amtwords=amtwords.replace(",", "")

        emplyrpf=payrolldata[0][31]
        emplyresi=payrolldata[0][32]
        totempcontrib=float(payrolldata[0][31])+float(payrolldata[0][32])
        payabledays=float(payabledays)
        overtime=float(overtime)
        totearn=float(totearn)
        emplyrpf=float(emplyrpf)
        emplyresi=float(emplyresi)
        totdeduc=float(totdeduc)
        netpay=int(netpay)
        emppf=float(emppf)
        empesi=float(empesi)
        
        encurl=str(pmonth)+","+str(ename)+","+str(eid)+","+str(designation)+","+str(dept)+","+str(payabledays)+","+str(uan)+","+str(esi)+","+str(bname)+","+str(baccno)+","+str(retearn)+","+str(overtime)+","+str(moballow)+","+str(travallow)+","+str(salarrear)+","+str(othincen)+","+str(totearn)+","+str(pt)+","+str(tds)+","+str(emppf)+","+str(empesi)+","+str(saladvance)+","+str(totdeduc)+","+str(netpay)+","+str(amtwords)+","+str(emplyrpf)+","+str(emplyresi)+","+str(totempcontrib)
        print(encurl)

        encoded = base64.b64encode(encurl.encode('ascii'))
        print(encoded)
        encurl=encoded.decode("utf-8")
        attach_file_name = "Payslip_"+str(eid)+"_"+str(paymonnum)+".pdf"
        url='http://127.0.0.1:5000/payslip?value='+encurl
        print(url)
        #pdfkit.from_url(url,'./static/Payslips/'+str(attach_file_name))
        htmlstr="""<html><body>               <table border="0" cellspacing="0" style="font-family:Tahoma; width:100%; font-size:9px; border:solid 1px">            <tr><td>  <table style="width:100%" cellspacing="0"  border= "1">       <tr><td style="width:100%" colspan="4" >           <table style="width:100%" border="0"><tr><td colspan="4">                 <div align='center'> <b>Transact BPO Services India Pvt. Ltd.</b><br>                   #44/1-1, Industrial Suburb Ward No-10, <br>Opp. Vaishnavi Sapphire Center/Shell Petrol Bunk<br>  Yeshwanthpur, Bangalore - 560022 <br>Tel: 080-44554466</div>	                        <div><br/></div>                                        </td><td style="text-align:right;width:150px;" ><img src="data:image/png;base64,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" alt="logo" width="150" height="90">                       </table>                </td></tr>      </table>       <table  cellspacing="0" border="1"  style="width:100%; ">      <tr ><td colspan="4" style="text-align:center; "> Salary Slip For the Month of <span class="paymonth"></span> </td></tr>	<!--  </table>	  <table border="1" cellspacing="0" style="width:100%; border:solid 1px" >-->           <tr><td colspan="4">                <table border="0" cellspacing="0" style="width:100%; " >                              <tr>                                <td style="width:25%">Employee Name</td><td style="width:25%"><span class="emp_name">Demo</span></td>                                    <td style="width:25%">Month</td><td style="width:25%"><span class="paymonth"></span></td>                                  </tr>                            <tr><td>Employee ID</td><td><span class="eid"></span></td>                                                               <td>UAN</td>                                <td><span class="uan"></span></td>                           </tr>                              <tr><td>Employee Designation</td><td><span class="designation"></span></td>                                <td>ESI</td>                                <td><span class="esi"></span></td>                                </tr>                              <tr>                            <td>Department/Process</td><td><span class="dept"></span></td>                                  <td>Bank Name</td>                                  <td><span class="bname"></span></td>                           </tr>                              <tr><td>No. of Payable Days</td><td><span class="paydays"></span></td><td>Bank Account No</td><td><span class="accnum"></span></td></tr>                                               </table>           </td></tr>    </table> <table  style="width:100%; border:solid 1px;" border="1" cellspacing="0"><tr><td colspan="2"><b>Earnings</b> </td><td colspan="2"><b>Deductions</b> </td></tr>      <tr><td>Retained Earnings </td><td style="text-align:right"><span class="retearnings"></span></td><td>Tax on Profession</td><td style="text-align:right"><span class="pt"></span></td></tr>      <tr><td>Overtime </td><td style="text-align:right"><span class="ot"></span></td><td>Income Tax(TDS)</td><td style="text-align:right"><span class="tds"></span></td></tr>      <tr><td>Mobile Allowance</td><td style="text-align:right"><span class="mob"></span></td><td>Provident Fund</td><td style="text-align:right"><span class="pf"></span></td></tr>      <tr><td>Travel Allowance</td><td style="text-align:right"><span class="travel"></span></td><td>ESI Contribution</td><td style="text-align:right"><span class="esi"></span></td></tr>            <tr><td>Arrears of Salary</td><td style="text-align:right"><span class="salarrears"></span></td><td>Salary Advance</td><td style="text-align:right"><span class="saladv"></span></td></tr>       <tr><td>Other Incentive Pay </td><td style="text-align:right"><span class="othinc"></span></td><td></td><td style="text-align:right"></td></tr>      <tr><td>Total Earnings</td> <td style="text-align:right"><span class="totearnings"></span></td><td>Total Deduction</td><td style="text-align:right"><span class="totdeduc"></span></td></tr>      <tr><td>Current NET Salary</td><td colspan="3" style="text-align:right"><b><span class="netpay"></span></b></td></tr>       <tr><td>Amount in Words</td><td colspan="3"><span class="amtwords"></span> Only</td></tr>      <tr><td colspan="4" style="text-align:center"><b>Employer Contribution</b></td></tr>      <tr><td style="vertical-align:top;text-align:left">Provident Fund<br />ESI<br />Total&nbsp;</td><td style="vertical-align:top;text-align:right"><span class="emplyrpf"></span><br /><span class="emplyresi"></span><br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="emptotcontrib"></span></td><td colspan="2"><i> Note: Please update your UAN details with HR <br />to get the PF credit on regular basis</i></td></tr>          <tr><td colspan="4" style="text-align:center;">Computer Generated Report does not required Signature</td></tr>      </table>               </td></tr>            </table>            <script src="https://code.jquery.com/jquery-3.6.0.js" integrity="sha256-H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk=" crossorigin="anonymous"></script>            <script>              debugger;              var paramaters = new URLSearchParams(window.location.search);              if(paramaters.has('value'))        {            //var parameter = paramaters.get('name');			var parameter = paramaters.get('value');			parameter=atob(parameter);			//alert(parameter);			var mydataArray = parameter.split(",");            //$("#name").text(parameter);            $(".paymonth").text(mydataArray[0])			$(".emp_name").text(mydataArray[1]);			$(".eid").text(mydataArray[2]);			$(".designation").text(mydataArray[3]);			$(".dept").text(mydataArray[4]);			$(".paydays").text(mydataArray[5]);			$(".uan").text(mydataArray[6]);			$(".esi").text(mydataArray[7]);			$(".bname").text(mydataArray[8]);			$(".accnum").text(mydataArray[9]);			$(".retearnings").text(mydataArray[10]);			$(".ot").text(mydataArray[11]);			$(".mobile").text(mydataArray[12]);			$(".travel").text(mydataArray[13]);			$(".salarrears").text(mydataArray[14]);			$(".othinc").text(mydataArray[15]);			$(".totearnings").text(mydataArray[16]);			$(".pt").text(mydataArray[17]);			$(".tds").text(mydataArray[18]);			$(".pf").text(mydataArray[19]);			$(".esi").text(mydataArray[20]);			$(".saladv").text(mydataArray[21]);			$(".totdeduc").text(mydataArray[22]);			$(".netpay").text(mydataArray[23]);			$(".amtwords").text(mydataArray[24]);			$(".emplyrpf").text(mydataArray[25]);			$(".emplyresi").text(mydataArray[26]);			$(".emptotcontrib").text(mydataArray[27]);            $(".emp_name").addClass("fw-bold text-capitalize");        }            </script></body></html>"""
        
        pdfkit.from_string(htmlstr,'./static/Payslips/'+str(attach_file_name))

        
        me = "Ramnath@tacexconsulting.com"
        you = str(empdata[i][5])
        port = 465  # For SSL
        smtp_server = "smtpout.secureserver.net"
        sender_email = "Ramnath@tacexconsulting.com"
        receiver_email = you
        password = "Bharat@160805"

        msg = MIMEMultipart()
        msg['Subject'] = "Payslip Mail for the Month of Apr-2022"
        msg['From'] = me
        msg['To'] = you

        html =f"""
        \
        <html>
          <head></head>
          <body>
            <p>Please find the attachment of the payslip with this email</p>
            <br/>
            <p>Regards,</p>
            <p>HR Department</p>
          </body>
        </html>
        """

        # Record the MIME types of both parts - text/plain and text/html.
        #part1 = MIMEText(text, 'plain')
        #part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        #msg.attach(part1)
        #msg.attach(part2)




        #Attachment code snippet
        attach_file = open('./static/Payslips/'+str(attach_file_name), 'rb') # Open the file as binary mode


        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())


        #payload=MIMEApplication(attach_file.read())
        encoders.encode_base64(payload) #encode the attachment

        #add payload header with filename
        #payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
        payload.add_header('Content-Disposition', "attachment; filename= %s" % attach_file_name)
        msg.attach(payload)
        msg.attach(MIMEText(html, 'html'))
        #--------------------------------

        message = msg.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)


        #-------------------------Mail Attachment End----------------------
            
        print(num2words(36.5))
        #Original: Sunil,May,2022,12000,3000
        #Encoded: U3VuaWwsTWF5LDIwMjIsMTIwMDAsMzAwMA==
        '''
        encoded = base64.b64encode(encurl.encode('ascii'))
        print(encoded)
        encurl=encoded.decode("utf-8")
        '''


    connection.commit()
    connection.close()
    cursor.close()
    return render_template('payrollsetup.html')



@app.route('/payslip')
def payslip():
    
    return render_template('payslip.html')

#*****************************************Master Pages End*******************************************************

#Web login
@app.route('/weblogin')
def weblogin():
    return render_template('weblogin1.html')

#Letters page
@app.route('/pfdeclaration')
def pfdeclaration():
    return render_template('pfdeclaration1.html')

@app.route('/uploadajaxpfdec', methods = ['POST'])
def uploadajaxpfdec():
    print("request :"+str(request), flush=True)
    resp=""
    if request.method == 'POST':    
        prod_mas = request.files['prod_maspfdec']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("./static/DeclarationDocs/", filename))
        resp = make_response(json.dumps("Success"))
    return resp

@app.route('/transactnda')
def transactnda():
    return render_template('transactnda.html')


@app.route('/transactservicerules')
def transactservicerules():
    return render_template('transactservicerules.html')


#Onboard Email Link Genrator page
@app.route('/genmail')
def genmail():
    
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()    
    sql_Query = "select * from tblonboarding where (stat='Pending' or stat='Approved') and (Uby='HROPS' or Uby='Candidate')"
    
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()

    
    sql_Query = "select * from tblcandidate_register where (Statuss='Approved' or Statuss='HR Shortlist')"
    
    cursor.execute(sql_Query)
    intervwd_can_data = cursor.fetchall()
    
    connection.commit()
    
    connection.close()
    cursor.close()
    return render_template('mailgenerator.html',emp_primarydata=emp_primarydata,intervwd_can_data=intervwd_can_data)

@app.route('/createnewempcand')
def createnewempcand():
    #global empid
    #empid=empid+1
    empname=request.args['empname']   
    empemail=request.args['email']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()    
    sql_Query = "select Max(offerid) from tblonboarding"
    
    cursor.execute(sql_Query)
    empondata = cursor.fetchall()
    empid=0
    try:
        empid=int(empondata[0][0])+1
    except:
        empid=1

    sql_Query = "select gender,DOB,email_address,phonenumber,address1 from tblcandidate_register where email_address='"+empemail+"'"
    print(sql_Query)
    cursor.execute(sql_Query)
    rec_cand_data = cursor.fetchall()

    
    sql_Query = "select distinct qualification from lkpqualifications"    
    cursor.execute(sql_Query)
    qualdata = cursor.fetchall()
    
    sql_Query = "select distinct idproof from lkpidproof"    
    cursor.execute(sql_Query)
    idproofdata = cursor.fetchall()

    sql_Query = "select distinct bankname from lkpbanks"    
    cursor.execute(sql_Query)
    banksdata = cursor.fetchall()
    
    connection.commit()        
    connection.close()
    cursor.close()
    
    return render_template('createnewempcand.html',empname=empname,empid=empid,rec_cand_data=rec_cand_data,qualdata=qualdata,idproofdata=idproofdata,banksdata=banksdata)

#Onboard mail generation
@app.route('/genonboardmail')
def genonboardmail():
    print("request :"+str(request), flush=True)
    email=request.args['email']
    name=request.args['name']
    phone=request.args['phone']
    msg="Mail Sent"
    '''
    import smtplib 
  
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
      
    # start TLS for security 
    s.starttls() 
      
    # Authentication 
    s.login("neyathip1612@gmail.com", "neyathi@123")

    #strval = "\nhttp://10.144.100.10:5000/createnewempcand?empname="+name
    strval="<html><body><p>Dear "+name+",</p><p> Congratulation. </p><p>With Reference to your candidature and interview with at Transact BPO services. To take forward your candidature, you are required to upload your credentials on the link shared below. We will scrutinize the same and let you know if there are any shortcomings in the same. For further clarification, please contact us on 080-44554466-3</p><br/><br/><p>Website Link: http://www.google.com</p><p>User Name : (Email ID) </p><p>Password: system Generated Password (should be Case Sensitive and combination of Alpha Numeric) </p>  <br/><p>Please find the below mandate documents to be uploaded.</p>&bull; Educational certificates<br/> &bull; Address proof <br/>&bull; Aaadhar card <br/>&bull; Two references (Tel Nos, names)&ndash; Professional/General : one each <br/>&bull; Last 3 months salary slip/ Salary structure / Appointment letter of current employment <br/>&bull; Relieving letters from Past two ex-employers.</p><p>Regards, <br/>HR Department1</p></body></html>"
    
      
    # sending the mail 
    s.sendmail("sheeban864@gmail.com", email, "Click here to update candidate information "+strval) 
      
    # terminating the session 
    s.quit()
    '''
    #HTML Mail
    # me == my email address
    # you == recipient's email address
    '''
    me = "neyathip1612@gmail.com"
    you = email

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Onboarding Email"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = """\
    <html>
      <head></head>
      <body>
        <p>Dear """+name+""",</p>
        <p>Congratulation.</p>
        <p>With Reference to your candidature and interview with at Transact BPO services. To take forward your candidature, you are required to upload your credentials on the link shared below. We will scrutinize the same and let you know if there are any shortcomings in the same.</p>
        <p>For further clarification, please contact us on 080-44554466-3</p>
        <br/>
        <p>URL : </p>
        <p>\nhttp://10.144.97.120:5000/createnewempcand?empname="""+name+"""</p>
        <br/>
        <p>Please find the below mandate documents to be uploaded.</p>
        <p>* Educational certificates</p>
        <p>* Address proof</p>
        <p>* Aaadhar card</p>
        <p>* Two references (Tel Nos, names)–  Professional/General : one each</p>
        <p>* Last 3 months salary slip/ Salary structure / Appointment letter of current employment</p>
        <p>* Relieving letters from Past two ex-employers.</p>
        <br/>
        <p>Regards,</p>
        <p>HR Department</p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    #s = smtplib.SMTP('localhost')
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
      
    # start TLS for security 
    s.starttls() 
      
    # Authentication 
    s.login("neyathip1612@gmail.com", "neyathi@123")
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()
    '''
    me = "Ramnath@tacexconsulting.com"
    you = email
    port = 465  # For SSL
    smtp_server = "smtpout.secureserver.net"
    sender_email = "Ramnath@tacexconsulting.com"
    receiver_email = you
    password = "Bharat@160805"

    msg = MIMEMultipart()
    msg['Subject'] = "Onboarding Email"
    msg['From'] = me
    msg['To'] = you
    namer=name.replace(' ','%20')
    html =f"""
    \
    <html>
      <head></head>
      <body>
        <p>Dear """+name+""",</p>
        <p>Congratulation.</p>
        <p>With Reference to your candidature and interview with at Transact BPO services. To take forward your candidature, you are required to upload your credentials on the link shared below. We will scrutinize the same and let you know if there are any shortcomings in the same.</p>
        <p>For further clarification, please contact us on 080-44554466-3</p>
        <br/>
        <p>URL : </p>
        <p>\nhttp://10.144.97.120:5000/createnewempcand?empname="""+namer+"""&email="""+email+"""</p>
        <br/>
        <p>Please find the below mandate documents to be uploaded.</p>
        <p>* Educational certificates</p>
        <p>* Address proof</p>
        <p>* Aaadhar card</p>
        <p>* Two references (Tel Nos, names)–  Professional/General : one each</p>
        <p>* Last 3 months salary slip/ Salary structure / Appointment letter of current employment</p>
        <p>* Relieving letters from Past two ex-employers.</p>
        <br/>
        <p>Regards,</p>
        <p>HR Department</p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    #msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    message = msg.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


    resp = make_response(json.dumps("Mail Sent"))
    return resp

    

#Onboard triggerndaletters
@app.route('/triggerndaletters')
def triggerndaletters():
    print("request :"+str(request), flush=True)
    encurl=request.args['encurl']
    email=request.args['email']
    empcode=request.args['empcode']
    msg="Mail Sent"
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()    
    sql_Query = "select Max(Empcode) from tblEmpMgrMap"
    
    cursor.execute(sql_Query)
    maxempid= cursor.fetchall()
    empid=0
    try:
        empid=int(maxempid[0][0])+1
    except:
        empid=1
    sql_Query = "Select ename,mgrnm,amgrnm,doj,process from tblonboarding where offerid='"+str(empcode)+"'"
    cursor.execute(sql_Query)
    onboarddata= cursor.fetchall()
    ename=onboarddata[0][0]
    mgrnm=onboarddata[0][1]
    amgrnm=onboarddata[0][2]
    doj=onboarddata[0][3]
    process=onboarddata[0][4]
    datetime_object = datetime.strptime(doj, '%Y-%m-%d')
    print(datetime_object)
    dater = datetime_object.strftime("%d-%b-%y")
    print(dater)
    print(doj)
    #https://www.programiz.com/python-programming/datetime/strftime#:~:text=The%20strftime()%20method%20takes,is%20stored%20in%20now%20variable.
    
    sql_Query = "INSERT INTO tblEmpMgrMap (Empcode, EmpName, ManagerName, AsstManagerName, DateofJoin) VALUES ('"+str(empid)+"','"+str(ename)+"', '"+str(mgrnm)+"', '"+str(amgrnm)+"', '"+str(dater)+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)

    sql_Query = "update tblonboarding set stat='Approved',Empcode='"+str(empid)+"',sname='TG"+str(empid)+"' where offerid='"+empcode+"'"    
    cursor.execute(sql_Query)
    
    sql_Query = "INSERT INTO tblEmpProcMap (Empcode, ProcName) VALUES ('"+str(empid)+"', '"+str(process)+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    connection.commit()        
    connection.close()
    cursor.close()

    
    encurl=encurl+str(empid)
    encoded = base64.b64encode(encurl.encode('ascii'))
    print(encoded)
    encurl=encoded.decode("utf-8")
    print(encurl)

    #Sendimg Mail
    '''
    port = 465  # For SSL
    smtp_server = "smtpout.secureserver.net"
    sender_email = "Ramnath@tacexconsulting.com"
    receiver_email = email
    password = "Bharat@160805"
    message = f"""From: {sender_email}
    To: {receiver_email}

    Read the documents attached in the below link below \nhttp://10.144.97.120:5000/pfdeclaration?value="""+encurl

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    '''
    '''
    
    import smtplib 
  
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
      
    # start TLS for security 
    s.starttls() 
      
    # Authentication 
    s.login("neyathip1612@gmail.com", "neyathi@123")

    strval = "Read the documents attached in the below link below \nhttp://10.144.97.120:5000/pfdeclaration?value="+encurl
      
    # message to be sent 
    message = "Message_you_need_to_send"
      
    # sending the mail 
    s.sendmail("neyathip1612@gmail.com", email, strval) 
      
    # terminating the session 
    s.quit()
    '''

    me = "Ramnath@tacexconsulting.com"
    you = email
    port = 465  # For SSL
    smtp_server = "smtpout.secureserver.net"
    sender_email = "Ramnath@tacexconsulting.com"
    receiver_email = you
    password = "Bharat@160805"

    msg = MIMEMultipart()
    msg['Subject'] = "Onboarding Email"
    msg['From'] = me
    msg['To'] = you
    #namer=name.replace(' ','%20')
    html =f"""
    \
    <html>
      <head></head>
      <body>
        <p>Dear """+ename+""",</p>
        <p>An hearty welcome to Transact !.</p>
        <p>In the next step of onboarding process, we expect your to read through the documents to accept the terms and conditions and agreements as a part of employment with Transact.</p>
        <br/>
		<p>Once the document is read, accepted and authorised the file has to be uploaded to complete your joining formalities.</p>
        <p>Our team is excited to meet and take you though the induction to familiarise the work culture and environment.</p>

		<p>Let us look forward to a mutually beneficial association.</p>
		<p>URL : </p>
        <p>Read the documents attached in the below link below \nhttp://10.144.97.120:5000/pfdeclaration?value="""+encurl+"""</p>
        <br/>
        
        <br/>
        <p>Regards,</p>
        <p>HR Department</p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    #msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    message = msg.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


    resp = make_response(json.dumps("Mail Sent"))
    
    return resp

@app.route('/login')
def login():
    return render_template('login1.html')

@app.route('/onboarding')
def onboarding():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "select * from tblonboarding where stat='Processed'"
    
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    return render_template('onboarding.html',emp_primarydata=emp_primarydata)

# Search onboard Employee
@app.route('/searchonboardemp')
def searchonboardemp():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    empid=''
    ename=''
    edob=''
    ephone=''
    procnm=''
    estatus=''
    empid=request.args['empid']
    ename=request.args['ename']
    edob=request.args['edob']
    ephone=request.args['ephone']
    procnm=request.args['procnm']
    estatus=request.args['estatus']
    
    sql_Query=''
    if empid!='':
        sql_Query = "select * from tblonboarding where Empcode='"+str(empid)+"'"
    elif ename!='':
        sql_Query = "select * from tblonboarding where ename like '%"+str(ename)+"%'"
    elif edob!='':
        sql_Query = "select * from tblonboarding where edob='"+str(edob)+"'"
    elif ephone!='':
        sql_Query = "select * from tblonboarding where phone='"+str(ephone)+"'"
    elif estatus!='':
        sql_Query = "select * from tblonboarding where estatus='"+str(estatus)+"'"
    elif procnm!='':
        sql_Query = "select * from tblonboarding where process='"+str(procnm)+"'"
    else:
        sql_Query = "select * from tblonboarding"
    print(sql_Query)
    '''
    if empid!='':
        sql_Query=sql_Query+"empid="+empid+" and "
    else:
        sql_Query=sql_Query+"empid="+empid+" or "
        
    if procnm!='':
        sql_Query=sql_Query+"process="+procnm
    if ename!='':
        sql_Query=sql_Query+"ename="+ename
    '''
    cursor.execute(sql_Query)
    onboarddata = cursor.fetchall()
    msg=""
    for i in range(len(onboarddata)):
        msg=msg+str(onboarddata[i][1])+","
        msg=msg+str(onboarddata[i][2])+","
        msg=msg+str(onboarddata[i][4])+","
        msg=msg+str(onboarddata[i][5])+","
        msg=msg+str(onboarddata[i][6])+","
        msg=msg+str(onboarddata[i][0])+"#"


        
    connection.commit()        
    connection.close()
    cursor.close()
    
    #print(msg)
    resp = make_response(json.dumps(msg))
    #print(msg, flush=True)
    return resp

#Sign PF -All docs in one
@app.route('/signpfdeclaration')
def signpfdeclaration():
    empid=request.args['empid']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "update tblonboarding set pfdeclaration='Signed',nda='Signed',servicerules='Signed' where Empcode='"+empid+"'"
    print(sql_Query)
    cursor.execute(sql_Query)
    connection.commit()
    
    connection.close()
    cursor.close()
    msg="Authorization captured"
    resp = make_response(json.dumps(msg))
    return resp



#Sign NDA
@app.route('/signndadeclaration')
def signndadeclaration():
    empid=request.args['empid']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "update tblonboarding set nda='Signed' where empid='"+empid+"'"
    
    cursor.execute(sql_Query)
    connection.commit()
    
    connection.close()
    cursor.close()
    msg="Signature captured"
    resp = make_response(json.dumps(msg))
    return resp


#Sign Service Rules
@app.route('/signserruledeclaration')
def signserruledeclaration():
    empid=request.args['empid']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "update tblonboarding set servicerules='Signed' where empid='"+empid+"'"    
    cursor.execute(sql_Query)
    connection.commit()
    
    connection.close()
    cursor.close()
    msg="Signature captured"
    resp = make_response(json.dumps(msg))
    return resp





@app.route('/verifyemp')
def verifyemp():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "select * from tblonboarding where stat='Approved'"# and Uby='HROPS'
    
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    return render_template('verifyemphome.html',emp_primarydata=emp_primarydata)

@app.route('/veremplist')
def veremplist():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "select * from tblonboarding where stat<>'Pending'"
    
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    return render_template('veremplist.html',emp_primarydata=emp_primarydata)

#Onboarding - empstat verify
@app.route('/verifyempstat')
def verifyempstat():
    empid=request.args['empid']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()  

    
    sql_Query = "update tblonboarding set stat='Processed',Uby='HROPS' where offerid='"+empid+"'"
    print(sql_Query)
    cursor.execute(sql_Query)
    print('aaa')
    sql_Query = "select * from tblonboarding where stat='Pending' and Uby='HROPS'"
    
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    return render_template('verifyemphome.html',emp_primarydata=emp_primarydata)



#Onboarding - HROPS emp verify
@app.route('/verifyempstat1', methods = ['GET','POST'])
def verifyempstat1():    
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        empid=request.form.get('empid')
        #prod_mas = request.files['imgfile']
        filename =request.form.get('imgfile')
        print(filename)
        #secure_filename(prod_mas.filename)
        #prod_mas.save(os.path.join("./static/ProfilePic/", filename))
        ename=request.form.get('ename')
        print(ename)
        edob=request.form.get('edob')
        email=request.form.get('email')
        phone=request.form.get('phone') 
        gender=request.form.get('gender')         
        landline=request.form.get('landline')
        bgroup=request.form.get('bgroup')
        sname=request.form.get('sname')
        ecat=request.form.get('ecat')
        emeconname=request.form.get('emeconname')
        emeconph=request.form.get('emeconph')
        fname=request.form.get('fname')
        fdob=request.form.get('fdob')
        mname=request.form.get('mname')
        mdob=request.form.get('mdob')
        paddr=request.form.get('paddr')
        taddr=request.form.get('taddr')
        mstatus=request.form.get('mstatus')
        sponame=request.form.get('sponame')
        spodob=request.form.get('spodob')
        
        estatus=request.form.get('estatus')
        idate=request.form.get('idate')
        doj=request.form.get('doj')
        dol=request.form.get('dol')
        bgv=request.form.get('bgv')
        certdate=request.form.get('certdate')
        reason=request.form.get('reason')
        walkinsource=request.form.get('walkinsource')
        exp=request.form.get('exp')
        depts=request.form.get('depts')
        process=request.form.get('process')
        position=request.form.get('position')
        mgrnm=request.form.get('mgrnm')
        amgrnm=request.form.get('amgrnm')
        ctc=request.form.get('ctc')
        bsal=request.form.get('bsal')
        gsal=request.form.get('gsal')
        bpay=request.form.get('bpay')
        nsal=request.form.get('nsal')
        sladh=request.form.get('sladh')
        effdate=request.form.get('effdate')
        bname=request.form.get('bname')
        ifsc=request.form.get('ifsc')
        accname=request.form.get('accname')
        branchname=request.form.get('branchname')
        partwagehr=request.form.get('partwagehr')
        baccnum=request.form.get('baccnum')
        minsnum=request.form.get('minsnum')
        minsamt=request.form.get('minsamt')
        opf=request.form.get('opf')
        oesi=request.form.get('oesi')
        enablepf=request.form.get('enablepf')
        enableesi=request.form.get('enableesi')
        enablepf=request.form.get('enablepf')
        enableesi=request.form.get('enableesi')
        uan=request.form.get('uan')
        esinum=request.form.get('esinum')
        emplyrpf=request.form.get('emplyrpf')
        emppf=request.form.get('emppf')
        emplyresic=request.form.get('emplyresic')
        empesic=request.form.get('empesic')
        proftax=request.form.get('proftax')
        proftax=request.form.get('proftax')
        edstatus=request.form.get('edstatus')
        stat='Pending'
        uby='HROPS'


        
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
        cursor = connection.cursor()

        sql_Query = "select filename from tblonboarding where offerid='"+str(empid)+"'"
        print(sql_Query)
        cursor.execute(sql_Query)
        imagename = cursor.fetchall()
        imagename=imagename[0][0]
        print(imagename)
        
        sql_Query = "delete from tblonboarding where offerid='"+str(empid)+"'"
        print(sql_Query)
        cursor.execute(sql_Query)
        
        
        
        sql_Query = "insert into tblonboarding values('"+str(empid)+"',0,'"+str(ename)+"','"+str(gender)+"','"+str(edob)+"','"+str(email)+"','"+str(phone)+"','"+str(landline)+"','"+str(bgroup)+"','TG"+str(empid)+"','"+str(ecat)+"','"+str(emeconname)+"','"+str(emeconph)+"','"+str(fname)+"','"+str(fdob)+"','"+str(mname)+"','"+str(mdob)+"','"+str(paddr)+"','"+str(taddr)+"','"+str(mstatus)+"','"+str(sponame)+"','"+str(spodob)+"','"+str(imagename)+"','"+str(estatus)+"','"+str(idate)+"','"+str(doj)+"','"+str(dol)+"','"+str(bgv)+"','"+str(certdate)+"','"+str(reason)+"','"+str(walkinsource)+"','"+str(exp)+"','"+str(depts)+"','"+str(process)+"','"+str(position)+"','"+str(mgrnm)+"','"+str(amgrnm)+"','"+str(ctc)+"','"+str(bsal)+"','"+str(gsal)+"','"+str(bpay)+"','"+str(nsal)+"','"+str(sladh)+"','"+str(effdate)+"','"+str(bname)+"','"+str(ifsc)+"','"+str(accname)+"','"+str(branchname)+"','"+str(partwagehr)+"','"+str(baccnum)+"','"+str(minsnum)+"','"+str(minsamt)+"','"+str(opf)+"','"+str(oesi)+"','"+str(enablepf)+"','"+str(enableesi)+"','"+str(uan)+"','"+str(esinum)+"','"+str(emplyrpf)+"','"+str(emppf)+"','"+str(emplyresic)+"','"+str(empesic)+"','"+str(proftax)+"','"+str(edstatus)+"','"+str(stat)+"','"+str(uby)+"','Not Signed','Not Signed','Not Signed')"
        print(sql_Query)
        cursor.execute(sql_Query)

        sql_Query = "INSERT INTO tblemppaymentinfo(Offerid,Empcode,CTC,BasicSal,GrossSal,BasePay,NetSal,SlAdhere,EffectDate,BankName,IFSC,AccountName,BranchName,PartTmrCost,Accnum,MedInsNum,MedInsAmt,OldPf,OldEsi,UAN,ESInum,EmprPF,EmpPF,EmprESIC,EmpESIC,PT) values ('"+str(str(empid))+"',0,'"+str(ctc)+"','"+str(bsal)+"', '"+str(gsal)+"','"+str(bpay)+"','"+str(nsal)+"','"+str(sladh)+"','"+str(effdate)+"','"+str(bname)+"','"+str(ifsc)+"','"+str(accname)+"','"+str(branchname)+"','"+str(partwagehr)+"','"+str(baccnum)+"','"+str(minsnum)+"','"+str(minsamt)+"','"+str(opf)+"','"+str(oesi)+"','"+str(uan)+"','"+str(esinum)+"','"+str(emplyrpf)+"','"+str(emppf)+"','"+str(emplyresic)+"','"+str(empesic)+"','"+str(proftax)+"')"
        print(sql_Query)
        cursor.execute(sql_Query)

        
        '''
        # Commented after offer id
        #sql_Query = "INSERT INTO `TABLE 18` (`Empcode`, `Tot Hrs`, `Basic(Rs)`, `Empr PF cont`, `Empr ESI cont`, `Emp PF Cont`, `Emp ESI Cont`, `CTC (Rs)`, `Gross Salary`, `Tot Present`, `WO`, `HD`, `LHD`, `NH`, `LOP`, `DLOP`, `CL`, `SL`, `AL`, `Payable Days`, `Training Days`, `Salary Per Day`, `Earned Gross`, `Travel Allowance`, `Mobile Bill`, `Over Time`, `100 Day Complete`, `Other Incentives`, `Arrears`, `Gross Earnings`, `Earned Basic`, `Emp PF Cont1`, `Emp ESI Cont1`, `Empr PF Cont1`, `Empr ESI Cont1`, `Prof TAX`, `Income TAX`, `ID Card`, `Quality Deductions`, `Advance`, `Others`, `Gross Deduction`, `Net Salary`, `Account No`, `Bank Name`, `Acc Holder Name`, `Branch Name`, `IFSC Code`, `UAN`, `PF Number`, `EmpStatus`, `Base Pay`, `SL Adherence`, `CalcSL Adherence`) VALUES ('"+empid+"', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--')"
        sql_Query = "INSERT INTO `TABLE 18` (`Empcode`, `Tot Hrs`, `Basic(Rs)`, `Empr PF cont`, `Empr ESI cont`, `Emp PF Cont`, `Emp ESI Cont`, `CTC (Rs)`, `Gross Salary`, `Tot Present`, `WO`, `HD`, `LHD`, `NH`, `LOP`, `DLOP`, `CL`, `SL`, `AL`, `Payable Days`, `Training Days`, `Salary Per Day`, `Earned Gross`, `Travel Allowance`, `Mobile Bill`, `Over Time`, `SLA Adherence`, `Other Incentives`, `Arrears`, `Gross Earnings`, `Earned Basic`, `Emp PF Cont1`, `Emp ESI Cont1`, `Empr PF Cont1`, `Empr ESI Cont1`, `Prof TAX`, `Income TAX`, `ID Card`, `Quality Deductions`, `Advance`, `Others`, `Gross Deduction`, `Net Salary`, `Account No`, `Bank Name`, `Acc Holder Name`, `Branch Name`, `IFSC Code`, `UAN`, `PF Number`, `EmpStatus`, `Base Pay`, `SL Adherence`, `CalcSL Adherence`) VALUES ('"+empid+"', '0', '"+bsal+"', '"+emplyrpf+"', '"+emplyresic+"', '"+emppf+"', '"+empesic+"', '"+ctc+"', '"+gsal+"', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--')"
        print(sql_Query)
        cursor.execute(sql_Query)
        
        sql_Query = "INSERT INTO `tblEmpMgrMap` (`Empcode`, `EmpName`, `ManagerName`, `AsstManagerName`, `DateofJoin`) VALUES ('"+str(empid)+"','"+str(ename)+"', '"+str(mgrnm)+"', '"+str(amgrnm)+"', '"+str(doj)+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        
        sql_Query = "INSERT INTO `tblEmpProcMap` (`Empcode`, `ProcName`) VALUES ('"+str(empid)+"', '"+str(process)+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        '''
        
        sql_Query = "select * from tblonboarding where stat='Pending' and Uby='Candidate'"    
        cursor.execute(sql_Query)
        emp_primarydata=[]
        try:
            emp_primarydata = cursor.fetchall()
        except:
            print('No data to return')
        connection.commit()
        
        connection.close()
        cursor.close()
        return render_template('mailgenerator.html',emp_primarydata=emp_primarydata)
'''
empid=request.args['empid']
connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
cursor = connection.cursor()

sql_Query = "update tblonboarding set Uby='HROPS' where empid='"+empid+"'"

cursor.execute(sql_Query)
print('aaa')

sql_Query = "select * from tblonboarding where stat='Pending' and Uby='Candidate'"

cursor.execute(sql_Query)
emp_primarydata = cursor.fetchall()
connection.commit()

connection.close()
cursor.close()
return render_template('mailgenerator.html',emp_primarydata=emp_primarydata)
'''



#Onboarding - empstat re-verify
@app.route('/updateverifyempstat')
def updateverifyempstat():
    empid=request.args['empid']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()

    sql_Query = "select * from tblonboarding where stat='Processed'"
    
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    return render_template('verifyemphome.html',emp_primarydata=emp_primarydata)



#HR Manager Verify emp
@app.route('/seedata')
def seedata():
    empcode=request.args['empcode']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "select * from tblonboarding where offerid="+str(empcode)
    
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()

    
    sql_Query = "select * from tblonboardingqual where offerid="+str(empcode)
    
    cursor.execute(sql_Query)
    emp_qualdata = cursor.fetchall()

    
    sql_Query = "select * from tblonboardingidcard where offerid="+str(empcode)
    
    cursor.execute(sql_Query)
    emp_idcarddata = cursor.fetchall()


    
    sql_Query = "select * from tblonboardingscandoc where offerid="+str(empcode)
    print(sql_Query)
    
    cursor.execute(sql_Query)
    emp_scandocdata = cursor.fetchall()
    print(emp_scandocdata)


    
    sql_Query = "select * from tblonboardingcovidrep where offerid="+str(empcode)
    print(sql_Query)
    
    cursor.execute(sql_Query)
    emp_covidrep = cursor.fetchall()
    print(emp_covidrep)
    
    sql_Query = "select * from tblonboardingexpcert where offerid="+str(empcode)
    print(sql_Query)
    
    cursor.execute(sql_Query)
    emp_expcert = cursor.fetchall()

    


    sql_Query = "select * from lkppayrollsetup"    
    cursor.execute(sql_Query)
    payrolldata = cursor.fetchall()

    sql_Query = "select srcwlkin from lkpsourofwalkin"    
    cursor.execute(sql_Query)
    sourcedata = cursor.fetchall()

    sql_Query = "select distinct procname from lkpprocmgrmap"    
    cursor.execute(sql_Query)
    processdata = cursor.fetchall()

    sql_Query = "select distinct dept from lkpdepartments"    
    cursor.execute(sql_Query)
    deptsdata = cursor.fetchall()

    sql_Query = "select distinct position from lkppositions"    
    cursor.execute(sql_Query)
    positionsdata = cursor.fetchall()


    sql_Query = "select distinct qualification from lkpqualifications"    
    cursor.execute(sql_Query)
    qualdata = cursor.fetchall()    
    
    sql_Query = "select distinct idproof from lkpidproof"    
    cursor.execute(sql_Query)
    idproofdata = cursor.fetchall()

    
    
    sql_Query = "select distinct catname from lkpempcategory"    
    cursor.execute(sql_Query)
    empcatdata = cursor.fetchall()

    
    sql_Query = "select distinct bankname from lkpbanks"    
    cursor.execute(sql_Query)
    banksdata = cursor.fetchall()

    connection.commit()
    
    connection.close()
    cursor.close()
    return render_template('verifyemp.html',sourcedata=sourcedata,deptsdata=deptsdata,positionsdata=positionsdata,qualdata=qualdata,banksdata=banksdata,empcatdata=empcatdata,idproofdata=idproofdata,payrolldata=payrolldata,processdata=processdata,emp_primarydata=emp_primarydata,emp_qualdata=emp_qualdata,emp_idcarddata=emp_idcarddata,emp_scandocdata=emp_scandocdata,emp_covidrep=emp_covidrep,emp_expcert=emp_expcert)        

#HROPS verify emp
@app.route('/seedata1')
def seedata1():
    empcode=request.args['empcode']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "select * from tblonboarding where offerid="+str(empcode)
    
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()

    
    sql_Query = "select * from tblonboardingqual where offerid="+str(empcode)
    
    cursor.execute(sql_Query)
    emp_qualdata = cursor.fetchall()

    
    sql_Query = "select * from tblonboardingidcard where offerid="+str(empcode)
    
    cursor.execute(sql_Query)
    emp_idcarddata = cursor.fetchall()


    
    sql_Query = "select * from tblonboardingscandoc where offerid="+str(empcode)
    print(sql_Query)
    
    cursor.execute(sql_Query)
    emp_scandocdata = cursor.fetchall()
    print(emp_scandocdata)
    
    
    sql_Query = "select * from tblonboardingcovidrep where offerid="+str(empcode)
    print(sql_Query)
    
    cursor.execute(sql_Query)
    emp_covidrep = cursor.fetchall()
    print(emp_covidrep)
    
    sql_Query = "select * from tblonboardingexpcert where offerid="+str(empcode)
    print(sql_Query)
    
    cursor.execute(sql_Query)
    emp_expcert = cursor.fetchall()


    sql_Query = "select * from lkppayrollsetup"    
    cursor.execute(sql_Query)
    payrolldata = cursor.fetchall()

    sql_Query = "select srcwlkin from lkpsourofwalkin"    
    cursor.execute(sql_Query)
    sourcedata = cursor.fetchall()

    sql_Query = "select distinct procname from lkpprocmgrmap"    
    cursor.execute(sql_Query)
    processdata = cursor.fetchall()

    sql_Query = "select distinct dept from lkpdepartments"    
    cursor.execute(sql_Query)
    deptsdata = cursor.fetchall()

    sql_Query = "select distinct position from lkppositions"    
    cursor.execute(sql_Query)
    positionsdata = cursor.fetchall()


    sql_Query = "select distinct qualification from lkpqualifications"    
    cursor.execute(sql_Query)
    qualdata = cursor.fetchall()    
    
    sql_Query = "select distinct idproof from lkpidproof"    
    cursor.execute(sql_Query)
    idproofdata = cursor.fetchall()

    
    
    sql_Query = "select distinct catname from lkpempcategory"    
    cursor.execute(sql_Query)
    empcatdata = cursor.fetchall()

    
    sql_Query = "select distinct bankname from lkpbanks"    
    cursor.execute(sql_Query)
    banksdata = cursor.fetchall()

    sql_Query = "select distinct mgrname, amgrname from lkpprocmgrmap"
    #sql_Query = "select distinct ManagerName,  AsstManagerName from tblEmpMgrMap where Empcode in (select Empcode from tblEmpProcMap where ProcName='"+str(process)+"')"
            
    cursor.execute(sql_Query)
    mgr_amgrdata = cursor.fetchall()

    
    connection.commit()    
    connection.close()
    cursor.close()
    return render_template('hropsverifyemp.html',mgr_amgrdata=mgr_amgrdata,banksdata=banksdata,qualdata=qualdata,idproofdata=idproofdata,empcatdata=empcatdata,emp_primarydata=emp_primarydata,emp_qualdata=emp_qualdata,emp_idcarddata=emp_idcarddata,emp_scandocdata=emp_scandocdata,emp_covidrep=emp_covidrep,emp_expcert=emp_expcert,sourcedata=sourcedata,deptsdata=deptsdata,processdata=processdata,positionsdata=positionsdata)   


@app.route('/seeverempdata')
def seeverempdata():
    empcode=request.args['empcode']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "select * from tblonboarding where offerid="+str(empcode)
    
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()

    
    sql_Query = "select * from tblonboardingqual where offerid="+str(empcode)
    
    cursor.execute(sql_Query)
    emp_qualdata = cursor.fetchall()

    
    sql_Query = "select * from tblonboardingidcard where offerid="+str(empcode)
    
    cursor.execute(sql_Query)
    emp_idcarddata = cursor.fetchall()


    
    sql_Query = "select * from tblonboardingscandoc where offerid="+str(empcode)
    print(sql_Query)
    
    cursor.execute(sql_Query)
    emp_scandocdata = cursor.fetchall()
    print(emp_scandocdata)

    sql_Query = "select * from tblonboardingcovidrep where offerid="+str(empcode)
    print(sql_Query)
    
    cursor.execute(sql_Query)
    emp_covidrep = cursor.fetchall()
    print(emp_covidrep)
    
    sql_Query = "select * from tblonboardingexpcert where offerid="+str(empcode)
    print(sql_Query)
    
    cursor.execute(sql_Query)
    emp_expcert = cursor.fetchall()


    
    sql_Query = "select distinct procname from lkpprocmgrmap"    
    cursor.execute(sql_Query)
    processdata = cursor.fetchall()

    sql_Query = "select distinct dept from lkpdepartments"    
    cursor.execute(sql_Query)
    deptsdata = cursor.fetchall()

    sql_Query = "select distinct position from lkppositions"    
    cursor.execute(sql_Query)
    positionsdata = cursor.fetchall()

    
    sql_Query = "select distinct mgrname from lkpprocmgrmap"    
    cursor.execute(sql_Query)
    mgrdata = cursor.fetchall()

    
    sql_Query = "select distinct amgrname from lkpprocmgrmap"    
    cursor.execute(sql_Query)
    amgrdata = cursor.fetchall()

    sql_Query = "select distinct catname from lkpempcategory"    
    cursor.execute(sql_Query)
    empcatdata = cursor.fetchall()

    sql_Query = "select distinct dept from lkpdepartments"    
    cursor.execute(sql_Query)
    deptsdata = cursor.fetchall()

    sql_Query = "select distinct position from lkppositions"    
    cursor.execute(sql_Query)
    positionsdata = cursor.fetchall()
    
    sql_Query = "select distinct qualification from lkpqualifications"    
    cursor.execute(sql_Query)
    qualdata = cursor.fetchall()    
    
    sql_Query = "select distinct idproof from lkpidproof"    
    cursor.execute(sql_Query)
    idproofdata = cursor.fetchall()

    

    sql_Query = "select distinct bankname from lkpbanks"    
    cursor.execute(sql_Query)
    banksdata = cursor.fetchall()

    
    connection.commit()
    
    connection.close()
    cursor.close()
    return render_template('seeveremp.html',idproofdata=idproofdata,banksdata=banksdata,qualdata=qualdata,empcatdata=empcatdata,emp_primarydata=emp_primarydata,emp_qualdata=emp_qualdata,emp_idcarddata=emp_idcarddata,emp_scandocdata=emp_scandocdata,mgrdata=mgrdata,amgrdata=amgrdata,emp_expcert=emp_expcert,emp_covidrep=emp_covidrep,processdata=processdata,deptsdata=deptsdata,positionsdata=positionsdata)        


@app.route('/load_mgr_amgr')
def load_mgr_amgr():    
    process=request.args['process']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select distinct mgrname, amgrname from lkpprocmgrmap where procname='"+str(process)+"'"
    #sql_Query = "select distinct ManagerName,  AsstManagerName from tblEmpMgrMap where Empcode in (select Empcode from tblEmpProcMap where ProcName='"+str(process)+"')"
            
    cursor.execute(sql_Query)
    mgr_amgrdata = cursor.fetchall()
    msg=""
    for i in range(len(mgr_amgrdata)):
        msg=msg+str(mgr_amgrdata[i][0])+","
        msg=msg+str(mgr_amgrdata[i][1])+"#"        
    connection.commit()        
    connection.close()
    cursor.close()
    
    #print(msg)
    resp = make_response(json.dumps(msg))
    #print(msg, flush=True)
    return resp

@app.route('/createnewemp')
def createnewemp():
    #global empid
    #empid=empid+1
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()    
    sql_Query = "select Max(offerid) from tblonboarding"
    
    cursor.execute(sql_Query)
    empondata = cursor.fetchall()
    empid=0
    try:
        print('aaaa')
        print(empid)
        empid=int(empondata[0][0])+1
    except:
        print('bbb')
        print(empid)
        empid=1
    sql_Query = "select * from lkppayrollsetup"    
    cursor.execute(sql_Query)
    payrolldata = cursor.fetchall()

    sql_Query = "select srcwlkin from lkpsourofwalkin"    
    cursor.execute(sql_Query)
    sourcedata = cursor.fetchall()

    sql_Query = "select distinct procname from lkpprocmgrmap"    
    cursor.execute(sql_Query)
    processdata = cursor.fetchall()

    sql_Query = "select distinct dept from lkpdepartments"    
    cursor.execute(sql_Query)
    deptsdata = cursor.fetchall()

    sql_Query = "select distinct position from lkppositions"    
    cursor.execute(sql_Query)
    positionsdata = cursor.fetchall()
    
    sql_Query = "select distinct qualification from lkpqualifications"    
    cursor.execute(sql_Query)
    qualdata = cursor.fetchall()    
    
    sql_Query = "select distinct idproof from lkpidproof"    
    cursor.execute(sql_Query)
    idproofdata = cursor.fetchall()

    
    
    sql_Query = "select distinct catname from lkpempcategory"    
    cursor.execute(sql_Query)
    empcatdata = cursor.fetchall()

    sql_Query = "select distinct bankname from lkpbanks"    
    cursor.execute(sql_Query)
    banksdata = cursor.fetchall()
    
    connection.commit()        
    connection.close()
    cursor.close()
    empname=request.args['empname']   
    
    return render_template('createnewemp.html',banksdata=banksdata,empname=empname,empid=empid,payrolldata=payrolldata,sourcedata=sourcedata,processdata=processdata,empcatdata=empcatdata,deptsdata=deptsdata,idproofdata=idproofdata,positionsdata=positionsdata,qualdata=qualdata)


#Salary Range verification onboarding

@app.route('/verifyctcval')
def verifyctcval():
    process=request.args['process']
    position=request.args['position']
    print(position)
    query=''
    if position=="Manager":
        query="Select MgrMinSal,MgrMaxSal from tblproc_setup where ProcessName='"+process+"' limit 1"
    elif position=="Assistant Manager":
        query="Select AsstMinSal,AsstMaxSal from tblproc_setup where ProcessName='"+process+"' limit 1"
    elif position=="Customer Service Representative":
        query="Select CSRMinSal,CSRMaxSal from tblproc_setup where ProcessName='"+process+"' limit 1"
    elif position=="Team Leader":
        query="Select TLMinSal,TLMaxSal from tblproc_setup where ProcessName='"+process+"' limit 1"

        
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    msg=''
    print(query)
    cursor.execute(query)
    saldata = cursor.fetchall()

    for i in range(len(saldata)):
        msg=msg+str(saldata[i][0])+","
        msg=msg+str(saldata[i][1])
    resp = make_response(json.dumps(msg))
    return resp


#Onboarding - Delete File
@app.route('/delfile')
def delfile():
    print("request :"+str(request), flush=True)
    empid=request.args['empid']
    fileid=request.args['fileid']
    tblname=request.args['tbl']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query=""
    msg=""
    if tblname=="tblonboardingidcard":
        
        sql_Query = "delete from "+str(tblname)+" where id="+str(fileid)
        print(sql_Query)
        cursor.execute(sql_Query)
        
        sql_Query = "select * from tblonboardingidcard where offerid="+str(empid)
            
        cursor.execute(sql_Query)
        empqualdata = cursor.fetchall()
        msg=""
        for i in range(len(empqualdata)):
            msg=msg+str(empqualdata[i][0])+","
            msg=msg+str(empqualdata[i][2])+","
            msg=msg+str(empqualdata[i][3])+"#"
            
    if tblname=="tblonboardingcovidrep":
        
        sql_Query = "delete from "+str(tblname)+" where id="+str(fileid)
        print(sql_Query)
        cursor.execute(sql_Query)
        
        sql_Query = "select * from tblonboardingcovidrep where offerid="+str(empid)
            
        cursor.execute(sql_Query)
        empcovrepdata = cursor.fetchall()
        msg=""
        for i in range(len(empcovrepdata)):
            msg=msg+str(empcovrepdata[i][0])+","
            msg=msg+str(empcovrepdata[i][2])+","
            msg=msg+str(empcovrepdata[i][3])+"#"
            
    if tblname=="tblonboardingqual":
        
        sql_Query = "delete from "+str(tblname)+" where id="+str(fileid)
        print(sql_Query)
        cursor.execute(sql_Query)
        
        sql_Query = "select * from tblonboardingqual where offerid="+str(empid)
            
        cursor.execute(sql_Query)
        empqualdata = cursor.fetchall()
        msg=""
        for i in range(len(empqualdata)):
            msg=msg+str(empqualdata[i][0])+","
            msg=msg+str(empqualdata[i][2])+","
            msg=msg+str(empqualdata[i][3])+"#"
            
    if tblname=="tblonboardingscandoc":
        
        sql_Query = "delete from "+str(tblname)+" where id="+str(fileid)
        print(sql_Query)
        cursor.execute(sql_Query)
        
        sql_Query = "select * from tblonboardingscandoc where offerid="+str(empid)
            
        cursor.execute(sql_Query)
        empqualdata = cursor.fetchall()
        msg=""
        for i in range(len(empqualdata)):
            msg=msg+str(empqualdata[i][0])+","
            msg=msg+str(empqualdata[i][2])+","
            msg=msg+str(empqualdata[i][3])+","
            msg=msg+str(empqualdata[i][4])+"#"
            
    if tblname=="tblonboardingexpcert":
        
        sql_Query = "delete from "+str(tblname)+" where id="+str(fileid)
        print(sql_Query)
        cursor.execute(sql_Query)
        
        sql_Query = "select * from tblonboardingexpcert where offerid="+str(empid)
            
        cursor.execute(sql_Query)
        empidcertdata = cursor.fetchall()
        msg=""
        for i in range(len(empidcertdata)):
            msg=msg+str(empidcertdata[i][0])+","
            msg=msg+str(empidcertdata[i][2])+","
            msg=msg+str(empidcertdata[i][3])+","
            msg=msg+str(empidcertdata[i][4])+","
            msg=msg+str(empidcertdata[i][5])+","
            msg=msg+str(empidcertdata[i][6])+"#"


        
    connection.commit()        
    connection.close()
    cursor.close()
    
    #print(msg)
    resp = make_response(json.dumps(msg))
    #print(msg, flush=True)
    return resp

#Onboarding - add qualification file
@app.route('/addqualfile', methods = ['POST'])
def addqualfile():
    print("request :"+str(request.method), flush=True)
    if request.method == 'POST':
        empid=request.form.get('empid')
        print(empid)
        qual=request.form.get('qual') 
        prod_mas = request.files['qualfile']
        print(prod_mas)
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("./static/QualFile/", filename))
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
        cursor = connection.cursor()        
        sql_Query = "insert into tblonboardingqual(offerid, qualification, document) values('"+empid+"','"+qual+"','"+filename+"')"
        print(sql_Query)
        cursor.execute(sql_Query)

        sql_Query = "select * from tblonboardingqual where offerid="+empid
        
        cursor.execute(sql_Query)
        empqualdata = cursor.fetchall()
        msg=""
        for i in range(len(empqualdata)):
            msg=msg+str(empqualdata[i][0])+","
            msg=msg+str(empqualdata[i][2])+","
            msg=msg+str(empqualdata[i][3])+"#"

        
        connection.commit()        
        connection.close()
        cursor.close()
        
        print(msg)
        resp = make_response(json.dumps(msg))
        #print(msg, flush=True)
        return resp

#Onboarding - add Covid report file
@app.route('/addcovidrep', methods = ['POST'])
def addcovidrep():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        empid=request.form.get('empid')
        cvaacine=request.form.get('cvaacine') 
        prod_mas = request.files['covidreport']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("./static/CovidReports/", filename))
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
        cursor = connection.cursor()        
        sql_Query = "insert into tblonboardingcovidrep(offerid, vactype, document) values('"+empid+"','"+cvaacine+"','"+filename+"')"
        print(sql_Query)
        cursor.execute(sql_Query)

        sql_Query = "select * from tblonboardingcovidrep where offerid="+empid
        
        cursor.execute(sql_Query)
        empcovidrepdata = cursor.fetchall()
        msg=""
        for i in range(len(empcovidrepdata)):
            msg=msg+str(empcovidrepdata[i][0])+","
            msg=msg+str(empcovidrepdata[i][2])+","
            msg=msg+str(empcovidrepdata[i][3])+"#"

        
        connection.commit()        
        connection.close()
        cursor.close()
        
        print(msg)
        resp = make_response(json.dumps(msg))
        #print(msg, flush=True)
        return resp
    
#Onboarding - add scan doc file
@app.route('/addscandoc', methods = ['POST'])
def addscandoc():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        empid=request.form.get('empid')
        scanletter=request.form.get('scanletter') 
        comporder=request.form.get('comporder') 
        prod_mas = request.files['scanletterfile']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("./static/ScanDoc/", filename))
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
        cursor = connection.cursor()        
        sql_Query = "insert into tblonboardingscandoc(offerid, lettertype, document,comporder) values('"+empid+"','"+scanletter+"','"+filename+"','"+comporder+"')"
        print(sql_Query)
        cursor.execute(sql_Query)

        sql_Query = "select * from tblonboardingscandoc where offerid="+empid
        
        cursor.execute(sql_Query)
        empqualdata = cursor.fetchall()
        msg=""
        for i in range(len(empqualdata)):
            msg=msg+str(empqualdata[i][0])+","
            msg=msg+str(empqualdata[i][2])+","
            msg=msg+str(empqualdata[i][3])+","
            msg=msg+str(empqualdata[i][4])+"#"

        
        connection.commit()        
        connection.close()
        cursor.close()
        
        print(msg)
        resp = make_response(json.dumps(msg))
        #print(msg, flush=True)
        return resp
    
#Onboarding - add id card file
@app.route('/addidcard', methods = ['POST'])
def addidcard():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        empid=request.form.get('empid')
        govtidcard=request.form.get('govtidcard')
        prod_mas = request.files['idcardfile']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("./static/IdCards/", filename))
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
        cursor = connection.cursor()        
        sql_Query = "insert into tblonboardingidcard(offerid, govtidcard, document) values('"+empid+"','"+govtidcard+"','"+filename+"')"
        print(sql_Query)
        cursor.execute(sql_Query)

        sql_Query = "select * from tblonboardingidcard where offerid="+empid
        
        cursor.execute(sql_Query)
        empidcarddata = cursor.fetchall()
        msg=""
        for i in range(len(empidcarddata)):
            msg=msg+str(empidcarddata[i][0])+","
            msg=msg+str(empidcarddata[i][2])+","
            msg=msg+str(empidcarddata[i][3])+"#"

        
        connection.commit()        
        connection.close()
        cursor.close()
        
        print(msg)
        resp = make_response(json.dumps(msg))
        #print(msg, flush=True)
        return resp

#Onboarding - add exp cert file
@app.route('/addcertfile', methods = ['POST'])
def addcertfile():
    print("request :"+str(request), flush=True)
    print(request.method)
    if request.method == 'POST':
        empid=request.form.get('empid')
        ecomp=request.form.get('ecomp')
        efrom=request.form.get('efrom')
        eto=request.form.get('eto')
        print(eto)
        edesig=request.form.get('edesig')
        prod_mas = request.files['expcert']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("./static/CertFile/", filename))
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
        cursor = connection.cursor()        
        sql_Query = "insert into tblonboardingexpcert(offerid, company, cfrom,cto,designation,certificate) values('"+empid+"','"+ecomp+"','"+efrom+"','"+eto+"','"+edesig+"','"+filename+"')"
        print(sql_Query)
        cursor.execute(sql_Query)

        sql_Query = "select * from tblonboardingexpcert where offerid="+empid
        
        cursor.execute(sql_Query)
        empidcertdata = cursor.fetchall()
        msg=""
        for i in range(len(empidcertdata)):
            msg=msg+str(empidcertdata[i][0])+","
            msg=msg+str(empidcertdata[i][2])+","
            msg=msg+str(empidcertdata[i][3])+","
            msg=msg+str(empidcertdata[i][4])+","
            msg=msg+str(empidcertdata[i][5])+","
            msg=msg+str(empidcertdata[i][6])+"#"

        
        connection.commit()        
        connection.close()
        cursor.close()
        
        print(msg)
        resp = make_response(json.dumps(msg))
        #print(msg, flush=True)
        return resp
    

#Onboarding - Save new employee
@app.route('/savenewemp', methods = ['POST'])
def savenewemp():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        empid=request.form.get('empid')        
        prod_mas = request.files['imgfile']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("./static/ProfilePic/", filename))
        ename=request.form.get('ename')
        edob=request.form.get('edob')
        email=request.form.get('email')
        phone=request.form.get('phone') 
        gender=request.form.get('gender')         
        landline=request.form.get('landline')
        bgroup=request.form.get('bgroup')
        sname=request.form.get('sname')
        ecat=request.form.get('ecat')
        emeconname=request.form.get('emeconname')
        emeconph=request.form.get('emeconph')
        fname=request.form.get('fname')
        fdob=request.form.get('fdob')
        mname=request.form.get('mname')
        mdob=request.form.get('mdob')
        paddr=request.form.get('paddr')
        taddr=request.form.get('taddr')
        mstatus=request.form.get('mstatus')
        sponame=request.form.get('sponame')
        spodob=request.form.get('spodob')
        
        estatus=request.form.get('estatus')
        idate=request.form.get('idate')
        doj=request.form.get('doj')
        dol=request.form.get('dol')
        bgv=request.form.get('bgv')
        certdate=request.form.get('certdate')
        reason=request.form.get('reason')
        walkinsource=request.form.get('walkinsource')
        exp=request.form.get('exp')
        depts=request.form.get('depts')
        process=request.form.get('process')
        position=request.form.get('position')
        mgrnm=request.form.get('mgrnm')
        amgrnm=request.form.get('amgrnm')
        ctc=request.form.get('ctc')
        bsal=request.form.get('bsal')
        gsal=request.form.get('gsal')
        bpay=request.form.get('bpay')
        nsal=request.form.get('nsal')
        sladh=request.form.get('sladh')
        effdate=request.form.get('effdate')
        bname=request.form.get('bname')
        ifsc=request.form.get('ifsc')
        accname=request.form.get('accname')
        branchname=request.form.get('branchname')
        partwagehr=request.form.get('partwagehr')
        baccnum=request.form.get('baccnum')
        minsnum=request.form.get('minsnum')
        minsamt=request.form.get('minsamt')
        opf=request.form.get('opf')
        oesi=request.form.get('oesi')
        enablepf=request.form.get('enablepf')
        enableesi=request.form.get('enableesi')
        enablepf=request.form.get('enablepf')
        enableesi=request.form.get('enableesi')
        uan=request.form.get('uan')
        esinum=request.form.get('esinum')
        emplyrpf=request.form.get('emplyrpf')
        emppf=request.form.get('emppf')
        emplyresic=request.form.get('emplyresic')
        empesic=request.form.get('empesic')
        proftax=request.form.get('proftax')
        edstatus=request.form.get('edstatus')
        stat='Pending'
        uby='HROPS'


        
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
        cursor = connection.cursor()
        
        sql_Query = "insert into tblonboarding values('"+str(empid)+"',0,'"+str(ename)+"','"+str(gender)+"','"+str(edob)+"','"+str(email)+"','"+str(phone)+"','"+str(landline)+"','"+str(bgroup)+"','TG"+str(empid)+"','"+str(ecat)+"','"+str(emeconname)+"','"+str(emeconph)+"','"+str(fname)+"','"+str(fdob)+"','"+str(mname)+"','"+str(mdob)+"','"+str(paddr)+"','"+str(taddr)+"','"+str(mstatus)+"','"+str(sponame)+"','"+str(spodob)+"','"+str(filename)+"','"+str(estatus)+"','"+str(idate)+"','"+str(doj)+"','"+str(dol)+"','"+str(bgv)+"','"+str(certdate)+"','"+str(reason)+"','"+str(walkinsource)+"','"+str(exp)+"','"+str(depts)+"','"+str(process)+"','"+str(position)+"','"+str(mgrnm)+"','"+str(amgrnm)+"','"+str(ctc)+"','"+str(bsal)+"','"+str(gsal)+"','"+str(bpay)+"','"+str(nsal)+"','"+str(sladh)+"','"+str(effdate)+"','"+str(bname)+"','"+str(ifsc)+"','"+str(accname)+"','"+str(branchname)+"','"+str(partwagehr)+"','"+str(baccnum)+"','"+str(minsnum)+"','"+str(minsamt)+"','"+str(opf)+"','"+str(oesi)+"','"+str(enablepf)+"','"+str(enableesi)+"','"+str(uan)+"','"+str(esinum)+"','"+str(emplyrpf)+"','"+str(emppf)+"','"+str(emplyresic)+"','"+str(empesic)+"','"+str(proftax)+"','"+str(edstatus)+"','"+str(stat)+"','"+str(uby)+"','Not Signed','Not Signed','Not Signed')"
        print(sql_Query)
        cursor.execute(sql_Query)

        sql_Query = "INSERT INTO tblemppaymentinfo(Offerid,Empcode,CTC,BasicSal,GrossSal,BasePay,NetSal,SlAdhere,EffectDate,BankName,IFSC,AccountName,BranchName,PartTmrCost,Accnum,MedInsNum,MedInsAmt,OldPf,OldEsi,UAN,ESInum,EmprPF,EmpPF,EmprESIC,EmpESIC,PT) values ('"+str(str(empid))+"',0,'"+str(ctc)+"','"+str(bsal)+"', '"+str(gsal)+"','"+str(bpay)+"','"+str(nsal)+"','"+str(sladh)+"','"+str(effdate)+"','"+str(bname)+"','"+str(ifsc)+"','"+str(accname)+"','"+str(branchname)+"','"+str(partwagehr)+"','"+str(baccnum)+"','"+str(minsnum)+"','"+str(minsamt)+"','"+str(opf)+"','"+str(oesi)+"','"+str(uan)+"','"+str(esinum)+"','"+str(emplyrpf)+"','"+str(emppf)+"','"+str(emplyresic)+"','"+str(empesic)+"','"+str(proftax)+"')"
        print(sql_Query)
        cursor.execute(sql_Query)

        
        '''
        # Commented after offer id
        #sql_Query = "INSERT INTO `TABLE 18` (`Empcode`, `Tot Hrs`, `Basic(Rs)`, `Empr PF cont`, `Empr ESI cont`, `Emp PF Cont`, `Emp ESI Cont`, `CTC (Rs)`, `Gross Salary`, `Tot Present`, `WO`, `HD`, `LHD`, `NH`, `LOP`, `DLOP`, `CL`, `SL`, `AL`, `Payable Days`, `Training Days`, `Salary Per Day`, `Earned Gross`, `Travel Allowance`, `Mobile Bill`, `Over Time`, `100 Day Complete`, `Other Incentives`, `Arrears`, `Gross Earnings`, `Earned Basic`, `Emp PF Cont1`, `Emp ESI Cont1`, `Empr PF Cont1`, `Empr ESI Cont1`, `Prof TAX`, `Income TAX`, `ID Card`, `Quality Deductions`, `Advance`, `Others`, `Gross Deduction`, `Net Salary`, `Account No`, `Bank Name`, `Acc Holder Name`, `Branch Name`, `IFSC Code`, `UAN`, `PF Number`, `EmpStatus`, `Base Pay`, `SL Adherence`, `CalcSL Adherence`) VALUES ('"+empid+"', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--')"
        sql_Query = "INSERT INTO `TABLE 18` (`Empcode`, `Tot Hrs`, `Basic(Rs)`, `Empr PF cont`, `Empr ESI cont`, `Emp PF Cont`, `Emp ESI Cont`, `CTC (Rs)`, `Gross Salary`, `Tot Present`, `WO`, `HD`, `LHD`, `NH`, `LOP`, `DLOP`, `CL`, `SL`, `AL`, `Payable Days`, `Training Days`, `Salary Per Day`, `Earned Gross`, `Travel Allowance`, `Mobile Bill`, `Over Time`, `SLA Adherence`, `Other Incentives`, `Arrears`, `Gross Earnings`, `Earned Basic`, `Emp PF Cont1`, `Emp ESI Cont1`, `Empr PF Cont1`, `Empr ESI Cont1`, `Prof TAX`, `Income TAX`, `ID Card`, `Quality Deductions`, `Advance`, `Others`, `Gross Deduction`, `Net Salary`, `Account No`, `Bank Name`, `Acc Holder Name`, `Branch Name`, `IFSC Code`, `UAN`, `PF Number`, `EmpStatus`, `Base Pay`, `SL Adherence`, `CalcSL Adherence`) VALUES ('"+empid+"', '0', '"+bsal+"', '"+emplyrpf+"', '"+emplyresic+"', '"+emppf+"', '"+empesic+"', '"+ctc+"', '"+gsal+"', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--')"
        print(sql_Query)
        cursor.execute(sql_Query)
        
        sql_Query = "INSERT INTO `tblEmpMgrMap` (`Empcode`, `EmpName`, `ManagerName`, `AsstManagerName`, `DateofJoin`) VALUES ('"+str(empid)+"','"+str(ename)+"', '"+str(mgrnm)+"', '"+str(amgrnm)+"', '"+str(doj)+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        
        sql_Query = "INSERT INTO `tblEmpProcMap` (`Empcode`, `ProcName`) VALUES ('"+str(empid)+"', '"+str(process)+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        '''

        
        
        sql_Query = "select * from tblonboarding"
        
        cursor.execute(sql_Query)
        emp_primarydata = cursor.fetchall()
        
        connection.commit()
        
        connection.close()
        cursor.close()
        return render_template('onboarding.html',emp_primarydata=emp_primarydata)
    '''
    empid=request.args['empid']
    ename=request.args['ename']
    edob=request.args['edob']
    email=request.args['email']
    phone=request.args['phone']
    #Empcode varchar(50), EmpName varchar(50), DOB varchar(50), Email varchar(50), Mobile varchar(50) 
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "insert into tblonboarding values('"+empid+"','"+ename+"','"+edob+"','"+email+"','"+phone+"')"
    cursor.execute(sql_Query)
    
    sql_Query = "select * from tblonboarding"
    
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()
    
    connection.commit()
    
    connection.close()
    cursor.close()

    return render_template('onboarding.html',emp_primarydata=emp_primarydata)
    '''



    


#Onboarding - Save new employee by candidate
@app.route('/savenewemp1', methods = ['POST'])
def savenewemp1():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        empid=request.form.get('empid')        
        prod_mas = request.files['imgfile']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("./static/ProfilePic/", filename))
        ename=request.form.get('ename')
        edob=request.form.get('edob')
        email=request.form.get('email')
        phone=request.form.get('phone') 
        gender=request.form.get('gender')         
        landline=request.form.get('landline')
        bgroup=request.form.get('bgroup')
        sname=request.form.get('sname')
        ecat=request.form.get('ecat')
        emeconname=request.form.get('emeconname')
        emeconph=request.form.get('emeconph')
        fname=request.form.get('fname')
        fdob=request.form.get('fdob')
        mname=request.form.get('mname')
        mdob=request.form.get('mdob')
        paddr=request.form.get('paddr')
        taddr=request.form.get('taddr')
        mstatus=request.form.get('mstatus')
        sponame=request.form.get('sponame')
        spodob=request.form.get('spodob')
        
        estatus=request.form.get('estatus')
        idate=request.form.get('idate')
        doj=request.form.get('doj')
        dol=request.form.get('dol')
        bgv=request.form.get('bgv')
        certdate=request.form.get('certdate')
        reason=request.form.get('reason')
        walkinsource=request.form.get('walkinsource')
        exp=request.form.get('exp')
        depts=request.form.get('depts')
        process=request.form.get('process')
        position=request.form.get('position')
        mgrnm=request.form.get('mgrnm')
        amgrnm=request.form.get('amgrnm')
        ctc=request.form.get('ctc')
        bsal=request.form.get('bsal')
        gsal=request.form.get('gsal')
        bpay=request.form.get('bpay')
        nsal=request.form.get('nsal')
        sladh=request.form.get('sladh')
        effdate=request.form.get('effdate')
        bname=request.form.get('bname')
        ifsc=request.form.get('ifsc')
        accname=request.form.get('accname')
        branchname=request.form.get('branchname')
        partwagehr=request.form.get('partwagehr')
        baccnum=request.form.get('baccnum')
        minsnum=request.form.get('minsnum')
        minsamt=request.form.get('minsamt')
        opf=request.form.get('opf')
        oesi=request.form.get('oesi')
        enablepf=request.form.get('enablepf')
        enableesi=request.form.get('enableesi')
        enablepf=request.form.get('enablepf')
        enableesi=request.form.get('enableesi')
        uan=request.form.get('uan')
        esinum=request.form.get('esinum')
        emplyrpf=request.form.get('emplyrpf')
        emppf=request.form.get('emppf')
        emplyresic=request.form.get('emplyresic')
        empesic=request.form.get('empesic')
        proftax=request.form.get('proftax')
        edstatus=request.form.get('edstatus')
        stat='Pending'
        uby='Candidate'


        
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
        cursor = connection.cursor()
        
        sql_Query = "insert into tblonboarding values('"+str(empid)+"',0,'"+str(ename)+"','"+str(gender)+"','"+str(edob)+"','"+str(email)+"','"+str(phone)+"','"+str(landline)+"','"+str(bgroup)+"','TG"+str(empid)+"','"+str(ecat)+"','"+str(emeconname)+"','"+str(emeconph)+"','"+str(fname)+"','"+str(fdob)+"','"+str(mname)+"','"+str(mdob)+"','"+str(paddr)+"','"+str(taddr)+"','"+str(mstatus)+"','"+str(sponame)+"','"+str(spodob)+"','"+str(filename)+"','"+str(estatus)+"','"+str(idate)+"','"+str(doj)+"','"+str(dol)+"','"+str(bgv)+"','"+str(certdate)+"','"+str(reason)+"','"+str(walkinsource)+"','"+str(exp)+"','"+str(depts)+"','"+str(process)+"','"+str(position)+"','"+str(mgrnm)+"','"+str(amgrnm)+"','"+str(ctc)+"','"+str(bsal)+"','"+str(gsal)+"','"+str(bpay)+"','"+str(nsal)+"','"+str(sladh)+"','"+str(effdate)+"','"+str(bname)+"','"+str(ifsc)+"','"+str(accname)+"','"+str(branchname)+"','"+str(partwagehr)+"','"+str(baccnum)+"','"+str(minsnum)+"','"+str(minsamt)+"','"+str(opf)+"','"+str(oesi)+"','"+str(enablepf)+"','"+str(enableesi)+"','"+str(uan)+"','"+str(esinum)+"','"+str(emplyrpf)+"','"+str(emppf)+"','"+str(emplyresic)+"','"+str(empesic)+"','"+str(proftax)+"','"+str(edstatus)+"','"+str(stat)+"','"+str(uby)+"','Not Signed','Not Signed','Not Signed')"
        print(sql_Query)
        cursor.execute(sql_Query)

        sql_Query = "INSERT INTO tblemppaymentinfo(Offerid,Empcode,CTC,BasicSal,GrossSal,BasePay,NetSal,SlAdhere,EffectDate,BankName,IFSC,AccountName,BranchName,PartTmrCost,Accnum,MedInsNum,MedInsAmt,OldPf,OldEsi,UAN,ESInum,EmprPF,EmpPF,EmprESIC,EmpESIC,PT) values ('"+str(str(empid))+"',0,'"+str(ctc)+"','"+str(bsal)+"', '"+str(gsal)+"','"+str(bpay)+"','"+str(nsal)+"','"+str(sladh)+"','"+str(effdate)+"','"+str(bname)+"','"+str(ifsc)+"','"+str(accname)+"','"+str(branchname)+"','"+str(partwagehr)+"','"+str(baccnum)+"','"+str(minsnum)+"','"+str(minsamt)+"','"+str(opf)+"','"+str(oesi)+"','"+str(uan)+"','"+str(esinum)+"','"+str(emplyrpf)+"','"+str(emppf)+"','"+str(emplyresic)+"','"+str(empesic)+"','"+str(proftax)+"')"
        print(sql_Query)
        cursor.execute(sql_Query)

        
        '''
        # Commented after offer id
        #sql_Query = "INSERT INTO `TABLE 18` (`Empcode`, `Tot Hrs`, `Basic(Rs)`, `Empr PF cont`, `Empr ESI cont`, `Emp PF Cont`, `Emp ESI Cont`, `CTC (Rs)`, `Gross Salary`, `Tot Present`, `WO`, `HD`, `LHD`, `NH`, `LOP`, `DLOP`, `CL`, `SL`, `AL`, `Payable Days`, `Training Days`, `Salary Per Day`, `Earned Gross`, `Travel Allowance`, `Mobile Bill`, `Over Time`, `100 Day Complete`, `Other Incentives`, `Arrears`, `Gross Earnings`, `Earned Basic`, `Emp PF Cont1`, `Emp ESI Cont1`, `Empr PF Cont1`, `Empr ESI Cont1`, `Prof TAX`, `Income TAX`, `ID Card`, `Quality Deductions`, `Advance`, `Others`, `Gross Deduction`, `Net Salary`, `Account No`, `Bank Name`, `Acc Holder Name`, `Branch Name`, `IFSC Code`, `UAN`, `PF Number`, `EmpStatus`, `Base Pay`, `SL Adherence`, `CalcSL Adherence`) VALUES ('"+empid+"', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--')"
        sql_Query = "INSERT INTO `TABLE 18` (`Empcode`, `Tot Hrs`, `Basic(Rs)`, `Empr PF cont`, `Empr ESI cont`, `Emp PF Cont`, `Emp ESI Cont`, `CTC (Rs)`, `Gross Salary`, `Tot Present`, `WO`, `HD`, `LHD`, `NH`, `LOP`, `DLOP`, `CL`, `SL`, `AL`, `Payable Days`, `Training Days`, `Salary Per Day`, `Earned Gross`, `Travel Allowance`, `Mobile Bill`, `Over Time`, `SLA Adherence`, `Other Incentives`, `Arrears`, `Gross Earnings`, `Earned Basic`, `Emp PF Cont1`, `Emp ESI Cont1`, `Empr PF Cont1`, `Empr ESI Cont1`, `Prof TAX`, `Income TAX`, `ID Card`, `Quality Deductions`, `Advance`, `Others`, `Gross Deduction`, `Net Salary`, `Account No`, `Bank Name`, `Acc Holder Name`, `Branch Name`, `IFSC Code`, `UAN`, `PF Number`, `EmpStatus`, `Base Pay`, `SL Adherence`, `CalcSL Adherence`) VALUES ('"+empid+"', '0', '"+bsal+"', '"+emplyrpf+"', '"+emplyresic+"', '"+emppf+"', '"+empesic+"', '"+ctc+"', '"+gsal+"', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--')"
        print(sql_Query)
        cursor.execute(sql_Query)
        
        sql_Query = "INSERT INTO `tblEmpMgrMap` (`Empcode`, `EmpName`, `ManagerName`, `AsstManagerName`, `DateofJoin`) VALUES ('"+str(empid)+"','"+str(ename)+"', '"+str(mgrnm)+"', '"+str(amgrnm)+"', '"+str(doj)+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        
        sql_Query = "INSERT INTO `tblEmpProcMap` (`Empcode`, `ProcName`) VALUES ('"+str(empid)+"', '"+str(process)+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        '''

        


        
        
        sql_Query = "select * from tblonboarding"
        
        cursor.execute(sql_Query)
        emp_primarydata = cursor.fetchall()
        
        connection.commit()
        
        connection.close()
        cursor.close()
        return render_template('onboarding.html',emp_primarydata=emp_primarydata)


@app.route('/exceldownload')
def download_excel():    
    month=request.args['month']
    print('ffff')
    year=request.args['year']
    secode=request.args['secode']
    procnm=request.args['procnm']
    mgrname=request.args['mgrnm']
    wb = Workbook()
    ws = wb.active
    findat=[]
    datesfinallist=[]
    
    #Dates Creation
    mydate = datetime.now()
    todays_date = datetime.today()
    '''
    # Fetching Dates
    #print("Current year:", todays_date.year)
    #print("Current month:", todays_date.month)
    #print("Current day:", todays_date.day)
    '''

    pmonth=''
    nmonth=''
    
    
    # Version 2 of attendance
    mydate = datetime.today()
    ##print(mydate.day)

    n = 0
    mydate = mydate - pd.DateOffset(months=n)
    
    startdate=""
    enddate=""
    if mydate.day>=16:
        startdate=str(mydate.year)+"-"+str(int(month)-1)+"-16"
        pmonth=mydate.month-1
        nmonth=mydate.month
        enddate=str(mydate.year)+"-"+str(month)+"-15"
    else:
        prevmonth=mydate.month-1
        pmonth=mydate.month
        nmonth=mydate.month+1
        startdate=str(mydate.year)+"-"+str(prevmonth)+"-16"    
        enddate=str(mydate.year)+"-"+str(mydate.month)+"-15"
    pmonth=monthname(int(month)-1)
    nmonth=monthname(int(month))
    dateslist=pd.date_range(start=startdate,end=enddate)
    for i in range(len(dateslist)):
        dt=str(dateslist[i])[0:10]
        dtval=dt.split('-')
        dtval[1]=getMonthName(str(dtval[1]))
        dtval[0]=int(dtval[0])-2000
        findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
        
        datesfinallist.append(findate)

    
    datescount=len(datesfinallist)
    startmon=int(month)-1
    endmon=int(month)
    smonname= monthname(startmon)
    emonname=monthname(endmon)
    #Header Creation
    header=["E.Code","E.Name","Asst.Manager","Manager","D.O.J","Process"]
    for i in range(len(datesfinallist)):
        header.append(datesfinallist[i])
    payrollheader=["Tot Hrs","Basic(Rs)","Empr PF cont","Empr ESI cont","Emp PF Cont","Emp ESI Cont","CTC (Rs)","Gross Salary","Tot Present","WO","HD","LHD","NH","LOP","DLOP","CL","SL","AL","Payable Days","Training Days","Salary Per Day","Earned Gross","Travel Allowance","Mobile Bill","Over Time","SLA Adherence","Other Incentives","Arrears","Gross Earnings","Earned Basic","Emp PF Cont","Emp ESI Cont","Empr PF Cont","Empr ESI Cont","Prof TAX","Income TAX","ID Card","Quality Deductions","Advance","Others","Gross Deduction","Net Salary","Account No","Bank Name","Acc Holder Name","Branch Name","IFSC Code","UAN","PF Number","EmpStatus","Base Pay","SL Adherence","CalcSL Adherence"]
    for i in range(len(payrollheader)):
        header.append(payrollheader[i])
    #print(header)

    findat.append(header)
    print(findat)
    
    #Data for excel
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()

    
    if secode=='' and procnm=='' and mgrname=='':
        #sql_Query = "SELECT distinct Cast(tblEmployeeTotalHours.Empcode as decimal) As ECode,empname,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmployeeTotalHours, tblEmpProcMap where tblEmployeeTotalHours.Empcode=tblEmpProcMap.Empcode  group by ECode order by ECode"
        
        sql_Query = "SELECT distinct Cast(tblEmpMgrMap.Empcode as decimal) As ECode,EmpName,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmpMgrMap, tblEmpProcMap where tblEmpMgrMap.Empcode=tblEmpProcMap.Empcode  group by ECode order by ECode"
        cursor.execute(sql_Query)
        emp_primarydata = cursor.fetchall()
        print(emp_primarydata)



        yr=int(todays_date.year)
        yr=yr-2000
        strval=str(todays_date.day)+"-"+mydate.strftime("%b")+"-"+str(yr)
        #print(strval)
        #Date 1-15 check
        #monwise="-"+mydate.strftime("%b")+"-"+str(yr)
        monwise="-"+pmonth+"-"+str(yr)
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode "
        print(sql_Query)
        cursor.execute(sql_Query)
        emp16_attdata = cursor.fetchall()
        print(emp16_attdata)
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp17_attdata = cursor.fetchall()
        
        sql_Query = "SELECT  CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp18_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        print(sql_Query)
        cursor.execute(sql_Query)
        emp18_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp19_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp20_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%'  and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp21_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp22_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp23_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp24_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp25_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp26_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp27_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp28_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp29_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp30_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp31_attdata = cursor.fetchall()

        #print('==========')
        #Date 1-15 check
        #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
        #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
        monwise="-"+nmonth+"-"+str(yr)
        print(monwise)
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp1_attdata = cursor.fetchall()
        ##print(emp1_attdata)
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp2_attdata = cursor.fetchall()
        ##print(emp2_attdata)
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp3_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp4_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp5_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        print(sql_Query)
        cursor.execute(sql_Query)
        emp6_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp7_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp8_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp9_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp10_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp11_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp12_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp13_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp14_attdata = cursor.fetchall()
        
        sql_Query = "SELECT CONVERT(Empcode,Decimal) as Empcode,Atype from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%' and Empcode in (Select Empcode from  tblEmpMgrMap) order by Empcode"
        print(sql_Query)
        cursor.execute(sql_Query)
        emp15_attdata = cursor.fetchall()

        '''
        smonwise="-"+str(smonname)+"-"+str(yr)
        emonwise="-"+str(emonname)+"-"+str(yr)
        sql_Query = "SELECT y.Empcode,y.thours FROM (SELECT distinct Cast(Empcode as decimal) As Empcode ,sum(TotalHrs) as 'thours' from tblEmpTotalHoursSimp where (DateFor like '%16"+str(smonwise)+"%' or DateFor like '%17"+str(smonwise)+"%' or DateFor like '%18"+str(smonwise)+"%' or DateFor like '%19"+str(smonwise)+"%' or DateFor like '%20"+str(smonwise)+"%') group by EmpCode order by EmpCode)y where y.thours>=0"
        #print(sql_Query)
        cursor.execute(sql_Query)
        tothrs_attdata = cursor.fetchall()
        '''
        monnum=int(month)
        sql_Query = "SELECT *,CONVERT(Empcode,Decimal) as Empcode from `TABLE 18` where PMonth='"+str(monnum)+"' order by Empcode"
        #print(sql_Query)
        cursor.execute(sql_Query)
        payrolldata = cursor.fetchall()
        #print(payrolldata)
        #print(emp16_attdata)
        #print('--------------------------')
        k=0
        k1=0
        k2=0
        k3=0
        k4=0
        k5=0
        k6=0
        k7=0
        k8=0
        k9=0
        k10=0
        k11=0
        k12=0
        k13=0
        k14=0
        k15=0
        k16=0
        k17=0
        k18=0
        k19=0
        k20=0
        k21=0
        k22=0
        k23=0
        k24=0
        k25=0
        k26=0
        k27=0
        k28=0
        k29=0
        k30=0
        k31=0
        th1=0
        for i in range(len(emp_primarydata)):
            dd=[]
            for j in range(0,len(emp_primarydata[i])):
                #print(emp_primarydata[i])
                #print('--------------------------')              
                dd.append(emp_primarydata[i][j])
            
            try:
                print(str(emp16_attdata[k][0]))
                print("x- "+str(emp_primarydata[i][0]))            
                if str(emp_primarydata[i][0])==str(emp16_attdata[k][0]):
                    dd.append(emp16_attdata[i][1]) 
                    print(emp16_attdata[k][1])  
                    k=k+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            '''
            try:
                print(str(emp16_attdata[k][0]))
                print("x- "+str(emp_primarydata[i][0]))
                if str(emp_primarydata[i][0])==str(emp16_attdata[k][0]):
                    dd.append(emp16_attdata[k][1])
                    print(emp16_attdata[k][1])
                    k=k+1
                else:
                    flagger=0
                    while(flagger==0):
                        k=k+1
                        
                        print(str(emp16_attdata[k][0]))
                        print("x- "+str(emp_primarydata[i][0]))
                        if str(emp_primarydata[i][0])==str(emp16_attdata[k][0]):
                            dd.append(emp16_attdata[k][1])
                            print(emp16_attdata[k][1])
                            flagger=1
                    if flagger==0:
                        dd.append("A")
                    #k=k-1
            except:
                    dd.append("")
            '''
            try:            
                if str(emp_primarydata[i][0])==str(emp17_attdata[k1][0]):
                    dd.append(emp17_attdata[i][1])   
                    k1=k1+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp18_attdata[k2][0]):
                    dd.append(emp18_attdata[i][1])   
                    k2=k2+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp19_attdata[k3][0]):
                    dd.append(emp19_attdata[i][1])   
                    k3=k3+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp20_attdata[k4][0]):
                    dd.append(emp20_attdata[i][1])   
                    k4=k4+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp21_attdata[k5][0]):
                    dd.append(emp21_attdata[i][1])   
                    k5=k5+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp22_attdata[k6][0]):
                    dd.append(emp22_attdata[i][1])   
                    k6=k6+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp23_attdata[k7][0]):
                    dd.append(emp23_attdata[i][1])   
                    k7=k7+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp24_attdata[k8][0]):
                    dd.append(emp24_attdata[i][1])   
                    k8=k8+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp25_attdata[k9][0]):
                    dd.append(emp25_attdata[i][1])   
                    k9=k9+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp26_attdata[k10][0]):
                    dd.append(emp26_attdata[i][1])   
                    k10=k10+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp27_attdata[k11][0]):
                    dd.append(emp27_attdata[i][1])   
                    k11=k11+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp28_attdata[k12][0]):
                    dd.append(emp28_attdata[i][1])   
                    k12=k12+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            if datescount>28:
                try:            
                    if str(emp_primarydata[i][0])==str(emp29_attdata[k13][0]):
                        dd.append(emp29_attdata[i][1])   
                        k13=k13+1
                    else:
                        dd.append("A")
                except:
                        dd.append("")
                try:            
                    if str(emp_primarydata[i][0])==str(emp30_attdata[k14][0]):
                        dd.append(emp30_attdata[i][1])   
                        k14=k14+1
                    else:
                        dd.append("A")
                except:
                        dd.append("")
                        
            if datescount==31:
                try:            
                    if str(emp_primarydata[i][0])==str(emp31_attdata[k15][0]):
                        dd.append(emp31_attdata[i][1])    
                        k15=k15+1 
                    else:
                        dd.append("A")
                except:
                        dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp1_attdata[k16][0]):
                    dd.append(emp1_attdata[i][1])     
                    k16=k16+1 
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp2_attdata[k17][0]):
                    dd.append(emp2_attdata[i][1])   
                    k17=k17+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp3_attdata[k18][0]):
                    dd.append(emp3_attdata[i][1])   
                    k18=k18+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp4_attdata[k19][0]):
                    dd.append(emp4_attdata[i][1])   
                    k19=k19+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp5_attdata[k20][0]):
                    dd.append(emp5_attdata[i][1])   
                    k20=k20+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp6_attdata[k21][0]):
                    dd.append(emp6_attdata[i][1])   
                    k21=k21+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp7_attdata[k22][0]):
                    dd.append(emp7_attdata[i][1])   
                    k22=k22+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp8_attdata[k23][0]):
                    dd.append(emp8_attdata[i][1])   
                    k23=k23+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp9_attdata[k24][0]):
                    dd.append(emp9_attdata[i][1])   
                    k24=k24+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp10_attdata[k25][0]):
                    dd.append(emp10_attdata[i][1])   
                    k25=k25+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp11_attdata[k26][0]):
                    dd.append(emp11_attdata[i][1])   
                    k26=k26+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:
                print("emp"+str(emp_primarydata[i][0]))
                print("mmm-"+str(emp12_attdata[k27][0]))
                if str(emp_primarydata[i][0])==str(emp12_attdata[k27][0]):
                    dd.append(emp12_attdata[i][1])
                    print(emp12_attdata[i][1])
                    k27=k27+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp13_attdata[k28][0]):
                    dd.append(emp13_attdata[i][1])   
                    k28=k28+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp14_attdata[k29][0]):
                    dd.append(emp14_attdata[i][1])   
                    k29=k29+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            try:            
                if str(emp_primarydata[i][0])==str(emp15_attdata[k30][0]):
                    dd.append(emp15_attdata[i][1])   
                    k30=k30+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            '''
            try:            
                if str(emp_primarydata[i][0])==str(tothrs_attdata[th1][0]):
                    dd.append(tothrs_attdata[i][1])   
                    th1=th1+1
                else:
                    dd.append("A")
            except:
                    dd.append("")
            '''
            
            try:
                print("emp"+str(emp_primarydata[i][0]))
                print("Pay-"+str(payrolldata[i][0]))
                
                for m in range(i,len(payrolldata)):                    
                    if str(emp_primarydata[i][0])==str(payrolldata[m][0]):
                        for j in range(1,len(payrolldata)):
                            dd.append(payrolldata[i][j])
                        break
                    #else:
                        #dd.append("A")
            except:
                    dd.append("")
                
            '''
            dd.append(emp17_attdata[i][0])
            dd.append(emp18_attdata[i][0])
            dd.append(emp19_attdata[i][0])
            dd.append(emp20_attdata[i][0])
            dd.append(emp21_attdata[i][0])
            dd.append(emp22_attdata[i][0])
            dd.append(emp23_attdata[i][0])
            dd.append(emp24_attdata[i][0])
            dd.append(emp25_attdata[i][0])
            dd.append(emp26_attdata[i][0])
            dd.append(emp27_attdata[i][0])
            dd.append(emp28_attdata[i][0])
            dd.append(emp29_attdata[i][0])
            dd.append(emp30_attdata[i][0])
            dd.append(emp31_attdata[i][0])
            dd.append(emp1_attdata[i][0])
            dd.append(emp2_attdata[i][0])
            dd.append(emp3_attdata[i][0])
            dd.append(emp4_attdata[i][0])
            dd.append(emp5_attdata[i][0])
            dd.append(emp6_attdata[i][0])
            dd.append(emp7_attdata[i][0])
            dd.append(emp8_attdata[i][0])
            dd.append(emp9_attdata[i][0])
            dd.append(emp10_attdata[i][0])
            dd.append(emp11_attdata[i][0])
            dd.append(emp12_attdata[i][0])
            dd.append(emp13_attdata[i][0])
            dd.append(emp14_attdata[i][0])
            dd.append(emp15_attdata[i][0])
            '''
            findat.append(dd)
    connection.commit() 
    connection.close()
    cursor.close()
    for i in range(len(findat)):
        ws.append(findat[i])

    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)
    print('DDDD')

    return send_file(file_stream, attachment_filename="attexceldata_"+str(month)+".xlsx", as_attachment=True)

def attDataGenerator(attdate):
    # To generate attendance data based on the date
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    #sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '"+str(attdate)+"%'"
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '"+str(attdate)+"%'"
    ##print(sql_Query)
    cursor.execute(sql_Query)
    attdata = cursor.fetchall()
    ##print(attdata)
    connection.commit() 
    connection.close()
    cursor.close()
    return attdata
    

def getMonthName(month_num):
    # To get the month name based on month number
    datetime_object = datetime.strptime(month_num, "%m")
    month_name = datetime_object.strftime("%b")
    ##print("Short name: ",month_name)

    full_month_name = datetime_object.strftime("%B")
    ##print("Full name: ",full_month_name)
    return month_name

@app.route('/')
def index():
    return render_template('login1.html')
#--------------------------------------------------------------------------------------------
#Delete Appraisal routing
@app.route('/appraisaldelete')
def appraisaldelete():
    rid=request.args['id']
    empcode=request.args['empcode']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "delete from tblnewappraisal where id='"+rid+"'"
    cursor.execute(sql_Query)
    
    sql_Query = "select bsal,gsal,ctc,nsal from tblonboarding where Empcode='"+str(empcode)+"'"   
    cursor.execute(sql_Query)
    saldata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblnewappraisal where empcode='"+str(empcode)+"'"
    cursor.execute(sql_Query)
    appraisaldata = cursor.fetchall()

    
    connection.commit()
    connection.close()
    cursor.close()
    return render_template('addappraisal.html',appraisaldata=appraisaldata,saldata=saldata,empcode=empcode)

#Save new appraisal routing
@app.route('/saveappraisal')
def saveappraisal():
    empcode=request.args['empcode']
    cbs=request.args['cbs']
    cgs=request.args['cgs']
    cctc=request.args['cctc']
    cns=request.args['cns']
    mon=request.args['mon']
    year=request.args['year']
    comment=request.args['comment']
    effectivemonth=str(mon)+"-"+str(year)
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "insert into tblnewappraisal(empcode,calc_bsal,calc_gsal,calc_ctc,calc_nsal,effec_monyear,comment,stat,app_date) values("+empcode+","+cbs+","+cgs+","+cctc+","+cns+",'"+effectivemonth+"','"+comment+"','Pending','--')"
    print(sql_Query)
    cursor.execute(sql_Query)
    connection.commit()
    connection.close()
    cursor.close()
    #return render_template('rolecreation.html',rolesdata=rolesdata)
    resp = make_response(json.dumps("Success"))
    return resp

# Add Appraisal
@app.route('/addappraisal')
def addappraisal():
    empcode=request.args['empcode']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()

    sql_Query = "select bsal,gsal,ctc,nsal from tblonboarding where Empcode='"+str(empcode)+"'"   
    cursor.execute(sql_Query)
    saldata = cursor.fetchall()

    sql_Query = "SELECT * from tblnewappraisal where empcode='"+str(empcode)+"'"
    cursor.execute(sql_Query)
    appraisaldata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    return render_template('addappraisal.html',saldata=saldata,empcode=empcode,appraisaldata=appraisaldata)
#---------------------------------------------------------------------------------------------------------------------------------
#List Unapproved Appraisals
@app.route('/unapprovedappraisals')
def unapprovedappraisals():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()

    sql_Query = "SELECT * from tblnewappraisal where stat='Pending'"
    cursor.execute(sql_Query)
    appraisaldata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    return render_template('unapprovedappraisals.html',appraisaldata=appraisaldata)


#Approve Appraisal
@app.route('/approveappraisal')
def approveappraisal():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "update tblnewappraisal set stat='Approved' where id='"+rid+"'"
    cursor.execute(sql_Query)

    
    sql_Query = "SELECT * from tblnewappraisal where stat='Pending'"
    cursor.execute(sql_Query)
    appraisaldata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    return render_template('unapprovedappraisals.html',appraisaldata=appraisaldata)




#Reject Appraisal
@app.route('/rejectappraisal')
def rejectappraisal():
    rid=request.args['id']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor(buffered=True)
    sql_Query = "update tblnewappraisal set stat='Rejected' where id='"+rid+"'"
    cursor.execute(sql_Query)

    
    sql_Query = "SELECT * from tblnewappraisal where stat='Pending'"
    cursor.execute(sql_Query)
    appraisaldata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    return render_template('unapprovedappraisals.html',appraisaldata=appraisaldata)
#-----------------------------------------------------------------------------------------------------------------------------------

@app.route('/candidatelist')
def candidatelist():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()

    sql_Query = "SELECT * from tblcandidate_register where Statuss='Open'"
    cursor.execute(sql_Query)
    candidatedata = cursor.fetchall()
    
    connection.commit()
    connection.close()
    cursor.close()
    return render_template('candidatelist.html',candidatedata=candidatedata)

@app.route('/attdashboard')
def attdashboard():
    global rolename
    rolename=session['rolename']
    try:
        code=request.args['code']
        code=int(code)
    except:
        code=0
    #print(code)
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    #sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '"+str(attdate)+"%'"
    sql_Query = "SELECT count(*) from tblEmpTotalHoursSimp where (AType='DLOP' or AType='LOP' or AType='HD' or AType='LHD') and DateFor like '26-Oct-%'"
    ##print(sql_Query)
    cursor.execute(sql_Query)
    tile1data = cursor.fetchall()
    tile1data=tile1data[0][0]
    #print(tile1data)
    sql_Query = "SELECT distinct s.Empcode,h.EmpName,s.Atype from tblEmpTotalHoursSimp s, tblEmployeeTotalHours h where (AType='DLOP' or AType='LOP' or AType='HD' or AType='LHD') and s.DateFor like '26-Oct-%' and s.Empcode=h.Empcode"
    cursor.execute(sql_Query)
    code1data = cursor.fetchall()
    
    sql_Query = "SELECT count(*) from tblEmpTotalHoursSimp where (AType='P') and DateFor like '26-Oct-%'"
    ##print(sql_Query)
    cursor.execute(sql_Query)
    tile2data = cursor.fetchall()
    tile2data=tile2data[0][0]
    #print(tile2data)
    sql_Query = "SELECT distinct s.Empcode,h.EmpName,s.Atype from tblEmpTotalHoursSimp s, tblEmployeeTotalHours h where (AType='P') and s.DateFor like '26-Oct-%' and s.Empcode=h.Empcode"
    cursor.execute(sql_Query)
    code2data = cursor.fetchall()


    sql_Query = "SELECT count(*) from tblEmpTotalHoursSimp where (AType='CL' or AType='NH' or AType='WO') and DateFor like '26-Oct-%'"
    ##print(sql_Query)
    cursor.execute(sql_Query)
    tile3data = cursor.fetchall()
    tile3data=tile3data[0][0]
    #print(tile3data)
    sql_Query = "SELECT distinct s.Empcode,h.EmpName,s.Atype from tblEmpTotalHoursSimp s, tblEmployeeTotalHours h where (AType='CL' or AType='NH' or AType='WO') and s.DateFor like '26-Oct-%' and s.Empcode=h.Empcode"
    cursor.execute(sql_Query)
    code3data = cursor.fetchall()
    
    connection.commit() 
    connection.close()
    cursor.close()
    if code==0:
        return render_template('AttDashboard.html',tile1data=tile1data,tile2data=tile2data,tile3data=tile3data,rolename=rolename)
    if code==1:
        return render_template('AttDashboard.html',tile1data=tile1data,tile2data=tile2data,tile3data=tile3data,data=code1data,rolename=rolename)
    if code==2:
        return render_template('AttDashboard.html',tile1data=tile1data,tile2data=tile2data,tile3data=tile3data,data=code2data,rolename=rolename)
    if code==3:
        return render_template('AttDashboard.html',tile1data=tile1data,tile2data=tile2data,tile3data=tile3data,data=code3data,rolename=rolename)




@app.route('/logdata')
def index1():
    email=request.args['name']
    pswd=request.args['passwrd']
    
    global rolename
    global userrole
    global empcodelist
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "SELECT * from lkpmapuserrole where email='"+str(email)+"' and pswd='"+str(pswd)+"'"
    print(sql_Query)
    cursor.execute(sql_Query)
    emproledata = cursor.fetchall()
    print(len(emproledata))
    if len(emproledata)==0:
        userrole=0
        session['rolename']="Employee"

        datesfinallist=[]  
        connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
        cursor = connection.cursor()
        sql_Query = "SELECT distinct Cast(tblEmpMgrMap.Empcode as decimal) As ECode,EmpName,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmpMgrMap, tblEmpProcMap where tblEmpMgrMap.Empcode=tblEmpProcMap.Empcode and EmpName='"+str(emproledata[0][1])+"'  group by ECode order by ECode limit 20"
        print(sql_Query)
        cursor.execute(sql_Query)
        emp_primarydata = cursor.fetchall()
        ##print(emp_primarydata)
        #print('---------')
        ##print(emp_primarydata[0])
        #print('---------')
        ##print(emp_primarydata[0][1])
        mydate = datetime.now()
        todays_date = datetime.today()
        '''
        # Fetching Dates
        #print("Current year:", todays_date.year)
        #print("Current month:", todays_date.month)
        #print("Current day:", todays_date.day)
        '''

        
        empcodelist=[]    
        sql_Query = "SELECT distinct Empcode from tblEmpTotalHoursSimp where Empcode in (Select Empcode from tblEmpMgrMap where ManagerName='"+str(emproledata[0][1])+"')"
        print(sql_Query)
        cursor.execute(sql_Query)
        empcodedata = cursor.fetchall()
        for i in range(len(empcodedata)):
            val=i+1
            testlist=[]
            testlist.append(val)
            testlist.append(empcodedata[i][0])
            empcodelist.append(testlist)
        ##print(empcodes)
        #print(empcodelist)
        
        
        # Version 2 of attendance
        mydate = datetime.today()
        #print(mydate)

        n = 0
        mydate = mydate - pd.DateOffset(months=n)
        #print(mydate)

        
        startdate=""
        enddate=""
        monnum=0
        startmon=0
        endmon=0
        if mydate.day>=16:
            startdate=str(mydate.year)+"-"+str(mydate.month)+"-16"
            monnum=mydate.month+1
            nmonth=mydate.month+1
            startmon=mydate.month
            endmon=nmonth     
            enddate=str(mydate.year)+"-"+str(nmonth)+"-15"
        else:
            prevmonth=mydate.month-1
            monnum=prevmonth+1
            startmon=prevmonth
            endmon=mydate.month     
            startdate=str(mydate.year)+"-"+str(prevmonth)+"-16"    
            enddate=str(mydate.year)+"-"+str(mydate.month)+"-15"
        #print(startdate)
        #print(enddate)
        dateslist=pd.date_range(start=startdate,end=enddate)
        for i in range(len(dateslist)):
            dt=str(dateslist[i])[0:10]
            dtval=dt.split('-')
            dtval[1]=getMonthName(str(dtval[1]))
            dtval[0]=int(dtval[0])-2000
            findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
            
            datesfinallist.append(findate)
            ##print(findate)
        datescount=len(datesfinallist)
        '''
        attdata=[]
        ##print(datesfinallist)
        for i in range(len(datesfinallist)):
            ##print(attDataGenerator(datesfinallist[i]))
            attdata.append(attDataGenerator(datesfinallist[i]))
            
        
        
        connection.commit() 
        connection.close()
        cursor.close()
        ##print(attdata[10])
        return render_template('HRattendance1.html',emp_primarydata=emp_primarydata,attdata=attdata,datesfinallist=datesfinallist)
        

        
        '''
        #print(datesfinallist)
        # Version 1 of attendance
        print(datescount)
        print(len(datesfinallist))
        smonname= monthname(startmon)
        emonname=monthname(endmon)
        print("smon"+str(smonname))
        print("emon"+str(emonname))
        yr=int(todays_date.year)
        yr=yr-2000
        strval=str(todays_date.day)+"-"+mydate.strftime("%b")+"-"+str(yr)
        #print(strval)
        #Date 1-15 check
        #monwise="-"+mydate.strftime("%b")+"-"+str(yr)
        monwise="-"+str(smonname)+"-"+str(yr)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp16_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp17_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp18_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp19_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp20_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp21_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp22_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp23_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp24_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp25_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp26_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp27_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp28_attdata = cursor.fetchall()
        
        emp29_attdata=[]
        emp30_attdata=[]
        
        if datescount>28:
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp29_attdata = cursor.fetchall()
        
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp30_attdata = cursor.fetchall()
        
        emp31_attdata=[]
        if datescount==31:
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp31_attdata = cursor.fetchall()

        #print('==========')
        #Date 1-15 check
        #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
        #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
        monwise="-"+str(emonname)+"-"+str(yr)
        #print(monwise)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp1_attdata = cursor.fetchall()
        ##print(emp1_attdata)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp2_attdata = cursor.fetchall()
        ##print(emp2_attdata)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp3_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp4_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp5_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp6_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp7_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp8_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp9_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp10_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp11_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp12_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp13_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp14_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp15_attdata = cursor.fetchall()
        '''
        smonwise="-"+str(smonname)+"-"+str(yr)
        emonwise="-"+str(emonname)+"-"+str(yr)
        sql_Query = "SELECT y.Empcode,y.thours FROM (SELECT distinct Cast(Empcode as decimal) As Empcode ,sum(TotalHrs) as 'thours' from tblEmpTotalHoursSimp where (DateFor like '%16"+str(smonwise)+"%' or DateFor like '%17"+str(smonwise)+"%' or DateFor like '%18"+str(smonwise)+"%' or DateFor like '%19"+str(smonwise)+"%' or DateFor like '%20"+str(smonwise)+"%') group by EmpCode order by EmpCode)y where y.thours>=0"
        #print(sql_Query)
        cursor.execute(sql_Query)
        tothrs_attdata = cursor.fetchall()
        #print(tothrs_attdata)
        '''
       
        
        sql_Query = "SELECT * from `TABLE 18` where PMonth='"+str(monnum)+"' and Empcode in (Select Empcode from tblEmpMgrMap where ManagerName like '%"+str(emproledata[0][1])+"%') order by Empcode limit 20"
        print(sql_Query)
        cursor.execute(sql_Query)
        payrolldata = cursor.fetchall()
        #print(payrolldata)
      
        connection.commit() 
        connection.close()
        cursor.close()            
        ur=rolename
        '''
        if ur==2:
            ur="HR Head"
        if ur==1:
            ur="Admin"
        if ur==50:
            ur="HR Team"
        '''
        ##print(emp25_attdata)
        return render_template('HRattendance1.html',payrolldata=payrolldata,userrole=ur,datesfinallist=datesfinallist,emp_primarydata=emp_primarydata,emp16_attdata=emp16_attdata,emp17_attdata=emp17_attdata,emp18_attdata=emp18_attdata,emp19_attdata=emp19_attdata,emp20_attdata=emp20_attdata,emp21_attdata=emp21_attdata,emp22_attdata=emp22_attdata,emp23_attdata=emp23_attdata,emp24_attdata=emp24_attdata,emp25_attdata=emp25_attdata,emp26_attdata=emp26_attdata,emp27_attdata=emp27_attdata,emp28_attdata=emp28_attdata,emp29_attdata=emp29_attdata,emp30_attdata=emp30_attdata,emp31_attdata=emp31_attdata,emp1_attdata=emp1_attdata,emp2_attdata=emp2_attdata,emp3_attdata=emp3_attdata,emp4_attdata=emp4_attdata,emp5_attdata=emp5_attdata,emp6_attdata=emp6_attdata,emp7_attdata=emp7_attdata,emp8_attdata=emp8_attdata,emp9_attdata=emp9_attdata,emp10_attdata=emp10_attdata,emp11_attdata=emp11_attdata,emp12_attdata=emp12_attdata,emp13_attdata=emp13_attdata,emp14_attdata=emp14_attdata,emp15_attdata=emp15_attdata,datescount=datescount,monnum=monnum,rolename=rolename)
       
    if len(emproledata)>0:
        print("aaaa"+str(emproledata[0][3])+"aaa")
        session['name']=emproledata[0][1]
        if str(emproledata[0][3])=="Admin":
            userrole=1
            session['rolename']="Admin"
        elif str(emproledata[0][3])=="HR Manager":
            userrole=2
            session['rolename']="HR Manager"
        elif str(emproledata[0][3])=="HR Ops":
            userrole=50
            session['rolename']="HR Ops"
        elif str(emproledata[0][3])=="Operations Manager":
            userrole=10
            session['rolename']="Operations Manager"
        else:
            userrole=0
            session['rolename']="Employee"
        '''
        if uname.lower()=="anna" and pswd.lower()=="user@1234":
            userrole=2
        elif uname.lower()=="darshan" and pswd.lower()=="user@1234":
            userrole=1
        elif uname.lower()=="nandini" and pswd.lower()=="user@1234":
            userrole=50
        elif uname.lower()=="12900" and pswd.lower()=="user@1234":
            return render_template('weblogin1.html')
        '''
        rolename=session['rolename']
        print(userrole)
        print(rolename)
        if rolename=="Admin" or rolename=="HR Manager" or rolename=="HR Ops":
            datesfinallist=[]  
            connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
            cursor = connection.cursor()
            sql_Query = "SELECT distinct Cast(tblEmpMgrMap.Empcode as decimal) As ECode,EmpName,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmpMgrMap, tblEmpProcMap where tblEmpMgrMap.Empcode=tblEmpProcMap.Empcode  group by ECode order by ECode limit 20"
            ##print(sql_Query)
            cursor.execute(sql_Query)
            emp_primarydata = cursor.fetchall()
            ##print(emp_primarydata)
            #print('---------')
            ##print(emp_primarydata[0])
            #print('---------')
            ##print(emp_primarydata[0][1])
            mydate = datetime.now()
            todays_date = datetime.today()
            '''
            # Fetching Dates
            #print("Current year:", todays_date.year)
            #print("Current month:", todays_date.month)
            #print("Current day:", todays_date.day)
            '''

            
            empcodelist=[]    
            sql_Query = "SELECT distinct Empcode from tblEmpTotalHoursSimp"
            cursor.execute(sql_Query)
            empcodedata = cursor.fetchall()
            for i in range(len(empcodedata)):
                val=i+1
                testlist=[]
                testlist.append(val)
                testlist.append(empcodedata[i][0])
                empcodelist.append(testlist)
            ##print(empcodes)
            #print(empcodelist)
            
            
            # Version 2 of attendance
            mydate = datetime.today()
            #print(mydate)

            n = 0
            mydate = mydate - pd.DateOffset(months=n)
            #print(mydate)

            
            startdate=""
            enddate=""
            monnum=0
            startmon=0
            endmon=0
            if mydate.day>=16:
                startdate=str(mydate.year)+"-"+str(mydate.month)+"-16"
                monnum=mydate.month+1
                nmonth=mydate.month+1
                startmon=mydate.month
                endmon=nmonth     
                enddate=str(mydate.year)+"-"+str(nmonth)+"-15"
            else:
                prevmonth=mydate.month-1
                monnum=prevmonth+1
                startmon=prevmonth
                endmon=mydate.month     
                startdate=str(mydate.year)+"-"+str(prevmonth)+"-16"    
                enddate=str(mydate.year)+"-"+str(mydate.month)+"-15"
            #print(startdate)
            #print(enddate)
            dateslist=pd.date_range(start=startdate,end=enddate)
            for i in range(len(dateslist)):
                dt=str(dateslist[i])[0:10]
                dtval=dt.split('-')
                dtval[1]=getMonthName(str(dtval[1]))
                dtval[0]=int(dtval[0])-2000
                findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
                
                datesfinallist.append(findate)
                ##print(findate)
            datescount=len(datesfinallist)
            '''
            attdata=[]
            ##print(datesfinallist)
            for i in range(len(datesfinallist)):
                ##print(attDataGenerator(datesfinallist[i]))
                attdata.append(attDataGenerator(datesfinallist[i]))
                
            
            
            connection.commit() 
            connection.close()
            cursor.close()
            ##print(attdata[10])
            return render_template('HRattendance1.html',emp_primarydata=emp_primarydata,attdata=attdata,datesfinallist=datesfinallist)
            

            
            '''
            #print(datesfinallist)
            # Version 1 of attendance
            print(datescount)
            print(len(datesfinallist))
            smonname= monthname(startmon)
            emonname=monthname(endmon)
            print("smon"+str(smonname))
            print("emon"+str(emonname))
            yr=int(todays_date.year)
            yr=yr-2000
            strval=str(todays_date.day)+"-"+mydate.strftime("%b")+"-"+str(yr)
            #print(strval)
            #Date 1-15 check
            #monwise="-"+mydate.strftime("%b")+"-"+str(yr)
            monwise="-"+str(smonname)+"-"+str(yr)
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp16_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp17_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp18_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp19_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp20_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp21_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp22_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp23_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp24_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp25_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp26_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp27_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp28_attdata = cursor.fetchall()
            
            emp29_attdata=[]
            emp30_attdata=[]
            
            if datescount>28:
                sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%'"
                #print(sql_Query)
                cursor.execute(sql_Query)
                emp29_attdata = cursor.fetchall()
            
                sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%'"
                #print(sql_Query)
                cursor.execute(sql_Query)
                emp30_attdata = cursor.fetchall()
            
            emp31_attdata=[]
            if datescount==31:
                sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%'"
                #print(sql_Query)
                cursor.execute(sql_Query)
                emp31_attdata = cursor.fetchall()

            #print('==========')
            #Date 1-15 check
            #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
            #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
            monwise="-"+str(emonname)+"-"+str(yr)
            #print(monwise)
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp1_attdata = cursor.fetchall()
            ##print(emp1_attdata)
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp2_attdata = cursor.fetchall()
            ##print(emp2_attdata)
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp3_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp4_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp5_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp6_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp7_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp8_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp9_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp10_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp11_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp12_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp13_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp14_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp15_attdata = cursor.fetchall()
            '''
            smonwise="-"+str(smonname)+"-"+str(yr)
            emonwise="-"+str(emonname)+"-"+str(yr)
            sql_Query = "SELECT y.Empcode,y.thours FROM (SELECT distinct Cast(Empcode as decimal) As Empcode ,sum(TotalHrs) as 'thours' from tblEmpTotalHoursSimp where (DateFor like '%16"+str(smonwise)+"%' or DateFor like '%17"+str(smonwise)+"%' or DateFor like '%18"+str(smonwise)+"%' or DateFor like '%19"+str(smonwise)+"%' or DateFor like '%20"+str(smonwise)+"%') group by EmpCode order by EmpCode)y where y.thours>=0"
            #print(sql_Query)
            cursor.execute(sql_Query)
            tothrs_attdata = cursor.fetchall()
            #print(tothrs_attdata)
            '''
           
            
            sql_Query = "SELECT * from `TABLE 18` where PMonth='"+str(monnum)+"' order by Empcode limit 20"
            #print(sql_Query)
            cursor.execute(sql_Query)
            payrolldata = cursor.fetchall()
            #print(payrolldata)
          
            connection.commit() 
            connection.close()
            cursor.close()
            #return render_template('dataloader.html',fire=data[0][1],airquality=data[0][2],methane=data[0][3])
            
            ur=rolename
            '''
            if ur==2:
                ur="HR Head"
            if ur==1:
                ur="Admin"
            if ur==50:
                ur="HR Team"
            '''
            ##print(emp25_attdata)
            return render_template('HRattendance1.html',payrolldata=payrolldata,userrole=ur,datesfinallist=datesfinallist,emp_primarydata=emp_primarydata,emp16_attdata=emp16_attdata,emp17_attdata=emp17_attdata,emp18_attdata=emp18_attdata,emp19_attdata=emp19_attdata,emp20_attdata=emp20_attdata,emp21_attdata=emp21_attdata,emp22_attdata=emp22_attdata,emp23_attdata=emp23_attdata,emp24_attdata=emp24_attdata,emp25_attdata=emp25_attdata,emp26_attdata=emp26_attdata,emp27_attdata=emp27_attdata,emp28_attdata=emp28_attdata,emp29_attdata=emp29_attdata,emp30_attdata=emp30_attdata,emp31_attdata=emp31_attdata,emp1_attdata=emp1_attdata,emp2_attdata=emp2_attdata,emp3_attdata=emp3_attdata,emp4_attdata=emp4_attdata,emp5_attdata=emp5_attdata,emp6_attdata=emp6_attdata,emp7_attdata=emp7_attdata,emp8_attdata=emp8_attdata,emp9_attdata=emp9_attdata,emp10_attdata=emp10_attdata,emp11_attdata=emp11_attdata,emp12_attdata=emp12_attdata,emp13_attdata=emp13_attdata,emp14_attdata=emp14_attdata,emp15_attdata=emp15_attdata,datescount=datescount,monnum=monnum,rolename=rolename)

        if rolename=="Employee":
            datesfinallist=[]  
            connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
            cursor = connection.cursor()
            sql_Query = "SELECT distinct Cast(tblEmpMgrMap.Empcode as decimal) As ECode,EmpName,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmpMgrMap, tblEmpProcMap where tblEmpMgrMap.Empcode=tblEmpProcMap.Empcode and EmpName='"+str(emproledata[0][1])+"'  group by ECode order by ECode limit 20"
            ##print(sql_Query)
            cursor.execute(sql_Query)
            emp_primarydata = cursor.fetchall()
            ##print(emp_primarydata)
            #print('---------')
            ##print(emp_primarydata[0])
            #print('---------')
            ##print(emp_primarydata[0][1])
            mydate = datetime.now()
            todays_date = datetime.today()
            '''
            # Fetching Dates
            #print("Current year:", todays_date.year)
            #print("Current month:", todays_date.month)
            #print("Current day:", todays_date.day)
            '''

            
            empcodelist=[]    
            sql_Query = "SELECT distinct Empcode from tblEmpTotalHoursSimp where Empcode in (Select Empcode from tblEmpMgrMap where EmpName='"+str(emproledata[0][1])+"')"
            cursor.execute(sql_Query)
            empcodedata = cursor.fetchall()
            for i in range(len(empcodedata)):
                val=i+1
                testlist=[]
                testlist.append(val)
                testlist.append(empcodedata[i][0])
                empcodelist.append(testlist)
            ##print(empcodes)
            #print(empcodelist)
            
            
            # Version 2 of attendance
            mydate = datetime.today()
            #print(mydate)

            n = 0
            mydate = mydate - pd.DateOffset(months=n)
            #print(mydate)

            
            startdate=""
            enddate=""
            monnum=0
            startmon=0
            endmon=0
            if mydate.day>=16:
                startdate=str(mydate.year)+"-"+str(mydate.month)+"-16"
                monnum=mydate.month+1
                nmonth=mydate.month+1
                startmon=mydate.month
                endmon=nmonth     
                enddate=str(mydate.year)+"-"+str(nmonth)+"-15"
            else:
                prevmonth=mydate.month-1
                monnum=prevmonth+1
                startmon=prevmonth
                endmon=mydate.month     
                startdate=str(mydate.year)+"-"+str(prevmonth)+"-16"    
                enddate=str(mydate.year)+"-"+str(mydate.month)+"-15"
            #print(startdate)
            #print(enddate)
            dateslist=pd.date_range(start=startdate,end=enddate)
            for i in range(len(dateslist)):
                dt=str(dateslist[i])[0:10]
                dtval=dt.split('-')
                dtval[1]=getMonthName(str(dtval[1]))
                dtval[0]=int(dtval[0])-2000
                findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
                
                datesfinallist.append(findate)
                ##print(findate)
            datescount=len(datesfinallist)
            '''
            attdata=[]
            ##print(datesfinallist)
            for i in range(len(datesfinallist)):
                ##print(attDataGenerator(datesfinallist[i]))
                attdata.append(attDataGenerator(datesfinallist[i]))
                
            
            
            connection.commit() 
            connection.close()
            cursor.close()
            ##print(attdata[10])
            return render_template('HRattendance1.html',emp_primarydata=emp_primarydata,attdata=attdata,datesfinallist=datesfinallist)
            

            
            '''
            #print(datesfinallist)
            # Version 1 of attendance
            print(datescount)
            print(len(datesfinallist))
            smonname= monthname(startmon)
            emonname=monthname(endmon)
            print("smon"+str(smonname))
            print("emon"+str(emonname))
            yr=int(todays_date.year)
            yr=yr-2000
            strval=str(todays_date.day)+"-"+mydate.strftime("%b")+"-"+str(yr)
            #print(strval)
            #Date 1-15 check
            #monwise="-"+mydate.strftime("%b")+"-"+str(yr)
            monwise="-"+str(smonname)+"-"+str(yr)
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp16_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp17_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp18_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp19_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp20_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp21_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp22_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp23_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp24_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp25_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp26_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp27_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp28_attdata = cursor.fetchall()
            
            emp29_attdata=[]
            emp30_attdata=[]
            
            if datescount>28:
                sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%'"
                #print(sql_Query)
                cursor.execute(sql_Query)
                emp29_attdata = cursor.fetchall()
            
                sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%'"
                #print(sql_Query)
                cursor.execute(sql_Query)
                emp30_attdata = cursor.fetchall()
            
            emp31_attdata=[]
            if datescount==31:
                sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%'"
                #print(sql_Query)
                cursor.execute(sql_Query)
                emp31_attdata = cursor.fetchall()

            #print('==========')
            #Date 1-15 check
            #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
            #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
            monwise="-"+str(emonname)+"-"+str(yr)
            #print(monwise)
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp1_attdata = cursor.fetchall()
            ##print(emp1_attdata)
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp2_attdata = cursor.fetchall()
            ##print(emp2_attdata)
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp3_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp4_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp5_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp6_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp7_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp8_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp9_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp10_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp11_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp12_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp13_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp14_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp15_attdata = cursor.fetchall()
            '''
            smonwise="-"+str(smonname)+"-"+str(yr)
            emonwise="-"+str(emonname)+"-"+str(yr)
            sql_Query = "SELECT y.Empcode,y.thours FROM (SELECT distinct Cast(Empcode as decimal) As Empcode ,sum(TotalHrs) as 'thours' from tblEmpTotalHoursSimp where (DateFor like '%16"+str(smonwise)+"%' or DateFor like '%17"+str(smonwise)+"%' or DateFor like '%18"+str(smonwise)+"%' or DateFor like '%19"+str(smonwise)+"%' or DateFor like '%20"+str(smonwise)+"%') group by EmpCode order by EmpCode)y where y.thours>=0"
            #print(sql_Query)
            cursor.execute(sql_Query)
            tothrs_attdata = cursor.fetchall()
            #print(tothrs_attdata)
            '''
           
            
            sql_Query = "SELECT * from `TABLE 18` where PMonth='"+str(monnum)+"' and Empcode in (Select Empcode from tblEmpMgrMap where EmpName like '%"+str(emproledata[0][1])+"%') order by Empcode"
            print(sql_Query)
            cursor.execute(sql_Query)
            payrolldata = cursor.fetchall()
            #print(payrolldata)
          
            connection.commit() 
            connection.close()
            cursor.close()            
            ur=rolename
            '''
            if ur==2:
                ur="HR Head"
            if ur==1:
                ur="Admin"
            if ur==50:
                ur="HR Team"
            '''
            ##print(emp25_attdata)
            return render_template('HRattendance1.html',payrolldata=payrolldata,userrole=ur,datesfinallist=datesfinallist,emp_primarydata=emp_primarydata,emp16_attdata=emp16_attdata,emp17_attdata=emp17_attdata,emp18_attdata=emp18_attdata,emp19_attdata=emp19_attdata,emp20_attdata=emp20_attdata,emp21_attdata=emp21_attdata,emp22_attdata=emp22_attdata,emp23_attdata=emp23_attdata,emp24_attdata=emp24_attdata,emp25_attdata=emp25_attdata,emp26_attdata=emp26_attdata,emp27_attdata=emp27_attdata,emp28_attdata=emp28_attdata,emp29_attdata=emp29_attdata,emp30_attdata=emp30_attdata,emp31_attdata=emp31_attdata,emp1_attdata=emp1_attdata,emp2_attdata=emp2_attdata,emp3_attdata=emp3_attdata,emp4_attdata=emp4_attdata,emp5_attdata=emp5_attdata,emp6_attdata=emp6_attdata,emp7_attdata=emp7_attdata,emp8_attdata=emp8_attdata,emp9_attdata=emp9_attdata,emp10_attdata=emp10_attdata,emp11_attdata=emp11_attdata,emp12_attdata=emp12_attdata,emp13_attdata=emp13_attdata,emp14_attdata=emp14_attdata,emp15_attdata=emp15_attdata,datescount=datescount,monnum=monnum,rolename=rolename)
           
        if rolename=="Operations Manager":
            datesfinallist=[]  
            connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
            cursor = connection.cursor()
            sql_Query = "SELECT distinct Cast(tblEmpMgrMap.Empcode as decimal) As ECode,EmpName,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmpMgrMap, tblEmpProcMap where tblEmpMgrMap.Empcode=tblEmpProcMap.Empcode and ManagerName='"+str(emproledata[0][1])+"'  group by ECode order by ECode limit 20"
            print(sql_Query)
            cursor.execute(sql_Query)
            emp_primarydata = cursor.fetchall()
            ##print(emp_primarydata)
            #print('---------')
            ##print(emp_primarydata[0])
            #print('---------')
            ##print(emp_primarydata[0][1])
            mydate = datetime.now()
            todays_date = datetime.today()
            '''
            # Fetching Dates
            #print("Current year:", todays_date.year)
            #print("Current month:", todays_date.month)
            #print("Current day:", todays_date.day)
            '''

            
            empcodelist=[]    
            sql_Query = "SELECT distinct Empcode from tblEmpTotalHoursSimp where Empcode in (Select Empcode from tblEmpMgrMap where ManagerName='"+str(emproledata[0][1])+"')"
            print(sql_Query)
            cursor.execute(sql_Query)
            empcodedata = cursor.fetchall()
            for i in range(len(empcodedata)):
                val=i+1
                testlist=[]
                testlist.append(val)
                testlist.append(empcodedata[i][0])
                empcodelist.append(testlist)
            ##print(empcodes)
            #print(empcodelist)
            
            
            # Version 2 of attendance
            mydate = datetime.today()
            #print(mydate)

            n = 0
            mydate = mydate - pd.DateOffset(months=n)
            #print(mydate)

            
            startdate=""
            enddate=""
            monnum=0
            startmon=0
            endmon=0
            if mydate.day>=16:
                startdate=str(mydate.year)+"-"+str(mydate.month)+"-16"
                monnum=mydate.month+1
                nmonth=mydate.month+1
                startmon=mydate.month
                endmon=nmonth     
                enddate=str(mydate.year)+"-"+str(nmonth)+"-15"
            else:
                prevmonth=mydate.month-1
                monnum=prevmonth+1
                startmon=prevmonth
                endmon=mydate.month     
                startdate=str(mydate.year)+"-"+str(prevmonth)+"-16"    
                enddate=str(mydate.year)+"-"+str(mydate.month)+"-15"
            #print(startdate)
            #print(enddate)
            dateslist=pd.date_range(start=startdate,end=enddate)
            for i in range(len(dateslist)):
                dt=str(dateslist[i])[0:10]
                dtval=dt.split('-')
                dtval[1]=getMonthName(str(dtval[1]))
                dtval[0]=int(dtval[0])-2000
                findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
                
                datesfinallist.append(findate)
                ##print(findate)
            datescount=len(datesfinallist)
            '''
            attdata=[]
            ##print(datesfinallist)
            for i in range(len(datesfinallist)):
                ##print(attDataGenerator(datesfinallist[i]))
                attdata.append(attDataGenerator(datesfinallist[i]))
                
            
            
            connection.commit() 
            connection.close()
            cursor.close()
            ##print(attdata[10])
            return render_template('HRattendance1.html',emp_primarydata=emp_primarydata,attdata=attdata,datesfinallist=datesfinallist)
            

            
            '''
            #print(datesfinallist)
            # Version 1 of attendance
            print(datescount)
            print(len(datesfinallist))
            smonname= monthname(startmon)
            emonname=monthname(endmon)
            print("smon"+str(smonname))
            print("emon"+str(emonname))
            yr=int(todays_date.year)
            yr=yr-2000
            strval=str(todays_date.day)+"-"+mydate.strftime("%b")+"-"+str(yr)
            #print(strval)
            #Date 1-15 check
            #monwise="-"+mydate.strftime("%b")+"-"+str(yr)
            monwise="-"+str(smonname)+"-"+str(yr)
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp16_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp17_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp18_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp19_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp20_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp21_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp22_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp23_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp24_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp25_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp26_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp27_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp28_attdata = cursor.fetchall()
            
            emp29_attdata=[]
            emp30_attdata=[]
            
            if datescount>28:
                sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%'"
                #print(sql_Query)
                cursor.execute(sql_Query)
                emp29_attdata = cursor.fetchall()
            
                sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%'"
                #print(sql_Query)
                cursor.execute(sql_Query)
                emp30_attdata = cursor.fetchall()
            
            emp31_attdata=[]
            if datescount==31:
                sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%'"
                #print(sql_Query)
                cursor.execute(sql_Query)
                emp31_attdata = cursor.fetchall()

            #print('==========')
            #Date 1-15 check
            #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
            #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
            monwise="-"+str(emonname)+"-"+str(yr)
            #print(monwise)
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp1_attdata = cursor.fetchall()
            ##print(emp1_attdata)
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp2_attdata = cursor.fetchall()
            ##print(emp2_attdata)
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp3_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp4_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp5_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp6_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp7_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp8_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp9_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp10_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp11_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp12_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp13_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp14_attdata = cursor.fetchall()
            
            sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%'"
            #print(sql_Query)
            cursor.execute(sql_Query)
            emp15_attdata = cursor.fetchall()
            '''
            smonwise="-"+str(smonname)+"-"+str(yr)
            emonwise="-"+str(emonname)+"-"+str(yr)
            sql_Query = "SELECT y.Empcode,y.thours FROM (SELECT distinct Cast(Empcode as decimal) As Empcode ,sum(TotalHrs) as 'thours' from tblEmpTotalHoursSimp where (DateFor like '%16"+str(smonwise)+"%' or DateFor like '%17"+str(smonwise)+"%' or DateFor like '%18"+str(smonwise)+"%' or DateFor like '%19"+str(smonwise)+"%' or DateFor like '%20"+str(smonwise)+"%') group by EmpCode order by EmpCode)y where y.thours>=0"
            #print(sql_Query)
            cursor.execute(sql_Query)
            tothrs_attdata = cursor.fetchall()
            #print(tothrs_attdata)
            '''
           
            
            sql_Query = "SELECT * from `TABLE 18` where PMonth='"+str(monnum)+"' and Empcode in (Select Empcode from tblEmpMgrMap where ManagerName like '%"+str(emproledata[0][1])+"%') order by Empcode limit 20"
            print(sql_Query)
            cursor.execute(sql_Query)
            payrolldata = cursor.fetchall()
            #print(payrolldata)
          
            connection.commit() 
            connection.close()
            cursor.close()            
            ur=rolename
            '''
            if ur==2:
                ur="HR Head"
            if ur==1:
                ur="Admin"
            if ur==50:
                ur="HR Team"
            '''
            ##print(emp25_attdata)
            return render_template('HRattendance1.html',payrolldata=payrolldata,userrole=ur,datesfinallist=datesfinallist,emp_primarydata=emp_primarydata,emp16_attdata=emp16_attdata,emp17_attdata=emp17_attdata,emp18_attdata=emp18_attdata,emp19_attdata=emp19_attdata,emp20_attdata=emp20_attdata,emp21_attdata=emp21_attdata,emp22_attdata=emp22_attdata,emp23_attdata=emp23_attdata,emp24_attdata=emp24_attdata,emp25_attdata=emp25_attdata,emp26_attdata=emp26_attdata,emp27_attdata=emp27_attdata,emp28_attdata=emp28_attdata,emp29_attdata=emp29_attdata,emp30_attdata=emp30_attdata,emp31_attdata=emp31_attdata,emp1_attdata=emp1_attdata,emp2_attdata=emp2_attdata,emp3_attdata=emp3_attdata,emp4_attdata=emp4_attdata,emp5_attdata=emp5_attdata,emp6_attdata=emp6_attdata,emp7_attdata=emp7_attdata,emp8_attdata=emp8_attdata,emp9_attdata=emp9_attdata,emp10_attdata=emp10_attdata,emp11_attdata=emp11_attdata,emp12_attdata=emp12_attdata,emp13_attdata=emp13_attdata,emp14_attdata=emp14_attdata,emp15_attdata=emp15_attdata,datescount=datescount,monnum=monnum,rolename=rolename)
           
    else:
        print('gggg')
        return render_template('login1.html',data="Failure")





#HR Attendance View - Main
@app.route('/hrattendance')
def hrattendance():
    print(str(session['name']))
    global rolename
    rolename=session['rolename']
    #Global Variables
    datesfinallist=[]  
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "SELECT distinct Cast(tblEmpMgrMap.Empcode as decimal) As ECode,EmpName,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmpMgrMap, tblEmpProcMap where tblEmpMgrMap.Empcode=tblEmpProcMap.Empcode  group by ECode order by ECode limit 20"
    ##print(sql_Query)
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()
    ##print(emp_primarydata)
    #print('---------')
    ##print(emp_primarydata[0])
    #print('---------')
    ##print(emp_primarydata[0][1])
    mydate = datetime.now()
    todays_date = datetime.today()
    '''
    # Fetching Dates
    #print("Current year:", todays_date.year)
    #print("Current month:", todays_date.month)
    #print("Current day:", todays_date.day)
    '''

    global empcodelist
    empcodelist=[]    
    sql_Query = "SELECT distinct Empcode from tblEmpTotalHoursSimp"
    cursor.execute(sql_Query)
    empcodedata = cursor.fetchall()
    for i in range(len(empcodedata)):
        val=i+1
        testlist=[]
        testlist.append(val)
        testlist.append(empcodedata[i][0])
        empcodelist.append(testlist)
    ##print(empcodes)
    #print(empcodelist)
    
    
    # Version 2 of attendance
    mydate = datetime.today()
    #print(mydate)

    n = 0
    mydate = mydate - pd.DateOffset(months=n)
    #print(mydate)

    
    startdate=""
    enddate=""
    monnum=0
    startmon=0
    endmon=0
    if mydate.day>=16:
        startdate=str(mydate.year)+"-"+str(mydate.month)+"-16"
        monnum=mydate.month+1
        nmonth=mydate.month+1
        startmon=mydate.month
        endmon=nmonth     
        enddate=str(mydate.year)+"-"+str(nmonth)+"-15"
    else:
        prevmonth=mydate.month-1
        monnum=prevmonth+1
        startmon=prevmonth
        endmon=mydate.month     
        startdate=str(mydate.year)+"-"+str(prevmonth)+"-16"    
        enddate=str(mydate.year)+"-"+str(mydate.month)+"-15"
    #print(startdate)
    #print(enddate)
    dateslist=pd.date_range(start=startdate,end=enddate)
    for i in range(len(dateslist)):
        dt=str(dateslist[i])[0:10]
        dtval=dt.split('-')
        dtval[1]=getMonthName(str(dtval[1]))
        dtval[0]=int(dtval[0])-2000
        findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
        
        datesfinallist.append(findate)
        ##print(findate)
    datescount=len(datesfinallist)
    '''
    attdata=[]
    ##print(datesfinallist)
    for i in range(len(datesfinallist)):
        ##print(attDataGenerator(datesfinallist[i]))
        attdata.append(attDataGenerator(datesfinallist[i]))
        
    
    
    connection.commit() 
    connection.close()
    cursor.close()
    ##print(attdata[10])
    return render_template('HRattendance1.html',emp_primarydata=emp_primarydata,attdata=attdata,datesfinallist=datesfinallist)
    

    
    '''
    #print(datesfinallist)
    # Version 1 of attendance
    print(datescount)
    print(len(datesfinallist))
    smonname= monthname(startmon)
    emonname=monthname(endmon)
    print("smon"+str(smonname))
    print("emon"+str(emonname))
    yr=int(todays_date.year)
    yr=yr-2000
    strval=str(todays_date.day)+"-"+mydate.strftime("%b")+"-"+str(yr)
    #print(strval)
    #Date 1-15 check
    #monwise="-"+mydate.strftime("%b")+"-"+str(yr)
    monwise="-"+str(smonname)+"-"+str(yr)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp16_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp17_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp18_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp19_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp20_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp21_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp22_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp23_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp24_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp25_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp26_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp27_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp28_attdata = cursor.fetchall()
    
    emp29_attdata=[]
    emp30_attdata=[]
    
    if datescount>28:
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp29_attdata = cursor.fetchall()
    
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp30_attdata = cursor.fetchall()
    
    emp31_attdata=[]
    if datescount==31:
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp31_attdata = cursor.fetchall()

    #print('==========')
    #Date 1-15 check
    #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
    #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
    monwise="-"+str(emonname)+"-"+str(yr)
    #print(monwise)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp1_attdata = cursor.fetchall()
    ##print(emp1_attdata)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp2_attdata = cursor.fetchall()
    ##print(emp2_attdata)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp3_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp4_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp5_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp6_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp7_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp8_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp9_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp10_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp11_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp12_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp13_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp14_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp15_attdata = cursor.fetchall()
    '''
    smonwise="-"+str(smonname)+"-"+str(yr)
    emonwise="-"+str(emonname)+"-"+str(yr)
    sql_Query = "SELECT y.Empcode,y.thours FROM (SELECT distinct Cast(Empcode as decimal) As Empcode ,sum(TotalHrs) as 'thours' from tblEmpTotalHoursSimp where (DateFor like '%16"+str(smonwise)+"%' or DateFor like '%17"+str(smonwise)+"%' or DateFor like '%18"+str(smonwise)+"%' or DateFor like '%19"+str(smonwise)+"%' or DateFor like '%20"+str(smonwise)+"%') group by EmpCode order by EmpCode)y where y.thours>=0"
    #print(sql_Query)
    cursor.execute(sql_Query)
    tothrs_attdata = cursor.fetchall()
    #print(tothrs_attdata)
    '''
    
    sql_Query = "SELECT * from `TABLE 18` where PMonth='"+str(monnum)+"' order by Empcode limit 20"
    #print(sql_Query)
    cursor.execute(sql_Query)
    payrolldata = cursor.fetchall()
    #print(payrolldata)
  
    connection.commit() 
    connection.close()
    cursor.close()
    #return render_template('dataloader.html',fire=data[0][1],airquality=data[0][2],methane=data[0][3])
    global userrole
    ur=userrole
    if ur==2:
        ur="HR Head"
    if ur==1:
        ur="Admin"
    if ur==50:
        ur="HR Team"
    ##print(emp25_attdata)
    return render_template('HRattendance1.html',payrolldata=payrolldata,userrole=ur,datesfinallist=datesfinallist,emp_primarydata=emp_primarydata,emp16_attdata=emp16_attdata,emp17_attdata=emp17_attdata,emp18_attdata=emp18_attdata,emp19_attdata=emp19_attdata,emp20_attdata=emp20_attdata,emp21_attdata=emp21_attdata,emp22_attdata=emp22_attdata,emp23_attdata=emp23_attdata,emp24_attdata=emp24_attdata,emp25_attdata=emp25_attdata,emp26_attdata=emp26_attdata,emp27_attdata=emp27_attdata,emp28_attdata=emp28_attdata,emp29_attdata=emp29_attdata,emp30_attdata=emp30_attdata,emp31_attdata=emp31_attdata,emp1_attdata=emp1_attdata,emp2_attdata=emp2_attdata,emp3_attdata=emp3_attdata,emp4_attdata=emp4_attdata,emp5_attdata=emp5_attdata,emp6_attdata=emp6_attdata,emp7_attdata=emp7_attdata,emp8_attdata=emp8_attdata,emp9_attdata=emp9_attdata,emp10_attdata=emp10_attdata,emp11_attdata=emp11_attdata,emp12_attdata=emp12_attdata,emp13_attdata=emp13_attdata,emp14_attdata=emp14_attdata,emp15_attdata=emp15_attdata,datescount=datescount,monnum=monnum,rolename=rolename)
   



#HR Attendance View - Month filter
@app.route('/hrattendance1')
def hrattendance1():
    global empcodelist  
    global userrole  
    month=request.args['month']    
    year=request.args['year']
    
    
    #Global Variables
    datesfinallist=[]  
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "SELECT distinct Cast(tblEmpMgrMap.Empcode as decimal) As ECode,EmpName,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmpMgrMap, tblEmpProcMap where tblEmpMgrMap.Empcode=tblEmpProcMap.Empcode  group by ECode order by ECode limit 20"
    ##print(sql_Query)
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()
    ##print(emp_primarydata)
    #print('---------')
    ##print(emp_primarydata[0])
    #print('---------')
    ##print(emp_primarydata[0][1])
    mydate = datetime.now()
    todays_date = datetime.today()
    '''
    # Fetching Dates
    #print("Current year:", todays_date.year)
    #print("Current month:", todays_date.month)
    #print("Current day:", todays_date.day)
    '''

    empcodelist=[]    
    sql_Query = "SELECT distinct Empcode from tblEmpTotalHoursSimp"
    cursor.execute(sql_Query)
    empcodedata = cursor.fetchall()
    for i in range(len(empcodedata)):
        val=i+1
        testlist=[]
        testlist.append(val)
        testlist.append(empcodedata[i][0])
        empcodelist.append(testlist)
    ##print(empcodes)
    #print(empcodelist)
    
    
    # Version 2 of attendance
    mydate = datetime.today()
    #print(mydate)

    n = 0
    mydate = mydate - pd.DateOffset(months=n)
    #print(mydate)

    
    startdate=""
    enddate=""
    monnum=int(month)
    startmon=0
    endmon=0
    startmon=int(month)-1
    endmon=int(month)     
    startdate=str(mydate.year)+"-"+str(startmon)+"-16"    
    enddate=str(mydate.year)+"-"+str(endmon)+"-15"
    #print(startdate)
    #print(enddate)
    dateslist=pd.date_range(start=startdate,end=enddate)
    for i in range(len(dateslist)):
        dt=str(dateslist[i])[0:10]
        dtval=dt.split('-')
        dtval[1]=getMonthName(str(dtval[1]))
        dtval[0]=int(dtval[0])-2000
        findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
        
        datesfinallist.append(findate)
        ##print(findate)
    datescount=len(datesfinallist)
    '''
    attdata=[]
    ##print(datesfinallist)
    for i in range(len(datesfinallist)):
        ##print(attDataGenerator(datesfinallist[i]))
        attdata.append(attDataGenerator(datesfinallist[i]))
        
    
    
    connection.commit() 
    connection.close()
    cursor.close()
    ##print(attdata[10])
    return render_template('HRattendance1.html',emp_primarydata=emp_primarydata,attdata=attdata,datesfinallist=datesfinallist)
    

    
    '''
    #print(datesfinallist)
    # Version 1 of attendance
    print(datescount)
    print(len(datesfinallist))
    smonname= monthname(startmon)
    emonname=monthname(endmon)
    print("smon"+str(smonname))
    print("emon"+str(emonname))
    yr=int(todays_date.year)
    yr=yr-2000
    strval=str(todays_date.day)+"-"+mydate.strftime("%b")+"-"+str(yr)
    #print(strval)
    #Date 1-15 check
    #monwise="-"+mydate.strftime("%b")+"-"+str(yr)
    monwise="-"+str(smonname)+"-"+str(yr)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp16_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp17_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp18_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp19_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp20_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp21_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp22_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp23_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp24_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp25_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp26_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp27_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp28_attdata = cursor.fetchall()
    
    emp29_attdata=[]
    emp30_attdata=[]
    
    if datescount>28:
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp29_attdata = cursor.fetchall()
    
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp30_attdata = cursor.fetchall()
    
    emp31_attdata=[]
    if datescount==31:
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp31_attdata = cursor.fetchall()

    #print('==========')
    #Date 1-15 check
    #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
    #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
    monwise="-"+str(emonname)+"-"+str(yr)
    #print(monwise)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp1_attdata = cursor.fetchall()
    ##print(emp1_attdata)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp2_attdata = cursor.fetchall()
    ##print(emp2_attdata)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp3_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp4_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp5_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp6_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp7_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp8_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp9_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp10_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp11_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp12_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp13_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp14_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp15_attdata = cursor.fetchall()

    '''
    smonwise="-"+str(smonname)+"-"+str(yr)
    emonwise="-"+str(emonname)+"-"+str(yr)
    sql_Query = "SELECT y.Empcode,y.thours FROM (SELECT distinct Cast(Empcode as decimal) As Empcode ,sum(TotalHrs) as 'thours' from tblEmpTotalHoursSimp where (DateFor like '%16"+str(smonwise)+"%' or DateFor like '%17"+str(smonwise)+"%' or DateFor like '%18"+str(smonwise)+"%' or DateFor like '%19"+str(smonwise)+"%' or DateFor like '%20"+str(smonwise)+"%') group by EmpCode order by EmpCode)y where y.thours>=0"
    #print(sql_Query)
    cursor.execute(sql_Query)
    tothrs_attdata = cursor.fetchall()
    #print(tothrs_attdata)
    '''
    
    sql_Query = "SELECT * from `TABLE 18` where PMonth='"+str(monnum)+"' order by Empcode limit 20"
    print(sql_Query)
    cursor.execute(sql_Query)
    payrolldata = cursor.fetchall()
    print(payrolldata)
  
    connection.commit() 
    connection.close()
    cursor.close()
    #return render_template('dataloader.html',fire=data[0][1],airquality=data[0][2],methane=data[0][3])
    global userrole
    ur=userrole
    if ur==2:
        ur="HR Head"
    if ur==1:
        ur="Admin"
    if ur==50:
        ur="HR Team"
    ##print(emp25_attdata)
    
    global rolename
    rolename=session['rolename']
    return render_template('HRattendance1.html',rolename=rolename,payrolldata=payrolldata,userrole=ur,datesfinallist=datesfinallist,emp_primarydata=emp_primarydata,emp16_attdata=emp16_attdata,emp17_attdata=emp17_attdata,emp18_attdata=emp18_attdata,emp19_attdata=emp19_attdata,emp20_attdata=emp20_attdata,emp21_attdata=emp21_attdata,emp22_attdata=emp22_attdata,emp23_attdata=emp23_attdata,emp24_attdata=emp24_attdata,emp25_attdata=emp25_attdata,emp26_attdata=emp26_attdata,emp27_attdata=emp27_attdata,emp28_attdata=emp28_attdata,emp29_attdata=emp29_attdata,emp30_attdata=emp30_attdata,emp31_attdata=emp31_attdata,emp1_attdata=emp1_attdata,emp2_attdata=emp2_attdata,emp3_attdata=emp3_attdata,emp4_attdata=emp4_attdata,emp5_attdata=emp5_attdata,emp6_attdata=emp6_attdata,emp7_attdata=emp7_attdata,emp8_attdata=emp8_attdata,emp9_attdata=emp9_attdata,emp10_attdata=emp10_attdata,emp11_attdata=emp11_attdata,emp12_attdata=emp12_attdata,emp13_attdata=emp13_attdata,emp14_attdata=emp14_attdata,emp15_attdata=emp15_attdata,datescount=datescount,monnum=monnum)
   



#HR Attendance View - Pagination
@app.route('/paginationload')
def paginationload():
    pnum=request.args['pgnum']
    monnum=request.args['month']
    monnum=int(monnum)
    rnum=(int(pnum)*20)-20
    #print(rnum)
    #Global Variables
    datesfinallist=[]  
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()    
    sql_Query = "SELECT distinct Cast(tblEmpMgrMap.Empcode as decimal) As ECode,EmpName,AsstManagerName,ManagerName,DateofJoin as 'DOJ',ProcName FROM tblEmpMgrMap, tblEmpProcMap where tblEmpMgrMap.Empcode=tblEmpProcMap.Empcode group by ECode order by ECode limit "+str(rnum)+",20"
    print(sql_Query)
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()
    ##print(emp_primarydata)
    #print('---------')
    ##print(emp_primarydata[0])
    #print('---------')
    ##print(emp_primarydata[0][1])
    mydate = datetime.now()
    todays_date = datetime.today()
    '''
    # Fetching Dates
    #print("Current year:", todays_date.year)
    #print("Current month:", todays_date.month)
    #print("Current day:", todays_date.day)
    '''

    global empcodelist
    empcodelist=[]    
    sql_Query = "SELECT distinct Empcode from tblEmpTotalHoursSimp"
    cursor.execute(sql_Query)
    empcodedata = cursor.fetchall()
    for i in range(len(empcodedata)):
        val=i+1
        testlist=[]
        testlist.append(val)
        testlist.append(empcodedata[i][0])
        empcodelist.append(testlist)
    ##print(empcodes)
    #print(empcodelist)
    
    
    # Version 2 of attendance
    mydate = datetime.today()
    #print(mydate)

    n = 0
    mydate = mydate - pd.DateOffset(months=n)
    #print(mydate)

    
    startdate=""
    enddate=""
    #earlier
    #monnum=0
    monnum=monnum-1
    startmon=0
    endmon=0
    #if mydate.day>=16:
    #startdate=str(mydate.year)+"-"+str(mydate.month)+"-16" #earlier
    startdate=str(mydate.year)+"-"+str(monnum)+"-16"
    #monnum=mydate.month+1
    nmonth=monnum+1
    startmon=monnum#mydate.month
    endmon=nmonth     
    enddate=str(mydate.year)+"-"+str(nmonth)+"-15"
    '''
    else:
        prevmonth=mydate.month-1
        monnum=prevmonth+1
        startmon=prevmonth
        endmon=mydate.month     
        startdate=str(mydate.year)+"-"+str(prevmonth)+"-16"    
        enddate=str(mydate.year)+"-"+str(mydate.month)+"-15"
    '''
    #print(startdate)
    #print(enddate)
    dateslist=pd.date_range(start=startdate,end=enddate)
    for i in range(len(dateslist)):
        dt=str(dateslist[i])[0:10]
        dtval=dt.split('-')
        dtval[1]=getMonthName(str(dtval[1]))
        dtval[0]=int(dtval[0])-2000
        findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
        
        datesfinallist.append(findate)
        ##print(findate)
    datescount=len(datesfinallist)
    '''
    attdata=[]
    ##print(datesfinallist)
    for i in range(len(datesfinallist)):
        ##print(attDataGenerator(datesfinallist[i]))
        attdata.append(attDataGenerator(datesfinallist[i]))
        
    
    
    connection.commit() 
    connection.close()
    cursor.close()
    ##print(attdata[10])
    return render_template('HRattendance1.html',emp_primarydata=emp_primarydata,attdata=attdata,datesfinallist=datesfinallist)
    

    
    '''
    #print(datesfinallist)
    # Version 1 of attendance
    print(datescount)
    print(len(datesfinallist))
    smonname= monthname(startmon)
    emonname=monthname(endmon)
    print("smon"+str(smonname))
    print("emon"+str(emonname))
    yr=int(todays_date.year)
    yr=yr-2000
    strval=str(todays_date.day)+"-"+mydate.strftime("%b")+"-"+str(yr)
    #print(strval)
    #Date 1-15 check
    #monwise="-"+mydate.strftime("%b")+"-"+str(yr)
    monwise="-"+str(smonname)+"-"+str(yr)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp16_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp17_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp18_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp19_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp20_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp21_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp22_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp23_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp24_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp25_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp26_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp27_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp28_attdata = cursor.fetchall()
    
    emp29_attdata=[]
    emp30_attdata=[]
    
    if datescount>28:
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp29_attdata = cursor.fetchall()
    
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp30_attdata = cursor.fetchall()
    
    emp31_attdata=[]
    if datescount==31:
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp31_attdata = cursor.fetchall()

    #print('==========')
    #Date 1-15 check
    #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
    #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
    monwise="-"+str(emonname)+"-"+str(yr)
    #print(monwise)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp1_attdata = cursor.fetchall()
    ##print(emp1_attdata)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp2_attdata = cursor.fetchall()
    ##print(emp2_attdata)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp3_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp4_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp5_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp6_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp7_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp8_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp9_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp10_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp11_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp12_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp13_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp14_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp15_attdata = cursor.fetchall()
    '''
    smonwise="-"+str(smonname)+"-"+str(yr)
    emonwise="-"+str(emonname)+"-"+str(yr)
    sql_Query = "SELECT y.Empcode,y.thours FROM (SELECT distinct Cast(Empcode as decimal) As Empcode ,sum(TotalHrs) as 'thours' from tblEmpTotalHoursSimp where (DateFor like '%16"+str(smonwise)+"%' or DateFor like '%17"+str(smonwise)+"%' or DateFor like '%18"+str(smonwise)+"%' or DateFor like '%19"+str(smonwise)+"%' or DateFor like '%20"+str(smonwise)+"%') group by EmpCode order by EmpCode)y where y.thours>=0 order by EmpCode limit "+str(rnum)+",20"
    print(sql_Query)
    cursor.execute(sql_Query)
    tothrs_attdata = cursor.fetchall()
    #print(tothrs_attdata)
    '''
   
    
    sql_Query = "SELECT * from `TABLE 18` where PMonth='"+str(monnum)+"' order by Empcode limit 20"
    #print(sql_Query)
    cursor.execute(sql_Query)
    payrolldata = cursor.fetchall()
    #print(payrolldata)
  
    connection.commit() 
    connection.close()
    cursor.close()
    #return render_template('dataloader.html',fire=data[0][1],airquality=data[0][2],methane=data[0][3])
    global userrole
    ur=userrole
    if ur==2:
        ur="HR Head"
    if ur==1:
        ur="Admin"
    if ur==50:
        ur="HR Team"
    ##print(emp25_attdata)
    return render_template('HRattendance1.html',payrolldata=payrolldata,userrole=ur,datesfinallist=datesfinallist,emp_primarydata=emp_primarydata,emp16_attdata=emp16_attdata,emp17_attdata=emp17_attdata,emp18_attdata=emp18_attdata,emp19_attdata=emp19_attdata,emp20_attdata=emp20_attdata,emp21_attdata=emp21_attdata,emp22_attdata=emp22_attdata,emp23_attdata=emp23_attdata,emp24_attdata=emp24_attdata,emp25_attdata=emp25_attdata,emp26_attdata=emp26_attdata,emp27_attdata=emp27_attdata,emp28_attdata=emp28_attdata,emp29_attdata=emp29_attdata,emp30_attdata=emp30_attdata,emp31_attdata=emp31_attdata,emp1_attdata=emp1_attdata,emp2_attdata=emp2_attdata,emp3_attdata=emp3_attdata,emp4_attdata=emp4_attdata,emp5_attdata=emp5_attdata,emp6_attdata=emp6_attdata,emp7_attdata=emp7_attdata,emp8_attdata=emp8_attdata,emp9_attdata=emp9_attdata,emp10_attdata=emp10_attdata,emp11_attdata=emp11_attdata,emp12_attdata=emp12_attdata,emp13_attdata=emp13_attdata,emp14_attdata=emp14_attdata,emp15_attdata=emp15_attdata,datescount=datescount,monnum=monnum)
   

#Payroll Update 
@app.route('/updatepayroll')
def updatepayroll():    
    month=request.args['month']
    year=request.args['year']
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()    
    sql_Query = "SELECT distinct Empcode from tblEmpMgrMap order by Empcode"
    print(sql_Query)
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()
    print(len(emp_primarydata))

    #Variables for payroll
    tothrs=0
    totp=0
    totWO=0
    totHD=0
    totLHD=0
    totNH=0
    totLOP=0
    totDLOP=0
    totCL=0
    totSL=0
    totAL=0
    totpDays=0
    tottrainDays=0
    grosssal=0
    basicrs=0
    salperday=0
    egross=0
    gearnings=0
    perks=0
    deductions=0
    ebasic=0
    EmpPFCont=0
    EmpESICont=0
    EmprPFCont=0
    EmprESICont=0
    grossdeduc=0
    netsal=0
    datesfinallist=[]
    
    startmonth=int(month)-1
    endmonth=int(month)
    smonthname=monthname(startmonth)
    emonthname=monthname(endmonth)
    yr=int(year)-2000
    
    startdate=str(year)+"-"+str(smonthname)+"-16"    
    enddate=str(year)+"-"+str(emonthname)+"-15"
    #print(startdate)
    #print(enddate)
    
    dateslist=pd.date_range(start=startdate,end=enddate)
    #print(dateslist)

    
    for i in range(len(dateslist)):
        dt=str(dateslist[i])[0:10]
        dtval=dt.split('-')
        dtval[1]=getMonthName(str(dtval[1]))
        dtval[0]=int(dtval[0])-2000
        findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
        #print(findate)        
        datesfinallist.append(findate)
        
    
    for i in range(len(emp_primarydata)):
        # tothrs  & P
        sql_Query ="SELECT sum(TotalHrs),count(*) FROM tblEmpTotalHoursSimp where ("
        for j in range(len(datesfinallist)):
            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[j])+"' or "
        sql_Query=sql_Query[0:len(sql_Query)-3]
        sql_Query=sql_Query+") and Atype='P' and Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        tothrsdata = cursor.fetchall()
        try:
            tothrs=round(tothrsdata[0][0],2)
        except:
            tothrs=0
        totp=tothrsdata[0][1]
        if str(tothrs)=="None":
            tothrs=0
        if str(totp)=="None":
            totp=0
        #print(str(emp_primarydata[i][0])+"-"+str(tothrs)+"-"+str(totp))

        #WO
        sql_Query ="SELECT count(*) FROM tblEmpTotalHoursSimp where ("
        for j in range(len(datesfinallist)):
            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[j])+"' or "
        sql_Query=sql_Query[0:len(sql_Query)-3]
        sql_Query=sql_Query+") and Atype='WO' and Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        totWO = cursor.fetchall()
        totWO=totWO[0][0]
        if str(totWO)=="None":
            totWO=0

        #HD
        sql_Query ="SELECT count(*) FROM tblEmpTotalHoursSimp where ("
        for j in range(len(datesfinallist)):
            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[j])+"' or "
        sql_Query=sql_Query[0:len(sql_Query)-3]
        sql_Query=sql_Query+") and Atype='HD' and Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        totHD = cursor.fetchall()
        totHD=totHD[0][0]
        if str(totHD)=="None":
            totHD=0

        #LHD
        sql_Query ="SELECT count(*) FROM tblEmpTotalHoursSimp where ("
        for j in range(len(datesfinallist)):
            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[j])+"' or "
        sql_Query=sql_Query[0:len(sql_Query)-3]
        sql_Query=sql_Query+") and Atype='LHD' and Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        totLHD = cursor.fetchall()
        totLHD=totLHD[0][0]
        if str(totLHD)=="None":
            totLHD=0

        #NH
        sql_Query ="SELECT count(*) FROM tblEmpTotalHoursSimp where ("
        for j in range(len(datesfinallist)):
            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[j])+"' or "
        sql_Query=sql_Query[0:len(sql_Query)-3]
        sql_Query=sql_Query+") and Atype='NH' and Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        totNH = cursor.fetchall()
        totNH=totNH[0][0]
        if str(totNH)=="None":
            totNH=0

        #LOP
        sql_Query ="SELECT count(*) FROM tblEmpTotalHoursSimp where ("
        for j in range(len(datesfinallist)):
            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[j])+"' or "
        sql_Query=sql_Query[0:len(sql_Query)-3]
        sql_Query=sql_Query+") and Atype='LOP' and Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        totLOP = cursor.fetchall()
        totLOP=totLOP[0][0]
        if str(totLOP)=="None":
            totLOP=0

        #DLOP
        sql_Query ="SELECT count(*) FROM tblEmpTotalHoursSimp where ("
        for j in range(len(datesfinallist)):
            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[j])+"' or "
        sql_Query=sql_Query[0:len(sql_Query)-3]
        sql_Query=sql_Query+") and Atype='DLOP' and Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        totDLOP = cursor.fetchall()
        totDLOP=totDLOP[0][0]
        if str(totDLOP)=="None":
            totDLOP=0

        #CL
        sql_Query ="SELECT count(*) FROM tblEmpTotalHoursSimp where ("
        for j in range(len(datesfinallist)):
            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[j])+"' or "
        sql_Query=sql_Query[0:len(sql_Query)-3]
        sql_Query=sql_Query+") and Atype='CL' and Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        totCL = cursor.fetchall()
        totCL=totCL[0][0]
        if str(totCL)=="None":
            totCL=0

        #SL
        sql_Query ="SELECT count(*) FROM tblEmpTotalHoursSimp where ("
        for j in range(len(datesfinallist)):
            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[j])+"' or "
        sql_Query=sql_Query[0:len(sql_Query)-3]
        sql_Query=sql_Query+") and Atype='SL' and Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        totSL = cursor.fetchall()
        totSL=totSL[0][0]
        if str(totSL)=="None":
            totSL=0

        #AL
        sql_Query ="SELECT count(*) FROM tblEmpTotalHoursSimp where ("
        for j in range(len(datesfinallist)):
            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[j])+"' or "
        sql_Query=sql_Query[0:len(sql_Query)-3]
        sql_Query=sql_Query+") and Atype='AL' and Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        totAL = cursor.fetchall()
        totAL=totAL[0][0]
        if str(totAL)=="None":
            totAL=0

        #TG
        sql_Query ="SELECT count(*) FROM tblEmpTotalHoursSimp where ("
        for j in range(len(datesfinallist)):
            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[j])+"' or "
        sql_Query=sql_Query[0:len(sql_Query)-3]
        sql_Query=sql_Query+") and Atype='TG' and Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        tottrainDays = cursor.fetchall()
        tottrainDays=tottrainDays[0][0]
        if str(tottrainDays)=="None":
            tottrainDays=0

        #Payable Days
        totpDays=totp+totWO+totNH+totCL+totSL+totAL+tottrainDays
        totpDays=totpDays+(totHD*0.5)
        temptotLHD=totLHD
        if temptotLHD<=3:
            totpDays=totpDays+temptotLHD
        else:
            totpDays=totpDays+3
            temptotLHD=temptotLHD-3
            totpDays=totpDays+(temptotLHD*0.5)
        totpDays=totpDays-totLOP
        totpDays=totpDays-(totDLOP*2)
        

        #TG
        sql_Query ="SELECT `Gross Salary`,`Basic(Rs)` FROM `TABLE 18` where Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        grosssaldata = cursor.fetchall()
        try:            
            grosssal=grosssaldata[0][0]
            basicrs=grosssaldata[0][1]
        except:
            grosssal=0
            basicrs=0
        if str(grosssal)=="None":
            grosssal=0
        if str(basicrs)=="None":
            basicrs=0
        salperday=float(grosssal)/len(datesfinallist)
        egross=salperday*totpDays

        sql_Query="SELECT (`Travel Allowance`+`Mobile Bill`+`Over Time`+`SLA Adherence`+`Other Incentives`+`Arrears`) AS Total  FROM `TABLE 18` where Empcode="+str(emp_primarydata[i][0])+" and PMonth="+str(month)
        cursor.execute(sql_Query)
        print(sql_Query)
        perks = cursor.fetchall()
        try:            
            perks=perks[0][0]
            if str(perks)=="None":
                perks=0
        except:
            perks=0
        gearnings=egross+perks
        ebasic=(float(basicrs)/len(datesfinallist))*totpDays
        '''
        sql_Query="SELECT (`Travel Allowance`+`Mobile Bill`+`Over Time`+`SLA Adherence`+`Other Incentives`+`Arrears`) AS Total  FROM `TABLE 18` where Empcode="+str(emp_primarydata[i][0])+" and PMonth="+str(month)
        perks = cursor.fetchall()
        perks=perks[0][0]
        if str(perks)=="None":
            perks=0
        gearnings=egross+perks
        ebasic=float(basicrs)/len(datesfinallist)
        '''
        sql_Query="SELECT `Empr PF cont`,`Emp PF Cont`,`Empr ESI cont`,`Emp ESI Cont` FROM `TABLE 18` where Empcode="+str(emp_primarydata[i][0])+" and PMonth="+str(month)
        cursor.execute(sql_Query)
        payrollsetupdata = cursor.fetchall()
        emprpf=0
        emppf=0
        empresic=0
        empesic=0
        try:
            emprpf=payrollsetupdata[0][0]
        except:
            emprpf=0
        try:
            emppf=payrollsetupdata[0][1]
        except:
            emppf=0
        try:
            empresic=payrollsetupdata[0][2]
        except:
            empresic=0
        try:
            empesic=payrollsetupdata[0][3]
        except:
            empesic=0
        
        
        
        EmprPFCont=totpDays*(float(emprpf)/len(datesfinallist))
        EmprESICont=totpDays*(float(empresic)/len(datesfinallist))
        
        EmpPFCont=totpDays*(float(emppf)/len(datesfinallist))
        EmpESICont=totpDays*(float(empesic)/len(datesfinallist))
        
        sql_Query="SELECT (`Prof TAX`+`Income TAX`+`ID Card`+`Quality Deductions`+`Advance`+`Others`) AS Total  FROM `TABLE 18` where Empcode="+str(emp_primarydata[i][0])+" and PMonth="+str(month)
        cursor.execute(sql_Query)
        expenses = cursor.fetchall()
        expenses=0
        try:
            
            expenses=expenses[0][0]
            if str(expenses)=="None":
                expenses=0
        except:
            expenses=0

        grossdeduc=expenses+EmpPFCont+EmpESICont+EmprPFCont+EmprESICont
        netsal=gearnings-grossdeduc
        '''
        gearnings=0
        ebasic=0
        EmpPFCont=0
        EmpESICont=0
        EmprPFCont=0
        EmprESICont=0
        grossdeduc=0
        netsal=0
        #`Travel Allowance`=[value-24],`Mobile Bill`=[value-25],`Over Time`=[value-26],`SLA Adherence`=[value-27],`Other Incentives`=[value-28],`Arrears`=[value-29]
        '''
        ##print(str(emp_primarydata[i][0])+"-"+str(tothrs)+"-"+str(totp)+"-"+str(totWO))
        
        '''
        sql_Query ="SELECT sum(Atype) FROM blEmpTotalHoursSimp where ("
        for j in range(len(datesfinallist)):
            sql_Query=sql_Query+"DateFor='"+str(datesfinallist[j])+"' or "
        sql_Query=sql_Query[0:len(sql_Query)-3]
        sql_Query=sql_Query+") Atype='P' and Empcode="+str(emp_primarydata[i][0])
        #print(sql_Query)
        cursor.execute(sql_Query)
        tothrs = cursor.fetchall()
        tothrs=tothrs[0][0]
        print(str(emp_primarydata[i][0])+"-"+str(tothrs))
        '''

        
        
        updatesqlquery="UPDATE `TABLE 18` SET `Tot Hrs`="+str(tothrs)+",`Tot Present`="+str(totp)+",`WO`="+str(totWO)+",`HD`="+str(totHD)+",`LHD`="+str(totLHD)+",`NH`="+str(totNH)+",`LOP`="+str(totLOP)+",`DLOP`="+str(totDLOP)+",`CL`="+str(totCL)+",`SL`="+str(totSL)+",`AL`="+str(totAL)+",`Payable Days`="+str(totpDays)+",`Training Days`="+str(tottrainDays)+",`Salary Per Day`="+str(salperday)+",`Earned Gross`="+str(egross)+",`Gross Earnings`="+str(gearnings)+",`Earned Basic`="+str(ebasic)+",`Empr PF Cont1`="+str(EmprPFCont)+",`Empr ESI Cont1`="+str(EmprESICont)+",`Empr PF Cont1`="+str(EmpPFCont)+",`Emp ESI Cont1`="+str(EmpESICont)+",`Gross Deduction`="+str(grossdeduc)+",`Net Salary`="+str(netsal)+" where Empcode="+str(emp_primarydata[i][0])+" and PMonth='"+str(month)+"'"
        #print(updatesqlquery)
        cursor.execute(updatesqlquery)
        connection.commit()
        print(str(emp_primarydata[i][0]))
        
        
    
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Payroll Update Successfull!!"
    resp = make_response(json.dumps(msg))
    return resp

#HR Attendance View - Search By Empcode
@app.route('/srchhrattendance')
def srchhrattendance():    
    month=request.args['month']
    year=request.args['year']
    secode=request.args['secode']
    procnm=request.args['procnm']
    mgrname=request.args['mgrnm']
    global rolename
    rolename=session['rolename']
    datescount=0
    #Global Variables
    datesfinallist=[]  
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    ##print(emp_primarydata)
    #print('---------')
    ##print(emp_primarydata[0])
    #print('---------')
    ##print(emp_primarydata[0][1])
    mydate = datetime.now()
    todays_date = datetime.today()
    '''
    # Fetching Dates
    #print("Current year:", todays_date.year)
    #print("Current month:", todays_date.month)
    #print("Current day:", todays_date.day)
    '''

    global empcodelist
    empcodelist=[]
    val=1
    testlist=[]
    testlist.append(val)
    testlist.append(secode)
    empcodelist.append(testlist)
    ##print(empcodes)
    #print(empcodelist)
    
    
    # Version 2 of attendance
    mydate = datetime.today()
    
    if month=='Nov':
        n = 2
        mydate = mydate - pd.DateOffset(months=n)

        
        #print(mydate.day)
        startdate=""
        enddate=""
        if mydate.day>=16:
            startdate=str(mydate.year)+"-"+str(mydate.month)+"-16"
            nmonth=0
            nyear=mydate.year
            if(mydate.month>=12):
                nmonth=1
                nyear=mydate.year+1
            else:
                nmonth=mydate.month+1
            enddate=str(nyear)+"-"+str(nmonth)+"-15"
            
        else:
            prevmonth=0
            prevmonth=mydate.month-1
            startdate=str(mydate.year)+"-"+str(prevmonth)+"-16"    
            enddate=str(mydate.year)+"-"+str(mydate.month)+"-15"

        dateslist=pd.date_range(start=startdate,end=enddate)
        for i in range(len(dateslist)):
            dt=str(dateslist[i])[0:10]
            dtval=dt.split('-')
            dtval[1]=getMonthName(str(dtval[1]))
            dtval[0]=int(dtval[0])-2000
            findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
            
            datesfinallist.append(findate)
            ##print(findate)
    
    elif month=='Dec':
        n = 1
        mydate = mydate - pd.DateOffset(months=n)

        
        #print(mydate.day)
        startdate=""
        enddate=""
        if mydate.day>=16:
            startdate=str(mydate.year)+"-"+str(mydate.month)+"-16"
            nmonth=0
            nyear=mydate.year
            if(mydate.month>=12):
                nmonth=1
                nyear=mydate.year+1
            else:
                nmonth=mydate.month+1
            enddate=str(nyear)+"-"+str(nmonth)+"-15"
            
        else:
            prevmonth=0
            prevmonth=mydate.month-1
            startdate=str(mydate.year)+"-"+str(prevmonth)+"-16"    
            enddate=str(mydate.year)+"-"+str(mydate.month)+"-15"

        dateslist=pd.date_range(start=startdate,end=enddate)
        for i in range(len(dateslist)):
            dt=str(dateslist[i])[0:10]
            dtval=dt.split('-')
            dtval[1]=getMonthName(str(dtval[1]))
            dtval[0]=int(dtval[0])-2000
            findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
            
            datesfinallist.append(findate)
            ##print(findate)
            
    else:
        
        mydate = mydate
        monnum=int(month)
        
        #print(mydate.day)
        startdate=""
        enddate=""
        startmonth=0
        endmonth=0
        
        startdate=str(year)+"-"+str(monnum-1)+"-16"    
        enddate=str(year)+"-"+str(monnum)+"-15"
        print(startdate)
        print(enddate)

        dateslist=pd.date_range(start=startdate,end=enddate)
        for i in range(len(dateslist)):
            dt=str(dateslist[i])[0:10]
            dtval=dt.split('-')
            dtval[1]=getMonthName(str(dtval[1]))
            dtval[0]=int(dtval[0])-2000
            findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
            
            datesfinallist.append(findate)
            print(findate)
        datescount=len(datesfinallist)
    '''
    attdata=[]
    ##print(datesfinallist)
    for i in range(len(datesfinallist)):
        ##print(attDataGenerator(datesfinallist[i]))
        attdata.append(attDataGenerator(datesfinallist[i]))
        
    
    
    connection.commit() 
    connection.close()
    cursor.close()
    ##print(attdata[10])
    return render_template('HRattendance1.html',emp_primarydata=emp_primarydata,attdata=attdata,datesfinallist=datesfinallist)
    

    
    '''
    # Version 1 of attendance
    yr=int(todays_date.year)
    yr=yr-2000
    strval=str(todays_date.day)+"-"+mydate.strftime("%b")+"-"+str(yr)
    #print(strval)
    #Date 1-15 check
    #monwise="-"+mydate.strftime("%b")+"-"+str(yr)
    emp16_attdata=[]
    emp17_attdata=[]
    emp18_attdata=[]
    emp19_attdata=[]
    emp20_attdata=[]
    emp21_attdata=[]
    emp22_attdata=[]
    emp23_attdata=[]
    emp24_attdata=[]
    emp25_attdata=[]
    emp26_attdata=[]
    emp27_attdata=[]
    emp28_attdata=[]
    emp29_attdata=[]
    emp30_attdata=[]
    emp31_attdata=[]
    emp1_attdata=[]
    emp2_attdata=[]
    emp3_attdata=[]
    emp4_attdata=[]
    emp5_attdata=[]
    emp6_attdata=[]
    emp7_attdata=[]
    emp8_attdata=[]
    emp9_attdata=[]
    emp10_attdata=[]
    emp11_attdata=[]
    emp12_attdata=[]
    emp13_attdata=[]
    emp14_attdata=[]
    emp15_attdata=[]
    emp_primarydata=[]
    payrolldata=[]
    if secode!='' and mgrname!='' and procnm!='':
        #sql_Query = "SELECT distinct Cast(tblEmployeeTotalHours.Empcode as decimal) As ECode,empname,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmployeeTotalHours, tblEmpProcMap where tblEmployeeTotalHours.Empcode=tblEmpProcMap.Empcode and tblEmployeeTotalHours.Empcode='"+secode+"' and tblEmployeeTotalHours.ManagerName='"+mgrname+"' and tblEmpProcMap.ProcName='"+procnm+"'   group by ECode order by ECode limit 20"
        sql_Query = "SELECT distinct Cast(tblEmpMgrMap.Empcode as decimal) As ECode,EmpName,AsstManagerName,ManagerName,DateofJoin as 'DOJ',ProcName FROM tblEmpMgrMap, tblEmpProcMap where tblEmpMgrMap.Empcode=tblEmpProcMap.Empcode and tblEmpMgrMap.Empcode='"+secode+"' and tblEmpMgrMap.ManagerName='"+mgrname+"' and tblEmpProcMap.ProcName='"+procnm+"' group by ECode order by ECode limit 20"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp_primarydata = cursor.fetchall()
        smonth=monthname(monnum-1)
        monwise="-"+smonth+"-"+str(yr)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp16_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp17_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp18_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp19_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp20_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp21_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp22_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp23_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp24_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp25_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp26_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp27_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp28_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp29_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp30_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp31_attdata = cursor.fetchall()

        #print('==========')
        #Date 1-15 check
        #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
        #monwise="-"+mydate.strftime("%b")+"-"+str(yr)  
        emonth=monthname(monnum)  
        monwise="-"+emonth+"-"+str(yr)
        #print(monwise)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp1_attdata = cursor.fetchall()
        ##print(emp1_attdata)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp2_attdata = cursor.fetchall()
        ##print(emp2_attdata)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp3_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp4_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp5_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp6_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp7_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp8_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp9_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp10_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp11_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp12_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp13_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp14_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"'))"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp15_attdata = cursor.fetchall()


        sql_Query = "SELECT * from `TABLE 18` where Empcode in (SELECT Empcode from tblEmployeeTotalHours where Empcode='"+secode+"' and ManagerName='"+mgrname+"' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')) order by Empcode limit 20"
        #print(sql_Query)
        cursor.execute(sql_Query)
        payrolldata = cursor.fetchall()
        #print(payrolldata)

    
    if secode!='' and mgrname=='' and procnm=='':
        #sql_Query = "SELECT distinct Cast(tblEmployeeTotalHours.Empcode as decimal) As ECode,empname,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmployeeTotalHours, tblEmpProcMap where tblEmployeeTotalHours.Empcode=tblEmpProcMap.Empcode and tblEmployeeTotalHours.Empcode='"+secode+"' group by ECode order by ECode limit 20"
        sql_Query = "SELECT distinct Cast(tblEmpMgrMap.Empcode as decimal) As ECode,EmpName,AsstManagerName,ManagerName,DateofJoin as 'DOJ',ProcName FROM tblEmpMgrMap, tblEmpProcMap where tblEmpMgrMap.Empcode=tblEmpProcMap.Empcode and tblEmpMgrMap.Empcode='"+secode+"'  group by ECode order by ECode limit 20"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp_primarydata = cursor.fetchall()
        
        smonth=monthname(monnum-1)
        monwise="-"+smonth+"-"+str(yr)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp16_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp17_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp18_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp19_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp20_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp21_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp22_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp23_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp24_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp25_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp26_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp27_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp28_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp29_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp30_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp31_attdata = cursor.fetchall()

        #print('==========')
        #Date 1-15 check
        #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
        #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
         
        emonth=monthname(monnum)  
        monwise="-"+emonth+"-"+str(yr)
        #print(monwise)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp1_attdata = cursor.fetchall()
        ##print(emp1_attdata)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp2_attdata = cursor.fetchall()
        ##print(emp2_attdata)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp3_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp4_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp5_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp6_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp7_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp8_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp9_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp10_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp11_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp12_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp13_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp14_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%' and Empcode='"+secode+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp15_attdata = cursor.fetchall()


        sql_Query = "SELECT * from `TABLE 18` where Empcode='"+secode+"' order by Empcode limit 20"
        #print(sql_Query)
        cursor.execute(sql_Query)
        payrolldata = cursor.fetchall()
        #print(payrolldata)
        
    if secode=='' and mgrname!='' and procnm=='':
        #sql_Query = "SELECT distinct Cast(tblEmployeeTotalHours.Empcode as decimal) As ECode,empname,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmployeeTotalHours, tblEmpProcMap where tblEmployeeTotalHours.Empcode=tblEmpProcMap.Empcode and tblEmployeeTotalHours.ManagerName='"+mgrname+"' group by ECode order by ECode limit 20"
        sql_Query = "SELECT distinct Cast(tblEmpMgrMap.Empcode as decimal) As ECode,EmpName,AsstManagerName,ManagerName,DateofJoin as 'DOJ',ProcName FROM tblEmpMgrMap, tblEmpProcMap where tblEmpMgrMap.Empcode=tblEmpProcMap.Empcode and tblEmpMgrMap.ManagerName='"+mgrname+"' group by ECode order by ECode limit 20"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp_primarydata = cursor.fetchall()
        print(emp_primarydata)
        
        smonth=monthname(monnum-1)
        monwise="-"+smonth+"-"+str(yr)
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '16"+str(monwise)+"%' and ths.Empcode=eth.Empcode and eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp16_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '17"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp17_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '18"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp18_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '19"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp19_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '20"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp20_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '21"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp21_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '22"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp22_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '23"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp23_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '24"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp24_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '25"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp25_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '26"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp26_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '27"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp27_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '28"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp28_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '29"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp29_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '30"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp30_attdata = cursor.fetchall()
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '31"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp31_attdata = cursor.fetchall()

        #print('==========')
        #Date 1-15 check
        #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
        #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
         
        emonth=monthname(monnum)  
        monwise="-"+emonth+"-"+str(yr)
        #print(monwise)
        
        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '01"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp1_attdata = cursor.fetchall()
        ##print(emp1_attdata)

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '02"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp2_attdata = cursor.fetchall()
        ##print(emp2_attdata)

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '03"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp3_attdata = cursor.fetchall()

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '04"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp4_attdata = cursor.fetchall()

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '05"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp5_attdata = cursor.fetchall()

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '06"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp6_attdata = cursor.fetchall()

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '07"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp7_attdata = cursor.fetchall()

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '08"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp8_attdata = cursor.fetchall()

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '09"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp9_attdata = cursor.fetchall()

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '10"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp10_attdata = cursor.fetchall()

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '11"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp11_attdata = cursor.fetchall()

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '12"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp12_attdata = cursor.fetchall()

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '13"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp13_attdata = cursor.fetchall()

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '14"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp14_attdata = cursor.fetchall()

        sql_Query = "SELECT distinct ths.* from tblEmpTotalHoursSimp ths inner join tblEmployeeTotalHours eth where ths.DateFor like '15"+str(monwise)+"%' and ths.Empcode=eth.Empcode and  eth.ManagerName='"+mgrname+"'"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp15_attdata = cursor.fetchall()


        sql_Query = "SELECT * from `TABLE 18` where Empcode in (SELECT Empcode from tblEmpMgrMap where ManagerName='"+mgrname+"') order by Empcode limit 20"
        #print(sql_Query)
        cursor.execute(sql_Query)
        payrolldata = cursor.fetchall()
        #print(payrolldata)
        
    if secode=='' and mgrname=='' and procnm!='':
        #sql_Query = "SELECT distinct Cast(tblEmployeeTotalHours.Empcode as decimal) As ECode,empname,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmployeeTotalHours, tblEmpProcMap where tblEmployeeTotalHours.Empcode=tblEmpProcMap.Empcode and tblEmpProcMap.ProcName='"+procnm+"'   group by ECode order by ECode limit 20"
        sql_Query = "SELECT distinct Cast(tblEmpMgrMap.Empcode as decimal) As ECode,EmpName,AsstManagerName,ManagerName,DateofJoin as 'DOJ',ProcName FROM tblEmpMgrMap, tblEmpProcMap where tblEmpMgrMap.Empcode=tblEmpProcMap.Empcode and tblEmpProcMap.ProcName='"+procnm+"' group by ECode order by ECode limit 20"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp_primarydata = cursor.fetchall()
        
        smonth=monthname(monnum-1)
        monwise="-"+smonth+"-"+str(yr)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp16_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp17_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp18_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp19_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp20_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp21_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp22_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp23_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp24_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp25_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp26_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp27_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp28_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp29_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp30_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp31_attdata = cursor.fetchall()

        #print('==========')
        #Date 1-15 check
        #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
        #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
         
        emonth=monthname(monnum)  
        monwise="-"+emonth+"-"+str(yr)
        #print(monwise)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp1_attdata = cursor.fetchall()
        ##print(emp1_attdata)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp2_attdata = cursor.fetchall()
        ##print(emp2_attdata)
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp3_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp4_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp5_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp6_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp7_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp8_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp9_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp10_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp11_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp12_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp13_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp14_attdata = cursor.fetchall()
        
        sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
        #print(sql_Query)
        cursor.execute(sql_Query)
        emp15_attdata = cursor.fetchall()

        
        sql_Query = "SELECT * from `TABLE 18` where Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"') and PMonth='"+str(monnum)+"' order by Empcode limit 20"
        #print(sql_Query)
        cursor.execute(sql_Query)
        payrolldata = cursor.fetchall()
        #print(payrolldata)
        
       
    #print(emp16_attdata)
    #print(emp17_attdata)
    #print(emp18_attdata)
    #print(emp19_attdata)
    #print(emp20_attdata)
    #print(emp21_attdata)
    #print(emp22_attdata)
    #print(emp23_attdata)
    #print(emp24_attdata)
    #print(emp25_attdata)
    #print(emp26_attdata)
    #print(emp27_attdata)
    #print(emp28_attdata)
    #print(emp29_attdata)
    #print(emp30_attdata)
    #print(emp31_attdata)
    #print(emp1_attdata)
    #print(emp2_attdata)
    #print(emp3_attdata)
    #print(emp4_attdata)
    #print(emp5_attdata)
    #print(emp6_attdata)
    #print(emp7_attdata)
    #print(emp8_attdata)
    #print(emp9_attdata)
    #print(emp10_attdata)
    #print(emp11_attdata)
    #print(emp12_attdata)
    #print(emp13_attdata)
    #print(emp14_attdata)
    #print(emp15_attdata) 
    connection.commit() 
    connection.close()
    cursor.close()
    #return render_template('dataloader.html',fire=data[0][1],airquality=data[0][2],methane=data[0][3])
    
    global userrole
    ur=userrole
    if ur==2:
        ur="HR Head"
    if ur==1:
        ur="Admin"
    if ur==50:
        ur="HR Team"
    #print("jjj")
    #print(payrolldata)
    return render_template('HRattendance1.html',userrole=ur,payrolldata=payrolldata,datesfinallist=datesfinallist,emp_primarydata=emp_primarydata,emp16_attdata=emp16_attdata,emp17_attdata=emp17_attdata,emp18_attdata=emp18_attdata,emp19_attdata=emp19_attdata,emp20_attdata=emp20_attdata,emp21_attdata=emp21_attdata,emp22_attdata=emp22_attdata,emp23_attdata=emp23_attdata,emp24_attdata=emp24_attdata,emp25_attdata=emp25_attdata,emp26_attdata=emp26_attdata,emp27_attdata=emp27_attdata,emp28_attdata=emp28_attdata,emp29_attdata=emp29_attdata,emp30_attdata=emp30_attdata,emp31_attdata=emp31_attdata,emp1_attdata=emp1_attdata,emp2_attdata=emp2_attdata,emp3_attdata=emp3_attdata,emp4_attdata=emp4_attdata,emp5_attdata=emp5_attdata,emp6_attdata=emp6_attdata,emp7_attdata=emp7_attdata,emp8_attdata=emp8_attdata,emp9_attdata=emp9_attdata,emp10_attdata=emp10_attdata,emp11_attdata=emp11_attdata,emp12_attdata=emp12_attdata,emp13_attdata=emp13_attdata,emp14_attdata=emp14_attdata,emp15_attdata=emp15_attdata,datescount=datescount,rolename=rolename)





#HR Attendance View - Search By Process
@app.route('/srchbyproc')
def srchbyproc():    
    procnm=request.args['procnm']
    #Global Variables
    datesfinallist=[]  
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "SELECT distinct Cast(tblEmployeeTotalHours.Empcode as decimal) As ECode,empname,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmployeeTotalHours, tblEmpProcMap where tblEmployeeTotalHours.Empcode=tblEmpProcMap.Empcode and tblEmpProcMap.ProcName='"+procnm+"'  group by ECode order by ECode limit 20"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()
    ##print(emp_primarydata)
    #print('---------')
    ##print(emp_primarydata[0])
    #print('---------')
    ##print(emp_primarydata[0][1])
    mydate = datetime.now()
    todays_date = datetime.today()
    '''
    # Fetching Dates
    #print("Current year:", todays_date.year)
    #print("Current month:", todays_date.month)
    #print("Current day:", todays_date.day)


    global empcodelist
    empcodelist=[]
    val=1
    testlist=[]
    testlist.append(val)
    testlist.append(secode)
    empcodelist.append(testlist)
    ##print(empcodes)
    #print(empcodelist)
    '''
    
    # Version 2 of attendance
    mydate = datetime.today()
    

    n = 1
    mydate = mydate - pd.DateOffset(months=n)

    
    ##print(mydate.day)
    startdate=""
    enddate=""
    if mydate.day>=16:
        startdate=str(mydate.year)+"-"+str(mydate.month)+"-16"
        nmonth=mydate.month+1
        enddate=str(mydate.year)+"-"+str(nmonth)+"-15"
    else:
        prevmonth=mydate.month-1
        startdate=str(mydate.year)+"-"+str(prevmonth)+"-16"    
        enddate=str(mydate.year)+"-"+str(mydate.month)+"-15"

    dateslist=pd.date_range(start=startdate,end=enddate)
    for i in range(len(dateslist)):
        dt=str(dateslist[i])[0:10]
        dtval=dt.split('-')
        dtval[1]=getMonthName(str(dtval[1]))
        dtval[0]=int(dtval[0])-2000
        findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
        
        datesfinallist.append(findate)
        ##print(findate)
    '''
    attdata=[]
    ##print(datesfinallist)
    for i in range(len(datesfinallist)):
        ##print(attDataGenerator(datesfinallist[i]))
        attdata.append(attDataGenerator(datesfinallist[i]))
        
    
    
    connection.commit() 
    connection.close()
    cursor.close()
    ##print(attdata[10])
    return render_template('HRattendance1.html',emp_primarydata=emp_primarydata,attdata=attdata,datesfinallist=datesfinallist)
    

    
    '''
    # Version 1 of attendance
    yr=int(todays_date.year)
    yr=yr-2000
    strval=str(todays_date.day)+"-"+mydate.strftime("%b")+"-"+str(yr)
    #print(strval)
    #Date 1-15 check
    #monwise="-"+mydate.strftime("%b")+"-"+str(yr)
    monwise="-Oct-"+str(yr)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp16_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp17_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp18_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp19_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp20_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp21_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp22_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp23_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp24_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp25_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp26_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp27_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp28_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp29_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp30_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp31_attdata = cursor.fetchall()

    #print('==========')
    #Date 1-15 check
    #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
    #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
    monwise="-Nov-"+str(yr)
    #print(monwise)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp1_attdata = cursor.fetchall()
    ##print(emp1_attdata)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp2_attdata = cursor.fetchall()
    ##print(emp2_attdata)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp3_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp4_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp5_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp6_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp7_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp8_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp9_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp10_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp11_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp12_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp13_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp14_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp15_attdata = cursor.fetchall()


    sql_Query = "SELECT * from `TABLE 18` where Empcode in (SELECT Empcode from tblEmpProcMap where ProcName='"+procnm+"') and PMonth='"+str(monnum)+"'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    payrolldata = cursor.fetchall()
    #print(payrolldata)
   
  
    connection.commit() 
    connection.close()
    cursor.close()
    #return render_template('dataloader.html',fire=data[0][1],airquality=data[0][2],methane=data[0][3])
    
    global userrole
    ur=userrole
    if ur==2:
        ur="HR Head"
    if ur==1:
        ur="Admin"
    if ur==50:
        ur="HR Team"
    ##print(emp25_attdata)
    return render_template('HRattendance1.html',userrole=ur,monnum=2,payrolldata=payrolldata,datesfinallist=datesfinallist,emp_primarydata=emp_primarydata,emp16_attdata=emp16_attdata,emp17_attdata=emp17_attdata,emp18_attdata=emp18_attdata,emp19_attdata=emp19_attdata,emp20_attdata=emp20_attdata,emp21_attdata=emp21_attdata,emp22_attdata=emp22_attdata,emp23_attdata=emp23_attdata,emp24_attdata=emp24_attdata,emp25_attdata=emp25_attdata,emp26_attdata=emp26_attdata,emp27_attdata=emp27_attdata,emp28_attdata=emp28_attdata,emp29_attdata=emp29_attdata,emp30_attdata=emp30_attdata,emp31_attdata=emp31_attdata,emp1_attdata=emp1_attdata,emp2_attdata=emp2_attdata,emp3_attdata=emp3_attdata,emp4_attdata=emp4_attdata,emp5_attdata=emp5_attdata,emp6_attdata=emp6_attdata,emp7_attdata=emp7_attdata,emp8_attdata=emp8_attdata,emp9_attdata=emp9_attdata,emp10_attdata=emp10_attdata,emp11_attdata=emp11_attdata,emp12_attdata=emp12_attdata,emp13_attdata=emp13_attdata,emp14_attdata=emp14_attdata,emp15_attdata=emp15_attdata)

'''
#HR Attendance View - Download Data
@app.route('/downloadattendance')
def downloadattendance():

    # connect the mysql with the python
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')  
    # read the data
    df=sql.read_sql('select * from tblEmpProcMap',con)
    # #print the data
    #print(df)
    # export the data into the excel sheet
    df.to_excel('ds.xls')
    
    return send_from_directory('ds.xls', as_attachment=True)
'''




#HR Attendance View - Search By Manager
@app.route('/srchbymgr')
def srchbymgr():    
    mgrname=request.args['mgrnm']
    #Global Variables
    datesfinallist=[]  
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "SELECT distinct Cast(tblEmployeeTotalHours.Empcode as decimal) As ECode,empname,AsstManagerName,ManagerName,SUBSTRING(DateofJoin, 1,9) as 'DOJ',ProcName FROM tblEmployeeTotalHours, tblEmpProcMap where tblEmployeeTotalHours.Empcode=tblEmpProcMap.Empcode and tblEmployeeTotalHours.ManagerName='"+mgrname+"'  group by ECode order by ECode limit 20"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp_primarydata = cursor.fetchall()
    ##print(emp_primarydata)
    #print('---------')
    ##print(emp_primarydata[0])
    #print('---------')
    ##print(emp_primarydata[0][1])
    mydate = datetime.now()
    todays_date = datetime.today()
    '''
    # Fetching Dates
    #print("Current year:", todays_date.year)
    #print("Current month:", todays_date.month)
    #print("Current day:", todays_date.day)


    global empcodelist
    empcodelist=[]
    val=1
    testlist=[]
    testlist.append(val)
    testlist.append(secode)
    empcodelist.append(testlist)
    ##print(empcodes)
    #print(empcodelist)
    '''
    
    # Version 2 of attendance
    mydate = datetime.today()
    

    n = 1
    mydate = mydate - pd.DateOffset(months=n)

    
    ##print(mydate.day)
    startdate=""
    enddate=""
    if mydate.day>=16:
        startdate=str(mydate.year)+"-"+str(mydate.month)+"-16"
        nmonth=mydate.month+1
        enddate=str(mydate.year)+"-"+str(nmonth)+"-15"
    else:
        prevmonth=mydate.month-1
        startdate=str(mydate.year)+"-"+str(prevmonth)+"-16"    
        enddate=str(mydate.year)+"-"+str(mydate.month)+"-15"

    dateslist=pd.date_range(start=startdate,end=enddate)
    for i in range(len(dateslist)):
        dt=str(dateslist[i])[0:10]
        dtval=dt.split('-')
        dtval[1]=getMonthName(str(dtval[1]))
        dtval[0]=int(dtval[0])-2000
        findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
        
        datesfinallist.append(findate)
        ##print(findate)
    '''
    attdata=[]
    ##print(datesfinallist)
    for i in range(len(datesfinallist)):
        ##print(attDataGenerator(datesfinallist[i]))
        attdata.append(attDataGenerator(datesfinallist[i]))
        
    
    
    connection.commit() 
    connection.close()
    cursor.close()
    ##print(attdata[10])
    return render_template('HRattendance1.html',emp_primarydata=emp_primarydata,attdata=attdata,datesfinallist=datesfinallist)
    

    
    '''
    # Version 1 of attendance
    yr=int(todays_date.year)
    yr=yr-2000
    strval=str(todays_date.day)+"-"+mydate.strftime("%b")+"-"+str(yr)
    #print(strval)
    #Date 1-15 check
    #monwise="-"+mydate.strftime("%b")+"-"+str(yr)
    monwise="-Oct-"+str(yr)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '16"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp16_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '17"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp17_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '18"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp18_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '19"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp19_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '20"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp20_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '21"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp21_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '22"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp22_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '23"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp23_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '24"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp24_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '25"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp25_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '26"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp26_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '27"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp27_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '28"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp28_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '29"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp29_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '30"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp30_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '31"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp31_attdata = cursor.fetchall()

    #print('==========')
    #Date 1-15 check
    #mydate=next_month = datetime.datetime(mydate.year + int(mydate.month / 12), ((mydate.month % 12) + 1), 1)    
    #monwise="-"+mydate.strftime("%b")+"-"+str(yr)    
    monwise="-Nov-"+str(yr)
    #print(monwise)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '01"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp1_attdata = cursor.fetchall()
    ##print(emp1_attdata)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '02"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp2_attdata = cursor.fetchall()
    ##print(emp2_attdata)
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '03"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp3_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '04"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp4_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '05"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp5_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '06"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp6_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '07"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp7_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '08"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp8_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '09"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp9_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '10"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp10_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '11"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp11_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '12"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp12_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '13"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp13_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '14"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp14_attdata = cursor.fetchall()
    
    sql_Query = "SELECT * from tblEmpTotalHoursSimp where DateFor like '15"+str(monwise)+"%' and Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"')"
    #print(sql_Query)
    cursor.execute(sql_Query)
    emp15_attdata = cursor.fetchall()


    


    sql_Query = "SELECT * from `TABLE 18` where Empcode in (SELECT Empcode from tblEmployeeTotalHours where ManagerName='"+mgrname+"') and PMonth='"+str(monnum)+"'"
    #print(sql_Query)
    cursor.execute(sql_Query)
    payrolldata = cursor.fetchall()
    #print(payrolldata)
   
  
    connection.commit() 
    connection.close()
    cursor.close()
    #return render_template('dataloader.html',fire=data[0][1],airquality=data[0][2],methane=data[0][3])
    
    global userrole
    ur=userrole
    if ur==2:
        ur="HR Head"
    if ur==1:
        ur="Admin"
    if ur==50:
        ur="HR Team"
    ##print(emp25_attdata)
    return render_template('HRattendance1.html',userrole=ur,payrolldata=payrolldata,datesfinallist=datesfinallist,emp_primarydata=emp_primarydata,emp16_attdata=emp16_attdata,emp17_attdata=emp17_attdata,emp18_attdata=emp18_attdata,emp19_attdata=emp19_attdata,emp20_attdata=emp20_attdata,emp21_attdata=emp21_attdata,emp22_attdata=emp22_attdata,emp23_attdata=emp23_attdata,emp24_attdata=emp24_attdata,emp25_attdata=emp25_attdata,emp26_attdata=emp26_attdata,emp27_attdata=emp27_attdata,emp28_attdata=emp28_attdata,emp29_attdata=emp29_attdata,emp30_attdata=emp30_attdata,emp31_attdata=emp31_attdata,emp1_attdata=emp1_attdata,emp2_attdata=emp2_attdata,emp3_attdata=emp3_attdata,emp4_attdata=emp4_attdata,emp5_attdata=emp5_attdata,emp6_attdata=emp6_attdata,emp7_attdata=emp7_attdata,emp8_attdata=emp8_attdata,emp9_attdata=emp9_attdata,emp10_attdata=emp10_attdata,emp11_attdata=emp11_attdata,emp12_attdata=emp12_attdata,emp13_attdata=emp13_attdata,emp14_attdata=emp14_attdata,emp15_attdata=emp15_attdata)




#Attendance Edit
@app.route('/attendanceedit')
def attendanceedit():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    ecode=request.args['Ecode']
    adate=request.args['Date']
    atype=request.args['Atype']
    global empcodelist
    
    
    sql_Query = "SELECT distinct Empcode from tblEmpTotalHoursSimp"
    cursor.execute(sql_Query)
    empcodes=[]
    empcodedata = cursor.fetchall()
    for i in range(len(empcodedata)):
        empcodes.append(empcodedata[i][0])
    ##print(empcodes)
    #print(empcodelist)
    
    sql_Query = "SELECT distinct DateFor from tblEmpTotalHoursSimp"
    cursor.execute(sql_Query)
    datedata = cursor.fetchall()
    dates=[]
    for i in range(len(datedata)):
        dateset=datedata[i][0].split(' ')
        date=dateset[0]
        dates.append(date)
    ##print(dates)

    
    connection.commit() 
    connection.close()
    cursor.close()
    global userrole
    ur=userrole
    if ur==2:
        ur="HR Head"
    elif ur==1:
        ur="Admin"
    elif ur==50:
        ur="HR Team"
    else:
        ur="Tester"
    
    return render_template('AttendanceEdit.html',empcodedata=empcodes,datedata=dates,ecode=ecode,adate=adate,atype=atype,userrole=ur)




@app.route('/updateattendance', methods =  ['GET','POST'])
def updateattendance():
    #print("request :"+str(request), flush=True)
    if request.method == 'POST':
        oldAttStat=request.form.get('attstat')
        if oldAttStat!="DLOP":
            connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')   
            cursor = connection.cursor()
            ecode=request.form.get('ecode')
            dated=request.form.get('adate')
            astatus=request.form.get('astatus')
            roleas=request.form.get('ras')
            comments=request.form.get('comments')
            username=request.form.get('loggeduser')
            print(username)
            

            comments=comments +" - Changed by "+str(username)+" from "+str(oldAttStat)+" to "+str(astatus)
            print(comments)
            #print(ecode)
            #print(dated)
            #print(astatus)
            #print(roleas)
            #print(comments)
            '''
            from datetime import datetime
            date_time_str = dated
            date_time_obj = datetime.strptime(date_time_str, '%d-%m-%Y')
            ##print ("The type of the date is now",  type(date_time_obj))
            ##print ("The date is", date_time_obj)
            d = date_time_obj.strftime("%d-%b-%y")
            #print (d)
            '''
            d=dated
            try:
            
                prod_mas = request.files['prod_mas']
                filename = secure_filename(prod_mas.filename)
                #print(filename)
                prod_mas.save(os.path.join("./static/JunkFiles/", filename))
            except:
                filename="no"
            if roleas=='HR Head':
                roleas='2'
            elif roleas=='HR Team':
                roleas='50'
            elif roleas=='Admin':
                roleas='1'


            sql_Query = "Update tblEmpTotalHoursSimp set Modifiedby='"+roleas+"',Atype='"+astatus+"',Comments='"+comments+"' where Empcode='"+ecode+"' and DateFor like '"+str(d)+"%'"        
            #print(sql_Query)
            cursor.execute(sql_Query)
            connection.commit()
            
            connection.close()
            cursor.close()
            return render_template('AttendanceEdit.html',data="Attendance Updated Successfully")
        else:
            return render_template('AttendanceEdit.html',data="Shift Not Assigned")
       

    
