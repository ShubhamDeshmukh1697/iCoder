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
    if request.method=="POST":
        title = request.POST.get('title')
        
        author = request.POST.get('author')
        content = request.POST.get('content')
        category = request.POST.get('category')
        timestamp = request.POST.get('datetime-local')
        
        a = Post.objects.get(sno=id)
        a.title = title
        a.author = author
        a.content = content
        a.category = category
        a.timestamp = timestamp
        print(a)
        a.save()
        messages.success(request,'Update Successful')
        return redirect('/')

    return render(request,'home/update.html',{'post':post})

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

