from datetime import timezone
from .models import Factura

def generar_numero_factura(tipo_factura):
    """
    Genera el siguiente número correlativo basado en el tipo.
    Formato: FAC-000001 o CCF-000001
    """
    prefijo = 'CCF' if tipo_factura == 'Convenio' else 'FAC'
    
    # Buscar la última factura de este tipo
    ultima_factura = Factura.objects.filter(
        numero_factura__startswith=prefijo
    ).order_by('factura_id').last()

    if not ultima_factura:
        return f"{prefijo}-000001"

    # Extraer el número, convertir a int e incrementar
    try:
        ultimo_numero = int(ultima_factura.numero_factura.split('-')[1])
        nuevo_numero = ultimo_numero + 1
        # Rellenar con ceros a la izquierda (6 dígitos)
        return f"{prefijo}-{str(nuevo_numero).zfill(6)}"
    except (IndexError, ValueError):
        # Fallback por si el formato manual anterior era diferente
        return f"{prefijo}-{timezone.now().strftime('%Y%m%d%H%M')}"