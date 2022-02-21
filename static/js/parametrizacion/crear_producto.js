
dctOpcionesCrearProducto = {

    fncCategoriaProductoslc: function () {
        $('select[name="product_cat"]').select2({
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
                        action: 'slcBuscarCategoriaProductojsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione o cree una nueva',
        });  
    },
    fncSubcategoriaProductoslc: function () {
        $('select[name="product_subcat"]').select2({
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
                        action: 'slcBuscarSubcategoriaProductojsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione o cree una nueva',
        });  
    },
    fncUnidadCompraslc: function () {
        $('select[name="purchase_unit"]').select2({
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
                        action: 'slcBuscarUnidadComprajsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione o cree una nueva',
        });  
    },
    fncUnidadVentaslc: function () {
        $('select[name="sales_unit"]').select2({
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
                        action: 'slcBuscarUnidadVentajsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione o cree una nueva',
        });  
    },
    
}

$(function(){

    // Definición de variables
    const intCantidadUnidadCompra = document.getElementById('quantity_udc');
    const fltPrecioCompra = document.getElementById('price_udc');
    const intCantidadUnidadVenta = document.getElementById('quantity_udv');
    const fltPrecioVenta = document.getElementById('price_udv');
    const fltIvaProducto = document.getElementById('prod_iva');
    const fltOtrosImpuestos = document.getElementById('prod_other_tax');
    const intTiempoEntregaProveedor = document.getElementById('prod_del_time');

    // Función para cargar libreria Select2 para los input tipo select
    fncCargarLibreriaSelect2('Seleccione o cree una nueva');
    
    // Función para cargar libreria TouchSpin para los input tipo número, decimal y moneda
    fncCargarLibreriaTouchSpinFormatoEntero();
    fncCargarLibreriaTouchSpinFormatoDecimal();
    fncCargarLibreriaTouchSpinFormatoMoneda();

    if (intCantidadUnidadCompra.value === '' || fltPrecioCompra.value === ''){
        intCantidadUnidadCompra.value = 0;
        fltPrecioCompra.value = 0;
    }
    
    if (intCantidadUnidadVenta.value === '' || fltPrecioVenta.value === ''){
        intCantidadUnidadVenta.value = 0;
        fltPrecioVenta.value = 0;
    }
    
    if (fltIvaProducto.value === '' || fltOtrosImpuestos.value === '' || intTiempoEntregaProveedor.value === ''){
        fltIvaProducto.value = 0.00;
        fltOtrosImpuestos.value = 0.00;
        intTiempoEntregaProveedor.value = 0;
    }
    
    // Abrir modal creación categoría producto
    $('.btnAddCat').on('click', function () {
        $('#myModalCategory').modal('show');
    });

    // Focus formulario categoría
    $('#myModalCategory').on('shown.bs.modal', function (e) {
        $('#category_name').focus();
    });
    
    // Borrar lo digitado en el formulario categoría
    $('#myModalCategory').on('hidden.bs.modal', function (e) {
        $('#frmCatProd').trigger('reset');
    });

    // Guardar el registro de categoría de producto
    $('#frmCatProd').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'frmCrearCategoriaProductojsn');
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                var newOption = new Option(response.product_cat, response.id, false, true);
                dctOpcionesCrearProducto.fncCategoriaProductoslc();
                $('#prod_category').append(newOption).trigger('change');
                $('#myModalCategory').modal('hide');
            });
    });
    
    // Abrir modal creación subcategoría producto
    $('.btnAddSubcat').on('click', function () {
        $('#myModalSubcategory').modal('show');
    });

    // Focus formulario subcategoría
    $('#myModalSubcategory').on('shown.bs.modal', function (e) {
        $('#subcategory_name').focus();
    });

    // Borrar lo digitado en el formulario subcategoría
    $('#myModalSubcategory').on('hidden.bs.modal', function (e) {
        $('#frmSubcatProd').trigger('reset');
    });

    // Guardar el registro de subcategoría de producto
    $('#frmSubcatProd').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'frmCrearSubcategoriaProductojsn');
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                var newOption = new Option(response.product_subcat, response.id, false, true);
                dctOpcionesCrearProducto.fncSubcategoriaProductoslc();
                $('select[name="product_subcat"]').append(newOption).trigger('change');
                $('#myModalSubcategory').modal('hide');
            });
    });

    // Abrir modal creación unidad de medida en compra
    $('.btnAddUdc').on('click', function () {
        $('#myModalUdc').modal('show');
    });

    // Focus formulario unidad de compra
    $('#myModalUdc').on('shown.bs.modal', function (e) {
        $('#udc_name').focus();
    });

    // Borrar lo digitado en el formulario unidad de compra
    $('#myModalUdc').on('hidden.bs.modal', function (e) {
        $('#frmUdcProd').trigger('reset');
    });

    // Guardar el registro de unidad de compra
    $('#frmUdcProd').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'frmCrearUnidadComprajsn');
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Está seguro de guardar el registro?', parameters, function (response) {
                var newOption = new Option(response.purchase_unit, response.id, false, true);
                dctOpcionesCrearProducto.fncUnidadCompraslc();
                $('select[name="purchase_unit"]').append(newOption).trigger('change');
                $('#myModalUdc').modal('hide');
            });
    });

    // Abrir modal creación unidad de medida en venta
    $('.btnAddUdv').on('click', function () {
        $('#myModalUdv').modal('show');
    });

    // Focus formulario unidad de venta
    $('#myModalUdv').on('shown.bs.modal', function (e) {
        $('#udv_name').focus();
    });

    // Borrar lo digitado en el formulario unidad de venta
    $('#myModalUdv').on('hidden.bs.modal', function (e) {
        $('#frmUdvProd').trigger('reset');
    });

    // Guardar el registro de unidad de venta
    $('#frmUdvProd').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'frmCrearUnidadVentajsn');
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Está seguro de guardar el registro?', parameters, function (response) {
                var newOption = new Option(response.sales_unit, response.id, false, true);
                dctOpcionesCrearProducto.fncUnidadVentaslc();
                $('select[name="sales_unit"]').append(newOption).trigger('change');
                $('#myModalUdv').modal('hide');
            });
    });

});




///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////// FUNCIONES PARA SCAN QRCODE Y BARCODE /////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
/*$('.btnScanQrCode').on('click', function () {
        $('#myModalQr').modal('show');
        let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
        scanner.addListener('scan', function (content) {
            console.log(content);
            $('#myModalQr').modal('hide');
            scanner.stop();
        });
        Instascan.Camera.getCameras().then(function (cameras) {
            if (cameras.length > 0) {
            scanner.start(cameras[0]);
            } else {
            console.error('Su equipo no tiene una camara conectada, por favor conecte una e intentelo nuevamente');
            }
        }).catch(function (e) {
            console.error(e);
        });    
    });*/

    // $('.btnScanQrCode').on('click', function () {
    //     Quagga.init({
    //         inputStream : {
    //           name : "Live",
    //           type : "LiveStream",
    //           target: document.getElementById('preview')
    //         },
    //         decoder : {
    //           readers : ["code_128_reader"]
    //         }
    //       }, function(err) {
    //           if (err) {
    //               console.log(err);
    //               return
    //           }
    //           console.log("Initialization finished. Ready to start");
    //           Quagga.start();
    //     });
    // });

    // Detener lector QR cuando se cierre el modal
    // $('#myModalQr').on('hidden.bs.modal', function (e) {
    //     let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
    //     scanner.stop();
    // });