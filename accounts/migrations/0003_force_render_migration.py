from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_didyouknowfact_faq_mp_mpesatransaction_publicevent_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="SELECT 1;",
            reverse_sql="SELECT 1;"
        ),
    ]
