/////////////////////////////////////////////////////////////
// Variables
var dctCotizacion = {

    dctResumenCotizacion:{
        lstDetalleCotizacion: [],
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
            var dctDataCliente = e.params.data;
            var intIdCliente = dctDataCliente.id;
            var jsnparameters = new FormData();
            jsnparameters.append('action', 'slcEstadoCarteraClientejsn');
            jsnparameters.append('intIdCliente', intIdCliente);
            fncValidarCarteraCliente(window.location.pathname, jsnparameters,
                function () {
                    if(!dctDataCliente.price_list){
                        fncCargarCliente(dctDataCliente);
                        fncMensajeInformacionmns('El cliente no tiene lista de precios asociada, los productos se mantienen en precio de venta full');
                        return;    
                    }
                    intIdListaPrecios = dctDataCliente.price_list.id;
                    var parameters = new FormData();
                    parameters.append('action', 'slcListaPreciosDetallejsn');
                    parameters.append('intIdListaPrecios', intIdListaPrecios);
                    fcnCargarListaPrecios(window.location.pathname, parameters,
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
    function fncValidarCarteraCliente(url, jsnParametros, fncRetorno) {
        $.ajax({
            url: url,
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
                    fncRetorno(request);
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
    function fcnCargarListaPrecios(url, jsnParametros, fncSuccess) {
        $.ajax({
            url: url,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                dctCotizacion.dctResumenCotizacion.lstListaPrecios = request.data;
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
        $('#city').val(dctDataCliente.city.id);
        $('#iptDireccionCliente').val(dctDataCliente.delivery_address);
        $('#iptCategoriaCliente').val(dctDataCliente.customer_cat.customer_cat);
        $('#iptObservacionesCliente').val('');
        $('#iptFormaPagoCliente').val(dctDataCliente.pay_method.name);
        $('#colEstadoCarteraCliente').prop('hidden', false);
        $('#iptEstadoCarteraCliente').val('Sin pagos pendientes');
    }
    
    // Función que limpia la información del cliente en el pedido
    function fncLimpiarCliente() {
        $('.dataCliente').prop('hidden', true);
        $('#iptIdentificacionCliente').val('');
        $('#iptCelularCliente').val('');
        $('#iptCiudadCliente').val('');
        $('#iptDireccionCliente').val('');
        $('#iptObservacionesCliente').val('');
        $('#iptFormaPagoCliente').val('');
        $('#colEstadoCarteraCliente').prop('hidden', true);
        $('#iptEstadoCarteraCliente').val('');
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
        var parameters = new FormData(this);
        parameters.append('action', 'frmCrearClientejsn');
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                var newOption = new Option(response.value, response.id, false, true);
                if(!response.price_list){
                    fncMensajeInformacionmns('El cliente no tiene lista de precios asociada, los productos se mantienen en precio de venta full');
                    return;    
                }
                intIdListaPrecios = response.price_list.id;
                var parameters = new FormData();
                parameters.append('action', 'slcListaPreciosDetallejsn');
                parameters.append('intIdListaPrecios', intIdListaPrecios);
                fcnCargarListaPrecios(window.location.pathname, parameters,
                    function () {
                        fncCLienteslc();
                        $('#identification').append(newOption).trigger('change');
                        fncCargarCliente(response);
                        $('#modalCustomer').modal('hide');
                        return;
                    }
                );
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
            if (dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion.length >= 1){
                bolValidarDuplicado = fncValidarDuplicadosbol(dctDataProducto.id);
                if (bolValidarDuplicado.bolValidacion == true) {
                    fncMensajeConfirmacionmns('Alerta', 'Ya se encuentra en la tabla este producto ¿desea eliminar el actual y establecerlo de nuevo?',
                        function () {
                            dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion.splice(bolValidarDuplicado.intIndice, 1);
                            $('#tblDetalleCotizacion').DataTable().clear().rows.add(dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion).draw();
                            let lstPrecios = dctCotizacion.dctResumenCotizacion.lstPrecios;
                            fncCargarProducto(dctDataProducto, lstPrecios);
                            return;
                        },  
                        function () {
                            fncLimpiarFormularioDetalle();
                            return;
                        });
                    return;
                }
                else if(bolValidarDuplicado.bolValidacion == false){
                    let lstPrecios = dctCotizacion.dctResumenCotizacion.lstPrecios;
                    fncCargarProducto(dctDataProducto, lstPrecios);
                    return;
                }
                return;
            }
            let lstPrecios = dctCotizacion.dctResumenCotizacion.lstPrecios;
            fncCargarProducto(dctDataProducto, lstPrecios);
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
        dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion.forEach(function (item, index) {
            if(item.product_code == intProductCode){
                dctValidacion.bolValidacion = true;
                dctValidacion.intIndice = index;
            }
        });
        return dctValidacion;
    }

    // Función para cargar la información de un producto
    function fncCargarProducto(dctDataProducto, lstPrecios) {
        if (lstPrecios.length > 0){
            lstPrecios.forEach(function (item, index) {
                if(item.product_code == dctDataProducto.id){
                    $('.dataProducto').prop('hidden', false);
                    $('#iptCodigo').val(dctDataProducto.id);
                    $('#iptUnidadVenta').val(dctDataProducto.sales_unit.sales_unit);
                    $('#iva_producto').val(dctDataProducto.iva + ' %');
                    $('#unit_price').val(item.unit_price); 
                    $('#quantity').focus();
                    return;
                }
                else if(item.product_code != dctDataProducto.id){
                    fncMensajeConfirmacionmns('Confirmación!', 'El producto no se encuentra registrado en la lista de precios ¿Desea envíar una notificación para incluirlo?',
                        function () {
                            // Enviar alerta para incluir producto a lista de precios
                            return;
                        },
                        function () {
                            $('.dataProducto').prop('hidden', false);
                            $('#iptCodigo').val(dctDataProducto.id);
                            $('#iptUnidadVenta').val(dctDataProducto.sales_unit.sales_unit);
                            $('#iva_producto').val(dctDataProducto.iva + ' %');
                            $('#unit_price').val(dctDataProducto.full_sale_price);
                            $('#quantity').focus();
                            return false;
                        }
                    );
                    return;
                }
            });
        }
        $('.dataProducto').prop('hidden', false);
        $('#iptCodigo').val(dctDataProducto.id);
        $('#iptUnidadVenta').val(dctDataProducto.sales_unit.sales_unit);
        $('#iva_producto').val(dctDataProducto.iva);
        $('#unit_price').val(dctDataProducto.full_sale_price);  
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'iptConsultarSaldo');
        jsnParametros.append('intCodigoProducto', dctDataProducto.id);
        return;
    }

    // Reestablecer formulario producto
    function fncLimpiarFormularioDetalle() {
        $('#product_code').val('').trigger('change.select2');
        $('#iptCodigo').val('');
        $('#iptUnidadVenta').val('');
        $('#lead_time').val('');
        $('#quantity').val('');
        $('#unit_price').val('');
        $('#due_date').val('');
        $('#observations').val('');
        $('#product_code').select2('open');
        $('.dataProducto').prop('hidden', true);
    }

    // Agregar producto a tabla
    function fncAgregarProductoTabla(dctProductoNuevo) {
        dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion.push(dctProductoNuevo);
        if(dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion.length == 1){
            fncDetallePedidotbl();
            $('.dataTotales').prop('hidden', false);
            $('#rowGuardarPedido').prop('hidden', false);
            document.getElementById('follow_up_date').setAttribute("min", '2022-05-09');
            $('#tblDetallePedido').DataTable().clear().rows.add(dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion).draw();
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
        $('#tblDetallePedido').DataTable().clear().rows.add(dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion).draw();
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
            data: dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion,
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
            $.each(dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion, function (pos, value) {
                if(data_row.product_code == value.product_code){
                    dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion.splice(pos, 1);
                    $('#tblDetallePedido').DataTable().clear().rows.add(dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion).draw();
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
        $.each(dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion, function (pos, dict) {
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
        if (dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion.length >= 1){
            fncMensajeConfirmacionmns('¡Confirmación!', '¿Desea eliminar todos los productos de la tabla?',
                function () {
                    dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion = [];
                    $('#tblDetallePedido').DataTable().clear().rows.add(dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion).draw();
                    $('.dataTotales').prop('hidden', true);
                    $('#rowGuardarPedido').prop('hidden', true);   
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
        if (dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion.length >= 1){
            var parameters = new FormData(this);
            parameters.append('action', 'btnGuardarPedidojsn');
            parameters.append('lstDetalleListaPrecios', JSON.stringify(dctCotizacion.dctResumenCotizacion.lstDetalleCotizacion));
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