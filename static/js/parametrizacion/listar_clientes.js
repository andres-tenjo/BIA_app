dctListarClientes = {
    
    dctVariables: {
        lstClientes: [],
    },

    fncCatalogoClientestbl: function () {
        tblClientes = $('#data').DataTable({
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
            data: this.dctVariables.lstClientes,
            columns: [
                { "data": "business_name"},
                { "data": "identification"},
                { "data": "cel_number"},
                { "data": "email"},
                { "data": "customer_cat.customer_cat"},
                { "data": "customer_zone.customer_zone"},
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
                        var buttons = '<a rel="details" class="btn btn-info btn-xs btn-flat" title="Detalle cliente"><i class="fas fa-search"></i></a> ';
                        buttons += '<a href="/configuracion/actualizar_cliente/' + row.id + '/" class="btn btn-success btn-xs btn-flat" title="Editar cliente"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo-alt"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });
        $('#data tbody')
            .on('click', 'a[rel="details"]', function () {
                var tr = tblClientes.cell($(this).closest('td, li')).index();
                var data = tblClientes.row(tr.row).data();
                $('#qrCode').attr('src', data.qr_code);
                $('input[name="id_type"]').val(data.id_type.name);
                $('input[name="id_number"]').val(data.identification);
                $('input[name="name"]').val(data.business_name);
                $('input[name="cel_number"]').val(data.cel_number);
                $('input[name="email"]').val(data.email);
                $('input[name="department"]').val(data.department.department_name);
                $('input[name="city"]').val(data.city.city_name);
                $('input[name="zone"]').val(data.customer_zone.customer_zone);
                $('input[name="address"]').val(data.delivery_address);
                $('input[name="del_schedule"]').val(data.del_schedule_init);
                $('input[name="del_schedule_end"]').val(data.del_schedule_end);
                $('input[name="category"]').val(data.customer_cat.customer_cat);
                $('input[name="advisor"]').val(data.commercial_advisor.advisor);
                $('input[name="pay_method"]').val(data.pay_method.name);
                if(data.pay_method.id == 'CR'){
                    $('#credDays').prop('hidden', false);
                    $('#credLimit').prop('hidden', false);
                    $('input[name="credit_days"]').val(data.credit_days);
                    $('input[name="credit_limit"]').val('$ ' + parseFloat(data.credit_value).toFixed(2));
                }
                $('#myModalDet').modal('show');
            })
            .on('click', 'a[rel="delete"]', function () {
                var tr = tblClientes.cell($(this).closest('td, li')).index();
                var data = tblClientes.row(tr.row).data();
                var parameters = new FormData();
                parameters.append('action', 'btnEliminarClientejsn');
                parameters.append('id', data.id);
                delete_action(window.location.pathname, parameters, function (response) {
                    dctListarClientes.dctVariables.lstClientes = [];
                    dctListarClientes.dctVariables.lstClientes.push(response);
                    $('#data').DataTable().clear().rows.add(dctListarClientes.dctVariables.lstClientes).draw();
            });
        });
    }
}

$(function () {
    
    dctListarClientes.fncCatalogoClientestbl();

    $('#buscar_cliente').select2({
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
                    action: 'slcBuscarClientejsn',
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el cliente, identificación o Nº celular',
        minimumInputLength: 1,
        templateResult: formatRepoCustomer,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        dctListarClientes.dctVariables.lstClientes = [];
        dctListarClientes.dctVariables.lstClientes.push(data);
        $('#dataTable').prop('hidden', false);
        $('#data').DataTable().clear().rows.add(dctListarClientes.dctVariables.lstClientes).draw();
    });
});