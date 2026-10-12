from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .selectors import dashboard_payload


@login_required
def index(request):
    return render(request, "dashboard/index.html", {"stats": dashboard_payload(request.user)})
