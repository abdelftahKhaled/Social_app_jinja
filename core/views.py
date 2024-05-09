from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login ,logout, authenticate
def registere(request):
     if  request.method=='POST':
        username=request.POST['username'] 
        email=request.POST['email'] 
        password1=request.POST['password1'] 
        password2=request.POST['password2'] 
        Query_if_email_exsist=User.objects.filter(email=email)
        if password1 != password2:
           messages.error(request,"password 1 not equal password 2")
           return redirect('register')
        elif(Query_if_email_exsist):
            messages.error(request,"email is exsist")
            return redirect('register')
        else:
            create_user=User.objects.create_user(username=username,email=email,password=password1)
            create_user.save()
            return redirect('login')




     return render(request,'core\signup.html',)
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
          username=request.POST['username']    
          password=request.POST['password']   

          try:
              user =User.objects.get(username=username)
              
          except :
              messages.error(request,'error in username')
              
              return redirect('login')
          else:
                auth=authenticate(request,username=username,password=password)
                if auth is not None:
                    login(request,auth)
                    return redirect('/')
                else:
                    messages.error(request,'error in username Or Password')
                    return redirect('login')
    return render(request,'core\signin.html',{})
                
              
       


            












    context={

        
    }
    return render(request,'core/signin.html',context)

@login_required(login_url="login")
def logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url="login")
def home (request):
    if request.method=='POST':

       image=request.FILES['image']
       caption=request.POST['caption']
       new_post=Post.objects.create(image=image,caption=caption,host=request.user)
       new_post.save()
    
    #algorithmes to get  followers
    followersByUser__Id=follower.objects.filter(Follower=request.user.id).values_list('user_id', flat=True)
    
    #algorithmes to get  non followers
    non_followers = User.objects.exclude(id__in=followersByUser__Id)

    ##algorithmes to get  posts of  followers
    followersByUser=follower.objects.filter(Follower=request.user.id).values_list('user', flat=True)
    postsOfFollower=Post.objects.filter(host__in=followersByUser)
    ##algorithmes to get  comment to posts of followers and collect all together
    post_and_comment_arr=[]
    for post in postsOfFollower:
        commentOfPosts=Comment.objects.filter(post=post)
        post_and_comment_arr.append((post,commentOfPosts))
    

    context={
    "post_and_comment_arr":post_and_comment_arr ,'non_followers':non_followers, 
    
    
     }
    return render(request,'core\index.html',context)
@login_required(login_url="login")
def setting(request):

    user=User.objects.get(id=request.user.id)
    profileUser=Profile.objects.get(user=user) 
    if request.method=='POST':
        frist_name=request.POST.get('first_name')
        image=request.FILES['image']
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        location=request.POST.get('location')
        bio=request.POST.get('bio')
        user.first_name=frist_name
        user.last_name=last_name
        user.email=email
        profileUser.bio=bio
        profileUser.image=image
        profileUser.locatios=location
        user.save()
        profileUser.save()
        return redirect('setting')


    context={
         
        'profile':profileUser

        
    }
    return render(request,'core\setting.html',context)

def profile(request,pk):
    current_user=User.objects.get(id=pk)
    

    posts=Post.objects.filter(host=current_user)
    psot_length=posts.count()
    user_followers=follower.objects.filter(user=current_user).count()
    user_following=follower.objects.filter(Follower=current_user.id).count()

    Queryfollowe=follower.objects.filter(user=current_user,Follower=request.user.id).count()

    if Queryfollowe:

       button_text='Unfollow'
    else:
        button_text='Follow'
 

    context={
     'current_user':current_user,
     'posts':posts,
     'psot_length':psot_length,
       'user_followers' :user_followers,
       'user_following':user_following,
       'button_text':button_text
    }
    return render(request,'core\profile.html',context)
def  follow(request):
     followe=request.POST['follower']
     user=request.POST['user']
     redir=request.POST['redir']
     User_Object=User.objects.get(username=user)
     _redirect=''
     if redir=='profile':
            username=User_Object.id
            redirct_profile=f'profile/{username}'
            _redirect=redirct_profile
     else:
            _redirect='home'
     Queryfollowe=follower.objects.filter(user=User_Object,Follower=followe).count()
     if Queryfollowe:
           Query=follower.objects.get(user=User_Object,Follower=followe)
           Query.delete()
           print('unfollow')
           return redirect(_redirect)
     else:
          foll=follower.objects.create(user=User_Object,Follower=followe)  
          foll.save()
          print('follow')
          return redirect(_redirect)

def like_post(request,pk):
    person_liker=request.user
    post=Post.objects.get(id=pk)
    Query_of_post=like.objects.filter(post=post,person_liker=person_liker).count()
    if Query_of_post==0:
       creat_like=like.objects.create(post=post,person_liker=person_liker)
       post.no_likes=post.no_likes+1
       post.save()
       creat_like.save()
       
    else:
        lik=like.objects.get(post=post,person_liker=person_liker)
        post.no_likes=post.no_likes-1
        lik.delete()
        post.save()
    return redirect('home')
     
     
