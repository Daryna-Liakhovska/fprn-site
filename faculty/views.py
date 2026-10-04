from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from .models import Department, HomePage, Program


def home(request):
    return render(
        request,
        "faculty/home.html",
        {
            "page": HomePage.load(),
            "departments": Department.objects.all(),
            "programs": Program.objects.select_related("department"),
        },
    )


def program_list(request):
    programs = Program.objects.select_related("department")
    return render(request, "faculty/program_list.html", {"programs": programs})


def program_detail(request, pk):
    program = get_object_or_404(Program.objects.select_related("department"), pk=pk)
    return render(request, "faculty/program_detail.html", {"program": program})


def department_list(request):
    departments = Department.objects.prefetch_related(
        Prefetch("programs", queryset=Program.objects.order_by("code"))
    )
    return render(request, "faculty/department_list.html", {"departments": departments})


def department_detail(request, pk):
    department = get_object_or_404(
        Department.objects.prefetch_related("programs", "teachers"), pk=pk
    )
    return render(
        request, "faculty/department_detail.html", {"department": department}
    )
