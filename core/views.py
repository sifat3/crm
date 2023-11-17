from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from django.db.models import Q



def home(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        invoice = (request.POST['invoice'].strip()).lower()
        problem = request.POST['problem']
        date =  datetime.now().strftime("%m/%d/%Y")
        if Completed_Project.objects.filter(invoice=invoice):
            project = Completed_Project.objects.get(invoice=invoice)
            if int(project.warranty.year) >= int(datetime.now().strftime("%Y")) and int(project.warranty.month) >= int(datetime.now().strftime("%m")) and int(project.warranty.day) >= int(datetime.now().strftime("%d")):
                token = Token.objects.create(name=name, email=email, invoice=invoice, problem=problem)
                token.save()
                messages.success(request, "We have recieved your message. We will fix the issue as soon as possible. You can see the status of your request on the STATUS section.")
                mail("NEW TOKEN ADDED", f"INVOICE: {invoice}, \n ISSUE: {problem}. Freelancers: {[project.freelancer_linkedIn]}", ['info@ibizn.com'])
                mail("REQUEST RECIEVED", f"We have recieved your request.\nAnd currently working on.\nThanks for your patience.\nIBIZN", [email])
        
            else:
                messages.success(request, "Sorry, Your warranty period is over, Please contact info@ibizn.com")
        else:
            messages.success(request, "Invalid invoice id")
        
    return render(request, 'core/home.html')


def status(request):
    pg = 0
    context = {
        "pg": pg,
    }
    if request.method == "POST":
        invoice = request.POST['invoice']
        tokens = Token.objects.filter(invoice=invoice)
        if tokens:
            pg += 1 
            context = {
            "tokens" : tokens,
            "pg" : pg
            }
        else:
            messages.success(request, "No TOKEN found")
        
    return render(request, 'core/status.html', context)


def mail(mail_subject, mail_body, to):
    subject = mail_subject
    message = mail_body
    from_email = 'admin@ibizn.com'
    recipient_list = to

    send_mail(subject, message, from_email, recipient_list)


def backend(request):
    completed_projects = Completed_Project.objects.filter(created__range=[datetime.now()-relativedelta(days=30), datetime.now()])
    profit = 0
    for i in completed_projects:
        profit += i.profit
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect('backend')
        else:
            messages.success("Invalid Username or Password")
    
    tokens = Token.objects.filter(solved=False)
    projects = Ongoing_project.objects.all()

    return render(request, 'core/backend.html', {"tokens": tokens, "projects": projects, 'profit': profit})

@login_required(login_url='backend')
def logout_user(request):
    logout(request)
    return redirect('backend')

@login_required(login_url='backend')
def solved(request, pk):
    token = Token.objects.get(invoice=pk)
    token.solved = True
    mail("ISSUE SOLVED", f"Dear {token.name} | INVOICE: {token.invoice},\n We succesfully resolved your issue.\n Please check. And if there still any issue left please contact at info@ibizn.com\n Thank you for staying with us.\n Ibizn", [token.email])
    token.save()
    return redirect('backend')


@login_required(login_url='backend')
def completed(request, pk):
    project = Ongoing_project.objects.get(invoice=pk)
    if project.due_amount <= 0:
        freelancers = project.freelancers.all()
        url = [i.linkedin for i in freelancers]
        email = [i.email for i in freelancers]
        complete_project = Completed_Project.objects.create(invoice=project.invoice, client=project.client, bill=project.bill, cost=project.cost, profit=project.profit, delivery_date=datetime.now(), warranty=datetime.now()+relativedelta(months=6), freelancer_linkedIn=url, freelancer_email=email)
        complete_project.save()
        project.delete()
    else:
        messages.success(request, "This Project's Bill is not paid yet. Can't Mark as comlete")
    return redirect('backend')


@login_required(login_url='backend')
def make_payment(request):
    if request.method == 'POST':
        invoice = (request.POST['invoice'].strip()).lower()
        amount = int(request.POST['amount'])
        project = Ongoing_project.objects.get(invoice=invoice)
        if request.POST['payment'] == 'cost':
            project.cost = project.cost + amount 
            project.profit = project.bill - project.cost
        elif request.POST['payment'] == 'payment1':
            project.first_payment = project.first_payment + amount
            project.due_amount = project.bill - (project.first_payment + project.second_payment + project.third_payment)
        elif request.POST['payment'] == 'payment2':
            project.second_payment = project.second_payment + amount
            project.due_amount = project.bill - (project.first_payment + project.second_payment + project.third_payment)
        else:
            project.third_payment = project.third_payment + amount
            project.due_amount = project.bill - (project.first_payment + project.second_payment + project.third_payment)
        project.save()
        return redirect('backend')
    return render(request, 'core/payment.html')


@login_required(login_url='backend')
def completed_projects(request):
    projects = Completed_Project.objects.all()
    profit = 0
    for i in projects:
        profit += i.profit
    return render(request ,'core/projects.html', {"projects":projects, 'profit': profit})

@login_required(login_url='backend')
def add_project(request):
    clients = Client.objects.all()
    if request.method == 'POST':
        invoice = (request.POST['invoice'].strip()).lower()
        client_id = request.POST['client']
        client = Client.objects.get(id=client_id)
        bill = request.POST['bill']
        delivery_date = request.POST['estimated_delivery_date']
        new_project = Ongoing_project.objects.create(invoice=invoice, client=client, bill=bill, cost=0, profit=bill, estimated_delivery_date=delivery_date, due_amount=bill)
        new_project.save()
        return redirect('backend')

    return render(request, 'core/add_project.html', {'clients': clients})

@login_required(login_url='backend')
def add_freelancer(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        linkedin = request.POST['linkedin']
        skill = request.POST['skill']
        if Freelancer.objects.filter(email=email):
            messages.success(request, "Email already exists")
            return redirect('backend')
        else:
            new_freelancer = Freelancer.objects.create(name=name, email=email, phone=phone, linkedin=linkedin, skill=skill)
            new_freelancer.save()
            return redirect('backend')
    return render(request, 'core/add_freelancer.html')

@login_required(login_url='backend')
def show_freelancers(request):
    query = request.GET.get('q')
    freelancers = Freelancer.objects.all()
    if query:
        freelancers = freelancers.filter(
            Q(name__icontains=query) | Q(skill__icontains=query)
        )

    projects = Ongoing_project.objects.all()
    if request.method == 'POST':
        project_id = request.POST['project']
        project = Ongoing_project.objects.get(id=project_id)
        freelancer_id = request.POST['freelancer']
        freelancer = Freelancer.objects.get(id=freelancer_id)
        freelancer.project = project
        earning = int(request.POST['amount'])
        freelancer.due_amount += earning
        project.cost += earning
        project.profit -= earning
        freelancer.save()
        project.save()
    return render(request, 'core/show_freelancers.html', {'freelancers': freelancers, 'projects': projects})

@login_required(login_url='backend')
def pay_freelancer(request, pk):
    freelancer = Freelancer.objects.get(id=pk)
    if freelancer.due_amount > 0:
        freelancer.total_earned += freelancer.due_amount
        freelancer.due_amount = 0
        freelancer.save()
        messages.success(request, "Marked As Paid.")
        return redirect('show_freelancers')
    else:
        messages.success(request, "It's already paid.")
        return redirect('show_freelancers')

@login_required(login_url='backend')
def add_client(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        if Client.objects.filter(email=email):
            messages.success(request, "Email already exists")
            return redirect('backend')
        else:
            client = Client.objects.create(name=name, email=email, phone=phone)
            client.save()
            messages.success(request, 'Client creation successfull')
            return redirect('backend')
    return render(request, 'core/add_client.html')