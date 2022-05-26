/////////////////////////////////////////////////////////////
// Variables y funciones
var dctPedido = {

    dctResumenPedido:{
        intIdCliente: '',
        datFechaEntrega: '',
        fltSubtotal: 0.00,
        fltIva: 0.00,
        fltDescuento: 0.00,
        fltTotal: 0.00,
        intIdBodega: '',
        lstDetallePedido: [],
        lstPrecios: [],
        lstListaPrecios: []
    },

};

/////////////////////////////////////////////////////////////
// Eventos
$(function () {

    // Init
    fncCLienteslc();
    fncBuscarProductoslc();
    fncCargarLibreriaSelect2('.select', 'Seleccione una opción');
    fncCargarLibreriaSelect2('.selectCity', 'Seleccione una opción');

    /////////////////////////////////////////////////////////////
    //////////////////////// Funciones Cliente//////////////////
    // Busqueda de cliente
    function fncCLienteslc() {
        $('#identification').select2({
            theme: "bootstrap4",
            language: 'es',
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                url: window.location.pathname,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: function (params) {
                    var queryParameters = {
                        term: params.term,
                        action: 'slcBuscarClientejsn',
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Nº de identificación, nombre o celular del cliente',
            minimumInputLength: 1,
            templateResult: fncBuscarClienteRepo,
        }).on('select2:select', function (e) {  
            let dctDataCliente = e.params.data;
            let intIdCliente = dctDataCliente.id;
            fncValidarCarteraCliente(intIdCliente,
                function () {
                    if(!dctDataCliente.price_list){
                        fncCargarCliente(dctDataCliente);
                        return;    
                    }
                    let intIdListaPrecios = dctDataCliente.price_list.id;
                    fcnCargarListaPrecios(intIdListaPrecios,
                        function () {
                            fncCargarCliente(dctDataCliente);
                            return;
                        }
                    );
                    return;
                }
            );
        }).on('select2:unselect', function (e) {
            fncLimpiarCliente();
        });    
    }

    // Validar cartera cliente
    function fncValidarCarteraCliente(intIdCliente, fncRetorno) {
        let jsnParametros = new FormData();
        jsnParametros.append('action', 'slcEstadoCarteraClientejsn');
        jsnParametros.append('intIdCliente', intIdCliente);
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                if (request.hasOwnProperty('success')) {
                    fncRetorno();
                    return false;
                }
                fncMensajeConfirmacionmns('Confirmación!', '' + request.error + ' ¿Desea visualizar el historial de crédito?',
                    function () {
                        // Visualizar la ventana de cartera del cliente
                        window.open('/configuracion/exportar_lista_pdf/' + request.intIdCliente + '/', '_blank');
                        return;
                    },
                    function () {
                        
                    }
                );
                return false;
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    }
    
    // Cargar lista de precios del cliente
    function fcnCargarListaPrecios(intIdListaPrecios, fncSuccess) {
        let jsnParametros = new FormData();
        jsnParametros.append('action', 'slcListaPreciosDetallejsn');
        jsnParametros.append('intIdListaPrecios', intIdListaPrecios);
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                dctPedido.dctResumenPedido.lstPrecios = request.qrsListaPreciosDetalle;
                fncSuccess();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    }

    // Función que carga la información del cliente al pedido una vez es validado
    function fncCargarCliente(dctDataCliente) {
        $('.dataCliente').prop('hidden', false);
        $('#iptIdentificacionCliente').val(dctDataCliente.identification);
        $('#iptCelularCliente').val(dctDataCliente.cel_number);
        $('#city').val(dctDataCliente.city.id).trigger('change');
        $('#customer_zone').val(dctDataCliente.customer_zone.id).trigger('change');
        $('#delivery_address').val(dctDataCliente.delivery_address);
        $('#iptFormaPagoCliente').val(dctDataCliente.pay_method.name);
    }
    
    // Función que limpia la información del cliente en el pedido
    function fncLimpiarCliente() {
        $('.dataCliente').prop('hidden', true);
        $('#iptIdentificacionCliente').val('');
        $('#iptCelularCliente').val('');
        $('#city').val('').trigger('change');
        $('#customer_zone').val('').trigger('change');
        $('#delivery_address').val('');
        $('#iptFormaPagoCliente').val('');
        $('#store').val('').trigger('change');
        $('#store').prop('disabled', false);
        dctPedido.dctResumenPedido.lstPrecios = [];
        if (dctPedido.dctResumenPedido.lstDetallePedido.length >= 1){
            fncMensajeConfirmacionmns('¡Confirmación!', 'Si modifica el cliente se eliminaran los productos agregados, ¿Desea continuar?',
                function () {
                    dctPedido.dctResumenPedido.lstDetallePedido = [];
                    $('#tblDetallePedido').DataTable().clear().rows.add(dctPedido.dctResumenPedido.lstDetallePedido).draw();
                    $('.dataTotales').prop('hidden', true);
                    $('#rowGuardarPedido').prop('hidden', true);   
                    return;
                },
                function () {
                    
                });
                return;
        }
    }

    /////////////////////////////////////////////////////////////
    //////////////////////// Eventos Cliente//////////////////
    // Abrir modal formulario creación cliente
    $('#btnModalCrearCliente').on('click', function () {
        $('#modalCustomer').modal('show');
    });

    // Reestablecer formulario creación cliente
    $('#modalCustomer').on('hidden.bs.modal', function (e) {
        $('#formCustomer').trigger('reset');
    })

    // Crear un cliente
    $('#formCustomer').on('submit', function (e) {
        e.preventDefault();
        let parameters = new FormData(this);
        parameters.append('action', 'frmCrearClientejsn');
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                var newOption = new Option(response.value, response.id, false, true);
                fncCLienteslc();
                $('#identification').append(newOption).trigger('change');
                fncCargarCliente(response);
                $('#modalCustomer').modal('hide');
                return;
            }
        );
    });

    /////////////////////////////////////////////////////////////
    //////////////////////// Funciones producto///////////////////
    // Busqueda de producto
    function fncBuscarProductoslc() {
        $('#product_code').select2({
            theme: "bootstrap4",
            language: 'es',
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                url: window.location.pathname,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: function (params) {
                    var queryParameters = {
                        term: params.term,
                        action: 'slcBuscarProductojsn',
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Ingrese el código, nombre o presentación del producto',
            minimumInputLength: 1,
            templateResult: fncBuscarProductoRepo,
        // Seleccionar un producto
        }).on('select2:select', function (e) {
            let dctDataProducto = e.params.data;
            if (dctPedido.dctResumenPedido.lstDetallePedido.length >= 1){
                bolValidarDuplicado = fncValidarDuplicadosbol(dctDataProducto.id);
                if (bolValidarDuplicado.bolValidacion == true) {
                    fncMensajeConfirmacionmns('Alerta', 'Ya se encuentra en la tabla este producto ¿desea eliminar el actual y establecerlo de nuevo?',
                        function () {
                            dctPedido.dctResumenPedido.lstDetallePedido.splice(bolValidarDuplicado.intIndice, 1);
                            $('#tblDetallePedido').DataTable().clear().rows.add(dctPedido.dctResumenPedido.lstDetallePedido).draw();
                            fncValidarProductoLista(dctDataProducto);
                            return;
                        },
                        function () {
                            fncLimpiarFormularioDetalle();
                            return;
                        });
                    return;
                }
                else if(bolValidarDuplicado.bolValidacion == false){
                    fncValidarProductoLista(dctDataProducto);
                    return;
                }
                return;
            }
            fncValidarProductoLista(dctDataProducto);
            return;
        }).on('select2:unselect', function (e) {
            fncLimpiarFormularioDetalle();
            return;
        });
    }

    // Validar si un producto esta en pedido
    function fncValidarDuplicadosbol(intProductCode) {
        dctValidacion = {
            'bolValidacion': false,
            'intIndice': false,
        }
        dctPedido.dctResumenPedido.lstDetallePedido.forEach(function (item, index) {
            if(item.product_code == intProductCode){
                dctValidacion.bolValidacion = true;
                dctValidacion.intIndice = index;
            }
        });
        return dctValidacion;
    }

    // Función para validar si un producto esta en lista de precios
    function fncValidarProductoLista(dctDataProducto) {
        let bolProductoLista = false;
        let fltPrecioProducto = 0.00;
        let lstPrecios = dctPedido.dctResumenPedido.lstPrecios;
        if (lstPrecios.length > 0){
            lstPrecios.forEach(function (item, index) {
                if(item.product_code == dctDataProducto.id){
                    bolProductoLista = true;
                    fltPrecioProducto = item.unit_price
                }
            });
            if(bolProductoLista == true){
                fncCargarProducto(dctDataProducto, fltPrecioProducto);
                return;
            }
            fncMensajeInformacionmns('El producto no se encuentra registrado en la lista de precios');
            fncCargarProducto(dctDataProducto, dctDataProducto.full_sale_price);
            return;
        }
        fncCargarProducto(dctDataProducto, dctDataProducto.full_sale_price);
        return;
    }

    // Función para cargar la información de un producto
    function fncCargarProducto(dctDataProducto, fltPrecioProducto) {
        $('.dataProducto').prop('hidden', false);
        $('#iptCodigo').val(dctDataProducto.id);
        $('#iptUnidadVenta').val(dctDataProducto.sales_unit.sales_unit);
        $('#iva_producto').val(dctDataProducto.iva);
        $('#unit_price').val(fltPrecioProducto);
        $('#quantity').val(1);
        fncCalcularTotalProducto();
        let intIdProducto = dctDataProducto.id
        fncConsultarSaldoInventario(intIdProducto);
    }

    // Consultar saldo de inventario
    function fncConsultarSaldoInventario(intIdProducto) {
        var jsnParametros = new FormData();
        let intIdBodega = $('#store').val()
        jsnParametros.append('action', 'iptConsultarSaldo');
        jsnParametros.append('intCodigoProducto', intIdProducto);
        jsnParametros.append('intCodigoBodega', intIdBodega);
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                if(request.hasOwnProperty('error')){
                    $('#iptCantidadDisponible').val(0);
                    fncCompararCantidades();
                    return;
                }
                $('#iptCantidadDisponible').val(request[0].inventory_avail);
                return;
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    }

    // Calcular total por producto
    function fncCalcularTotalProducto() {
        let fltSubtotal = 0.00;
        let fltTotal = 0.00;
        let intCantidad = parseInt($('#quantity').val());
        let fltPrecioUnitario = parseFloat($('#unit_price').val()).toFixed(2);
        let fltIva = parseFloat($('#iva_producto').val()/100).toFixed(2);
        fltSubtotal = intCantidad * fltPrecioUnitario;
        fltIva = fltSubtotal * fltIva
        fltTotal = fltSubtotal + fltIva
        $('#subtotal_producto').val(parseFloat(fltSubtotal).toFixed(2));
        $('#iva_producto').val(parseFloat(fltIva).toFixed(2));
        $('#total_producto').val(parseFloat(fltTotal).toFixed(2));
        $('#quantity').focus();
    }

    // Reestablecer formulario producto
    function fncLimpiarFormularioDetalle() {
        $('#product_code').val('').trigger('change.select2');
        $('#iptCodigo').val('');
        $('#iptUnidadVenta').val('');
        $('#unit_price').val('');
        $('#iptCantidadDisponible').val('');
        $('#quantity').val('');
        $('#subtotal_producto').val('');
        $('#iva_producto').val('');
        $('#total_producto').val('');
        $('#product_code').select2('open');
        $('.dataProducto').prop('hidden', true);
    }
    
    // Validar inventario de producto
    function fncCompararCantidades() {
        let intCodigoProducto = $('#product_code').val();
        let intSaldoInventario = parseInt($('#iptCantidadDisponible').val());
        let intCantidadSolicitada = parseInt($('#quantity').val());
        if(intCantidadSolicitada > intSaldoInventario){
            var jsnParametros = new FormData();
            jsnParametros.append('action', 'iptValidarOrdenesComprajsn');
            jsnParametros.append('intCodigoProducto', intCodigoProducto);
            fncValidarOrdenesCompra(jsnParametros, intSaldoInventario, intCantidadSolicitada);
            return;
        }
    }

    // Validar ordenes de compra
    function fncValidarOrdenesCompra(jsnParametros, intSaldoInventario, intCantidadSolicitada) {
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                if(request.hasOwnProperty('qrsOrdenesCompraDetalle')){
                    let qrsOrdenesCompraDetalle = request;
                    let strDocumentoOrdenCompra = '';
                    let intCantidad = 0;
                    let datFechaEntregaOrden = '';
                    $.each(qrsOrdenesCompraDetalle, function (pos, dict) {
                    if(dict.qrsOrdenesCompraDetalle.order.condition.name == 'Abierta'){
                        strDocumentoOrdenCompra = dict.doc_number;
                        intCantidad = parseInt(dict.quantity);
                        datFechaEntregaOrden = dict.order.delivery_date;
                        intCantidadTotal = parseInt(intSaldoInventario) + intCantidad;
                        if(intSaldoInventario == 0){
                            strContenidoMensaje = 'El producto ' + request.product_code + ' tiene previsto el ingreso para ' + datFechaEntregaOrden + ' con la cantidad de ' + intCantidad + ' en la O.C. ' + strDocumentoOrdenCompra +
                                ' ¿Desea continuar la venta?';
                            fncMensajeConfirmarProximosIngresos(strContenidoMensaje, true);
                            return;
                        }
                        if(intCantidadSolicitada < intCantidadTotal){
                            strContenidoMensaje = 'El producto ' + request.product_code + ' tiene previsto el ingreso para ' + datFechaEntregaOrden + ' con la cantidad de ' + intCantidad + ' en la O.C. ' + strDocumentoOrdenCompra;
                            fncMensajeConfirmarProximosIngresos(strContenidoMensaje, false);
                            return;
                        }else if(intCantidadSolicitada > intCantidadTotal){
                            strContenidoMensaje = 'El producto ' + request.product_code + ' tiene previsto el ingreso para ' + datFechaEntregaOrden + ' con la cantidad de ' + intCantidad + ' en la O.C. ' + strDocumentoOrdenCompra +
                                '<br> Si se genera O.C. hoy el producto tendría un ingreso previsto para el '
                            fncMensajeConfirmarProximosIngresos(strContenidoMensaje, false);
                            return;
                        }
                    }
                });
                }else if(request.hasOwnProperty('datTiempoEntrega')){
                    if(intSaldoInventario == 0){
                        datFechaEntrega = request.datTiempoEntrega;
                        strContenidoMensaje = 'Si se genera O.C. hoy el producto tendría un ingreso previsto para el ' + datFechaEntrega +
                            '¿Desea continuar la venta?';
                        fncMensajeConfirmarProximosIngresos(strContenidoMensaje, true);
                        return;
                    }
                    datFechaEntrega = request.datTiempoEntrega;
                    strContenidoMensaje = 'Si se genera O.C. hoy el producto tendría un ingreso previsto para el ' + datFechaEntrega;
                    fncMensajeConfirmarProximosIngresos(strContenidoMensaje, false);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    }

    // Confirmar próximos ingresos de inventario
    function fncMensajeConfirmarProximosIngresos(strContenidoMensaje, bolSaldoCero) {
        let intCodigoCliente = $('#identification').val();
        let intCodigoProducto = $('#product_code').val();
        let strUnidadVenta = $('#iptUnidadVenta').val();
        let strDescripcionProducto = $('#product_code  :selected').text();
        var intCantidad = $('#quantity').val();
        let intSaldoInventario = $('#iptCantidadDisponible').val();
        let fltPrecioUnitario = parseFloat($('#unit_price').val()).toFixed(2);
        let fltSubtotal = parseFloat($('#subtotal_producto').val()).toFixed(2);
        let fltIva = parseFloat($('#iva_producto').val()).toFixed(2);
        let fltTotal = parseFloat($('#total_producto').val()).toFixed(2);
        if(bolSaldoCero == true){
            $.confirm({
                title: 'Próximos ingresos',
                content: '' +
                '<form action="" class="formName">' +
                '<div class="form-group">' +
                '<label>' + strContenidoMensaje + '</label>' +
                '<input type="number" placeholder="Ingrese la cantidad" class="quant form-control" required />' +
                '</div>' +
                '</form>',
                buttons: {
                    formSubmit: {
                        text: 'Confirmar',
                        btnClass: 'btn-blue',
                        action: function () {
                            let intCantidadFormulario = this.$content.find('.quant').val();
                            if(!intCantidadFormulario){
                                $.alert('Ingrese una cantidad');
                                return false;
                            }
                            intCantidad = intCantidadFormulario;
                            $('#quantity').val(intCantidadFormulario);
                            fncCalcularTotalProducto();
                            fltSubtotal = parseFloat($('#subtotal_producto').val()).toFixed(2);
                            fltIva = parseFloat($('#iva_producto').val()).toFixed(2);
                            fltTotal = parseFloat($('#total_producto').val()).toFixed(2);
                            dctProductoNuevo = {
                                'product_code': intCodigoProducto,
                                'product_desc': strDescripcionProducto,
                                'sales_unit': strUnidadVenta,
                                'unit_price': fltPrecioUnitario,
                                'quantity': intCantidad,
                                'subtotal': fltSubtotal,
                                'iva': fltIva,
                                'total': fltTotal,
                            }
                            fncAgregarProductoTabla(dctProductoNuevo);
                            return;
                        }
                    },
                    cancelar: {
                        text: "Cancelar venta",
                        btnClass: 'btn-red',
                        action: function () {
                            let intCantidad = 0;
                            jsnParametros = new FormData();
                            jsnParametros.append('action', 'btnVentasPerdidasjsn');
                            jsnParametros.append('identification', intCodigoCliente);
                            jsnParametros.append('product_code', intCodigoProducto);
                            jsnParametros.append('quantity', intCantidad);
                            fncGuardarVentaPerdida(jsnParametros, function () {
                                fncLimpiarFormularioDetalle();
                            });
                            return;
                        }
                    },
                },
                onContentReady: function () {
                    // bind to events
                    var jc = this;
                    this.$content.find('form').on('submit', function (e) {
                        // if the user submits the form by pressing enter in the field.
                        console.log('adentro');
                        e.preventDefault();
                        jc.$$formSubmit.trigger('click'); // reference the button and click it
                    });
                }
            });
            return;
        }
        $.confirm({
            columnClass: 'col-md-12',
            title: 'Próximos ingresos',
            content: strContenidoMensaje,
            buttons: {
                continuar: {
                    text: "Venta total",
                    btnClass: 'btn-success',
                    action: function () {
                        dctProductoNuevo = {
                            'product_code': intCodigoProducto,
                            'product_desc': strDescripcionProducto,
                            'sales_unit': strUnidadVenta,
                            'unit_price': fltPrecioUnitario,
                            'quantity': intCantidad,
                            'subtotal': fltSubtotal,
                            'iva': fltIva,
                            'total': fltTotal,
                        }
                        fncAgregarProductoTabla(dctProductoNuevo);
                    }
                },
                parcial: {
                    text: "Venta parcial",
                    btnClass: 'btn-dark',
                    action: function () {
                        jsnParametros = new FormData();
                        jsnParametros.append('action', 'btnVentasPerdidasjsn');
                        jsnParametros.append('identification', intCodigoCliente);
                        jsnParametros.append('product_code', intCodigoProducto);
                        jsnParametros.append('quantity', intCantidad);
                        fncGuardarVentaPerdida(jsnParametros, function () {
                            dctProductoNuevo = {
                                'product_code': intCodigoProducto,
                                'product_desc': strDescripcionProducto,
                                'sales_unit': strUnidadVenta,
                                'unit_price': fltPrecioUnitario,
                                'quantity': intSaldoInventario,
                                'subtotal': fltSubtotal,
                                'iva': fltIva,
                                'total': fltTotal,
                            }
                            if(intSaldoInventario > 0){
                                fncAgregarProductoTabla(dctProductoNuevo);
                            }
                            fncLimpiarFormularioDetalle();
                        });
                    }
                },
                cancelar: {
                    text: "Cancelar venta",
                    btnClass: 'btn-red',
                    action: function () {
                        jsnParametros = new FormData();
                        jsnParametros.append('action', 'btnVentasPerdidasjsn');
                        jsnParametros.append('identification', intCodigoCliente);
                        jsnParametros.append('product_code', intCodigoProducto);
                        jsnParametros.append('quantity', intCantidad);
                        fncGuardarVentaPerdida(jsnParametros, function () {
                            fncLimpiarFormularioDetalle();
                        });
                    }
                },
            }
        });   
    }

    // Agregar producto a tabla
    function fncAgregarProductoTabla(dctProductoNuevo) {
        dctPedido.dctResumenPedido.lstDetallePedido.push(dctProductoNuevo);
        if(dctPedido.dctResumenPedido.lstDetallePedido.length == 1){
            fncDetallePedidotbl();
            fncTiempoEntrega();
            $('.dataTotales').prop('hidden', false);
            $('#rowGuardarPedido').prop('hidden', false);
            $('#store').prop('disabled', true);            
            $('#tblDetallePedido').DataTable().clear().rows.add(dctPedido.dctResumenPedido.lstDetallePedido).draw();
            fncMensajeConfirmacionmns('Confirmación', '¿Desea agregar otro producto?',
            function () {    
                fncLimpiarFormularioDetalle();
                fncCalcularPedido();
                return;
            },
            function () {
                fncCalcularPedido();
                $('#mdlAgregarProducto').modal('hide');
                return;
            });
            return;
        }
        $('#tblDetallePedido').DataTable().clear().rows.add(dctPedido.dctResumenPedido.lstDetallePedido).draw();
        fncMensajeConfirmacionmns('Confirmación', '¿Desea agregar otro producto?',
        function () {    
            fncLimpiarFormularioDetalle();
            fncCalcularPedido();
            return;
        },
        function () {
            fncCalcularPedido();
            $('#mdlAgregarProducto').modal('hide');
            return;
        });
    }

    // Cargar tabla detalle de pedido
    function fncDetallePedidotbl() {
        tblDetallePedido = $('#tblDetallePedido').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            pageLength: 0,
            lengthMenu: [5, 10, 20, 50, 100],
            deferRender: true,
            language: {
                "decimal": "",
                "emptyTable": "No existe información creada",
                "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                "infoEmpty": "Mostrando 0 de 0 Entradas",
                "infoFiltered": "(Filtrado de _MAX_ total entradas)",
                "infoPostFix": "",
                "thousands": ",",
                "lengthMenu": "Mostrar _MENU_ Entradas",
                "loadingRecords": "Cargando...",
                "processing": "Procesando...",
                "search": "Buscar:",
                "zeroRecords": "Sin resultados encontrados",
                "paginate": {
                    "first": "Primero",
                    "last": "Ultimo",
                    "next": "Siguiente",
                    "previous": "Anterior"
                },
            },
            data: dctPedido.dctResumenPedido.lstDetallePedido,
            columns: [
                { "data": "product_code"},
                { "data": "product_desc"},
                { "data": "sales_unit"},
                { "data": "unit_price"},
                { "data": "quantity"},
                { "data": "subtotal"},
                { "data": "iva"},
                { "data": "total"},
                { "data": "product_code"}
            ],
            columnDefs: [
                {
                    targets: [-5, -7, -8, -9],
                    class: 'text-center',
                    orderable: true,
                },
                {
                    targets: [-2, -3, -4, -6],
                    class: 'text-center',
                    orderable: true,
                    render: function (data, type, row) {
                        return '$ '+ parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat" title="Editar producto"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Eliminar producto"><i class="fas fa-trash"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });

        // Editar producto
        $('#tblDetallePedido tbody').on('click', 'a[rel="edit"]', function (e) {
            e.preventDefault();
            var tr = tblDetallePedido.cell($(this).closest('td, li')).index();
            var data_row = tblDetallePedido.row(tr.row).data();
            $.each(dctPedido.dctResumenPedido.lstDetallePedido, function (pos, value) {
                if(data_row.product_code == value.product_code){
                    dctPedido.dctResumenPedido.lstDetallePedido.splice(pos, 1);
                    $('#tblDetallePedido').DataTable().clear().rows.add(dctPedido.dctResumenPedido.lstDetallePedido).draw();
                    $('#product_code').val(data_row.product_code).trigger('change.select2');
                    $('#iptCodigo').val(data_row.product_code).trigger('change.select2');
                    $('#iptUnidadVenta').val(data_row.sales_unit).trigger('change.select2');
                    $('#quantity').val(data_row.quantity);
                    $('#unit_price').val(data_row.unit_price);
                    $('#subtotal').val(data_row.subtotal);
                    $('#iva_producto').val(data_row.iva_producto);
                    $('#total_producto').val(data_row.total_producto);
                    var jsnParametros = new FormData();
                    jsnParametros.append('action', 'iptConsultarSaldo');
                    jsnParametros.append('intCodigoProducto', data_row.product_code);
                    fncConsultarSaldoInventario(jsnParametros);
                    $('#mdlAgregarProducto').modal('show');
                    return;
                }
            });
            return;
        });
        
        $('#tblDetallePedido tbody').on('click', 'a[rel="delete"]', function (e) {
            e.preventDefault();
            var tr = tblDetallePedido.cell($(this).closest('td, li')).index();
            var data_row = tblDetallePedido.row(tr.row).data();
            $.each(dctListaPreciosDetalle.lstDetalleListaPrecios, function (pos, value) {
                if(data_row.product_code == value.product_code){
                    fncMensajeConfirmacionmns('Confirmación!', '¿Desea eliminar el producto de la tabla?',
                    function () {
                        dctListaPreciosDetalle.lstDetalleListaPrecios.splice(pos, 1);
                        $('#tblDetallePedido').DataTable().clear().rows.add(dctListaPreciosDetalle.lstDetalleListaPrecios).draw();
                        return;
                    },
                    function () {
                        
                    });
                    return;
                }
            });
            return;
        });
    }

    function fncTiempoEntrega() {
        intCodigoCiudad = $('#city').val();
        intCodigoZona = $('#customer_zone').val();
        intCodigoBodega = $('#store').val();
        let jsnParametros = new FormData();
        jsnParametros.append('action', 'iptValidarTiempoEntregajsn');
        jsnParametros.append('intCodigoCiudad', intCodigoCiudad);
        jsnParametros.append('intCodigoZona', intCodigoZona);
        jsnParametros.append('intCodigoBodega', intCodigoBodega);
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                console.log(request);
                if (request.hasOwnProperty('qrsTiemposEntrega')) {
                    datTiempoEntrega = String(request.qrsTiemposEntrega)
                    document.getElementById('deliver_date').setAttribute("min", datTiempoEntrega);
                } else{
                    datTiempoEntrega = String(request.datTiempoEntrega)
                    document.getElementById('deliver_date').setAttribute("min", datTiempoEntrega);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    }
    // Guardar venta perdida
    function fncGuardarVentaPerdida(jsnParametros, fncRetorno) {
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                fncRetorno();
                return;
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    } 

    // Actualizar calcular totales pedido
    function fncCalcularPedido() {
        let subtotal = 0.00;
        let iva = 0.00;
        let total = 0.00;
        $.each(dctPedido.dctResumenPedido.lstDetallePedido, function (pos, dict) {
            subtotal += parseFloat(dict.subtotal);
            iva += parseFloat(dict.iva)
            total += parseFloat(dict.total)
        });
        $('#subtotal').val('$ ' + subtotal.toFixed(2));
        $('#iva').val('$ ' + iva.toFixed(2));
        $('#total').val('$ ' + total.toFixed(2));
    }

    /////////////////////////////////////////////////////////////
    //////////////////////// Eventos producto///////////////////
    // Abrir modal formulario producto
    $('#btnModalProductos').on('click', function () {
        let strBodega = $('#store').val()
        if (strBodega == ''){
            fncMensajeInformacionmns('!Seleccione una bodega!');
            return;
        }
        else if (dctPedido.dctResumenPedido.lstPrecios.length == 0) {
            fncMensajeInformacionmns('El cliente no tiene lista de precios asociada, los productos se mantienen en precio de venta full');
        }
        $('#mdlAgregarProducto').modal('show');
    });

    // Enfocar busqueda de producto
    $('#mdlAgregarProducto').on('shown.bs.modal', function (e) {
        $('#product_code').select2('open');
    });

    // Cerrar modal formulario producto
    $('#mdlAgregarProducto').on('hidden.bs.modal', function () {
        fncLimpiarFormularioDetalle();
    });

    // Establecer cantidad del producto
    $("#quantity").on('change', function (){
        fncCompararCantidades();
        fncCalcularTotalProducto();
    });

    // Agregar producto
    $('#frmProducto').on('submit', function (e) {
        e.preventDefault();
        let intCodigoProducto = $('#product_code').val();
        let strUnidadVenta = $('#iptUnidadVenta').val();
        let strDescripcionProducto = $('#product_code  :selected').text();
        let intCantidad = $('#quantity').val();
        let fltPrecioUnitario = parseFloat($('#unit_price').val()).toFixed(2);
        let fltSubtotal = parseFloat($('#subtotal_producto').val()).toFixed(2);
        let fltIva = parseFloat($('#iva_producto').val()).toFixed(2);
        let fltTotal = parseFloat($('#total_producto').val()).toFixed(2);
        dctProductoNuevo = {
            'product_code': intCodigoProducto,
            'product_desc': strDescripcionProducto,
            'sales_unit': strUnidadVenta,
            'unit_price': fltPrecioUnitario,
            'quantity': intCantidad,
            'subtotal': fltSubtotal,
            'iva': fltIva,
            'total': fltTotal,
        }
        fncAgregarProductoTabla(dctProductoNuevo)
    });

    // Eliminar productos de la tabla
    $('#btnEliminarProductos').on('click', function (e) {
        e.preventDefault();
        if (dctPedido.dctResumenPedido.lstDetallePedido.length >= 1){
            fncMensajeConfirmacionmns('¡Confirmación!', '¿Desea eliminar todos los productos de la tabla?',
                function () {
                    dctPedido.dctResumenPedido.lstDetallePedido = [];
                    $('#tblDetallePedido').DataTable().clear().rows.add(dctPedido.dctResumenPedido.lstDetallePedido).draw();
                    $('.dataTotales').prop('hidden', true);
                    $('#rowGuardarPedido').prop('hidden', true);
                    $('#store').prop('disabled', false);
                    return;
                },
                function () {
                    
                });
                return;
        }
        fncMensajeInformacionmns('!La tabla se encuentra vacia!');
        return;
    })

    //Guardar pedido
    $('#frm').on('submit', function (e) {
        e.preventDefault();
        if (dctPedido.dctResumenPedido.lstDetallePedido.length >= 1){
            var parameters = new FormData(this);
            parameters.append('action', 'btnGuardarPedidojsn');
            parameters.append('lstDetalleListaPrecios', JSON.stringify(dctPedido.dctResumenPedido.lstDetallePedido));
            fncGuardarFormularioAjax(window.location.pathname, 'Notificación', '¿Está seguro de guardar el registro?', parameters, function (response) {
                fncMensajeConfirmacionDocumentomns('¡Confirmación!', 'Seleccione una opción:',
                function () {
                    window.open('/configuracion/exportar_lista_pdf/' + response.id + '/', '_blank');
                    fncMensajeConfirmacionmns('¡Confirmación!', '¿Desea crear una nueva lista?',
                        function () {
                            location.href = '/configuracion/crear_lista_precios/';
                            return;
                        },
                        function () {
                            location.href = '/configuracion/ver_lista_precios/';
                            return;
                        });
                        return;
                },
                function () {
                    location.href = '/configuracion/crear_lista_precios/';
                    return;
                });
            });
            return;
        }
        fncMensajeInformacionmns('!Debe agregar al menos un producto a la lista de precios!');
        return;
    });

});