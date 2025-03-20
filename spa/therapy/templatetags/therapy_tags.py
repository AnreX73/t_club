from django import template

from therapy.models import User, Bid

register = template.Library()


@register.inclusion_tag("registration/include/worker_profile.html")
def worker_profile(user):
    clients = Bid.objects.filter(worker=user).order_by("date")
    return {"clients": clients}


@register.inclusion_tag("registration/include/admin_profile.html")
def admin_profile():
    clients = Bid.objects.all().order_by("date")
    return {"clients": clients}
