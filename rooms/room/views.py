from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from room.models import Person, Relationship
from django.views.decorators.csrf import csrf_exempt
import json, re
import requests

def login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')
        r = requests.get("http://www.cse.iitb.ac.in/~arunb/ldap.php?user="+uname+"&pass="+passwd).text
        if re.match('.*rollno":"(.*)","name":"(.*)"',r) != None:
            request.session['rollno'] = re.match('.*rollno":"(.*)","name":"(.*)"',r).group(1)
            request.session['uname'] = re.match('.*rollno":"(.*)","name":"(.*)"',r).group(2)
            return HttpResponseRedirect('/insertPerson/')
        else:
            request.session['rollno'] = None
            request.session['uname'] = None
            return HttpResponseRedirect('/login/')
    return render(request, 'login.html')

def insertPerson(request):
    if request.session['uname'] == None:
        return HttpResponseRedirect('/login/')
    name = request.session['uname']
    rollno = request.session['rollno']
    roomno = ""
    r = None
    if len(Person.objects.filter(rollno=rollno)) != 0:
        a = Person.objects.get(rollno = rollno)
        r = Relationship.objects.filter(from_person=a)
    if request.method == 'POST':
        roomno = request.POST.get('roomno')
        if len(Person.objects.filter(roomno=roomno)) == 0:
            a = Person(name=name, roomno=roomno, rollno=rollno)
            a.save()
        for room in [x.strip() for x in request.POST.getlist('roomsarray[]')]:
            b = Person.objects.get(roomno = room)
            Relationship(from_person = a, to_person = b).save()
        return HttpResponseRedirect('/insertPerson/')
    if r != None:
        return render(request, 'getPersonDetails.html', {'name':name,'rollno':rollno,'roomno':a.roomno,'relns':r})
    return render(request, 'getPersonDetails.html', {'name':name,'rollno':rollno,'roomno':""})

def success(request):
    return HttpResponse("hey")

def getRooms(request):
    rooms = [x.strip() for x in Person.objects.all().values_list('roomno', flat=True)]
    return HttpResponse(json.dumps(rooms))
