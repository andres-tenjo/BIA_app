var dctListaPreciosDetalle = {
    lstDetalleListaPrecios: []
}

$(function () {

    // Variables y funciones
    dctListaPrecios = {

        // Tabla indicadores por asesor comercial
        fncDetalleListaPreciostbl: function () {
            tblDetalleListaPrecio = $('#tblDetalleListaPrecios').DataTable({
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
                data: dctListaPreciosDetalle.lstDetalleListaPrecios,
                columns: [
                    { "data": "product_code"},
                    { "data": "product_desc"},
                    { "data": "unit_price"},
                    { "data": "lead_time"},
                    { "data": "quantity"},
                    { "data": "observations"},
                    { "data": "observations"},
                ],
                columnDefs: [
                    {
                        targets: [-2, -3, -4, -6, -7],
                        class: 'text-center',
                        orderable: true,
                    },
                    {
                        targets: [-5],
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
            $('#tblDetalleListaPrecios tbody').on('click', 'a[rel="edit"]', function (e) {
                e.preventDefault();
                var tr = tblDetalleListaPrecio.cell($(this).closest('td, li')).index();
                var data_row = tblDetalleListaPrecio.row(tr.row).data();
                $.each(dctListaPreciosDetalle.lstDetalleListaPrecios, function (pos, value) {
                    if(data_row.product_code == value.product_code){
                        dctListaPreciosDetalle.lstDetalleListaPrecios.splice(pos, 1);
                        $('#tblDetalleListaPrecios').DataTable().clear().rows.add(dctListaPreciosDetalle.lstDetalleListaPrecios).draw();
                        $('#product_code').val(data_row.product_code).trigger('change.select2');
                        $('#quantity').val(data_row.quantity);
                        $('#lead_time').val(data_row.lead_time);
                        $('#unit_price').val(data_row.unit_price);
                        $('#observation').val(data_row.observation);
                        $('#mdlAgregarProducto').modal('show');
                        return;
                    }
                });
                return;
            });
            
            $('#tblDetalleListaPrecios tbody').on('click', 'a[rel="delete"]', function (e) {
                e.preventDefault();
                var tr = tblDetalleListaPrecio.cell($(this).closest('td, li')).index();
                var data_row = tblDetalleListaPrecio.row(tr.row).data();
                $.each(dctListaPreciosDetalle.lstDetalleListaPrecios, function (pos, value) {
                    if(data_row.product_code == value.product_code){
                        fncMensajeConfirmacionmns('Confirmación!', '¿Desea eliminar el producto de la tabla?',
                        function () {
                            dctListaPreciosDetalle.lstDetalleListaPrecios.splice(pos, 1);
                            $('#tblDetalleListaPrecios').DataTable().clear().rows.add(dctListaPreciosDetalle.lstDetalleListaPrecios).draw();
                            return;
                        },
                        function () {
                            
                        });
                        return;
                    }
                });
                return;
            });
        },

        fncLimpiarFormularioDetalle: function () {
            $('#product_code').val('').trigger('change.select2');
            $('#quantity').val('');
            $('#lead_time').val('');
            $('#unit_price').val('');
            $('#observation').val('');
            $('#product_code').select2('open');
        },

        fncAgregarProductoTabla: function () {
            fncMensajeConfirmacionmns('Confirmación', '¿Desea agregar otro producto?',
            function () {
                dctListaPreciosDetalle.lstDetalleListaPrecios.push(dctProductoNuevo);
                $('#tblDetalleListaPrecios').DataTable().clear().rows.add(dctListaPreciosDetalle.lstDetalleListaPrecios).draw();
                dctListaPrecios.fncLimpiarFormularioDetalle();
                return;
            },
            function () {
                dctListaPreciosDetalle.lstDetalleListaPrecios.push(dctProductoNuevo);
                $('#tblDetalleListaPrecios').DataTable().clear().rows.add(dctListaPreciosDetalle.lstDetalleListaPrecios).draw();
                $('#mdlAgregarProducto').modal('hide');
                return;
            });
        },

        fncValidarDuplicadosbol: function (intProductCode) {
            dctValidacion = {
                'bolValidacion': false,
                'intIndice': false,
            }
            dctListaPreciosDetalle.lstDetalleListaPrecios.forEach(function (item, index) {
                if(item.product_code == intProductCode){
                    dctValidacion.bolValidacion = true;
                    dctValidacion.intIndice = index;
                }
            });
            return dctValidacion;
        }
    }
    
    // Eventos
    
    // Cargar tabla detalle lista precios
    dctListaPrecios.fncDetalleListaPreciostbl()

    // Función para cargar libreria Select2 para los input tipo select
    fncCargarLibreriaSelect2('.select2', 'Seleccione o cree una nueva');

    // Función para cargar libreria TouchSpin para los input tipo número, decimal y moneda
    fncCargarLibreriaTouchSpinFormatoEntero();
    fncCargarLibreriaTouchSpinFormatoDecimal();
    fncCargarLibreriaTouchSpinFormatoMoneda();

    // Abrir modal detalle de lista
    $('#btnModalProductos').on('click', function () {
        $('#mdlAgregarProducto').modal('show');
    });

    // Buscar producto
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
    });

    // Focus formulario categoría
    $('#mdlAgregarProducto').on('shown.bs.modal', function (e) {
        $('#product_code').select2('open');
    });

    // Borrar lo digitado en el formulario detalle de lista
    $('#mdlAgregarProducto').on('hidden.bs.modal', function () {
        dctListaPrecios.fncLimpiarFormularioDetalle();
    });

    // Agregar producto a tabla detalle lista precios
    $('#frmProducto').on('submit', function (e) {
        e.preventDefault();
        var intCodigoProducto = $('#product_code').val();
        var strDescripcionProducto = $('#product_code  :selected').text();
        var fltPrecioUnitario = parseFloat($('#unit_price').val()).toFixed(2);
        var datTiempoEntrega = $('#lead_time').val();
        var intCantidad = $('#quantity').val();
        var strObservacion = $('#observation').val();
        dctProductoNuevo = {
            'product_code': intCodigoProducto,
            'product_desc': strDescripcionProducto,
            'unit_price': fltPrecioUnitario,
            'lead_time': datTiempoEntrega,
            'quantity': intCantidad,
            'observations': strObservacion
        }
        if (dctListaPreciosDetalle.lstDetalleListaPrecios.length >= 1){
            bolValidarDuplicado = dctListaPrecios.fncValidarDuplicadosbol(dctProductoNuevo.product_code);
            if (bolValidarDuplicado.bolValidacion == true) {
                fncMensajeConfirmacionmns('Alerta', 'Ya se encuentra en la tabla este producto ¿desea eliminar el actual y establecerlo de nuevo?',
                    function () {
                        dctListaPreciosDetalle.lstDetalleListaPrecios.splice(bolValidarDuplicado.intIndice, 1);
                        dctListaPrecios.fncAgregarProductoTabla();
                        $('#tblDetalleListaPrecios').DataTable().clear().rows.add(dctListaPreciosDetalle.lstDetalleListaPrecios).draw();
                        dctListaPrecios.fncLimpiarFormularioDetalle();
                        return;
                    },
                    function () {
                        dctListaPrecios.fncLimpiarFormularioDetalle();
                        return;
                    });
            }
            else if(bolValidarDuplicado.bolValidacion == false){
                dctListaPrecios.fncAgregarProductoTabla();
            }
        }
        else if (dctListaPreciosDetalle.lstDetalleListaPrecios.length < 1){
            dctListaPrecios.fncAgregarProductoTabla();
        }
    });

    // Guardar lista de precios exportar pdf e imprimir
    $('#frm').on('submit', function (e) {
        e.preventDefault();
        if (dctListaPreciosDetalle.lstDetalleListaPrecios.length >= 1){
            var parameters = new FormData(this);
            parameters.append('action', 'btnGuardarListaPreciosjsn');
            parameters.append('lstDetalleListaPrecios', JSON.stringify(dctListaPreciosDetalle.lstDetalleListaPrecios));
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
                    location.href = '/configuracion/exportar_lista_excel/' + response.id + '';
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

    // Eliminar productos de la tabla
    $('#btnEliminarProductos').on('click', function (e) {
        e.preventDefault();
        if (dctListaPreciosDetalle.lstDetalleListaPrecios.length >= 1){
            fncMensajeConfirmacionmns('¡Confirmación!', '¿Desea eliminar todos los productos de la tabla?',
                function () {
                    dctListaPreciosDetalle.lstDetalleListaPrecios = [];
                    $('#tblDetalleListaPrecios').DataTable().clear().rows.add(dctListaPreciosDetalle.lstDetalleListaPrecios).draw();
                    return;
                },
                function () {
                    
                });
                return;
        }
        fncMensajeInformacionmns('!La tabla se encuentra vacia!');
        return;
    })
    
});