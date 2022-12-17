from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
import requests
from bs4 import BeautifulSoup
import random

import pickle
popular_df= pickle.load(open('home/popularD.pkl','rb'))
pt= pickle.load(open('home/pt.pkl','rb'))
similarity_score= pickle.load(open('home/similarity_score.pkl','rb'))
final_data= pickle.load(open('home/final_data.pkl','rb'))


avg_rating=[]
title=[]
img_url=[]
for i in popular_df['title']:
  title.append(i)
for i in popular_df['avg_rating']:
  avg_rating.append(i)
for i in popular_df['img_url']:
  img_url.append(i)

final_list=[]
for n in range(0,50):
  dict={}
  dict['title']=title[n]
  dict['image']=img_url[n]
  dict['rating']=avg_rating[n]
  final_list.append(dict)


# Create your views here.

def get_html_content(element): 
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
        'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    response = requests.get(f'https://www.amazon.com/s?k={element}', headers=headers)
    return response

def search(request):
  if request.user.is_anonymous:
    return redirect("/login")
  
  return render(request, 'search.html')    



def index(request):
  if request.user.is_anonymous:
    return redirect("/login")
  if 'element' in request.GET:
    element = request.GET.get('element')
    html_content= get_html_content(element)
    soup= BeautifulSoup(html_content.text, 'html.parser')
    titles = soup.findAll('span', {'class':'a-size-small a-color-base a-text-normal'})
    ratings = soup.findAll('span', {'class':'a-icon-alt'})
    img_urls=soup.find_all('img',{'class':'s-image'})
    title_list=[]
    rating_list=[]
    imgurl_list=[]

    # appending into list 
    for img_url in img_urls:
        if 'jpg' in img_url['src']:
            imgurl_list.append(img_url['src'])

    for title in titles:
        title_list.append(title.text)
    for rating in ratings:
        rating_list.append(rating.text.replace(' out of 5 stars',''))

    scrap_amz=[]
    for m in range(0,13):
        dict_scrap={}
        dict_scrap['title']=title_list[m]
        dict_scrap['image']=imgurl_list[m]
        dict_scrap['rating']=rating_list[m]
        scrap_amz.append(dict_scrap)



    return render(request, 'search.html', {'scrap_amz':scrap_amz})  

  return render(request, 'index.html', {'popularlist':final_list})
   # return HttpResponse("this is about page")

def about(request):
   if request.user.is_anonymous:
        return redirect("/login")
   return render(request, "about.html")
   # return HttpResponse("this is about page")
def services(request):
   if request.user.is_anonymous:
        return redirect("/login")
   return render(request, "services.html")
   # return HttpResponse("this is services page")
def contact(request):
  if request.user.is_anonymous:
        return redirect("/login")
  #this is process of sending information of user in the database.
  if request.method == "POST":
     name = request.POST.get('name')
     email = request.POST.get('email')
     desc = request.POST.get('desc')
     contact = Contact(name=name,email=email,desc=desc,date=datetime.today())
     contact.save()
     messages.success(request, 'Your message has been sent!')
  return render(request, "contact.html")


def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # check if user has entered corect credentials or not
        user = authenticate(username=username, password=password)
        if user is not None:
          # A backend authenticated the credentials
          login(request, user)
          return redirect("/")
        else:
          # No backend authenticated the credentials
          return render(request, 'login.html')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")


def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        error_message = None
        if pass1!=pass2:
          error_message ='your confirm password donot match with password'    

   

   # check for errorneous inputs
        if not error_message:
   #create the user
          myuser = User.objects.create_user(username, email, pass1)
          myuser.first_name = fname
          myuser.last_name =lname
          myuser.save()
          messages.success(request, "your account has been successfully created")
          login(request, myuser)
          return redirect('/login')
        else:
          return render(request, 'login.html', {'error':error_message})  

    else: 
        return HttpResponse('404 Error - Not Found') 