from flask import Flask, render_template,request,make_response
import numpy as np
import pandas as pd
import os, sys
import random
from random import randint
import mysql.connector
from mysql.connector import Error
from werkzeug.utils import secure_filename
import warnings
warnings.filterwarnings("ignore")
from flask import Flask, render_template,request,make_response
import sys
import random
import pandas as pd
import numpy as np
import json  #json request
#from acc import Processor
import os

app = Flask(__name__)



@app.route('/')
def index():
    
    connection = mysql.connector.connect(host='sg2nlmysql15plsk.secureserver.net',database='transacthrmsdb',user='transactroot',password='Tran@696')    
    cursor = connection.cursor()
    sql_Query = "select * from tblEmployeeTotalHours"
    print(sql_Query)
    cursor.execute(sql_Query)
    data = cursor.fetchall()
    print(data)
    print('---------')
    print(data[0])
    print('---------')
    print(data[0][1])
    connection.commit() 
    connection.close()
    cursor.close()
    #return render_template('dataloader.html',fire=data[0][1],airquality=data[0][2],methane=data[0][3])
    
    
    return render_template('HRattendance.html',data=data)




if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
