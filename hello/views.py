from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import pyrebase

config={
    "apiKey": "AIzaSyCa9H0rqt71YSqnSW5ngHTTcMCG-0j8Hi0",
    "authDomain": "senior-project-4d031.firebaseapp.com",
    "databaseURL": "https://senior-project-4d031-default-rtdb.firebaseio.com/",
    "projectId": "senior-project-4d031",
    "storageBucket": "senior-project-4d031.appspot.com",
    "messagingSenderId": "830621799742",
    "appId": "1:830621799742:web:7501962d6b10ea4b4b486f"
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()
def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote

def index(request):
    return render(request, "index.html")

def group(request):
    args = {}
    return render(request, "group.html", args)

def explore(request):
    try:
        auth.get_account_info(request.session['uid'])
        results = database.child("groups").get()
        groups = []
        for key, value in results.val().items():
            groups.append((key, value))
        args = {'groups': groups}
        return render(request, "explore.html", args)
    except:
        pass
    return redirect("/login")

def groups(request):
    try:
        account = auth.get_account_info(request.session['uid'])
        curr_email = account['users'][0]['email']
        results = database.child("users").order_by_child("email").equal_to(curr_email).get()
        user = []
        for key, value in results.val().items():
            user.append((key, value))
        args = {'user': user}
        return render(request, "groups.html", args)
    except:
        pass
    return redirect("/login")


def signIn(request):
    try:
        auth.get_account_info(request.session['uid'])
        return redirect("/home")
    except:
        pass
    return render(request, "login.html")

def home(request):
    try:
        account = auth.get_account_info(request.session['uid'])
        username = account['users'][0]['email'].split("@")[0]
        args = {'username': username}
        return render(request, "home.html", args)
    except:
        pass
    return redirect("/login")

def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user=auth.sign_in_with_email_and_password(email,pasw)
    except:
        return render(request, "login.html", {"credentials":False})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return redirect("/home")


def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"login.html",{"logged_out":True})

def signUp(request):
    return render(request,"registration.html")

def postsignUp(request):
     email = request.POST.get('email')
     passs = request.POST.get('pass')
     name = request.POST.get('name')
     try:
        # creating a user with the given email and password
        user=auth.create_user_with_email_and_password(email,passs)
        # must create an entry in the users database as well
        uid = user['localId']
     except:
        return render(request, "registration.html")
     return render(request,"login.html")
