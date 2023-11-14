from django.contrib import admin

from Users.models import UserInfo


# Register your models here.
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = [
        "Name",
        "Phone",
    ]
    search_fields = [
        "Phone",
        "Name",
    ]
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
