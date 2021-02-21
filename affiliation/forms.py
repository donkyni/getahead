from django import forms

from affiliation.models import User, CodePays, Poste, Niveau, Palier, Groupe, Payement, Wara, Message, Versions, \
    Modules, Vague


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'nom_d_utilisateur', 'nom_du_parent', 'nom', 'prenom', 'adresse',
            'pays_de_residence', 'telephone', 'groupe',
            'avatar', 'sexe',
        )
        widgets = {
            'nom_du_parent': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'pays_de_residence': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'groupe': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'nom_d_utilisateur', 'nom_du_parent', 'nom', 'prenom', 'adresse',
            'pays_de_residence', 'telephone', 'groupe',
            'avatar', 'sexe',
        )


class UserUpdateForm(forms.ModelForm):
    annee_de_naissance = forms.DateTimeField(widget=DateInput)
    nom_d_utilisateur = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = (
            'nom_d_utilisateur', 'nom', 'prenom', 'adresse', 'pays_de_residence', 'telephone',
            'avatar', 'annee_de_naissance', 'sexe',
        )


class PosteForm(forms.ModelForm):
    class Meta:
        model = Poste
        fields = ('nom_du_poste',)


class CodePaysForm(forms.ModelForm):
    class Meta:
        model = CodePays
        fields = ('pays', 'code_pays',)


class NiveauForm(forms.ModelForm):
    class Meta:
        model = Niveau
        fields = ('nom_du_niveau',)


class PalierForm(forms.ModelForm):
    class Meta:
        model = Palier
        fields = ('nom_du_palier', 'niveau',)


class GroupeForm(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = ('nom_du_groupe', 'manageur_du_groupe',)


class PayementForm(forms.ModelForm):
    class Meta:
        model = Payement
        fields = ('libelle', 'montant', 'membre',)
        exclude = ('etat', 'archive')
        widgets = {
            'membre': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
        }


class PayementFormUser(forms.ModelForm):
    class Meta:
        model = Payement
        fields = ('etat',)
        widgets = {
            'etat': forms.CheckboxInput(attrs={'class': 'form-control'})
        }


class WaraForm(forms.ModelForm):
    class Meta:
        model = Wara
        fields = ('nom', 'prenom', 'telephone', 'email', 'parrain')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('email', 'message',)


###################################################################################################

class VersionsForm(forms.ModelForm):
    class Meta:
        model = Versions
        fields = ('nom_de_version',)


class ModulesForm(forms.ModelForm):
    class Meta:
        model = Modules
        exclude = ('created', 'archive', )

        widgets = {
            'version': forms.Select(attrs={'class': 'form-control'}),
            'nom_du_module': forms.TextInput(attrs={'class': 'form-control'}),
            'intro_text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class VagueForm(forms.ModelForm):
    class Meta:
        model = Vague
        exclude = ('created', 'archive', )

        widgets = {
            'nom_de_vague': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'utilisateurs': forms.SelectMultiple(attrs={'class': 'selectpicker', 'multiple data-live-search': 'true'}),
        }
