##
#    Copyright (C) 2013 Jessica Tallon & Matt Molyneaux
#   
#    This file is part of Inboxen front-end.
#
#    Inboxen front-end is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Inboxen front-end is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Inboxen front-end.  If not, see <http://www.gnu.org/licenses/>.
##

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from inboxen.tasks import delete_account

@login_required
def delete(request):

    if request.method == "POST":
        if "username" in request.POST and request.POST["username"]:
            if request.user.username == request.POST["username"]:
                # right!
                delete_account.delay(request.user)
                logout(request)
                return HttpResponseRedirect("/user/deleted")
            else:
                return render(request, "user/settings/delete.html")

    context = {
        "page":"Delete Account",
    }

    return render(request, "user/settings/delete/confirm.html", context)

def success(request):
    context = {
        "page":"Goodbye",
    }
     
    return render(request, "user/settings/delete/success.html", context)
