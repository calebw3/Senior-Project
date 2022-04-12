from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import pyrebase
import json

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

def group(request, name):
    group_ref =  database.child("groups").child(name).get()
    group_data = []
    for key, value in group_ref.val().items():
        group_data.append((key, value))
    description = group_data[0][1]
    github = group_data[1][1]
    members = group_data[2][1]
    pending_members = group_data[3][1]
    tasks = group_data[6][1]
    completed = []
    in_progress = []
    todo = []
    for key, value in tasks.items():
        if value == "completed":
            completed.append(key)
        if value == "in progress":
            in_progress.append(key)
        if value == "todo":
            todo.append(key)
    args = {
    'name': name,
    'group': group_data,
    'pending': pending_members,
    'membs': members,
    'desc': description,
    'git' : github,
    'completed': completed,
    'in_progress': in_progress,
    'todo': todo}

    return render(request, "group.html", args)

def mark_task(request, name, description, status):
    group_ref =  database.child("groups").child(name).get()
    group_data = []
    for key, value in group_ref.val().items():
        group_data.append((key, value))
    tasks = group_data[6][1]
    for key, value in tasks.items():
        if key == description:
            tasks[key] = status
    try:
        database.child("groups").child(name).update({"tasks": tasks})
    except:
        return render(request, "group.html")
    return redirect("/groups/" + name)


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

def member_decision(request, user_email, group_name, decision):
    try:
        account = auth.get_account_info(request.session['uid'])
        group_ref =  database.child("groups").child(group_name).get()
        group_data = []
        for key, value in group_ref.val().items():
            group_data.append((key, value))
        pending_members = group_data[3][1]
        pending_members.remove(user_email)
        if(pending_members == []):
            pending_members = [""]
        database.child("groups").child(group_name).update({"pending_members": pending_members})
        if decision == "accept":
            members = group_data[2][1]
            members.append(user_email)
            database.child("groups").child(group_name).update({"members": members})
        return redirect("/groups/" + group_name)
    except:
        pass
    return redirect("/groups")

def filter(request):
    group_name = request.POST.get('proj_name')
    members_name = request.POST.get('memb_name')
    skills_raw = request.POST.get('skills')
    if group_name == "" and members_name == "" and skills_raw == "":
        return redirect("/explore")
    else:
        members = members_name.replace(" ", "").split(",")
        skills = skills_raw.replace(" ", "").split(",")
    try:
        auth.get_account_info(request.session['uid'])
        results = database.child("groups").get()
        groups = []
        for key, value in results.val().items():
            if (key == group_name) or (len((set(members) & set(value['members']))) > 0) or (len((set(skills) & set(value['skills']))) > 0):
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

def join_request(request, group_name):
    reasoning = request.POST.get('reasoning')
    try:
        account = auth.get_account_info(request.session['uid'])
        curr_email = account['users'][0]['email']
        group_ref =  database.child("groups").child(group_name).get()
        group_data = []
        for key, value in group_ref.val().items():
            group_data.append((key, value))
        pending_members = group_data[3][1]
        pending_members.append(curr_email)
        database.child("groups").child(group_name).update({"pending_members": pending_members})
        return redirect("/explore")
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

def postcreateGroup(request):
    group_name = request.POST.get('new-group-name')
    github = request.POST.get('new-group-github')
    description = request.POST.get('new-group-description')
    skills = request.POST.get('new-group-skills').replace(" ", "").split(",")

    account = auth.get_account_info(request.session['uid'])
    user_email = account['users'][0]['email']

    members = request.POST.get('new-group-members').replace(" ", "").split(",")
    members.insert(0, user_email)

    try:
        for email in reversed(members):
            print(email)
            user_ref = database.child("users").order_by_child("email").equal_to(email).get()

            if not user_ref.val():
                members.remove(email)
                continue

            key = ""
            updated_groups = []
            for result in user_ref.each():
                key = result.key()
                try:
                    updated_groups = list(result.val().get("groups"))
                except:
                    pass

            updated_groups.append(group_name)

            database.child("users").child(key).update({"groups": updated_groups})
            print(members)

        group_ref =  database.child("groups")
        group_posts_ref = group_ref.child(group_name)
        tasks = {'finalize team': 'in progress'}
        pending_members = [""]
        new_post_ref = group_posts_ref.set(
            {
                'description': description,
                'github': github,
                'skills': skills,
                'members': members,
                'public': 'true',
                'tasks': tasks,
                'pending_members': pending_members
            }
        )

    except:
        return render(request, "groups.html")
    return redirect("/groups")
