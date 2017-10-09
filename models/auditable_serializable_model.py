##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2017 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
import uuid
import logging
import json
import datetime
import time

from django.conf import settings
from django.contrib import admin, messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import DateTimeField, DateField
from django.core import serializers
from django.utils.encoding import force_text
from django.apps import apps
from osis_common.models import message_queue_cache
from osis_common.models.message_queue_cache import MessageQueueCache
from osis_common.models.serializable_model import serialize, serializable_model_post_change, \
    serializable_model_resend_messages_to_queue, wrap_serialization

from pika.exceptions import ChannelClosed, ConnectionClosed
from osis_common.models.exception import MultipleModelsSerializationException, MigrationPersistanceError
from osis_common.queue import queue_sender


LOGGER = logging.getLogger(settings.DEFAULT_LOGGER)


class AuditableSerializableQuerySet(models.QuerySet):
    # Called in case of bulk delete
    # Override this function is important to force to call the delete() function of a model's instance
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete()


class AuditableSerializableModelManager(models.Manager):
    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)

    def get_queryset(self):
        return AuditableSerializableQuerySet(self.model, using=self._db).exclude(deleted=True)


class AuditableSerializableModelAdmin(admin.ModelAdmin):
    actions = ['resend_messages_to_queue']

    def resend_messages_to_queue(self, request, queryset):
        serializable_model_resend_messages_to_queue(self, request, queryset)


class AuditableSerializableModel(models.Model):
    objects = AuditableSerializableModelManager()

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    deleted = models.BooleanField(null=False, blank=False, default=False)

    def save(self, *args, **kwargs):
        super(AuditableSerializableModel, self).save(*args, **kwargs)
        serializable_model_post_change(self)

    def delete(self, *args, **kwargs):
        super(AuditableSerializableModel, self).delete(*args, **kwargs)
        serializable_model_post_change(self)

    def natural_key(self):
        return [self.uuid]

    def __str__(self):
        return "{}".format(self.uuid)

    class Meta:
        abstract = True

    @classmethod
    def find_by_uuid(cls, uuid):
        try:
            return cls.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            return None
