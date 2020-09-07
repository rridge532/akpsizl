from django.contrib.admin import AdminSite

# Register your models here.

class AKPsiAdminSite(AdminSite):
    site_header = "AKPsi ZL Exec Administration"
    site_title = "Exec Administration"
    index_title = "AKPsi ZL"

admin_site = AKPsiAdminSite(name='akpsiadmin')
