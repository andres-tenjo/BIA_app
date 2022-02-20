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

// Cargar repo de bodegas
function formatRepoWarehouse(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-12 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Bodega:</b> ' + repo.warehouse_name + '<br>' +
        '<b>Responsable: </b>' + repo.contact_name + '<br>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

// Diccionario que almacena las funciones y variables de la ventana
dctAjustesInventario = {
    
    // Diccionario de variables
    dctVariables: {
        intIdBodega: '',
        strBodega: '',
        strTipoAjusteId: '',
        strTipoAjuste: '',
        intIdProducto:'',
        strProducto:'',
        strLote: '',
        datFechaVencimiento: '',
        intCantidad:'',
        fltCostoUnitario:'',
        fltCostoTotalUnitario:'',
    },

    dctLstAjustesInventario: {
        lstAjustesInventario: [],
        fltCostoTotal: 0.00
    },

    // Función para ontener ids lista   
    fncObtenerIdsProductoslst: function () {
        return this.lstAjustesInventario.map(value => value.id);
    },

    // Función para calcular el costo total unitario del producto que se agregara a la tabla
    fncCalcularCostoTotalUnitario: function () {
        var fltCostoTotalUnitario = 0.00;
        const intCantidad = document.getElementById('quantity');
        const fltCostoUnitario = document.getElementById('costoUnitario');
        const fltCostototal = document.getElementById('total_cost');
        fltCostoTotalUnitario = intCantidad.value * this.dctVariables.fltCostoUnitario;
        this.dctVariables.fltCostoTotalUnitario = fltCostoTotalUnitario;
        fltCostoUnitario.value = '$ ' + parseFloat(this.dctVariables.fltCostoUnitario).toFixed(2);
        fltCostototal.value = '$ ' + parseFloat(this.dctVariables.fltCostoTotalUnitario).toFixed(2);
    },

    // Función para calcular el costo total acumulado de los productos agregados a la tabla
    fncCalcularCostoTotalAcumulado: function () {
        const fltInputCostoTotal = document.getElementById('costoTotalAcumulado');
        var fltCostoTotal = 0.00;
        $.each(this.dctLstAjustesInventario.lstAjustesInventario, function (pos, dict) {
            fltCostoTotal += dict.fltCostoTotalUnitario;
        });
        this.dctLstAjustesInventario.fltCostoTotal = fltCostoTotal;
        fltInputCostoTotal.value = '$ ' + this.dctLstAjustesInventario.fltCostoTotal;
    },
}

$(function () {

    // Buscar bodega
    $('#store').select2({
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
                    action: 'jsnBuscarBodega',
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
        templateResult: formatRepoWarehouse,
    }).on('select2:select', function (e) {
        dctAjustesInventario.dctVariables.intIdBodega = e.params.data.id;
        dctAjustesInventario.dctVariables.strBodega = e.params.data.warehouse_name;;
    });
    
    // Buscar producto
    $('#product_code').select2({
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
                    action: 'jsnBucarProducto',
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
        var dctData = e.params.data;
        dctAjustesInventario.dctVariables.intIdProducto = dctData.id;
        dctAjustesInventario.dctVariables.strProducto = dctData.product_desc;
        dctAjustesInventario.dctVariables.fltCostoUnitario = dctData.cost_pu;
        $('#filaDescripcionProducto').prop('hidden', false);
        const strUnidadCompra = document.getElementById('unidadCompra');
        strUnidadCompra.value = dctData.purchase_unit.purchase_unit;
        dctAjustesInventario.fncCalcularCostoTotalUnitario();
    });
    
    // Datetimepicker fecha de vencimiento
    $('#expiration_date').datetimepicker({
        format: 'DD/MM/YYYY',
        locale: 'es',
    });

    // Touchspin cantidad
    $(".touchNumber").TouchSpin({
        min: 0,
        max: 10000000,
        step: 1,
    }).on('change', function (){
        dctAjustesInventario.fncCalcularCostoTotalUnitario();
    }).val(1)
    
    // Agregar producto a tabla 
    $('#frm').on('submit', function (e) {
        e.preventDefault();
        const strInputTypeId = $('#type :selected').text();
        const strInputType = document.getElementById('type');
        const strInputLote = document.getElementById('batch');
        const datInputDatFechaVencimiento = document.getElementById('expiration_date');
        const intInputCantidad = document.getElementById('quantity');
        const strUnidadCompra = document.getElementById('unidadCompra');
        const fltCostoUnitario = document.getElementById('costoUnitario');
        const fltCostoTotalUnitario = document.getElementById('total_cost');
        dctAjustesInventario.dctVariables.strTipoAjusteId = strInputType.value;
        dctAjustesInventario.dctVariables.strTipoAjuste = strInputTypeId;
        dctAjustesInventario.dctVariables.strLote = strInputLote.value;
        dctAjustesInventario.dctVariables.datFechaVencimiento = datInputDatFechaVencimiento.value;
        dctAjustesInventario.dctVariables.intCantidad = intInputCantidad.value;
        var parameters = new FormData();
        parameters.append('action', 'jsnValidarAjuste');
        parameters.append('dctVariables', JSON.stringify(dctAjustesInventario.dctVariables));
        parameters.append('dctLstAjustesInventario', JSON.stringify(dctAjustesInventario.dctLstAjustesInventario));
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataType: 'json',
            processData: false,
            contentType: false,
        }).done(function(data) {
            if (!data.hasOwnProperty('error')){
                dctAjustesInventario.dctLstAjustesInventario.lstAjustesInventario.push(dctAjustesInventario.dctVariables)
                $('#tblAjustesInventario').DataTable().clear().rows.add(dctAjustesInventario.dctLstAjustesInventario.lstAjustesInventario).draw();
                dctAjustesInventario.dctVariables = {
                    intIdBodega: '',
                    strBodega: '',
                    strTipoAjusteId: '',
                    strTipoAjuste: '',
                    intIdProducto:'',
                    strProducto:'',
                    strLote: '',
                    datFechaVencimiento: '',
                    intCantidad:'',
                    fltCostoUnitario:'',
                    fltCostoTotalUnitario:'',
                }
                $('#store').val("").trigger("change");
                strInputType.value = '';
                $('#product_code').val("").trigger("change");
                strInputLote.value = '';
                datInputDatFechaVencimiento.value = '';
                intInputCantidad.value = 0;
                strUnidadCompra.value = '';
                fltCostoUnitario.value = '';
                fltCostoTotalUnitario.value = '';
                dctAjustesInventario.fncCalcularCostoTotalAcumulado();
            }
            else if(data.hasOwnProperty('error')){
                dctAjustesInventario.dctVariables = {
                    intIdBodega: '',
                    strBodega: '',
                    strTipoAjusteId: '',
                    strTipoAjuste: '',
                    intIdProducto:'',
                    strProducto:'',
                    strLote: '',
                    datFechaVencimiento: '',
                    intCantidad:'',
                    fltCostoUnitario:'',
                    fltCostoTotalUnitario:'',
                }
                $('#store').val("").trigger("change");
                strInputType.value = '';
                $('#product_code').val("").trigger("change");
                strInputLote.value = '';
                datInputDatFechaVencimiento.value = '';
                intInputCantidad.value = 0;
                strUnidadCompra.value = '';
                fltCostoUnitario.value = '';
                fltCostoTotalUnitario.value = '';
                message_error(data.error);
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus +': '+errorThrown);
        }).always(function(data) {                
        });
        
    });

    var tblAjustesInventario = $('#tblAjustesInventario').DataTable({
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
        data: dctAjustesInventario.dctLstAjustesInventario.lstAjustesInventario,
        columns: [
            { "data": "strBodega"},
            { "data": "strTipoAjuste"},
            { "data": "strProducto"},
            { "data": "strLote"},
            { "data": "datFechaVencimiento"},
            { "data": "intCantidad"},
            { "data": "fltCostoTotalUnitario"},
            { "data": "fltCostoTotalUnitario"},
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
                    var buttons = '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-undo-alt"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings, json) {
        }
    });
    // Eliminar un producto del listado de productos
    $('#tblAjustesInventario tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblAjustesInventario.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Está seguro de eliminar el producto?', function () {
                dctAjustesInventario.dctLstAjustesInventario.lstAjustesInventario.splice(tr.row, 1);
                $('#tblAjustesInventario').DataTable().clear().rows.add(dctAjustesInventario.dctLstAjustesInventario.lstAjustesInventario).draw();
        });
    });
    
    // Boton eliminar productos de la tabla
    $('#btnRemoverProductos').on('click', function () {
        if(dctAjustesInventario.dctLstAjustesInventario.lstAjustesInventario.length === 0) return false;
        alert_action('Notificación', '¿Está seguro de eliminar todos los productos?', function () {
            dctAjustesInventario.dctLstAjustesInventario.lstAjustesInventario = [];
            $('#tblAjustesInventario').DataTable().clear().rows.add(dctAjustesInventario.dctLstAjustesInventario.lstAjustesInventario).draw();
        });
    }); 

    // Guardar ajuste
    $('#guardarAjusteInventario').on('click', function (e) {
        e.preventDefault();
        var parameters = new FormData();
        parameters.append('action', 'jsnGuardarAjuste');
        parameters.append('dctLstAjustesInventario', JSON.stringify(dctAjustesInventario.dctLstAjustesInventario));
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataType: 'json',
            processData: false,
            contentType: false,
        }).done(function(data) {
            if (data.hasOwnProperty('msg')){
                $.confirm({
                    columnClass: 'col-md-12',
                    title: 'Felicidades',
                    icon: 'fas fa-clipboard-check',
                    content: data.msg,
                    theme: 'supervan',
                    buttons: {
                        Aceptar: function () {
                            location.reload();
                        }
                    }
                });            
            }
            else if(data.hasOwnProperty('error')){
                message_error(data.error);
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus +': '+errorThrown);
        }).always(function(data) {                
        }); 
    });

});