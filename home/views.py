from django.shortcuts import render,redirect
from django.http import request,HttpResponse
# Create your views here.
from .models import Contact
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from blog. models import Post
from .forms import *

# HTML Pages
def home(request):
    users=[]
    user=User.objects.all()
    current_user=request.user
    posts=Post.objects.all()
    for i in user:
        if i==current_user:
            pass
        else:
            users.append(i)
    

    return render(request,'home/home.html',{'users':users,'current_user':current_user,'posts':posts})

def profile(request,slug):
    return render(request,'home/profile.html')
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

def delete(request,id):
    post=Post.objects.get(sno=id)
    post.delete()
    return redirect('/')
def update(request,id):

    post=Post.objects.get(sno=id)
    post.author="unknown"
    post.save()
    return redirect('/')

def about(request):
    
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        
    else:
        form = PostForm()
    context = {'form':form}
    return render(request,"home/about.html",context)      

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

# Authentication API's
def handleSignup(request):
    if request.method == "POST":
        # get the parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname= request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        profile_image= request.POST['profileImage']

        # checks for erroneous input
        if len(username)<10:
            messages.error(request,"username must be more than 10 characters")
            return redirect('/')
        if (not username.isalnum()):
            messages.error(request,"username should only contain letters and numbers")
            return redirect('/')
        if (pass1 != pass2):
            messages.error(request,"Passwords don't match")
            
            return redirect('/')    

        # create user
        myuser= User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        
        myuser.save()
        messages.success(request, 'Your account has been created')
       
        return redirect('/')
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
            return redirect('/')
        else:
            messages.error(request,"invalid credentials...please try again")
            return redirect('/')

    return HttpResponse("login")

def handleLogout(request):
    # if request.method=="POST":
    logout(request)
    messages.success(request,"logged out")
    return redirect('/')

