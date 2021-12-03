from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
def check(request):
    return redirect("Login")


def user_login(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        return redirect("Details")
    context = {"error_msgs": []}
    if request.method == "POST":
        if check_values(request.POST, context):
            try:
                student = Student.objects.get(username=request.POST["rollno"])
            except:
                context["error_msgs"].append("User does not exist")
            student = authenticate(request, username=request.POST["rollno"], password=request.POST["pwd"])
            if student is not None:
                if not student.is_staff:
                    login(request, student)
                    return redirect("Details")
                else:
                    context["error_msgs"].append("staff cant login here")

            else:
                context["error_msgs"].append("check your username or password")
    return render(request, "User/login.html", context)


def check_student(user):
    return not user.is_staff


@login_required(login_url="/login")
@user_passes_test(check_student, login_url="/admin/login")
def details(request):
    user = request.user
    user_details = user.details_set.all()[0]
    context = {"user": user_details, "percent": (user_details.cgpa - 0.75) * 10}
    return render(request, "User/Details.html", context)


def user_logout(request):
    logout(request)
    return redirect("Login")


# functions
def check_values(user, context):
    crt = True
    if user["rollno"] == "":
        crt = False
        msg = "UserName should not be empty"
        context["error_msgs"].append(msg)
    if user["pwd"] == "":
        crt = False
        msg = "Password should not be empty"
        context["error_msgs"].append(msg)
    return crt
