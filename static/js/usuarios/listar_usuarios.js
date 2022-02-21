var tblUsuarios;

$(function () {
    tblUsuarios = $('#data').DataTable({
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
                'action':'tblListarUsuariosjsn'
            },
            dataSrc: "",
            headers: {
                'X-CSRFToken': csrftoken
            },
        },
        columns: [
            { "data": "n"},
            { "data": "full_name"},
            { "data": "username"},
            { "data": "date_joined"},
            { "data": "email"},
            { "data": "image"},
            { "data": "is_active"},
            { "data": "id"},
        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + row.image + '" class="img-fluid mx-auto d-block" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/usuarios/editar_usuarios/' + row.id + '/" class="btn btn-success btn-xs btn-flat" title="Editar usuario"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar"><i class="fas fa-undo-alt"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings, json) {
        }
    });

    $('#data tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tblUsuarios.cell($(this).closest('td, li')).index();
        var data = tblUsuarios.row(tr.row).data();
        var parameters = new FormData();
        parameters.append('action', 'btnEliminarUsuariojsn');
        parameters.append('id', data.id);
        fncModificarEstadoItem(window.location.pathname, parameters, function () {
            tblUsuarios.ajax.reload();
        });
    });
});