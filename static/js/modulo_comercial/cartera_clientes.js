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
            { "data": "customer.customer"},
            { "data": "credit_value"},
            { "data": "next_payment_value"},
            { "data": "next_payment_date"},
            { "data": "balance_credit_value"},
            { "data": "state.name"},
            { "data": "state"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                    return buttons;
                }
            },
            {
                targets: [-3, -4, -5, -6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
        ],
        initComplete: function(settings, json) {
        }
    });
    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            var tr = tblCust.cell($(this).closest('td, li')).index();
            var data = tblCust.row(tr.row).data();
            console.log(data)
            $('input[name="ord"]').val(data.order.id);
            $('input[name="value"]').val('$ ' + data.order.total);
            $('input[name="date"]').val(data.order.order_date);
            $('input[name="subt"]').val('$ ' + data.order.subtotal);
            $('input[name="iva"]').val('$ ' + data.order.iva);
            $('input[name="desc"]').val('$ ' + data.order.dcto);
            $('#myModalDet').modal('show');
    });
});