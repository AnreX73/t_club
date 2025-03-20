from django.contrib import admin
from django.utils.safestring import mark_safe

from therapy.models import (
    User,
    ServicesCategory,
    Services,
    Bid,
    Abonements,
    WorkerSchedule, AbonementBid,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "gethtmlPhoto", "role")
    list_display_links = ("id", "username", "gethtmlPhoto", "role")
    search_fields = ("role",)
    save_on_top = True

    def gethtmlPhoto(self, picture):
        if picture.photo:
            return mark_safe(f"<img src='{picture.photo.url}' width=50>")

    gethtmlPhoto.short_description = "миниатюра"


@admin.register(ServicesCategory)
class ServicesCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ('id',)


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "category",
        "duration",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("category",)
    save_on_top = True
    ordering = ("category", "name")


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    pass


@admin.register(Abonements)
class AbonementsAdmin(admin.ModelAdmin):
    pass


@admin.register(AbonementBid)
class AbonementBidAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkerSchedule)
class WorkerScheduleAdmin(admin.ModelAdmin):
    list_display = ("worker", "day_of_week", "start_time", "end_time", "pre_entry_days")
    save_on_top = True
    ordering = ("worker", "day_of_week")


admin.site.site_header = "THERAPY CLUB"
