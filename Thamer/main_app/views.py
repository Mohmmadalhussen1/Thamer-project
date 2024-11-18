
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login, logout
from .models import Company,Review, User,Contact
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.db.models import Avg



# Create your views here.
@login_required(login_url="/users/login/")

def add_company(request):
    if request.method == "POST":
        name = request.POST.get('name')
        sectors = request.POST.get('sectors')
        local_score = request.POST.get('local_score')
        pdf_file_local = request.FILES.get('pdf_file_local')
        ikteva_score_now = request.POST.get('ikteva_score_now')
        ikteva_score_before = request.POST.get('ikteva_score_before')
        pdf_file_ikteva = request.FILES.get('pdf_file_ikteva')
        description = request.POST.get('description', '')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')

        # Perform validation
        errors = []
        try:
            local_score = int(local_score)
        except ValueError:
            errors.append("Invalid value for Current local Content Score. Please enter a valid number.")

        try:
            ikteva_score_now = int(ikteva_score_now)
        except ValueError:
            errors.append("Invalid value for Current Iktva Score. Please enter a valid number.")

        try:
            ikteva_score_before = int(ikteva_score_before)
        except ValueError:
            errors.append("Invalid value for Last Year Iktva Score. Please enter a valid number.")

        if errors:
            return render(request, "main_app/add_company.html", {'errors': errors})

        # Continue with saving the company if validation passes
        new_company = Company(
            name=name,
            sectors=sectors,
            local_score=local_score,
            pdf_file_local=pdf_file_local,
            ikteva_score_now=ikteva_score_now,
            ikteva_score_before=ikteva_score_before,
            pdf_file_ikteva=pdf_file_ikteva,
            description=description,
            email=email,
            contact_number=contact_number,
            owner=request.user,
            status='pending'
        )

        new_company.save()
        return redirect("main_app:market_page")

    return render(request, "main_app/add_company.html")


def market_page(request:HttpRequest):

    #Show all data inside the model in MArket

        
    companys = Company.objects.filter(status='approved')


    return render(request, "main_app/market.html",  {"companys" : companys})





def company_detail(request:HttpRequest, company_id):

        #Show each  data inside the model in thier ID


    company = Company.objects.get(id=company_id)

    return render(request, 'main_app/company_detail.html', {"company" : company}) 

def profile_page(request:HttpRequest):

        #Show each  data inside the model in thier ID


    company = Company.objects.all()


    return render(request, 'main_app/profile_page.html', {"company" : company}) 


@login_required(login_url="/users/login/")
def update_company(request:HttpRequest, company_id):

    company = Company.objects.get(id=company_id)

    #updating the Company model
    if request.method == "POST":
        company.name=request.POST["name"]
        company.description = request.POST["description"]
        company.local_score=request.POST["local_score"]
        company.ikteva_score_now=request.POST["ikteva_score_now"]
        company.ikteva_score_before=request.POST["ikteva_score_before"]
        company.email=request.POST["email"]
        company.contact_number =request.POST["contact_number"]
        company.twitter_link = request.POST["twitter_link"]
        company.linkdin= request.POST["linkdin"]
        company.website = request.POST["website"]
        company.instagram_link = request.POST["instagram_link"]



        company.save()

        return redirect("main_app:company_detail", company_id=company.id)

    return render(request, 'main_app/update_company.html', {"company" : company})

@login_required(login_url="/users/login/")
def delete_company(request:HttpRequest, company_id):

    #Delete the company from the model 
    
    company = Company.objects.get(id=company_id)
    company.delete()

    return redirect("main_app:market_page")




def faq_page(request:HttpRequest):
    
# About us HTML
    return render(request, "main_app/faq_page.html")

def entry_page(request:HttpRequest):
    
# About us HTML
    return render(request, "main_app/entry_page.html")




def contact_us(request:HttpRequest):
    if request.method == "POST":
        
        newContact = Contact(name=request.POST['name'],email=request.POST['email'],subject=request.POST['subject'],message=request.POST['message'])
        newContact.save()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject= request.POST.get('subject')
        message = request.POST.get('message')
        
        form_data = {
            'name':name,
            'email':email,
            'subject':subject,
            'message':message,
        }
        message= '''
        New message:{}

        From: {}
        '''.format(form_data["message"], form_data["email"])
        send_mail(form_data["subject"],message,'fasialalhussin@gmail.com',['fasialalhussin@gmail.com'])

        return redirect("main_app:submit_done")
    return render(request, "main_app/contact_us.html") 



from django.shortcuts import render
from .models import Company

def index_page(request):
    # Fetch all companies
    companys = Company.objects.filter(status='approved')

    # Count the total number of companies
    total_companies = companys.count()

    average_ikteva_score = companys.aggregate(avg_ikteva_score=Avg('ikteva_score_now'))['avg_ikteva_score']
    average_ikteva_score = int(average_ikteva_score) if average_ikteva_score is not None else None
        # Calculate the average local_score
    average_local_score = companys.aggregate(avg_local_score=Avg('local_score'))['avg_local_score']

    # Convert to integer if the average is a whole number
    average_local_score = int(average_local_score) if average_local_score is not None else None


    
    return render(request, 'main_app/index.html', {"companys": companys, "total_companies": total_companies, "average_ikteva_score": average_ikteva_score,"average_local_score": average_local_score})


def dashboard_page(request:HttpRequest):
    
# Home HTML

    return render(request, "main_app/dashboard_page.html")



# Future feature

def add_review(request:HttpRequest, company_id):

    if request.method == "POST":
        company_object = Company.objects.get(id=company_id)
        new_review = Review(company=company_object, user=request.user, content=request.POST["content"], rating=request.POST["rating"])
        new_review.save()

    
    return redirect("main_app:company_detail", company_id=company_id)



def consultion_page(request:HttpRequest):
    
    # payment page HTML

    return render(request, "main_app/consultion_page.html")

def what_we_do(request:HttpRequest):
    
    # payment page HTML

    return render(request, "main_app/what_we_do_page.html")



def over_view(request:HttpRequest):

    # payment page HTML


    return render(request, "main_app/over_view.html")

@login_required(login_url="/users/login/")
def company_page(request:HttpRequest):
    # Retrieve companies associated with the currently logged-in user
    company = Company.objects.filter(owner=request.user)

    # Pass the companies variable to the template in the context dictionary
    return render(request, "main_app/my_compnies.html", {"company": company})


def onwer_details(request:HttpRequest, company_id):

        #Show each  data inside the model in thier ID


    company = Company.objects.get(id=company_id)

    return render(request, 'main_app/onwer_details.html', {"company" : company}) 

def submit_done(request:HttpRequest):

    return render(request,"main_app/submit_done.html")



