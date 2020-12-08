from django.shortcuts import render,redirect
from django.http import request,HttpResponse
# Create your views here.
from .models import Contact
from django.contrib.auth.models import User
from django.contrib import messages
from blog. models import Post
from django.contrib.auth import authenticate,login,logout

def home(request):
    return render(request,'home/home.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        content=request.POST.get('content','')

        ContactObj=Contact(name=name,email=email,phone=phone,content=content)
        ContactObj.save()
        messages.success(request, 'Feedback Sent!!!')
    return render(request,"home/contact.html")      

def about(request):
    return render(request,"home/about.html")      


def search(request):
    
    query=request.GET.get('search','')
    if(len(query)>80):
        allPosts=[]
    else:
        allPostsContent=Post.objects.filter(content__icontains=query)
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsCategory = Post.objects.filter(category__icontains=query)
        allPosts= allPostsTitle.union(allPostsContent,allPostsCategory)
    params={'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)

def handleSignup(request):
    if request.method == "POST":
        # get the parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname= request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # checks for erroneous input
        if len(username)<10:
            messages.error(request,"username must be more than 10 characters")
            return redirect('/blog')
        if (not username.isalnum()):
            messages.error(request,"username should only contain letters and numbers")
            return redirect('/blog')
        if (pass1 != pass2):
            messages.error(request,"Passwords don't match")
            return redirect('/blog')    

        # create user
        myuser= User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request, 'Your account has been created')
       
        return redirect('/blog')
    else:
        return HttpResponse("404 - Not Found")


def handleLogin(request):
    if request.method== "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"successfully logged in")
            return redirect('/blog')
        else:
            messages.error(request,"invalid credentials...please try again")
            return redirect('/blog')

    return HttpResponse("login")

def handleLogout(request):
    # if request.method=="POST":
    logout(request)
    messages.success(request,"logged out")
    return redirect('/blog')
