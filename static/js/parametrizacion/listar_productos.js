dctListarProductos = {

    dctVariables: {
        lstProductos: [],
    },

    fncCatalogoProductostbl: function () {
        tblProductos = $('#data').DataTable({
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
            data: this.lstProductos,
            columns: [
                { "data": "id"},
                { "data": "product_desc"},
                { "data": "presentation"},
                { "data": "trademark"},
                { "data": "sales_unit.sales_unit"},
                { "data": "full_sale_price"},
                { "data": "state.name"},
                { "data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4, -5, -6, -7, -8],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$ '+ parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a rel="details" class="btn btn-info btn-xs btn-flat" title="Detalle producto"><i class="fas fa-search"></i></a> ';
                        buttons += '<a href="/configuracion/actualizar_producto/' + row.id + '/" class="btn btn-success btn-xs btn-flat" title="Editar producto"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo-alt"></i></a> ';
                        return buttons;
                    }
                },
    
            ],
            initComplete: function(settings, json) {
            }
        });
        
        $('#data tbody').on('click', 'a[rel="details"]', function () {
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            var data = tblProductos.row(tr.row).data();
            $('#qrCode').attr('src', data.qr_code);
            $('input[name="cod"]').val(data.id);
            $('input[name="name"]').val(data.product_desc);
            $('input[name="presentation"]').val(data.presentation);
            if (data.product_cat){
                $('input[name="category"]').val(data.product_cat.product_cat);
            }
            if (data.product_subcat){
                $('input[name="subcategory"]').val(data.product_subcat.product_subcat);
            }
            $('input[name="brand"]').val(data.trademark);
            $('input[name="udc"]').val(data.purchase_unit.purchase_unit);
            $('input[name="cost_pu"]').val('$ ' + parseFloat(data.cost_pu).toFixed(2));
            $('input[name="q_pu"]').val(data.quantity_pu);
            $('input[name="udv"]').val(data.sales_unit.sales_unit);
            $('input[name="unit_price"]').val('$ ' + parseFloat(data.full_sale_price).toFixed(2));
            $('input[name="q_su"]').val(data.quantity_su);
            $('input[name="split"]').val(data.split);
            $('input[name="state"]').val(data.state.name);
            $('input[name="iva"]').val(parseFloat(data.iva).toFixed(2) + ' %');
            $('input[name="otherImp"]').val(parseFloat(data.other_tax).toFixed(2) + ' %');
            if(data.product_dimention == true){
                $('#productDimention').prop("hidden", false)
                $('input[name="weight_udc"]').val(data.weight_udc);
                $('input[name="width_udc"]').val(data.width_udc);
                $('input[name="high_udc"]').val(data.high_udc);
                $('input[name="length_udc"]').val(data.length_udc);
                $('input[name="stacking_udc"]').val(data.stacking_udc);
                if(data.orientation_udc == true){
                    $('#orientation_udc').attr("checked", true);
                }else if(data.orientation_udc == false){
                    $('#orientation_udc').attr("checked", false);
                }
                $('input[name="weight_udv"]').val(data.weight_udv);
                $('input[name="width_udv"]').val(data.width_udv);
                $('input[name="high_udv"]').val(data.high_udv);
                $('input[name="length_udv"]').val(data.length_udv);
                $('input[name="stacking_udv"]').val(data.stacking_udv);
                if(data.orientation_udv == true){
                    $('#orientation_udv').attr("checked", true);
                }else if(data.orientation_udv == false){
                    $('#orientation_udv').attr("checked", false);
                }
            }
            if(data.storage_conditions == true){
                $('#storageConditions').prop("hidden", false)
                $('input[name="cross_contamination"]').val(data.cross_contamination.name);
                $('input[name="restriction_temperature"]').val(data.restriction_temperature);
            }
            $('#myModalDet').modal('show');
        });
        
        $('#data tbody').on('click', 'a[rel="delete"]', function () {
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            var data = tblProductos.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'frmEliminarProductojsn');
            parameters.append('id', data.id);
            fncModificarEstadoItem(window.location.pathname, parameters, function (response) {
                dctListarProductos.dctVariables.lstProductos = [];
                dctListarProductos.dctVariables.lstProductos.push(response);
                $('#data').DataTable().clear().rows.add(dctListarProductos.dctVariables.lstProductos).draw();
            });
        });
    },
}

$(function () {
    
    dctListarProductos.fncCatalogoProductostbl();

    $('#buscar_producto').select2({
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
                    action: 'slcBuscarProductosjsn',
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese código de producto, nombre o presentación del producto',
        minimumInputLength: 1,
        templateResult: fncBuscarProductoRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        dctListarProductos.dctVariables.lstProductos = [];
        dctListarProductos.dctVariables.lstProductos.push(data);
        $('#dataTable').prop('hidden', false);
        $('#data').DataTable().clear().rows.add(dctListarProductos.dctVariables.lstProductos).draw();
    });
});