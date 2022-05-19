from xml.etree.ElementTree import Comment
from django.contrib import admin

from auctions.models import Listings, User, Comments

# Register your models here.
admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Comments)