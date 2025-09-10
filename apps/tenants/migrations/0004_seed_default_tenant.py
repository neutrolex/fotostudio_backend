from django.db import migrations


def seed_default_tenant(apps, schema_editor):
    Tenant = apps.get_model('tenants', 'Tenant')
    if not Tenant.objects.filter(subdomain='default').exists():
        Tenant.objects.create(
            name='Default Tenant',
            subdomain='default',
            status='active',
        )


def unseed_default_tenant(apps, schema_editor):
    Tenant = apps.get_model('tenants', 'Tenant')
    Tenant.objects.filter(subdomain='default').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('tenants', '0003_create_tenant_table_if_missing'),
    ]

    operations = [
        migrations.RunPython(seed_default_tenant, reverse_code=unseed_default_tenant),
    ]
