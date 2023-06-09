from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404

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
            form = {'text': request.POST["text"], 'title': request.POST["title"]}
            if form["text"] and form["title"]:
                i = [x.id for x in Article.objects.all()]
                Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                for x in Article.objects.all():
                    if x.id not in i:
                        return redirect('get_article', article_id=x.id)
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            return render(request, 'create_post.html', {})
    else:
        raise Http404
