var dctOpcionesCatalogoClientes = {
    dctVariables: {
        lstCategoriaProductoMargen: [],
    },

    // Tabla categoría de cliente
    fncCategoriaClientetbl: function () {
        tblCategoriaCliente = $('#catTable').DataTable({
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
                    'action':'tblCategoriaClientejsn'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                { "data": "n"},
                { "data": "customer_cat"},
                { "data": "state.name"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo-alt"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });

        // Editar categorías de cliente
        $('#catTable tbody').on('click', 'a[rel="edit"]', function (e) {
            e.preventDefault();
            var tr = tblCategoriaCliente.cell($(this).closest('td, li')).index();
            var data_row = tblCategoriaCliente.row(tr.row).data();
            $('#act_cat').val('frmEditarCategoriaClientejsn');
            $('input[name="id"]').val(data_row.id);
            $('#cat_cust').val(data_row.customer_cat);
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action':'btnEditarMargenCategoriaClientejsn',
                    'id': data_row.id
                },
                dataType: 'json',
            }).done(function(data) {
                dctOpcionesCatalogoClientes.dctVariables.lstCategoriaProductoMargen.push(data);
                dctOpcionesCatalogoClientes.fncMargenCategoriatbl();
                modal_title = $('.modal-title');
                modal_title.find('span').html('Editar categoría de cliente');
                modal_title.find('i').removeClass().addClass('fas fa-edit');    
                $('#myModalCategory').modal('show');
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus +': '+errorThrown);
            }).always(function(data) {                
            }); 
        });

        // Eliminar categorías de cliente
        $('#catTable tbody').on('click', 'a[rel="delete"]', function () {
            var tr = tblCategoriaCliente.cell($(this).closest('td, li')).index();
            var data = tblCategoriaCliente.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'btnEliminarCategoriaClientejsn');
            parameters.append('id', data.id);
            delete_action(window.location.pathname, parameters, function () {
                tblCategoriaCliente.ajax.reload();
            });
        });
    },

    // Tabla margén categoría
    fncMargenCategoriatbl: function () {
        tblMargenCategoria = $('#tblMargin').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            dom: 'Bfrtip',
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
            data: this.dctVariables.lstCategoriaProductoMargen[0],
            columns: [
                { "data": "product_cat"},
                { "data": "margin_max"},
                { "data": "margin_min"}
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input name="margin_min" type="number" min="0" value="' + data + '"step=".01" required="true"></input>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input name="margin_max" type="number" min="0" value="' + data + '"step=".01" required="true"></input>';
                    }
                }
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="margin_max"]').TouchSpin({
                    min: 0,
                    max: 100,
                    step: 0.01,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 1,
                    postfix: '%'
                });
                $(row).find('input[name="margin_min"]').TouchSpin({
                    min: 0,
                    max: 100,
                    step: 0.01,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 1,
                    postfix: '%'
                });
            },
            initComplete: function(settings, json) {
            }
        });

        // Grabar margén por fila
        $('#tblMargin tbody')
            .on('change', 'input[name="margin_min"]', function () {
                var margin_min = parseFloat($(this).val());
                var tr = tblMargenCategoria.cell($(this).closest('td, li')).index();
                dctOpcionesCatalogoClientes.dctVariables.lstCategoriaProductoMargen[0][tr.row].margin_min = margin_min;
            })
            .on('change', 'input[name="margin_max"]', function () {
                var margin_max = parseFloat($(this).val());
                var tr = tblMargenCategoria.cell($(this).closest('td, li')).index();
                dctOpcionesCatalogoClientes.dctVariables.lstCategoriaProductoMargen[0][tr.row].margin_max = margin_max;
        });
    },

    // Tabla zona cliente
    fncZonaClientetbl: function () {
        tblZonaCliente = $('#zoneTable').DataTable({
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
                    'action':'tblZonaClientejsn'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                { "data": "n"},
                { "data": "customer_zone"},
                { "data": "state.name"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo-alt"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });
        
        // Editar zona cliente
        $('#zoneTable tbody').on('click', 'a[rel="edit"]', function () {
            modal_title = $('.modal-title');
            modal_title.find('span').html('Editar zona de cliente');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblZonaCliente.cell($(this).closest('td, li')).index();
            var data = tblZonaCliente.row(tr.row).data();
            $('#act_zone').val('frmEditarZonaClientejsn');
            $('input[name="id"]').val(data.id);
            $('input[name="customer_zone"]').val(data.customer_zone);
            $('#myModalZone').modal('show');    
        });

        // Eliminar zona cliente
        $('#zoneTable tbody').on('click', 'a[rel="delete"]', function () {
            var tr = tblZonaCliente.cell($(this).closest('td, li')).index();
            var data = tblZonaCliente.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'btnEliminarZonaCliente');
            parameters.append('id', data.id);
            delete_action(window.location.pathname, parameters, function () {
                tblZonaCliente.ajax.reload();
            });
        });
    },

    // Tabla asesor comercial
    fncAsesorComercialtbl: function () {
        tblAsesorComercial = $('#advisorTable').DataTable({
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
                    'action':'slcBuscarAsesorComercialjsn'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                { "data": "n"},
                { "data": "advisor"},
                { "data": "state.name"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo-alt"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });

        // Editar asesor comercial
        $('#advisorTable tbody').on('click', 'a[rel="edit"]', function () {
            modal_title = $('.modal-title');
            modal_title.find('span').html('Editar asesor comercial');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblAsesorComercial.cell($(this).closest('td, li')).index();
            var data = tblAsesorComercial.row(tr.row).data();
            console.log(data);
            $('#act_advisor').val('frmEditarAsesorComercialjsn');
            $('input[name="id"]').val(data.id);
            $('#advisor').val(data.advisor);
            $('select[name="user"]').val(data.user).trigger('change');
            $('select[name="zone"]').val(data.zone).trigger('change');
            $('#myModalAdvisor').modal('show');    
        });

        // Eliminar asesor comercial
        $('#advisorTable tbody').on('click', 'a[rel="delete"]', function () {
            var tr = tblAsesorComercial.cell($(this).closest('td, li')).index();
            var data = tblAsesorComercial.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'btnEliminarAsesorComercialjsn');
            parameters.append('id', data.id);
            delete_action(window.location.pathname, parameters, function () {
                tblAsesorComercial.ajax.reload();
            });
        });
    },

    // Input zona asesor
    fncBuscarZonaslc: function () {
        $('select[name="zone"]').select2({
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
                        action: 'slcBuscarZonaActivajsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione una zona',
        });  
    },

    // Input asesor cliente
    fncBuscarAsesorslc: function () {
        $('select[name="commercial_advisor"]').select2({
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
                        action: 'slcBuscarAsesorComercialjsn'
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

$(function () {

    dctOpcionesCatalogoClientes.fncCategoriaClientetbl();
    dctOpcionesCatalogoClientes.fncZonaClientetbl();
    dctOpcionesCatalogoClientes.fncAsesorComercialtbl();

    // Función para cargar libreria Select2 para los input tipo select
    fncCargarLibreriaSelect2('Seleccione o cree una nueva');

    // Cargar datetimepicker
    fncCargarLibreriaDateTimePicker();
    
    // Abrir collapse de categoria
    $('#collapseCategory').on('shown.bs.collapse', function () {
        tblCategoriaCliente.ajax.reload();
    });

    // Abrir modal creación categoría cliente
    $('.btnAddCat').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                'action':'tblMargenCategoriaProducto'
            },
            dataType: 'json',
        }).done(function(data) {
            if(data.hasOwnProperty('error')){
                error = data.error;
                $.confirm({
                    columnClass: 'col-md-12',
                    title: 'Error en categoría',
                    icon: 'fa fa-warning',
                    content: error,
                    theme: 'supervan',
                    buttons: {
                        Aceptar: function () {
                            location.href = '/configuracion/opciones_producto/';
                        },
                        Cancelar: function () {
                                    
                        },
                    }
                });
            }
            else{
                $('input[name="cat_cust"]').prop('focus', true);
                dctOpcionesCatalogoClientes.dctVariables.lstCategoriaProductoMargen.push(data);
                dctOpcionesCatalogoClientes.fncMargenCategoriatbl();
                modal_title = $('.modal-title');
                modal_title.find('span').html('Crear categoría de cliente');
                modal_title.find('i').removeClass().addClass('fas fa-plus');
                $('#act_cat').val('frmCrearCategoriaClientejsn');
                $('#myModalCategory').modal('show');

            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus +': '+errorThrown);
        }).always(function(data) {                
        });        
    });

    // Focus formulario categoría
    $('#myModalCategory').on('shown.bs.modal', function (e) {
        $('#cat_cust').focus();
    });

    // Borrar lo digitado en el formulario categoría
    $('#myModalCategory').on('hidden.bs.modal', function (e) {
        $('#frmCatCust').trigger('reset');
        dctOpcionesCatalogoClientes.dctVariables.lstCategoriaProductoMargen = []
    })

    // Guardar el registro de categoría de cliente
    $('#frmCatCust').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', $('#act_cat').val());
        parameters.append('customer_cat', $('#cat_cust').val());
        parameters.append('margin_cat', JSON.stringify(dctOpcionesCatalogoClientes.dctVariables.lstCategoriaProductoMargen));
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                $('#myModalCategory').modal('hide');
                tblCategoriaCliente.ajax.reload();
                dctOpcionesCatalogoClientes.dctVariables.lstCategoriaProductoMargen = []
            });
    });

    // Abrir collapse de zona
    $('#collapseZone').on('shown.bs.collapse', function () {
        tblZonaCliente.ajax.reload();
    });

    // Abrir modal creación zona cliente
    $('.btnAddZone').on('click', function () {
        modal_title = $('.modal-title');
        modal_title.find('span').html('Crear zona de cliente');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('#act_zone').val('frmCrearZonaClientejsn');
        $('#myModalZone').modal('show');
    });

    // Focus formulario zona
    $('#myModalZone').on('shown.bs.modal', function (e) {
        $('#customer_zone').focus();
    });

    // Borrar lo digitado en el formulario zona
    $('#myModalZone').on('hidden.bs.modal', function (e) {
        $('#frmCatZone').trigger('reset');
    })

    // Guardar el registro de zona de cliente
    $('#frmCatZone').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', $('#act_zone').val());
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                $('#myModalZone').modal('hide');
                dctOpcionesCatalogoClientes.fncBuscarZonaslc();
                tblZonaCliente.ajax.reload();
            });
    });
    
    // Abrir collapse de asesor
    $('#collapseAdvisor').on('shown.bs.collapse', function () {
        tblAsesorComercial.ajax.reload();
    });

    // Abrir modal creación asesor comercial
    $('.btnAddAdv').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                'action':'btnAbrirFormularioAsesorComercialjsn'
            },
            dataType: 'json',
        }).done(function(data) {
            if(data.hasOwnProperty('error_user')){
                $.confirm({
                    columnClass: 'col-md-12',
                    title: 'Error en asesor',
                    icon: 'fa fa-warning',
                    content: data.error_user,
                    theme: 'supervan',
                    buttons: {
                        Aceptar: function () {
                            location.href = '/usuarios/crear_usuarios';
                        },
                        Cancelar: function () {
                                    
                        },
                    }
                });
            }
            else if(data.hasOwnProperty('error_zone')){   
                $.confirm({
                    columnClass: 'col-md-12',
                    title: 'Error en asesor',
                    icon: 'fa fa-warning',
                    content: data.error_zone,
                    theme: 'supervan',
                    buttons: {
                        Aceptar: function () {
                            modal_title = $('.modal-title');
                            modal_title.find('span').html('Crear zona de cliente');
                            modal_title.find('i').removeClass().addClass('fas fa-plus');
                            $('#act_zone').val('frmCrearZonaClientejsn');
                            $('#myModalZone').modal('show');                    
                        },
                        Cancelar: function () {
                                    
                        },
                    }
                });
            }
            else{
                modal_title = $('.modal-title');
                modal_title.find('span').html('Crear asesor comercial');
                modal_title.find('i').removeClass().addClass('fas fa-plus');
                $('#act_advisor').val('frmCrearAsesorComercialjsn');
                $('#myModalAdvisor').modal('show');
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus +': '+errorThrown);
        }).always(function(data) {                
        });        
    });

    // Focus formulario asesor
    $('#myModalAdvisor').on('shown.bs.modal', function (e) {
        $('#advisor').focus();
    });

    // Borrar lo digitado en el formulario asesor
    $('#myModalAdvisor').on('hidden.bs.modal', function (e) {
        $('#frmAdvisor').trigger('reset');
        $('select[name="user"]').val('').trigger('change');
        $('select[name="zone"]').val('').trigger('change');
    })

    // Guardar el registro de zona de cliente
    $('#frmAdvisor').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        //parameters.append('action', $('#act_advisor').val());
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                $('#myModalAdvisor').modal('hide');
                tblAsesorComercial.ajax.reload();
            });
    });

    // Exportar catálogo de productos
    $('#exportCat').on('click', function () {
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                'action':'btnExportarCatalogoClientes',
            },
            dataType: 'json',
        }).done(function(data) {
            if (!data.hasOwnProperty('msg')){
                location.href = '/configuracion/export_customers/';
            }
            else if (data.hasOwnProperty('msg')){
                message_error(data.msg);
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus +': '+errorThrown);
        }).always(function(data) {                
        });
    });

});