from flask import Flask
from flask import request
from flask import render_template
import sys, os
sys.path.append('/home/ec2-user/python-image-gallery/gallery/ui')
from db_functions import *
import secrets

app = Flask(__name__)

@app.route('/admin')
def admin_list():
    data = listUsers2()
    return render_template('admin.html', results = data)

@app.route('/admin/addUser')
def addUser():
    return render_template('addUser.html')

@app.route('/admin/userAdded', methods=['POST'])
def userAdded():
    a = request.form['username']
    b = request.form['password']
    c = request.form['full_name']
    addUser2(a, b, c)
    return render_template('userAdded.html')

@app.route('/admin/modifyUser')
def modify_user():
    return render_template('modifyUser.html')

@app.route('/admin/deleteUser')
def delete_user():
    return render_template('deleteUser.html')

@app.route('/admin/userDeleted', methods=['POST'])
def userDeleted():
    x = request.form['submit']
    deleteUser2()
    return render_template('userDeleted.html')

if __name__ == '__main__':
    main()
