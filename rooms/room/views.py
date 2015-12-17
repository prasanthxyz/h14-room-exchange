from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from room.models import Person, Relationship
from django.views.decorators.csrf import csrf_exempt
import json, re
import requests
import ldap
from django_auth_ldap.config import LDAPSearch
from django.contrib.auth import authenticate, login

def logout(request):
    request.session['rollno'] = None
    request.session['uname'] = None
    return HttpResponseRedirect('/login/')

#def login(request):
#    if request.session.get('uname', None) != None:
#        return insertPerson(request)
#
#    if request.method == 'POST':
#        uname = request.POST.get('uname')
#        passwd = request.POST.get('passwd')
#        AUTH_LDAP_BIND_DN = ""
#        AUTH_LDAP_BIND_PASSWORD = passwd
#        AUTH_LDAP_USER_SEARCH = LDAPSearch("dc=iitb,dc=ac,dc=in",ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
#        user = authenticate(username=uname, password=passwd)
#        if user is not None:
#            login(request, user)
#            state = "Valid account"
#        else:
#            state = "Inactive account"
#        print state
#        #ldap.SCOPE_SUBTREE, "(uid="+uname+")")
#    return render(request, 'login.html', {'errorclass':'hidden'})


def login(request):
    if request.session.get('uname', None) != None:
        return insertPerson(request)

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
            return HttpResponseRedirect('/login/retry/')
    return render(request, 'login.html', {'errorclass':'hidden'})

def retrylogin(request):
    return render(request, 'login.html')

def insertPerson(request):
    if request.session['uname'] == None:
        return HttpResponseRedirect('/login/')

    name = request.session['uname']
    rollno = request.session['rollno']

    objects = Person.objects.filter(rollno=rollno)
    if len(objects) != 1:
        current_person = Person(name=name, rollno=rollno)
        current_person.save()
    else:
        current_person = objects[0]

    relationships_to_me = Relationship.objects.filter(to_person=current_person)

    matches = getMatches(current_person)

    if request.method == 'POST':
        roomno = request.POST.get('roomno').strip()
        phno = request.POST.get('phno').strip()
        if roomno == "":
            return HttpResponseRedirect('/insertPerson/')

        current_person.roomno = roomno
        current_person.phno = phno
        current_person.save()

        needed_rooms_list = request.POST.getlist('roomsarray[]')
        relationships_from_me = Relationship.objects.filter(from_person=current_person)
        for e in relationships_from_me:
            if e.to_person not in needed_rooms_list:
                e.delete()

        for room in [x.strip() for x in needed_rooms_list]:
            b = Person.objects.get(roomno = room)
            if len(Relationship.objects.filter(from_person = current_person, to_person = b)) == 0:
                Relationship(from_person = current_person, to_person = b).save()

        return HttpResponseRedirect('/insertPerson/')
    return render(request, 'getPersonDetails.html', {'person': current_person, 'relns':relationships_to_me, 'matches':matches})

def success(request):
    return HttpResponse("hey")

def getRooms(request):
    rollno = request.session['rollno']
    if rollno == None:
        return HttpResponse("")

    person = Person.objects.filter(rollno=rollno)
    if len(person) != 1:
        return HttpResponse("")

    a = Person.objects.get(rollno=rollno)
    needed = [x.to_person.roomno for x in Relationship.objects.filter(from_person=a)]
    rooms = []
    for p in Person.objects.all():
        if p.rollno.strip() == rollno:
            continue
        if p.roomno.strip() == "":
            continue
        if p.roomno.strip() in needed:
            checked = "yes"
        else:
            checked = "no"
        rooms.append((p.roomno.strip(), checked, p.name.strip().title()))
    return HttpResponse(json.dumps(rooms))

def profile(request, rollno):
    error = False
    current_person = None
    person = Person.objects.filter(rollno=rollno)
    if len(person) != 1:
        error = True
    else:
        current_person = Person.objects.get(rollno=rollno)
    return render(request, 'profile.html', {'error':error,'person':current_person})

def getMatches(current_person):
    persons_i_am_interested = [x.to_person for x in Relationship.objects.filter(from_person=current_person)]
    persons_interested_in_me = [x.from_person for x in Relationship.objects.filter(to_person=current_person)]
    matches = list(set(persons_i_am_interested).intersection(persons_interested_in_me))
    return matches
"""
    
    needed = [x.to_person.roomno for x in Relationship.objects.filter(from_person=a)]
    rooms = []
    for p in Person.objects.all():
        if p.rollno.strip() == rollno:
            continue
        if p.roomno.strip() == "":
            continue
        if p.roomno.strip() in needed:
            checked = "yes"
        else:
            checked = "no"
        rooms.append((p.roomno.strip(), checked, p.name.strip().title()))
    return HttpResponse(json.dumps(rooms))
"""

def about(request):
    return render(request, 'about.html')
