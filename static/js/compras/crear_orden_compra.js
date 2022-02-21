var tblProducts;
var idCartera = '';
var product = '';
var id_prod = '';
var creditValue = '';

var purchase = {
    items: {
        sup_id: '',
        sup_name: '',
        sup_identification: '',
        sup_cel: '',
        sup_mail: '',
        //debt_status: '',
        order_date: '',
        order_city:'',
        order_address: '',
        //pay_method: '',
        //urgency_level:'',
        //deliver_date: '',
        //del_schedule: '',
        observation:'',
        subtotal: 0.00,
        iva: 00,
        dcto: 0.00,
        total: 0.00,
        products: []
    },
    get_prods_id: function () {
        var ids = [];
        $.each(this.items.products, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    add_prod: function (item) {
        this.items.products.push(item);
        this.list();
    },
    calculate_order: function () {
        var subtotal = 0.00;
        var iva = 0.00;
        var dcto = 0.00;
        var total = 0.00;
        cbDesc = $('.cbDesc').val();
        $.each(this.items.products, function (pos, dict) {
            subtotal += dict.subtotal;
            iva += (dict.cant * dict.cost_pu) * dict.iva
            dcto += (dict.cant * dict.cost_pu) * dict.desc
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
        this.calculate_order();
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
                { "data": "id"},
                { "data": "product_desc"},
                { "data": "purchase_unit.purchase_unit"},
                { "data": "cost_pu"},
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

// Cargar repo de proveedor
function formatRepoSupplier(repo) {
    if (repo.loading) {
        return repo.text;
    }
    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-12 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.supplier_name + '<br>' +
        '<b>Id:</b> ' + repo.identification + '<br>' +
        '<b>Contacto:</b> ' + repo.contact_name + '<br>' +
        '<b>Celular:</b> ' + repo.contact_cel + '<br>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

// Cargar repo de productos
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
        '<b>Nombre:</b> ' + repo.product_desc + '<br>' +
        '<b>Código:</b> ' + repo.id + '<br>' +
        '<b>Presentación:</b> ' + repo.presentation + '<br>' +
        '<b>Precio:</b> <span class="badge badge-warning">$'+repo.cost_pu+'</span>'+
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function(){

    // Cargar libreria select2
    $('.select2').select2({                                                                                                                                                                                                                                                                                                                                         
        theme: "bootstrap4",
        language: 'es'
    });

    // Buscador de proveedor
    $('#identification').select2({
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
                    action: 'search_supplier'
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
        templateResult: formatRepoSupplier,

    // Seleccionar proveedor
    }).on('select2:select', function (e) {
        var data = e.params.data;
        purchase.items.sup_id = data.id;
        purchase.items.sup_name = data.supplier_name;
        purchase.items.sup_identification = data.identification;
        purchase.items.sup_cel = data.contact_cel;
        purchase.items.sup_mail = data.email;
        purchase.items.order_city = data.city.name;
        purchase.items.order_address = data.supplier_address;
        $('#supplierData').attr('hidden', false)
        $('#supId').val(data.identification);
        $('#supCel').val(data.contact_cel);
        $('#supMail').val(data.email);
        $('#supCity').val(data.city.name);
        $('#delivery_address').val(data.supplier_address);
        debt = data.pay_method.name;
        id_customer = data.id;
        if(debt == 'Crédito' ){
            credit_value = data.credit_limit;
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action':'supplier_debt',
                    'id': id_customer,
                    'credit_value': credit_value
                },
                dataType: 'json',
            }).done(function(data) {
                if (!data.hasOwnProperty('msg')){
                    $('#supplierDebt').attr('hidden', false)
                    $('#debtStatus').val(data.cartera[0])
                    $('#creditValue').val('$ ' + data.cartera[1])
                    creditValue = data.cartera[1]
                    $('#minPay').val('$ ' + data.cartera[2])
                    $('#totalPay').val('$ ' + data.cartera[3])
                    Swal.fire({
                        icon: 'warning',
                        html: data.cartera[4],
                        showConfirmButton: false,
                        timer: 2500
                    });
                }else if(data.hasOwnProperty('msg')){
                    $('#supplierDebt').attr('hidden', false)
                    $('#stateCart').val(data.state)
                    $('#creditValue').val('$ ' + data.credit_value)
                    creditValue = data.credit_value
                    $('#minPay').val('$ ' + 0)
                    $('#totalPay').val('$ '+ 0)
                    $('#pay_method').val('CR')
                    Swal.fire({
                        icon: 'warning',
                        html: data.msg,
                        showConfirmButton: false,
                        timer: 2500
                    });
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus +': '+errorThrown);
            }).always(function(data) {                
            });
        }
    }).on('select2:unselect', function (e) {
        $('#supId').val('');
        $('#supCel').val('');
        $('#supMail').val('');
        $('#supCity').val('');
        $('#delivery_address').val('');
        $('#supplierData').attr('hidden', true)
        $('#addProds').collapse("hide");
        $('#debtStatus').val('');
        $('#creditValue').val('');
        $('#minPay').val('');
        $('#totalPay').val('');
        $('#supplierDebt').attr('hidden', true)
    });

    // Abrir modal creación proveedor
    $('.addSup').on('click', function () {
        $('#modalSupplier').modal('show');
    });

    // Borrar lo digitado en el formulario cliente
    $('#modalSupplier').on('hidden.bs.modal', function (e) {
        $('#formSupplier').trigger('reset');
    });

    // Guardar el registro de cliente
    $('#formSupplier').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_supplier');
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                var newOption = new Option(response.name, false, true);
                $('#identification').append(newOption).trigger('change');
                $('#modalSupplier').modal('hide');
            });
    });

    // Cargar libreria datetimepicker a fecha de venta
    $('#order_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD"),
        maxDate: moment().format("YYYY-MM-DD"),
    });
    
    purchase.items.order_date = $('#order_date').val();

    // Cargar libreria datetimepicker a fecha de entrega
    $('#delivery_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD"),
    });

    // Cargar libreria touchspin para input cantidad
    $("#quantityPurchase").TouchSpin({
        min: 1,
        step: 1,
    }).val(1)
    
    // Activar botón 'agregar productos'
    $('.btnAddProd').on('click', function () {
        sup = $('#identification').val();
        debt = $('#debtStatus').val();
        if(sup == ''){
            fncMensajeInformacionmns('Debe ingresar un proveedor a la orden');
            $('#identification').select2('focus');
            return false;
        }else if(debt == 'Vencida'){
            fncMensajeInformacionmns('El cliente presenta una cartera vencida');
            return false;
        }else{
            $('#searchProd').select2('focus');
        }
    });
    
    // Buscador de productos
    $('#searchProd').select2({
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
                    ids: JSON.stringify(purchase.get_prods_id())
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
        products = purchase.get_prods_id();
        if (products.length > 0){
            $.each(products, function (pos, value) {
                if(id_prod == value){
                    $.confirm({
                        title: 'Alerta',
                        content: '¿El producto ya se registro, desea modificarlo?',
                        buttons: {
                            Si: function () {
                                purchase.items.products.splice(pos, 1);
                                $('input[name="cod"]').val(data.id);
                                $('input[name="nameProd"]').val(data.product_desc);
                                $('input[name="pres"]').val(data.presentation);
                                $('input[name="udv"]').val(data.sales_unit.sales_unit);
                                $('input[name="uniPrice"]').val('$ ' + parseFloat(data.full_sale_price).toFixed(2));
                                $('input[name="ivaProd"]').val(parseFloat(data.iva).toFixed(2) + ' %');
                                if(data.saldos_inv.length > 0){
                                    $('#quantityBalance').val(data.saldos_inv[0].inventory_balance);
                                }
                                $('#searchProd').val('').trigger('change.select2');
                                data.cant = 1;
                                data.subtotal = 0.00;
                                data.desc = 0.00;
                                data.total = 0.00;
                                product = data;
                                purchase.list();
                                $('#quantityPurchase').focus();
                            },
                            Cancelar: function () {
                                $('#searchProd').val('').trigger('change.select2');
                                $('#searchProd').select2('open');
                            }
                        }
                    });
                } else if(id_prod != value){
                $('input[name="cod"]').val(data.id);
                $('input[name="nameProd"]').val(data.product_desc);
                $('input[name="pres"]').val(data.presentation);
                $('input[name="udv"]').val(data.sales_unit.sales_unit);
                $('input[name="uniPrice"]').val('$ ' + parseFloat(data.full_sale_price).toFixed(2));
                $('input[name="ivaProd"]').val(parseFloat(data.iva).toFixed(2) + ' %');
                if(data.saldos_inv.length > 0){
                    $('#quantityBalance').val(data.saldos_inv[0].inventory_avail);
                }
                $('#searchProd').val('').trigger('change.select2');
                data.cant = 1;
                data.subtotal = 0.00;
                data.desc = 0.00;
                data.total = 0.00;
                product = data;
                purchase.list();
                $('#quantityPurchase').focus();
                }
            });
        }
        else if (products.length == 0){
            $('input[name="cod"]').val(data.id);
            $('input[name="nameProd"]').val(data.product_desc);
            $('input[name="pres"]').val(data.presentation);
            $('input[name="udv"]').val(data.sales_unit.sales_unit);
            $('input[name="uniPrice"]').val('$ ' + parseFloat(data.full_sale_price).toFixed(2));
            $('input[name="ivaProd"]').val(parseFloat(data.iva).toFixed(2) + ' %');
            if(data.saldos_inv.length > 0){
                $('#quantityBalance').val(data.saldos_inv[0].inventory_avail);
            }
            $(this).val('').trigger('change.select2');
            $('#quantityPurchase').focus();
            data.cant = 1;
            data.subtotal = 0.00;
            data.desc = 0.00;
            data.total = 0.00;
            product = data;
            purchase.list();
        }
    });
    
    // Activar botón agregar producto
    $('.btnAddP').on('click', function () {
        if (product == ''){
            fncMensajeInformacionmns('Ingrese un producto');
            $('#searchProd').focus();
            return false;
        }
        cant = $('#quantityPurchase').val(); 
        product.cant = cant;
        product.subtotal = product.cant * product.cost_pu;
        product.cost_pu = parseFloat(product.cost_pu);
        product.iva = parseFloat(product.iva)/100;
        product.total = product.subtotal + product.iva + product.desc
        $('input[name="cod"]').val('');
        $('input[name="nameProd"]').val('');
        $('input[name="pres"]').val('');
        $('input[name="udv"]').val('');
        $('input[name="uniPrice"]').val('');
        $('input[name="ivaProd"]').val('');
        $('#descProd').val(0);
        $('#quantityBalance').val('');
        $('#quantityPurchase').val(1);
        purchase.add_prod(product);
        purchase.calculate_order();
        product = '';
    });
    
    // Checkbutton para establecer descuentos
    $('.cbDesc').on('click', function () {
        cbDesc = parseInt($('.cbDesc').val());
        dcto = purchase.items.dcto;
        if(cbDesc == 0){
            if(purchase.items.products.length === 0){
                fncMensajeInformacionmns('Agregue al menos un producto para aplicar el descuento')
                return false;
            } else {
                $('.cbDesc').val(1);
                fncMensajeInformacionmns('ingrese el % de descuento que desea aplicar')
                $('#inpDesc').attr('disabled', false);
                $('#inpDesc').focus();
            }
        } else if (cbDesc == 1){
            $('.cbDesc').val(0);
            $('#inpDesc').val(0)
            $('#inpDesc').attr('disabled', true);
            $('input[name="discount"]').val('$ 0');
            purchase.calculate_order();
        }
    });

    // Cargar TouchSpin para descuento por producto
    $("#descProd").TouchSpin({
        min: 0,
        max: 100,
        step: 1,
        decimals: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
    }).val(0);

    // TouchSpin y función para descuento por compra
    $("#inpDesc").TouchSpin({
        min: 0,
        max: 100,
        step: 1,
        decimals: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
    }).on('change', function (){
        subtotal = purchase.items.subtotal;
        desGen = $("#inpDesc").val()/100;
        desc = parseFloat(subtotal * desGen).toFixed(2);
        purchase.items.dcto = desc;
        $('input[name="discount"]').val('$ ' + desc);
    }).val(0.00)

    // Activar botón 'eliminar productos'
    $('.btnRemoveAll').on('click', function () {
        if(purchase.items.products.length === 0) 
        return false;
        alert_action('Notificación', '¿Está seguro de eliminar todos los productos?', function () {
            purchase.items.products = [];
            purchase.list();
        });
    });
    
    // Eventos de la tabla
    $('#tblProducts tbody')
        //Eliminar un producto de la tabla
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Está seguro de eliminar el producto?', function () {
                purchase.items.products.splice(tr.row, 1);
                purchase.list();
            });
        })        
        //Calcular cantidades de la tabla
        .on('change', 'input[name="cant"]', function () {
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            sales.items.products[tr.row].cant = cant;
            sales.items.products[tr.row].subtotal = cant * sales.items.products[tr.row].price_udv
            sales.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + sales.items.products[tr.row].subtotal.toFixed(2));
    });

    // Función para generar pedido
    $('.genOrder').on('click', function (e) {
        e.preventDefault();
        if(purchase.items.products.length === 0 ){
            fncMensajeErrormns('Debe agregar al menos un producto a la orden ')
            return false;
        }else{
            $('#addProds').collapse('hide');
        }
    });

    // event submit form
    $('#frmOrder').on('submit', function (e) {
        e.preventDefault();
        pay_method = $('#pay_method').val();
        if(pay_method == 'CR' ){
            if(sales.items.total > creditValue){
                $.confirm({
                    animation: 'Rotate',
                    closeAnimation: 'scale',
                    columnClass: 'col-md-9',
                    icon: 'fa fa-save',
                    title: 'Confirmación',
                    content: 'El cupo disponible de credito ($ '+ credit_value +') excede el total del pedido ($ '+ sales.items.total +') seleccione una opción',
                    buttons: {
                        Generar: {
                            text: 'Pagar excedente de pedido en contado',
                            btnClass: 'btn-green',
                            action: function () {
                                sales.items.order_date = $('#order_date').val();
                                sales.items.deliver_date = $('input[name="deliver_date"]').val();
                                sales.items.deliver_hour = $('#deliver_hour').val();
                                sales.items.urgency_level = $('#urgency_level').val();
                                sales.items.pay_method = pay_method;
                                sales.items.order_address = $('input[name="order_address"]').val();
                                sales.items.observation = $('textarea[name="obs"]').val();
                                var parameters = new FormData();
                                parameters.append('action', $('input[name="action"]').val());
                                parameters.append('sales', JSON.stringify(sales.items));
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
                                        content: 'Se ha generado el pedido Nº 000'+ response.id + ', por favor seleccione una opción',
                                        buttons: {
                                            Generar: {
                                                text: 'Generar PDF',
                                                btnClass: 'btn-green',
                                                action: function () {
                                                    window.open('/comercial/sale/invoice/pdf/' + response.id + '/', '_blank');
                                                    location.href = '/comercial/lista_pedidos/';
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
                            },
                        },
                        Cancelar: {
                            text: 'Modificar pedido',
                            btnClass: 'btn-red',
                            action: function(){
                                
                            }
                        }
                    }
                });
            return false;
            }        
        }else{
            sales.items.order_date = $('#order_date').val();
            sales.items.deliver_date = $('input[name="deliver_date"]').val();
            sales.items.deliver_hour = $('#deliver_hour').val();
            sales.items.urgency_level = $('#urgency_level').val();
            sales.items.pay_method = pay_method;
            sales.items.order_address = $('input[name="order_address"]').val();
            sales.items.observation = $('textarea[name="obs"]').val();
            var parameters = new FormData();
            parameters.append('action', $('input[name="action"]').val());
            parameters.append('sales', JSON.stringify(sales.items));
            $.confirm({
                theme: 'material',
                title: 'Confirmaciòn',
                icon: 'fa fa-bell',
                content: '¿Está seguro de generar la orden?',
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
                                    content: 'Se ha generado la orden de compra Nº 000'+ response.id + ', por favor seleccione una opción',
                                    buttons: {
                                        Generar: {
                                            text: 'Generar PDF',
                                            btnClass: 'btn-green',
                                            action: function () {
                                                window.open('/comercial/sale/invoice/pdf/' + response.id + '/', '_blank');
                                                location.href = '/comercial/lista_pedidos/';
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
            
            });
        }
    });
});