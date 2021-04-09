from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from affiliation.models import Poste, Niveau, Palier, Groupe, CodePays, Droits, Profils, Payement, Wara, Message, User, \
    DroitsProfils, Versions, Modules, Vague, Packs


class PosteAdmin(admin.ModelAdmin):
    list_display = ('nom_du_poste', 'archive')
    list_filter = ('nom_du_poste',)
    ordering = ('nom_du_poste',)
    search_fields = ('nom_du_poste',)


admin.site.register(Poste, PosteAdmin)


class NiveauAdmin(admin.ModelAdmin):
    list_display = ('nom_du_niveau', 'archive')
    list_filter = ('nom_du_niveau',)
    ordering = ('nom_du_niveau',)
    search_fields = ('nom_du_niveau',)


admin.site.register(Niveau, NiveauAdmin)


class PalierAdmin(admin.ModelAdmin):
    list_display = ('nom_du_palier', 'niveau', 'archive')
    list_filter = ('nom_du_palier',)
    ordering = ('nom_du_palier',)
    search_fields = ('nom_du_palier',)


admin.site.register(Palier, PalierAdmin)


class GroupeAdmin(admin.ModelAdmin):
    list_display = ('nom_du_groupe', 'manageur_du_groupe', 'archive')
    list_filter = ('manageur_du_groupe',)
    ordering = ('nom_du_groupe',)
    search_fields = ('manageur_du_groupe',)


admin.site.register(Groupe, GroupeAdmin)


class CodePaysAdmin(admin.ModelAdmin):
    list_display = ('pays', 'code_pays', 'archive')
    list_filter = ('pays',)
    ordering = ('pays',)
    search_fields = ('pays',)


admin.site.register(CodePays, CodePaysAdmin)


class DroitsAdmin(admin.ModelAdmin):
    list_display = ('nom_du_droit', 'archive')
    list_filter = ('nom_du_droit',)
    ordering = ('nom_du_droit',)
    search_fields = ('nom_du_droit',)


admin.site.register(Droits, DroitsAdmin)


class ProfilsAdmin(admin.ModelAdmin):
    list_display = ('nom', 'archive')
    list_filter = ('nom',)
    ordering = ('nom',)
    search_fields = ('nom',)


admin.site.register(Profils, ProfilsAdmin)


class DroitsProfilsAdmin(admin.ModelAdmin):
    list_display = ('profil', 'droit', 'ecriture', 'lecture', 'modification', 'suppression')
    list_filter = ('profil', 'droit')
    ordering = ('profil',)
    search_fields = ('profil',)


admin.site.register(DroitsProfils, DroitsProfilsAdmin)


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'nom_d_utilisateur', 'nom_du_parent', 'nom', 'prenom', 'adresse',
            'pays_de_residence', 'telephone', 'groupe',
            'avatar', 'sexe',
        )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'nom_d_utilisateur', 'nom_du_parent', 'nom', 'prenom', 'adresse',
            'pays_de_residence', 'telephone', 'groupe',
            'avatar', 'sexe', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'nom_d_utilisateur', 'nom_du_parent', 'nom', 'prenom', 'adresse',
        'pays_de_residence', 'telephone', 'groupe',
        'avatar', 'sexe', 'profil', 'gam', 'unique_id', 'dix_milles', 'point_a_affecter', 'point', 'stock_point', 'point_fictive_inv', 'point_fictive_col',
        'point_fictive_manag', 'palier', 'poste', 'don_bam', 'don_zou', 'don_maya', 'espace', 'jours_ouvrables', 'don_mand', 'is_admin')
    list_filter = ('is_admin', 'nom')
    fieldsets = (
        (None, {'fields': ('nom_d_utilisateur', 'password')}),
        ('Personal info', {'fields': (
            'nom_du_parent', 'nom', 'prenom', 'adresse',
            'pays_de_residence', 'telephone', 'groupe',
            'avatar', 'sexe', 'profil', 'gam', 'unique_id', 'dix_milles', 'point_a_affecter', 'point', 'stock_point', 'point_fictive_inv', 'point_fictive_col',
            'point_fictive_manag', 'palier', 'poste', 'don_bam', 'don_zou', 'don_maya', 'don_mand', 'espace', 'jours_ouvrables',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'nom_d_utilisateur', 'nom_du_parent', 'nom', 'prenom', 'adresse',
                'pays_de_residence', 'telephone', 'groupe',
                'avatar', 'sexe', 'profil', 'gam', 'unique_id', 'dix_milles', 'point_a_affecter', 'point', 'stock_point', 'point_fictive_inv', 'point_fictive_col', 'point_fictive_manag',  'palier', 'poste', 'don_bam', 'don_zou', 'don_maya',
                'don_mand', 'espace', 'jours_ouvrables', 'password'),
        }),
    )
    search_fields = ('nom_d_utilisateur', 'nom',)
    ordering = ('date_d_ajout',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)


class PayementAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'montant', 'membre', 'poursuivre', 'etat', 'date_d_ajout', 'archive')
    list_filter = ('libelle', 'montant',)
    date_hierarchy = 'date_d_ajout'
    ordering = ('membre',)
    search_fields = ('libelle',)


admin.site.register(Payement, PayementAdmin)


class WaraAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone', 'email', 'archive', 'date')
    list_filter = ('nom', 'prenom',)
    date_hierarchy = 'date'
    ordering = ('date',)
    search_fields = ('nom',)


admin.site.register(Wara, WaraAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'message', 'archive')
    list_filter = ('email',)
    ordering = ('message',)
    search_fields = ('email',)


admin.site.register(Message, MessageAdmin)


class VersionsAdmin(admin.ModelAdmin):
    list_display = ('nom_de_version', 'libelle', 'created', 'archive')
    list_filter = ('nom_de_version',)
    date_hierarchy = 'created'
    ordering = ('nom_de_version',)
    search_fields = ('nom_de_version',)


admin.site.register(Versions, VersionsAdmin)


class ModulesAdmin(admin.ModelAdmin):
    list_display = ('version', 'nom_du_module', 'intro_text', 'video6', 'video7', 'video8', 'video9', 'video10',
                    'audio1', 'audio2', 'audio3', 'audio4', 'audio5',
                    'pdf1', 'pdf2', 'pdf3', 'pdf4', 'pdf5', 'created', 'archive')
    list_filter = ('version',)
    date_hierarchy = 'created'
    ordering = ('version',)
    search_fields = ('version',)


admin.site.register(Modules, ModulesAdmin)


class VagueAdmin(admin.ModelAdmin):
    list_display = ('nom_de_vague', 'version', 'date_deb', 'date_fin', 'created', 'archive')
    list_filter = ('nom_de_vague',)
    date_hierarchy = 'created'
    ordering = ('nom_de_vague',)
    search_fields = ('nom_de_vague',)


admin.site.register(Vague, VagueAdmin)


class PacksAdmin(admin.ModelAdmin):
    list_display = ('nouveau_nom', 'prix', 'jours', 'archive')
    list_filter = ('nouveau_nom',)
    date_hierarchy = 'date'
    ordering = ('nouveau_nom',)
    search_fields = ('nouveau_nom',)


admin.site.register(Packs, PacksAdmin)
