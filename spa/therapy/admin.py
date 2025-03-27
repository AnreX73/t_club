from django.contrib import admin
from django.utils.safestring import mark_safe

from therapy.models import (
    User,
    ServicesCategory,
    Services,
    BidStatus,
    Bid,
    Abonements,
    WorkerSchedule,
    AbonementBid,
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
    list_display = (
        "id",
        "name",
        'is_public',
    )
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("id",)
    list_editable = ('is_public',)


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


@admin.register(BidStatus)
class BidStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name")
    search_fields = ("code", "name")
    list_display_links = ("id", "code", "name")


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "worker",
        "service",
        "date",
        
    )


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
