from django.shortcuts import render

from .models import ExchangeProgram


def program_list(request):
    programs = ExchangeProgram.objects.all()
    countries = (
        ExchangeProgram.objects.exclude(country="")
        .order_by("country")
        .values_list("country", flat=True)
        .distinct()
    )
    selected = request.GET.get("country", "")
    if selected:
        programs = programs.filter(country=selected)
    return render(
        request,
        "exchange/program_list.html",
        {"programs": programs, "countries": countries, "selected": selected},
    )
