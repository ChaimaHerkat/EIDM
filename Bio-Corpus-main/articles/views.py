from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import Article
from fetch_scripts.domains import DOMAINS


@cache_page(60 * 5)  # Cache for 5 minutes
def article_list(request):
    domain = request.GET.get("domain", "").strip()
    source = request.GET.get("source", "").strip()
    q = request.GET.get("q", "").strip()

    qs = Article.objects.all()
    if domain:
        qs = qs.filter(domain=domain)
    if source:
        qs = qs.filter(source=source)
    if q:
        qs = qs.filter(__raw__={"$text": {"$search": q}})

    # Optimized: Only load fields needed for list view
    qs = qs.only('title', 'abstract', 'journal', 'year', 'authors', 'domain', 'source', 'url', 'fetched_at').order_by("-fetched_at")

    paginator = Paginator(list(qs[:2000]), 25)  # cap for snappy paging
    page = paginator.get_page(request.GET.get("page"))

    # Cache statistics for 30 minutes
    stats_cache_key = "article_stats"
    stats = cache.get(stats_cache_key)
    if stats is None:
        stats = {
            "total": Article.objects.count(),
            "by_domain": [
                {"key": k, "label": v["label"], "count": Article.objects(domain=k).count()}
                for k, v in DOMAINS.items()
            ],
            "by_source": [
                {"key": s, "count": Article.objects(source=s).count()}
                for s in ["pubmed", "pmc", "semantic_scholar"]
            ],
        }
        cache.set(stats_cache_key, stats, 60 * 30)

    return render(request, "articles/list.html", {
        "page_obj": page, "stats": stats, "domains": DOMAINS,
        "current": {"domain": domain, "source": source, "q": q},
    })


def article_detail(request, article_id):
    try:
        art = Article.objects.get(id=article_id)
    except (Article.DoesNotExist, Exception):
        raise Http404("Article not found")
    return render(request, "articles/detail.html", {"article": art})
