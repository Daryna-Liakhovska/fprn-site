from django.contrib import admin

from .models import ExchangeProgram


@admin.register(ExchangeProgram)
class ExchangeProgramAdmin(admin.ModelAdmin):
    list_display = ("university", "country", "languages", "seats_display", "deadline", "status")
    list_filter = ("country",)
    search_fields = ("university", "country", "languages")
    date_hierarchy = "deadline"

    @admin.display(description="Кількість місць", ordering="seats")
    def seats_display(self, obj):
        return obj.seats_display

    @admin.display(description="Статус", boolean=True)
    def status(self, obj):
        return obj.is_open
