from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep


# Unregister Group
admin.site.unregister(Group)



# mix profile inside user
class ProfileInline(admin.StackedInline):
    model=Profile
    
# Extend User Model

#class UserAdmin(admin.ModelAdmin):
#    model = User
    # Display only username
#    fields = ["username","is_staff","password"]
#    inlines = [ProfileInline]

# unregister initial user
#admin.site.unregister(User)
# register my custom user
#admin.site.register(User1, UserAdmin)
# register profile model
admin.site.register(Profile)


admin.site.register(Meep)




