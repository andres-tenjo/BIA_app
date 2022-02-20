var tblProducts;
var idCartera = '';
var product = '';
var id_prod = '';
var sales = {
    items: {
        customer: '',
        name: '',
        nit: '',
        cel: '',
        pay_method: '',
        estado_cartera: '',
        order_date: '',
        order_city:'',
        order_address: '',
        deliver_date: '',
        del_schedule: '',
        observation:'',
        subtotal: 0.00,
        iva: 00,
        dcto: 0.00,
        total: 0.00,
        products: []
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.products, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    view_state_cartera: function () {
        
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        var iva = 0.00;
        var dcto = 0.00;
        var total = 0.00;
        cbDesc = $('.cbDesc').val();
        $.each(this.items.products, function (pos, dict) {
            subtotal += dict.subtotal;
            iva += (dict.cant * dict.price_udv) * dict.iva
            dcto += (dict.cant * dict.price_udv) * dict.desc
        });
        this.items.subtotal = subtotal;
        this.items.iva = iva;
        this.items.dcto = dcto;
        total = subtotal + iva - dcto
        this.items.total = total;

        $('input[name="subtotal"]').val('$ ' + this.items.subtotal.toFixed(2));
        $('input[name="iva"]').val('$ ' + this.items.iva.toFixed(2));
        $('input[name="dcto"]').val('$ ' + this.items.dcto);
        $('input[name="total"]').val('$ ' + this.items.total.toFixed(2));
    },
    list: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
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
            data: this.items.products,
            columns: [
                { "data": "cod"},
                { "data": "name"},
                { "data": "udv.name"},
                { "data": "price_udv"},
                { "data": "cant"},
                { "data": "subtotal"},
                { "data": "iva"},
                { "data": "desc"},
                { "data": "id"},
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
                    targets: [-4, -6],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$ '+parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2, -3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return (parseFloat(data).toFixed(2) * 100) + ' %';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1
                });

            },
            initComplete: function(settings, json) {
            }
        });
    },
};

function formatRepoProd(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-12 text-left shadow-sm">' +
        //'<br>' +
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

function formatRepoCustomer(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-12 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.customer + '<br>' +
        '<b>Id:</b> ' + repo.id_number + '<br>' +
        '<b>Categoría:</b> ' + repo.category.name + '<br>' +
        '<b>Celular:</b> ' + repo.cel_number + '<br>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function(){

    // Cargar select2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // Buscar cliente
    $('select[name="customer"]').select2({
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
                    action: 'search_customer'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el nombre, número de identificación ó celular del proveedor',
        minimumInputLength: 1,
        templateResult: formatRepoCustomer,

    // Seleccionar cliente
    }).on('select2:select', function (e) {
        var data = e.params.data;
        console.log(data);
        sales.items.customer = data.id;
        sales.items.name = data.customer;
        sales.items.nit = data.id_number;
        sales.items.cel = data.cel_number;
        sales.items.order_city = data.city.name;
        sales.items.del_schedule = data.del_schedule;
        $('input[name="id_number"]').val(data.id_number);
        $('input[name="cel_number"]').val(data.cel_number);
        $('input[name="mail"]').val(data.email);
        $('input[name="pay_method"]').val(data.pay_method.name);
        $('input[name="city"]').val(data.city.name);
        $('input[name="zone"]').val(data.zone.name);
        $('input[name="order_address"]').val(data.address);
        id_customer = data.id;
        if($('input[name="pay_method"]').val() === 'Crédito' ){
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action':'cartera_cliente',
                    'id': id_customer
                },
                dataType: 'json',
            }).done(function(data) {
                console.log(data);
                if(data[0].state == 'VE') {
                    message_info('El proveedor presenta actualmente una cartera vencida, solicite una autorización para continuar')
                    $('input[name="stateCartera"]').val('Vencida');
                    $('.btnCartera').removeAttr('disabled');
                    return false;
                }
                return false;
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus +': '+errorThrown);
            }).always(function(data) {                
            });
        }
        $('select[name="search"]').focus();

    }).on('select2:unselect', function (e) {
        $('input[name="id_number"]').val('');
        $('input[name="cel_number"]').val('');
        $('input[name="mail"]').val('');
        $('input[name="pay_method"]').val('');
        $('input[name="stateCartera"]').val('');
        // falta btn cartera
        $('.btnCartera').attr('disabled');
    });
    
    // Agregar productos collapse
    $('.btnAddProd').on('click', function () {
        cust = $('select[name="customer"]').val();
        cart = $('input[name="stateCartera"]').val();
        if(cust == ''){
            message_info('Debe ingresar un proveedor para gestionar una negociación');
            $('select[name="customer"]').focus();
            return false;
        }else if(cart == 'Vencida'){
            message_info('El proveedor presenta una cartera vencida');
            return false;
        }
    });

    // Cargar datetimepicker a fecha de venta
    $('#order_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD"),
        maxDate: moment().format("YYYY-MM-DD"),
    });

    sales.items.order_date = $('#order_date').val();

    // Cargar datetimepicker a fecha de venta
    $('#deliver_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD"),
    });

    // Buscar productos
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
                    ids: JSON.stringify(sales.get_ids())
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
        templateResult: formatRepoProd,

    }).on('select2:select', function (e) {
        var data = e.params.data;
        id_prod = data.id;
        products = sales.get_ids();
        if (products.length > 0){
            $.each(products, function (pos, value) {
                if(id_prod == value){
                    $.confirm({
                        title: 'Alerta',
                        content: '¿El producto ya se registro, desea modificarlo?',
                        buttons: {
                            Si: function () {
                                sales.items.products.splice(pos, 1);
                                $('input[name="cod"]').val(data.cod);
                                $('input[name="nameProd"]').val(data.name);
                                $('input[name="pres"]').val(data.pres);
                                $('input[name="udv"]').val(data.udc.name);
                                $('input[name="uniPrice"]').val('$ ' + parseFloat(data.price_udv).toFixed(2));
                                $('input[name="ivaProd"]').val(parseFloat(data.iva).toFixed(2) + ' %');
                                $('input[name="cantDisp"]').val(data.saldos_inv[0].inventory_balance);
                                $('select[name="search"]').val('').trigger('change.select2');
                                data.cant = 1;
                                data.subtotal = 0.00;
                                data.desc = 0.00;
                                data.total = 0.00;
                                product = data;
                                sales.list();
                                $('input[name="cantSol"]').focus();
                            },
                            Cancelar: function () {
                                $('select[name="search"]').val('').trigger('change.select2');
                                $('select[name="search"]').focus();
                            }
                        }
                    });
                } else if(id_prod != value){
                $('input[name="cod"]').val(data.cod);
                $('input[name="nameProd"]').val(data.name);
                $('input[name="pres"]').val(data.pres);
                $('input[name="udv"]').val(data.udc.name);
                $('input[name="uniPrice"]').val('$ ' + parseFloat(data.price_udv).toFixed(2));
                $('input[name="ivaProd"]').val(parseFloat(data.iva).toFixed(2) + ' %');
                $('input[name="cantDisp"]').val(data.saldos_inv[0].inventory_balance);
                $('select[name="search"]').val('').trigger('change.select2');
                data.cant = 1;
                data.subtotal = 0.00;
                data.desc = 0.00;
                data.total = 0.00;
                product = data;
                sales.list();
                $('input[name="cantSol"]').focus();
                }
            });
        }
        else if (products.length == 0){
            $('input[name="cod"]').val(data.cod);
            $('input[name="nameProd"]').val(data.name);
            $('input[name="pres"]').val(data.pres);
            $('input[name="udv"]').val(data.udc.name);
            $('input[name="uniPrice"]').val('$ ' + parseFloat(data.price_udv).toFixed(2));
            $('input[name="ivaProd"]').val(parseFloat(data.iva).toFixed(2) + ' %');
            $('input[name="cantDisp"]').val(data.saldos_inv[0].inventory_balance);
            $(this).val('').trigger('change.select2');
            $('input[name="cantSol"]').focus();
            data.cant = 1;
            data.subtotal = 0.00;
            data.desc = 0.00;
            data.total = 0.00;
            product = data;
            sales.list();
        }
    });
    
    // Función para calcular la cantidad disponible vs la solicitada
    $("input[name='cantSol']").TouchSpin({
        min: 1,
        step: 1,
    }).on('change', function (){
        disp = parseInt($('input[name="cantDisp"]').val());
        real = parseInt($('input[name="cantSol"]').val());
        parcial = real - disp
        prod = $('input[name="nameProd"]').val();
        udv = $('input[name="udv"]').val();
        if (real > disp){
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action':'compare_quantity',
                    'id': id_prod
                },
                dataType: 'json',
            }).done(function(data) {
                ordersPurchase = data;
                if(ordersPurchase.length > 0){
                    order = '';
                    cant = 0;
                    fecha = '';
                    $.each(ordersPurchase, function (pos, dict) {
                    if(dict.order_purchase.state.name == 'Abierta'){
                        order = dict.order_purchase.id;
                        cant = dict.cant;
                        fecha = dict.order_purchase.deliver_date;
                        cant_total = disp + cant;
                        if(real < cant_total){
                            $.confirm({
                                columnClass: 'col-md-12',
                                title: 'Próximos ingresos',
                                content: 'El producto ' + prod + ' tiene previsto el ingreso para ' + fecha + ' con la cantidad de ' + cant  + udv + ' en la O.C. ' + order,
                                buttons: {
                                    Continuar: function () {
                                        cant = real;
                                        product.cant = cant;
                                        product.subtotal = product.cant * product.price_udv;
                                        product.price_udv = parseFloat(product.price_udv);
                                        product.iva = parseFloat(product.iva)/100;
                                        $('input[name="cod"]').val('');
                                        $('input[name="nameProd"]').val('');
                                        $('input[name="pres"]').val('');
                                        $('input[name="udv"]').val('');
                                        $('input[name="uniPrice"]').val('');
                                        $('input[name="ivaProd"]').val('');
                                        $('input[name="descProd"]').val('');
                                        $('input[name="cantDisp"]').val('');
                                        $('input[name="cantSol"]').val(0);
                                        sales.add(product);
                                        sales.calculate_invoice();
                                        product = '';
                                    },
                                    Cancelar: function () {
                                        $.ajax({
                                            url: window.location.pathname,
                                            type: 'POST',
                                            data: {
                                                'action':'lost_sales',
                                                'date' : sales.items.order_date,
                                                'id_cust': sales.items.customer,
                                                'id_prod': id_prod,
                                                'cant': real
                                            },
                                            dataType: 'json',
                                        }).done(function(data) {
                                            if (!data.hasOwnProperty('error')){
                                                $('input[name="cod"]').val('');
                                                $('input[name="nameProd"]').val('');
                                                $('input[name="pres"]').val('');
                                                $('input[name="udv"]').val('');
                                                $('input[name="uniPrice"]').val('');
                                                $('input[name="ivaProd"]').val('');
                                                $('input[name="descProd"]').val('');
                                                $('input[name="cantDisp"]').val('');
                                                $('input[name="cantSol"]').val(0);
                                                return false;
                                            }
                                            message_error(data.error);
                                        }).fail(function (jqXHR, textStatus, errorThrown) {
                                            alert(textStatus +': '+errorThrown);
                                        }).always(function(data) {                
                                        });        
                                    },
                                    Parcial: {
                                        text: 'Venta parcial',
                                        btnClass: 'btn-blue',
                                        keys: ['enter', 'shift'],
                                        action: function(){
                                            $.ajax({
                                                url: window.location.pathname,
                                                type: 'POST',
                                                data: {
                                                    'action':'lost_sales',
                                                    'date' : sales.items.order_date,
                                                    'id_cust': sales.items.customer,
                                                    'id_prod': id_prod,
                                                    'cant': parcial
                                                },
                                                dataType: 'json',
                                            }).done(function(data) {
                                                if (!data.hasOwnProperty('error')){
                                                    cant = disp;
                                                    product.cant = cant;
                                                    product.subtotal = product.cant * product.price_udv;
                                                    product.price_udv = parseFloat(product.price_udv);
                                                    product.iva = parseFloat(product.iva)/100;
                                                    $('input[name="cod"]').val('');
                                                    $('input[name="nameProd"]').val('');
                                                    $('input[name="pres"]').val('');
                                                    $('input[name="udv"]').val('');
                                                    $('input[name="uniPrice"]').val('');
                                                    $('input[name="ivaProd"]').val('');
                                                    $('input[name="descProd"]').val('');
                                                    $('input[name="cantDisp"]').val('');
                                                    $('input[name="cantSol"]').val(0);
                                                    sales.add(product);
                                                    sales.calculate_invoice();
                                                    product = '';
                                                    return false;
                                                }
                                                message_error(data.error);
                                            }).fail(function (jqXHR, textStatus, errorThrown) {
                                                alert(textStatus +': '+errorThrown);
                                            }).always(function(data) {                
                                            });
                                        }
                                    }
                                }
                            });
                        }else if(real > cant_total){
                            $.confirm({
                                columnClass: 'col-md-12',
                                title: 'Próximos ingresos',
                                content: 'El producto ' + prod + ' tiene previsto el ingreso para ' + fecha + ' con la cantidad de ' + cant  + udv + ' en la O.C. ' + order + 
                                '<br> Si se genera O.C. hoy el producto tendría un ingreso previsto para el ' + fecha,
                                buttons: {
                                    Continuar: function () {
                                        cant = real;
                                        product.cant = cant;
                                        product.subtotal = product.cant * product.price_udv;
                                        product.price_udv = parseFloat(product.price_udv);
                                        product.iva = parseFloat(product.iva)/100;
                                        $('input[name="cod"]').val('');
                                        $('input[name="nameProd"]').val('');
                                        $('input[name="pres"]').val('');
                                        $('input[name="udv"]').val('');
                                        $('input[name="uniPrice"]').val('');
                                        $('input[name="ivaProd"]').val('');
                                        $('input[name="descProd"]').val('');
                                        $('input[name="cantDisp"]').val('');
                                        $('input[name="cantSol"]').val(0);
                                        sales.add(product);
                                        sales.calculate_invoice();
                                        product = '';
                                    },
                                    Cancelar: function () {
                                        $.ajax({
                                            url: window.location.pathname,
                                            type: 'POST',
                                            data: {
                                                'action':'lost_sales',
                                                'date' : sales.items.order_date,
                                                'id_cust': sales.items.customer,
                                                'id_prod': id_prod,
                                                'cant': real
                                            },
                                            dataType: 'json',
                                        }).done(function(data) {
                                            if (!data.hasOwnProperty('error')){
                                                $('input[name="cod"]').val('');
                                                $('input[name="nameProd"]').val('');
                                                $('input[name="pres"]').val('');
                                                $('input[name="udv"]').val('');
                                                $('input[name="uniPrice"]').val('');
                                                $('input[name="ivaProd"]').val('');
                                                $('input[name="descProd"]').val('');
                                                $('input[name="cantDisp"]').val('');
                                                $('input[name="cantSol"]').val(0);
                                                return false;
                                            }
                                            message_error(data.error);
                                        }).fail(function (jqXHR, textStatus, errorThrown) {
                                            alert(textStatus +': '+errorThrown);
                                        }).always(function(data) {                
                                        });        
                                    },
                                    Parcial: {
                                        text: 'Venta parcial',
                                        btnClass: 'btn-blue',
                                        keys: ['enter', 'shift'],
                                        action: function(){
                                            $.ajax({
                                                url: window.location.pathname,
                                                type: 'POST',
                                                data: {
                                                    'action':'lost_sales',
                                                    'date' : sales.items.order_date,
                                                    'id_cust': sales.items.customer,
                                                    'id_prod': id_prod,
                                                    'cant': parcial
                                                },
                                                dataType: 'json',
                                            }).done(function(data) {
                                                if (!data.hasOwnProperty('error')){
                                                    cant = disp;
                                                    product.cant = cant;
                                                    product.subtotal = product.cant * product.price_udv;
                                                    product.price_udv = parseFloat(product.price_udv);
                                                    product.iva = parseFloat(product.iva)/100;
                                                    $('input[name="cod"]').val('');
                                                    $('input[name="nameProd"]').val('');
                                                    $('input[name="pres"]').val('');
                                                    $('input[name="udv"]').val('');
                                                    $('input[name="uniPrice"]').val('');
                                                    $('input[name="ivaProd"]').val('');
                                                    $('input[name="descProd"]').val('');
                                                    $('input[name="cantDisp"]').val('');
                                                    $('input[name="cantSol"]').val(0);
                                                    sales.add(product);
                                                    sales.calculate_invoice();
                                                    product = '';
                                                    return false;
                                                }
                                                message_error(data.error);
                                            }).fail(function (jqXHR, textStatus, errorThrown) {
                                                alert(textStatus +': '+errorThrown);
                                            }).always(function(data) {                
                                            });
                                        }
                                    }
                                }
                            });
                        }
                    }
                });
                }else if(ordersPurchase.length == 0){
                    $.confirm({
                        columnClass: 'col-md-12',
                        title: 'Próximos ingresos',
                        content: 'Si se genera O.C. hoy el producto tendría un ingreso previsto para el ' + fecha,
                        buttons: {
                            Continuar: function () {
                                cant = real;
                                product.cant = cant;
                                product.subtotal = product.cant * product.price_udv;
                                product.price_udv = parseFloat(product.price_udv);
                                product.iva = parseFloat(product.iva)/100;
                                $('input[name="cod"]').val('');
                                $('input[name="nameProd"]').val('');
                                $('input[name="pres"]').val('');
                                $('input[name="udv"]').val('');
                                $('input[name="uniPrice"]').val('');
                                $('input[name="ivaProd"]').val('');
                                $('input[name="descProd"]').val('');
                                $('input[name="cantDisp"]').val('');
                                $('input[name="cantSol"]').val(0);
                                sales.add(product);
                                sales.calculate_invoice();
                                product = '';
                            },
                            Cancelar: function () {
                                $.ajax({
                                    url: window.location.pathname,
                                    type: 'POST',
                                    data: {
                                        'action':'lost_sales',
                                        'date' : sales.items.order_date,
                                        'id_cust': sales.items.customer,
                                        'id_prod': id_prod,
                                        'cant': real
                                    },
                                    dataType: 'json',
                                }).done(function(data) {
                                    if (!data.hasOwnProperty('error')){
                                        $('input[name="cod"]').val('');
                                        $('input[name="nameProd"]').val('');
                                        $('input[name="pres"]').val('');
                                        $('input[name="udv"]').val('');
                                        $('input[name="uniPrice"]').val('');
                                        $('input[name="ivaProd"]').val('');
                                        $('input[name="descProd"]').val('');
                                        $('input[name="cantDisp"]').val('');
                                        $('input[name="cantSol"]').val(0);
                                        return false;
                                    }
                                    message_error(data.error);
                                }).fail(function (jqXHR, textStatus, errorThrown) {
                                    alert(textStatus +': '+errorThrown);
                                }).always(function(data) {                
                                });        
                            },
                            Parcial: {
                                text: 'Venta parcial',
                                btnClass: 'btn-blue',
                                keys: ['enter', 'shift'],
                                action: function(){
                                    $.ajax({
                                        url: window.location.pathname,
                                        type: 'POST',
                                        data: {
                                            'action':'lost_sales',
                                            'date' : sales.items.order_date,
                                            'id_cust': sales.items.customer,
                                            'id_prod': id_prod,
                                            'cant': parcial
                                        },
                                        dataType: 'json',
                                    }).done(function(data) {
                                        if (!data.hasOwnProperty('error')){
                                            cant = disp;
                                            product.cant = cant;
                                            product.subtotal = product.cant * product.price_udv;
                                            product.price_udv = parseFloat(product.price_udv);
                                            product.iva = parseFloat(product.iva)/100;
                                            $('input[name="cod"]').val('');
                                            $('input[name="nameProd"]').val('');
                                            $('input[name="pres"]').val('');
                                            $('input[name="udv"]').val('');
                                            $('input[name="uniPrice"]').val('');
                                            $('input[name="ivaProd"]').val('');
                                            $('input[name="descProd"]').val('');
                                            $('input[name="cantDisp"]').val('');
                                            $('input[name="cantSol"]').val(0);
                                            sales.add(product);
                                            sales.calculate_invoice();
                                            product = '';
                                            return false;
                                        }
                                        message_error(data.error);
                                    }).fail(function (jqXHR, textStatus, errorThrown) {
                                        alert(textStatus +': '+errorThrown);
                                    }).always(function(data) {                
                                    });
                                }
                            }
                        }
                    });
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus +': '+errorThrown);
            }).always(function(data) {                
            });
        }
    }).val(1)

    // Función para agregar productos a la tabla
    $('.btnAddP').on('click', function () {
        if (product == ''){
            message_info('Ingrese un producto');
            $('select[name="search"]').focus();
            return false;
        }
        cant = $('input[name="cantSol"]').val();
        product.cant = cant;
        product.subtotal = product.cant * product.price_udv;
        product.price_udv = parseFloat(product.price_udv);
        product.iva = parseFloat(product.iva)/100;
        product.total = product.subtotal + product.iva + product.desc
        $('input[name="cod"]').val('');
        $('input[name="nameProd"]').val('');
        $('input[name="pres"]').val('');
        $('input[name="udv"]').val('');
        $('input[name="uniPrice"]').val('');
        $('input[name="ivaProd"]').val('');
        $('input[name="descProd"]').val('');
        $('input[name="cantDisp"]').val('');
        $('input[name="cantSol"]').val(0);
        sales.add(product);
        sales.calculate_invoice();
        product = '';
    });
    
    // Checkbutton para establecer descuentos
    $('.cbDesc').on('click', function () {
        cbDesc = parseInt($('.cbDesc').val());
        console.log(cbDesc);
        dcto = sales.items.dcto;
        if(cbDesc == 0){
            if(sales.items.products.length === 0){
                message_info('Agregue al menos un producto para aplicar el descuento')
                return false;
            } else if(dcto > 0){
                $('.cbDesc').val(1);
                message_info('ingrese el % de descuento que desea aplicar')
                $('input[name="inpDesc"]').removeAttr('disabled')
            }
        } else if (cbDesc == 1){
            $('.cbDesc').val(0);
            $('input[name="inpDesc"]').attr('disabled');
            sales.calculate_invoice();
        }
    });

    // Función para establecer descuento
    $("input[name='inpDesc']").TouchSpin({
        min: 0,
        max: 100,
        step: 1,
        decimals: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
    }).on('change', function (){
        subtotal = sales.items.subtotal;
        desGen = $("input[name='inpDesc']").val()/100;
        desc = subtotal * desGen;
        sales.items.dcto = desc;
        $('input[name="dcto"]').val('$ ' + desc);
    }).val(0.00)

    // Boton eliminar productos de la tabla
    $('.btnRemoveAll').on('click', function () {
        if(sales.items.products.length === 0) return false;
        alert_action('Notificación', '¿Está seguro de eliminar todos los productos?', function () {
            sales.items.products = [];
            sales.list();    
        });
    });

    
    // Eventos de la tabla
    $('#tblProducts tbody')
        //Eliminar un producto de la tabla
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Está seguro de eliminar el producto?', function () {
                sales.items.products.splice(tr.row, 1);
                sales.list();
            });
        })
        /*Calcular cantidades de la tabla
        .on('change', 'input[name="cant"]', function () {
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            sales.items.products[tr.row].cant = cant;
            sales.items.products[tr.row].subtotal = cant * sales.items.products[tr.row].price_udv
            sales.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + sales.items.products[tr.row].subtotal.toFixed(2));
    });*/

    // event submit form
    $('form').on('submit', function (e) {
        e.preventDefault();
        if(sales.items.products.length === 0 ){
            message_error('Debe agregar al menos un producto a la factura de venta ')
            return false;
        }
        sales.items.deliver_date = $('input[name="deliver_date"]').val();
        sales.items.pay_method = $('input[name="pay_method"]').val();
        sales.items.order_address = $('input[name="order_address"]').val();
        sales.items.observation = $('textarea[name="obs"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('sales', JSON.stringify(sales.items));
        $.confirm({
            theme: 'material',
            title: 'Confirmaciòn',
            icon: 'fa fa-bell',
            content: '¿Está seguro de generar la factura de venta?',
            columnClass: 'small',
            typeAnimated: true,
            cancelButtonClass: 'btn-primary',
            draggable: true,
            dragWindowBorder: false,
            buttons: {
                info: {
                    text: "Si",
                    btnClass: 'btn-primary',
                    action: function () {
                        $.ajax({
                            url: window.location.pathname,
                            type: 'POST',
                            data: parameters,
                            dataType: 'json',
                            processData: false,
                            contentType: false,
                        }).done(function(response) {
                            $.confirm({
                                animation: 'Rotate',
                                closeAnimation: 'scale',
                                columnClass: 'col-md-6',
                                icon: 'fa fa-save',
                                title: 'Confirmación',
                                content: 'Se ha generado la factura de venta Nº 000'+ response.id + ', por favor seleccione una opción',
                                buttons: {
                                    Generar: {
                                        text: 'Generar PDF',
                                        btnClass: 'btn-green',
                                        action: function () {
                                            console.log(response.id);
                                            console.log('si');
                                            window.open('/comercial/sale/invoice/pdf/' + response.id + '/', '_blank');
                                            location.href = '/comercial/lista_pedidos/';
                                            /*var parameters = new FormData();
                                            parameters.append('action', 'get_pdf');
                                            parameters.append('id_order', JSON.stringify(response.id));
                                            parameters.append('ids_prods', JSON.stringify(sales.get_ids()));
                                            parameters.append('sales', JSON.stringify(sales.items));
                                            $.ajax({
                                                url: window.location.pathname,
                                                type: 'POST',
                                                data: parameters,
                                                dataType: 'json',
                                                processData: false,
                                                contentType: false,
                                            }).done(function(data) {
                                                
                                            }).fail(function (jqXHR, textStatus, errorThrown) {
                                                alert(textStatus +': '+errorThrown);
                                            }).always(function(data) {                
                                            });*/
                                        },
                                    },
                                    Correo: {
                                        text: 'Envìar por correo',
                                        btnClass: 'btn-blue',
                                        action: function () {
                                            
                                        },
                                    },
                                    Cancelar: {
                                        text: 'Cancelar',
                                        btnClass: 'btn-red',
                                        action: function(){
                
                                        }
                                    }
                                }
                            });
                        }).fail(function (jqXHR, textStatus, errorThrown) {
                            alert(textStatus +': '+errorThrown);
                        }).always(function(data) {                
                        });
                    }
                },
                danger: {
                    text: "No",
                    btnClass: 'btn-red',
                    action: function () {
                        
                    }
                },
            }
        })
    });
});