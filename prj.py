from flask import Flask, render_template, request, redirect, url_for, session,make_response, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from pytz import timezone
from datetime import datetime
from dateutil import parser 
import pytz
import json
from json import JSONEncoder
from werkzeug.utils import secure_filename
import hashlib
from flask import jsonify
import re
from datetime import datetime


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'srm'
CORS(app) 
 
app.secret_key = 'your secret key'
mysql = MySQL(app)
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))


@app.route('/',methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/log',methods=['GET', 'POST'])
def log():
    return render_template('log.html')

@app.route('/user_login', methods=['GET','POST'])
def user_login():
    return render_template('user_login.html')

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    
    # Validate email and password (you can add more specific checks here)
    if not email or not pwd:
        return "Please provide both email and password."
    
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT userid FROM userlogin WHERE email=%s AND pwd=MD5(%s)''', (email, pwd))
    row = cursor.fetchone()
    cursor.close()
    
    if row:
        userid = str(row[0])
        response = make_response()
        response.set_cookie('userid', userid)
        return "success"
    else:
        return "Failed to login. Invalid credentials."



@app.route('/signup', methods=['POST'])
def signup():
    uname = request.form.get('uname')
    pwd = request.form.get('pwd')
    email = request.form.get('email')

    # Check if email already exists
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM userlogin WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        return "Email already exists"

    # Validate email format (optional but recommended)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        cursor.close()
        return "Invalid email format"

    # Validate password length (minimal requirement: 8 characters)
    if len(pwd) < 8:
        return "Password must be at least 8 characters long"
    if not any(char.isupper() for char in pwd):
        return "Password must contain at least one uppercase letter"
    if not any(char.islower() for char in pwd):
        return "Password must contain at least one lowercase letter"
    if not any(char.isdigit() for char in pwd):
        return "Password must contain at least one digit"

    # Insert user data into the database
    cursor.execute('''INSERT INTO userlogin (uname, pwd, email) VALUES (%s, MD5(%s), %s)''', (uname, pwd, email))
    mysql.connection.commit()
    cursor.close()

    return "success"


@app.route('/user_dash',methods=['GET', 'POST'])
def user_dash():
    return render_template('user_dash.html')




@app.route('/deptregister', methods=['POST'])
def deptregister():
    try:
        deptname = request.form.get('deptname')
        dloc = request.form.get('dloc')

        if not deptname:
            raise ValueError("Department name cannot be empty")

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO department(dname, dloc) VALUES (%s, %s)''', (deptname, dloc))
        mysql.connection.commit()
        cursor.close()

        return "Inserted successfully"
    except Exception as ex:
        return f"Error: {str(ex)}"

# Other routes and app configuration remain unchanged


@app.route('/department', methods=['GET','POST'])
def department():
    return render_template('department.html')

@app.route('/deptshow', methods =['GET', 'POST'])
def dshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM department")
    row_headers=[x[0] for x in cursor.description]  
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(did)+" value="+str(row)+"></td>"  
            else:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=update("+str(did)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=del("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function update(did)
    {
       deptname=$("#B"+did).val();
       dloc=$("#C"+did).val();
       
       $.ajax({
        url: \"/deptupdate\",
        type: \"POST\",
        data: {did:did,deptname:deptname,dloc:dloc},
        success: function(data){    
        alert(data);
        loaddepartments();
        }
       });
    }
   
    function del(did)
    {
    $.ajax({
        url: \"/deptdelete\",
        type: \"POST\",
        data: {did:did},
        success: function(data){
            alert(data);
            loaddepartments();
        }
        });
    }
    function loaddepartments(){

       $.ajax({
        url: 'http://127.0.0.1:5000/deptshow',
        type: 'POST',
        success: function(data){
          $('#dshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr

@app.route('/deptupdate', methods =['GET', 'POST'])
def deptupdate():
    try:
        did=request.form.get('did')
        deptname = request.form.get('deptname')
        dloc = request.form.get('dloc')
        
        if not deptname:
            raise ValueError("Department name cannot be empty")
    
        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE department SET dname=%s,dloc=%s WHERE dept_id=%s''',(deptname,dloc,did))
        mysql.connection.commit()
        cursor.close()
        return "Updated successfully"
    except Exception as ex:
        return f"Error: {str(ex)}"

@app.route('/deptdelete', methods =['GET', 'POST'])
def deptdelete():
    
    did=request.form.get('did')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM department WHERE dept_id=%s''',(did,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"






@app.route('/catregister', methods=['GET', 'POST'])
def catregister():
    try:
        catname = request.form.get('catname')
        catdes = request.form.get('catdes')
        
        if not catname:
            raise ValueError("Category name cannot be empty")
    
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO item_category(Category_Name,Description) VALUES(%s,%s)''',(catname,catdes))
        mysql.connection.commit()
        cursor.close()
        return "Inserted successfully"
    except Exception as ex:
        return f"Error: {str(ex)}"

@app.route('/itemregister', methods=['GET', 'POST'])
def itemregister():
    
    try:
        iname = request.form.get('iname')
        idesc = request.form.get('idesc')
        idom = request.form.get('idom')
        itype = request.form.get('itype')
        dtype = request.form.get('dtype')
        userid=request.cookies.get('userid')
        
        if not iname:
            raise ValueError("Item name cannot be empty")
        
        try:
            parsed_idom = datetime.strptime(idom, '%Y-%m-%d')
            # Check if the parsed date is not in the future
            if parsed_idom > datetime.now():
                raise ValueError("Please enter a valid past date for item date of manufacture")
        except ValueError:
            raise ValueError("Invalid date format. item date of manufacture cannot be the future date")


        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO item(Item_Name, Description, DOM, Category_Id, dept_id, uid) VALUES(%s, %s, %s, %s, %s, %s)''', (iname, idesc, idom, itype, dtype, userid))
        mysql.connection.commit()
        cursor.close()
        return "Inserted successfully"
    
    except Exception as ex:
        return f"Error: {str(ex)}"
    


@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    return render_template('admin_login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    cursor = mysql.connection.cursor()

    # Hash the entered password (use bcrypt or argon2 instead of MD5)
    # hashed_password = hashlib.md5(pwd.encode()).hexdigest()

    cursor.execute('''SELECT * FROM service_provider WHERE email=%s AND pwd=MD5(%s)''', (email, pwd))
    row = cursor.fetchone()
    cursor.close()

    if row:
        response = make_response("success")
        response.set_cookie('spemail', email)
        return response
    else:
        return "Failed to login"

    
    
@app.route('/reg', methods=['POST'])
def reg():
    Provider_Name = request.form.get('Provider_Name')
    pwd = request.form.get('pwd')
    email = request.form.get('email')
    ppno = request.form.get('ppno')

    # Validate email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email address"

    # Validate password
    if len(pwd) < 8:
        return "Password must be at least 8 characters long"
    if not any(char.isupper() for char in pwd):
        return "Password must contain at least one uppercase letter"
    if not any(char.islower() for char in pwd):
        return "Password must contain at least one lowercase letter"
    if not any(char.isdigit() for char in pwd):
        return "Password must contain at least one digit"

    cursor = mysql.connection.cursor()
    # Check if email already exists
    cursor.execute("SELECT * FROM service_provider WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        return "Email already exists"

    # Insert user data into the database
    cursor.execute('''INSERT INTO service_provider(Provider_Name, pwd, email, Phone)
                      VALUES(%s, MD5(%s), %s, %s)''', (Provider_Name, pwd, email, ppno))
    mysql.connection.commit()
    cursor.close()

    return "success"


@app.route('/itemcategory', methods=['GET','POST'])
def itemcategory():
    return render_template('itemcategory.html')

@app.route('/items', methods=['GET','POST'])
def items():
    return render_template('items.html')



@app.route('/catshow', methods =['GET', 'POST'])
def cshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM item_category")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(did)+" value="+str(row)+"></td>"  
            else:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=update("+str(did)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=del("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function update(did)
    {
       cname=$("#B"+did).val();
       cdes=$("#C"+did).val();
       
       $.ajax({
        url: \"/catupdate\",
        type: \"POST\",
        data: {did:did,cname:cname,cdes:cdes},
        success: function(data){    
        alert(data);
        loadcategories();
        }
       });
    }
   
    function del(did)
    {
    $.ajax({
        url: \"/catdelete\",
        type: \"POST\",
        data: {did:did},
        success: function(data){
            alert(data);
            loadcategories();
        }
        });
    }
    function loadcategories(){

       $.ajax({
        url: 'http://127.0.0.1:5000/catshow',
        type: 'POST',
        success: function(data){
          $('#cshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr

@app.route('/service_request', methods=['GET', 'POST'])
def service_request():
    return render_template('service_request.html')

@app.route('/requestregister', methods=['GET', 'POST'])
def requestregister():
    try:
        ptype = request.form.get('ptype')
        pdes = request.form.get('pdes')
        rdate = request.form.get('rdate')
        
        if not pdes:
            raise ValueError("Problem description cannot be empty")
        
        try:
            parsed_rdate = datetime.strptime(rdate, '%Y-%m-%d')
            # Check if the parsed date is not in the future
            if parsed_rdate > datetime.now():
                raise ValueError("Please enter a valid date for item service request")
        
        except ValueError:
            raise ValueError("Invalid date format. item service request cannot be the future or past date")
    

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO service_request(item_id, pdes, rdate) VALUES(%s, %s, %s)''', (ptype, pdes, rdate))
        mysql.connection.commit()
        cursor.close()
        return "Inserted successfully"
    except Exception as ex:
        return f"Error: {str(ex)}"


@app.route('/itemnames', methods =['GET', 'POST'])
def itemnames():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM item")
    DBData = cursor.fetchall() 
    cursor.close()
    
    itemnames=''
    for result in DBData:
        print(result)
        itemnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return itemnames

@app.route('/requestshow', methods =['GET', 'POST'])
def requestshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT item_id,pdes,rdate FROM service_request")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt>=4:
                rstr=rstr+"<td>"+str(row)+"</td>"
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=date id=KK"+str(ll[cnt])+str(did)+" value="+str(row)+"></td>"  
            else:
                rstr=rstr+"<td>"+"<input type=text id=KK"+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=update("+str(did)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=del("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function update(did)
    {
       pdes=$("#KKB"+did).val();
       rdate=$("#KKC"+did).val();
       
       $.ajax({
        url: \"/requestupdate\",
        type: \"POST\",
        data: {did:did,pdes:pdes,rdate:rdate},
        success: function(data){    
        alert(data);
        loadreq();
        }
       });
    }
   
    function del(did)
    {
    $.ajax({
        url: \"/requestdelete\",
        type: \"POST\",
        data: {did:did},
        success: function(data){
            alert(data);
            loadreq();
        }
        });
    }
    function loadreq(){

       $.ajax({
        url: 'http://127.0.0.1:5000/requestshow',
        type: 'POST',
        success: function(data){
          $('#requestshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr

@app.route('/requestupdate', methods =['GET', 'POST'])
def requestupdate():
    try:
        did=request.form.get('did')
        pdes = request.form.get('pdes')
        rdate = request.form.get('rdate')
        
        if not pdes:
            raise ValueError("pdes name cannot be empty")
    
        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE service_request SET pdes=%s,rdate=%s WHERE item_id=%s''',(pdes,rdate,did))
        mysql.connection.commit()
        cursor.close()
        return "Updated successfully"
    except Exception as ex:
        return f"Error: {str(ex)}"

@app.route('/requestdelete', methods =['GET', 'POST'])
def requestdelete():
    
    did=request.form.get('did')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM service_request WHERE Item_Id=%s''',(did,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"




@app.route('/itemshow', methods =['GET', 'POST'])
def itemshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT item_id,item_name,description,dom,category_id,dept_id FROM item")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt>=4:
                rstr=rstr+"<td>"+str(row)+"</td>"
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=text id=ii"+str(ll[cnt])+str(did)+" value="+str(row)+"></td>"  
            else:
                rstr=rstr+"<td>"+"<input type=text id=ii"+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=update("+str(did)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=del("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function update(did)
    {
       iname=$("#iiB"+did).val();
       ides=$("#iiC"+did).val();
       idom=$("#iiD"+did).val();
       
       $.ajax({
        url: \"/itemupdate\",
        type: \"POST\",
        data: {did:did,iname:iname,ides:ides,idom:idom},    
        success: function(data){    
        alert(data);
        loaditems();
        }
       });
    }
   
    function del(did)
    {
    $.ajax({
        url: \"/itemdelete\",
        type: \"POST\",
        data: {did:did},
        success: function(data){
            alert(data);
            loaditems();
        }
        });
    }
    function loaditems(){

       $.ajax({
        url: 'http://127.0.0.1:5000/itemshow',
        type: 'POST',
        success: function(data){
          $('#itemshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr


@app.route('/catnames', methods =['GET', 'POST'])
def catnames():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM item_category")
    DBData = cursor.fetchall() 
    cursor.close()
    
    rtnames=''
    for result in DBData:
        print(result)
        rtnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return rtnames

@app.route('/deptnames', methods =['GET', 'POST'])
def deptnames():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM department")
    DBData = cursor.fetchall() 
    cursor.close()
    
    deptnames=''
    for result in DBData:
        print(result)
        deptnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return deptnames

@app.route('/itemupdate', methods =['GET', 'POST'])
def itemupdate():
    try:
        did=request.form.get('did')
        iname = request.form.get('iname')
        ides = request.form.get('ides')
        idom = request.form.get('idom')
        if not iname:
            raise ValueError("item name cannot be empty")
        
        try:
            parsed_idom = datetime.strptime(idom, '%Y-%m-%d')
            # Check if the parsed date is not in the future
            if parsed_idom > datetime.now():
                raise ValueError("Please enter a valid past date for item date of manufacture")
        except ValueError:
            raise ValueError("Invalid date format. item date of manufacture cannot be the future date")
    
    
        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE item SET Item_Name=%s,Description=%s,DOM=%s WHERE Item_Id=%s''',(iname,ides,idom,did))
        mysql.connection.commit()
        cursor.close()
        return "Updated successfully"
    except Exception as ex:
        return f"Error: {str(ex)}"

@app.route('/itemdelete', methods =['GET', 'POST'])
def itemdelete():
    
    did=request.form.get('did')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM item WHERE Item_Id=%s''',(did,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"


@app.route('/catupdate', methods =['GET', 'POST'])
def catupdate():
    try:
        did=request.form.get('did')
        cname = request.form.get('cname')
        cdes = request.form.get('cdes')
        
        if not cname:
            raise ValueError("Category name cannot be empty")
    
    
        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE Item_Category SET Category_Name=%s,Description=%s WHERE Category_Id=%s''',(cname,cdes,did))
        mysql.connection.commit()
        cursor.close()
        return "Updated successfully"
    except Exception as ex:
        return f"Error: {str(ex)}"


@app.route('/catdelete', methods =['GET', 'POST'])
def catdelete():
    
    did=request.form.get('did')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM Item_Category WHERE Category_Id=%s''',(did,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"


@app.route('/service_status', methods=['GET', 'POST'])
def service_status():
    return render_template('service_status.html')

@app.route('/statusshow', methods =['GET', 'POST'])
def statusshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM service")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"</tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt>=4:
                rstr=rstr+"<td>"+str(row)+"</td>"
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=text id=ii"+str(ll[cnt])+str(did)+" value="+str(row)+"></td>"  
            else:
                rstr=rstr+"<td>"+"<input type=text id=ii"+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        # rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=update("+str(did)+")></i></a></td>"
        # rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=del("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    

'''
    return rstr




@app.route('/admin_dash',methods=['GET', 'POST'])
def admin_dash():
    return render_template('admin_dash.html')

@app.route('/provider', methods=['GET', 'POST'])
def provider():
    return render_template('admin/provider.html')

@app.route('/spshow', methods =['GET', 'POST'])
def pshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT Provider_Id, Provider_Name, Phone, Email, address FROM service_provider")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
                
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(did)+" value="+str(row)+"></td>"  
            else:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=update("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function update(did)
    {
       Provider_Name=$("#B"+did).val();
       Phone=$("#C"+did).val();
       Email=$("#D"+did).val();
       address=$("#E"+did).val();
       
       $.ajax({
        url: \"/spupdate\",
        type: \"POST\",
        data: {did:did,Provider_Name:Provider_Name,Phone:Phone,Email:Email, address:address},
        success: function(data){    
        alert(data);
        loadsprovider();
        }
       });
    }
   
    
    function loadsprovider(){

       $.ajax({
        url: 'http://127.0.0.1:5000/spshow',
        type: 'POST',
        success: function(data){
          $('#pshow').html(data);
        }
      });
    }
    
    
    </script>

'''

    return rstr

@app.route('/myspshow', methods =['GET', 'POST'])
def myspshow():
    
    cursor = mysql.connection.cursor()
    spemail=request.cookies.get('spemail')
    cursor.execute("SELECT Provider_Name, Phone, Email FROM service_provider where Email=%s",(spemail,))
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr+="</tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt>=0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
                    
            cnt+=1
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    
    return rstr


@app.route('/spupdate', methods =['GET', 'POST'])
def spupdate():
    
    did=request.form.get('did')
    Provider_Name = request.form.get('Provider_Name')
    Phone = request.form.get('Phone')
    Email = request.form.get('Email')
    address = request.form.get('address')
    
    
    cursor = mysql.connection.cursor()
    cursor.execute(''' UPDATE service_provider SET Provider_Name=%s,Phone=%s,Email=%s,address=%s WHERE provider_id=%s''',(Provider_Name,Phone,Email,address,did))
    mysql.connection.commit()
    cursor.close()
    return "Updated successfully"


def validate_phone_number(phone_number):
    # Use regex to validate phone number (10 digits)
    return bool(re.match(r'^\d{10}$', phone_number))

def validate_email(email):
    # Use regex to validate email
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+$', email))

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()

    if 'phone_number' in data:
        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return jsonify({'error': 'Invalid phone number'}), 400

    if 'email' in data:
        email = data['email']
        if not validate_email(email):
            return jsonify({'error': 'Invalid email'}), 400

    return jsonify({'success': 'Data is valid'}), 200



@app.route('/staff', methods=['GET', 'POST'])
def staff():
    return render_template('admin/staff.html')

@app.route('/staffregister', methods=['POST'])
def staffregister():
    try:
        sname = request.form.get('sname')
        sdes = request.form.get('sdes')
        sphone = request.form.get('sphone')
        semail = request.form.get('semail')
        address = request.form.get('address')
        
        # Validation
        if not sname:
            raise ValueError("Staff name cannot be empty")
        if not sdes:
            raise ValueError("Staff description cannot be empty")
        if not sphone:
            raise ValueError("Staff Phone cannot be empty")
        if not validate_phone_number(sphone):
            raise ValueError("Invalid phone number")
        if not semail:
            raise ValueError("Staff email cannot be empty")
        if not validate_email(semail):
            raise ValueError("Invalid email")
        if not address:
            raise ValueError("Staff address cannot be empty")

        # Database insertion
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO staff(staff_name, designation, phone, email, address) VALUES (%s, %s, %s, %s, %s)''', (sname, sdes, sphone, semail, address))
        mysql.connection.commit()
        cursor.close()
        return "Inserted successfully"
    except Exception as ex:
        return f"Error: {str(ex)}"

    

@app.route('/stshow', methods =['GET', 'POST'])
def stshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM staff")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(did)+" value="+str(row)+"></td>"  
            else:
                rstr=rstr+"<td>"+"<input type=text id="+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=update("+str(did)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=del("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function update(did)
    {
       sname=$("#B"+did).val();
       sdes=$("#C"+did).val();
       sphone=$("#D"+did).val();
       semail=$("#E"+did).val();
       address=$("#F"+did).val();
       
       
       $.ajax({
        url: \"/staffupdate\",
        type: \"POST\",
        data: {did:did,sname:sname,sdes:sdes, sphone:sphone, semail:semail, address:address},
        success: function(data){    
        alert(data);
        loadStaffs();
        }
       });
    }
   
    function del(did)
    {
    $.ajax({
        url: \"/staffdelete\",
        type: \"POST\",
        data: {did:did},
        success: function(data){
            alert(data);
            loadStaffs();
        }
        });
    }
    function loadStaffs(){

       $.ajax({
        url: 'http://127.0.0.1:5000/stshow',
        type: 'POST',
        success: function(data){
          $('#stshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr

@app.route('/staffupdate', methods =['GET', 'POST'])
def staffupdate():
    try:
        did=request.form.get('did')
        sname = request.form.get('sname')
        sdes = request.form.get('sdes')
        sphone = request.form.get('sphone')
        semail = request.form.get('semail')
        address = request.form.get('address')
        
        # Validation
        if not sname:
            raise ValueError("Staff name cannot be empty")
        if not sdes:
            raise ValueError("Staff description cannot be empty")
        if not sphone:
            raise ValueError("Staff Phone cannot be empty")
        if not validate_phone_number(sphone):
            raise ValueError("Invalid phone number")
        if not semail:
            raise ValueError("Staff email cannot be empty")
        if not validate_email(semail):
            raise ValueError("Invalid email")
        if not address:
            raise ValueError("Staff address cannot be empty")
    
    
        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE staff SET Staff_name=%s,Designation=%s,Phone=%s,Email=%s,address=%s WHERE staff_id=%s''',(sname,sdes,sphone,semail,address,did))
        mysql.connection.commit()
        cursor.close()
        return "Updated successfully"
    except Exception as ex:
        return f"Error: {str(ex)}"

@app.route('/staffdelete', methods =['GET', 'POST'])
def staffdelete():
    
    did=request.form.get('did')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM staff WHERE staff_id=%s''',(did,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"



@app.route('/srq', methods=['GET', 'POST'])
def srq():
    return render_template('admin/srq.html')

@app.route('/srqshow', methods =['GET', 'POST'])
def srqshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM service_request")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"</tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt>=4:
                rstr=rstr+"<td>"+str(row)+"</td>"
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=text id=ii"+str(ll[cnt])+str(did)+" value="+str(row)+"></td>"  
            else:
                rstr=rstr+"<td>"+"<input type=text id=ii"+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        # rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=update("+str(did)+")></i></a></td>"
        # rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=del("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    

'''
    return rstr


@app.route('/service', methods=['GET', 'POST'])
def service():
    return render_template('admin/service.html')

@app.route('/serviceregister', methods=['GET', 'POST'])
def serviceregister():
    try:
        istype = request.form.get('istype')
        sttype = request.form.get('sttype')
        sdes = request.form.get('sdes')
        sdate = request.form.get('sdate')
        service_cost = request.form.get('service_cost')
        
        if not sdes:
            raise ValueError("description cannot be empty")
        
        if not service_cost:
            raise ValueError("service_cost cannot be empty")
        
        try:
            parsed_idom = datetime.strptime(sdate, '%Y-%m-%d')
            # Check if the parsed date is not in the future
            if parsed_idom > datetime.now():
                raise ValueError("Please enter a valid date of item service")
        except ValueError:
            raise ValueError("Invalid date format. item date of Service cannot be the future date")

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO service(item_id, sid, sdes, sdate, service_cost) VALUES(%s, %s, %s, %s, %s)''', (istype, sttype, sdes, sdate, service_cost))
        mysql.connection.commit()
        cursor.close()
        return "Inserted successfully"
    except Exception as ex:
        return f"Error: {str(ex)}"

@app.route('/rqitemnames', methods =['GET', 'POST'])
def rqitemnames():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM service_request")
    DBData = cursor.fetchall() 
    cursor.close()
    
    rqitemnames=''
    for result in DBData:
        print(result)
        rqitemnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return rqitemnames

@app.route('/staffnames', methods =['GET', 'POST'])
def staffnames():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM staff")
    DBData = cursor.fetchall() 
    cursor.close()
    
    staffnames=''
    for result in DBData:
        print(result)
        staffnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return staffnames

@app.route('/serviceshow', methods =['GET', 'POST'])
def serviceshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT item_id,sid,sdes,sdate,service_cost FROM service")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
                
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=date id=SS"+str(ll[cnt])+str(did)+" value="+str(row)+"></td>" 
            
            else:
                rstr=rstr+"<td>"+"<input type=text id=SS"+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=update("+str(did)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=del("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
        
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function update(did)
    {
       
       
       sdes=$("#SSC"+did).val();
       sdate=$("#SSD"+did).val();
       service_cost=$("#SSE"+did).val();
       
       
       $.ajax({
        url: \"/serviceupdate\",
        type: \"POST\",
        data: {did:did,sdes:sdes,sdate:sdate,service_cost:service_cost},    
        success: function(data){    
        alert(data);
        loadservice();
        }
       });
    }
   
    function del(did)
    {
    $.ajax({
        url: \"/servicedelete\",
        type: \"POST\",
        data: {did:did},
        success: function(data){
            alert(data);
            loadservice();
        }
        });
    }
    function loadservice(){

       $.ajax({
        url: 'http://127.0.0.1:5000/serviceshow',
        type: 'POST',
        success: function(data){
          $('#serviceshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr
    
    
@app.route('/serviceupdate', methods =['GET', 'POST'])
def serviceupdate():
    try:
        did=request.form.get('did')
        sdes = request.form.get('sdes')
        sdate = request.form.get('sdate')
        service_cost = request.form.get('service_cost')
        
        if not service_cost:
            raise ValueError("service_cost cannot be empty")
        
        try:
            parsed_idom = datetime.strptime(sdate, '%Y-%m-%d')
            # Check if the parsed date is not in the future
            if parsed_idom > datetime.now():
                raise ValueError("Please enter a valid date of item service")
        except ValueError:
            raise ValueError("Invalid date format. item date of Service cannot be the future date")
    
    
    
        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE service SET sdes=%s,sdate=%s,service_cost=%s WHERE Item_Id=%s''' ,(sdes,sdate,service_cost,did))
        mysql.connection.commit()
        cursor.close()
        return "Updated successfully"
    except Exception as ex:
        return f"Error: {str(ex)}"
    


@app.route('/servicedelete', methods =['GET', 'POST'])
def servicedelete():
    
    did=request.form.get('did')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM service WHERE Item_Id=%s ''',(did,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"

if __name__ == '__main__':
    app.run(debug=True)