from django.shortcuts import render,redirect
from django.http import request,HttpResponse
from blog.models import Post,BlogComment
from django.contrib import messages
from blog.templatetags import extra_filters
from next_prev import next_in_order,prev_in_order

# Create your views here.

def blogHome(request):
    allPosts=Post.objects.all()
    context={'allPosts':allPosts}
    return render(request,"blog/blogHome.html",context)

def blogPost(request,slug):
    allPosts=Post.objects.all()
    post = Post.objects.filter(slug=slug).first()
    next = next_in_order(post)
    
    prev = prev_in_order(post)
    
    # getting comment for above post
    comments=BlogComment.objects.filter(post=post,parent=None)
    # getting replies
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    print("replydict is" ,replyDict)

    context={'post':post,'next':next,'prev':prev,'comments':comments,'user':request.user,'replyDict':replyDict}
    return render(request,"blog/blogPost.html",context)      

def postComment(request):
    if request.method=="POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if (parentSno==""):
            commentObj=BlogComment(comment=comment,user=user,post=post)
            messages.success(request,'your comment has been posted')
        else:
            parent=BlogComment.objects.get(sno=parentSno)
            commentObj=BlogComment(comment=comment,user=user,post=post,parent=parent)
            messages.success(request,'your gave a reply')
        commentObj.save()
        

    return redirect(f"/blog/{post.slug}")      