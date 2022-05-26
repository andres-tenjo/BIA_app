STATE = (
        ('AC', 'Activo'),
        ('IN', 'Inactivo'),
    )
STATEORDER = (
        ('AB', 'Abierta'),
        ('CU', 'Cumplida'),
        ('CE', 'Cerrada')
    )
STATEORDERPROD = (
        ('AB', 'Abierto'),
        ('CE', 'Cerrado'),
        ('CU', 'Cumplido'),
        ('AN', 'Anulado'),
    )
STATEPAYORDER = (
    ('PG', 'Pagada'),
    ('SP', 'Sin pagar'),
    ('AT', 'Atrasada'),
    )
STATECARTERA = (
    ('AC', 'Activa'),
    ('CE', 'Cerrada'),
    ('VE', 'Vencida'),
    )
TYPEMOVEMENT = (
    ('PG', 'Pago'),
    ('PD', 'Pedido')
    )
DAYS_WEEK = (
        ('LU', 'Lunes'),
        ('MA', 'Martes'),
        ('MI', 'Miércoles'),
        ('JU', 'Jueves'),
        ('VI', 'Viernes'),
        ('SA', 'Sábado'),
        ('DO', 'Dómingo'),
    )
PAYMETHOD = (
        ('CR', 'Crédito'),
        ('CO', 'Contado'),
    )
ID_TYPE = (
        ('CC', 'Cédula'),
        ('NI', 'Nit'),
        ('RU', 'Rut'),
    )
PERSON_TYPE = (
        ('NT', 'Natural'),
        ('JU', 'Jurídica'),
    )
CONTRIB_TYPE = (
        ('RC', 'Régimen común'),
        ('RS', 'Régimen simplificado'),
        ('RE', 'Régimen especial')
    )
COUNTRY = (
        ('CO', 'Colombia'),
    )
VEHICLETYPE = (
        ('LI', 'Liviano'),
        ('TU', 'Turbo'),
        ('SE', 'Sencillo'),
        ('DT', 'Doble troque'),
        ('CM', 'Cuatro manos'),
        ('MM', 'Mini mula'),
        ('TD', 'Tractomula 2 troques'),
        ('TT', 'Tractomula 3 troques'),
    )
BODYWORK = (
        ('ES', 'Estacas'),
        ('FU', 'Furgón'),
    )
URGENCYLEVEL = (
    ('AL', 'Alta'),
    ('MD', 'Media'),
    ('BJ', 'Baja'),
    )
EVALUATIONTYPE = (
    ('CT', 'Cumplimiento en tiempo de entrega'),
    ('CP', 'Calidad en productos'),
    ('PR', 'Precio'),
    ('FP', 'Forma de pago'),
    ('FD', 'Flexibilidad de la demanda'),
    ('DC', 'Documentación'),
    )
INVENTORYTYPE = (
    ('AL', 'Aleatorio'),
    ('TT', 'Total'),
    ('SL', 'Selección'),
    )
EXITTYPE = (
    ('EP', 'Entrega de pedido'),
    ('BM', 'Baja por manipulación'),
    ('OB', 'Obsequio'),
    ('DV', 'Devolución'),
    ('AN', 'Anulación de ingreso'),
    )
WAREHOUSEENTRY = (
    ('CA', 'Causada'),
    ('NC', 'No causada')
    )
WAREHOUSEEXIT = (
    ('CE', 'Cerrada'),
    ('AN', 'Anulada')
    )
LOGISTICCONDITION = (
    ('CD', 'Con despacho'),
    ('SD', 'Sin despacho'),
    ('MX', 'Mixta')
    )
ORDERCONDITION = (
    ('CU', 'Cumplido'),
    ('NC', 'No cumplido')
    )
INCOMECONDITION = (
    ('CA', 'Causado'),
    ('NC', 'No causado')
    )
INCOMETYPE = (
    ('EN', 'Entrada'),
    ('SA', 'Salida')
    )
VALIDARCANTIDAD = (
    ('CO', 'Completo'),
    ('IN', 'Incompleto'),
    ('SU', 'Superior')
    )

ESTADOCLIENTE = (
    ('PR', 'Prospecto'),
    ('CL', 'Cliente'),
    ('PE', 'Cliente perdido')
    )

OBJETIVOACTIVIDAD = (
    ('SE', 'Seguimiento'),
    ('CO', 'Cotización'),
    ('PE', 'Pedido'),
    ('GP', 'Gestión PQR'),
    ('GC', 'Gestión cartera'),
    ('OT', 'Otro')
    )