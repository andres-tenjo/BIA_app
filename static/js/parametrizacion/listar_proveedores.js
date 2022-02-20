dctListarProveedores = {
    
    dctVariables: {
        lstProveedores: [],
    },

    fncCatalogoProveedorestbl: function () {
        tblProvedores = $('#data').DataTable({
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
            data: this.lstProveedores,
            columns: [
                { "data": "person_type.name"},
                { "data": "id_type.name"},
                { "data": "identification"},
                { "data": "email"},
                { "data": "contact_name"},
                { "data": "contact_cel"},
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
                        var buttons = '<a rel="details" class="btn btn-info btn-xs btn-flat" title="Detalle proveedor"><i class="fas fa-search"></i></a> ';
                        buttons += '<a href="/configuracion/actualizar_proveedor/' + row.id + '/" class="btn btn-success btn-xs btn-flat" title="Editar proveedor"><i class="fas fa-edit"></i></a> ';
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
                var tr = tblProvedores.cell($(this).closest('td, li')).index();
                var data = tblProvedores.row(tr.row).data();
                $('#qrCode').attr('src', data.qr_code);
                $('input[name="supp_name"]').val(data.supplier_name);
                $('input[name="type_person"]').val(data.person_type.name);
                $('input[name="id_type"]').val(data.id_type.name);
                $('input[name="id_number"]').val(data.identification);
                $('input[name="mail"]').val(data.email);
                $('input[name="contact"]').val(data.contact_name);
                $('input[name="cel"]').val(data.contact_cel);
                if(data.other_contact_name){
                    $('input[name="contact2"]').prop('hidden', false);
                    $('input[name="contact2"]').val(data.other_contact_name);
                }
                if(data.other_contact_cel){
                    $('input[name="cel2"]').prop('hidden', false);
                    $('input[name="cel2"]').val(data.other_contact_cel);
                }
                $('input[name="depto"]').val(data.department.department_name);
                $('input[name="city"]').val(data.city.city_name);
                $('input[name="dir"]').val(data.supplier_address);
                $('input[name="postal"]').val(data.postal_code);
                $('input[name="min_purchase_value"]').val(data.min_purchase_value);
                $('input[name="logistic_condition"]').val(data.logistic_condition.name);
                $('input[name="pay_method"]').val(data.pay_method.name);
                if(data.pay_method.id == 'CR'){
                    $('#credDays').prop('hidden', false);
                    $('#credLimit').prop('hidden', false);
                    $('input[name="credit_days"]').val(data.credit_days);
                    $('input[name="credit_limit"]').val('$ ' + parseFloat(data.credit_limit).toFixed(2));
                }
                if(data.purchase_conditions == true){
                    $('#purchaseConditions').prop('hidden', false);
                }
                if(data.min_quantity == true){
                    $('#q_min').prop('hidden', false);
                    $('input[name="q_min"]').val(data.min_purchase_quantity);
                }
                if(data.min_volume == true){
                    $('#vol_min').prop('hidden', false);
                    $('input[name="vol_min"]').val(data.min_purchase_quantity);
                }
                if(data.min_value == true){
                    $('#val_min').prop('hidden', false);
                    $('input[name="val_min"]').val(data.min_purchase_quantity);
                }
                $('#myModalDet').modal('show');
            }) 
            .on('click', 'a[rel="delete"]', function () {
                var tr = tblProvedores.cell($(this).closest('td, li')).index();
                var data = tblProvedores.row(tr.row).data();
                var parameters = new FormData();
                parameters.append('action', 'btnEliminarProveedorjsn');
                parameters.append('id', data.id);
                delete_action(window.location.pathname, parameters, function (response) {
                    dctListarProveedores.dctVariables.lstProveedores = [];
                    dctListarProveedores.dctVariables.lstProveedores.push(response);
                    $('#data').DataTable().clear().rows.add(dctListarProveedores.dctVariables.lstProveedores).draw();
            });
            
        });
    }
}

$(function () {

    dctListarProveedores.fncCatalogoProveedorestbl();
    
    $('#buscar_proveedor').select2({
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
                    action: 'slcBuscarProveedoresjsn',
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
        templateResult: formatRepoSupplier,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        $('#dataTable').prop('hidden', false);
        dctListarProveedores.dctVariables.lstProveedores.push(data);
        $('#data').DataTable().clear().rows.add(dctListarProveedores.dctVariables.lstProveedores).draw();
    });
});