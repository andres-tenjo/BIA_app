var tblProducts;
var product = '';
var prom = {
    items: {
        name: '',
        quantity: '',
        expiration_date: '',
        desc: '',
        cons: '',
        obs: '',
        products: []
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.products, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "name"},
                {"data": "udc.name"},
                {"data": "quantity_udv"},
                {"data": "price_udv"},
                {"data": "price_udc"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-2, -3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.quantity_udv + '">';
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    step: 1
                });

            },
            initComplete: function (settings, json) {
            }
        });
    },
};

function fncBuscarProductoRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-12 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.name + '<br>' +
        '<b>Código:</b> ' + repo.cod + '<br>' +
        '<b>Presentación:</b> ' + repo.pres + '<br>' +
        '<b>Precio:</b> <span class="badge badge-warning">$'+repo.price_udv+'</span>'+
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#expiration_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });

    $('#frmProm').on('submit', function (e) {
        e.preventDefault();
        if (prom.items.products.length === 0) {
            fncMensajeErrormns('Debe al menos agregar un producto a su promoción');
            return false;
        }
        prom.items.name = $('input[name="name"]').val();
        prom.items.desc = $('textarea[name="desc"]').val();
        prom.items.quantity = $('input[name="quantity"]').val();
        prom.items.obs = $('textarea[name="obs"]').val();
        prom.items.cons = $('textarea[name="cons"]').val();
        prom.items.expiration_date = $('input[name="expiration_date"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('prom', JSON.stringify(prom.items));
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación','¿Estas seguro de generar esta promoción?', parameters, function (response) {
            location.href = '/configuracion/listar_promociones';
        });
    });

    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_products',
                    ids: JSON.stringify(prom.get_ids())
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el código, nombre o presentación del producto',
        minimumInputLength: 1,
        templateResult: fncBuscarProductoRepo,

    }).on('select2:select', function (e) {
        var data = e.params.data;
        $('input[name="cod"]').val(data.cod);
        $('input[name="nameProd"]').val(data.name);
        $('input[name="pres"]').val(data.pres);
        $('input[name="udv"]').val(data.udc.name);
        $('input[name="uniPrice"]').val('$ ' + parseFloat(data.price_udv).toFixed(2));
        $('input[name="cantDisp"]').val(data.quantity_udc);
        $('input[name="cant"]').focus();
        $(this).val('').trigger('change.select2');
        product = data;
    });

    $("input[name='cant']").TouchSpin({
        min: 0,
        step: 1,
    }).on('change', function (){
        disp = parseInt($('input[name="cantDisp"]').val());
        real = parseInt($('input[name="cant"]').val());
        if (real > disp){
            fncMensajeInformacionmns('La cantidad que esta digitando es mayor que la disponible, ingrese una cantodad menor o igual')
            $('input[name="cant"]').val(0);
            return false;
        }
    }).val(0)

    $("input[name='descProm']").TouchSpin({
        min: 0,
        max: 100,
        step: 1,
        decimals: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
    }).on('change', function (){
        
    }).val(0.00)

    $('.btnAddProd').on('click', function () {
        if (product == ''){
            fncMensajeInformacionmns('Ingrese un producto');
            $('select[name="search"]').focus();
            return false;
        }
        cant = $('input[name="cant"]').val();
        product.quantity_udv = cant;
        price = parseFloat(product.price_udv);
        desc = parseFloat($('input[name="descProm"]').val()).toFixed(2)/100;
        product.price_udc = price - (price * desc);
        $('input[name="cod"]').val('');
        $('input[name="nameProd"]').val('');
        $('input[name="pres"]').val('');
        $('input[name="udv"]').val('');
        $('input[name="uniPrice"]').val('');
        $('input[name="cantDisp"]').val('');
        $('input[name="cant"]').val(0);
        $('input[name="descProm"]').val(0);
        $('select[name="search"]').focus();
        prom.add(product);
        product = '';
    });

    $('.btnRemoveAll').on('click', function () {
        if(prom.items.products.length === 0) return false;
        fncMensajeAlertamns('Notificación', '¿Está seguro de eliminar todos los productos?', function () {
            prom.items.products = [];
            prom.list();    
        });
    });

    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            fncMensajeAlertamns('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    prom.items.products.splice(tr.row, 1);
                    prom.list();
                }, function () {

            });
        })
        /*.on('change', 'input[name="cant"]', function () {
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            prom.items.products[tr.row].cant = cant;
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + prom.items.products[tr.row].subtotal.toFixed(2));
        });*/

});

