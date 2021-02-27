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


class Droits(models.Model):
    nom_du_droit = models.CharField(max_length=255)
    archive = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.nom_du_droit


class Profils(models.Model):
    nom = models.CharField(max_length=255, null=True)
    archive = models.BooleanField(default=False, null=True)
    droits = models.ManyToManyField(Droits, through="DroitsProfils")

    def __str__(self):
        return self.nom


class DroitsProfils(models.Model):
    profil = models.ForeignKey(Profils, on_delete=models.SET_NULL, null=True)
    droit = models.ForeignKey(Droits, on_delete=models.SET_NULL, null=True)
    ecriture = models.BooleanField(default=False, null=True)
    lecture = models.BooleanField(default=False, null=True)
    modification = models.BooleanField(default=False, null=True)
    suppression = models.BooleanField(default=False, null=True)


class UserManager(auth_models.BaseUserManager):

    def create_user(self, nom_d_utilisateur, adresse, nom, prenom, password=None):
        if not nom_d_utilisateur:
            raise ValueError('Users must have an telephone number')
        user = self.model(nom_d_utilisateur=nom_d_utilisateur)
        user.adresse = adresse
        user.nom = nom
        user.prenom = prenom
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nom_d_utilisateur, adresse, nom, prenom, password):
        user = self.create_user(
            nom_d_utilisateur,
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
    nom_d_utilisateur = models.CharField(unique=True, max_length=255, null=True, blank=False,
                                         help_text="Le nom d'utilisateur servira à se connecter à la plateforme, "
                                                   "également pour parrainer un membre. Ex. toto21")
    nom_du_parent = models.ForeignKey("self", on_delete=models.SET_NULL, verbose_name='Parrain',
                                      help_text="Indiquez le parent qui l'adhère. S'il est le premier membre de son "
                                                "groupe, laissez vide", null=True, blank=True)
    nom = models.CharField(max_length=255, null=True)
    prenom = models.CharField(max_length=255, blank=False, null=True)
    adresse = models.CharField(max_length=255, null=True, blank=False)
    pays_de_residence = models.ForeignKey(CodePays, on_delete=models.SET_NULL, null=True, blank=False)
    telephone = models.BigIntegerField(blank=False, null=True, unique=True)
    # telephone = models.CharField(max_length=25, blank=False, null=True, unique=True)
    poste = models.ForeignKey(Poste, null=True, blank=True, on_delete=models.SET_NULL)
    palier = models.ForeignKey(Palier, null=True, blank=True, on_delete=models.SET_NULL)
    groupe = models.ForeignKey(Groupe, null=True, blank=False, on_delete=models.SET_NULL,
                               verbose_name="Nom de l'équipe",
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
    ########################################################
    don_bam = models.BooleanField(default=False, null=True)
    don_zou = models.BooleanField(default=False, null=True)
    don_maya = models.BooleanField(default=False, null=True)
    don_mand = models.BooleanField(default=False, null=True)
    ########################################################

    profil = models.ForeignKey(Profils, on_delete=models.SET_NULL, null=True, blank=True)
    pied_gauche = models.BooleanField(default=False, null=True, blank=False)
    pied_droit = models.BooleanField(default=False, null=True, blank=False)
    nb_pers_amene = models.PositiveSmallIntegerField(null=True, blank=False, default=0)
    point = models.PositiveSmallIntegerField(null=True, blank=False, default=0)
    stock_point = models.PositiveSmallIntegerField(null=True, blank=False, default=0)
    point_fictive_inv = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    point_fictive_col = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    point_fictive_manag = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    # gam = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    gam = models.DecimalField(null=True, blank=True, default=0, decimal_places=2, max_digits=5)

    """
    Django settings
    """
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_d_ajout = models.DateTimeField(auto_now_add=True, null=True,
                                        verbose_name="Date d'enrégistrement de l'utilisateur")

    objects = UserManager()

    USERNAME_FIELD = 'nom_d_utilisateur'
    REQUIRED_FIELDS = ['nom', 'prenom', 'adresse']

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateur'
        ordering = ('id',)

    def __str__(self):
        return self.nom + ' ' + self.prenom

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
        return u'{0} {1}'.format(self.nom, self.prenom)


class Payement(models.Model):
    libelle = models.CharField(max_length=255, null=True, default="Payement")
    montant = models.DecimalField(null=True, max_digits=15, decimal_places=1)
    membre = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    poursuivre = models.BooleanField(null=True, blank=False)
    etat = models.BooleanField(default=True, null=True, blank=True)
    date_d_ajout = models.DateTimeField(auto_now_add=True, null=True)
    archive = models.BooleanField(default=False, null=True)


class Wara(models.Model):
    nom = models.CharField(max_length=255, null=True)
    prenom = models.CharField(max_length=255, null=True)
    telephone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    parrain = models.CharField(max_length=150, null=True, blank=True)
    archive = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)


class Message(models.Model):
    email = models.EmailField(null=True)
    message = models.TextField(null=True)
    archive = models.BooleanField(default=False, null=True)


###########################################    PROGRAMME WARA      ###################################################

class Versions(models.Model):
    nom_de_version = models.CharField(max_length=50, null=True)
    libelle = models.CharField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    archive = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.nom_de_version


class Modules(models.Model):
    version = models.ForeignKey(Versions, on_delete=models.SET_NULL, null=True, verbose_name="Version Wara")
    nom_du_module = models.CharField(max_length=100, null=True, verbose_name="Nom du module")
    intro_text = models.TextField(null=True, blank=True, verbose_name="Mot d'introduction")

    video6 = models.FileField(null=True, blank=True, upload_to="wara/%y %m %d", verbose_name="Fichier vidéo 1")
    texte6 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Intitulé du fichier video")
    longueur_video6 = models.FloatField(null=True, blank=True)
    temps_lu_video6 = models.FloatField(null=True, blank=True)

    video7 = models.FileField(null=True, blank=True, upload_to="wara/%y %m %d", verbose_name="Fichier vidéo 2")
    texte7 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Intitulé du fichier video")
    longueur_video7 = models.FloatField(null=True, blank=True)
    temps_lu_video7 = models.FloatField(null=True, blank=True)

    video8 = models.FileField(null=True, blank=True, upload_to="wara/%y %m %d", verbose_name="Fichier vidéo 3")
    texte8 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Intitulé du fichier video")
    longueur_video8 = models.FloatField(null=True, blank=True)
    temps_lu_video8 = models.FloatField(null=True, blank=True)

    video9 = models.FileField(null=True, blank=True, upload_to="wara/%y %m %d", verbose_name="Fichier vidéo 4")
    texte9 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Intitulé du fichier video")
    longueur_video9 = models.FloatField(null=True, blank=True)
    temps_lu_video9 = models.FloatField(null=True, blank=True)

    video10 = models.FileField(null=True, blank=True, upload_to="wara/%y %m %d", verbose_name="Fichier vidéo 5")
    texte10 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Intitulé du fichier video")
    longueur_video10 = models.FloatField(null=True, blank=True)
    temps_lu_video10 = models.FloatField(null=True, blank=True)

    audio1 = models.FileField(null=True, blank=True, upload_to="wara/%y %m %d", verbose_name="Fichier audio 1")
    texte1 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Intitulé du fichier audio")
    longueur_audio1 = models.FloatField(null=True, blank=True)
    temps_lu_audio1 = models.FloatField(null=True, blank=True)

    audio2 = models.FileField(null=True, blank=True, upload_to="wara/%y %m %d", verbose_name="Fichier audio 2")
    texte2 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Intitulé du fichier audio")
    longueur_audio2 = models.FloatField(null=True, blank=True)
    temps_lu_audio2 = models.FloatField(null=True, blank=True)

    audio3 = models.FileField(null=True, blank=True, upload_to="wara/%y %m %d", verbose_name="Fichier audio 3")
    texte3 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Intitulé du fichier audio")
    longueur_audio3 = models.FloatField(null=True, blank=True)
    temps_lu_audio3 = models.FloatField(null=True, blank=True)

    audio4 = models.FileField(null=True, blank=True, upload_to="wara/%y %m %d", verbose_name="Fichier audio 4")
    texte4 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Intitulé du fichier audio")
    longueur_audio4 = models.FloatField(null=True, blank=True)
    temps_lu_audio4 = models.FloatField(null=True, blank=True)

    audio5 = models.FileField(null=True, blank=True, upload_to="wara/%y %m %d", verbose_name="Fichier audio 5")
    texte5 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Intitulé du fichier audio")
    longueur_audio5 = models.FloatField(null=True, blank=True)
    temps_lu_audio5 = models.FloatField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    archive = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.nom_du_module


class Vague(models.Model):
    nom_de_vague = models.CharField(max_length=150, null=True, blank=True)
    version = models.ForeignKey(Versions, on_delete=models.SET_NULL, null=True)
    utilisateurs = models.ManyToManyField(User, verbose_name="Participants")
    date_deb = models.DateField(null=True, verbose_name="Date de début de la formation")
    date_fin = models.DateField(null=True, verbose_name="Date de clôture de la formation")

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    archive = models.BooleanField(default=False, null=True, blank=True)
