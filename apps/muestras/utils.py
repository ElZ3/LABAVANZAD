from .models import Muestra

def generar_codigo_muestra(orden_id):
    """
    Genera un código único para la muestra basado en la orden.
    Formato: M-{ORDEN_ID}-{CORRELATIVO}
    Ejemplo: M-1005-01, M-1005-02
    """
    # Contamos cuántas muestras hay ya en esta orden
    count = Muestra.objects.filter(orden_id=orden_id).count()
    
    # El siguiente número es el conteo + 1
    siguiente = count + 1
    
    # Formateamos con ceros a la izquierda (01, 02...)
    codigo = f"M-{orden_id}-{str(siguiente).zfill(2)}"
    
    return codigo