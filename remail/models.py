from django.db import models
from django.contrib import admin


class Email(models.Model):
    subject = models.CharField(max_length=30)
    senders_email = models.EmailField()
    body = models.TextField()

    def __unicode__(self):
        return self.senders_email


class EmailAdmin(admin.ModelAdmin):
    list_display = ('senders_email', 'subject', 'body')
