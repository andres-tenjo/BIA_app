dctOpcionesCatalogoProveedores = {
    
    dctVariables: {
        tblProducts: '',
        dctProducto: '',
        strProveedorId: '',
        lstCantidadProductoCondicion: [],
        lstDescuentoProductoCondicion: [],
    },

    // Tabla cantidades mínimas
    fncCantidadesMinimastbl: function () {
        tblCantidadesMinimas = $('#tblCantidadMinimas').DataTable({
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
                    'action':'tblCantidadesMinimasjsn'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                { "data": "n"},
                { "data": "identification.supplier_name"},
                { "data": "product_code.product_desc"},
                { "data": "product_code.purchase_unit.purchase_unit"},
                { "data": "min_amount"},
                { "data": "state.name"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat" title="Editar"><i class="fas fa-edit"></i></a> ';
                        return buttons;
                    }
                }
            ],
            initComplete: function(settings, json) {
            }
        });
        
        // Editar cantidad mínima de proveedor
        $('#tblCantidadMinimas tbody').on('click', 'a[rel="edit"]', function (e) {
            e.preventDefault();
            var tr = tblCantidadesMinimas.cell($(this).closest('td, li')).index();
            var data_row = tblCantidadesMinimas.row(tr.row).data();
            $('#id_cantidad').val(data_row.id);
            $('#proveedor_cantidad').val(data_row.identification.supplier_name);
            $('#producto_cantidad').val(data_row.product_code.product_desc);
            $('#unidad_compra_cantidad').val(data_row.product_code.purchase_unit.purchase_unit);
            $('#editar_cantidad_minima').val(data_row.min_amount);
            $('#estado_cantidad').val(data_row.state.id);
            $('#myModalEditarCantidades').modal('show');
        });
    },

    // Tabla subcategoría de producto
    fncCondicionDescuentotbl: function () {
        tblDescuentos = $('#tblDescuentos').DataTable({
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
                    'action':'tblCondicionDescuentojsn'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                { "data": "n"},
                { "data": "identification.supplier_name"},
                { "data": "product_code.product_desc"},
                { "data": "product_code.purchase_unit.purchase_unit"},
                { "data": "product_code.cost_pu"},
                { "data": "min_amount"},
                { "data": "discount"},
                { "data": "state.name"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-3, -4, -5],
                    class: 'text-center',
                    orderable: false,
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat" title="Editar"><i class="fas fa-edit"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });
        
        // Editar cantidad mínima de proveedor
        $('#tblDescuentos tbody').on('click', 'a[rel="edit"]', function (e) {
            e.preventDefault();
            var tr = tblDescuentos.cell($(this).closest('td, li')).index();
            var data_row = tblDescuentos.row(tr.row).data();
            $('#id_descuentos').val(data_row.id);
            $('#proveedor_descuentos').val(data_row.identification.supplier_name);
            $('#producto_descuentos').val(data_row.product_code.product_desc);
            $('#unidad_compra_descuento').val(data_row.product_code.purchase_unit.purchase_unit);
            $('#precio_compra_descuento').val(data_row.product_code.cost_pu);
            $('#editar_cantidad_descuento').val(data_row.min_amount);
            $('#editar_descuento_producto').val(data_row.discount);
            $('#estado_descuento').val(data_row.state.id);
            $('#myModalEditarDescuentos').modal('show');
        });
    },

    // Obtener ids de productos de una ista
    fncObtenerIdslst: function (lst_name) {
        var ids = [];
        $.each(lst_name, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },

    // Agregar un nuevo item a una lista
    fncNuevoElementoLista: function (item, lst_name) {
        lst_name.push(item);
    },

    // Tabla de productos agregados condición cantidades mínimas por producto
    fncCantidadProductotbl: function () {
        tblCantidadesProductos = $('#tblCantidadesProductos').DataTable({
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
            data: this.dctVariables.lstCantidadProductoCondicion,
            columns: [
                { "data": "product_desc"},
                { "data": "purchase_unit.purchase_unit"},
                { "data": "cantidad"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Eliminar producto"><i class="fas fa-trash"></i></i></a> ';
                        return buttons;
                    }
                }
            ],
            initComplete: function(settings, json) {
            }
        });
        
        // Eliminar producto
        $('#tblCantidadesProductos tbody').on('click', 'a[rel="delete"]', function () {
            var tr = tblCantidadesProductos.cell($(this).closest('td, li')).index();
            fncMensajeAlertamns('Notificación', '¿Está seguro de eliminar el producto?', function () {
                dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion.splice(tr.row, 1);
                $('#tblCantidadesProductos').DataTable().clear().rows.add(dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion).draw();
                $('#buscar_producto').select2('open');
            });
        });
    },

    // Tabla de productos agregados condición descuentos por producto
    fncDescuentoProductotbl: function () {
        tblDescuentosProductos = $('#tblDescuentosProductos').DataTable({
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
            data: this.dctVariables.lstDescuentoProductoCondicion,
            columns: [
                { "data": "product_desc"},
                { "data": "purchase_unit.purchase_unit"},
                { "data": "cost_pu"},
                { "data": "cantidad"},
                { "data": "descuento"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Eliminar producto"><i class="fas fa-trash"></i></i></a> ';
                        return buttons;
                    }
                },
                {
                    targets: [-2, -3],
                    class: 'text-center',
                    orderable: false,
                },
            ],
            initComplete: function(settings, json) {
            }
        });

        // Eliminar producto
        $('#tblDescuentosProductos tbody').on('click', 'a[rel="delete"]', function () {
            var tr = tblDescuentosProductos.cell($(this).closest('td, li')).index();
            fncMensajeAlertamns('Notificación', '¿Está seguro de eliminar el producto?', function () {
                dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion.splice(tr.row, 1);
                $('#tblDescuentosProductos').DataTable().clear().rows.add(dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion).draw();
                $('#buscar_producto_descuento').select2('open');
            });
        });
    },
}

$(function () {

    // Cargar subtablas de producto
    dctOpcionesCatalogoProveedores.fncCantidadesMinimastbl();
    dctOpcionesCatalogoProveedores.fncCondicionDescuentotbl();
    dctOpcionesCatalogoProveedores.fncCantidadProductotbl();
    dctOpcionesCatalogoProveedores.fncDescuentoProductotbl();

    // Función para cargar libreria TouchSpin para los input tipo número, decimal y moneda
    fncCargarLibreriaTouchSpinFormatoEntero();
    fncCargarLibreriaTouchSpinFormatoDecimal();

    // Buscar proveedor formulario cantidades mínimas
    $('.buscar_proveedor').select2({
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
                    action: 'slcBuscarProveedorjsn',
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el proveedor, identificación o nombre de contacto',
        minimumInputLength: 1,
        templateResult: fncBuscarProveedorRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        dctOpcionesCatalogoProveedores.dctVariables.strProveedorId = data.id;
    });
    
    // Buscar producto formulario cantidades
    $('#buscar_producto').select2({
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
    }).on('select2:select', function (e) {
        var data = e.params.data;
        id_prod = data.id;
        products = dctOpcionesCatalogoProveedores.fncObtenerIdslst(dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion);
        if (products.length > 0){
            $.each(products, function (pos, value) {
                if(id_prod == value){
                    $.confirm({
                        title: 'Alerta',
                        content: '¿El producto ya se registro, desea modificarlo?',
                        buttons: {
                            Si: function () {
                                dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion.splice(pos, 1);
                                dctOpcionesCatalogoProveedores.dctVariables.dctProducto = data;
                                $('#productDesc').val(data.product_desc);
                                $('#unidadCompra').val(data.purchase_unit.purchase_unit);
                                $('#buscar_producto').val('').trigger('change.select2');
                                $('#quantityMin').focus();
                                dctOpcionesCatalogoProveedores.fncCantidadProductotbl();
                            },
                            No: function () {
                                $('#buscar_producto').val('').trigger('change.select2');
                                $('#buscar_producto').select2('open');
                            }
                        }
                    });
                } else if(id_prod != value){
                    dctOpcionesCatalogoProveedores.dctVariables.dctProducto = data;
                    $('#productDesc').val(data.product_desc);
                    $('#unidadCompra').val(data.purchase_unit.purchase_unit);
                    $('#product').val('').trigger('change.select2');
                    $('#quantityMin').focus();
                }
            });
        }
        else if (products.length == 0){
            dctOpcionesCatalogoProveedores.dctVariables.dctProducto = data;
            $('#productDesc').val(data.product_desc);
            $('#unidadCompra').val(data.purchase_unit.purchase_unit);
            $('#product').val('').trigger('change.select2');
            $('#quantityMin').focus();
        }
    });
    
    // Buscar producto formulario cantidades
    $('#buscar_producto_descuento').select2({
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
    }).on('select2:select', function (e) {
        var data = e.params.data;
        id_prod = data.id;
        products = dctOpcionesCatalogoProveedores.fncObtenerIdslst(dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion);
        if (products.length > 0){
            $.each(products, function (pos, value) {
                if(id_prod == value){
                    $.confirm({
                        title: 'Alerta',
                        content: '¿El producto ya se registro, desea modificarlo?',
                        buttons: {
                            Si: function () {
                                dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion.splice(pos, 1);
                                dctOpcionesCatalogoProveedores.dctVariables.dctProducto = data;
                                $('#productDescription').val(data.product_desc);
                                $('#unidadCompraDescuento').val(data.purchase_unit.purchase_unit);
                                $('#precioCompra').val(data.cost_pu);
                                $('#buscar_producto_descuento').val('').trigger('change.select2');
                                $('#cantidadMinima').focus();
                                dctOpcionesCatalogoProveedores.fncDescuentoProductotbl();
                            },
                            No: function () {
                                $('#buscar_producto_descuento').val('').trigger('change.select2');
                                $('#buscar_producto_descuento').select2('open');
                            }
                        }
                    });
                } else if(id_prod != value){
                    dctOpcionesCatalogoProveedores.dctVariables.dctProducto = data;
                    $('#productDescription').val(data.product_desc);
                    $('#unidadCompraDescuento').val(data.purchase_unit.purchase_unit);
                    $('#precioCompra').val(data.cost_pu);
                    $('#buscar_producto_descuento').val('').trigger('change.select2');
                    $('#cantidadMinima').focus();
                }
            });
        }
        else if (products.length == 0){
            dctOpcionesCatalogoProveedores.dctVariables.dctProducto = data;
            $('#productDescription').val(data.product_desc);
            $('#unidadCompraDescuento').val(data.purchase_unit.purchase_unit);
            $('#precioCompra').val(data.cost_pu);
            $('#buscar_producto_descuento').val('').trigger('change.select2');
            $('#cantidadMinima').focus();
        }
    });

    // Abrir modal creación condición cantidad de compra por producto
    $('.btnAgregarCantidad').on('click', function () {
        $('#tblCantidadesProductos').DataTable().clear().rows.add(dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion).draw();
        $('#quantityMin').val(1);
        $('#action_cantidad').val('btnGuardarCondicionCantidadMinimajsn');
        $('#myModalCantidades').modal('show');
    });

    // Focus formulario cantidades mínimas
    $('#myModalCantidades').on('shown.bs.modal', function (e) {
        $('#buscar_proveedor').val('').trigger("change");
        $('#buscar_proveedor').select2('open');
    });

    // Borrar lo digitado en el formulario cantidades mínimas
    $('#myModalCantidades').on('hidden.bs.modal', function (e) {
        dctOpcionesCatalogoProveedores.dctVariables.strProveedorId = '';
        dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion = [];
        $('#frmCantidades').trigger('reset');
    });

    // Función para agregar productos a la tabla cantidades mínimas
    $('#agregarProductoTblCantidades').on('click', function () {
        if (dctOpcionesCatalogoProveedores.dctVariables.dctProducto == ''){
            fncMensajeInformacionmns('Ingrese un producto');
            $('#buscar_producto').select2('open');
            return false;
        }else if (dctOpcionesCatalogoProveedores.dctVariables.dctProducto != ''){
            cantidad = $('#quantityMin').val();
            dctOpcionesCatalogoProveedores.dctVariables.dctProducto.cantidad = cantidad;
            $('#productDesc').val('');
            $('#unidadCompra').val('');
            $('#quantityMin').val(1);
            dctOpcionesCatalogoProveedores.fncNuevoElementoLista(
                dctOpcionesCatalogoProveedores.dctVariables.dctProducto, 
                dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion
                );
            $('#tblCantidadesProductos').DataTable().clear().rows.add(dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion).draw();
            $('#buscar_producto').select2('open');
            dctOpcionesCatalogoProveedores.dctProducto = '';
        }
    });
    
    // Boton eliminar productos de la tabla cantidades minimas
    $('#eliminarProductosTblCantidades').on('click', function () {
        if(dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion.length === 0) return false;
        fncMensajeAlertamns('Notificación', '¿Está seguro de eliminar todos los productos?', function () {
            dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion = [];
            $('#tblCantidadesProductos').DataTable().clear().rows.add(dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion).draw();
            $('#product').select2('open');
        });
    });

    // Guardar el registro de formulario cantidades mínimas
    $('#frmCantidades').on('submit', function (e) {
        e.preventDefault();
        if(dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion.length === 0 ){
            fncMensajeErrormns('Debe agregar al menos un producto')
            return false;
        }
        else if(dctOpcionesCatalogoProveedores.dctVariables.strProveedorId == ''){
            fncMensajeErrormns('Seleccione un proveedor')
            return false;
        }
        else{
            var parameters = new FormData();
            parameters.append('action', $('#action_cantidad').val());
            parameters.append('proveedor', dctOpcionesCatalogoProveedores.dctVariables.strProveedorId);
            parameters.append('items', JSON.stringify(dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion));
            fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
                '¿Estas seguro de guardar el registro?', parameters, function (response) {
                    dctOpcionesCatalogoProveedores.dctVariables.strProveedorId == '';
                    dctOpcionesCatalogoProveedores.dctVariables.lstCantidadProductoCondicion = [];
                    tblCantidadesMinimas.ajax.reload();
                    $('#myModalCantidades').modal('hide');
                });
        }
    });

    // Guardar la edición de un producto con cantidades mínimas
    $('#frmEditarCantidades').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', $('#action_editar_cantidad').val());
        parameters.append('id', $('#id_cantidad').val());
        parameters.append('cantidad', parseInt($('#editar_cantidad_minima').val()));
        parameters.append('estado', $('#estado_cantidad').val());
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                $('#myModalEditarCantidades').modal('hide');
                tblCantidadesMinimas.ajax.reload();
        });
    });

    // Abrir modal descuento por producto
    $('.btnAgregarDescuento').on('click', function () {
        $('#tblDescuentosProductos').DataTable().clear().rows.add(dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion).draw();
        $('#cantidadMinima').val(1);
        $('#discountInput').val(0.00);
        $('#action_descuento').val('frmGuardarCondicionDescuentojsn');
        $('#myModalDescuentos').modal('show');
    });

    // Focus formulario categoría
    $('#myModalDescuentos').on('shown.bs.modal', function (e) {
        $('#buscar_proveedor_descuento').val('').trigger("change");
        $('#buscar_proveedor_descuento').select2('open');
    });

    // Borrar lo digitado en el formulario categoría
    $('#myModalDescuentos').on('hidden.bs.modal', function (e) {
        dctOpcionesCatalogoProveedores.dctVariables.strProveedorId = '';
        dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion = [];
        $('#frmDescuentos').trigger('reset');
    });

    // Función para agregar productos a la tabla cantidades
    $('#agregarProductoTblDescuentos').on('click', function () {
        if (dctOpcionesCatalogoProveedores.dctVariables.dctProducto == ''){
            fncMensajeInformacionmns('Ingrese un producto');
            $('#buscar_producto_descuento').select2('open');
            return false;
        }else if (dctOpcionesCatalogoProveedores.dctVariables.dctProducto != ''){
            cantidad = $('#cantidadMinima').val();
            descuento = $('#discountInput').val();
            dctOpcionesCatalogoProveedores.dctVariables.dctProducto.cantidad = cantidad;
            dctOpcionesCatalogoProveedores.dctVariables.dctProducto.descuento = descuento;
            $('#productDescription').val('');
            $('#unidadCompraDescuento').val('');
            $('#precioCompra').val('');
            $('#cantidadMinima').val(1);
            $('#discountInput').val(0.00);
            dctOpcionesCatalogoProveedores.fncNuevoElementoLista(
                dctOpcionesCatalogoProveedores.dctVariables.dctProducto, 
                dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion
                );
            $('#tblDescuentosProductos').DataTable().clear().rows.add(dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion).draw();
            $('#buscar_producto_descuento').select2('open');
            dctOpcionesCatalogoProveedores.dctVariables.dctProducto = '';
        }
    });
    
    // Boton eliminar productos de la tabla
    $('#eliminarProductosTblDescuentos').on('click', function () {
        if(dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion.length === 0) return false;
        fncMensajeAlertamns('Notificación', '¿Está seguro de eliminar todos los productos?', function () {
            dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion = [];
            $('#tblDescuentosProductos').DataTable().clear().rows.add(dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion).draw();
            $('#buscar_producto_descuento').select2('open');
        });
    });

    // Guardar el registro de categoría de producto
    $('#frmDescuentos').on('submit', function (e) {
        e.preventDefault();
        if(dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion.length === 0 ){
            fncMensajeErrormns('Debe agregar al menos un producto')
            return false;
        }
        else if(dctOpcionesCatalogoProveedores.dctVariables.strProveedorId == ''){
            fncMensajeErrormns('Seleccione un proveedor')
            return false;
        }
        else{
            var parameters = new FormData();
            parameters.append('action', $('#action_descuento').val());
            parameters.append('proveedor', dctOpcionesCatalogoProveedores.dctVariables.strProveedorId);
            parameters.append('items', JSON.stringify(dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion));
            fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
                '¿Estas seguro de guardar el registro?', parameters, function (response) {
                    $('#myModalDescuentos').modal('hide');
                    dctOpcionesCatalogoProveedores.dctVariables.strProveedorId == '';
                    dctOpcionesCatalogoProveedores.dctVariables.lstDescuentoProductoCondicion = [];
                    tblDescuentos.ajax.reload();
                });
        }
    });

    // Guardar el registro de categoría de producto
    $('#frmEditarDescuentos').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', $('#action_editar_descuentos').val());
        parameters.append('id', $('#id_descuentos').val());
        parameters.append('cantidad', parseInt($('#editar_cantidad_descuento').val()));
        parameters.append('descuento', parseFloat($('#editar_descuento_producto').val()));
        parameters.append('estado', $('#estado_descuento').val());
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                $('#myModalEditarDescuentos').modal('hide');
                tblDescuentos.ajax.reload();
        });
    });
});
// para push