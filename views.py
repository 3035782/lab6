from .models import Article
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
            raise Http404

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {'text': request.POST["text"], 'title': request.POST["title"]}
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                # если поля заполнены без ошибок
                articles = Article.objects.all()
                for article in articles:
                    if article.title == form["title"]:
                        form['errors'] = u"Статья с таким названием уже существует"
                        return render(request, 'create_post.html', {'form': form})
                Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=Article.objects.get(title=form["title"]).id)
                # перейти на страницу поста
            else:
                # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        raise Http404

    
def new_profile(request):
    if request.method == "POST":
        form = {'username': request.POST["username"], 'email': request.POST["email"], 'password':request.POST["password"]}
        if form["username"] and form["email"] and form["password"]:
            users = User.objects.all()
            for user in users:
                if user.username == form['username']:
                    form['errors'] = u"Логин занят"
                    return render(request,'new_profile.html',{'form':form})
                if user.email == form['email']:
                    form['errors'] = u"Почта уже используется"
                    return render(request,'new_profile.html',{'form':form})
            User.objects.create_user(username=form['username'],email=form['email'],password=form['password'])
            return redirect('site')
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'new_profile.html',{'form': form})
    else:
        return render(request, 'new_profile.html', {})




def authentication(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = {'username': request.POST["username"], 'password':request.POST["password"]}
            if form["username"] and form["password"]:
                user = authenticate(username=form['username'], password=form['password'])
                if user == None:
                    form['errors'] = u"Такого аккаунта нет"
                    return render(request,'authentication.html',{'form':form})
                else:
                    login(request, user)
                    return redirect('site')
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'authentication.html',{'form': form})
        else:
            return render(request, 'authentication.html', {})
    else:
        return redirect('site')
        
    























    
