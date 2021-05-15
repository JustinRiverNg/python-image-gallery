import psycopg2
import json
import sys, os
sys.path.insert(1, '/home/ec2-user/python-image-gallery/gallery/ui')
from secrets import get_secret_image_gallery
import secrets

connection = None

def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)

def get_password(secret):
    return secret['password']

def get_host(secret):
    return secret['host']

def get_username(secret):
    return secret['username']

def get_dbname(secret):
    return secret['database_name']

def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))

def execute(query, args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

def main():
    connect()
    while True:
        promptUser()
        userInput = input("Enter command> ")
        if userInput == "1":
            listUsers()
        elif userInput == "2":
            addUser()
        elif userInput == "3":
            editUser()
        elif userInput == "4":
            deleteUser()
        elif userInput == "5":
            print("\nBye.")
            break
        else:
            print("\nInvalid Choice.")

def promptUser():
    print("\n1) List users\n2) Add user\n3) Edit user\n4) Delete user\n5) Quit")

def listUsers():
    connect()
    cursor = connection.cursor()
    result = execute('select * from users')
    print("\n{: <25} {: <25} {: <25}".format("username", "password", "full name"))
    print("-------------------------------------------------------------------------")
    for row in result:
        print("{: <25} {: <25} {: <25}".format(*row))

def listUsers2():
    connect()
    cursor = connection.cursor()
    cursor.execute('select username as us, full_name as fn from users')
    listResults = cursor.fetchall()
    print(listResults)
    return listResults

def addUser():
    cursor = connection.cursor()
    usernameIn = input("\nUsername> ")
    passwordIn = input("Password> ")
    fullNameIn = input("Full Name> ")
    existsQuery = 'select exists (select 1 from users where username=%s)'
    cursor.execute(existsQuery, (usernameIn,))
    userExists = cursor.fetchone()[0]
    if userExists == True:
        print("\nError: username with username " + usernameIn + " already exists")
    else:
        cursor.execute("""
            insert into users (username, password, full_name)
            values (%s, %s, %s);
            """,
            (usernameIn, passwordIn, fullNameIn,))
    connection.commit()

def addUser2(usernameIn, passwordIn, fullNameIn):
    connect()
    cursor = connection.cursor()
    usernameIn = usernameIn
    passwordIn = passwordIn
    fullNameIn = fullNameIn
    cursor.execute("""
        insert into users (username, password, full_name)
        values (%s, %s, %s);
        """,
        (usernameIn, passwordIn, fullNameIn,))
    connection.commit()

def deleteUser():
    cursor = connection.cursor()
    userToDelete = input("\nEnter username to delete> ")
    deleteValidation = input("\nAre you sure you want to delete " + userToDelete + "? ")
    if deleteValidation.lower() == "yes":
        print("\nDeleted.")
        cursor.execute('delete from users where username=%s', (userToDelete,))
    connection.commit()

def deleteUser2(userToDeleteIn):
    cursor = connection.cursor()
    userToDelete = userToDeleteIn
    cursor.execute('delete from users where username=%s', (userToDelete,))
    connection.commit()

def editUser():
    cursor = connection.cursor()
    userToEdit = input("\nEnter username to edit> ")
    existsQuery = 'select exists (select 1 from users where username=%s)'
    cursor.execute(existsQuery, (userToEdit,))
    userExists = cursor.fetchone()[0]
    if userExists == False:
        print("\nNo such user.")
    else:
        newPassword = input("New password (press enter to keep current)> ")
        if newPassword != "":
            cursor.execute('update users set password=%s where username =%s', (newPassword, userToEdit))
        newFullName = input("New full name (press enter to keep current)> ")
        if newFullName != "":
            cursor.execute('update users set full_name=%s where username=%s', (newFullName, userToEdit))
    connection.commit()

if __name__ == '__main__':
    main()
