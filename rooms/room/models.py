from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=500)
    roomno = models.CharField(max_length=20)
    rollno = models.CharField(max_length=20)
    phno = models.CharField(default="",max_length=30)
    def __unicode__(self):
        return self.name+", "+self.roomno

class Relationship(models.Model):
    from_person = models.ForeignKey(Person, related_name='from_person');
    to_person = models.ForeignKey(Person, related_name='to_person');
    def __unicode__(self):
        return self.from_person.name + "->" + self.to_person.name
