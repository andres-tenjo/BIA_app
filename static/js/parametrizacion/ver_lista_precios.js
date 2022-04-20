$(function () {

    tblListaPrecios = $('#data').DataTable({
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
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action':'tblListaPreciosjsn'
            },
            dataSrc: "",
            headers: {
                'X-CSRFToken': csrftoken
            },
        },
        columns: [
            {"data": "id"},
            {"data": "doc_number"},
            {"data": "list_name"},
            {"data": "due_date"},
            {"data": "state.name"},
            {"data": "list_name"}
        ],
        columnDefs: [
            {
                targets: [-2, -3, -4, -5, -6],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="details" class="btn btn-info btn-xs btn-flat" title="Detalle lista"><i class="fas fa-search"></i></a> ';
                    buttons += '<a href="/configuracion/editar_lista_precios/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" title="Editar lista"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo"></i></a> ';
                    buttons += '<a href="/configuracion/exportar_lista_excel/'+row.id+'/" target="_blank" class="btn btn-success btn-xs btn-flat" title="Exportar excel"><i class="fas fa-file-excel"></i></a> ';
                    buttons += '<a href="/configuracion/exportar_lista_pdf/'+row.id+'/" target="_blank" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-file-pdf" title="Exportar pdf"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            var tr = tblListaPrecios.cell($(this).closest('td, li')).index();
            var data = tblListaPrecios.row(tr.row).data();
            $('#iptCodigoLista').val(data.doc_number);
            $('#iptNombreLista').val(data.list_name);
            $('#iptVigenciaLista').val(data.due_date);
            $('#tblListaPreciosDetalle').DataTable({
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
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action':'tblListaPreciosDetallejsn',
                        'id': data.id
                    },
                    dataSrc: "",
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                },
                columns: [
                    {"data": "product_code.id"},
                    {"data": "product_code.product_desc"},
                    {"data": "quantity"},
                    {"data": "lead_time"},
                    {"data": "unit_price"},
                    {"data": "observations"},
                ],
                columnDefs: [
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-1, -3, -4, -5, -6],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#mdlDetalleListaPrecios').modal('show');
        })
        .on('click', 'a[rel="delete"]', function (e) {
            e.preventDefault();
            var tr = tblListaPrecios.cell($(this).closest('td, li')).index();
            var data = tblListaPrecios.row(tr.row).data();
            console.log(data);
            var parameters = new FormData();
            parameters.append('action', 'frmCambiarEstadoListajsn');
            parameters.append('id', data.id);
            fncModificarEstadoItem(window.location.pathname, parameters, function (response) {
                tblListaPrecios.ajax.reload();
            });
        });
});