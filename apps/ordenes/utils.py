import os
from django.conf import settings
from django.contrib.staticfiles import finders

def link_callback(uri, rel):
    """
    Convierte URLs de HTML (ej: /static/css/style.css) a rutas absolutas
    del sistema de archivos para que xhtml2pdf pueda generar el PDF.
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL        # /static/
        sRoot = settings.STATIC_ROOT      # C:/.../static/
        mUrl = settings.MEDIA_URL         # /media/
        mRoot = settings.MEDIA_ROOT       # C:/.../media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # Asegurarse de que el archivo exista
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path