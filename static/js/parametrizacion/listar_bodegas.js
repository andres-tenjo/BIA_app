dctListarBodegas = {
    
    dctVariables: {
        lstBodegas: [],
    },

    fncCatalogoBodegastbl: function () {
        tblBodegas = $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            bLengthChange: false,
            bPaginate: false,
            bInfo: false,
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
            data: this.dctVariables.lstBodegas,
            columns: [
                { "data": "warehouse_name"},
                { "data": "department.department_name"},
                { "data": "city.city_name"},
                { "data": "warehouse_address"},
                { "data": "contact_name"},
                { "data": "state.name"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3, -4, -5, -6, -7],
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
                        var buttons = '<a href="/configuracion/editar_bodega/' + row.id + '/" class="btn btn-success btn-xs btn-flat" title="Editar bodega"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo-alt"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });
        $('#data tbody')
            .on('click', 'a[rel="delete"]', function () {
                var tr = tblBodegas.cell($(this).closest('td, li')).index();
                var data = tblBodegas.row(tr.row).data();
                var parameters = new FormData();
                parameters.append('action', 'btnEliminarBodegajsn');
                parameters.append('id', data.id);
                fncModificarEstadoItem(window.location.pathname, parameters, function (response) {
                    dctListarBodegas.dctVariables.lstBodegas = [];
                    dctListarBodegas.dctVariables.lstBodegas.push(response);
                    $('#data').DataTable().clear().rows.add(dctListarBodegas.dctVariables.lstBodegas).draw();
            });
        });
    }
}
$(function () {
    
    dctListarBodegas.fncCatalogoBodegastbl();

    $('#buscar_bodega').select2({
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
                    action: 'slcBuscarBodegajsn',
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el nombre de la bodega o responsable',
        minimumInputLength: 1,
        templateResult: fncBuscarBodegaRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        dctListarBodegas.dctVariables.lstBodegas = [];
        dctListarBodegas.dctVariables.lstBodegas.push(data);
        $('#dataTable').prop('hidden', false);
        $('#data').DataTable().clear().rows.add(dctListarBodegas.dctVariables.lstBodegas).draw();
    });
});

