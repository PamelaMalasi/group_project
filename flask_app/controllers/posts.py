from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post

from flask import render_template, redirect, session, request, flash

from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
# The limit is 3 MB

#Check if the format is right
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add/post')
def addPost():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        loggedUser = User.get_user_by_id(data)
        return render_template('addPost.html', loggedUser = loggedUser)
    return redirect('/')

@app.route('/create/post', methods = ['POST'])
def createPost():
    if 'user_id' in session:
        if not Post.validate_post(request.form):
            return redirect(request.referrer)
        

     
        if not request.files['image']:
            flash('Image is required!', 'post')
            return redirect(request.referrer)
        image = request.files['image']
        # IMAGE
        # 2  Controll if it is in the correct format 
        if not allowed_file(image.filename):
            flash('Image should be in png, jpg. jpeg format!', 'postImage')
            return redirect(request.referrer)
  
        # 3  ADD Timestamp to use as name to avaid same names on uploaded files

        if image and allowed_file(image.filename):
            filename1 = secure_filename(image.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename1
            filename1=time
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename1))
        
        # 4 - Save it in the db at data 
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'contact': request.form['contact'],
            'location': request.form['location'],
            'user_id': session['user_id'],
            'image' : filename1
        }
        Post.save(data)
        return redirect('/myconcern')
    return redirect('/')

@app.route('/edit/post/<int:id>')
def editPost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data)
        post = Post.get_post_by_id(data)
        print(loggedUser['id'])
        print(post['user_id'])
        if loggedUser['id'] == post['user_id']:
            return render_template('editPost.html', loggedUser = loggedUser, post= post)
        return redirect('/dashboard')
    return redirect('/')


@app.route('/post/<int:id>')
def viewPost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data)
        post = Post.get_post_by_id(data)
        savesNr = Post.get_post_savers(data)
        loggedUserSavedPost = User.get_user_saved_posts(data)


        return render_template('showOne.html',savedpodts=loggedUserSavedPost, loggedUser = loggedUser, post= post, savesNr= savesNr)
    return redirect('/')

@app.route('/edit/post/<int:id>', methods = ['POST'])
def updatePost(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data1)
        post = Post.get_post_by_id(data1)
        if loggedUser['id'] == post['user_id']:

            if not Post.validate_post(request.form):
                return redirect(request.referrer)
            
   
            if not request.files['image']:
                filename1 = post['image']
            image = request.files['image']
            
            if request.files['image']:
                if not allowed_file(image.filename):
                    flash('Image should be in png, jpg. jpeg format!', 'postImage')
                    return redirect(request.referrer)
        
               

                if image and allowed_file(image.filename):
                    filename1 = secure_filename(image.filename)
                    time = datetime.now().strftime("%d%m%Y%S%f")
                    time += filename1
                    filename1=time
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename1))
                    print(image)
            # 4 - Save it in the db at data 
            data = {
                'name': request.form['name'],
                'description': request.form['description'],
                'contact': request.form['contact'],
                'location': request.form['location'],

                'post_id': post['id'],
                'user_id': session['user_id'],
                'image' : filename1
            }
            Post.update(data)
            return redirect('/myconcern')
        return redirect('/concern')
    return redirect('/')

@app.route('/delete/post/<int:id>')
def deletePost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data)
        post = Post.get_post_by_id(data)
                
        if isinstance(post, bool):
            return "Error: Could not retrieve user or product data"
        Post.deleteAllSaves(data)
        Post.delete(data)
        return redirect(request.referrer)
    
    return redirect('/dashboard')
    return redirect('/')


@app.route('/save/<int:id>')
def savePost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        
        savedPost = User.get_user_saved_posts(data)
        print("///////////////////////////////")
        print(savedPost)
        if id not in savedPost:
            Post.addSave(data)
            print("************************************")
            return redirect(request.referrer)
        return redirect(request.referrer)
    return redirect('/')


@app.route('/unsave/<int:id>')
def unsavePost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        print("/------------------------------------")
        Post.unSave(data)
        return redirect(request.referrer)
    return redirect('/')





