from django.shortcuts import render, get_object_or_404, redirect
from ..models import Receita
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    paginator = Paginator(receitas, 3)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)

    dados = {
        'receitas' : receitas_por_pagina
    }

    return render(request, 'cookbook/index.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_exibir = {
        'receita' : receita
    }
    return render(request, 'cookbook/receita.html', receita_a_exibir)

def buscar(request):
    lista_receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        if buscar:
            lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)
    dados = {
        'receitas': lista_receitas
    }

    return render(request, 'cookbook/buscar.html', dados)

def cria_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita,
                            ingredientes=ingredientes, modo_preparo=modo_preparo, 
                            tempo_preparo=tempo_preparo, rendimento=rendimento, 
                            categoria=categoria, foto_receita=foto_receita)
        receita.save()
        messages.success(request, 'Receita cadastrada com sucesso!')
        return redirect('dashboard')
    else:
        messages.error(request, 'Erro ao cadastrar receita!')
        return render(request, 'cookbook/cria_receita.html')

def deleta_receita(request, id):
    receita = get_object_or_404(Receita, pk=id)
    receita.delete()
    messages.success(request, 'Receita deletada com sucesso!')
    return redirect('dashboard')

def edita_receita(request, id):
    receita = get_object_or_404(Receita, pk=id)
    dados = {
        'receita': receita
    }
    return render(request, 'cookbook/edita_receita.html', dados)

def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_preparo = request.POST['modo_preparo']
        r.tempo_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']
        r.save()
        messages.success(request, 'Receita atualizada com sucesso!')
        return redirect('dashboard')
    else:
        messages.error(request, 'Erro ao atualizar receita!')
        return redirect('dashboard')
    