# Src: https://github.com/toastdriven/django-tastypie/blob/master/tastypie/compat.py
# Note: Appending original license in file itself. License files are hard :(.
#
# Copyright (c) 2010, Daniel Lindsley
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the tastypie nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL tastypie BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import unicode_literals
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import django

__all__ = ['get_user_model',]

# Django 1.5+ compatibility
def get_user_model():
    if django.VERSION >= (1, 5):
        try:
            from django.contrib import auth
            return auth.get_user_model()
        except ImproperlyConfigured:
            # The the users model might not be read yet.
            # This can happen is when setting up the create_api_key signal, in your
            # custom user module.
            return None
    else:
        from django.contrib.auth.models import User
        return User

USER_MODEL_CLASS_NAME = getattr(settings, 'AUTH_USER_CLASS', 'auth.User')
