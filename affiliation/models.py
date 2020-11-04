
from django.db import models
from django.contrib.auth import models as auth_models


class Poste(models.Model):
    nom_du_poste = models.CharField(max_length=255, null=True, blank=False)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.nom_du_poste


class Niveau(models.Model):
    nom_du_niveau = models.CharField(max_length=255, null=True, blank=False)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.nom_du_niveau


class Palier(models.Model):
    nom_du_palier = models.CharField(max_length=255, null=True, blank=False)
    niveau = models.ForeignKey(Niveau, null=True, blank=False, on_delete=models.SET_NULL)
    archive = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.nom_du_palier


class Groupe(models.Model):
    nom_du_groupe = models.CharField(max_length=255, null=True, blank=False,
                                     help_text="Le nom du groupe permet de différencier les groupes, ex. Groupe 1")
    manageur_du_groupe = models.CharField(max_length=255,
                                          help_text="Celui pour qui le groupe se cré et contiendra tous ses filleuls")
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.nom_du_groupe


class CodePays(models.Model):
    pays = models.CharField(max_length=100, null=True, blank=False)
    code_pays = models.CharField(max_length=15, null=True, blank=False)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.code_pays


class UserManager(auth_models.BaseUserManager):

    def create_user(self, code, adresse, nom, prenom, password=None):
        if not code:
            raise ValueError('Users must have an telephone number')
        user = self.model(code=code)
        user.adresse = adresse
        user.nom = nom
        user.prenom = prenom
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, code, adresse, nom, prenom, password):
        user = self.create_user(
            code,
            adresse=adresse,
            nom=nom,
            prenom=prenom,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    SEXE = (
        (u"Homme", u"Homme"),
        (u"Femme", u"Femme")
    )

    """
    Informations de base
    """
    code = models.CharField(unique=True, max_length=255, null=True, blank=False,
                            help_text="Ce code servira à se connecter à la plateforme, également pour parrainer un "
                                      "membre. Ex. 228DS000000001")
    nom_du_parent = models.ForeignKey("self", on_delete=models.SET_NULL, verbose_name='ID du parrain',
                                      help_text="Indiquez le parent qui l'adhère. S'il est le premier membre de son "
                                                "groupe, laissez vide", null=True, blank=True)
    nom = models.CharField(max_length=255, null=True)
    prenom = models.CharField(max_length=255, blank=False, null=True)
    adresse = models.CharField(max_length=255, null=True, blank=False)
    pays_de_residence = models.ForeignKey(CodePays, on_delete=models.SET_NULL, null=True, blank=False)
    telephone = models.IntegerField(blank=False, null=True, unique=True)
    poste = models.ForeignKey(Poste, null=True, blank=False, on_delete=models.SET_NULL)
    palier = models.ForeignKey(Palier, null=True, blank=False, on_delete=models.SET_NULL)
    groupe = models.ForeignKey(Groupe, null=True, blank=False, on_delete=models.SET_NULL,
                               help_text="Le groupe permettra de voir l'ensemble de ses membres")

    """
    Informations supplémentaires
    """
    avatar = models.ImageField(blank=True, null=True, upload_to="avatars")
    annee_de_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(choices=SEXE, max_length=120, null=True, blank=True,
                            help_text="Le sexe servira pour les statistiques")

    """
    Données systèmes
    """
    pied_gauche = models.BooleanField(default=False, null=True, blank=False)
    pied_droit = models.BooleanField(default=False, null=True, blank=False)
    nb_pers_amene = models.PositiveSmallIntegerField(null=True, blank=False, default=0)
    point = models.PositiveSmallIntegerField(null=True, blank=False, default=0)
    gam = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_d_ajout = models.DateTimeField(auto_now_add=True, null=True,
                                        verbose_name="Date d'enrégistrement de l'utilisateur")

    objects = UserManager()

    USERNAME_FIELD = 'code'
    REQUIRED_FIELDS = ['nom', 'prenom', 'adresse']

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateur'
        ordering = ('id',)

    def __str__(self):
        return self.prenom + ' ' + self.nom

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return self.is_admin

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Réponse la plus simple possible : Tous les administrateurs sont du personnel
        return self.is_active

    def __unicode__(self):
        # pass
        return u'{0}'.format(self.get_full_name())

    def get_short_name(self):
        # pass
        return self.nom

    def get_full_name(self):
        # pass
        return u'{0} {1}'.format(self.prenom, self.nom)
