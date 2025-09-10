from django.db import migrations


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS `Tenant` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `subdomain` varchar(100) NOT NULL UNIQUE,
  `status` varchar(10) NOT NULL DEFAULT 'active',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


DROP_TABLE_SQL = """
DROP TABLE IF EXISTS `Tenant`;
"""


class Migration(migrations.Migration):
    dependencies = [
        ('tenants', '0002_alter_tenant_options'),
    ]

    operations = [
        migrations.RunSQL(sql=CREATE_TABLE_SQL, reverse_sql=DROP_TABLE_SQL),
    ]
