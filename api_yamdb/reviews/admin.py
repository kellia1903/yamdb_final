from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'first_name',
                    'last_name',
                    'email',
                    'role',
                    'bio'
                    )


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'year',
                    'description',
                    'category',
                    # 'rating'
                    )
    search_fields = ('name',
                     'description',
                     )
    list_filter = ('year',)


admin.site.register(User, UserAdmin)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title, TitleAdmin)
