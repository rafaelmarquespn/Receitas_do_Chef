from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from cookbook.models import Receita


def cadastro(request):
    """Cadastra um novo usuário no sistema"""

    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        senha2 = request.POST['senha2']

        if campo_vazio(nome):
            messages.error(request, 'O nome não pode ficar em branco!')
            return redirect('cadastro')
        
        if campo_vazio(email):
            messages.error(request, 'O email não pode ficar em branco!')
            return redirect('cadastro')
        
        if senhas_n_iguais(senha, senha2):
            messages.error(request, 'As senhas não conferem!')
            return redirect('cadastro')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado!')
            return redirect('cadastro')

        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Nome de usuário já cadastrado!')
            return redirect('cadastro')
        
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login')
    
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    """Realiza o login de um usuário"""

    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'O email e a senha não podem ficar em branco!')
            return redirect('dashboard')
        
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')


def logout(request):
    """Realiza o logout de um usuário"""
    auth.logout(request)
    return redirect('index')


def dashboard(request):
    """Exibe todas as receitas cadastradas por um usuário"""

    if request.user.is_authenticated:
        receitas =  Receita.objects.order_by('-data_receita').filter(pessoa=request.user.id)
        dados = {
            'receitas': receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


def campo_vazio(campo): 
    """Verifica se um campo está vazio"""  
    return not campo.strip()


def senhas_n_iguais(senha, senha2):
    """Verifica se as senhas são iguais"""
    return senha != senha2

