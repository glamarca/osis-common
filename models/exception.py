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
from django.utils.translation import ugettext_lazy as _


class MultipleModelsSerializationException(Exception):
    def __init__(self, errors=None):
        message = _('Only objects from the same models are allowed')
        super(MultipleModelsSerializationException, self).__init__(message)
        self.errors = errors


class MigrationPersistanceError(Exception):
    def __init__(self, errors=None):
        message = _('Migration persistence error')
        super(MigrationPersistanceError, self).__init__(message)
        self.errors = errors


class OverrideSubClassError(Exception):
    def __init__(self, subclass_name, errors=None):
        message = _('%(subclass_name)s is not a sub-class').format(subclass_name=subclass_name)
        super(OverrideSubClassError, self).__init__(message)
        self.errors = errors


class OverrideMethodError(Exception):
    def __init__(self, function_name, super_classes_names, subclass_name, errors=None):
        message = _(
            '%(function_name)s is not a function of a super-class of %(subclass_name)s [%(super_classes_names)s]'
        ).format(
            function_name=function_name,
            subclass_name=subclass_name,
            super_classes_names=super_classes_names
        )
        super(OverrideMethodError, self).__init__(message)
        self.errors = errors
