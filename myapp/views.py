from django.shortcuts import render,redirect
from .forms import signupForm,notesForm,updateForm,feedbackForm
from .models import user_signup,mynotes
from django.contrib.auth import logout
from django.core.mail import send_mail
from NotesApp import settings

# Create your views here.
def index(request):
    if request.method=='POST':
        if request.POST.get('signup')=='signup':
            newuser=signupForm(request.POST)
            if newuser.is_valid():
                newuser.save()
                print("Signup Successful")
            else:
                print(newuser.errors)  
        elif request.POST.get("login")=="login":
            unm=request.POST['username']
            pas=request.POST['password']


            uid=user_signup.objects.get(username=unm)
            print("Current User:",uid.id)
            user=user_signup.objects.filter(username=unm,password=pas)
            if user:
                print("Login Successfully")
                request.session['user']=unm
                request.session['userid']=uid.id
                return redirect('notes')
            else:
                print("Error! Login Failed!")    
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def notes(request):
    user=request.session.get('user')
    if request.method=='POST':
        newnotes=notesForm(request.POST,request.FILES)
        if newnotes.is_valid():
            newnotes.save()
            print("Your Notes has been Uploaded!")
        else:
            print(newnotes.errors)          
    return render(request,'notes.html',{'user':user})

def contact(request):
    if request.method=='POST':
        newfeedback=feedbackForm(request.POST)
        if newfeedback.is_valid():
            newfeedback.save()
            print("Your Feedback has been Sent!!")

            #Email Sending Code
            # send_mail(subject="Thank You!",message="Dear user\nWe got your feedback,\nThank you for your interest.\nNeed any help,\nContact us on +91 9898876789 | amdavadigamers@gmail.com",from_email=settings.EMAIL_HOST_USER,recipient_list=['h.mosam23@gmail.com','smitbhatti30@gmail.com','patelbhumil8666@gmail.com'])

            sub="Thank You!"
            msg="Dear user\n We got your feedback,\nThank you for your interest.\nNeed any help,\nContact us on +91 9898876789 |"
            from_ID=settings.EMAIL_HOST_USER
            to_ID=[request.POST['email']]
            send_mail(subject=sub,message=msg,from_email=from_ID,recipient_list=to_ID)


        else:
            print(newfeedback.errors)    
    return render(request,'contact.html')

def profile(request):
    user=request.session.get('user')
    uid=request.session.get('userid')
    cuser=user_signup.objects.get(id=uid)
    if request.method=='POST':
        updateuser=updateForm(request.POST)
        if updateuser.is_valid():
            updateuser=signupForm(request.POST,instance=cuser)
            updateuser.save()
            print("Your Profile has been updated")
        else:
            print(updateuser.errors)    
    return render(request,'profile.html',{'user':user,'cuser':user_signup.objects.get(id=uid)})

def userlogout(request):
    logout(request)
    return redirect('/')

