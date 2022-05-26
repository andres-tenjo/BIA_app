$(function () {

    tblPedidos = $('#data').DataTable({
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
                'action':'tblPedidojsn'
            },
            dataSrc: "",
            headers: {
                'X-CSRFToken': csrftoken
            },
        },
        columns: [
            {"data": "doc_number"},
            {"data": "creation_date"},
            {"data": "business_name"},
            {"data": "subtotal"},
            {"data": "iva"},
            {"data": "discount"},
            {"data": "total"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [1, 2, 3],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            },
            {
                targets: [-2, -3, -4, -5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="details" class="btn btn-info btn-xs btn-flat" title="Detalle pedido"><i class="fas fa-search"></i></a> ';
                    buttons += '<a href="/comercial/exportar_pedido_pdf/'+row.id+'/" target="_blank" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-file-pdf" title="Exportar pdf"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            var tr = tblPedidos.cell($(this).closest('td, li')).index();
            var data = tblPedidos.row(tr.row).data();
            $('#iptDocumentoPedido').val(data.doc_number);
            $('#iptNombreCliente').val(data.business_name);
            $('#iptIdentificacionCliente').val(data.identification);
            $('#iptCiudadCliente').val(data.city);
            $('#iptZonaCliente').val(data.customer_zone);
            $('#iptDireccionCliente').val(data.delivery_address);
            $('#iptBodega').val(data.store);
            $('#iptFechaEntrega').val(data.delivery_date);
            $('#iptCondicionPedido').val(data.condition.name);
            $('#iptSubtotal').val(data.subtotal);
            $('#iptIva').val(data.iva);
            $('#iptDescuento').val(data.discount);
            $('#iptTotal').val(data.total);
            $('#tblDetallePedido').DataTable({
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
                        'action':'tblDetallePedidojsn',
                        'id': data.id
                    },
                    dataSrc: "",
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                },
                columns: [
                    {"data": "product_code"},
                    {"data": "product_desc"},
                    {"data": "quantity"},
                    {"data": "unit_price"},
                    {"data": "subtotal"},
                    {"data": "iva"},
                    {"data": "total"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -2, -3, -4],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [1, 2, 3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#mdlDetallePedido').modal('show');
        });
});