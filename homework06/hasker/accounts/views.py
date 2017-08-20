# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import SignUpForm

def signup(request):
    if request.user.is_authenticated:
        return redirect("qa:index")

    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.avatar = form.cleaned_data.get("avatar") or "accounts/avatars/avatar.png"
            user.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("qa:index")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {
        "form": form
    })

