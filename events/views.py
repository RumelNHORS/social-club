from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
import calendar
import csv
from calendar import HTMLCalendar
from datetime import datetime
from . models import Event, Venue
from . forms import VenueForm, EventForm, EventFormAdmin
#Import PDF stuff
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
#Import Pegination stuff
from django.core.paginator import Paginator

#Show Events by Admin approval page
def show_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	# e = Event.objects.filter(approved=True)
	return render(request, 'events/show_event.html', {'event': event})

# Create Events By Venue page
def venue_events(request, venue_id):
	#Grabe The Venue
	venue = Venue.objects.get(id=venue_id)
	#Grabe the events from that venue
	events = venue.event_set.all()
	if events:
		context = {
			'events': events,
		}
		return render(request, 'events/venue_events.html', context)
	else:
		messages.success(request, ("That Venue Has No Event At This Time.."))
		return redirect('admin-approval')

#Create Admin Event Approval Page
def admin_approval(request):
	# Get Venue List
	venue_list = Venue.objects.all()

	#Get Count
	event_count = Event.objects.all().count()
	venue_count = Venue.objects.all().count()
	user_count = User.objects.all().count()

	event_list = Event.objects.all().order_by("-event_date")
	if request.user.is_superuser:
		if request.method == 'POST':
			id_list = request.POST.getlist('boxes')

			#uncheck all events
			event_list.update(approved=False)
			#Update The Database
			for x in id_list:
				Event.objects.filter(pk=int(x)).update(approved=True)

			messages.success(request, ("Event List Approved Has Been  Updated."))
			return redirect('list-events')


		else:
			context = {
				'event_list': event_list,
				'event_count': event_count,
				'venue_count': venue_count,
				'user_count': user_count,
				'venue_list': venue_list,

			}
			return render(request, 'events/admin_approval.html', context)
	else:
		messages.success(request, ("You aren't Authorized To View This Page!"))
		return redirect('home')
	return render(request, 'events/admin_approval.html')

#Create my Events Page
def my_events(request):
	if request.user.is_authenticated:
		me = request.user.id
		events = Event.objects.filter(attendess=me)

		context = {
			'events': events
		}
		return render(request, 'events/my_events.html', context)

	else:
		messages.success(request,("You aren't Authorized to View This Page! Please Register or Login to View This Page"))
		return redirect('home')

#generate a view for pdf file
def venue_pdf(request):
	#Create a Bytestrim
	buf = io.BytesIO()
	#Create a canvase
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)	
	#Create a Text object
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont('Helvetica', 10)

	#Add some lines of text
	#lines = [
	#	'This is line 1',
	#	'This is line 1',
	#	'This is line 1',
	#]

	#Designet The Model
	venues = Venue.objects.all()

	#Creat a blank list
	lines = []

	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.Zip_code)
		lines.append(venue.phone)
		lines.append(venue.web)
		lines.append(venue.email_address)
		lines.append('==========')


	#loop here
	for line in lines:
		textob.textLine(line)

	#Finish up
	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	#Return something
	return FileResponse(buf, as_attachment=True, filename='venue.pdf')


# Generate Text file venue list
def venue_csv(request):
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=venue.csv'
	#create a csv weiter
	writer = csv.writer(response)

	#Designet The Model
	venues = Venue.objects.all()

	#Add column heading to the csv file
	writer.writerow(['Vanue Name', 'Address', 'Zip Code', 'Phone',' Web Address','Email'])

	#looping for output
	for venue in venues:
		writer.writerow([venue.name,venue.address,venue.Zip_code,venue.phone,venue.web,venue.email_address])

	return response

# venue text file
def venue_text(request):
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=venue.text'
	#Designet The Model
	venues = Venue.objects.all()

	#Creat a blank list
	lines = []

	#looping for output
	for venue in venues:
		lines.append(f'{venue.name}\n{venue.address}\n{venue.Zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n')

	#lines = ['This is Line 1\n',
	#'This is line 2\n',
	#'This is line 3\n']

	#Write to Textfile
	response.writelines(lines)
	return response

#Event list here
def all_events(request):
	event_list = Event.objects.all().order_by('-event_date')
	#Pagination here
	p = Paginator(Event.objects.all(), 3)
	page = request.GET.get('page')
	events = p.get_page(page)
	nums = 'a' * events.paginator.num_pages

	context = {
		'event_list': event_list,
		'events': events,
		'nums': nums,
		}

	return render(request, 'events/event_list.html', context)

#Search Event to the page
def search_events(request):
	if request.method == 'POST':
		searched = request.POST['searched']
		events = Event.objects.filter(name__contains=searched)

		context = {
			'searched': searched,
			'events': events
		}
		return render(request, 'events/search_events.html', context)
	else:
		return render(request, 'events/search_events.html',{})

#Search venue to the page
def search_venues(request):
	if request.method == 'POST':
		searched = request.POST['searched']
		venues = Venue.objects.filter(name__contains=searched)
		return render(request, 'events/search_venues.html', 
			{'searched': searched, 'venues': venues})
	else:
		return render(request, 'events/search_venues.html',{})

#Add new venue
def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST, request.FILES)
		if form.is_valid():
			venue = form.save(commit=False)
			venue.owner = request.user.id
			venue.save()
			#form.save()
			return HttpResponseRedirect('/add_venue?submitted=True')
	else:
		form = VenueForm
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'events/add_venue.html', {'form':form, 'submitted':submitted})

# All venue List here
def list_venues(request):
	venue_list = Venue.objects.all().order_by('name')
	#Pagination here
	p = Paginator(Venue.objects.all(), 5)
	page = request.GET.get('page')
	venues = p.get_page(page)
	nums = 'a' * venues.paginator.num_pages

	context = {
		'venue_list': venue_list,
		'venues': venues,
		'nums': nums,
	}

	return render(request, 'events/venue.html', context)

#Show all the venue
def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	
	#Grabe the events from that venue
	events = venue.event_set.all()
	venue_owner = User.objects.get(pk=venue.owner)
	return render(request, 'events/show_venue.html', {
		'venue': venue,
		'venue_owner': venue_owner,
		'events': events,
		})
#Venue Update section
def update_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
	if form.is_valid():
		form.save()
		return redirect('list-venues')
	return render(request, 'events/update_venue.html', {
		'venue': venue,
		'form': form
		})
#Add new event
def add_event(request):
	submitted = False
	if request.method == "POST":
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/add_event?submitted=True')
		else:
			form = EventForm(request.POST)
			if form.is_valid():
				#form.save()
				event = form.save(commit=False)
				event.manager = request.user
				event.save()
				return HttpResponseRedirect('/add_event?submitted=True')		
			
	else:
		#Just going to the page, not submitting
		if request.user.is_superuser:
			form = EventFormAdmin
		else:
			form = EventForm

		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'events/add_event.html', {'form':form, 'submitted':submitted})

#Update the event here
def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user.is_superuser:
		form = EventFormAdmin(request.POST or None, instance=event)
	else:
		form = EventForm(request.POST or None, instance=event)
	if form.is_valid():
		form.save()
		return redirect('list-events')
	return render(request, 'events/update_event.html', {
		'event': event,
		'form': form,
		})

#Delete event from the database
def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user == event.manager:
		event.delete()
		messages.success(request,('Event Deleted !!'))
		return redirect('list-events')

	else:
		messages.success(request,("You aren't Authorized to Delet This Event !"))
		return redirect('list-events')

#Delete venue from the database
def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue.delete()
	return redirect('list-venues')

# The Home page is here
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	name = "Rumel"
	month = month.capitalize()
	#Convert month name to number
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)
	#Creat a calendar
	cal = HTMLCalendar().formatmonth(year, month_number)
	#Get crrunt year
	now = datetime.now()
	crrunt_year = now.year

	#Quary the events model for dates
	event_list = Event.objects.filter(
		event_date__year = year,
		event_date__month = month_number
		)

	#Get Crrunt Time
	time = now.strftime('%I: %M %p')
	return render(request, 'events/home.html', {
		'first_name': name,
		'year': year,
		'month' : month,
		'month_number' : month_number,
		'cal': cal,
		'crrunt_year': crrunt_year,
		'time': time,
		'event_list': event_list,
		})