from django import forms

from affiliation.models import User, CodePays, Poste, Niveau, Palier, Groupe, Parent


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    annee_de_naissance = forms.DateTimeField(widget=DateInput)

    class Meta:
        model = User
        fields = (
            'code', 'nom_du_parent', 'nom', 'prenom', 'adresse',
            'pays_de_residence', 'telephone', 'poste', 'palier', 'groupe',
            'avatar', 'annee_de_naissance', 'sexe',
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


class UserForm(forms.ModelForm):
    annee_de_naissance = forms.DateTimeField(widget=DateInput)

    class Meta:
        model = User
        fields = (
            'code', 'nom_du_parent', 'nom', 'prenom', 'adresse',
            'pays_de_residence', 'telephone', 'poste', 'palier', 'groupe',
            'avatar',  'annee_de_naissance', 'sexe',
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'nom', 'prenom', 'adresse', 'pays_de_residence', 'telephone',
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


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ('nom_du_parent', 'code_du_parent',)
