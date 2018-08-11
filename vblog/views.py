from django.shortcuts import *
from django.http import *
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q



fullname=''

def index(request):
    #post_obj = Post.objects.all().order_by('-timestamp')
    contact_list = Post.objects.all()
    paginator = Paginator(contact_list, 3) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        post_obj = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post_obj = paginator.page(paginator.num_pages)
    return render(request,'post_list.html',{'list':post_obj})



def login(request):
    return render(request,'login.html')


def logout_page(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def search(request):
    if request.method =='POST':

        
        squery = request.POST.get('search_box', None)
        s = Post.objects.filter(Q(title__icontains=squery) | Q(content__icontains=squery ))
        if s:
            return render(request,'post_search.html',{'q':s})
        else:
            return render(request,'post_notfound.html')
            
            
    return render(request,'post_search.html',{'q':s})    
    #return HttpResponse(squery)

def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/postcreate/')
    else:
        return HttpResponseRedirect('/accounts/invalid')
'''
def loggedin(request):
    if request.user.is_authenticated():
        return render(request,'loggedin.html',{'fullname':request.user.username})
    else:
        return HttpResponse('/')
 '''   

@login_required
def post_create(request):
    global fullname
    
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            fullname=request.user.username
            title=request.POST.get('title')
            content=request.POST.get('content')
            image=form.cleaned_data['image']
            post_con = Post.objects.create(user=request.user,title=title,image=image,content=content)
            post_con.save()
        
            messages.success(request, 'Post has been created...')
            #return HttpResponseRedirect("/post_insert/")
            return render(request,'post_create.html',{'form':PostForm(),'uname':request.user.username})
    else:
        form=PostForm()
    return render(request,'post_create.html',{'form':form,'uname':request.user.username})    

def post_insert(request):
    return render(request,'post_success.html')

def updates(request):
    r=request.user
    #u=User.objects.get(username=fullname)
    n=Post.objects.filter(user=r)
    return render(request,'all_posts.html',{'list':n})
    
    

def post_detail(request,id):
    
    instance = get_object_or_404(Post,id=id)

    return render(request,'post_detail.html',{'det':instance})

    
    

def post_update(request,id=None):
    #ins = get_object_or_404(Post,id=id)
    if request.user.is_authenticated():
        p=Post.objects.get(id=id)
        print p.title
        if request.POST:
            form = PostForm(request.POST,request.FILES,instance=p)
            if form.is_valid():
            #instance = form.save(commit=False)
                form.save()
                messages.success(request, 'Post has been updated successfully')
            #return render(request,'post_create.html',{'instance':p})

        else:
            form = PostForm(instance=p)
            
        return render(request,'post_edit.html',{'form':form,'instance':p}) 
    else:
        return HttpResponseRedirect('/')
    
@login_required    
def post_del(request,id=None):
    ins = get_object_or_404(Post,id=id)
    ins.delete()
    messages.success(request, 'Post has been deleted successfully')
    return HttpResponseRedirect('/all_updates/')



def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            '''
            user = User.objects.create_user(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password1'],
            email = form.cleaned_data['email'])
            '''
            messages.success(request, 'You have registered successfully')
            #return HttpResponseRedirect('/success/')
            return render(request,'register.html',{'form':UserCreationForm()})

    else:
        form = UserCreationForm()
    return render(request,'register.html',{'form':form})

def success(request):
    return render(request,'success.html')




