#Mysql
import mysql.connector
from mysql.connector import Error

#User Role - Fetch Personal Email data
def mfetchmgrpersonaldata(empid):
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()

    sql_Query = "select ename,email from tblonboarding where Empcode="+empid   
    cursor.execute(sql_Query)
    mgrinfodata = cursor.fetchall()
    connection.commit()
    print(mgrinfodata)
    connection.close()
    cursor.close()
    return mgrinfodata


#Process Salary Range
def mfetchprocsalrange():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()

    sql_Query = "select * from tblproc_setup where Statuss='Approved'"   
    cursor.execute(sql_Query)
    procsalrangedata = cursor.fetchall()
    connection.commit()
    connection.close()
    cursor.close()
    return procsalrangedata    






#Source of Walkin
def maddsow(sow):
    print(sow)
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "insert into lkpsourofwalkin(srcwlkin) values('"+sow+"')"
    #sql_Query = "IF EXISTS(select * from lkpsourofwalkin where srcwlkin = '"+sow+"') THEN update lkpsourofwalkin set srcwlkin = '"+sow+"' where srcwlkin = '"+sow+"'"
    #print(sql_Query)
    cursor.execute(sql_Query)

    sql_Query = "select * from lkpsourofwalkin order by id"    
    cursor.execute(sql_Query)
    walkindata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    msg=""
    for i in range(len(walkindata)):
        msg=msg+str(walkindata[i][0])+","
        msg=msg+str(walkindata[i][1])+"#"
    return msg

def mupdatesow(sow,sowid):
    print(sow)
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "update lkpsourofwalkin set srcwlkin='"+sow+"' where id="+str(sowid)
    cursor.execute(sql_Query)

    sql_Query = "select * from lkpsourofwalkin order by id"    
    cursor.execute(sql_Query)
    walkindata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    msg=""
    for i in range(len(walkindata)):
        msg=msg+str(walkindata[i][0])+","
        msg=msg+str(walkindata[i][1])+"#"
    return msg
    

def mfetchsow():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()

    sql_Query = "select * from lkpsourofwalkin order by id"    
    cursor.execute(sql_Query)
    walkindata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    return walkindata


def mdeletesow(sowid):
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "delete from lkpsourofwalkin where id="+sowid    
    cursor.execute(sql_Query)

    sql_Query = "select * from lkpsourofwalkin order by id"    
    cursor.execute(sql_Query)
    walkindata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    return walkindata
#-------------------------------------------------------------------------------------------------



#Process - Mgr Amgr
def maddproc(pname,mgr,amgr,texclude,iscommon):
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "insert into lkpprocmgrmap(procname,mgrname,amgrname,timexclude,iscommon) values('"+str(pname)+"','"+str(mgr)+"','"+str(amgr)+"','"+str(texclude)+"','"+str(iscommon)+"')"
    #sql_Query = "IF EXISTS(select * from lkpsourofwalkin where srcwlkin = '"+sow+"') THEN update lkpsourofwalkin set srcwlkin = '"+sow+"' where srcwlkin = '"+sow+"'"
    #print(sql_Query)
    cursor.execute(sql_Query)

    sql_Query = "select * from lkpprocmgrmap order by id"    
    cursor.execute(sql_Query)
    procdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    msg=""
    for i in range(len(procdata)):
        msg=msg+str(procdata[i][0])+","
        msg=msg+str(procdata[i][1])+","
        msg=msg+str(procdata[i][2])+","
        msg=msg+str(procdata[i][3])+","
        msg=msg+str(procdata[i][4])+","
        msg=msg+str(procdata[i][5])+"#"
    return msg

def mupdateproc(pid,pname,mgr,amgr,texclude,iscommon):
    
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "update lkpprocmgrmap set procname='"+str(pname)+"',mgrname='"+str(mgr)+"',amgrname='"+str(amgr)+"',timexclude='"+str(texclude)+"',iscommon='"+str(iscommon)+"' where id="+str(pid)
    cursor.execute(sql_Query)

    sql_Query = "select * from lkpprocmgrmap order by id"    
    cursor.execute(sql_Query)
    procdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    msg=""
    for i in range(len(procdata)):
        msg=msg+str(procdata[i][0])+","
        msg=msg+str(procdata[i][1])+","
        msg=msg+str(procdata[i][2])+","
        msg=msg+str(procdata[i][3])+","
        msg=msg+str(procdata[i][4])+","
        msg=msg+str(procdata[i][5])+"#"
    return msg
    

def mfetchproc():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()

    sql_Query = "select * from lkpprocmgrmap order by id"    
    cursor.execute(sql_Query)
    procdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    return procdata


def mdeleteproc(procid):
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "delete from lkpprocmgrmap where id="+procid    
    cursor.execute(sql_Query)

    sql_Query = "select * from lkpprocmgrmap order by id"    
    cursor.execute(sql_Query)
    procdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    return procdata


#--------------------------------------------------------------------------------------------------












#Employee Category
def maddempcat(empcat,acolor,hdtime,hdcolor,fdtime,fdcolor):
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "insert into lkpempcategory(catname,abscolor,hdtime,hdcolor,fdtime,fdcolor) values('"+empcat+"','"+acolor+"','"+hdtime+"','"+hdcolor+"','"+fdtime+"','"+fdcolor+"')"
    #sql_Query = "IF EXISTS(select * from lkpsourofwalkin where srcwlkin = '"+sow+"') THEN update lkpsourofwalkin set srcwlkin = '"+sow+"' where srcwlkin = '"+sow+"'"
    #print(sql_Query)
    cursor.execute(sql_Query)

    sql_Query = "select * from lkpempcategory order by id"    
    cursor.execute(sql_Query)
    empcatdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    msg=""
    for i in range(len(empcatdata)):
        msg=msg+str(empcatdata[i][0])+","
        msg=msg+str(empcatdata[i][1])+","
        msg=msg+str(empcatdata[i][2])+","
        msg=msg+str(empcatdata[i][3])+","
        msg=msg+str(empcatdata[i][4])+","
        msg=msg+str(empcatdata[i][5])+","
        msg=msg+str(empcatdata[i][6])+"#"
    return msg



def mupdateempcat(empcat,catid,acolor,hdtime,hdcolor,fdtime,fdcolor):
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "update lkpempcategory set catname='"+empcat+"',abscolor='"+acolor+"',hdtime='"+hdtime+"',hdcolor='"+hdcolor+"',fdtime='"+fdtime+"',fdcolor='"+fdcolor+"' where id="+str(catid)
    cursor.execute(sql_Query)

    sql_Query = "select * from lkpempcategory order by id"    
    cursor.execute(sql_Query)    
    empcatdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    msg=""
    for i in range(len(empcatdata)):
        msg=msg+str(empcatdata[i][0])+","
        msg=msg+str(empcatdata[i][1])+","
        msg=msg+str(empcatdata[i][2])+","
        msg=msg+str(empcatdata[i][3])+","
        msg=msg+str(empcatdata[i][4])+","
        msg=msg+str(empcatdata[i][5])+","
        msg=msg+str(empcatdata[i][6])+"#"
    return msg
    

def mfetchempcat():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()

    sql_Query = "select * from lkpempcategory order by id"    
    cursor.execute(sql_Query)
    walkindata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    return walkindata


def mdeleteempcat(catid):
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "delete from lkpempcategory where id="+catid    
    cursor.execute(sql_Query)

    sql_Query = "select * from lkpempcategory order by id"    
    cursor.execute(sql_Query)
    walkindata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    return walkindata

#--------------------------------Payroll Setup-----------------------------------
def mupdatepayroll(emplrpf,emppf,emplyresic,empesic,pt,sdate,odeduc):
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    #sql_Query = "update lkppayrollsetup set emplyrpf='"+str(emplrpf)+"',emppf='"+str(emppf)+"',emplyresic='"+str(emplyresic)+"',empesic='"+str(empesic)+"',pt='"+str(pt)+"',sdate='"+str(sdate)+"',odeduc='"+str(odeduc)+"'"
    sql_Query = "insert into lkppayrollsetup (emplyrpf,emppf,emplyresic,empesic,pt,sdate,odeduc) values('"+str(emplrpf)+"','"+str(emppf)+"','"+str(emplyresic)+"','"+str(empesic)+"','"+str(pt)+"','"+str(sdate)+"','"+str(odeduc)+"')"
    print(sql_Query)
    cursor.execute(sql_Query)

    sql_Query = "select * from lkppayrollsetup order by id desc"    
    cursor.execute(sql_Query)
    payrolldata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    print(payrolldata)
    return payrolldata


def mfetchpayroll():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkppayrollsetup order by id desc"     
    cursor.execute(sql_Query)
    payrolldata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return payrolldata

#--------------------------------Roles Fetch-----------------------------------
def mfetchroles():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkproles"    
    cursor.execute(sql_Query)
    rolesdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return rolesdata

#--------------------------------Users with EmpCode Fetch-----------------------------------
def mfetchuserswithempcode():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "SELECT CONCAT(Empcode,'-',EmpName) FROM tblEmpMgrMap"    
    cursor.execute(sql_Query)
    usersdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return usersdata
#--------------------------------Languages Fetch-----------------------------------
def mfetchlanguages():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkplanguages"    
    cursor.execute(sql_Query)
    languagesdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return languagesdata

#--------------------------------Banks Fetch-----------------------------------
def mfetchbanks():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkpbanks"    
    cursor.execute(sql_Query)
    banksdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return banksdata

#--------------------------------Holidays Fetch-----------------------------------
def mfetchholidays():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkpholidays"    
    cursor.execute(sql_Query)
    holidaydata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return holidaydata

#--------------------------------Weblogins Fetch-----------------------------------
def mfetchweblogins():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkpweblogins"    
    cursor.execute(sql_Query)
    weblogindata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return weblogindata

#--------------------------------Ip Address Fetch-----------------------------------
def mfetchipvals():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkpipvals"    
    cursor.execute(sql_Query)
    ipaddressdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return ipaddressdata
#--------------------------------Qualifications Fetch-----------------------------------
def mfetchqualifications():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkpqualifications"    
    cursor.execute(sql_Query)
    qualdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return qualdata
#--------------------------------ShiftTimings Fetch-----------------------------------
def mfetchshifttimings():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkpshifttimings"    
    cursor.execute(sql_Query)
    shifttimingdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return shifttimingdata
#--------------------------------Paytypes Fetch-----------------------------------
def mfetchpaytypes():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkppaytypes"    
    cursor.execute(sql_Query)
    paytypesdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return paytypesdata
#--------------------------------Departments Fetch-----------------------------------
def mfetchdepartments():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkpdepartments"    
    cursor.execute(sql_Query)
    deptsdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return deptsdata
#--------------------------------Positions Fetch-----------------------------------
def mfetchpositions():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkppositions"    
    cursor.execute(sql_Query)
    positionssdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return positionssdata
#--------------------------------Id proof Fetch-----------------------------------
def mfetchidproofs():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkpidproof"    
    cursor.execute(sql_Query)
    idproofdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return idproofdata
#--------------------------------Manager - Asst manager Fetch-----------------------------------
def mfetchmgr_amgr():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    #sql_Query = "select distinct Managername from tblEmpMgrMap where Managername<>''"    
    #cursor.execute(sql_Query)
    #mgrdata = cursor.fetchall()

    
    sql_Query = "select distinct AsstManagerName from tblEmpMgrMap where AsstManagerName<>''"    
    cursor.execute(sql_Query)
    amgrdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    #mgrdata
    return amgrdata

#--------------------------------Process Fetch - From recruit-----------------------------------
def mfetchrec_procdata():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select ProcessName from tblproc_setup where Statuss='Approved'"     
    cursor.execute(sql_Query)
    procdata = cursor.fetchall()
    
    connection.commit()    
    connection.close()
    cursor.close()
    print(procdata)
    #mgrdata
    return procdata


#--------------------------------Menu Fetch-----------------------------------
def mfetchmenus():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from lkpmenulist"    
    cursor.execute(sql_Query)
    menudata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return menudata

def mfetchroleusers():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select lkpmapuserrole.*,lkproles.rolename from lkpmapuserrole,lkproles where lkpmapuserrole.rolename=lkproles.rolename"    
    cursor.execute(sql_Query)
    usermenudata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return usermenudata

#--------------------------------Rostering Setup-----------------------------------
def mfetchprocdata():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "select distinct ProcName from tblEmpProcMap"
    cursor.execute(sql_Query)
    procdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return procdata

def mfetchtimedata():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "select id,sname from lkpshifttimings"
    cursor.execute(sql_Query)
    timedata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return timedata

def mfetchemplist():
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "select EmpCode, EmpName from tblEmpMgrMap"
    cursor.execute(sql_Query)
    empdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return empdata

def mfetchempproclist(procname):
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    
    sql_Query = "select EmpCode, EmpName from tblEmpMgrMap where EmpCode in (select Empcode from tblEmpProcMap where ProcName='"+procname+"')"
    cursor.execute(sql_Query)
    empdata = cursor.fetchall()
    connection.commit()
    
    connection.close()
    cursor.close()
    
    return empdata


