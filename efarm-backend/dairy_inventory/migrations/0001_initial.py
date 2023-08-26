# Generated by Django 4.1.7 on 2023-08-22 06:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("dairy", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BarnInventory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number_of_cows", models.PositiveIntegerField(default=0)),
                ("number_of_pens", models.PositiveIntegerField(default=1)),
                ("last_update", models.DateTimeField(auto_now=True)),
                (
                    "barn",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="dairy.barn",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CowInventory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "total_number_of_cows",
                    models.PositiveIntegerField(
                        default=0, editable=False, verbose_name="Total Number of Cows"
                    ),
                ),
                (
                    "number_of_male_cows",
                    models.PositiveIntegerField(
                        default=0, editable=False, verbose_name="Number of Male Cows"
                    ),
                ),
                (
                    "number_of_female_cows",
                    models.PositiveIntegerField(
                        default=0, editable=False, verbose_name="Number of Female Cows"
                    ),
                ),
                (
                    "number_of_sold_cows",
                    models.PositiveIntegerField(
                        default=0, editable=False, verbose_name="Number of Sold Cows"
                    ),
                ),
                (
                    "number_of_dead_cows",
                    models.PositiveIntegerField(
                        default=0, editable=False, verbose_name="Number of Dead Cows"
                    ),
                ),
                ("last_update", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="CowInventoryUpdateHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number_of_cows",
                    models.PositiveIntegerField(
                        default=0, editable=False, verbose_name="Total number of cows"
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        auto_now_add=True,
                        verbose_name="Cow Inventory Update History Date",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MilkInventory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "total_amount_in_kgs",
                    models.FloatField(
                        default=0.0,
                        editable=False,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                        verbose_name="Amount (kg)",
                    ),
                ),
                ("last_update", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Milk Inventory",
                "verbose_name_plural": "Milk Inventory",
                "ordering": ["-last_update"],
            },
        ),
        migrations.CreateModel(
            name="MilkInventoryUpdateHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount_in_kgs",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        editable=False,
                        max_digits=7,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                        verbose_name="Total Amount (kg)",
                    ),
                ),
                ("date", models.DateField(auto_now_add=True, verbose_name="Date")),
            ],
        ),
        migrations.CreateModel(
            name="CowPenInventory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number_of_cows", models.PositiveIntegerField(default=0)),
                (
                    "pen",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="dairy.cowpen"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CowPenHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("Movable", "Movable"), ("Fixed", "Fixed")],
                        max_length=15,
                    ),
                ),
                ("number_of_cows", models.PositiveIntegerField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "barn",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dairy.barn"
                    ),
                ),
                (
                    "pen",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dairy.cowpen"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BarnInventoryHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number_of_cows", models.PositiveIntegerField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "barn_inventory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dairy_inventory.barninventory",
                    ),
                ),
            ],
        ),
    ]
