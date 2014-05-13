from models import Lab, Test, TestResponse, ActionPlanResponse

from django.contrib import admin

admin.site.register(Lab)
admin.site.register(TestResponse)
admin.site.register(ActionPlanResponse)

class TestAdmin(admin.ModelAdmin):
    class Meta:
        model = Test
    list_display = ("name", "lab")

admin.site.register(Test, TestAdmin)
