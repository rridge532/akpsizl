from django.contrib.admin.filters import RelatedFieldListFilter

class RelatedDropdownFilter(RelatedFieldListFilter):
    template = 'base/dropdown_filter.html'
