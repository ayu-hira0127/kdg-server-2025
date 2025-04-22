from django.db import migrations

def add_new_categories(apps, schema_editor):
    Category = apps.get_model('search_app', 'Category')
    new_categories = ['トップス', 'ボトムス', 'アクセサリー', 'アウター', 'その他']
    
    for category in new_categories:
        Category.objects.create(name=category)

class Migration(migrations.Migration):

    dependencies = [
        ('search_app', '0013_product_is_featured'),  # 直前のマイグレーションファイルを指定します
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_featured',
        ),
        migrations.RunPython(add_new_categories),
    ]