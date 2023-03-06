from django.shortcuts import render

def index(request):
    receitas = {
        1: 'Lasanha',
        2: 'Sopa de Legumes',
        3: 'Sorvete'
    }
    return render(request, 'index.html', 
                  {'nome_da_receita': receitas}
                  )

def receita(request):
    return render(request, 'receita.html')
