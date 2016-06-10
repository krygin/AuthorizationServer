from django.templatetags.static import register


@register.filter()
def marks_by_owner(queryset, owner):
    return queryset.filter(owner__user=owner)


@register.filter()
def by_owner(queryset, owner):
    return queryset.filter(owner=owner)


@register.filter()
def by_criterion(queryset, criterion):
    return queryset.filter(criteria=criterion)


@register.filter()
def not_filled(queryset):
    return queryset.filter(mark__isnull=True)


@register.filter()
def count(queryset):
    return queryset.count()
