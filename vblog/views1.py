from django.shortcuts import render,get_object_or_404
from django.http import *
from .forms import *
from .models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q


class blog():
    
    def index(self,request):
        #post_obj = Post.objects.all().order_by('-timestamp')
        post_obj = Post.objects.all()
        return render(request,'post_list.html',{'list':post_obj})

    def login(self,request):
        return render(request,'login.html')


    def logout_page(self,request):
        auth.logout(request)
        return HttpResponseRedirect('/')

    def search(self,request):
        if request.method =='POST':

            
            squery = request.POST.get('search_box', None)
            s = Post.objects.filter(Q(title__icontains=squery) | Q(content__icontains=squery ))
            if s:
                return render(request,'post_search.html',{'q':s})
            else:
                return render(request,'post_notfound.html')
                
                
        return render(request,'post_search.html',{'q':s})    
        #return HttpResponse(squery)

    def auth_view(self,request):
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
    

    def post_create(self,request):
        
        if request.method == 'POST':
            form = PostForm(request.POST,request.FILES)
            if form.is_valid():
                self.fullname=request.user.username
                title=request.POST.get('title')
                content=request.POST.get('content')
                image=form.cleaned_data['image']
                post_con = Post.objects.create(title=title,image=image,content=content)
                post_con.save()
            #instance = form.save(commit=False)
            #instance.save()
                messages.success(request, 'Post has been created...')
                #return HttpResponse("Post has been created...")
        else:
            form=PostForm()
        return render(request,'post_create.html',{'form':form})    

    def post_detail(self,request,id):
        instance = get_object_or_404(Post,id=id)
        name=instance.user.username
        return render(request,'post_detail.html',{'det':instance,'name':self.fullname})
    
    def post_update(self,request,id=None):
        #ins = get_object_or_404(Post,id=id)
        p=Post.objects.get(id=id)
        print p.title
        if request.POST:
            form = PostForm(request.POST,request.FILES,instance=p)
            if form.is_valid():
            #instance = form.save(commit=False)
                form.save()
            #return render(request,'post_create.html',{'instance':p})

        else:
            form = PostForm(instance=p)
            
        return render(request,'post_edit.html',{'form':form,'instance':p}) 

    def post_del(self,request,id=None):
        ins = get_object_or_404(Post,id=id)
        ins.delete()
        return HttpResponse('Post has been deleted')



    def register_user(self,request):
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                #form.save()
                user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
                email = form.cleaned_data['email'])

                messages.success(request, 'You have registered successfully')
                #return HttpResponseRedirect('/accounts/register_success/')

        else:
            form = RegistrationForm()
        return render(request,'register.html',{'form':form})






