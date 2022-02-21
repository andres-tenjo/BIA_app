$(function () {
    $('#tabla_visitas').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
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
                'action':'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            { "data": "cod_visita"},
            { "data": "cod_cliente"},
            { "data": "fecha_visita"},
            { "data": "hora_inicio"},
            { "data": "estado_visita"},
            { "data": "estado_visita"},
        ],
        columnDefs: [
            {
                targets: [5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    buttons += buttons = '<a href="/comercial/prom_assign/' + row.cod_visita + '/" class="btn btn-xs btn-flat"><i class="fas fa-sign-in-alt"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings, json) {
        }
    });
});

$(function () {
    
    modal_title = $('.modal-title');
    
    getData();
    
    $('.btnAdd').on('click', function() {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de producto');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $('#ModalProd').modal('show');
    });
    
    $('#data tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edición de producto');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblProd.cell($(this).closest('td, li')).index();
            var data = tblProd.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="cod"]').val(data.cod);
            $('input[name="name"]').val(data.name);
            $('input[name="pres"]').val(data.pres);
            $('input[name="brand"]').val(data.brand);
            $('select[name="category"]').val(data.category);
            $('select[name="subcategory"]').val(data.subcategory);
            $('input[name="unit_price"]').val(data.unit_price);
            $('select[name="udc"]').val(data.udc);
            $('select[name="udv"]').val(data.udv);
            $('input[name="equiv"]').val(data.equiv);
            $('input[name="del_time"]').val(data.equiv);
            $('input[name="bar_code"]').val(data.bar_code);
            $('input[name="iva"]').val(data.iva);
            $('select[name="state"]').val(data.state);
            $('form')[0].reset();
            $('#ModalProd').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblProd.cell($(this).closest('td, li')).index();
            var data = tblProd.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            fncGuardarFormularioAjax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar registro?', parameters, function () {
                tblProd.ajax.reload();
            });
        });
    $('#ModalProd').on('shown.bs.modal', function () {
        $('form')[0].reset();
    });
    
    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación', '¿Desea guardar el registro?', parameters, function () {
            $('#ModalProd').modal('hide');
            tblProd.ajax.reload();
            //getData();
        });
    });
});

