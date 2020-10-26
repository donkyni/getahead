from random import shuffle

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from affiliation.forms import UserCreationForm, CodePaysForm, PosteForm, NiveauForm, PalierForm, GroupeForm, ParentForm
from affiliation.models import User, CodePays, Poste, Niveau, Palier, Groupe, Parent


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
                  '&', '=', '#', '|', '?', '@', '$', '*', 'µ', '%', '!', '/'
                  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    mdp = str()
    shuffle(caracteres)
    for x in range(longueur):
        mdp += caracteres[x]
    return mdp


def ajouter(request):
    utilisateurs = User.objects.all()
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
    else:
        form = UserCreationForm()

    long = 14
    longueur = 8
    code = generatepassword(long)
    mdp = generatepassword(longueur)

    context = {
        'utilisateurs': utilisateurs,
        'form': form,
        'code': code,
        'mdp': mdp
    }
    return render(request, 'affiliation/ajouter_utilisateur.html', context)


def liste(request):
    return render(request, 'affiliation/liste_utilisateur.html', locals())


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


def parent(request):
    parents = Parent.objects.filter(archive=False)
    mycontext = {
        'parents': parents
    }
    return render(request, 'affiliation/parent/parent.html', mycontext)


def createparent(request):
    parents = Parent.objects.filter(archive=False)
    if request.method == 'POST':
        form = ParentForm(request.POST)
    else:
        form = ParentForm()
    mycontext = {'parents': parents, 'form': form}
    return save_all(request, form, 'affiliation/parent/createparent.html',
                    'parent', 'affiliation/parent/listeparent.html', mycontext)


def updateparent(request, id):
    parents = Parent.objects.filter(archive=False)
    mycontext = {
        'parents': parents
    }
    parent = get_object_or_404(Parent, id=id)
    if request.method == 'POST':
        form = ParentForm(request.POST, instance=parent)
    else:
        form = ParentForm(instance=parent)

    return save_all(request, form, 'affiliation/parent/updateparent.html',
                    'parent', 'affiliation/parent/listeparent.html', mycontext)


def deleteparent(request, id):
    data = dict()
    parent = get_object_or_404(Parent, id=id)
    if request.method == "POST":
        parent.archive = True
        parent.save()
        data['form_is_valid'] = True
        parents = Parent.objects.filter(archive=False)
        data['parent'] = render_to_string('affiliation/parent/listeparent.html', {'parents': parents})
    else:
        context = {
            'parent': parent
        }
        data['html_form'] = render_to_string('affiliation/parent/deleteparent.html', context, request=request)

    return JsonResponse(data)
