from django.shortcuts import render,redirect
from .forms import ExpenseForm, UserRegistrationForm
from .models import Expense
import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def index(request):
    if request.method =="POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            # expense.save()
            new_expense = expense.save(commit=False)
            new_expense.creator = request.user
            # new_expense.date = datetime.date(2024, 2, 15)
            new_expense.save()
            return redirect('index')

    expenses = Expense.objects.filter(creator = request.user)
    total_expenses = expenses.aggregate(Sum('amount'))
    

    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(creator=request.user, date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))
    

    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expense.objects.filter(creator=request.user, date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))
    

    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = Expense.objects.filter(creator=request.user, date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))
    
    daily_sums = Expense.objects.filter(creator=request.user).values('date').order_by('date').annotate(sum=Sum('amount'))
    
    
    categorical_sums = Expense.objects.filter(creator=request.user).values('category').order_by('category').annotate(sum=Sum('amount'))
    print(categorical_sums)
    
    expense_form = ExpenseForm()
    return render(request,'myapp/index.html',{'expense_form':expense_form,'expenses':expenses,'total_expenses':total_expenses,'yearly_sum':yearly_sum,'weekly_sum':weekly_sum,'monthly_sum':monthly_sum,'daily_sums':daily_sums,'categorical_sums':categorical_sums})

@login_required(login_url='login')
def edit(request,id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    if request.method =="POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
        
    return render(request,'myapp/edit.html',{'expense_form':expense_form})

@login_required(login_url='login')
def delete(request,id):
    if request.method =='POST' and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, 'Konto zostało utworzone pomyślnie!')
            return redirect('index')
    else:
        user_form = UserRegistrationForm()

    for field, errors in user_form.errors.items():
        for error in errors:
            messages.error(request, f"{field}: {error}")

    return render(request, 'myapp/register.html', {'user_form': user_form})
    
def expense_history(request):
    expenses = Expense.objects.order_by('-date')  # Sortowanie od najnowszych
    return render(request, 'myapp/expense_history.html', {'expenses': expenses})