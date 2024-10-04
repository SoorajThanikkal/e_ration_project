from django.contrib import admin
from . models import reg,sreg,pro,shop,feed,super_user
from .models import*
# Register your models here.

admin.site.register(reg)

admin.site.register(sreg)

admin.site.register(pro)

admin.site.register(shop)

admin.site.register(feed)

admin.site.register(add2cart)

admin.site.register(super_user)

admin.site.register(Payment)