from django.contrib import admin

from .models import Department, HomePage, Program, Teacher


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ("title", "dean", "phone", "email")

    def has_add_permission(self, request):
        return not HomePage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class TeacherInline(admin.TabularInline):
    model = Teacher
    extra = 1


class ProgramInline(admin.TabularInline):
    model = Program
    fields = ("code", "name", "coordinator_name")
    extra = 0
    show_change_link = True


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "head")
    search_fields = ("name", "head")
    inlines = [ProgramInline, TeacherInline]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "department", "coordinator_name")
    list_filter = ("department",)
    search_fields = ("name", "code", "coordinator_name")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "degree", "department")
    list_filter = ("department", "position")
    search_fields = ("name",)
