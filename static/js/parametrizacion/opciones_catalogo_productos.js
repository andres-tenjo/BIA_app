dctOpcionesCatalogoProductos = {
        
    // Tabla categoría de producto
    fncCategoriaProductotbl: function () {
        tblCategoriaProducto = $('#catTable').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: false,
            info: false,
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
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action':'tblCategoriaProductojsn'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                { "data": "n"},
                { "data": "product_cat"},
                { "data": "state.name"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat" title="Editar categoría"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo-alt"></i></a> ';
                        return buttons;
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    searchable: false,
                    orderable: false
                }
            ],
            initComplete: function(settings, json) {
            }
        });

        // Editar categoría de producto
        $('#catTable tbody').on('click', 'a[rel="edit"]', function () {
            modal_title = $('.modal-title');
            modal_title.find('span').html('Editar categoría de producto');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblCategoriaProducto.cell($(this).closest('td, li')).index();
            var data = tblCategoriaProducto.row(tr.row).data();
            $('#act_cat').val('frmEditarCategoriaProductojsn');
            $('input[name="id"]').val(data.id);
            $('input[name="product_cat"]').val(data.product_cat);
            $('#myModalCategory').modal('show');
        });
        
        // Eliminar categoría de producto
        $('#catTable tbody').on('click', 'a[rel="delete"]', function () {
            var tr = tblCategoriaProducto.cell($(this).closest('td, li')).index();
            var data = tblCategoriaProducto.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'frmEliminarCategoriaProductojsn');
            parameters.append('id', data.id);
            fncModificarEstadoRelacion(window.location.pathname, parameters, function () {
                tblCategoriaProducto.ajax.reload();
                tblSubcategoriaProducto.ajax.reload();
            });
        });
    },

    // Tabla subcategoría de producto
    fncSubcategoriaProductotbl: function () {
        tblSubcategoriaProducto = $('#subcatTable').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: false,
            info: false,
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
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action':'tblSubcategoriaProductojsn'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                { "data": "n"},
                { "data": "product_subcat"},
                { "data": "product_cat.product_cat"},
                { "data": "state.name"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3],
                    class: 'text-center',
                    orderable: false,
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat" title="Editar subcategoría"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo-alt"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });
        
        // Editar subcategoría de producto
        $('#subcatTable tbody').on('click', 'a[rel="edit"]', function () {
            modal_title = $('#modalLabelSubc');
            modal_title.find('span').html('Editar subcategoría de producto');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblSubcategoriaProducto.cell($(this).closest('td, li')).index();
            var data = tblSubcategoriaProducto.row(tr.row).data();
            $('#act_subc').val('frmEditarSubcategoriaProductojsn');
            $('input[name="id"]').val(data.id);
            $('input[name="product_subcat"]').val(data.product_subcat);
            $('select[name="product_cat"]').val(data.product_cat.id).trigger("change");
            $('#myModalSubcategory').modal('show');
        });

        // Eliminar subcategoría de producto
        $('#subcatTable tbody').on('click', 'a[rel="delete"]', function () {
            var tr = tblSubcategoriaProducto.cell($(this).closest('td, li')).index();
            var data = tblSubcategoriaProducto.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'frmEliminarSubcategoriaProductojsn');
            parameters.append('id', data.id);
            fncModificarEstadoItem(window.location.pathname, parameters, function () {
                tblSubcategoriaProducto.ajax.reload();
            });
        });
    },

    // Tabla unidad de compra producto
    fncUnidadesCompratbl: function () {
        tblUnidadesCompra = $('#udcTable').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: false,
            info: false,
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
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action':'tblUnidadComprajsn'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                { "data": "n"},
                { "data": "purchase_unit"},
                { "data": "state.name"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3],
                    class: 'text-center',
                    orderable: false,
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat" title="Editar unidad compra"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo-alt"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });
        
        // Editar unidad de compra producto
        $('#udcTable tbody').on('click', 'a[rel="edit"]', function () {
            modal_title = $('#modalLabelUdc');
            modal_title.find('span').html('Editar unidad de compra');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblUnidadesCompra.cell($(this).closest('td, li')).index();
            var data = tblUnidadesCompra.row(tr.row).data();
            $('#act_udc').val('frmEditarUnidadComprajsn');
            $('input[name="id"]').val(data.id);
            $('input[name="purchase_unit"]').val(data.purchase_unit);
            $('#myModalUdc').modal('show');
        });

        // Eliminar unidad de compra producto
        $('#udcTable tbody').on('click', 'a[rel="delete"]', function () {
            var tr = tblUnidadesCompra.cell($(this).closest('td, li')).index();
            var data = tblUnidadesCompra.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'frmEliminarUnidadComprajsn');
            parameters.append('id', data.id);
            fncModificarEstadoItem(window.location.pathname, parameters, function () {
                tblUnidadesCompra.ajax.reload();
            });
        });
    },

    // Tabla unidad de venta producto
    fncUnidadesVentatbl: function () {
        tblUnidadesVenta = $('#udvTable').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: false,
            info: false,
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
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action':'tblUnidadVentajsn'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                { "data": "n"},
                { "data": "sales_unit"},
                { "data": "state.name"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3],
                    class: 'text-center',
                    orderable: false,
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat" title="Editar unidad venta"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo-alt"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });
        
        // Editar unidad de venta producto
        $('#udvTable tbody').on('click', 'a[rel="edit"]', function () {
            modal_title = $('#modalLabelUdv');
            modal_title.find('span').html('Editar unidad de venta');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblUnidadesVenta.cell($(this).closest('td, li')).index();
            var data = tblUnidadesVenta.row(tr.row).data();
            $('#act_udv').val('frmEditarUnidadVentajsn');
            $('input[name="id"]').val(data.id);
            $('input[name="sales_unit"]').val(data.sales_unit);
            $('#myModalUdv').modal('show');
        });

        // Eliminar unidad de venta producto
        $('#udvTable tbody').on('click', 'a[rel="delete"]', function () {
            var tr = tblUnidadesVenta.cell($(this).closest('td, li')).index();
            var data = tblUnidadesVenta.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'frmEliminarUnidadVentajsn');
            parameters.append('id', data.id);
            fncModificarEstadoItem(window.location.pathname, parameters, function () {
                tblUnidadesVenta.ajax.reload();
            });
        });
    },

    // Input categorías de producto
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
                        action: 'slcCategoriaProductojsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Ingrese una categoría',
        });
    }
}

$(function () {

    // Cargar subtablas de producto
    dctOpcionesCatalogoProductos.fncCategoriaProductotbl();
    dctOpcionesCatalogoProductos.fncSubcategoriaProductotbl();
    dctOpcionesCatalogoProductos.fncUnidadesCompratbl();
    dctOpcionesCatalogoProductos.fncUnidadesVentatbl();

    // Cargar libreria Select2 para input de tipo select
    fncCargarLibreriaSelect2('');

    // Abrir modal creación categoría producto
    $('.btnAddCat').on('click', function () {
        modal_title = $('.modal-title');
        modal_title.find('span').html('Crear categoría de producto');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('#act_cat').val('frmCrearCategoriaProductojsn');
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
        parameters.append('action', $('#act_cat').val());
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                $('#myModalCategory').modal('hide');
                tblCategoriaProducto.ajax.reload();
            });
    });


    // Abrir modal creación subcategoría producto
    $('.btnAddSubcat').on('click', function () {
        modal_title = $('.modal-title');
        modal_title.find('span').html('Crear subcategoría de producto');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('#act_subc').val('frmCrearSubcategoriaProductojsn');
        dctOpcionesCatalogoProductos.fncCategoriaProductoslc();
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
        parameters.append('action', $('#act_subc').val());
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                $('#myModalSubcategory').modal('hide');
                tblSubcategoriaProducto.ajax.reload();
            });
    });

    // Abrir modal creación unidad de medida en compra
    $('.btnAddUdc').on('click', function () {
        modal_title = $('#modalLabelUdc');
        modal_title.find('span').html('Crear unidad de compra');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('#act_udc').val('frmCrearUnidadComprajsn');
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
        parameters.append('action', $('#act_udc').val());
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Está seguro de guardar el registro?', parameters, function (response) {
                $('#myModalUdc').modal('hide');
                tblUnidadesCompra.ajax.reload();
            });
    });

    // Abrir modal creación unidad de medida en venta
    $('.btnAddUdv').on('click', function () {
        modal_title = $('#modalLabelUdv');
        modal_title.find('span').html('Crear unidad de venta');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('#act_udv').val('frmCrearUnidadVentajsn');
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
        parameters.append('action', $('#act_udv').val());
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Está seguro de guardar el registro?', parameters, function (response) {
                $('#myModalUdv').modal('hide');
                tblUnidadesVenta.ajax.reload();
            });
    });

    // Exportar catálogo de productos
    $('#exportCat').on('click', function () {
        $.ajax({
            url: window.location.pathname,
            data: {
                'action':'btnExportarCatalogojsn',
            },
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    location.href = '/configuracion/export_products/';
                }
                else if (request.hasOwnProperty('error')){
                    fncMensajeErrormns(request.error);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    });

});