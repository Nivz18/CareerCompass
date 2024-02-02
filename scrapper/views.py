from django.shortcuts import render,redirect
import requests
from bs4 import BeautifulSoup
from .models import *
from django.core.paginator import Paginator
# Create your views here.

def scrape(request):
    
    return render(request,'friends.html')  
  
def jobs(request):
    #page=requests.get('https://www.placementindia.com/')
    page=requests.get('https://www.placementindia.com/job-search/search.php?seeker_search_keyword=developer+engineer&seeker_search_city=&seeker_search_experience=0')
    soup=BeautifulSoup(page.text,'html.parser')
    role_list=[]
    company_list=[]
    exp_list=[]
    ctc_list=[]
    l_list=[]
    jd=JobDetails.objects.all()
    if(jd!=None):
       jd.delete()
    for link in soup.find_all('a',class_='job-name'):
        role=link.text
        role_list.append(role)
    for link in soup.find_all('a',class_='job-name'):
        lnk=link.get('href')
        l_list.append(lnk)  
    

    cmpnylst=soup.find_all('p',class_='job-cname')#get the company name in list
    for cl in cmpnylst:
        c_name=cl.text
        company_list.append(c_name)
            
    
    lst=soup.find_all('ul',class_='sjci-need')
    li1=[]
    li2=[]
    li3=[]
    for l in lst:
        li_tag=l.find_all('li')
        if(len(li_tag)==2):
          for i in range(0,2):
              if(i==0):
                li1.append(li_tag[i].text)
              else:
                li3.append(li_tag[i].text)
          li2.append("Not disclosed")      
        else:
          for i in range(0,3):
             if(i==0):
                li1.append(li_tag[i].text)
             elif(i==1):
                li2.append(li_tag[i].text)
             else:
                li3.append(li_tag[i].text)   

    
    for i in range(0,len(company_list)):
        role=role_list[i]
        c_name=company_list[i]
        lnk=l_list[i]
        exp=li1[i]
        ctc=li2[i]
        loc=li3[i]
        JobDetails.objects.create(company_name=c_name,role=role,link=lnk,ctc=ctc,location=loc,experience=exp)
        #print("created")
    
    
    role=request.GET.get('name')
    '''jd=JobDetails.objects.filter(role__icontains=role)
       paginator=Paginator(jd,8)
       page=request.GET.get('page')
       jd=paginator.get_page(page)
       return render(request,'home.html',{'jd':jd,'role':role})'''
       #jd.delete()
    '''else:
       jd=JobDetails.objects.all()
       paginator=Paginator(jd,8)
       page=request.GET.get('page')
       jd=paginator.get_page(page)
       #jd.delete()
       return render(request,'home.html',{'jd':jd})'''
    if role:
       jd=JobDetails.objects.filter(role__icontains=role)
    else:
       jd=JobDetails.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(jd,4)
    jd=paginator.page(page)
    return render(request,'home.html',{'jd':jd})



        

    





