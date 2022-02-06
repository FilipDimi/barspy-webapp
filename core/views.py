from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from core import models
import datetime


def index(request):
    all_drinks = models.Drink.objects.all()
    all_categories = models.Category.objects.all()
    dateNow = datetime.datetime.now()
    dateNow = str(dateNow.strftime("%Y-%m-%d"))

    try:
        findDateInHistory = models.History.objects.get(date=dateNow)
    except ObjectDoesNotExist:
        newDate = models.History()
        newDate.date = str(dateNow)
        newDate.save()

    today_history = models.History.objects.last()
    today_transaction = models.Transaction.objects.filter(date=today_history)

    passing_dict = {
        "all_drinks": all_drinks,
        "all_categories": all_categories,
        "today_transaction": today_transaction,
        "dateNow": dateNow
    }
    return render(request, 'core/index.html', passing_dict)


@login_required(login_url="")
@user_passes_test(lambda u: u.is_superuser)
def adminPanel(request):
    bartenders = User.objects.all()
    last_checkin = models.CheckIn.objects.latest('pk')
    categories = models.Category.objects.all()
    subcategories = models.SubCategory.objects.all()

    passing_dict = {'bartenders': bartenders, 'last_checkin': last_checkin, 'categories': categories, 'subcategories': subcategories}
    return render(request, 'core/admin.html', passing_dict)


@login_required(login_url="")
def history(request):
    history = models.History.objects.all().order_by('-id')

    passing_dict = {
        'history': history
    }
    return render(request, 'core/history.html', passing_dict)


@login_required(login_url="")
def transactions_per_day(request, pk):
    history_date = models.History.objects.get(pk=pk)
    daily_transactions = models.Transaction.objects.filter(date=history_date)
    bartenders = []

    for trans in daily_transactions:
        if trans.bartender.first_name not in bartenders:
            bartenders.append(trans.bartender.first_name)

    passing_dict = {
        'daily_transactions': daily_transactions,
        'history_date': history_date,
        'bartenders': bartenders
    }
    return render(request, 'core/daily_transactions.html', passing_dict)


@login_required(login_url="")
def inventory(request):
    all_drinks = list(models.Drink.objects.all())
    all_categories = models.Category.objects.all()
    all_subcategories = models.SubCategory.objects.all()

    for i in range(len(all_drinks)):
        for j in range(0, len(all_drinks) - i - 1):
            if all_drinks[j].inStock > all_drinks[j + 1].inStock:
                all_drinks[j], all_drinks[j + 1] = all_drinks[j + 1], all_drinks[j]

    passing_dict = {
        "all_drinks": all_drinks,
        "all_categories": all_categories,
        "all_subcategories": all_subcategories
    }
    return render(request, 'core/inventory.html', passing_dict)


@login_required(login_url="")
def checkin(request):
    all_drinks = models.Drink.objects.all()
    all_checkin = models.CheckIn.objects.all().order_by('-pk')
    all_dates = models.History.objects.all().order_by('-pk')
    checkinDates = []

    if len(all_checkin) > 4:
        all_checkin = all_checkin[:5]

    for date in all_dates:
        for check in all_checkin:
            if check.history == date:
                checkinDates.append(date)
                break

    passing_dict = {'all_drinks': all_drinks, 'all_checkin': all_checkin, 'all_dates': all_dates, 'checkinDates': checkinDates}
    return render(request, 'core/checkin.html', passing_dict)


@login_required(login_url="")
def add_checkin(request):
    if request.method == 'POST':
        if not request.POST['checkinalcohol'] or not request.POST['newqty']:
            return redirect('checkin')

        findAlcohol = request.POST['checkinalcohol'].split("#")[1]

        dateNow = datetime.datetime.now()
        dateNow = dateNow.strftime("%Y-%m-%d")

        try:
            findDateInHistory = models.History.objects.get(date=dateNow)
        except ObjectDoesNotExist:
            newDate = models.History()
            newDate.date = str(dateNow)
            newDate.save()


        drink = models.Drink.objects.get(pk=findAlcohol)
        new_checkin = models.CheckIn()

        new_checkin.drink = drink
        new_checkin.history = models.History.objects.get(date=findDateInHistory)
        new_checkin.inStockOld = drink.inStock
        new_checkin.inStockNew = request.POST['newqty']

        drink.inStock = request.POST['newqty']

        new_checkin.save()
        drink.save()



    return redirect('checkin')


@login_required(login_url="")
def checkinDetails(request, pk):
    date = models.History.objects.get(pk=pk)
    checkins = models.CheckIn.objects.filter(history=date).order_by('-pk')

    passing_dict = {'checkins': checkins, 'date': date }
    return render(request, 'core/checkindetails.html', passing_dict)


@login_required(login_url="")
def add_transaction(request):
    if request.method == 'POST':
        if not request.POST['instockchange'] or not request.POST['stockalcohol'].split("#")[1]:
            return redirect('index')

        changeInstock = request.POST['instockchange']
        findAlcohol = request.POST['stockalcohol'].split("#")[1]

        drink = models.Drink.objects.get(pk=findAlcohol)

        dateNow = datetime.datetime.now()
        dateNow = dateNow.strftime("%Y-%m-%d")

        try:
            findDateInHistory = models.History.objects.get(date=dateNow)
        except ObjectDoesNotExist:
            newDate = models.History()
            newDate.date = str(dateNow)
            newDate.save()

        newTransaction = models.Transaction()
        newTransaction.bartender = request.user
        newTransaction.date = models.History.objects.get(date=findDateInHistory)
        newTransaction.drink = drink
        newTransaction.change = changeInstock
        newTransaction.save()

        drink.inStock += int(changeInstock)
        if drink.inStock < 0:
            drink.inStock = 0

        if int(changeInstock) > 0:
            drink.emergencyNotification = True

        drink.save()

        return redirect('index')
    else:
        return redirect('index')


@login_required(login_url="")
def send_report(request):
    all_users = User.objects.all()
    user_emails = []
    dateNow = datetime.datetime.now()
    dateNow = str(dateNow.strftime("%Y-%m-%d"))
    history_date = models.History.objects.get(date=dateNow)
    daily_transactions = models.Transaction.objects.filter(date=history_date)
    all_drinks = models.Drink.objects.all()

    # Emergency Feature
    critical_drinks = []
    emergency_message = "BAR SPY NOTICE THAT WE ARE LOW ON THESE SPIRITS.\n"
    emergency_message += "---------------------\n\n"

    for drink in all_drinks:
        if (drink.inStock <= drink.emergencyNumber) and drink.emergencyNotification:
            critical_drinks.append(drink)

    for drink in critical_drinks:
        emergency_message += "{} ".format(drink.name)
        emergency_message += "{} \n".format(drink.inStock)

    # Daily Transaction
    bartenders = []
    transaction_subject = "Bar Spy Daily Changes"
    transaction_message = "Today's Transaction\n"
    transaction_message += "---------------------\n\n"

    for transaction in daily_transactions:
        transaction_message += "{}:\n".format(transaction.drink.name)
        transaction_message += "\tIn Stock: {}\n".format(transaction.drink.inStock)
        transaction_message += "\tDaily Update: {}\n\n".format(transaction.change)

        if transaction.bartender.first_name not in bartenders:
            bartenders.append(transaction.bartender.first_name)
    transaction_message += "Stocking made by {}".format(bartenders)

    for user in all_users:
        user_emails.append(user.email)

    emergency_subject = 'Bar Spy Critical'
    sender = 'f_dimitrievski@outlook.com'
    receiver = user_emails

    if critical_drinks:
        send_mail(emergency_subject, emergency_message, sender, receiver)
    send_mail(transaction_subject, transaction_message, sender, receiver)

    return redirect('index')


@login_required(login_url="")
@user_passes_test(lambda u: u.is_superuser)
def send_alert(request):
    subject = request.POST['subject']
    msg = request.POST['message']

    if not subject or not msg:
        return redirect('adminPanel')

    all_users = User.objects.all()
    user_emails = []

    for user in all_users:
        user_emails.append(user.email)

    sender = 'f_dimitrievski@outlook.com'
    receiver = user_emails

    send_mail(subject, msg, sender, receiver)
    return redirect('adminPanel')



@login_required(login_url="")
def toggleEmergency(request, pk):
    drink = models.Drink.objects.get(pk=pk)

    if drink.emergencyNotification == False:
        drink.emergencyNotification = True
    else:
        drink.emergencyNotification = False

    drink.save()

    return redirect('inventory')


@login_required(login_url="")
@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    if request.method == 'POST':
        if not request.POST['cat_name']:
            return redirect('adminPanel')

        new_category = models.Category()
        new_category.name = request.POST['cat_name']
        new_category.save()
        return redirect('adminPanel')
    else:
        return redirect('adminPanel')


@login_required(login_url="")
@user_passes_test(lambda u: u.is_superuser)
def add_sub(request):
    if request.method == 'POST':
        if not request.POST['subcat_name'] or not request.POST['cat_fk']:
            return redirect('adminPanel')

        new_sub = models.SubCategory()
        new_sub.name = request.POST['subcat_name']
        new_sub.subcategory = models.Category.objects.get(name=request.POST['cat_fk'])
        new_sub.save()

        return redirect('adminPanel')
    else:
        return redirect('adminPanel')


@login_required(login_url="")
@user_passes_test(lambda u: u.is_superuser)
def add_drink(request):
    if request.method == 'POST':
        if not request.POST['dri_name'] or not request.POST['dri_cat'] or not request.POST['dri_sub'] or not request.POST['qty'] or not request.POST['eme_num']:
            return redirect('adminPanel')

        new_drink = models.Drink()
        new_drink.name = request.POST['dri_name']
        new_drink.category = models.Category.objects.get(name=request.POST['dri_cat'])
        new_drink.subCategory = models.SubCategory.objects.get(name=request.POST['dri_sub'])
        new_drink.inStock = request.POST['qty']
        new_drink.emergencyNumber = request.POST['eme_num']
        new_drink.save()

        return redirect('adminPanel')
    else:
        return redirect('adminPanel')



def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'core/index.html', {"error": "The Bartender doesn't exists!"})
    else:
        return render(request, 'core/index.html')
