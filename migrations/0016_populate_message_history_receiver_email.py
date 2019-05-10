# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-26 12:56
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import migrations


def populate_message_history_receiver_email(apps, schema_editor):
    Person = apps.get_model("base", "Person")
    MessageHistory = apps.get_model("osis_common", "MessageHistory")
    message_history_items = MessageHistory.objects.all()
    for item in message_history_items:
        try:
            if _detect_inconsistent_item(item):
                # items where item.receiver_id is user.id
                user = User.objects.get(pk=item.receiver_id)
                item.receiver_email = user.email
            else:
                # items where item.receiver_id is person.id
                person = Person.objects.get(pk=item.receiver_id)
                if person.email:
                    item.receiver_email = person.email
                elif person.user.email:
                    item.receiver_email = person.user.email
            item.save()
        except (User.DoesNotExist, Person.DoesNotExist, AttributeError):
            pass


def _detect_inconsistent_item(item):
    return 'IUFC - Nouvelle demande d' in item.subject


class Migration(migrations.Migration):
    dependencies = [
        ('osis_common', '0015_messagehistory_receiver_email'),
    ]

    operations = [
        migrations.RunPython(populate_message_history_receiver_email),
    ]