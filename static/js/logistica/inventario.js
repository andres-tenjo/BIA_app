var tblCust;

$(function () {
    tblCust = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
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
                'action':'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            { "data": "id"},
            { "data": "product.name"},
            { "data": "previous_balance"},
            { "data": "warehouse_entry.real_quantity"},
            { "data": "warehouse_exit.real_quantity"},
            { "data": "inventory_balance"},
            { "data": "inventory_count.real_quantity"},
            { "data": "difference"},
            { "data": "final_balance"},
            { "data": "indice_rotacion"},
        ],
        columnDefs: [
            {
                targets: [-1, -2, -3, -4, -5, -6, -7, -8],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            },
        ],
        initComplete: function(settings, json) {
        }
    });
});