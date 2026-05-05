from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import FeedbackForm
from .models import Feedback
from articles.models import Article


@login_required
def submit(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except Exception:
        messages.error(request, "Article introuvable.")
        return redirect("articles:list")

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            Feedback(
                article_id=str(article.id),
                username=request.user.username,
                rating=form.cleaned_data["rating"],
                comment=form.cleaned_data["comment"],
                suggested_domain=form.cleaned_data["suggested_domain"],
            ).save()
            messages.success(request, "Merci pour votre retour !")
            return redirect("articles:detail", article_id=str(article.id))
    else:
        form = FeedbackForm()

    return render(request, "feedbacks/submit.html", {"form": form, "article": article})
