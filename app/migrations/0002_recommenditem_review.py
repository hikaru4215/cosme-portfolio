# Generated by Django 2.2.19 on 2021-03-19 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommenditem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100, verbose_name='ブランド名')),
                ('product', models.CharField(max_length=100, verbose_name='製品名')),
                ('content', models.TextField(verbose_name='説明')),
                ('image', models.ImageField(upload_to='images', verbose_name='イメージ画像')),
                ('item', models.CharField(max_length=100, verbose_name='アイテムの種類')),
                ('price', models.CharField(max_length=100, verbose_name='本体価格')),
                ('price_data', models.IntegerField(default=1000, verbose_name='価格データ')),
                ('age', models.IntegerField(default=10, verbose_name='年齢')),
                ('skintype', models.CharField(max_length=100, verbose_name='肌タイプ')),
                ('acne_point', models.IntegerField(default=0, verbose_name='ニキビポイント')),
                ('pores_point', models.IntegerField(default=0, verbose_name='毛穴ポイント')),
                ('spots_point', models.IntegerField(default=0, verbose_name='シミポイント')),
                ('wrinkle_point', models.IntegerField(default=0, verbose_name='シワポイント')),
                ('official_page', models.URLField(verbose_name='公式URL')),
                ('rakuten_page', models.URLField(verbose_name='楽天URL')),
                ('amazon_page', models.URLField(verbose_name='アマゾンURL')),
                ('trouble_name1', models.CharField(blank=True, max_length=100, verbose_name='ニキビ')),
                ('trouble_name2', models.CharField(blank=True, max_length=100, verbose_name='毛穴')),
                ('trouble_name3', models.CharField(blank=True, max_length=100, verbose_name='シワ')),
                ('trouble_name4', models.CharField(blank=True, max_length=100, verbose_name='シミ')),
                ('capacity', models.CharField(max_length=100, verbose_name='容量')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(blank=True, max_length=100, verbose_name='ブランド名')),
                ('product', models.CharField(max_length=100, verbose_name='製品名')),
                ('comment', models.TextField(verbose_name='クチコミ')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('image', models.ImageField(blank=True, upload_to='images', verbose_name='イメージ画像')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category', verbose_name='カテゴリー')),
                ('price', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.Price', verbose_name='プライス')),
                ('score', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Score', verbose_name='おすすめ度')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
