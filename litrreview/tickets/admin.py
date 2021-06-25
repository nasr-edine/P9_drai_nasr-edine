from django.contrib import admin
# from django.contrib.admin.options import ModelAdmin

from .models import Ticket, Review


class ReviewInline(admin.TabularInline):
    # class ReviewInline(admin.StackedInline):
    model = Review


class ReviewAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline,
    ]


# Register your models here.
admin.site.register(Ticket, ReviewAdmin)
admin.site.register(Review)
