// Función que valida los requerimientos de una ventana y retorna un mensaje o lo permite ingresar
function fncValidarRequerimientosjsn(action, strLocation) {
    $.ajax({
        url: "/modulo_configuracion",
        type: 'POST',
        data: {
            'action': action
        },
        dataType: 'json',
    }).done(function(data) {
        console.log(data);
        if(data.hasOwnProperty('error')){
            error = data.error;
            fncMensajeErrormns(error);
            return;
        }
        else{
            location.href = strLocation;
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus +': '+errorThrown);
    }).always(function(data) {                
    });
}

// Validación parametrización usuarios
$('#btnUsuarios').on('click', function (e) {
    e.preventDefault();
    fncValidarRequerimientosjsn('btnUsuariosPermisosjsn', '/configuracion/vista_usuarios')
});

// Validación parametrización productos
$('#btnCatalogoProductos').on('click', function (e) {
    e.preventDefault();
    fncValidarRequerimientosjsn('btnCatalogoProductosjsn', '/configuracion/product_catalogue/')
});

// Validación parametrización proveedores
$('#btnCatalogoProveedores').on('click', function (e) {
    e.preventDefault();
    fncValidarRequerimientosjsn('btnCatalogoProveedoresjsn', '/configuracion/cat_sup/')
});

// Validación parametrización bodegas
$('#btnCatalogoBodegas').on('click', function (e) {
    e.preventDefault();
    fncValidarRequerimientosjsn('btnCatalogoBodegasjsn', '/configuracion/catalogo_bodegas/')
});

// Validación parametrización listas de precios
$('#btnListasPrecios').on('click', function (e) {
    e.preventDefault();
    fncValidarRequerimientosjsn('btnListasPreciosjsn', '/configuracion/listas_precios/')
});

// Validación parametrización clientes
$('#btnCatalogoClientes').on('click', function (e) {
    e.preventDefault();
    fncValidarRequerimientosjsn('btnCatalogoClientesjsn', '/configuracion/cat_cli/')
});

// Validación parametrización tiempos de entrega
$('#btnTiemposEntrega').on('click', function (e) {
    e.preventDefault();
    fncValidarRequerimientosjsn('btnTiemposEntregajsn', '/configuracion/tiempos_entrega/')
});

// Validación parametrización historico movimientos
$('#btnHistoricoMovimientos').on('click', function (e) {
    e.preventDefault();
    fncValidarRequerimientosjsn('btnHistoricoMovimientosjsn', '/configuracion/importar_historico_movimientos/')
});

// Validación parametrización historico movimientos
$('#btnAjustesInventario').on('click', function (e) {
    e.preventDefault();
    fncValidarRequerimientosjsn('btnAjusteInventariosjsn', '/configuracion/ajustes_inventario/')
});