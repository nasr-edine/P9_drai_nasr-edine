from django.contrib import admin

from .models import Review, Ticket


class ReviewInline(admin.TabularInline):
    model = Review


class ReviewAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline,
    ]


# Register your models here.
admin.site.register(Ticket, ReviewAdmin)
admin.site.register(Review)
