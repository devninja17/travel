from django.shortcuts import render, HttpResponse, redirect
from .models import User, Trip
from django.contrib import messages
import bcrypt

def index(request):
    if request.method == "POST": #Register user on POST
        errors = User.objects.validate_reg(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/main')
        else:
            found_users = User.objects.filter(username=request.POST['username'])
            if found_users.count() > 0:
                messages.error(request, "Sorry, this username had previously registered.", extra_tags="username")
                return redirect('/main')
            else:
                hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                created_user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed_pw)
                request.session['user_id'] = created_user.id
                request.session['user_name'] = created_user.name
                return redirect('/travels')
    return render(request, 'travelbuddy/index.html')

def login(request):
	found_users = User.objects.filter(username=request.POST['username'])
	if found_users.count() > 0:
		found_user = found_users.first()
		if bcrypt.checkpw(request.POST['password'].encode(), found_user.password.encode()) == True:
			request.session['user_id'] = found_user.id
			request.session['user_name'] = found_user.name
			print found_user
			return redirect('/travels')
		else:
			messages.error(request, "Login Failed, incorrect password", extra_tags="password")
			return redirect('/')
	else:
		messages.error(request, "Login Failed, username is not registered", extra_tags="username")
		return redirect('/')

def travels(request):
    myTrip = User.objects.get(id=request.session['user_id']).m2m_trips
    otherTrip = Trip.objects.exclude(user_id=request.session['user_id'])

    context = {
        "my_schedules": myTrip.all(),
        "other_schedules": otherTrip.all()
    }
    return render(request, 'travelbuddy/travels.html', context)

def addplan(request):
    if request.method == "POST":
        created_trip = Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], travelDateFrom=request.POST['travelDateFrom'], travelDateTo=request.POST['travelDateTo'], user_id=request.session['user_id'])
        request.session['trip_id'] = created_trip.id
        request.session['trip_destination'] = created_trip.destination
        return redirect('/travels')
    return render(request, 'travelbuddy/addtrip.html')

def destination(request, trip_id):
    context = {
        "destination": Trip.objects.get(id=trip_id)
    }
    return render(request, 'travelbuddy/destination.html', context)

def join_trip(request, trip_id):
    the_trip = Trip.objects.get(id=trip_id)
    the_user = User.objects.get(id=request.session['user_id'])
    the_trip.travelers.add(the_user)
    return redirect('/travels')

def logout(request):
    request.session['user_id'] = 0
    return redirect('/')