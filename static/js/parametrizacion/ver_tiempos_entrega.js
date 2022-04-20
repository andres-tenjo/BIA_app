$(function () {

    tblTiemposEntrega = $('#data').DataTable({
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
                'action':'tblTiemposEntregajsn'
            },
            dataSrc: "",
            headers: {
                'X-CSRFToken': csrftoken
            },
        },
        columns: [
            {"data": "id"},
            {"data": "city.city_name"},
            {"data": "customer_zone.customer_zone"},
            {"data": "warehouse.warehouse_name"},
            {"data": "enlistment_time"},
            {"data": "travel_time"},
            {"data": "download_time"},
            {"data": "total_time"},
            {"data": "state.name"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2, -3, -4, -5, -6, -7, -8, -9, -10],
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
                    var buttons = '<a href="/configuracion/editar_tiempo_entrega/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" title="Editar tiempo"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="delete"]', function (e) {
            e.preventDefault();
            var tr = tblTiemposEntrega.cell($(this).closest('td, li')).index();
            var data = tblTiemposEntrega.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'frmCambiarEstadoTiempoEntregajsn');
            parameters.append('id', data.id);
            fncModificarEstadoItem(window.location.pathname, parameters, function (response) {
                tblTiemposEntrega.ajax.reload();
            });
        });
});