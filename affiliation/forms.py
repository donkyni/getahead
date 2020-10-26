from django import forms

from affiliation.models import User, CodePays, Poste


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    date_de_naissance = forms.DateTimeField(widget=DateInput)

    class Meta:
        model = User
        fields = (
            'code', 'nom_du_parent', 'nom', 'prenom', 'adresse',
            'pays_de_residence', 'telephone', 'poste', 'palier', 'groupe',
            'avatar', 'date_de_naissance', 'sexe',
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
    date_de_naissance = forms.DateTimeField(widget=DateInput)

    class Meta:
        model = User
        fields = (
            'code', 'nom_du_parent', 'nom', 'prenom', 'adresse',
            'pays_de_residence', 'telephone', 'poste', 'palier', 'groupe',
            'avatar', 'date_de_naissance', 'sexe',
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'nom', 'prenom', 'adresse', 'pays_de_residence', 'telephone',
            'avatar', 'date_de_naissance', 'sexe',
        )


class PosteForm(forms.ModelForm):
    class Meta:
        model = Poste
        fields = ('nom_du_poste',)


class CodePaysForm(forms.ModelForm):
    class Meta:
        model = CodePays
        fields = ('pays', 'code_pays',)
