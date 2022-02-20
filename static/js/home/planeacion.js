// Validación parametrización usuarios
$('#userButton').on('click', function (e) {
    e.preventDefault();
    $.ajax({
        url: "/modulo_configuracion",
        type: 'POST',
        data: {
            'action': 'user'
        },
        dataType: 'json',
    }).done(function(data) {
        if(data.hasOwnProperty('error')){
            error = data.error;
            message_error(error);
        }
        else{
            location.href = '/configuracion/vista_usuarios';
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus +': '+errorThrown);
    }).always(function(data) {                
    });
});

// Validación parametrización productos
$('#productsButton').on('click', function (e) {
    e.preventDefault();
    $.ajax({
        url: "/modulo_configuracion",
        type: 'POST',
        data: {
            'action': 'products'
        },
        dataType: 'json',
    }).done(function(data) {
        if(data.hasOwnProperty('error')){
            error = data.error;
            message_error(error);
        }
        else{
            location.href = '/configuracion/product_catalogue/';
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus +': '+errorThrown);
    }).always(function(data) {                
    });
});

// Validación parametrización proveedores
$('#suppliersButton').on('click', function (e) {
    e.preventDefault();
    $.ajax({
        url: "/modulo_configuracion",
        type: 'POST',
        data: {
            'action': 'suppliers'
        },
        dataType: 'json',
    }).done(function(data) {
        if(data.hasOwnProperty('error')){
            error = data.error;
            message_error(error);
        }
        else{
            location.href = '/configuracion/cat_sup/';
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus +': '+errorThrown);
    }).always(function(data) {                
    });
});

// Validación parametrización clientes
$('#customersButton').on('click', function (e) {
    e.preventDefault();
    $.ajax({
        url: "/modulo_configuracion",
        type: 'POST',
        data: {
            'action': 'customers'
        },
        dataType: 'json',
    }).done(function(data) {
        if(data.hasOwnProperty('error')){
            error = data.error;
            message_error(error);
        }
        else{
            location.href = '/configuracion/cat_cli/';
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus +': '+errorThrown);
    }).always(function(data) {                
    });
});

// Validación parametrización bodegas
$('#warehouseButton').on('click', function (e) {
    e.preventDefault();
    $.ajax({
        url: "/modulo_configuracion",
        type: 'POST',
        data: {
            'action': 'warehouse'
        },
        dataType: 'json',
    }).done(function(data) {
        if(data.hasOwnProperty('error')){
            error = data.error;
            message_error(error);
        }
        else{
            location.href = '/configuracion/catalogo_bodegas/';
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus +': '+errorThrown);
    }).always(function(data) {                
    });
});

// Validación parametrización historico movimientos
$('#historicoMovimientosButton').on('click', function (e) {
    e.preventDefault();
    $.ajax({
        url: "/modulo_configuracion",
        type: 'POST',
        data: {
            'action': 'historico_movimientos'
        },
        dataType: 'json',
    }).done(function(data) {
        if(data.hasOwnProperty('error')){
            error = data.error;
            message_error(error);
        }
        else{
            location.href = '/configuracion/importar_historico_movimientos/';
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus +': '+errorThrown);
    }).always(function(data) {                
    });
});