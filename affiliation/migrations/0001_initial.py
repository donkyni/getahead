# Generated by Django 3.1.7 on 2021-03-23 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('nom_d_utilisateur', models.CharField(help_text="Le nom d'utilisateur servira à se connecter à la plateforme, également pour parrainer un membre. Ex. toto21", max_length=255, null=True, unique=True)),
                ('nom', models.CharField(max_length=255, null=True)),
                ('prenom', models.CharField(max_length=255, null=True)),
                ('adresse', models.CharField(max_length=255, null=True)),
                ('telephone', models.BigIntegerField(null=True, unique=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars')),
                ('annee_de_naissance', models.DateField(blank=True, null=True)),
                ('sexe', models.CharField(blank=True, choices=[('Homme', 'Homme'), ('Femme', 'Femme')], help_text='Le sexe servira pour les statistiques', max_length=120, null=True)),
                ('don_bam', models.BooleanField(default=False, null=True)),
                ('don_zou', models.BooleanField(default=False, null=True)),
                ('don_maya', models.BooleanField(default=False, null=True)),
                ('don_mand', models.BooleanField(default=False, null=True)),
                ('pied_gauche', models.BooleanField(default=False, null=True)),
                ('pied_droit', models.BooleanField(default=False, null=True)),
                ('nb_pers_amene', models.PositiveSmallIntegerField(default=0, null=True)),
                ('point', models.PositiveSmallIntegerField(default=0, null=True)),
                ('stock_point', models.PositiveSmallIntegerField(default=0, null=True)),
                ('point_fictive_inv', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('point_fictive_col', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('point_fictive_manag', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('gam', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('date_d_ajout', models.DateTimeField(auto_now_add=True, null=True, verbose_name="Date d'enrégistrement de l'utilisateur")),
            ],
            options={
                'verbose_name': 'Utilisateur',
                'verbose_name_plural': 'Utilisateur',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='CodePays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pays', models.CharField(max_length=100, null=True)),
                ('code_pays', models.CharField(max_length=15, null=True)),
                ('archive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Droits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_du_droit', models.CharField(max_length=255)),
                ('archive', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DroitsProfils',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ecriture', models.BooleanField(default=False, null=True)),
                ('lecture', models.BooleanField(default=False, null=True)),
                ('modification', models.BooleanField(default=False, null=True)),
                ('suppression', models.BooleanField(default=False, null=True)),
                ('droit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliation.droits')),
            ],
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_du_groupe', models.CharField(help_text='Le nom du groupe permet de différencier les groupes, ex. Groupe 1', max_length=255, null=True)),
                ('manageur_du_groupe', models.CharField(help_text='Celui pour qui le groupe se cré et contiendra tous ses filleuls', max_length=255)),
                ('archive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('message', models.TextField(null=True)),
                ('archive', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Niveau',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_du_niveau', models.CharField(max_length=255, null=True)),
                ('archive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Poste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_du_poste', models.CharField(max_length=255, null=True)),
                ('archive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Versions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_de_version', models.CharField(max_length=50, null=True)),
                ('libelle', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('archive', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, null=True)),
                ('prenom', models.CharField(max_length=255, null=True)),
                ('telephone', models.IntegerField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('parrain', models.CharField(blank=True, max_length=150, null=True)),
                ('archive', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vague',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_de_vague', models.CharField(blank=True, max_length=150, null=True)),
                ('date_deb', models.DateField(null=True, verbose_name='Date de début de la formation')),
                ('date_fin', models.DateField(null=True, verbose_name='Date de clôture de la formation')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('archive', models.BooleanField(blank=True, default=False, null=True)),
                ('utilisateurs', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Participants')),
                ('version', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliation.versions')),
            ],
        ),
        migrations.CreateModel(
            name='Profils',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, null=True)),
                ('archive', models.BooleanField(default=False, null=True)),
                ('droits', models.ManyToManyField(through='affiliation.DroitsProfils', to='affiliation.Droits')),
            ],
        ),
        migrations.CreateModel(
            name='Payement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(default='Payement', max_length=255, null=True)),
                ('montant', models.DecimalField(decimal_places=1, max_digits=15, null=True)),
                ('poursuivre', models.BooleanField(null=True)),
                ('etat', models.BooleanField(blank=True, default=True, null=True)),
                ('date_d_ajout', models.DateTimeField(auto_now_add=True, null=True)),
                ('archive', models.BooleanField(default=False, null=True)),
                ('membre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Palier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_du_palier', models.CharField(max_length=255, null=True)),
                ('archive', models.BooleanField(default=False)),
                ('niveau', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliation.niveau')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_du_module', models.CharField(max_length=100, null=True, verbose_name='Nom du module')),
                ('intro_text', models.TextField(blank=True, null=True, verbose_name="Mot d'introduction")),
                ('video6', models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier vidéo 1')),
                ('texte6', models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier video')),
                ('longueur_video6', models.FloatField(blank=True, null=True)),
                ('temps_lu_video6', models.FloatField(blank=True, null=True)),
                ('video7', models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier vidéo 2')),
                ('texte7', models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier video')),
                ('longueur_video7', models.FloatField(blank=True, null=True)),
                ('temps_lu_video7', models.FloatField(blank=True, null=True)),
                ('video8', models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier vidéo 3')),
                ('texte8', models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier video')),
                ('longueur_video8', models.FloatField(blank=True, null=True)),
                ('temps_lu_video8', models.FloatField(blank=True, null=True)),
                ('video9', models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier vidéo 4')),
                ('texte9', models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier video')),
                ('longueur_video9', models.FloatField(blank=True, null=True)),
                ('temps_lu_video9', models.FloatField(blank=True, null=True)),
                ('video10', models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier vidéo 5')),
                ('texte10', models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier video')),
                ('longueur_video10', models.FloatField(blank=True, null=True)),
                ('temps_lu_video10', models.FloatField(blank=True, null=True)),
                ('audio1', models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier audio 1')),
                ('texte1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier audio')),
                ('longueur_audio1', models.FloatField(blank=True, null=True)),
                ('temps_lu_audio1', models.FloatField(blank=True, null=True)),
                ('audio2', models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier audio 2')),
                ('texte2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier audio')),
                ('longueur_audio2', models.FloatField(blank=True, null=True)),
                ('temps_lu_audio2', models.FloatField(blank=True, null=True)),
                ('audio3', models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier audio 3')),
                ('texte3', models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier audio')),
                ('longueur_audio3', models.FloatField(blank=True, null=True)),
                ('temps_lu_audio3', models.FloatField(blank=True, null=True)),
                ('audio4', models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier audio 4')),
                ('texte4', models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier audio')),
                ('longueur_audio4', models.FloatField(blank=True, null=True)),
                ('temps_lu_audio4', models.FloatField(blank=True, null=True)),
                ('audio5', models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier audio 5')),
                ('texte5', models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier audio')),
                ('longueur_audio5', models.FloatField(blank=True, null=True)),
                ('temps_lu_audio5', models.FloatField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('archive', models.BooleanField(blank=True, default=False, null=True)),
                ('version', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliation.versions', verbose_name='Version Wara')),
            ],
        ),
        migrations.AddField(
            model_name='droitsprofils',
            name='profil',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliation.profils'),
        ),
        migrations.AddField(
            model_name='user',
            name='groupe',
            field=models.ForeignKey(help_text="Le groupe permettra de voir l'ensemble de ses membres", null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliation.groupe', verbose_name="Nom de l'équipe"),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='nom_du_parent',
            field=models.ForeignKey(blank=True, help_text="Indiquez le parent qui l'adhère. S'il est le premier membre de son groupe, laissez vide", null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Parrain'),
        ),
        migrations.AddField(
            model_name='user',
            name='palier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliation.palier'),
        ),
        migrations.AddField(
            model_name='user',
            name='pays_de_residence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliation.codepays'),
        ),
        migrations.AddField(
            model_name='user',
            name='poste',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliation.poste'),
        ),
        migrations.AddField(
            model_name='user',
            name='profil',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliation.profils'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
