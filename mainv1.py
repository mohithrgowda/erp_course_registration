from flask import Flask
import pandas as pd
import datetime

app= Flask(__name__)



def getMonthName(month_num):
    datetime_object = datetime.datetime.strptime(month_num, "%m")
    month_name = datetime_object.strftime("%b")
    #print("Short name: ",month_name)

    full_month_name = datetime_object.strftime("%B")
    #print("Full name: ",full_month_name)
    return month_name



@app.route('/')
def index():
  datesfinallist=[]
  mydate = datetime.datetime.today()
  print(mydate.day)
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
      
      

  #startdate="2021-10-16"
  #enddate="2021-11-15"
  dateslist=pd.date_range(start=startdate,end=enddate)
  for i in range(len(dateslist)):
      dt=str(dateslist[i])[0:10]
      dtval=dt.split('-')
      dtval[1]=getMonthName(str(dtval[1]))
      
      dtval[0]=int(dtval[0])-2000
      findate=str(dtval[2])+"-"+str(dtval[1])+"-"+str(dtval[0])
      #global datesfinallist
      datesfinallist.append(findate)
      print(findate)


  print(datesfinallist)
  return "<h1>Welcome to CodingX</h1>"


