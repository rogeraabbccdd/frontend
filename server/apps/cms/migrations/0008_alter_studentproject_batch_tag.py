from django.db import migrations, models


def clear_generic_batch_tag(apps, schema_editor):
    """將舊的通用預設值清空。

    「前端專班結訓成果」是 model 的舊預設值，所有作品都相同、不具鑑別度，
    也讓「期別標籤」欄位失去原本要區分屆別的用途。此處清空後，
    前台不再顯示無意義的標籤，待後台填入真實期別（例：114年第一期）即可正常呈現。
    """
    StudentProject = apps.get_model('cms', 'StudentProject')
    StudentProject.objects.filter(batch_tag='前端專班結訓成果').update(batch_tag='')


def restore_generic_batch_tag(apps, schema_editor):
    StudentProject = apps.get_model('cms', 'StudentProject')
    StudentProject.objects.filter(batch_tag='').update(batch_tag='前端專班結訓成果')


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_alter_admissionbatch_deleted_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentproject',
            name='batch_tag',
            field=models.CharField(
                blank=True,
                default='',
                help_text='例：114年第一期。留空則前台不顯示期別標籤。',
                max_length=50,
                verbose_name='期別標籤',
            ),
        ),
        migrations.RunPython(clear_generic_batch_tag, restore_generic_batch_tag),
    ]
