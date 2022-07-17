# Generated by Django 3.2 on 2022-07-17 16:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            sql='CREATE SCHEMA IF NOT EXISTS billing;',
            reverse_sql='DROP SCHEMA [IF EXISTS] billing CASCADE;',
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cart_id', models.UUIDField(default=uuid.uuid4)),
                ('idempotence_uuid', models.UUIDField(default=uuid.uuid4)),
                ('description', models.TextField(verbose_name='description')),
                ('payment_system', models.CharField(max_length=20, verbose_name='payment system')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'payment',
                'verbose_name_plural': 'payments',
                'db_table': 'billing"."payment',
            },
        ),
    ]
