# Generated by Django 2.0.3 on 2019-07-02 00:25

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='通讯录')),
                ('description', models.TextField(default='通讯录', help_text='用来作为SEO中description,长度参考SEO标准', max_length=240, verbose_name='描述')),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': '通讯录',
                'verbose_name_plural': '通讯录',
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='ouser',
            options={'ordering': ['id'], 'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.AlterField(
            model_name='ouser',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='avatar/default.png', upload_to='avatar/%Y/%m/%d', verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='ouser',
            name='contact',
            field=models.ManyToManyField(default='1', to='user.Contacts', verbose_name='通讯录'),
        ),
    ]