from .models import SiteContent


def site_content(request):
    """
    Добавляет контент сайта в контекст всех шаблонов.
    В шаблоне можно писать: {{ site_content.home_about.title }}
    """
    content = {}
    try:
        for item in SiteContent.objects.all():
            content[item.section] = {
                'title': item.title,
                'content': item.content,
            }
    except:
        pass
    return {'site_content': content}