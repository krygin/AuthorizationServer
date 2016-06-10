from django import forms
from django.contrib import admin

# Register your models here.
from resources.models import ResourceOwner, ResourceCriteria, OwnersMark, Resource, ResourceAccessRequest, Client, \
    Criteria


class ResourceCriteriaInline(admin.TabularInline):
    model = ResourceCriteria
    extra = 1


class ResourceOwnerInline(admin.TabularInline):
    model = ResourceOwner
    extra = 1


class ResourceAdmin(admin.ModelAdmin):
    inlines = [ResourceCriteriaInline, ResourceOwnerInline]
    list_display = ('path',)


class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def get_model_perms(self, request):
        perms = super(CriteriaAdmin, self).get_model_perms(request)
        perms['list_hide'] = True
        return perms


class OwnersMarkAdmin(admin.ModelAdmin):
    list_display = ('owner', 'criteria', 'mark')


class MarksInline(admin.TabularInline):
    model = OwnersMark
    extra = 0
    fields = ('mark',)
    can_delete = False

    def has_add_permission(self, request):
        return False


class CreateAccessRequestForm(forms.ModelForm):
    class Meta:
        model = ResourceAccessRequest
        fields = ('resource', 'user', 'client')


class UpdateAccessRequestForm(forms.ModelForm):
    resource = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = ResourceAccessRequest
        fields = ('resource', 'user', 'client',)


class ResourceAccessRequestAdmin(admin.ModelAdmin):
    inlines = [MarksInline, ]
    fields = ('resource', 'user', 'client', 'submitted')
    readonly_fields = ('resource', 'user', 'client', 'submitted')

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide MyInline in the add view
            if isinstance(inline, MarksInline) and obj is None:
                continue
            yield inline.get_formset(request, obj), inline

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        else:
            return self.readonly_fields



class ClientAdmin(admin.ModelAdmin):
    pass


admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceAccessRequest, ResourceAccessRequestAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Criteria, CriteriaAdmin)
