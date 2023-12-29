# Generated by Django 4.2.3 on 2023-12-29 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('cmp_id', models.AutoField(primary_key=True, serialize=False, verbose_name='CID')),
                ('company_name', models.CharField(max_length=200)),
                ('phone_number', models.BigIntegerField(blank=True, null=True)),
                ('gst_number', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('state', models.CharField(blank=True, max_length=150, null=True)),
                ('country', models.CharField(blank=True, max_length=150, null=True)),
                ('logo', models.ImageField(null=True, upload_to='logo/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('hsn', models.IntegerField()),
                ('unit', models.CharField(max_length=100)),
                ('tax', models.CharField(max_length=50)),
                ('sale_price', models.FloatField(blank=True, null=True)),
                ('purchase_price', models.FloatField(blank=True, null=True)),
                ('stock', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BillApp.company')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentTerms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(default=0, null=True)),
                ('term', models.CharField(default='Days', max_length=20, null=True)),
                ('days', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('bill_no', models.AutoField(primary_key=True, serialize=False, verbose_name='bill_no')),
                ('bill_number', models.CharField(max_length=20, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('party_name', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=15)),
                ('gstin', models.CharField(max_length=15)),
                ('subtotal', models.FloatField(blank=True, null=True)),
                ('tax', models.FloatField(blank=True, null=True)),
                ('adjustment', models.FloatField(blank=True, null=True)),
                ('total_amount', models.FloatField(blank=True, null=True)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BillApp.company')),
            ],
        ),
        migrations.CreateModel(
            name='Sales_items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('hsn', models.CharField(max_length=15)),
                ('quantity', models.IntegerField()),
                ('rate', models.FloatField()),
                ('tax', models.CharField(max_length=10)),
                ('total', models.FloatField()),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BillApp.company')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BillApp.items')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BillApp.sales')),
            ],
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('bill_no', models.AutoField(primary_key=True, serialize=False, verbose_name='bill_no')),
                ('bill_number', models.CharField(max_length=20, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('party_name', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=15)),
                ('gstin', models.CharField(max_length=15)),
                ('subtotal', models.FloatField(blank=True, null=True)),
                ('tax', models.FloatField(blank=True, null=True)),
                ('adjustment', models.FloatField(blank=True, null=True)),
                ('total_amount', models.FloatField(blank=True, null=True)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BillApp.company')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase_items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('hsn', models.CharField(max_length=15)),
                ('quantity', models.IntegerField()),
                ('rate', models.FloatField()),
                ('tax', models.CharField(max_length=10)),
                ('total', models.FloatField()),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BillApp.company')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BillApp.items')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BillApp.purchases')),
            ],
        ),
        migrations.CreateModel(
            name='Item_units',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BillApp.company')),
            ],
        ),
        migrations.CreateModel(
            name='Item_transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('date', models.DateField(blank=True, null=True)),
                ('quantity', models.IntegerField()),
                ('bill_number', models.CharField(blank=True, max_length=50, null=True)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BillApp.company')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BillApp.items')),
            ],
        ),
        migrations.CreateModel(
            name='DeletedSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_number', models.CharField(max_length=50)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BillApp.company')),
            ],
        ),
        migrations.CreateModel(
            name='DeletedPurchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_number', models.CharField(max_length=50)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BillApp.company')),
            ],
        ),
        migrations.CreateModel(
            name='ClientTrials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('trial_status', models.BooleanField(default=True, null=True)),
                ('purchase_start_date', models.DateField(null=True)),
                ('purchase_end_date', models.DateField(null=True)),
                ('payment_term', models.CharField(max_length=50, null=True)),
                ('purchase_status', models.CharField(default='false', max_length=15, null=True)),
                ('subscribe_status', models.CharField(default='null', max_length=50, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='BillApp.company')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
