from random import shuffle

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from affiliation.forms import UserCreationForm, CodePaysForm, PosteForm, NiveauForm, PalierForm, GroupeForm
from affiliation.models import User, CodePays, Poste, Niveau, Palier, Groupe


def save_all(request, form, template_name, model, template_name2, mycontext):
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


def tableaudebord(request):
    return render(request, 'affiliation/tableaudebord.html', locals())


def poste(request):
    postes = Poste.objects.filter(archive=False)
    mycontext = {
        'postes': postes
    }
    return render(request, 'affiliation/poste/poste.html', mycontext)


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


def generatepassword(longueur):
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


def ajouter(request):
    dict = {}
    utilisateurs = User.objects.all()
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            systeme = form.save()

            # Faire une MAJ par rapport au groupe de l'adhérent, donc de retrouver le groupe de ce dernier
            group = systeme.groupe
            groupe = get_object_or_404(Groupe, nom_du_groupe=group)

            if groupe:  # Si on a le groupe recherché alors '->
                membres = User.objects.filter(groupe=group)  # On recupère tous ses membres
                dict[groupe] = membres

                code = systeme.code
                membre = get_object_or_404(User, code=code)
                if membre.nom_du_parent is None:
                    print(membre.nom_du_parent)
                    print("C'est le plus haut parent")
                    systeme.save()
                elif membre.nom_du_parent is not None:
                    while membre.nom_du_parent is not None:
                        membre = get_object_or_404(User, id=membre.nom_du_parent.id)
                        # membre.point += 5
                        total_parrainages = User.objects.filter(nom_du_parent=membre).count()
                        membre.nb_pers_amene = total_parrainages
                        if total_parrainages > 2 and membre == systeme.nom_du_parent:
                            if groupe == membre.groupe:
                                membre.point += 5
                            elif groupe != membre.groupe and membre == systeme.nom_du_parent:
                                membre.gam += 1
                        else:
                            if membre.palier.nom_du_palier == "Bamiléké":

                                membre.point += 5   # ce n'est qu'a ce palier qu'on donne du point aux parents
                                # lors de l'enregistrement de l'un de ses filleuls

                                if 0 <= membre.point < 10:
                                    poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste_invite
                                    print("Vous etes un invité, recruter 2 membres pour devenir un colibri")
                                elif membre.point == 10:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                    print("Vous etes un colibri")
                                elif 10 < membre.point <= 30:
                                    poste_animateur = get_object_or_404(Poste, nom_du_poste="Animateur")
                                    membre.poste = poste_animateur
                                    print("Vous etes un animateur")
                                elif 30 < membre.point <= 70:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous avez fini ce palier, Voulez-vous continuer pour le palier suviant ou "
                                          "arreter ?")
                                elif membre.point == 75:
                                    membre.point = 0
                                    poste = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste
                                    palier_zoulou = get_object_or_404(Palier, nom_du_palier="Zoulou")
                                    membre.palier = palier_zoulou

                            elif membre.palier.nom_du_palier == "Zoulou":
                                parraines = User.objects.filter(nom_du_parent=membre)
                                for parraine in parraines:
                                    if parraine.point != 0:     # Ici on verifie que le parrainé est bien devenu
                                        # un manageur reconnu et donc qu'il est pret a rejoindre son parrain au second
                                        # palier
                                        membre.point += 0
                                    elif parraine.point == 0:
                                        membre.point += 5
                                if 5 <= membre.point < 10:
                                    poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste_invite
                                elif membre.point == 10:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                elif 10 < membre.point <= 30:
                                    poste_animateur = get_object_or_404(Poste, nom_du_poste="Animateur")
                                    membre.poste = poste_animateur
                                elif 30 < membre.point <= 70:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous avez fini ce palier, Voulez-vous continuer pour le palier suviant ou "
                                          "arreter ?")
                                elif membre.point == 75:
                                    membre.point = 0
                                    palier_maya = get_object_or_404(Palier, nom_du_palier="Maya")
                                    membre.palier = palier_maya

                            elif membre.palier.nom_du_palier == "Maya":
                                parraines = User.objects.filter(nom_du_parent=membre)
                                for parraine in parraines:
                                    if parraine.point != 0:
                                        membre.point += 0
                                    elif parraine.point == 0:
                                        membre.point += 5
                                if 5 <= membre.point < 10:
                                    poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste_invite
                                elif membre.point == 10:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                elif 10 < membre.point <= 30:
                                    poste_animateur = get_object_or_404(Poste, nom_du_poste="Animateur")
                                    membre.poste = poste_animateur
                                elif 30 < membre.point <= 70:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous avez fini ce palier, Voulez-vous continuer pour le palier suviant ou "
                                          "arreter ?")
                                elif membre.point == 75:
                                    membre.point = 0
                                    palier_gladiateurs = get_object_or_404(Palier, nom_du_palier="Gladiateurs")
                                    membre.palier = palier_gladiateurs

                            elif membre.palier.nom_du_palier == "Gladiateurs":
                                parraines = User.objects.filter(nom_du_parent=membre)
                                for parraine in parraines:
                                    if parraine.point != 0:
                                        membre.point += 0
                                    elif parraine.point == 0:
                                        membre.point += 5
                                if 5 <= membre.point < 10:
                                    poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste_invite
                                elif membre.point == 10:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                elif 10 < membre.point <= 30:
                                    poste_animateur = get_object_or_404(Poste, nom_du_poste="Animateur")
                                    membre.poste = poste_animateur
                                elif 30 < membre.point <= 70:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous avez fini ce palier, Voulez-vous continuer pour le palier suviant ou "
                                          "arreter ?")
                                elif membre.point == 75:
                                    membre.point = 0
                                    palier_samourails = get_object_or_404(Palier, nom_du_palier="Samourails")
                                    membre.palier = palier_samourails

                            elif membre.palier.nom_du_palier == "Samourails":
                                parraines = User.objects.filter(nom_du_parent=membre)
                                for parraine in parraines:
                                    if parraine.point != 0:
                                        membre.point += 0
                                    elif parraine.point == 0:
                                        membre.point += 5
                                if 5 <= membre.point < 10:
                                    poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste_invite
                                elif membre.point == 10:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                elif 10 < membre.point <= 30:
                                    poste_animateur = get_object_or_404(Poste, nom_du_poste="Animateur")
                                    membre.poste = poste_animateur
                                elif 30 < membre.point <= 70:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous avez fini ce palier, Voulez-vous continuer pour le palier suviant ou "
                                          "arreter ?")
                                elif membre.point == 75:
                                    membre.point = 5
                                    palier_mandingues = get_object_or_404(Palier, nom_du_palier="Mandingues")
                                    membre.palier = palier_mandingues

                            elif membre.palier.nom_du_palier == "Mandingues":
                                parraines = User.objects.filter(nom_du_parent=membre)
                                for parraine in parraines:
                                    if parraine.point != 0:
                                        membre.point += 0
                                    elif parraine.point == 0:
                                        membre.point += 5
                                if 5 <= membre.point < 10:
                                    poste_invite = get_object_or_404(Poste, nom_du_poste="Invité")
                                    membre.poste = poste_invite
                                elif membre.point == 10:
                                    poste_colibri = get_object_or_404(Poste, nom_du_poste="Colibri")
                                    membre.poste = poste_colibri
                                elif 10 < membre.point <= 30:
                                    poste_animateur = get_object_or_404(Poste, nom_du_poste="Animateur")
                                    membre.poste = poste_animateur
                                elif 30 < membre.point <= 70:
                                    poste_manageur = get_object_or_404(Poste, nom_du_poste="Manageur")
                                    membre.poste = poste_manageur
                                    print("Vous avez fini ce palier et vous etes arrivé a la fin du programme")
                                elif membre.point == 75:
                                    membre.point = 70

                        membre.save()
                        print(membre)
                        print(total_parrainages, 'parrainé(s)')
                    systeme.save()

            return redirect('ajouter')
    else:
        form = UserCreationForm()

    long = 14
    longueur = 15
    code = generatepassword(long)
    mdp = generatepassword(longueur)

    context = {
        'utilisateurs': utilisateurs,
        'form': form,
        'code': code,
        'mdp': mdp,
    }
    return render(request, 'affiliation/donnee_base/ajouter.html', context)


def liste(request):
    utilisateurs = User.objects.all()
    context = {
        "utilisateurs": utilisateurs
    }
    return render(request, 'affiliation/donnee_base/liste_adherent/liste_adherent.html', locals())


def parcours(request):
    count = [5, 7, 9, 0, 15, 7, 9, 0, 15, 7, 9, 0, 15, 7, 9, 0, 1]
    return render(request, 'affiliation/parcours_utilisateur.html', locals())


def codepays(request):
    codes = CodePays.objects.filter(archive=False)
    context = {'codes': codes}
    return render(request, 'affiliation/code_pays/codepays.html', context)


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


def niveau(request):
    niveaux = Niveau.objects.filter(archive=False)
    mycontext = {
        'niveaux': niveaux
    }
    return render(request, 'affiliation/niveau/niveau.html', mycontext)


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


def palier(request):
    paliers = Palier.objects.filter(archive=False)
    mycontext = {
        'paliers': paliers
    }
    return render(request, 'affiliation/palier/palier.html', mycontext)


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


def groupe(request):
    groupes = Groupe.objects.filter(archive=False)
    mycontext = {
        'groupes': groupes
    }
    return render(request, 'affiliation/groupe/groupe.html', mycontext)


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


def bamileke(request):
    groupes = Groupe.objects.filter(archive=False)
    niveau1 = get_object_or_404(Niveau, nom_du_niveau="Niveau 1")

    context = {
        'groupes': groupes,
        'niveau1': niveau1
    }

    return render(request, 'affiliation/niveau1/bamileke.html', context)


def pyramide(request, id):
    niveau1 = get_object_or_404(Niveau, nom_du_niveau="Niveau 1")
    group = get_object_or_404(Groupe, id=id)  # on recupere le groupe dont l'identifiant a été passé en argument

    # Prendre un groupe donnee et voir tous les membres qui y sont present

    dict = {}
    if group:  # si on a un groupe alors '->
        membres = User.objects.filter(groupe=group)  # on lance un requete pour recuperer ses membres ou users en
        # se servant du groupe selectionner
        dict[group] = membres
        for membre in membres:
            print(membre, membre.groupe)
        print(group.manageur_du_groupe)

    context = {
        'group': group,
        'niveau1': niveau1
    }

    return render(request, 'affiliation/niveau1/pyramide.html', context)
