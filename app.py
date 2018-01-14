from flask import Flask, render_template, json, request, redirect, session, flash ,url_for
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import os
from datetime import datetime


mysql = MySQL()
app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL configurations

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'blogapp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_blog;")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', posts = posts)


@app.route('/post/<pid>')
def post(pid):
    # print(pid)
    post_id = str(pid)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_blog where blog_id = " + post_id + ";")
    post = cursor.fetchall()
    # cursor.execute("SELECT blog_user.user_name FROM  blog_user,tbl_blog WHERE tbl_blog.blog_id = " + post_id + "AND  blog_user_id = user_id" + ";")
    cursor.execute("SELECT blog_user.user_fname,blog_user.user_lname FROM  blog_user,tbl_blog WHERE blog_user_id = user_id AND tbl_blog.blog_id = " + post_id +  ";")
    name = cursor.fetchall()
    cursor.execute("SELECT blog_user.user_fname,comment FROM blog_user,comments WHERE comments.user_id = blog_user.user_id AND comments.blog_id = " + post_id +  ";")
    comments = cursor.fetchall()
    cursor.execute("SELECT COUNT(l_id) FROM likes WHERE likes.blog_id =  " + post_id +  ";")
    likes = cursor.fetchall()
    # cursor.execute("SELECT tag FROM tags WHERE blog_id = " + post_id +  ";")
    # tags = cursor.fetchall()
    # cursor.execute("SELECT * FROM comments where cid = 5;")
    # cursor.execute("SELECT blog_user.user_name FROM  blog_user,comments WHERE comments.user_id = blog_user.user_id AND comments.blog_id = " + post_id +  ";")
    # commented_by = cursor.fetchall()
    # print(comments)
    return render_template('post.html', post=post, name=name, likes=likes, comments=comments)


@app.route('/Userpost/<pid>')
def Userpost(pid):
    # post_title = str(ptitle)
    post_id = str(pid)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_blog where blog_id = " + post_id + ";")
    post = cursor.fetchall()
    cursor.execute("SELECT blog_user.user_fname,comment FROM blog_user,comments WHERE comments.user_id = blog_user.user_id AND comments.blog_id = " + post_id +  ";")
    comments = cursor.fetchall()


    return render_template('UsersPost.html', post=post, comments=comments)

@app.route('/showSignUp')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    _fname = request.form['inputFName']
    _lname = request.form['inputLName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    if _fname and _lname and _email and _password:

    # All Good, let's call MySQL

        conn = mysql.connect()
        cursor = conn.cursor()
    #_hashed_password = generate_password_hash(_password)
    cursor.callproc('sp_createUser',(_fname,_lname,_email,_password))
    data = cursor.fetchall()
    conn.commit()

    cursor.close()
    conn.close()
    # flash ('Sucessfull signup')

    return render_template('SucessfulSignUp.html')


@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # connect to mysql
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            #if check_password_hash(str(data[0][3]),_password):
            if _password == str(data[0][4]) :
                session['user'] = data[0][0]
                # return redirect('/userHome')
                return redirect('/showDashboard')

            return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/userHome', methods=['POST','GET'])
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')
#     if session.get('user'):
#         try:
#             if session.get('user'):
#                 _user = session.get('user')
#
#                 con = mysql.connect()
#                 cursor = con.cursor()
#                 #cursor.callproc('sp_GetBlogByUser',(_user,))
#                 cursor.execute("select * from tbl_blog;")
#                 blogs = cursor.fetchall()
#
#
#                 blogs_dict = []
#                 # for blog in blogs:
#                 #     blogs_dict.append(list(blog))
#                 # print(blogs_dict)
#
#                 for blog in blogs:
#                     blog_dict = {
#                                 'Id': blog[0],
#                                 'Title': blog[1],
#                                 'Description': blog[2],
#                                 'Date': blog[4]}
#                 blogs_dict.append(blog_dict)
#
#                 return json.dumps(blogs_dict)
#             else:
#                 return render_template('error.html', error = 'Unauthorized Access')
#         except Exception as e:
#     	       return render_template('error.html', error = str(e))
#         return render_template('userHome.html',blogs_dict=blogs_dict)
#
#         return render_template('userHome.html')
#     else:
#         return render_template('error.html',error = 'Unauthorized Access')
# # def getBlog():
#     try:
#         if session.get('user'):
#             _user = session.get('user')
#
#             con = mysql.connect()
#             cursor = con.cursor()
#             #cursor.callproc('sp_GetBlogByUser',(_user,))
#             cursor.execute("select * from tbl_blog;")
#             blogs = cursor.fetchall()
#
#
#             blogs_dict = []
#             for blog in blogs:
#                 blogs_dict.append(list(blog))
#             print(blogs_dict)
#
#
#                 # blog_dict = {
#                 #         'Id': blog[0],
#                 #         'Title': blog[1],
#                 #         'Description': blog[2],
#                 #         'Date': blog[4]}
#                 # blogs_dict.append(blog_dict)
#
#             #return json.dumps(blogs_dict)
#         else:
#             return render_template('error.html', error = 'Unauthorized Access')
#     except Exception as e:
# 	       return render_template('error.html', error = str(e))
#
#     return render_template('userHome.html',blogs_dict=blogs_dict)






@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/showAddBlog')
def showAddBlog():
    return render_template('addBlog.html')


@app.route('/addBlog',methods=['POST'])
def addBlog():
    _title=0
    _description=0
    _user=0
    _tags=" "
    _datetime=" "
    if session.get('user'):
       _title = request.form['inputTitle']
       _tags = request.form['inputTags']
       _description = request.form['inputDescription']
       _user = session.get('user')
       _datetime = datetime.now()
    conn = mysql.connect()
    cursor = conn.cursor()
    #cursor.execute("INSERT INTO tbl_blog VALUES('_title','_description','_user','_datetime')")
    cursor.callproc('sp_addBlog',(_title,_description,_user))
    tags=_tags.split(",")
    cursor.execute("select blog_id from tbl_blog where blog_description = '" + str(_description) + "';")
    _blog_id = cursor.fetchone()[0]
    for tag in tags:
        cursor.execute("INSERT INTO tags VALUES(0,'%s','%s')" %(tag,_blog_id))
        print(tag)
    data = cursor.fetchall()
    if len(data) is 0:
        conn.commit()
        return redirect('/userHome')
    else:
        return render_template('error.html',error = 'An error occurred!')


@app.route('/getBlog')
def getBlog():
    try:
        if session.get('user'):
            _user = session.get('user')

            con = mysql.connect()
            cursor = con.cursor()
            cursor.execute("select * from tbl_blog where blog_user_id = " + str(_user) + ";")
            blogs = cursor.fetchall()

            blogs_dict = []
            for blog in blogs:
                blog_dict = {
                    'Id': blog[0],
                    'Title': blog[1],
                    'Description': blog[2],
                    'Date': blog[4]}
                blogs_dict.append(blog_dict)
            return json.dumps(blogs_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')

    except Exception as e:
        return render_template('error.html', error = str(e))
    return render_template('userHome.html', posts=blogs_dict)


@app.route('/getBlogById',methods=['POST'])
def getBlogById():
    try:
        if session.get('user'):

            _id = request.form['id']
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetBlogById',(_id,_user))
            result = cursor.fetchall()

            blog = []
            blog.append({'Id':result[0][0],'Title':result[0][1],'Description':result[0][2]})

            return json.dumps(blog)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/updateBlog', methods=['POST'])
def updateBlog():
    try:
        if session.get('user'):
            _user = session.get('user')
            _title = request.form['title']
            _description = request.form['description']
            _blog_id = request.form['id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_updateBlog',(_title,_description,_blog_id,_user))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'ERROR'})
    except Exception as e:
        return json.dumps({'status':'Unauthorized access'})
    finally:
        cursor.close()
        conn.close()


@app.route('/deleteBlog',methods=['POST'])
def deleteBlog():
    try:
        if session.get('user'):
            _id = request.form['id']
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteBlog',(_id,_user))
            result = cursor.fetchall()

            if len(result) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'An Error occured'})
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/showDashboard')
def showDashboard():
    try:
        if session.get('user'):
            # _id = request.form['id']
            _user = session.get('user')
            print(_user)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tbl_blog;")
            posts = cursor.fetchall()
            print(posts)
            return render_template('dashboard.html', posts=posts)
        else:
            return render_template('error.html',error = 'An error occured.')

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()



@app.route('/getAllBlogs')
def getAllBlogs():
    try:
        if session.get('user'):

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetAllBlogs')
            result = cursor.fetchall()

            blogs_dict = []
            for blog in result:
                blog_dict = {
                        'Id': blog[0],
                        'Title': blog[1],
                        'Description': blog[2],
                        }
                blogs_dict.append(blog_dict)

            return json.dumps(blogs_dict)

        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/Comment/<pid>', methods=['GET','POST'])
# def getBlogId(pid):
#     try:
#         if session.get('user'):
#
#             _id = pid
#             _user = session.get('user')
#
#             # conn = mysql.connect()
#             # cursor = conn.cursor()
#             # result = cursor.fetchall()
#
#             # blog_id = result[0][0]
#             return _id
#
#         else:
#             return render_template('error.html', error = 'Unauthorized Access')
#     except Exception as e:
#         return render_template('error.html',error = str(e))



def Comment(pid):
    try:
        if session.get('user'):
            user_id = session.get('user')
            post_id = pid
            pid=str(post_id)
            comment = request.form['inputComment']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO comments  VALUES(0,'%s','%s','%s')" %(pid,user_id,comment))
            result=cursor.fetchall()
            # print(result)
            if len(result) is 0:
                cursor.execute("SELECT * FROM tbl_blog where blog_id = " + post_id + ";")
                post = cursor.fetchall()
                conn.commit()
            cursor.execute("SELECT blog_user.user_fname FROM  blog_user,tbl_blog WHERE blog_user_id = user_id AND tbl_blog.blog_id = " + post_id +  ";")
            name = cursor.fetchall()
            cursor.execute("SELECT blog_user.user_fname,comment FROM blog_user,comments WHERE comments.user_id = blog_user.user_id AND comments.blog_id = " + post_id +  ";")
            comments = cursor.fetchall()
            cursor.execute("SELECT COUNT(l_id) FROM likes WHERE likes.blog_id =  " + post_id +  ";")
            likes = cursor.fetchall()
            # return render_template('UsersPost.html' ,post=post)
            # cursor.execute("SELECT tag FROM tags WHERE blog_id = " + post_id +  ";")
            # tags = cursor.fetchall()
            # print(tags)
            return render_template('post.html',post = post, name=name, likes=likes, comments=comments)

        else:
            return render_template('error.html',error = 'U have not logged in, Please log in !')

            # return render_template('UsersPost.html', result=result)

    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/Like/<pid>', methods=['GET','POST'])
def Like(pid):
    try:
        if session.get('user'):
            user_id = session.get('user')
            post_id = pid
            pid=str(post_id)
            # comment = request.form['inputComment']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO likes VALUES(0,'%s','%s')" %(pid,user_id))
            result=cursor.fetchall()
            # print(result)
            if len(result) is 0:
                cursor.execute("SELECT * FROM tbl_blog where blog_id = " + post_id + ";")
                post = cursor.fetchall()
                conn.commit()
            cursor.execute("SELECT blog_user.user_fname FROM  blog_user,tbl_blog WHERE blog_user_id = user_id AND tbl_blog.blog_id = " + post_id +  ";")
            name = cursor.fetchall()
            cursor.execute("SELECT blog_user.user_fname,comment FROM blog_user,comments WHERE comments.user_id = blog_user.user_id AND comments.blog_id = " + post_id +  ";")
            comments = cursor.fetchall()
            cursor.execute("SELECT COUNT(l_id) FROM likes WHERE likes.blog_id =  " + post_id +  ";")
            likes = cursor.fetchall()
            # return redirect('UsersPost.html' ,post=post)
            return render_template('post.html',post = post, name=name, likes=likes, comments=comments)
        else:
            return render_template('error.html',error = 'U have not logged in, Please log in !')

            # return render_template('UsersPost.html', result=result)

    except Exception as e:
        return render_template('error.html',error = str(e))




if __name__ == "__main__":
    app.run(debug=True,port=5000)
