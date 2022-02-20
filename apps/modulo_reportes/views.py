from django.shortcuts import render, HttpResponse

def reportes_generales(request):
    return render(request, 'modulo_reportes/reportes_generales.html')

def reportes_modulo_comercial(request):
    return render(request, 'modulo_reportes/reportes_modulo_comercial.html')

def reportes_modulo_compras(request):
    return render(request, 'modulo_reportes/reportes_modulo_compras.html')

def reportes_modulo_almacen(request):
    return render(request, 'modulo_reportes/reportes_modulo_almacen.html')

def reportes_modulo_transporte(request):
    return render(request, 'modulo_reportes/reportes_modulo_transporte.html')

def reportes_costos(request):
    return render(request, 'modulo_reportes/reportes_costos.html')
