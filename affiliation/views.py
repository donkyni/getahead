import datetime
from decimal import Decimal

from random import shuffle

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from affiliation.forms import UserCreationForm, CodePaysForm, PosteForm, NiveauForm, PalierForm, GroupeForm, \
    UserUpdateForm, PayementFormUser, PayementForm, WaraForm, MessageForm, VersionsForm, ModulesForm, VagueForm, \
    UserCreation20Form, ActivationForm, SujetForumForm, MessagesSujetsForumsForm, ForumForm
from affiliation.models import User, CodePays, Poste, Niveau, Palier, Groupe, Payement, Profils, DroitsProfils, Droits, \
    Wara, Versions, Modules, Vague, Packs, Forums, SujetForum, MessagesSujetsForums


def acceuil(request):
    if request.method == 'POST':
        w_form = WaraForm(request.POST)
        if w_form.is_valid():
            w_form.save()
            redirect('acceuil')
    else:
        w_form = WaraForm()

    if request.method == 'POST':
        m_form = MessageForm(request.POST)
        if m_form.is_valid():
            m_form.save()
            redirect('acceuil')
    else:
        m_form = MessageForm()

    context = {
        'w_form': w_form,
        'm_form': m_form
    }

    return render(request, 'acceuil.html', locals())


def cabinet(request):
    return render(request, 'cabinet_jgk_ec.html', locals())


def presentation(request):
    return render(request, 'presentation_get_ahead.html', locals())


def programme(request):
    return render(request, 'programme_wara.html', locals())


def controllers(request, url, droit, context):
    user_profil = request.user.profil
    dict = {}
    if user_profil:
        profils = get_object_or_404(Profils, nom=user_profil)
        droits = get_object_or_404(Droits, nom_du_droit=droit)
        if profils:
            permissions = DroitsProfils.objects.filter(profil=profils, droit=droits)
            dict[profils] = permissions
            for permission in permissions:
                if permission.lecture:
                    print(permission)
                    return render(request, url, context)
                else:
                    return render(request, 'access_denied.html')


@login_required
def save_all(request, form, template_name, model, template_name2, mycontext):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            if model == "niveau1":
                form.save(commit=False)
                system = form.save()

                bam = system.membre.palier.nom_du_palier
                id_membre = system.membre.id
                print(id_membre)

                if bam == "Bamiléké":
                    member = get_object_or_404(User, id=id_membre)
                    member.don_bam = True
                    member.save()
                    print(member)

                if bam == "Zoulou":
                    member = get_object_or_404(User, id=id_membre)
                    member.don_bam = True
                    # member.don_zou = True
                    member.save()
                    print(member)

                    print(member.don_bam, member.don_zou)
                if bam == "Maya":
                    member = get_object_or_404(User, id=id_membre)
                    member.don_bam = True
                    # member.don_zou = True
                    # member.don_maya = True
                    member.save()
                    print(member)

                if bam == "Mandingue":
                    member = get_object_or_404(User, id=id_membre)
                    member.don_bam = True
                    # member.don_zou = True
                    # member.don_maya = True
                    # member.don_mand = True
                    member.save()
                    print(member)

                system.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
            else:
                form.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
        else:
            data['form_is_valid'] = False

    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def tableaudebord(request):
    droit = "Dashboard"
    niveau = get_object_or_404(Niveau, nom_du_niveau="Niveau 1")
    membres = User.objects.all()[:5]

    for membre in membres:
        if membre.palier is not None:
            if membre.palier.nom_du_palier == "Bamiléké":
                point = membre.point
                progress_bar_bam = int(point * (100 / 30))
            elif membre.palier.nom_du_palier == "Zoulou":
                point = membre.point
                progress_bar_zou = int(point * (100 / 120))
            elif membre.palier.nom_du_palier == "Maya":
                point = membre.point
                progress_bar_maya = int(point * (100 / 480))
            elif membre.palier.nom_du_palier == "Mandingue":
                point = membre.point
                progress_bar_mand = int(point * (100 / 1920))

    bamileke = get_object_or_404(Palier, nom_du_palier="Bamiléké")
    total_pers_bam = User.objects.filter(palier=bamileke).count()

    zoulou = get_object_or_404(Palier, nom_du_palier="Zoulou")
    total_pers_zou = User.objects.filter(palier=zoulou).count()

    maya = get_object_or_404(Palier, nom_du_palier="Maya")
    total_pers_maya = User.objects.filter(palier=maya).count()

    mandingue = get_object_or_404(Palier, nom_du_palier="Mandingue")
    total_pers_mand = User.objects.filter(palier=mandingue).count()

    # recuperer les membres selon leur dates
    memb_janv = User.objects.filter(
        date_d_ajout=datetime.date(2020, 1, 1)
    )
    data = [43, 65, 27, 89, 30, 12, 150]
    data2 = [34, 56, 72, 40, 13, 21, 51]

    return controllers(request, 'affiliation/tableaudebord.html', droit, locals())


def list_total_pers_pymt(request):
    bam = get_object_or_404(Palier, nom_du_palier="Bamiléké")
    poste = get_object_or_404(Poste, nom_du_poste="Manageur")
    manageurs_bam = User.objects.filter(palier=bam, poste=poste, point=30)

    zoulou = get_object_or_404(Palier, nom_du_palier="Zoulou")
    total_pers_zou = User.objects.filter(palier=zoulou)

    maya = get_object_or_404(Palier, nom_du_palier="Maya")
    total_pers_maya = User.objects.filter(palier=maya)

    mandingue = get_object_or_404(Palier, nom_du_palier="Mandingue")
    total_pers_mand = User.objects.filter(palier=mandingue)

    return render(request, 'affiliation/list_total_pers_pymt.html', locals())


@login_required
def compte(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,
                                request.FILES,
                                instance=request.user)
        if u_form.is_valid():
            u_form.save()
            redirect('compte')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
    }
    return render(request, 'affiliation/mon_espace/info_de_compte.html', context)


@login_required
def mongroupe(request):

    groupe = request.user.groupe
    # parrain = request.user
    if request.user.nom_du_parent is not None:
        parrain = get_object_or_404(User, id=request.user.nom_du_parent.id)
    payements = Payement.objects.filter(archive=False, membre=request.user)

    if request.user.palier is not None:
        bam = get_object_or_404(Palier, nom_du_palier="Bamiléké")
        membres_bam = User.objects.filter(palier=bam)
        zou = get_object_or_404(Palier, nom_du_palier="Zoulou")
        membres_zou = User.objects.filter(palier=zou)
        maya = get_object_or_404(Palier, nom_du_palier="Maya")
        membres_maya = User.objects.filter(palier=maya)
        mand = get_object_or_404(Palier, nom_du_palier="Mandingue")
        membres_mand = User.objects.filter(palier=mand)

    if request.user.palier is not None:
        if request.user.palier.nom_du_palier == "Bamiléké":
            point = request.user.point
            progress_bar_bam = int(point * (100 / 30))
        elif request.user.palier.nom_du_palier == "Zoulou":
            point = request.user.point
            progress_bar_zou = int(point * (100 / 120))
        elif request.user.palier.nom_du_palier == "Maya":
            point = request.user.point
            progress_bar_maya = int(point * (100 / 480))
        elif request.user.palier.nom_du_palier == "Mandingue":
            point = request.user.point
            progress_bar_mand = int(point * (100 / 1920))

    if request.user.nb_pers_amene >= 2:
        nb_pers_total = request.user.nb_pers_amene
        solde = request.user.gam * 2000
    elif request.user.nb_pers_amene < 2:
        solde = 0

    import uuid

    utilisateur = request.user
    if utilisateur.unique_id is None:
        utilisateur.unique_id = uuid.uuid4()
        utilisateur.save()

    context = {
        'groupe': groupe,

    }

    return render(request, 'affiliation/mon_espace/mon_groupe.html', locals())


@login_required
def voirmongroupe(request):
    groupe = request.user.groupe
    parrain = get_object_or_404(User, id=request.user.id)

    if request.user.palier is not None:
        mon_groupe = User.objects.filter(groupe=groupe)

    context = {
        'groupe': groupe,
        'parrain': parrain,
    }

    return render(request, 'affiliation/mon_espace/voirmongroupe.html', locals())


def voir_membre_palier_id(request, id):
    bam = get_object_or_404(Palier, id=id)
    membres_bam = User.objects.filter(palier=bam)
    zou = get_object_or_404(Palier, id=id)
    membres_zou = User.objects.filter(palier=zou)
    maya = get_object_or_404(Palier, id=id)
    membres_maya = User.objects.filter(palier=maya)
    mand = get_object_or_404(Palier, id=id)
    membres_mand = User.objects.filter(palier=mand)

    context = {
        'membres_bam': membres_bam,
        'membres_zou': membres_zou,
        'membres_maya': membres_maya,
        'membres_mand': membres_mand,
    }

    return render(request, 'affiliation/mon_espace/voir_membre_palier.html', context)


@login_required
def bamileke(request):
    droit = "Bamiléké"
    bam = get_object_or_404(Palier, nom_du_palier="Bamiléké")
    poste = get_object_or_404(Poste, nom_du_poste="Manageur")
    manageurs_bam = User.objects.filter(palier=bam, poste=poste, point=30, don_bam=False)

    zoulou = get_object_or_404(Palier, nom_du_palier="Zoulou")
    manageurs_zou = User.objects.filter(palier=zoulou, don_bam=False)

    maya = get_object_or_404(Palier, nom_du_palier="Maya")
    manageurs_maya = User.objects.filter(palier=maya, don_bam=False)

    mandingue = get_object_or_404(Palier, nom_du_palier="Mandingue")
    manageurs_mand = User.objects.filter(palier=mandingue, don_bam=False)

    return controllers(request, 'affiliation/niveau1/bamileke.html', droit, locals())


@login_required
def save_all_zou(request, form, template_name, model, template_name2, mycontext):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            if model == "niveau1":
                form.save(commit=False)
                system = form.save()

                bam = system.membre.palier.nom_du_palier
                id_membre = system.membre.id
                print(id_membre)

                if bam == "Zoulou":
                    member = get_object_or_404(User, id=id_membre)
                    # member.don_bam = True
                    member.don_zou = True
                    member.save()
                    print(member)

                    print(member.don_bam, member.don_zou)
                if bam == "Maya":
                    member = get_object_or_404(User, id=id_membre)
                    # member.don_bam = True
                    member.don_zou = True
                    # member.don_maya = True
                    member.save()
                    print(member)

                if bam == "Mandingue":
                    member = get_object_or_404(User, id=id_membre)
                    # member.don_bam = True
                    member.don_zou = True
                    # member.don_maya = True
                    # member.don_mand = True
                    member.save()
                    print(member)

                system.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
            else:
                form.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
        else:
            data['form_is_valid'] = False

    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def createpayementzou(request):
    payements = Payement.objects.filter(archive=False)
    mycontext = {
        'payements': payements
    }
    if request.method == 'POST':
        form = PayementForm(request.POST)
    else:
        form = PayementForm()
    return save_all_zou(request, form, 'affiliation/niveau1/createpayementzou.html', 'niveau1',
                        'affiliation/niveau1/listepayement.html', mycontext)


@login_required
def zoulou(request):
    droit = "Zoulou"
    zou = get_object_or_404(Palier, nom_du_palier="Zoulou")
    poste = get_object_or_404(Poste, nom_du_poste="Manageur")

    manageurs_zou = User.objects.filter(palier=zou, poste=poste, point=120, don_zou=False)

    maya = get_object_or_404(Palier, nom_du_palier="Maya")
    manageurs_maya = User.objects.filter(palier=maya, don_zou=False)

    mandingue = get_object_or_404(Palier, nom_du_palier="Mandingue")
    manageurs_mand = User.objects.filter(palier=mandingue, don_zou=False)

    context = {
        'manageurs_zou': manageurs_zou,
        'manageurs_maya': manageurs_maya,
        'manageurs_mand': manageurs_mand,
    }

    return controllers(request, 'affiliation/niveau1/zoulou.html', droit, context)


@login_required
def save_all_maya(request, form, template_name, model, template_name2, mycontext):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            if model == "niveau1":
                form.save(commit=False)
                system = form.save()

                bam = system.membre.palier.nom_du_palier
                id_membre = system.membre.id
                print(id_membre)

                if bam == "Maya":
                    member = get_object_or_404(User, id=id_membre)
                    # member.don_bam = True
                    # member.don_zou = True
                    member.don_maya = True
                    member.save()
                    print(member)

                if bam == "Mandingue":
                    member = get_object_or_404(User, id=id_membre)
                    # member.don_bam = True
                    # member.don_zou = True
                    member.don_maya = True
                    # member.don_mand = True
                    member.save()
                    print(member)

                system.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
            else:
                form.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
        else:
            data['form_is_valid'] = False

    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def createpayementmaya(request):
    payements = Payement.objects.filter(archive=False)
    mycontext = {
        'payements': payements
    }
    if request.method == 'POST':
        form = PayementForm(request.POST)
    else:
        form = PayementForm()
    return save_all_zou(request, form, 'affiliation/niveau1/createpayementmaya.html', 'niveau1',
                        'affiliation/niveau1/listepayement.html', mycontext)


@login_required
def maya(request):
    droit = "Maya"
    maya = get_object_or_404(Palier, nom_du_palier="Maya")
    poste = get_object_or_404(Poste, nom_du_poste="Manageur")

    manageurs_maya = User.objects.filter(palier=maya, poste=poste, point=480, don_maya=False)

    mandingue = get_object_or_404(Palier, nom_du_palier="Mandingue")
    manageurs_mand = User.objects.filter(palier=mandingue, don_maya=False)

    context = {
        'manageurs_maya': manageurs_maya,
        'manageurs_mand': manageurs_mand,
    }

    return controllers(request, 'affiliation/niveau1/maya.html', droit, context)


@login_required
def mandingue(request):
    droit = "Mandingue"
    mand = get_object_or_404(Palier, nom_du_palier="Mandingue")
    poste = get_object_or_404(Poste, nom_du_poste="Manageur")
    manageurs_mand = User.objects.filter(palier=mand, poste=poste, point=1920)

    context = {
        'manageurs_mand': manageurs_mand
    }

    return controllers(request, 'affiliation/niveau1/mandingue.html', droit, context)


def payement(request):
    payements = Payement.objects.filter(archive=False)
    mycontext = {
        'payements': payements,
    }
    return render(request, 'affiliation/niveau1/payement.html', mycontext)


def createpayement(request):
    payements = Payement.objects.filter(archive=False)
    mycontext = {
        'payements': payements
    }
    if request.method == 'POST':
        form = PayementForm(request.POST)
    else:
        form = PayementForm()
    return save_all(request, form, 'affiliation/niveau1/createpayement.html', 'niveau1',
                    'affiliation/niveau1/listepayement.html', mycontext)


def updatepayement(request, id):
    payements = Payement.objects.all()
    mycontext = {
        'payements': payements
    }
    payement = get_object_or_404(Payement, id=id)
    if request.method == 'POST':
        form = PayementForm(request.POST, instance=payement)
    else:
        form = PayementForm(instance=payement)
    return save_all(request, form, 'affiliation/niveau1/updatepayement.html', 'niveau1',
                    'ressources/salaire/listepayement.html', mycontext)


def deletepayement(request, id):
    data = dict()
    payement = get_object_or_404(Payement, id=id)
    if request.method == "POST":
        payement.archive = True
        payement.save()
        data['form_is_valid'] = True
        payements = Payement.objects.filter(archive=False)
        data['niveau1'] = render_to_string('affiliation/niveau1/listepayement.html', {'payements': payements})
    else:
        context = {
            'payement': payement
        }
        data['html_form'] = render_to_string('affiliation/niveau1/deletepayement.html', context, request=request)

    return JsonResponse(data)


def validerpayement(request, id):
    payements = Payement.objects.filter(archive=False, membre=request.user)
    mycontext = {
        'payements': payements
    }
    payement = get_object_or_404(Payement, id=id)
    if request.method == 'POST':
        form = PayementFormUser(request.POST, instance=payement)
    else:
        form = PayementFormUser(instance=payement)
    return save_all(request, form, 'affiliation/mon_espace/validerpayement.html', 'payement',
                    'affiliation/mon_espace/listpayement.html', mycontext)


@login_required
def poste(request):
    droit = "Postes"
    postes = Poste.objects.filter(archive=False)
    mycontext = {
        'postes': postes
    }
    return controllers(request, 'affiliation/poste/poste.html', droit, mycontext)


def createposte(request):
    postes = Poste.objects.filter(archive=False)
    if request.method == 'POST':
        form = PosteForm(request.POST)
    else:
        form = PosteForm()
    mycontext = {'postes': postes, 'form': form}
    return save_all(request, form, 'affiliation/poste/createposte.html',
                    'poste', 'affiliation/poste/listeposte.html', mycontext)


def updateposte(request, id):
    postes = CodePays.objects.filter(archive=False)
    mycontext = {
        'postes': postes
    }
    poste = get_object_or_404(Poste, id=id)
    if request.method == 'POST':
        form = PosteForm(request.POST, instance=poste)
    else:
        form = PosteForm(instance=poste)

    return save_all(request, form, 'affiliation/poste/updateposte.html',
                    'poste', 'affiliation/poste/listeposte.html', mycontext)


@login_required
def deleteposte(request, id):
    data = dict()
    poste = get_object_or_404(Poste, id=id)
    if request.method == "POST":
        poste.archive = True
        poste.save()
        data['form_is_valid'] = True
        postes = Poste.objects.filter(archive=False)
        data['poste'] = render_to_string('affiliation/poste/listeposte.html', {'postes': postes})
    else:
        context = {
            'poste': poste
        }
        data['html_form'] = render_to_string('affiliation/poste/deleteposte.html', context, request=request)

    return JsonResponse(data)


def generateuniqueid(longueur):
    caracteres = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                  '&', '=', '#', '|', '?', '@', '$', '*', 'µ', '%', '!', '/',
                  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    mdp = str()
    shuffle(caracteres)
    for x in range(longueur):
        mdp += caracteres[x]
    return mdp


@login_required
def ajouter(request):
    dict = {}
    utilisateurs = User.objects.all()
    invite = User.objects.filter(poste__nom_du_poste="Invité").count()
    total_membre = User.objects.all().count()

    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            systeme = form.save()
            poste_inv = get_object_or_404(Poste, nom_du_poste="Invité")
            palier_bam = get_object_or_404(Palier, nom_du_palier="Bamiléké")
            systeme.poste = poste_inv
            systeme.palier = palier_bam
            systeme.dix_milles = True

            profil = get_object_or_404(Profils, nom="Utilisateur")
            systeme.profil = profil

            # Faire une MAJ par rapport au groupe de l'adhérent, donc de retrouver le groupe de ce dernier
            group = systeme.groupe
            groupe = get_object_or_404(Groupe, nom_du_groupe=group)

            if groupe:  # Si on a le groupe recherché alors '->
                membres = User.objects.filter(groupe=group)  # On recupère tous ses membres
                dict[groupe] = membres

                nom_d_utilisateur = systeme.nom_d_utilisateur
                membre = get_object_or_404(User, nom_d_utilisateur=nom_d_utilisateur)
                if membre.nom_du_parent is None:
                    print(membre.nom_du_parent)
                    print("C'est le plus haut parent")
                    systeme.save()
                elif membre.nom_du_parent is not None:
                    while membre.nom_du_parent is not None:
                        """
                        Quand on place un membre dans un groupe pour avoir un gam,
                        tout se passe bien sauf qu'au moment ou ce dernier qui a ete placé decide
                        de mettre un invité sous lui, non seulement il recoit les points
                        mais aussi son parrain dans l'autre groupe et ainsi de suite recoit les points
                        """
                        membre = get_object_or_404(User, id=membre.nom_du_parent.id)
                        # membre = get_object_or_404(User, id=membre.nom_du_parent.id, groupe=group)
                        # membre.point += 5
                        total_parrainages = User.objects.filter(nom_du_parent=membre).count()
                        membre.nb_pers_amene = total_parrainages
                        if total_parrainages > 2 and membre == systeme.nom_du_parent:
                            if groupe == membre.groupe:
                                if membre.palier.nom_du_palier == "Bamiléké":

                                    if membre.dix_milles:
                                        membre.point += 5  # ce n'est qu'a ce palier qu'on donne du point aux
                                        # parents lors de l'enregistrement de l'un de ses filleuls
                                    elif not membre.dix_milles:
                                        membre.point_a_affecter += 5  # On stocke le point dans une variable
                                        # pour tous les utilisateurs qui n'ont pas encore payé leur frais de
                                        # formation 10.000
                                        # Les points sont cumulées une fois l'administrateur change l'etat en True
                                        # depuis son espace

                                    if 0 <= membre.point < 5:
                                        poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste_invite
                                        membre.point_fictive_inv = 0
                                        print("Vous etes un invité, recruter 2 membres pour devenir un colibri")
                                    elif membre.point == 5:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes un colibri")
                                        membre.point_fictive_col = 5
                                    elif membre.point == 10:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes un colibri reconnu")
                                        membre.point_fictive_col = 10
                                    elif 15 <= membre.point < 30:
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print("Vous etes manageur")
                                        if membre.point == 15:
                                            membre.point_fictive_manag = 15
                                        elif membre.point == 20:
                                            membre.point_fictive_manag = 20
                                        elif membre.point == 25:
                                            membre.point_fictive_manag = 25
                                    elif membre.point == 30:
                                        membre.stock_point = 30  # ICI ON STOCK LE POINT DU PALIER CI POUR LA SUITE
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print(
                                            "Vous etes manageur reconnu et avez fini ce palier, Voulez-vous continuer "
                                            "pour le palier suviant ou arreter ?")
                                        membre.point_fictive_manag = 30
                                    elif membre.point == 35:
                                        membre.point = 5
                                        poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste
                                        palier_zoulou = get_object_or_404(Palier, nom_du_palier="Zoulou")
                                        membre.palier = palier_zoulou
                                        member_pursue_bam = 700/2000
                                        membre.gam = membre.gam + Decimal(member_pursue_bam)
                                        print("Applique Gam")

                                elif membre.palier.nom_du_palier == "Zoulou":

                                    if membre.dix_milles:
                                        membre.point += 5
                                    elif not membre.dix_milles:
                                        membre.point_a_affecter += 5

                                    if membre.point == 5:
                                        poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste_invite
                                        print("Vous etes invité")
                                        membre.point_fictive_inv = 0
                                    if 5 < membre.point < 40:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes colibri")
                                        membre.point_fictive_col = 5
                                    if membre.point == 40:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes colibri reconnu")
                                        membre.point_fictive_col = 10
                                    elif 40 < membre.point < 120:
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print("Vous etes manageur")
                                        if membre.point == 45:
                                            membre.point_fictive_manag = 15
                                        elif 45 < membre.point == 75:
                                            membre.point_fictive_manag = 20
                                        elif 75 < membre.point == 115:
                                            membre.point_fictive_manag = 25
                                    elif membre.point == 120:
                                        membre.stock_point += 120  # ici on devrait avoir 30 + 120 = 150 points
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print(
                                            "Vous etes manageur reconnu et avez fini ce palier, Voulez-vous continuer "
                                            "pour le palier suviant ou arreter ?")
                                        membre.point_fictive_manag = 30
                                    elif membre.point == 125:
                                        membre.point = 5
                                        poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste
                                        palier_maya = get_object_or_404(Palier, nom_du_palier="Maya")
                                        membre.palier = palier_maya
                                        member_pursue_zou = 1000/2000
                                        membre.gam = membre.gam + Decimal(member_pursue_zou)

                                elif membre.palier.nom_du_palier == "Maya":

                                    if membre.dix_milles:
                                        membre.point += 5
                                    elif not membre.dix_milles:
                                        membre.point_a_affecter += 5

                                    if membre.point == 5:
                                        poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste_invite
                                        print("Vous etes invité")
                                        membre.point_fictive_inv = 0
                                    if 5 < membre.point < 160:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes colibri")
                                        membre.point_fictive_col = 5
                                    if membre.point == 160:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes colibri reconnu")
                                        membre.point_fictive_col = 10
                                    elif 160 < membre.point < 480:
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print("Vous etes manageur")
                                        if membre.point == 165:
                                            membre.point_fictive_manag = 15
                                        elif 45 < membre.point == 315:
                                            membre.point_fictive_manag = 20
                                        elif 75 < membre.point == 475:
                                            membre.point_fictive_manag = 25
                                    elif membre.point == 480:
                                        membre.stock_point += 480  # ici on devrait avoir 150 + 480 = 630 points
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print(
                                            "Vous etes manageur reconnu et avez fini ce palier, Voulez-vous continuer "
                                            "pour le palier suviant ou arreter ?")
                                        membre.point_fictive_manag = 30
                                    elif membre.point == 485:
                                        membre.point = 5
                                        poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste
                                        palier_mandingue = get_object_or_404(Palier, nom_du_palier="Mandingue")
                                        membre.palier = palier_mandingue
                                        member_pursue_maya = 2000/2000
                                        membre.gam = membre.gam + Decimal(member_pursue_maya)

                                elif membre.palier.nom_du_palier == "Mandingue":

                                    if membre.dix_milles:
                                        membre.point += 5
                                    elif not membre.dix_milles:
                                        membre.point_a_affecter += 5

                                    if membre.point == 5:
                                        poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste_invite
                                        print("Vous etes invité")
                                        membre.point_fictive_inv = 0
                                    if 5 < membre.point < 640:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes colibri")
                                        membre.point_fictive_col = 5
                                    if membre.point == 640:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes colibri reconnu")
                                        membre.point_fictive_col = 10
                                    elif 640 < membre.point < 1920:
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print("Vous etes manageur")
                                        if membre.point == 645:
                                            membre.point_fictive_manag = 15
                                        elif 45 < membre.point == 1275:
                                            membre.point_fictive_manag = 20
                                        elif 75 < membre.point == 1915:
                                            membre.point_fictive_manag = 25
                                    elif membre.point == 1920:
                                        membre.stock_point += 1920  # ici on devrait avoir 150 + 480 + 1920 = 2550
                                        # points
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print(
                                            "Vous etes manageur reconnu et avez fini ce palier, Voulez-vous continuer "
                                            "pour le palier suviant ou arreter ?")
                                        membre.point_fictive_manag = 30
                                    elif membre.point == 1925:
                                        membre.point = membre.stock_point
                            elif groupe != membre.groupe and membre == systeme.nom_du_parent:
                                membre.gam += 1
                                membre.save()
                                break
                        else:
                            if membre.palier.nom_du_palier == "Bamiléké":

                                if membre.dix_milles:
                                    membre.point += 5  # ce n'est qu'a ce palier qu'on donne du point aux
                                    # parents lors de l'enregistrement de l'un de ses filleuls
                                elif not membre.dix_milles:
                                    membre.point_a_affecter += 5  # On stocke le point dans une variable
                                    # pour tous les utilisateurs qui n'ont pas encore payé leur frais de
                                    # formation 10.000
                                    # Les points sont cumulées une fois l'administrateur change l'etat en True
                                    # depuis son espace

                                if 0 <= membre.point < 5:
                                    poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste_invite
                                    membre.point_fictive_inv = 0
                                    print("Vous etes un invité, recruter 2 membres pour devenir un colibri")
                                elif membre.point == 5:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                    print("Vous etes un colibri")
                                    membre.point_fictive_col = 5
                                elif membre.point == 10:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                    print("Vous etes un colibri reconnu")
                                    membre.point_fictive_col = 10
                                elif 15 <= membre.point < 30:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous etes manageur")
                                    if membre.point == 15:
                                        membre.point_fictive_manag = 15
                                    elif membre.point == 20:
                                        membre.point_fictive_manag = 20
                                    elif membre.point == 25:
                                        membre.point_fictive_manag = 25
                                elif membre.point == 30:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous etes manageur reconnu et avez fini ce palier, Voulez-vous continuer "
                                          "pour le palier suviant ou arreter ?")
                                    membre.point_fictive_manag = 30
                                elif membre.point == 35:
                                    membre.stock_point = 30  # ICI ON STOCK LE POINT DU PALIER CI POUR LA SUITE
                                    membre.point = 5
                                    poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste
                                    palier_zoulou = get_object_or_404(Palier, nom_du_palier="Zoulou")
                                    membre.palier = palier_zoulou
                                    member_pursue_bam = 700/2000
                                    membre.gam = membre.gam + Decimal(member_pursue_bam)

                            elif membre.palier.nom_du_palier == "Zoulou":

                                if membre.dix_milles:
                                    membre.point += 5
                                elif not membre.dix_milles:
                                    membre.point_a_affecter += 5

                                if membre.point == 5:
                                    poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste_invite
                                    print("Vous etes invité")
                                    membre.point_fictive_inv = 0
                                if 5 < membre.point < 40:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                    print("Vous etes colibri")
                                    membre.point_fictive_col = 5
                                if membre.point == 40:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                    print("Vous etes colibri reconnu")
                                    membre.point_fictive_col = 10
                                elif 40 < membre.point < 120:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous etes manageur")
                                    if membre.point == 45:
                                        membre.point_fictive_manag = 15
                                    elif 45 < membre.point == 75:
                                        membre.point_fictive_manag = 20
                                    elif 75 < membre.point == 115:
                                        membre.point_fictive_manag = 25
                                elif membre.point == 120:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous etes manageur reconnu et avez fini ce palier, Voulez-vous continuer "
                                          "pour le palier suviant ou arreter ?")
                                    membre.point_fictive_manag = 30
                                elif membre.point == 125:
                                    membre.stock_point += 120  # ici on devrait avoir 30 + 120 = 150 points
                                    membre.point = 5
                                    poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste
                                    palier_maya = get_object_or_404(Palier, nom_du_palier="Maya")
                                    membre.palier = palier_maya
                                    member_pursue_zou = 1000/2000
                                    membre.gam = membre.gam + Decimal(member_pursue_zou)

                            elif membre.palier.nom_du_palier == "Maya":

                                if membre.dix_milles:
                                    membre.point += 5
                                elif not membre.dix_milles:
                                    membre.point_a_affecter += 5

                                if membre.point == 5:
                                    poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste_invite
                                    print("Vous etes invité")
                                    membre.point_fictive_inv = 0
                                if 5 < membre.point < 160:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                    print("Vous etes colibri")
                                    membre.point_fictive_col = 5
                                if membre.point == 160:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                    print("Vous etes colibri reconnu")
                                    membre.point_fictive_col = 10
                                elif 160 < membre.point < 480:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous etes manageur")
                                    if membre.point == 165:
                                        membre.point_fictive_manag = 15
                                    elif 45 < membre.point == 315:
                                        membre.point_fictive_manag = 20
                                    elif 75 < membre.point == 475:
                                        membre.point_fictive_manag = 25
                                elif membre.point == 480:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous etes manageur reconnu et avez fini ce palier, Voulez-vous continuer "
                                          "pour le palier suviant ou arreter ?")
                                    membre.point_fictive_manag = 30
                                elif membre.point == 485:
                                    membre.stock_point += 480  # ici on devrait avoir 150 + 480 = 630 points
                                    membre.point = 5
                                    poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste
                                    palier_mandingue = get_object_or_404(Palier, nom_du_palier="Mandingue")
                                    membre.palier = palier_mandingue
                                    member_pursue_maya = 2000/2000
                                    membre.gam = membre.gam + Decimal(member_pursue_maya)

                            elif membre.palier.nom_du_palier == "Mandingue":

                                if membre.dix_milles:
                                    membre.point += 5
                                elif not membre.dix_milles:
                                    membre.point_a_affecter += 5

                                if membre.point == 5:
                                    poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste_invite
                                    print("Vous etes invité")
                                    membre.point_fictive_inv = 0
                                if 5 < membre.point < 640:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                    print("Vous etes colibri")
                                    membre.point_fictive_col = 5
                                if membre.point == 640:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                    print("Vous etes colibri reconnu")
                                    membre.point_fictive_col = 10
                                elif 640 < membre.point < 1920:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous etes manageur")
                                    if membre.point == 645:
                                        membre.point_fictive_manag = 15
                                    elif 45 < membre.point == 1275:
                                        membre.point_fictive_manag = 20
                                    elif 75 < membre.point == 1915:
                                        membre.point_fictive_manag = 25
                                elif membre.point == 1920:
                                    membre.stock_point += 1920  # ici on devrait avoir 150 + 480 + 1920 = 2550 points
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous etes manageur reconnu et avez fini ce palier, Voulez-vous continuer "
                                          "pour le palier suviant ou arreter ?")
                                    membre.point_fictive_manag = 30
                                elif 1920 < membre.point:
                                    membre.point = membre.stock_point

                        membre.save()
                        print(membre)
                        print(total_parrainages, 'parrainé(s)')
                    systeme.save()

            return redirect('ajouter')
    else:
        form = UserCreationForm()

    droit = "Ajouter"
    context = {
        'utilisateurs': utilisateurs,
        'form': form,
        'invite': invite,
        'total_membre': total_membre,
    }
    return controllers(request, 'affiliation/donnee_base/ajouter.html', droit, context)


@login_required
def liste(request):
    droit = "Liste"
    utilisateurs = User.objects.filter(is_active=True)

    context = {
        "utilisateurs": utilisateurs
    }
    return controllers(request, 'affiliation/donnee_base/liste_adherent/liste_adherent.html', droit, locals())


@login_required
def listeupdateuser(request, id):
    updateuser = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=updateuser)
        if form.is_valid():
            form.save()
            redirect('liste')
    else:
        form = UserUpdateForm(instance=updateuser)

    context = {
        'form': form,
    }
    return render(request, 'affiliation/donnee_base/liste_adherent/listeupdateuser.html', locals())


@login_required
def change_password(request, id):
    user_u = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = PasswordChangeForm(user_u, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Le mot de passe a bien été enrégistré')
            return redirect('listeupdateuser', user_u.id)
        else:
            messages.error(request, 'ERREUR | VERIFIER VOS DONNEES')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'affiliation/password_change_form.html', {
        'form': form,
        'user_u': user_u
    })


@login_required
def listesuppruser(id):
    user_s = get_object_or_404(User, id=id)
    user_s.is_active = False
    user_s.save()
    return redirect('liste')


@login_required
def voirplus(request, id):
    membre = get_object_or_404(User, id=id)
    gam = membre.gam

    if membre:
        groupe = membre.groupe
        if membre.nom_du_parent is not None:
            parrain = get_object_or_404(User, id=membre.nom_du_parent.id)
        payements = Payement.objects.filter(archive=False, membre=request.user)

        if membre.palier is not None:
            bam = get_object_or_404(Palier, nom_du_palier="Bamiléké")
            membres_bam = User.objects.filter(palier=bam)
            zou = get_object_or_404(Palier, nom_du_palier="Zoulou")
            membres_zou = User.objects.filter(palier=zou)
            maya = get_object_or_404(Palier, nom_du_palier="Maya")
            membres_maya = User.objects.filter(palier=maya)
            mand = get_object_or_404(Palier, nom_du_palier="Mandingue")
            membres_mand = User.objects.filter(palier=mand)

        if membre.palier is not None:
            if membre.palier.nom_du_palier == "Bamiléké":
                point = membre.point
                progress_bar_bam = int(point * (100 / 30))
            elif membre.palier.nom_du_palier == "Zoulou":
                point = membre.point
                progress_bar_zou = int(point * (100 / 120))
            elif membre.palier.nom_du_palier == "Maya":
                point = membre.point
                progress_bar_maya = int(point * (100 / 480))
            elif membre.palier.nom_du_palier == "Mandingue":
                point = membre.point
                progress_bar_mand = int(point * (100 / 1920))

        if membre.nb_pers_amene >= 2:
            nb_pers_total = membre.nb_pers_amene
            solde = membre.gam * 2000
        elif membre.nb_pers_amene < 2:
            solde = 0

    return render(request, 'affiliation/donnee_base/liste_adherent/voirplus.html', locals())


@login_required
def parcours(request):
    count = [5, 7, 9, 0, 15, 7, 9, 0, 15, 7, 9, 0, 15, 7, 9, 0, 1]
    return render(request, 'affiliation/parcours_utilisateur.html', locals())


@login_required
def codepays(request):
    droit = "Pays"
    codes = CodePays.objects.filter(archive=False)
    context = {'codes': codes}
    return controllers(request, 'affiliation/code_pays/codepays.html', droit, context)


def createcodepays(request):
    codes = CodePays.objects.filter(archive=False)
    if request.method == 'POST':
        form = CodePaysForm(request.POST)
    else:
        form = CodePaysForm()
    mycontext = {'codes': codes, 'form': form}
    return save_all(request, form, 'affiliation/code_pays/createcodepays.html',
                    'code', 'affiliation/code_pays/listecodepays.html', mycontext)


def updatecodepays(request, id):
    codes = CodePays.objects.all()
    mycontext = {
        'codes': codes
    }
    code = get_object_or_404(CodePays, id=id)
    if request.method == 'POST':
        form = CodePaysForm(request.POST, instance=code)
    else:
        form = CodePaysForm(instance=code)

    return save_all(request, form, 'affiliation/code_pays/updatecodepays.html',
                    'code', 'affiliation/code_pays/listecodepays.html', mycontext)


@login_required
def deletecodepays(request, id):
    data = dict()
    code = get_object_or_404(CodePays, id=id)
    if request.method == "POST":
        code.archive = True
        code.save()
        data['form_is_valid'] = True
        codes = CodePays.objects.filter(archive=False)
        data['code'] = render_to_string('affiliation/code_pays/listecodepays.html', {'codes': codes})
    else:
        context = {
            'code': code
        }
        data['html_form'] = render_to_string('affiliation/code_pays/deletecodepays.html', context, request=request)

    return JsonResponse(data)


@login_required
def niveau(request):
    droit = "Niveau"
    niveaux = Niveau.objects.filter(archive=False)
    mycontext = {
        'niveaux': niveaux
    }
    return controllers(request, 'affiliation/niveau/niveau.html', droit, mycontext)


def createniveau(request):
    niveaux = Niveau.objects.filter(archive=False)
    if request.method == 'POST':
        form = NiveauForm(request.POST)
    else:
        form = NiveauForm()
    mycontext = {'niveaux': niveaux, 'form': form}
    return save_all(request, form, 'affiliation/niveau/createniveau.html',
                    'niveau', 'affiliation/niveau/listeniveau.html', mycontext)


def updateniveau(request, id):
    niveaux = Niveau.objects.filter(archive=False)
    mycontext = {
        'niveaux': niveaux
    }
    niveau = get_object_or_404(Niveau, id=id)
    if request.method == 'POST':
        form = NiveauForm(request.POST, instance=niveau)
    else:
        form = NiveauForm(instance=niveau)

    return save_all(request, form, 'affiliation/niveau/updateniveau.html',
                    'niveau', 'affiliation/niveau/listeniveau.html', mycontext)


@login_required
def deleteniveau(request, id):
    data = dict()
    niveau = get_object_or_404(Niveau, id=id)
    if request.method == "POST":
        niveau.archive = True
        niveau.save()
        data['form_is_valid'] = True
        niveaux = Niveau.objects.filter(archive=False)
        data['niveau'] = render_to_string('affiliation/niveau/listeniveau.html', {'niveaux': niveaux})
    else:
        context = {
            'niveau': niveau
        }
        data['html_form'] = render_to_string('affiliation/niveau/deleteniveau.html', context, request=request)

    return JsonResponse(data)


@login_required
def palier(request):
    droit = "Paliers"
    paliers = Palier.objects.filter(archive=False)
    mycontext = {
        'paliers': paliers
    }
    return controllers(request, 'affiliation/palier/palier.html', droit, mycontext)


def createpalier(request):
    paliers = Palier.objects.filter(archive=False)
    if request.method == 'POST':
        form = PalierForm(request.POST)
    else:
        form = PalierForm()
    mycontext = {'paliers': paliers, 'form': form}
    return save_all(request, form, 'affiliation/palier/createpalier.html',
                    'palier', 'affiliation/palier/listepalier.html', mycontext)


def updatepalier(request, id):
    paliers = Palier.objects.filter(archive=False)
    mycontext = {
        'paliers': paliers
    }
    palier = get_object_or_404(Palier, id=id)
    if request.method == 'POST':
        form = PalierForm(request.POST, instance=palier)
    else:
        form = PalierForm(instance=palier)

    return save_all(request, form, 'affiliation/palier/updatepalier.html',
                    'palier', 'affiliation/palier/listepalier.html', mycontext)


@login_required
def deletepalier(request, id):
    data = dict()
    palier = get_object_or_404(Palier, id=id)
    if request.method == "POST":
        palier.archive = True
        palier.save()
        data['form_is_valid'] = True
        paliers = Palier.objects.filter(archive=False)
        data['palier'] = render_to_string('affiliation/palier/listepalier.html', {'paliers': paliers})
    else:
        context = {
            'palier': palier
        }
        data['html_form'] = render_to_string('affiliation/palier/deletepalier.html', context, request=request)

    return JsonResponse(data)


@login_required
def groupe(request):
    droit = "Groupes"
    groupes = Groupe.objects.filter(archive=False)
    mycontext = {
        'groupes': groupes
    }
    return controllers(request, 'affiliation/groupe/groupe.html', droit, mycontext)


def creategroupe(request):
    groupes = Groupe.objects.filter(archive=False)
    if request.method == 'POST':
        form = GroupeForm(request.POST)
    else:
        form = GroupeForm()
    mycontext = {'groupes': groupes, 'form': form}
    return save_all(request, form, 'affiliation/groupe/creategroupe.html',
                    'groupe', 'affiliation/groupe/listegroupe.html', mycontext)


def updategroupe(request, id):
    groupes = Groupe.objects.filter(archive=False)
    mycontext = {
        'groupes': groupes
    }
    groupe = get_object_or_404(Groupe, id=id)
    if request.method == 'POST':
        form = GroupeForm(request.POST, instance=groupe)
    else:
        form = GroupeForm(instance=groupe)

    return save_all(request, form, 'affiliation/groupe/updategroupe.html',
                    'groupe', 'affiliation/groupe/listegroupe.html', mycontext)


@login_required
def deletegroupe(request, id):
    data = dict()
    groupe = get_object_or_404(Groupe, id=id)
    if request.method == "POST":
        groupe.archive = True
        groupe.save()
        data['form_is_valid'] = True
        groupes = Groupe.objects.filter(archive=False)
        data['groupe'] = render_to_string('affiliation/groupe/listegroupe.html', {'groupes': groupes})
    else:
        context = {
            'groupe': groupe
        }
        data['html_form'] = render_to_string('affiliation/groupe/deletegroupe.html', context, request=request)

    return JsonResponse(data)


@login_required
def pyramide(request, id):
    niveau1 = get_object_or_404(Niveau, nom_du_niveau="Niveau 1")
    group = get_object_or_404(Groupe, id=id)  # on recupere le groupe dont l'identifiant a été passé en argument

    # Prendre un groupe donnee et voir tous les membres qui y sont present

    if group:  # si on a un groupe alors '->
        premier_membre = get_object_or_404(User, groupe=group, nom_du_parent=None)  # on lance un requete pour
        # recuperer le membre qui n'a pas de parent se servant du groupe selectionner
        nb_total_membre = User.objects.filter(groupe=group).count()

        # while premier_membre.nom_du_parent is None:
        # premier_membre = User.objects.filter(nom_du_parent=premier_membre)
        # for membre in premier_membre:
        # while membre is not None:
        # membre = User.objects.filter(nom_du_parent=membre)

        print(group.manageur_du_groupe)

    context = {
        'group': group,
        'niveau1': niveau1,
        'nb_total_membre': nb_total_membre
    }

    return render(request, 'affiliation/niveau1/pyramide.html', context)


def wara(request):
    waras = Wara.objects.all()
    context = {
        "waras": waras
    }
    return render(request, 'affiliation/wara/wara.html', context)


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

"""
PARTIE CONCERNANT LA PARTIE DE WARA : FORMATION EN LIGNE
"""

from django.contrib.auth.views import LoginView


class WaraLoginView(LoginView):
    template_name = 'formation-wara/wlogin.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or '/base/'


"""ACCUEIL : WARA"""


@login_required(redirect_field_name='suivant', login_url='wlogin')
def base(request):
    participant = request.user
    dict = {}
    data = {}
    vagues = Vague.objects.filter(archive=False)
    dict[participant] = vagues

    versions = Versions.objects.filter(archive=False)

    for vague in vagues:
        for utilisateur in vague.utilisateurs.filter(nom=participant.nom):
            if utilisateur:
                modules = Modules.objects.filter(version=vague.version, archive=False)
                data[vague.version] = modules
                modules_total = Modules.objects.filter(version=vague.version, archive=False).count()

                print(vague.version, ' | ', modules_total, 'modules')
                vague_version = vague.version

                print(utilisateur)
                vague_utilisateur = utilisateur

                print(vague.utilisateurs.count(), 'personnes\n')
                vague_utilisateur_total = vague.utilisateurs.count()

    list_total_member = User.objects.filter(is_active=True).count()
    list_total_vague = Vague.objects.filter(archive=False).count()
    list_total_module = Modules.objects.filter(archive=False).count()
    list_total_version = Versions.objects.filter(archive=False).count()

    return render(request, 'formation-wara/wara/base-wara.html', locals())


@login_required(redirect_field_name='suivant', login_url='wlogin')
def voir_modules(request, id):
    participant = request.user
    dict = {}
    vagues = Vague.objects.filter(archive=False)
    dict[participant] = vagues

    for vague in vagues:
        for utilisateur in vague.utilisateurs.filter(nom=participant.nom):
            if utilisateur:
                modules = Modules.objects.filter(version=vague.version, archive=False)
                modules_total = Modules.objects.filter(version=vague.version, archive=False).count()

                print(vague.version, ' | ', modules_total, 'modules')
                vague_version = vague.version

                print(utilisateur)
                vague_utilisateur = utilisateur

                print(vague.utilisateurs.count(), 'personnes\n')
                vague_utilisateur_total = vague.utilisateurs.count()

    modules = Modules.objects.filter(version=id, archive=False)
    return render(request, 'formation-wara/wara/users/voir-modules.html', locals())


@login_required(redirect_field_name='suivant', login_url='wlogin')
def voir_modules_detail(request, id):
    versions = Versions.objects.filter(archive=False)
    participant = request.user
    dict = {}
    vagues = Vague.objects.filter(archive=False)
    dict[participant] = vagues
    module = get_object_or_404(Modules, id=id)
    for vague in vagues:
        for utilisateur in vague.utilisateurs.filter(nom=participant.nom):
            if utilisateur:
                modules = Modules.objects.filter(version=vague.version, archive=False)
                modules_total = Modules.objects.filter(version=vague.version, archive=False).count()

                print(vague.version, ' | ', modules_total, 'modules')
                vague_version = vague.version

                print(utilisateur)
                vague_utilisateur = utilisateur

                print(vague.utilisateurs.count(), 'personnes\n')
                vague_utilisateur_total = vague.utilisateurs.count()

    import time

    from mutagen.mp3 import MP3
    from mutagen.mp4 import MP4

    if module.video6:
        audio = MP4(module.video6)
        module.longueur_video6 = audio.info.length
        module.save()
        float_time = module.longueur_video6
        result6 = time.strftime('%H:%M:%S', time.gmtime(float_time))

    if module.video7:
        audio = MP4(module.video7)
        module.longueur_video7 = audio.info.length
        module.save()
        float_time = module.longueur_video7
        result7 = time.strftime('%H:%M:%S', time.gmtime(float_time))

    if module.video8:
        audio = MP4(module.video8)
        module.longueur_video8 = audio.info.length
        module.save()
        float_time = module.longueur_video8
        result8 = time.strftime('%H:%M:%S', time.gmtime(float_time))

    if module.video9:
        audio = MP4(module.video9)
        module.longueur_video9 = audio.info.length
        module.save()
        float_time = module.longueur_video9
        result9 = time.strftime('%H:%M:%S', time.gmtime(float_time))

    if module.video10:
        audio = MP4(module.video10)
        module.longueur_video10 = audio.info.length
        module.save()
        float_time = module.longueur_video10
        result10 = time.strftime('%H:%M:%S', time.gmtime(float_time))

    if module.audio1:
        audio = MP3(module.audio1)
        module.longueur_audio1 = audio.info.length
        module.save()
        float_time = module.longueur_audio1
        result1 = time.strftime('%H:%M:%S', time.gmtime(float_time))

    if module.audio2:
        audio = MP3(module.audio2)
        module.longueur_audio2 = audio.info.length
        module.save()
        float_time = module.longueur_audio2
        result2 = time.strftime('%H:%M:%S', time.gmtime(float_time))

    if module.audio3:
        audio = MP3(module.audio3)
        module.longueur_audio3 = audio.info.length
        module.save()
        float_time = module.longueur_audio3
        result3 = time.strftime('%H:%M:%S', time.gmtime(float_time))

    if module.audio4:
        audio = MP3(module.audio4)
        module.longueur_audio4 = audio.info.length
        module.save()
        float_time = module.longueur_audio
        result4 = time.strftime('%H:%M:%S', time.gmtime(float_time))

    if module.audio5:
        audio = MP3(module.audio5)
        module.longueur_audio5 = audio.info.length
        module.save()
        float_time = module.longueur_audio5
        result5 = time.strftime('%H:%M:%S', time.gmtime(float_time))

    return render(request, 'formation-wara/wara/users/voir-modules-detail.html', locals())


@login_required(redirect_field_name='suivant', login_url='wlogin')
def formation_wara(request):
    list_total_member = User.objects.filter(is_active=True).count()
    list_total_vague = Vague.objects.filter(archive=False).count()
    list_total_module = Modules.objects.filter(archive=False).count()
    list_total_version = Versions.objects.filter(archive=False).count()
    vagues = Vague.objects.filter(archive=False)

    versions = Versions.objects.filter(archive=False)
    return render(request, 'formation-wara/wara/formation-wara.html', locals())


@login_required(redirect_field_name='suivant', login_url='wlogin')
def formation_wara_utilisateur(request):
    versions = Versions.objects.filter(archive=False)
    participant = request.user
    dict = {}
    data = {}
    vagues = Vague.objects.filter(archive=False)
    dict[participant] = vagues

    for vague in vagues:
        for utilisateur in vague.utilisateurs.filter(nom=participant.nom):
            if utilisateur:
                modules = Modules.objects.filter(version=vague.version, archive=False)
                data[vague.version] = modules
                modules_total = Modules.objects.filter(version=vague.version, archive=False).count()

                print(vague.version, ' | ', modules_total, 'modules')
                vague_version = vague.version

                print(utilisateur)
                vague_utilisateur = utilisateur

                print(vague.utilisateurs.count(), 'personnes\n')
                vague_utilisateur_total = vague.utilisateurs.count()
    return render(request, 'formation-wara/wara/formation-wara-utilisateur.html', locals())


@login_required(redirect_field_name='suivant', login_url='wlogin')
def version_module(request, id):
    versions = Versions.objects.filter(archive=False)
    version = get_object_or_404(Versions, archive=False, id=id)
    modules = Modules.objects.filter(archive=False, version=version)
    return render(request, 'formation-wara/wara/versions/version_module.html', locals())


@login_required(redirect_field_name='suivant', login_url='wlogin')
def version_module_detail(request, id):
    versions = Versions.objects.filter(archive=False)
    module = get_object_or_404(Modules, id=id)

    return render(request, 'formation-wara/wara/versions/version_module_detail.html', locals())


"""MODULE DE FORMATION : WARA"""


@login_required(redirect_field_name='suivant', login_url='wlogin')
def module_formation(request):
    versions = Versions.objects.filter(archive=False)
    if request.method == 'POST':
        form = ModulesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('module_formation')
    else:
        form = ModulesForm()
    context = {
        'form': form,
    }
    return render(request, 'formation-wara/wara/modules/module_formation.html', locals())


"""VAGUE DE FORMATION : WARA"""


@login_required(redirect_field_name='suivant', login_url='wlogin')
def vague_formation(request):
    versions = Versions.objects.filter(archive=False)
    if request.method == 'POST':
        form = VagueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('module_formation')
    else:
        form = VagueForm()
    context = {
        'form': form,
    }
    return render(request, 'formation-wara/wara/vagues/vague_formation.html', locals())


@login_required(redirect_field_name='suivant', login_url='wlogin')
def update_vague_by_id(request, id):
    versions = Versions.objects.filter(archive=False)
    vague_id = get_object_or_404(Vague, id=id)
    if request.method == 'POST':
        form = VagueForm(request.POST, instance=vague_id)
        if form.is_valid():
            form.save()
            return redirect('formation-wara')
    else:
        form = VagueForm(instance=vague_id)
    context = {
        'form': form,
        'vague_id': vague_id,
        'versions': versions,
    }
    return render(request, 'formation-wara/wara/vagues/update_vague_by_id.html', context)


@login_required(redirect_field_name='suivant', login_url='wlogin')
def lire_pdf(request):
    return render(request, 'formation-wara/wara/versions/lire_pdf.html', locals())


@login_required(redirect_field_name='suivant', login_url='wlogin')
def version_wara(request):
    versions = Versions.objects.filter(archive=False)
    return render(request, 'formation-wara/wara/version_wara.html', locals())


@login_required(redirect_field_name='suivant', login_url='wlogin')
def save_all_wara(request, form, template_name, model, template_name2, mycontext):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            data[model] = render_to_string(template_name2, mycontext)
        else:
            data['form_is_valid'] = False

    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def create_version(request):
    versions = Versions.objects.filter(archive=False)
    if request.method == 'POST':
        form = VersionsForm(request.POST)
    else:
        form = VersionsForm()
    mycontext = {'versions': versions, 'form': form}

    return save_all_wara(request, form, 'formation-wara/wara/create-version.html',
                         'version', 'formation-wara/wara/liste-version.html', mycontext)


def liste_forum(request):
    versions = Versions.objects.filter(archive=False)
    forums = Forums.objects.filter(archive=False)
    return render(request, 'formation-wara/wara/forum/liste_forum.html', locals())


def liste_sujet(request, id):
    versions = Versions.objects.filter(archive=False)
    forum = get_object_or_404(Forums, id=id)
    auteur = request.user

    sujets = SujetForum.objects.filter(archive=False, forum=forum)
    for sujet in sujets:
        tous_les_messages_du_sujet = MessagesSujetsForums.objects.filter(archive=False, sujet=sujet)

    return render(request, 'formation-wara/wara/forum/liste_sujet.html', locals())


def liste_sujet_user(request):
    versions = Versions.objects.filter(archive=False)
    auteur = request.user

    vagues_auteur = Vague.objects.filter(archive=False, utilisateurs=auteur)
    for vague_auteur in vagues_auteur:
        forum = get_object_or_404(Forums, vague=vague_auteur)

    return render(request, 'formation-wara/wara/users/liste_sujet.html', locals())


def creer_sujet(request, id):
    versions = Versions.objects.filter(archive=False)
    auteur = request.user   # information a ajouter automatiquement au formulaire
    forum = get_object_or_404(Forums, id=id)    # donnée a ajouter automatiquement au formulaire

    sujets = SujetForum.objects.filter(archive=False, forum=forum)

    if request.method == 'POST':
        s_form = SujetForumForm(request.POST)

        if s_form.is_valid():
            systeme = s_form.save(commit=False)
            systeme.auteur = auteur
            systeme.forum = forum
            systeme.save()

            return redirect('liste_sujet', forum.id)

    else:
        s_form = SujetForumForm()

    return render(request, 'formation-wara/wara/forum/creer_sujet.html', locals())


def creer_forum(request):
    versions = Versions.objects.filter(archive=False)
    forums = Forums.objects.filter(archive=False)

    if request.method == 'POST':
        f_form = ForumForm(request.POST)

        if f_form.is_valid():
            f_form.save()

            return redirect('liste_forum')

    else:
        f_form = ForumForm()

    return render(request, 'formation-wara/wara/forum/creer_forum.html', locals())


def page_discussion(request, id):
    versions = Versions.objects.filter(archive=False)
    auteur = request.user
    sujet = get_object_or_404(SujetForum, id=id)

    messages = MessagesSujetsForums.objects.filter(archive=False, sujet=sujet)

    if request.method == 'POST':
        m_form = MessagesSujetsForumsForm(request.POST)

        if m_form.is_valid():
            systeme = m_form.save(commit=False)
            systeme.auteur = auteur
            systeme.sujet = sujet
            systeme.save()

            return redirect('page_discussion', sujet.id)

    else:
        m_form = MessagesSujetsForumsForm()

    return render(request, 'formation-wara/wara/forum/page_discussion.html', locals())


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

"""
PARTIE CONCERNANT LA PARTIE DE GET AHEAD V2.0 : LES INVESTISSEMENTS
"""


def generate_lien(request, unique_id):
    parrain = get_object_or_404(User, unique_id=unique_id)
    groupe_parrain_html = parrain.groupe
    nom_parrain_html = parrain

    groupe_parrain = parrain.groupe
    nom_parrain = parrain

    if request.method == 'POST':
        form = UserCreation20Form(request.POST, request.FILES,
                                  initial={'groupe': groupe_parrain, 'nom_du_parent': nom_parrain})
        if form.is_valid():
            if form.is_valid():
                form.save(commit=False)
                systeme = form.save()
                poste_inv = get_object_or_404(Poste, nom_du_poste="Invité")
                palier_bam = get_object_or_404(Palier, nom_du_palier="Bamiléké")
                systeme.poste = poste_inv
                systeme.palier = palier_bam

                profil = get_object_or_404(Profils, nom="Utilisateur")
                systeme.profil = profil

                # Faire une MAJ par rapport au groupe de l'adhérent, donc de retrouver le groupe de ce dernier
                # group = systeme.groupe
                group = groupe_parrain
                # groupe = get_object_or_404(Groupe, nom_du_groupe=group)

                if groupe:  # Si on a le groupe recherché alors '->

                    nom_d_utilisateur = systeme.nom_d_utilisateur
                    # nom_d_utilisateur = nom_parrain
                    membre = get_object_or_404(User, nom_d_utilisateur=nom_d_utilisateur)
                    if membre.nom_du_parent is None:
                        print(membre.nom_du_parent)
                        print("C'est le plus haut parent")
                        systeme.save()
                    elif membre.nom_du_parent is not None:
                        while membre.nom_du_parent is not None:
                            """
                            Quand on place un membre dans un groupe pour avoir un gam,
                            tout se passe bien sauf qu'au moment ou ce dernier qui a ete placé decide
                            de mettre un invité sous lui, non seulement il recoit les points
                            mais aussi son parrain dans l'autre groupe et ainsi de suite recoit les points
                            """
                            membre = get_object_or_404(User, id=membre.nom_du_parent.id)
                            # membre = get_object_or_404(User, id=membre.nom_du_parent.id, groupe=group)
                            # membre.point += 5
                            total_parrainages = User.objects.filter(nom_du_parent=membre).count()
                            membre.nb_pers_amene = total_parrainages
                            if total_parrainages > 2 and membre == systeme.nom_du_parent:
                                if groupe == membre.groupe:
                                    if membre.palier.nom_du_palier == "Bamiléké":
                                        if membre.dix_milles:
                                            membre.point_a_affecter += 5  # ce n'est qu'a ce palier qu'on donne du
                                            # point aux parents lors de l'enregistrement de l'un de ses filleuls
                                        elif not membre.dix_milles:
                                            membre.point_a_affecter += 5  # On stocke le point dans une variable
                                            # pour tous les utilisateurs qui n'ont pas encore payé leur frais de
                                            # formation 10.000
                                            # Les points sont cumulées une fois l'administrateur change l'etat en True
                                            # depuis son espace

                                        if 0 <= membre.point < 5:
                                            poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                            membre.poste = poste_invite
                                            membre.point_fictive_inv = 0
                                            print("Vous etes un invité, recruter 2 membres pour devenir un colibri")
                                        elif membre.point == 5:
                                            poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                            membre.poste = poste_colibri
                                            print("Vous etes un colibri")
                                            membre.point_fictive_col = 5
                                        elif membre.point == 10:
                                            poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                            membre.poste = poste_colibri
                                            print("Vous etes un colibri reconnu")
                                            membre.point_fictive_col = 10
                                        elif 15 <= membre.point < 30:
                                            poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                            membre.poste = poste_manageur
                                            print("Vous etes manageur")
                                            if membre.point == 15:
                                                membre.point_fictive_manag = 15
                                            elif membre.point == 20:
                                                membre.point_fictive_manag = 20
                                            elif membre.point == 25:
                                                membre.point_fictive_manag = 25
                                        elif membre.point == 30:
                                            membre.stock_point = 30  # ICI ON STOCK LE POINT DU PALIER CI POUR LA SUITE
                                            poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                            membre.poste = poste_manageur
                                            print(
                                                "Vous etes manageur reconnu et avez fini ce palier, Voulez-vous "
                                                "continuer pour le palier suviant ou arreter ?")
                                            membre.point_fictive_manag = 30
                                        elif membre.point == 35:
                                            membre.point = 5
                                            poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                            membre.poste = poste
                                            palier_zoulou = get_object_or_404(Palier, nom_du_palier="Zoulou")
                                            membre.palier = palier_zoulou
                                            member_pursue_zou = 700/2000
                                            membre.gam = membre.gam + Decimal(member_pursue_zou)

                                    elif membre.palier.nom_du_palier == "Zoulou":

                                        if membre.dix_milles:
                                            membre.point_a_affecter += 5
                                        elif not membre.dix_milles:
                                            membre.point_a_affecter += 5

                                        if membre.point == 5:
                                            poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                            membre.poste = poste_invite
                                            print("Vous etes invité")
                                            membre.point_fictive_inv = 0
                                        if 5 < membre.point < 40:
                                            poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                            membre.poste = poste_colibri
                                            print("Vous etes colibri")
                                            membre.point_fictive_col = 5
                                        if membre.point == 40:
                                            poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                            membre.poste = poste_colibri
                                            print("Vous etes colibri reconnu")
                                            membre.point_fictive_col = 10
                                        elif 40 < membre.point < 120:
                                            poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                            membre.poste = poste_manageur
                                            print("Vous etes manageur")
                                            if membre.point == 45:
                                                membre.point_fictive_manag = 15
                                            elif 45 < membre.point == 75:
                                                membre.point_fictive_manag = 20
                                            elif 75 < membre.point == 115:
                                                membre.point_fictive_manag = 25
                                        elif membre.point == 120:
                                            membre.stock_point += 120  # ici on devrait avoir 30 + 120 = 150 points
                                            poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                            membre.poste = poste_manageur
                                            print(
                                                "Vous etes manageur reconnu et avez fini ce palier, Voulez-vous "
                                                "continuer pour le palier suviant ou arreter ?")
                                            membre.point_fictive_manag = 30
                                        elif membre.point == 125:
                                            membre.point = 5
                                            poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                            membre.poste = poste
                                            palier_maya = get_object_or_404(Palier, nom_du_palier="Maya")
                                            membre.palier = palier_maya
                                            member_pursue_maya = 1000/2000
                                            membre.gam = membre.gam + Decimal(member_pursue_maya)

                                    elif membre.palier.nom_du_palier == "Maya":

                                        if membre.dix_milles:
                                            membre.point_a_affecter += 5
                                        elif not membre.dix_milles:
                                            membre.point_a_affecter += 5

                                        if membre.point == 5:
                                            poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                            membre.poste = poste_invite
                                            print("Vous etes invité")
                                            membre.point_fictive_inv = 0
                                        if 5 < membre.point < 160:
                                            poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                            membre.poste = poste_colibri
                                            print("Vous etes colibri")
                                            membre.point_fictive_col = 5
                                        if membre.point == 160:
                                            poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                            membre.poste = poste_colibri
                                            print("Vous etes colibri reconnu")
                                            membre.point_fictive_col = 10
                                        elif 160 < membre.point < 480:
                                            poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                            membre.poste = poste_manageur
                                            print("Vous etes manageur")
                                            if membre.point == 165:
                                                membre.point_fictive_manag = 15
                                            elif 45 < membre.point == 315:
                                                membre.point_fictive_manag = 20
                                            elif 75 < membre.point == 475:
                                                membre.point_fictive_manag = 25
                                        elif membre.point == 480:
                                            membre.stock_point += 480  # ici on devrait avoir 150 + 480 = 630 points
                                            poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                            membre.poste = poste_manageur
                                            print(
                                                "Vous etes manageur reconnu et avez fini ce palier, Voulez-vous "
                                                "continuer pour le palier suviant ou arreter ?")
                                            membre.point_fictive_manag = 30
                                        elif membre.point == 485:
                                            membre.point = 5
                                            poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                            membre.poste = poste
                                            palier_mandingue = get_object_or_404(Palier, nom_du_palier="Mandingue")
                                            membre.palier = palier_mandingue
                                            member_pursue_mand = 2000/2000
                                            membre.gam = membre.gam + Decimal(member_pursue_mand)

                                    elif membre.palier.nom_du_palier == "Mandingue":

                                        if membre.dix_milles:
                                            membre.point_a_affecter += 5
                                        elif not membre.dix_milles:
                                            membre.point_a_affecter += 5

                                        if membre.point == 5:
                                            poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                            membre.poste = poste_invite
                                            print("Vous etes invité")
                                            membre.point_fictive_inv = 0
                                        if 5 < membre.point < 640:
                                            poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                            membre.poste = poste_colibri
                                            print("Vous etes colibri")
                                            membre.point_fictive_col = 5
                                        if membre.point == 640:
                                            poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                            membre.poste = poste_colibri
                                            print("Vous etes colibri reconnu")
                                            membre.point_fictive_col = 10
                                        elif 640 < membre.point < 1920:
                                            poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                            membre.poste = poste_manageur
                                            print("Vous etes manageur")
                                            if membre.point == 645:
                                                membre.point_fictive_manag = 15
                                            elif 45 < membre.point == 1275:
                                                membre.point_fictive_manag = 20
                                            elif 75 < membre.point == 1915:
                                                membre.point_fictive_manag = 25
                                        elif membre.point == 1920:
                                            membre.stock_point += 1920  # ici on devrait avoir 150 + 480 + 1920 = 2550
                                            # points
                                            poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                            membre.poste = poste_manageur
                                            print(
                                                "Vous etes manageur reconnu et avez fini ce palier, Voulez-vous "
                                                "continuer pour le palier suviant ou arreter ?")
                                            membre.point_fictive_manag = 30
                                        elif membre.point == 1925:
                                            membre.point = membre.stock_point
                                elif groupe != membre.groupe and membre == systeme.nom_du_parent:
                                    membre.gam += 1
                                    membre.save()
                                    break
                            else:
                                if membre.palier.nom_du_palier == "Bamiléké":

                                    if membre.dix_milles:
                                        membre.point_a_affecter += 5
                                    elif not membre.dix_milles:
                                        membre.point_a_affecter += 5

                                    if 0 <= membre.point < 5:
                                        poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste_invite
                                        membre.point_fictive_inv = 0
                                        print("Vous etes un invité, recruter 2 membres pour devenir un colibri")
                                    elif membre.point == 5:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes un colibri")
                                        membre.point_fictive_col = 5
                                    elif membre.point == 10:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes un colibri reconnu")
                                        membre.point_fictive_col = 10
                                    elif 15 <= membre.point < 30:
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print("Vous etes manageur")
                                        if membre.point == 15:
                                            membre.point_fictive_manag = 15
                                        elif membre.point == 20:
                                            membre.point_fictive_manag = 20
                                        elif membre.point == 25:
                                            membre.point_fictive_manag = 25
                                    elif membre.point == 30:
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print(
                                            "Vous etes manageur reconnu et avez fini ce palier, Voulez-vous continuer "
                                            "pour le palier suviant ou arreter ?")
                                        membre.point_fictive_manag = 30
                                    elif membre.point == 35:
                                        membre.stock_point = 30  # ICI ON STOCK LE POINT DU PALIER COURANT POUR LA SUITE
                                        if membre.dix_milles:
                                            membre.point = 5
                                        elif not membre.dix_milles:
                                            membre.point = 0
                                        poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste
                                        palier_zoulou = get_object_or_404(Palier, nom_du_palier="Zoulou")
                                        membre.palier = palier_zoulou
                                        member_pursue_bam = 700/2000
                                        membre.gam = membre.gam + Decimal(member_pursue_bam)

                                elif membre.palier.nom_du_palier == "Zoulou":

                                    if membre.dix_milles:
                                        membre.point_a_affecter += 5
                                    elif not membre.dix_milles:
                                        membre.point_a_affecter += 5

                                    if membre.point == 5:
                                        poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste_invite
                                        print("Vous etes invité")
                                        membre.point_fictive_inv = 0
                                    if 5 < membre.point < 40:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes colibri")
                                        membre.point_fictive_col = 5
                                    if membre.point == 40:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes colibri reconnu")
                                        membre.point_fictive_col = 10
                                    elif 40 < membre.point < 120:
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print("Vous etes manageur")
                                        if membre.point == 45:
                                            membre.point_fictive_manag = 15
                                        elif 45 < membre.point == 75:
                                            membre.point_fictive_manag = 20
                                        elif 75 < membre.point == 115:
                                            membre.point_fictive_manag = 25
                                    elif membre.point == 120:
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print(
                                            "Vous etes manageur reconnu et avez fini ce palier, Voulez-vous continuer "
                                            "pour le palier suviant ou arreter ?")
                                        membre.point_fictive_manag = 30
                                    elif membre.point == 125:
                                        membre.stock_point += 120  # ici on devrait avoir 30 + 120 = 150 points

                                        if membre.dix_milles:
                                            membre.point = 5
                                        elif not membre.dix_milles:
                                            membre.point = 0

                                        poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste
                                        palier_maya = get_object_or_404(Palier, nom_du_palier="Maya")
                                        membre.palier = palier_maya
                                        member_pursue_zou = 1000/2000
                                        membre.gam = membre.gam + Decimal(member_pursue_zou)

                                elif membre.palier.nom_du_palier == "Maya":

                                    if membre.dix_milles:
                                        membre.point_a_affecter += 5
                                    elif not membre.dix_milles:
                                        membre.point_a_affecter += 5

                                    if membre.point == 5:
                                        poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste_invite
                                        print("Vous etes invité")
                                        membre.point_fictive_inv = 0
                                    if 5 < membre.point < 160:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes colibri")
                                        membre.point_fictive_col = 5
                                    if membre.point == 160:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes colibri reconnu")
                                        membre.point_fictive_col = 10
                                    elif 160 < membre.point < 480:
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print("Vous etes manageur")
                                        if membre.point == 165:
                                            membre.point_fictive_manag = 15
                                        elif 45 < membre.point == 315:
                                            membre.point_fictive_manag = 20
                                        elif 75 < membre.point == 475:
                                            membre.point_fictive_manag = 25
                                    elif membre.point == 480:
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print(
                                            "Vous etes manageur reconnu et avez fini ce palier, Voulez-vous continuer"
                                            "pour le palier suviant ou arreter ?")
                                        membre.point_fictive_manag = 30
                                    elif membre.point == 485:
                                        membre.stock_point += 480  # ici on devrait avoir 150 + 480 = 630 points
                                        membre.point = 5
                                        poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste
                                        palier_mandingue = get_object_or_404(Palier, nom_du_palier="Mandingue")
                                        membre.palier = palier_mandingue
                                        member_pursue_maya = 2000/2000
                                        membre.gam = membre.gam + Decimal(member_pursue_maya)

                                elif membre.palier.nom_du_palier == "Mandingue":

                                    if membre.dix_milles:
                                        membre.point_a_affecter += 5
                                    elif not membre.dix_milles:
                                        membre.point_a_affecter += 5

                                    if membre.point == 5:
                                        poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                        membre.poste = poste_invite
                                        print("Vous etes invité")
                                        membre.point_fictive_inv = 0
                                    if 5 < membre.point < 640:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes colibri")
                                        membre.point_fictive_col = 5
                                    if membre.point == 640:
                                        poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                        membre.poste = poste_colibri
                                        print("Vous etes colibri reconnu")
                                        membre.point_fictive_col = 10
                                    elif 640 < membre.point < 1920:
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print("Vous etes manageur")
                                        if membre.point == 645:
                                            membre.point_fictive_manag = 15
                                        elif 45 < membre.point == 1275:
                                            membre.point_fictive_manag = 20
                                        elif 75 < membre.point == 1915:
                                            membre.point_fictive_manag = 25
                                    elif membre.point == 1920:
                                        membre.stock_point += 1920  # ici on devrait avoir 150 + 480 + 1920 = 2550
                                        # points
                                        poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                        membre.poste = poste_manageur
                                        print(
                                            "Vous etes manageur reconnu et avez fini ce palier, Voulez-vous continuer "
                                            "pour le palier suviant ou arreter ?")
                                        membre.point_fictive_manag = 30
                                    elif 1920 < membre.point:
                                        membre.point = membre.stock_point

                            membre.save()
                            print(membre)
                            print(total_parrainages, 'parrainé(s)')
                        systeme.save()

                return redirect('mongroupe')
    else:
        form = UserCreation20Form(initial={'groupe': groupe_parrain, 'nom_du_parent': nom_parrain})

    return render(request, 'investissement/generate_lien.html', locals())


@login_required
def menu(request):
    return render(request, 'investissement/menu.html', locals())


@login_required
def menu_user(request):
    packs = Packs.objects.filter(archive=False)
    import uuid

    utilisateur = request.user
    if utilisateur.unique_id is None:
        utilisateur.unique_id = uuid.uuid4()
        utilisateur.save()
    return render(request, 'investissement/menu_user.html', locals())


@login_required
def activation_compte(request):
    comptes = User.objects.filter(is_active=True, dix_milles=False, is_admin=False)
    return render(request, 'investissement/activation_compte/activation_compte.html', locals())


@login_required
def gestion_investissement(request):
    return render(request, 'investissement/gestion_investissement/gestion_investissement.html', locals())


@login_required
def save_activation(request, form, template_name, template_name2, mycontext):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            system = form.save()

            invite = get_object_or_404(Poste, nom_du_poste="Invité")
            colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
            manageur = get_object_or_404(Poste, nom_du_poste="Manageur")

            bamileke = get_object_or_404(Palier, nom_du_palier="Bamiléké")
            zoulou = get_object_or_404(Palier, nom_du_palier="Zoulou")
            maya = get_object_or_404(Palier, nom_du_palier="Maya")
            mandingue = get_object_or_404(Palier, nom_du_palier="Mandingue")

            # id_compte = system.id
            compte = system
            print(compte)

            palier = compte.palier

            if palier == bamileke or palier == zoulou or palier == maya or palier == mandingue:
                if 0 <= compte.point_a_affecter <= 35:
                    if 0 <= compte.point_a_affecter < 5:
                        compte.dix_milles = True
                        compte.point += compte.point_a_affecter  # On met a jour le point du compte

                        compte.point_fictive_inv = 0

                        compte.poste = invite  # on met a jour le poste
                        compte.palier = bamileke  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                    if 5 <= compte.point_a_affecter < 15:
                        compte.dix_milles = True
                        compte.point += compte.point_a_affecter  # On met a jour le point du compte

                        if compte.point_a_affecter == 5:
                            compte.point_fictive_col = 5
                        elif compte.point_a_affecter == 10:
                            compte.point_fictive_col = 10

                        compte.poste = colibri  # on met a jour le poste
                        compte.palier = bamileke  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                    if 15 <= compte.point_a_affecter < 35:
                        compte.dix_milles = True
                        compte.point += compte.point_a_affecter  # On met a jour le point du compte

                        if compte.point_a_affecter == 15:
                            compte.point_fictive_manag = 15
                        elif compte.point_a_affecter == 20:
                            compte.point_fictive_manag = 20
                        elif compte.point_a_affecter == 25:
                            compte.point_fictive_manag = 25
                        elif compte.point_a_affecter == 30:
                            compte.point_fictive_manag = 30

                        compte.poste = manageur  # on met a jour le poste
                        compte.palier = bamileke  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                        print(compte.poste, compte.palier, compte.point, compte.point_a_affecter)
                    if compte.point_a_affecter == 35:
                        compte.dix_milles = True
                        compte.stock_point = 30
                        compte.point = 5  # on ramène le point a 5

                        compte.poste = invite  # on met a jour le poste
                        compte.palier = zoulou  # on met a jour le palier
                        compte.point_a_affecter = 0
                elif 35 < compte.point_a_affecter <= 155:
                    print("Boucle 2")
                    if 35 < compte.point_a_affecter < 70:
                        compte.dix_milles = True
                        compte.stock_point = 30
                        compte.point = compte.point_a_affecter - 30  # On met a jour le point du compte

                        compte.point_fictive_col = 5

                        compte.poste = colibri  # on met a jour le poste
                        compte.palier = zoulou  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                    if compte.point_a_affecter == 70:
                        compte.dix_milles = True
                        compte.stock_point = 30
                        compte.point = compte.point_a_affecter - 30  # On met a jour le point du compte

                        compte.point_fictive_col = 10

                        compte.poste = colibri  # on met a jour le poste
                        compte.palier = zoulou  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                    if 70 < compte.point_a_affecter <= 150:
                        compte.dix_milles = True
                        compte.stock_point = 30
                        compte.point = compte.point_a_affecter - 30  # On met a jour le point du compte

                        if compte.point_a_affecter == 75:
                            compte.point_fictive_manag = 15
                        elif 75 < compte.point_a_affecter == 105:
                            compte.point_fictive_manag = 20
                        elif 105 < compte.point_a_affecter == 145:
                            compte.point_fictive_manag = 25
                        elif compte.point_a_affecter == 150:
                            compte.point_fictive_manag = 30

                        compte.poste = manageur  # on met a jour le poste
                        compte.palier = zoulou  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                    if compte.point_a_affecter == 155:
                        compte.dix_milles = True
                        compte.stock_point = 30 + 120
                        compte.point = 5  # on ramène le point a 5

                        compte.poste = invite  # on met a jour le poste
                        compte.palier = maya  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                elif 155 < compte.point_a_affecter <= 635:
                    print("Boucle 3")
                    if 155 < compte.point_a_affecter < 310:
                        compte.dix_milles = True
                        compte.stock_point = 30 + 120
                        compte.point = compte.point_a_affecter - 150  # On met a jour le point du compte

                        compte.point_fictive_col = 5

                        compte.poste = colibri  # on met a jour le poste
                        compte.palier = maya  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                    if compte.point_a_affecter == 310:
                        compte.dix_milles = True
                        compte.stock_point = 30 + 120
                        compte.point = compte.point_a_affecter - 150  # On met a jour le point du compte

                        compte.point_fictive_col = 10

                        compte.poste = colibri  # on met a jour le poste
                        compte.palier = maya  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                    if 310 < compte.point_a_affecter <= 630:
                        compte.dix_milles = True
                        compte.stock_point = 30 + 120
                        compte.point = compte.point_a_affecter - 150  # On met a jour le point du compte

                        if compte.point_a_affecter == 315:
                            compte.point_fictive_manag = 15
                        elif 315 < compte.point_a_affecter == 465:
                            compte.point_fictive_manag = 20
                        elif 465 < compte.point_a_affecter < 625:
                            compte.point_fictive_manag = 25
                        elif compte.point_a_affecter == 630:
                            compte.point_fictive_manag = 30

                        compte.poste = manageur  # on met a jour le poste
                        compte.palier = zoulou  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                    if compte.point_a_affecter == 635:
                        compte.dix_milles = True
                        compte.stock_point = 30 + 120 + 480
                        compte.point = 5  # on ramène le point a 5

                        compte.poste = invite  # on met a jour le poste
                        compte.palier = mandingue  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                elif 635 < compte.point_a_affecter:
                    print("Boucle 4")
                    if 635 < compte.point_a_affecter < 1120:
                        compte.dix_milles = True
                        compte.stock_point = 30 + 120 + 480
                        compte.point = compte.point_a_affecter - 630  # On met a jour le point du compte

                        compte.point_fictive_col = 5

                        compte.poste = colibri  # on met a jour le poste
                        compte.palier = mandingue  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                    if compte.point_a_affecter == 1120:
                        compte.dix_milles = True
                        compte.stock_point = 30 + 120 + 480
                        compte.point = compte.point_a_affecter - 630  # On met a jour le point du compte

                        compte.point_fictive_col = 10

                        compte.poste = colibri  # on met a jour le poste
                        compte.palier = mandingue  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                    if 1120 < compte.point_a_affecter <= 2550:
                        compte.dix_milles = True
                        compte.stock_point = 30 + 120 + 480
                        compte.point = compte.point_a_affecter - 630  # On met a jour le point du compte

                        if compte.point_a_affecter == 1120:
                            compte.point_fictive_manag = 15
                        elif 1120 < compte.point_a_affecter == 1975:
                            compte.point_fictive_manag = 20
                        elif 1975 < compte.point_a_affecter < 2545:
                            compte.point_fictive_manag = 25
                        elif compte.point_a_affecter == 2550:
                            compte.point_fictive_manag = 30
                            compte.stock_point = 30 + 120 + 480 + 1920

                        compte.poste = manageur  # on met a jour le poste
                        compte.palier = mandingue  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0
                    if 2550 < compte.point_a_affecter:
                        compte.dix_milles = True
                        compte.point = compte.point_a_affecter  # on ramène le point a 5

                        compte.poste = manageur  # on met a jour le poste
                        compte.palier = mandingue  # on met a jour le palier
                        compte.point_a_affecter = 0  # on ramène le point_a_affecter a 0

                compte.save()
            system.save()
            data['form_is_valid'] = True
            data['activation'] = render_to_string(template_name2, mycontext)
        else:
            data['form_is_valid'] = False

    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def formulaire_activation(request, id):
    comtpes = User.objects.filter(is_active=True, dix_milles=False, is_admin=False)
    compte = get_object_or_404(User, id=id)
    mycontext = {
        'comptes': comtpes,
        'compte': compte,
    }
    if request.method == 'POST':
        form = ActivationForm(request.POST, instance=compte)
    else:
        form = ActivationForm(instance=compte)

    return save_activation(request, form, 'investissement/activation_compte/formulaire_activation.html',
                           'investissement/activation_compte/liste_compte_a_activer.html', mycontext)


@login_required
def packs(request):
    packs = Packs.objects.filter(archive=False)
    return render(request, 'investissement/nos_packs/packs.html', locals())


@login_required
def mall_achat(request):
    packs = Packs.objects.filter(archive=False)
    return render(request, 'investissement/menu_user/mall_achat/mall_achat.html', locals())
