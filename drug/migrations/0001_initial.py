# Generated by Django 3.2.9 on 2022-07-07 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MedicineEfficacyClassification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_classification_en', models.CharField(blank=True, max_length=200, null=True)),
                ('drug_classification_jp', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(blank=True, max_length=200, null=True)),
                ('sales_name_code', models.CharField(blank=True, max_length=200, null=True)),
                ('standard_name', models.CharField(blank=True, max_length=500, null=True)),
                ('japan_standard_prod_classification_number', models.CharField(blank=True, max_length=200, null=True)),
                ('yj_code', models.CharField(blank=True, max_length=200, null=True)),
                ('medicinal_effect_classification_name', models.CharField(blank=True, max_length=200, null=True)),
                ('approval_number', models.CharField(blank=True, max_length=200, null=True)),
                ('european_trademark_name', models.CharField(blank=True, max_length=200, null=True)),
                ('nhi_price_standard_listing_date', models.DateField(blank=True, null=True)),
                ('sales_start_date', models.DateField(blank=True, null=True)),
                ('saving_method', models.CharField(blank=True, max_length=200, null=True)),
                ('expiration_date', models.CharField(blank=True, max_length=200, null=True)),
                ('regulation_classification', models.CharField(blank=True, max_length=500, null=True)),
                ('active_ingredient', models.CharField(blank=True, max_length=500, null=True)),
                ('additive', models.CharField(blank=True, max_length=500, null=True)),
                ('properties', models.TextField(blank=True, null=True)),
                ('caveat', models.TextField(blank=True, null=True)),
                ('contraindications', models.TextField(blank=True, null=True)),
                ('contraindications_in_principle', models.TextField(blank=True, null=True)),
                ('efficacy', models.TextField(blank=True, null=True)),
                ('usage_dosage', models.TextField(blank=True, null=True)),
                ('precautions_related_to_usage', models.TextField(blank=True, null=True)),
                ('precautions_for_use', models.TextField(blank=True, null=True)),
                ('warning', models.CharField(blank=True, max_length=500, null=True)),
                ('important_basic_notes', models.TextField(blank=True, null=True)),
                ('interaction', models.CharField(blank=True, max_length=500, null=True)),
                ('drug_name', models.CharField(blank=True, max_length=500, null=True)),
                ('clinical_symptoms', models.TextField(blank=True, null=True)),
                ('mechanism_riskfactors', models.CharField(blank=True, max_length=500, null=True)),
                ('caution_for_combined_use', models.TextField(blank=True, null=True)),
                ('side_effects', models.TextField(blank=True, null=True)),
                ('other_side_effects', models.TextField(blank=True, null=True)),
                ('administration_to_the_elderly', models.TextField(blank=True, null=True)),
                ('administration_to_pregnant_women', models.TextField(blank=True, null=True)),
                ('administration_to_children', models.TextField(blank=True, null=True)),
                ('overdose', models.TextField(blank=True, null=True)),
                ('precautions_for_application', models.TextField(blank=True, null=True)),
                ('pharmacokinetics', models.TextField(blank=True, null=True)),
                ('pharmacology', models.CharField(blank=True, max_length=500, null=True)),
                ('pharmacological_action', models.TextField(blank=True, null=True)),
                ('physicochemical_knowledge_about_active_ingredients', models.TextField(blank=True, null=True)),
                ('packaging', models.TextField(blank=True, null=True)),
                ('main_documents_and_document_request_destinations', models.TextField(blank=True, null=True)),
                ('document_request_destination', models.TextField(blank=True, null=True)),
                ('information_on_medications_with_limited_dosing_periods', models.TextField(blank=True, null=True)),
                ('name_of_manufacturer_or_distributor', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('drug_classification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='drug.medicineefficacyclassification')),
            ],
        ),
    ]
