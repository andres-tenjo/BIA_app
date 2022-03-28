// Diccionario de planeación comercial
dctPlaneacionComercial = {
    
    // Diccionario con listas que contienen la data para el indicador de venta total
    dctIndicadorVentaTotal:{
        lstCategorias: [],
        lstSeries: [],
    },
    
    // Diccionario con listas que contienen la data para el indicador de ventas nuevas
    dctIndicadorVentasNuevas:{
        lstCategorias: [],
        lstSeries: [],
    },
    
    // Diccionario con listas que contienen la data para el indicador de profundización de clientes
    dctIndicadorProfundizacionClientes:{
        lstCategorias: [],
        lstSeries: [],
    },
    
    // Diccionario con listas que contienen la data para el indicador de clientes nuevos
    dctIndicadorClientesNuevos:{
        lstCategorias: [],
        lstSeries: [],
    },
    
    // Diccionario con listas que contienen la data para el indicador de margén de venta
    dctIndicadorMargenVenta:{
        lstCategorias: [],
        lstSeries: [],
    },

    // Diccionario con listas que contienen la data para el indicador detallado de ciudad
    dctIndicadoresCiudades:{
        bolCollapseCiudad: false,
        lstCiudades: [],
        lstCategoriasGraficoCiudad: [],
        lstSeriesCiudades: [],
        lstTablaCiudades: []
    },

    // Diccionario con listas que contienen la data para el indicador detallado de zona
    dctIndicadoresZonas:{
        bolCollapseZona: false,
        lstZonas: [],
        lstCategoriasGraficoZonas: [],
        lstSeriesZonas: [],
        lstTablaZonas: []
    },
    
    // Diccionario con listas que contienen la data para el indicador detallado de categoria cliente
    dctIndicadoresCategoriaCliente:{
        bolCollapseCategoriaCliente: false,
        lstCategoriaCliente: [],
        lstCategoriasGraficoCategoriaCliente: [],
        lstSeriesCategoriaCliente: [],
        lstTablaCategoriaCliente: []
    },
    
    // Diccionario con listas que contienen la data para el indicador detallado de asesores comerciales
    dctIndicadoresAsesorComercial:{
        bolCollapseAsesorComercial: false,
        lstAsesoresComerciales: [],
        lstCategoriasGraficoAsesorComercial: [],
        lstSeriesAsesorComercial: [],
        lstTablaAsesorComercial: []
    },

    // Función que carga el gráfico para el indicador de venta total
    fncIndicadorVentaTotalgrf: function () {
        Highcharts.chart('grfVentaMensual', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Indicador de venta total'
            },
            xAxis: {
                categories: dctPlaneacionComercial.dctIndicadorVentaTotal.lstCategorias
            },
            yAxis: {
                title: {
                    text: 'Millones de pesos ($)'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: dctPlaneacionComercial.dctIndicadorVentaTotal.lstSeries
        });
    },
    
    // Función que carga el gráfico para el indicador de ventas nuevas
    fncIndicadorVentasNuevasgrf: function () {
        Highcharts.chart('grfVentasNuevas', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Indicador de ventas nuevas'
            },
            xAxis: {
                categories: dctPlaneacionComercial.dctIndicadorVentasNuevas.lstCategorias
            },
            yAxis: {
                title: {
                    text: 'Millones de pesos ($)'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: dctPlaneacionComercial.dctIndicadorVentasNuevas.lstSeries
        });
    },
    
    // Función que carga el gráfico para el indicador de profundización de clientes
    fncIndicadorProfundizacionClientesgrf: function () {
        Highcharts.chart('grfProfundizacionClientes', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Indicador de profundización de clientes'
            },
            xAxis: {
                categories: dctPlaneacionComercial.dctIndicadorProfundizacionClientes.lstCategorias
            },
            yAxis: {
                title: {
                    text: 'Millones de pesos ($)'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: dctPlaneacionComercial.dctIndicadorProfundizacionClientes.lstSeries
        });
    },
    
    // Función que carga el gráfico para el indicador de profundización de clientes
    fncIndicadorClientesNuevosgrf: function () {
        Highcharts.chart('grfClientesNuevos', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Indicador de clientes nuevos'
            },
            xAxis: {
                categories: dctPlaneacionComercial.dctIndicadorClientesNuevos.lstCategorias
            },
            yAxis: {
                title: {
                    text: 'Millones de pesos ($)'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: dctPlaneacionComercial.dctIndicadorClientesNuevos.lstSeries
        });
    },

    // Función que carga el gráfico para el indicador de margén de venta
    fncIndicadorMargenVentagrf: function () {
        Highcharts.chart('grfMargenVenta', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Indicador de margén de venta'
            },
            xAxis: {
                categories: dctPlaneacionComercial.dctIndicadorMargenVenta.lstCategorias
            },
            yAxis: {
                title: {
                    text: 'Millones de pesos ($)'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: dctPlaneacionComercial.dctIndicadorMargenVenta.lstSeries
        });
    },
    
    // Función que carga el gráfico para el indicador por filtro de ciudad
    fncIndicadorCiudadgrf: function () {
        Highcharts.chart('grfCiudad', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Indicador por ciudad'
            },
            xAxis: {
                categories: dctPlaneacionComercial.dctIndicadoresCiudades.lstCategoriasGraficoCiudad
            },
            yAxis: {
                title: {
                    text: 'Millones de pesos ($)'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: dctPlaneacionComercial.dctIndicadoresCiudades.lstSeriesCiudades
        });
    },

    // Tabla indicadores por ciudad
    fncIndicadoresCiudadtbl: function () {
        tblIndicadorCiudad = $('#tblIndicadorCiudad').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: false,
            info: false,
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
            data: dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades,
            columns: [
                { "data": "strIndicador"},
                { "data": "strSubset"},
                { "data": "fltObjetivoIndicador"},
                { "data": "fltObjetivoIndicador"},
            ],
            columnDefs: [
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    orderable: true,
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: true,
                    render: function (data, type, row) {
                        return '$ '+ parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat" title="Editar unidad compra"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-trash"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });
    },
    
    // Función que carga el gráfico para el indicador por filtro de zona
    fncIndicadorZonagrf: function () {
        Highcharts.chart('grfZona', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Indicador por zona'
            },
            xAxis: {
                categories: dctPlaneacionComercial.dctIndicadoresZonas.lstCategoriasGraficoZonas
            },
            yAxis: {
                title: {
                    text: 'Millones de pesos ($)'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: dctPlaneacionComercial.dctIndicadoresZonas.lstSeriesZonas
        });
    },

    // Tabla indicadores por zona
    fncIndicadoresZonatbl: function () {
        tblIndicadorZona = $('#tblIndicadorZona').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: false,
            info: false,
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
            data: dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas,
            columns: [
                { "data": "strIndicador"},
                { "data": "strSubset"},
                { "data": "fltObjetivoIndicador"},
                { "data": "fltObjetivoIndicador"},
            ],
            columnDefs: [
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    orderable: true,
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: true,
                    render: function (data, type, row) {
                        return '$ '+ parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat" title="Editar unidad compra"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-trash"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });
    },
    
    // Función que carga el gráfico para el indicador por filtro de categoria cliente
    fncIndicadorCategoriaClientegrf: function () {
        Highcharts.chart('grfCategoriaCliente', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Indicador por categoría cliente'
            },
            xAxis: {
                categories: dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriasGraficoCategoriaCliente
            },
            yAxis: {
                title: {
                    text: 'Millones de pesos ($)'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstSeriesCategoriaCliente
        });
    },

    // Tabla indicadores por categoría cliente
    fncIndicadoresCategoriaClientetbl: function () {
        tblIndicadorCategoriaCliente = $('#tblIndicadorCategoriaCliente').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: false,
            info: false,
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
            data: dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstTablaCategoriaCliente,
            columns: [
                { "data": "strIndicador"},
                { "data": "strSubset"},
                { "data": "fltObjetivoIndicador"},
                { "data": "fltObjetivoIndicador"},
            ],
            columnDefs: [
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    orderable: true,
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: true,
                    render: function (data, type, row) {
                        return '$ '+ parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat" title="Editar unidad compra"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-trash"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });
    },
    
    // Función que carga el gráfico para el indicador por filtro de asesor comercial
    fncIndicadorAsesorComercialgrf: function () {
        Highcharts.chart('grfAsesorComercial', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Indicador por asesor comercial'
            },
            xAxis: {
                categories: dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstCategoriasGraficoAsesorComercial
            },
            yAxis: {
                title: {
                    text: 'Millones de pesos ($)'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstSeriesAsesorComercial
        });
    },

    // Tabla indicadores por asesor comercial
    fncIndicadoresAsesorComercialtbl: function () {
        tblIndicadorAsesorComercial = $('#tblIndicadorAsesorComercial').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: false,
            info: false,
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
            data: dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstTablaAsesorComercial,
            columns: [
                { "data": "strIndicador"},
                { "data": "strSubset"},
                { "data": "fltObjetivoIndicador"},
                { "data": "fltObjetivoIndicador"},
            ],
            columnDefs: [
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    orderable: true,
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: true,
                    render: function (data, type, row) {
                        return '$ '+ parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href ="#" rel="edit" class="btn btn-success btn-xs btn-flat" title="Editar unidad compra"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat" title="Cambiar estado"><i class="fas fa-trash"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });
    },
}

$(function () {
    
    // Ejecutar funciones de librerias
    fncCargarLibreriaTouchSpinFormatoEntero();
    fncCargarLibreriaTouchSpinFormatoDecimal();
    fncCargarLibreriaTouchSpinFormatoMoneda();

    // Función que ejcuta una petición ajax para un indicador y una ciudad especifica y retorna la data con el gráfico si existe
    function fncRetornarDataGraficoCiudad() {
        var intIndicadorCiudad = $('#slcIndicadorCiudad').val();
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'slcIndicadorCiudadjsn');
        jsnParametros.append('intCiudad', $('#slcCiudad').val());
        jsnParametros.append('strIndicadorCiudad', $('#slcIndicadorCiudad').val());
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                dctPlaneacionComercial.dctIndicadoresCiudades.lstCategoriasGraficoCiudad = []
                dctPlaneacionComercial.dctIndicadoresCiudades.lstSeriesCiudades = []
                if(request != false){
                    dctPlaneacionComercial.dctIndicadoresCiudades.lstCategoriasGraficoCiudad = request[0];
                    dctPlaneacionComercial.dctIndicadoresCiudades.lstSeriesCiudades = request[1]
                    dctPlaneacionComercial.fncIndicadorCiudadgrf();
                    $('#rowGraficoCiudad').attr('hidden', false);
                }
                if(intIndicadorCiudad == 'Total_Sales_Objetive'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades, function (pos, value) {
                            if(value.intIndicador == 'Total_Sales_Objetive'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneral').attr('hidden', false);
                    $('#iptMetaGeneralCiudad').val($('#iptVentaTotal').val());
                    $('#iptMetaAcumuladaCiudad').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteCiudad').val(parseFloat($('#iptVentaTotal').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoCiudad').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100000000000000,
                        decimals: 2,
                        step: 0.01,
                        prefix: '$',
                        postfix: ''
                    });
                    return;
                }
                else if(intIndicadorCiudad == 'Customer_Retention_Rate'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades, function (pos, value) {
                            if(value.intIndicador == 'Customer_Retention_Rate'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneral').attr('hidden', false);
                    $('#iptMetaGeneralCiudad').val($('#iptVentasNuevas').val());
                    $('#iptMetaAcumuladaCiudad').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteCiudad').val(parseFloat($('#iptVentasNuevas').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoCiudad').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100000000000000,
                        decimals: 2,
                        step: 0.01,
                        prefix: '$',
                        postfix: ''
                    });
                    return;
                }
                else if(intIndicadorCiudad == 'Sales_Deepening'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades, function (pos, value) {
                            if(value.intIndicador == 'Sales_Deepening'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneral').attr('hidden', false);
                    $('#iptMetaGeneralCiudad').val($('#iptProfundizacionClientes').val());
                    $('#iptMetaAcumuladaCiudad').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteCiudad').val(parseFloat($('#iptProfundizacionClientes').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoCiudad').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100000000000000,
                        decimals: 2,
                        step: 0.01,
                        prefix: '$',
                        postfix: ''
                    });
                    return;
                }
                else if(intIndicadorCiudad == 'New_Customers'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades, function (pos, value) {
                            if(value.intIndicador == 'New_Customers'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneral').attr('hidden', false);
                    $('#iptMetaGeneralCiudad').val($('#iptClientesNuevos').val());
                    $('#iptMetaAcumuladaCiudad').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteCiudad').val(parseFloat($('#iptClientesNuevos').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoCiudad').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 10000000,
                        step: 1,
                        decimals: 0,
                        prefix:'Nº',
                        postfix: ''
                    });
                    return; 
                }
                else if(intIndicadorCiudad == 'Margin'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades, function (pos, value) {
                            if(value.intIndicador == 'Margin'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneral').attr('hidden', false);
                    $('#iptMetaGeneralCiudad').val($('#iptMargenVenta').val());
                    $('#iptMetaAcumuladaCiudad').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteCiudad').val(parseFloat($('#iptMargenVenta').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoCiudad').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100,
                        step: 0.01,
                        decimals: 2,
                        prefix:'',
                        postfix: '%'
                    });
                    return;
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });    
    }

    // Función que ejcuta una petición ajax para un indicador y una zona especifica y retorna la data con el gráfico si existe
    function fncRetornarDataGraficoZona() {
        var intIndicadorZona = $('#slcIndicadorZona').val();
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'slcIndicadorZonajsn');
        jsnParametros.append('intZona', $('#slcZona').val());
        jsnParametros.append('strIndicadorZona', intIndicadorZona);
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                dctPlaneacionComercial.dctIndicadoresZonas.lstCategoriasGraficoZonas = []
                dctPlaneacionComercial.dctIndicadoresZonas.lstSeriesZonas = []
                if(request != false){
                    dctPlaneacionComercial.dctIndicadoresZonas.lstCategoriasGraficoZonas = request[0];
                    dctPlaneacionComercial.dctIndicadoresZonas.lstSeriesZonas = request[1]
                    dctPlaneacionComercial.fncIndicadorZonagrf();
                    $('#rowGraficoZona').attr('hidden', false);
                }
                if(intIndicadorZona == 'Total_Sales_Objetive'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas, function (pos, value) {
                            if(value.intIndicador == 'Total_Sales_Objetive'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralZona').attr('hidden', false);
                    $('#iptMetaGeneralZona').val($('#iptVentaTotal').val());
                    $('#iptMetaAcumuladaZona').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteZona').val(parseFloat($('#iptVentaTotal').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoZona').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100000000000000,
                        decimals: 2,
                        step: 0.01,
                        prefix: '$',
                        postfix: ''
                    });
                    return;
                }
                else if(intIndicadorZona == 'Customer_Retention_Rate'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas, function (pos, value) {
                            if(value.intIndicador == 'Customer_Retention_Rate'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralZona').attr('hidden', false);
                    $('#iptMetaGeneralZona').val($('#iptVentasNuevas').val());
                    $('#iptMetaAcumuladaZona').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteZona').val(parseFloat($('#iptVentasNuevas').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoZona').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100000000000000,
                        decimals: 2,
                        step: 0.01,
                        prefix: '$',
                        postfix: ''
                    });
                    return;
                }
                else if(intIndicadorZona == 'Sales_Deepening'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas, function (pos, value) {
                            if(value.intIndicador == 'Sales_Deepening'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralZona').attr('hidden', false);
                    $('#iptMetaGeneralZona').val($('#iptProfundizacionClientes').val());
                    $('#iptMetaAcumuladaZona').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteZona').val(parseFloat($('#iptProfundizacionClientes').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoZona').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100000000000000,
                        decimals: 2,
                        step: 0.01,
                        prefix: '$',
                        postfix: ''
                    });
                    return;
                }
                else if(intIndicadorZona == 'New_Customers'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas, function (pos, value) {
                            if(value.intIndicador == 'New_Customers'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralZona').attr('hidden', false);
                    $('#iptMetaGeneralZona').val($('#iptClientesNuevos').val());
                    $('#iptMetaAcumuladaZona').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteZona').val(parseFloat($('#iptClientesNuevos').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoZona').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 10000000,
                        step: 1,
                        decimals: 0,
                        prefix:'Nº',
                        postfix: ''
                    });
                    return; 
                }
                else if(intIndicadorZona == 'Margin'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas, function (pos, value) {
                            if(value.intIndicador == 'Margin'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralZona').attr('hidden', false);
                    $('#iptMetaGeneralZona').val($('#iptMargenVenta').val());
                    $('#iptMetaAcumuladaZona').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteZona').val(parseFloat($('#iptMargenVenta').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoZona').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100,
                        step: 0.01,
                        decimals: 2,
                        prefix:'',
                        postfix: '%'
                    });
                    return;
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    }
    
    // Función que ejcuta una petición ajax para un indicador y una categoría cliente especifica y retorna la data con el gráfico si existe
    function fncRetornarDataGraficoCategoriaCliente() {
        var intIndicadorCategoriaCliente = $('#slcIndicadorCategoriaCliente').val();
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'slcIndicadorCategoriaClientejsn');
        jsnParametros.append('intCategoriaCliente', $('#slcCategoriaCliente').val());
        jsnParametros.append('strIndicadorCategoriaCliente', $('#slcIndicadorCategoriaCliente').val());
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriasGraficoCategoriaCliente = []
                dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstSeriesCategoriaCliente = []
                if(request != false){
                    dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriasGraficoCategoriaCliente = request[0];
                    dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstSeriesCategoriaCliente = request[1]
                    dctPlaneacionComercial.fncIndicadorCategoriaClientegrf();
                    $('#rowGraficoCategoriaCliente').attr('hidden', false);
                }
                if(intIndicadorCategoriaCliente == 'Total_Sales_Objetive'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente, function (pos, value) {
                            if(value.intIndicador == 'Total_Sales_Objetive'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralCategoriaCliente').attr('hidden', false);
                    $('#iptMetaGeneralCategoriaCliente').val($('#iptVentaTotal').val());
                    $('#iptMetaAcumuladaCategoriaCliente').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteCategoriaCliente').val(parseFloat($('#iptVentaTotal').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoCategoriaCliente').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100000000000000,
                        decimals: 2,
                        step: 0.01,
                        prefix: '$',
                        postfix: ''
                    });
                    return;
                }
                else if(intIndicadorCategoriaCliente == 'Customer_Retention_Rate'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente, function (pos, value) {
                            if(value.intIndicador == 'Customer_Retention_Rate'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralCategoriaCliente').attr('hidden', false);
                    $('#iptMetaGeneralCategoriaCliente').val($('#iptVentasNuevas').val());
                    $('#iptMetaAcumuladaCategoriaCliente').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteCategoriaCliente').val(parseFloat($('#iptVentasNuevas').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoCategoriaCliente').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100000000000000,
                        decimals: 2,
                        step: 0.01,
                        prefix: '$',
                        postfix: ''
                    });
                    return;
                }
                else if(intIndicadorCategoriaCliente == 'Sales_Deepening'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente, function (pos, value) {
                            if(value.intIndicador == 'Sales_Deepening'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralCategoriaCliente').attr('hidden', false);
                    $('#iptMetaGeneralCategoriaCliente').val($('#iptProfundizacionClientes').val());
                    $('#iptMetaAcumuladaCategoriaCliente').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteCategoriaCliente').val(parseFloat($('#iptProfundizacionClientes').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoCategoriaCliente').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100000000000000,
                        decimals: 2,
                        step: 0.01,
                        prefix: '$',
                        postfix: ''
                    });
                    return;
                }
                else if(intIndicadorCategoriaCliente == 'New_Customers'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente, function (pos, value) {
                            if(value.intIndicador == 'New_Customers'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralCategoriaCliente').attr('hidden', false);
                    $('#iptMetaGeneralCategoriaCliente').val($('#iptClientesNuevos').val());
                    $('#iptMetaAcumuladaCategoriaCliente').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteCategoriaCliente').val(parseFloat($('#iptClientesNuevos').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoCategoriaCliente').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 10000000,
                        step: 1,
                        decimals: 0,
                        prefix:'Nº',
                        postfix: ''
                    });
                    return; 
                }
                else if(intIndicadorCategoriaCliente == 'Margin'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente, function (pos, value) {
                            if(value.intIndicador == 'Margin'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralCategoriaCliente').attr('hidden', false);
                    $('#iptMetaGeneralCategoriaCliente').val($('#iptMargenVenta').val());
                    $('#iptMetaAcumuladaCategoriaCliente').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteCategoriaCliente').val(parseFloat($('#iptMargenVenta').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoCategoriaCliente').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100,
                        step: 0.01,
                        decimals: 2,
                        prefix:'',
                        postfix: '%'
                    });
                    return;
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    }

    // Función que ejcuta una petición ajax para un indicador y una categoría cliente especifica y retorna la data con el gráfico si existe
    function fncRetornarDataGraficoAsesorComercial() {
        var intIndicadorAsesorComercial = $('#slcIndicadorAsesorComercial').val();
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'slcIndicadorAsesorComercialjsn');
        jsnParametros.append('intAsesorComercial', $('#slcAsesorComercial').val());
        jsnParametros.append('strIndicadorAsesorComercial', intIndicadorAsesorComercial);
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstCategoriasGraficoAsesorComercial = []
                dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstSeriesAsesorComercial = []
                if(request != false){
                    dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstCategoriasGraficoAsesorComercial = request[0];
                    dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstSeriesAsesorComercial = request[1]
                    dctPlaneacionComercial.fncIndicadorAsesorComercialgrf();
                    $('#rowGraficoAsesorComercial').attr('hidden', false);
                }
                if(intIndicadorAsesorComercial == 'Total_Sales_Objetive'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales, function (pos, value) {
                            if(value.intIndicador == 'Total_Sales_Objetive'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralAsesorComercial').attr('hidden', false);
                    $('#iptMetaGeneralAsesorComercial').val($('#iptVentaTotal').val());
                    $('#iptMetaAcumuladaAsesorComercial').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteAsesorComercial').val(parseFloat($('#iptVentaTotal').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoAsesorComercial').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100000000000000,
                        decimals: 2,
                        step: 0.01,
                        prefix: '$',
                        postfix: ''
                    });
                    return;
                }
                else if(intIndicadorAsesorComercial == 'Customer_Retention_Rate'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales, function (pos, value) {
                            if(value.intIndicador == 'Customer_Retention_Rate'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralAsesorComercial').attr('hidden', false);
                    $('#iptMetaGeneralAsesorComercial').val($('#iptVentasNuevas').val());
                    $('#iptMetaAcumuladaAsesorComercial').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteAsesorComercial').val(parseFloat($('#iptVentasNuevas').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoAsesorComercial').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100000000000000,
                        decimals: 2,
                        step: 0.01,
                        prefix: '$',
                        postfix: ''
                    });
                    return;
                }
                else if(intIndicadorAsesorComercial == 'Sales_Deepening'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales, function (pos, value) {
                            if(value.intIndicador == 'Sales_Deepening'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralAsesorComercial').attr('hidden', false);
                    $('#iptMetaGeneralAsesorComercial').val($('#iptProfundizacionClientes').val());
                    $('#iptMetaAcumuladaAsesorComercial').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteAsesorComercial').val(parseFloat($('#iptProfundizacionClientes').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoAsesorComercial').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100000000000000,
                        decimals: 2,
                        step: 0.01,
                        prefix: '$',
                        postfix: ''
                    });
                    return;
                }
                else if(intIndicadorAsesorComercial == 'New_Customers'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales, function (pos, value) {
                            if(value.intIndicador == 'New_Customers'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralAsesorComercial').attr('hidden', false);
                    $('#iptMetaGeneralAsesorComercial').val($('#iptClientesNuevos').val());
                    $('#iptMetaAcumuladaAsesorComercial').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteAsesorComercial').val(parseFloat($('#iptClientesNuevos').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoAsesorComercial').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 10000000,
                        step: 1,
                        decimals: 0,
                        prefix:'Nº',
                        postfix: ''
                    });
                    return; 
                }
                else if(intIndicadorAsesorComercial == 'Margin'){
                    var fltAcumuladoIndicador = 0.00;
                    if(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales.length >= 1){
                        $.each(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales, function (pos, value) {
                            if(value.intIndicador == 'Margin'){
                                fltAcumuladoIndicador += parseFloat(value.fltObjetivoIndicador);
                            }
                        });
                    }
                    $('#rowMetaGeneralAsesorComercial').attr('hidden', false);
                    $('#iptMetaGeneralAsesorComercial').val($('#iptMargenVenta').val());
                    $('#iptMetaAcumuladaAsesorComercial').val(fltAcumuladoIndicador);
                    $('#iptMetaRestanteAsesorComercial').val(parseFloat($('#iptMargenVenta').val() - fltAcumuladoIndicador).toFixed(2));
                    $('#iptObjetivoAsesorComercial').trigger("touchspin.updatesettings", {
                        min: 0,
                        max: 100,
                        step: 0.01,
                        decimals: 2,
                        prefix:'',
                        postfix: '%'
                    });
                    return;
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    }

    // Ejecutar consulta de histórico para gráficar indicadores generales
    $(function fncRetornarGraficosGenerales() {
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'jsnConsultarIndicadoresjsn');
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                console.log(request);
                if(request[0].Total_Sales_Objetive != false){
                    for (let i = 0; i < request[0].Total_Sales_Objetive[0].length; i++) {
                        dctPlaneacionComercial.dctIndicadorVentaTotal.lstCategorias.push(request[0].Total_Sales_Objetive[0][i]);
                    };
                    for (let i = 0; i < request[0].Total_Sales_Objetive[1].length; i++) {
                        dctPlaneacionComercial.dctIndicadorVentaTotal.lstSeries.push(request[0].Total_Sales_Objetive[1][i]);
                    };
                    dctPlaneacionComercial.fncIndicadorVentaTotalgrf();
                }
                if(request[1].Customer_Retention_Rate != false){
                    for (let i = 0; i < request[1].Customer_Retention_Rate[0].length; i++) {
                        dctPlaneacionComercial.dctIndicadorVentasNuevas.lstCategorias.push(request[1].Customer_Retention_Rate[0][i]);
                    };
                    for (let i = 0; i < request[1].Customer_Retention_Rate[1].length; i++) {
                        dctPlaneacionComercial.dctIndicadorVentasNuevas.lstSeries.push(request[1].Customer_Retention_Rate[1][i]);
                    };
                    dctPlaneacionComercial.fncIndicadorVentasNuevasgrf();
                }
                if(request[2].Sales_Deepening != false){
                    for (let i = 0; i < request[2].Sales_Deepening[0].length; i++) {
                        dctPlaneacionComercial.dctIndicadorProfundizacionClientes.lstCategorias.push(request[2].Sales_Deepening[0][i]);
                    };
                    for (let i = 0; i < request[2].Sales_Deepening[1].length; i++) {
                        dctPlaneacionComercial.dctIndicadorProfundizacionClientes.lstSeries.push(request[2].Sales_Deepening[1][i]);
                    };
                    dctPlaneacionComercial.fncIndicadorProfundizacionClientesgrf();
                }
                if(request[3].New_Customers != false){
                    for (let i = 0; i < request[3].New_Customers[0].length; i++) {
                        dctPlaneacionComercial.dctIndicadorClientesNuevos.lstCategorias.push(request[3].New_Customers[0][i]);
                    };
                    for (let i = 0; i < request[3].New_Customers[1].length; i++) {
                        dctPlaneacionComercial.dctIndicadorClientesNuevos.lstSeries.push(request[3].New_Customers[1][i]);
                    };
                    dctPlaneacionComercial.fncIndicadorClientesNuevosgrf();
                }
                if(request[4].Margin != false){
                    for (let i = 0; i < request[4].Margin[0].length; i++) {
                        dctPlaneacionComercial.dctIndicadorMargenVenta.lstCategorias.push(request[4].Margin[0][i]);
                    };
                    for (let i = 0; i < request[4].Margin[1].length; i++) {
                        dctPlaneacionComercial.dctIndicadorMargenVenta.lstSeries.push(request[4].Margin[1][i]);
                    };
                    dctPlaneacionComercial.fncIndicadorMargenVentagrf();
                }
                return;
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });    
    });
    
    // Evento cuando collapse de ciudad se muestra
    $('#cllCiudad').on('shown.bs.collapse', function () {
        dctPlaneacionComercial.dctIndicadoresCiudades.bolCollapseCiudad = true;
    });
     
    // Evento cuando collapse de ciudad se oculta
    $('#cllCiudad').on('hidden.bs.collapse', function () {
        dctPlaneacionComercial.dctIndicadoresCiudades.bolCollapseCiudad = false;
    });

    // Ejecutar consulta para establecer indicadores por ciudad
    $('#btnCollapseCiudad').on('click', function (e) {
        e.stopPropagation();
        if (dctPlaneacionComercial.dctIndicadoresCiudades.lstCiudades.length >= 1){
            if (dctPlaneacionComercial.dctIndicadoresCiudades.bolCollapseCiudad == false){
                $('#cllCiudad').collapse('show');
                return;
            }
            else{
                $('#cllCiudad').collapse('hide');
                return;
            }
        }
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'btnConsultarCiudadesClientesjsn');
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                if (request.hasOwnProperty('strError')) {   
                    fncMensajeErrormns(request.strError);
                    return;
                }
                dctPlaneacionComercial.dctIndicadoresCiudades.lstCiudades = request.lstSelectCiudad;
                $("#slcCiudad").select2({
                    theme: "bootstrap4",
                    placeholder: "Seleccione una ciudad",
                    language: 'es',
                    allowClear: true,
                    data: request.lstSelectCiudad
                });
                $("#slcIndicadorCiudad").select2({
                    theme: "bootstrap4",
                    placeholder: "Seleccione un indicador",
                    language: 'es',
                    allowClear: true,
                });
                $('#slcCiudad').val('').trigger('change.select2');
                $('#slcIndicadorCiudad').val('').trigger('change.select2');
                $('#cllCiudad').collapse('show');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    });    

    // Ejecutar consulta de indicador por ciudad
    $('#slcIndicadorCiudad').on('select2:select', function (e) { 
        e.preventDefault();
        var intIndicadorCiudad = $('#slcIndicadorCiudad').val();
        var strCiudad = $('#slcCiudad :selected').text();
        var strIndicadorCiudad = $('#slcIndicadorCiudad :selected').text();
        if(intIndicadorCiudad == ''){
            fncMensajeErrormns('Seleccione una ciudad');
            $('#slcIndicadorCiudad').val('').trigger('change.select2');
            return;
        }
        else if(intIndicadorCiudad == 'Total_Sales_Objetive'){
            if($('#iptVentaTotal').val() == ''){
                fncMensajeErrormns('Para establecer indicador de venta total por ciudad, debe establecer indicador general de venta total');
                $('#slcIndicadorCiudad').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorCiudad == 'Customer_Retention_Rate'){
            if($('#iptVentasNuevas').val() == ''){
                fncMensajeErrormns('Para establecer indicador de ventas nuevas por ciudad, debe establecer indicador general de ventas nuevas');
                $('#slcIndicadorCiudad').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorCiudad == 'Sales_Deepening'){
            if($('#iptProfundizacionClientes').val() == ''){
                fncMensajeErrormns('Para establecer indicador de profundización de ventas por ciudad, debe establecer indicador general de profundización de ventas');
                $('#slcIndicadorCiudad').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorCiudad == 'New_Customers'){
            if($('#iptClientesNuevos').val() == ''){
                fncMensajeErrormns('Para establecer indicador de clientes nuevos por ciudad, debe establecer indicador general de clientes nuevos');
                $('#slcIndicadorCiudad').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorCiudad == 'Margin'){
            if($('#iptMargenVenta').val() == ''){
                fncMensajeErrormns('Para establecer indicador de margén de venta por ciudad, debe establecer indicador general de margén de venta');
                $('#slcIndicadorCiudad').val('').trigger('change.select2');
                return;
            }
        }
        if (dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades.length >= 1){
            $.each(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades, function (pos, value) {
                if(strCiudad == value.strSubset && strIndicadorCiudad == value.strIndicador){
                    fncMensajeConfirmacionmns('Alerta', 'Ya se encuentra en la tabla esta ciudad con este indicador ¿desea eliminar el actual y establecerlo de nuevo?',
                    function () {
                        dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades.splice(pos, 1);
                        $('#tblIndicadorCiudad').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades).draw();
                        $('#iptObjetivoCiudad').focus();
                        fncRetornarDataGraficoCiudad();
                        return;
                    },
                    function () {
                        $('#slcCiudad').val('').trigger('change.select2');
                        $('#slcIndicadorCiudad').val('').trigger('change.select2');
                        $('#iptObjetivoCiudad').val('');
                        $('#iptMetaGeneralCiudad').val('');
                        $('#iptMetaAcumuladaCiudad').val('');
                        $('#iptMetaRestanteCiudad').val('');
                        $('#rowMetaGeneral').attr('hidden', true);
                        $('#rowGraficoCiudad').attr('hidden', true);
                        return;
                    });
                    return;
                }
                else{
                    fncRetornarDataGraficoCiudad();
                }
            });
            return;
        }
        fncRetornarDataGraficoCiudad();
    });
    
    // Agregar indicador a la tabla de ciudades
    $('#frmCiudad').on('submit', function (e) {
        e.preventDefault();
        var intCiudad = $('#slcCiudad').val();
        var strCiudad = $('#slcCiudad :selected').text();
        var fltObjetivoIndicador = parseFloat($('#iptObjetivoCiudad').val()).toFixed(2);
        var intIndicadorCiudad = $('#slcIndicadorCiudad').val();
        var strIndicadorCiudad = $('#slcIndicadorCiudad :selected').text();
        var fltMetaRestanteCiudad = $('#iptMetaRestanteCiudad').val();
        var strObjetivoIndicador = fltObjetivoIndicador.toString()
        var strMetaRestanteCiudad = fltMetaRestanteCiudad.toString()
        if(strObjetivoIndicador.length >= strMetaRestanteCiudad.length ){
            if(fltObjetivoIndicador > fltMetaRestanteCiudad){
                fncMensajeErrormns('No puede establecer una meta para este indicador mayor que la meta general, por favor valide el recuadro de meta restante');
                return;
            }
        }
        dctNuevoIndicador = {
            'strSet': 'City',
            'intSubset': intCiudad,
            'strSubset': strCiudad,
            'intIndicador': intIndicadorCiudad,
            'strIndicador': strIndicadorCiudad,
            'fltObjetivoIndicador': parseFloat(fltObjetivoIndicador).toFixed(2)
        }
        if(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades.length >= 1){
            dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades.push(dctNuevoIndicador);
            $('#slcCiudad').val('').trigger('change.select2');
            $('#slcIndicadorCiudad').val('').trigger('change.select2');
            $('#iptObjetivoCiudad').val('');
            $('#iptMetaGeneralCiudad').val('');
            $('#iptMetaAcumuladaCiudad').val('');
            $('#iptMetaRestanteCiudad').val('');
            $('#rowMetaGeneral').attr('hidden', true);
            $('#rowGraficoCiudad').attr('hidden', true);
            $('#tblIndicadorCiudad').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades).draw();
        }
        else{
            dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades.push(dctNuevoIndicador);
            $('#slcCiudad').val('').trigger('change.select2');
            $('#slcIndicadorCiudad').val('').trigger('change.select2');
            $('#iptObjetivoCiudad').val('');
            $('#iptMetaGeneralCiudad').val('');
            $('#iptMetaAcumuladaCiudad').val('');
            $('#iptMetaRestanteCiudad').val('');
            $('#rowMetaGeneral').attr('hidden', true);
            $('#rowGraficoCiudad').attr('hidden', true);
            dctPlaneacionComercial.fncIndicadoresCiudadtbl();
        }
    });
    
    // Editar indicador de tabla ciudades
    $('#tblIndicadorCiudad tbody').on('click', 'a[rel="edit"]', function () {
        var tr = tblIndicadorCiudad.cell($(this).closest('td, li')).index();
        var data = tblIndicadorCiudad.row(tr.row).data();
        $.each(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades, function (pos, value) {
            if(data == value){
                dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades.splice(pos, 1);
            }
        });
        $('#slcCiudad').val(data.intSubset).trigger('change.select2');
        $('#slcIndicadorCiudad').val(data.intIndicador).trigger('change.select2');
        $('#iptObjetivoCiudad').val(data.fltObjetivoIndicador);
        $('#rowMetaGeneral').attr('hidden', false);
        $('#tblIndicadorCiudad').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades).draw();
        fncRetornarDataGraficoCiudad();
    });

    // Eliminar indicador de tabla ciudades
    $('#tblIndicadorCiudad tbody').on('click', 'a[rel="delete"]', function (e) {
        e.preventDefault();
        var tr = tblIndicadorCiudad.cell($(this).closest('td, li')).index();
        var data = tblIndicadorCiudad.row(tr.row).data();
        fncMensajeAlertamns('Eliminar indicador', '¿Está seguro de eliminar este indicador?', function () {
            $.each(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades, function (pos, value) {
                if(data == value){
                    dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades.splice(pos, 1);
                }
            });
            $('#tblIndicadorCiudad').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades).draw();    
        })
    });

    // Evento cuando collapse de zona se muestra
    $('#cllZona').on('shown.bs.collapse', function () {
        dctPlaneacionComercial.dctIndicadoresZonas.bolCollapseZona = true;
    });
     
    // Evento cuando collapse de zona se oculta
    $('#cllZona').on('hidden.bs.collapse', function () {
        dctPlaneacionComercial.dctIndicadoresZonas.bolCollapseZona = false;
    });

    // Ejecutar consulta para establecer indicadores por zona
    $('#btnCollapseZona').on('click', function (e) {
        e.stopPropagation();
        if (dctPlaneacionComercial.dctIndicadoresZonas.lstZonas.length >= 1){
            if (dctPlaneacionComercial.dctIndicadoresZonas.bolCollapseZona == false){
                $('#cllZona').collapse('show');
                return;
            }
            else{
                $('#cllZona').collapse('hide');
                return;
            }
        }
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'btnConsultarZonasClientesjsn');
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                if (request.hasOwnProperty('strError')) {   
                    fncMensajeErrormns(request.strError);
                    return;
                }
                dctPlaneacionComercial.dctIndicadoresZonas.lstZonas = request.lstSelectZonas;
                $("#slcZona").select2({
                    theme: "bootstrap4",
                    placeholder: "Seleccione una zona",
                    language: 'es',
                    allowClear: true,
                    data: request.lstSelectZonas
                });
                $("#slcIndicadorZona").select2({
                    theme: "bootstrap4",
                    placeholder: "Seleccione un indicador",
                    language: 'es',
                    allowClear: true,
                });
                $('#slcZona').val('').trigger('change.select2');
                $('#slcIndicadorZona').val('').trigger('change.select2');
                $('#cllZona').collapse('show');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    });

    // Ejecutar consulta de indicador por zona
    $('#slcIndicadorZona').on('select2:select', function (e) { 
        e.preventDefault();
        var intIndicadorZona = $('#slcIndicadorZona').val();
        var strZona = $('#slcZona :selected').text();
        var strIndicadorZona = $('#slcIndicadorZona :selected').text();
        if(intIndicadorZona == ''){
            fncMensajeErrormns('Seleccione una zona');
            $('#slcIndicadorZona').val('').trigger('change.select2');
            return;
        }
        else if(intIndicadorZona == 'Total_Sales_Objetive'){
            if($('#iptVentaTotal').val() == ''){
                fncMensajeErrormns('Para establecer indicador de venta total por zona, debe establecer indicador general de venta total');
                $('#slcIndicadorZona').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorZona == 'Customer_Retention_Rate'){
            if($('#iptVentasNuevas').val() == ''){
                fncMensajeErrormns('Para establecer indicador de ventas nuevas por zona, debe establecer indicador general de ventas nuevas');
                $('#slcIndicadorZona').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorZona == 'Sales_Deepening'){
            if($('#iptProfundizacionClientes').val() == ''){
                fncMensajeErrormns('Para establecer indicador de profundización de ventas por zona, debe establecer indicador general de profundización de ventas');
                $('#slcIndicadorZona').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorZona == 'New_Customers'){
            if($('#iptClientesNuevos').val() == ''){
                fncMensajeErrormns('Para establecer indicador de clientes nuevos por zona, debe establecer indicador general de clientes nuevos');
                $('#slcIndicadorZona').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorZona == 'Margin'){
            if($('#iptMargenVenta').val() == ''){
                fncMensajeErrormns('Para establecer indicador de margén de venta por zona, debe establecer indicador general de margén de venta');
                $('#slcIndicadorZona').val('').trigger('change.select2');
                return;
            }
        }
        if (dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas.length >= 1){
            $.each(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas, function (pos, value) {
                if(strZona == value.strSubset && strIndicadorZona == value.strIndicador){
                    fncMensajeConfirmacionmns('Alerta', 'Ya se encuentra en la tabla esta zona con este indicador ¿desea eliminar el actual y establecerlo de nuevo?',
                    function () {
                        dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas.splice(pos, 1);
                        $('#tblIndicadorZona').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas).draw();
                        $('#iptObjetivoZona').focus();
                        fncRetornarDataGraficoZona();
                        return;
                    }, 
                    function () {
                        $('#slcZona').val('').trigger('change.select2');
                        $('#slcIndicadorZona').val('').trigger('change.select2');
                        $('#iptObjetivoZona').val('');
                        $('#iptMetaGeneralZona').val('');
                        $('#iptMetaAcumuladaZona').val('');
                        $('#iptMetaRestanteZona').val('');
                        $('#rowMetaGeneral').attr('hidden', true);
                        $('#rowGraficoZona').attr('hidden', true);
                        return;
                    });
                    return;
                }
                else{
                    fncRetornarDataGraficoZona();
                }
            });
            return;
        }
        fncRetornarDataGraficoZona();
    });
    
    // Agregar indicador a la tabla de zonas
    $('#frmZona').on('submit', function (e) {
        e.preventDefault();
        var intZona = $('#slcZona').val();
        var strZona = $('#slcZona :selected').text();
        var fltObjetivoIndicador = parseFloat($('#iptObjetivoZona').val()).toFixed(2);
        var intIndicadorZona = $('#slcIndicadorZona').val();
        var strIndicadorZona = $('#slcIndicadorZona :selected').text();
        var fltMetaRestanteZona = $('#iptMetaRestanteZona').val();
        var strObjetivoIndicador = fltObjetivoIndicador.toString()
        var strMetaRestanteZona = fltMetaRestanteZona.toString()
        if(strObjetivoIndicador.length >= strMetaRestanteZona.length ){
            if(fltObjetivoIndicador > fltMetaRestanteZona){
                fncMensajeErrormns('No puede establecer una meta para este indicador mayor que la meta general, por favor valide el recuadro de meta restante');
                return;
            }
        }
        dctNuevoIndicador = {
            'strSet': 'Zones',
            'intSubset': intZona,
            'strSubset': strZona,
            'intIndicador': intIndicadorZona,
            'strIndicador': strIndicadorZona,
            'fltObjetivoIndicador': parseFloat(fltObjetivoIndicador).toFixed(2)
        }
        if(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas.length >= 1){
            dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas.push(dctNuevoIndicador);
            $('#slcZona').val('').trigger('change.select2');
            $('#slcIndicadorZona').val('').trigger('change.select2');
            $('#iptObjetivoZona').val('');
            $('#iptMetaGeneralZona').val('');
            $('#iptMetaAcumuladaZona').val('');
            $('#iptMetaRestanteZona').val('');
            $('#rowMetaGeneralZona').attr('hidden', true);
            $('#rowGraficoZona').attr('hidden', true);
            $('#tblIndicadorZona').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas).draw();
        }
        else{
            dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas.push(dctNuevoIndicador);
            $('#slcZona').val('').trigger('change.select2');
            $('#slcIndicadorZona').val('').trigger('change.select2');
            $('#iptObjetivoZona').val('');
            $('#iptMetaGeneralZona').val('');
            $('#iptMetaAcumuladaZona').val('');
            $('#iptMetaRestanteZona').val('');
            $('#rowMetaGeneralZona').attr('hidden', true);
            $('#rowGraficoZona').attr('hidden', true);
            dctPlaneacionComercial.fncIndicadoresZonatbl();
        }
        
    });
    
    // Editar indicador de tabla zonas
    $('#tblIndicadorZona tbody').on('click', 'a[rel="edit"]', function () {
        var tr = tblIndicadorZona.cell($(this).closest('td, li')).index();
        var data = tblIndicadorZona.row(tr.row).data();
        $.each(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas, function (pos, value) {
            if(data == value){
                dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas.splice(pos, 1);
            }
        });
        $('#slcZona').val(data.intSubset).trigger('change.select2');
        $('#slcIndicadorZona').val(data.intIndicador).trigger('change.select2');
        $('#iptObjetivoZona').val(data.fltObjetivoIndicador);
        $('#rowMetaGeneralZona').attr('hidden', false);
        $('#tblIndicadorZona').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas).draw();
        fncRetornarDataGraficoZona();
    });

    // Eliminar indicador de tabla zonas
    $('#tblIndicadorZona tbody').on('click', 'a[rel="delete"]', function (e) {
        e.preventDefault();
        var tr = tblIndicadorZona.cell($(this).closest('td, li')).index();
        var data = tblIndicadorZona.row(tr.row).data();
        fncMensajeAlertamns('Eliminar indicador', '¿Está seguro de eliminar este indicador?', function () {
            $.each(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas, function (pos, value) {
                if(data == value){
                    dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas.splice(pos, 1);
                }
            });
            $('#tblIndicadorZona').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas).draw();    
        })
    });

    // Evento cuando collapse de categoría cliente se muestra
    $('#cllCategoriaCliente').on('shown.bs.collapse', function () {
        dctPlaneacionComercial.dctIndicadoresCategoriaCliente.bolCollapseCategoriaCliente = true;
    });
     
    // Evento cuando collapse de categoría cliente se oculta
    $('#cllCategoriaCliente').on('hidden.bs.collapse', function () {
        dctPlaneacionComercial.dctIndicadoresCategoriaCliente.bolCollapseCategoriaCliente = false;
    });

    // Ejecutar consulta para establecer indicadores por categoría cliente
    $('#btnCollapseCategoriaCliente').on('click', function (e) {
        e.stopPropagation();
        if (dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente.length >= 1){
            if (dctPlaneacionComercial.dctIndicadoresCategoriaCliente.bolCollapseCategoriaCliente == false){
                $('#cllCategoriaCliente').collapse('show');
                return;
            }
            else{
                $('#cllCategoriaCliente').collapse('hide');
                return;
            }
        }
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'btnConsultarCategoriasClientesjsn');
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                if (request.hasOwnProperty('strError')) {   
                    fncMensajeErrormns(request.strError);
                    return;
                }
                dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente = request.lstSelectCategoriaCliente;
                $("#slcCategoriaCliente").select2({
                    theme: "bootstrap4",
                    placeholder: "Seleccione una categoría",
                    language: 'es',
                    allowClear: true,
                    data: request.lstSelectCategoriaCliente
                });
                $("#slcIndicadorCategoriaCliente").select2({
                    theme: "bootstrap4",
                    placeholder: "Seleccione un indicador",
                    language: 'es',
                    allowClear: true,
                });
                $('#slcCategoriaCliente').val('').trigger('change.select2');
                $('#slcIndicadorCategoriaCliente').val('').trigger('change.select2');
                $('#cllCategoriaCliente').collapse('show');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    });

    // Ejecutar consulta de indicador por categoría cliente
    $('#slcIndicadorCategoriaCliente').on('select2:select', function (e) {
        e.preventDefault();
        var intIndicadorCategoriaCliente = $('#slcIndicadorCategoriaCliente').val();
        var strCategoriaCliente = $('#slcCategoriaCliente :selected').text();
        var strIndicadorCategoriaCliente = $('#slcIndicadorCategoriaCliente :selected').text();
        if(intIndicadorCategoriaCliente == ''){
            fncMensajeErrormns('Seleccione una categoría cliente');
            $('#slcIndicadorCategoriaCliente').val('').trigger('change.select2');
            return;
        }
        else if(intIndicadorCategoriaCliente == 'Total_Sales_Objetive'){
            if($('#iptVentaTotal').val() == ''){
                fncMensajeErrormns('Para establecer indicador de venta total por categoría cliente, debe establecer indicador general de venta total');
                $('#slcIndicadorCategoriaCliente').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorCategoriaCliente == 'Customer_Retention_Rate'){
            if($('#iptVentasNuevas').val() == ''){
                fncMensajeErrormns('Para establecer indicador de ventas nuevas por categoría cliente, debe establecer indicador general de ventas nuevas');
                $('#slcIndicadorCategoriaCliente').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorCategoriaCliente == 'Sales_Deepening'){
            if($('#iptProfundizacionClientes').val() == ''){
                fncMensajeErrormns('Para establecer indicador de profundización de ventas por categoría cliente, debe establecer indicador general de profundización de ventas');
                $('#slcIndicadorCategoriaCliente').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorCategoriaCliente == 'New_Customers'){
            if($('#iptClientesNuevos').val() == ''){
                fncMensajeErrormns('Para establecer indicador de clientes nuevos por categoría cliente, debe establecer indicador general de clientes nuevos');
                $('#slcIndicadorCategoriaCliente').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorCategoriaCliente == 'Margin'){
            if($('#iptMargenVenta').val() == ''){
                fncMensajeErrormns('Para establecer indicador de margén de venta por categoría cliente, debe establecer indicador general de margén de venta');
                $('#slcIndicadorCategoriaCliente').val('').trigger('change.select2');
                return;
            }
        }
        if (dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente.length >= 1){
            $.each(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente, function (pos, value) {
                if(strCategoriaCliente == value.strSubset && strIndicadorCategoriaCliente == value.strIndicador){
                    fncMensajeConfirmacionmns('Alerta', 'Ya se encuentra en la tabla esta categoría cliente con este indicador ¿desea eliminar el actual y establecerlo de nuevo?',
                    function () {
                        dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente.splice(pos, 1);
                        $('#tblIndicadorCategoriaCliente').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente).draw();
                        $('#iptObjetivoCategoriaCliente').focus();
                        fncRetornarDataGraficoCategoriaCliente();
                        return;
                    }, 
                    function () {
                        $('#slcCategoriaCliente').val('').trigger('change.select2');
                        $('#slcIndicadorCategoriaCliente').val('').trigger('change.select2');
                        $('#iptObjetivoCategoriaCliente').val('');
                        $('#iptMetaGeneralCategoriaCliente').val('');
                        $('#iptMetaAcumuladaCategoriaCliente').val('');
                        $('#iptMetaRestanteCategoriaCliente').val('');
                        $('#rowMetaGeneral').attr('hidden', true);
                        $('#rowGraficoCategoriaCliente').attr('hidden', true);
                        return;
                    });
                    return;
                }
                else{
                    fncRetornarDataGraficoCategoriaCliente();
                }
            });
            return;
        }
        fncRetornarDataGraficoCategoriaCliente();
    });
    
    // Agregar indicador a la tabla de categorías cliente
    $('#frmCategoriaCliente').on('submit', function (e) {
        e.preventDefault();
        var intCategoriaCliente = $('#slcCategoriaCliente').val();
        var strCategoriaCliente = $('#slcCategoriaCliente :selected').text();
        var fltObjetivoIndicador = parseFloat($('#iptObjetivoCategoriaCliente').val()).toFixed(2);
        var intIndicadorCategoriaCliente = $('#slcIndicadorCategoriaCliente').val();
        var strIndicadorCategoriaCliente = $('#slcIndicadorCategoriaCliente :selected').text();
        var fltMetaRestanteCategoriaCliente = $('#iptMetaRestanteCategoriaCliente').val();
        var strObjetivoIndicador = fltObjetivoIndicador.toString()
        var strMetaRestanteCategoriaCliente = fltMetaRestanteCategoriaCliente.toString()
        if(strObjetivoIndicador.length >= strMetaRestanteCategoriaCliente.length ){
            if(fltObjetivoIndicador > fltMetaRestanteCategoriaCliente){
                fncMensajeErrormns('No puede establecer una meta para este indicador mayor que la meta general, por favor valide el recuadro de meta restante');
                return;
            }
        }
        dctNuevoIndicador = {
            'strSet': 'Customer_Category',
            'intSubset': intCategoriaCliente,
            'strSubset': strCategoriaCliente,
            'intIndicador': intIndicadorCategoriaCliente,
            'strIndicador': strIndicadorCategoriaCliente,
            'fltObjetivoIndicador': parseFloat(fltObjetivoIndicador).toFixed(2)
        }
        if(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstTablaCategoriaCliente.length >= 1){
            dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstTablaCategoriaCliente.push(dctNuevoIndicador);
            $('#slcCategoriaCliente').val('').trigger('change.select2');
            $('#slcIndicadorCategoriaCliente').val('').trigger('change.select2');
            $('#iptObjetivoCategoriaCliente').val('');
            $('#iptMetaGeneralCategoriaCliente').val('');
            $('#iptMetaAcumuladaCategoriaCliente').val('');
            $('#iptMetaRestanteCategoriaCliente').val('');
            $('#rowMetaGeneralCategoriaCliente').attr('hidden', true);
            $('#rowGraficoCategoriaCliente').attr('hidden', true);
            $('#tblIndicadorCategoriaCliente').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstCategoriaCliente).draw();
        }
        else{
            dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstTablaCategoriaCliente.push(dctNuevoIndicador);
            $('#slcCategoriaCliente').val('').trigger('change.select2');
            $('#slcIndicadorCategoriaCliente').val('').trigger('change.select2');
            $('#iptObjetivoCategoriaCliente').val('');
            $('#iptMetaGeneralCategoriaCliente').val('');
            $('#iptMetaAcumuladaCategoriaCliente').val('');
            $('#iptMetaRestanteCategoriaCliente').val('');
            $('#rowMetaGeneralCategoriaCliente').attr('hidden', true);
            $('#rowGraficoCategoriaCliente').attr('hidden', true);
            dctPlaneacionComercial.fncIndicadoresCategoriaClientetbl();
        }
        
    });

    // Editar indicador de tabla categoría cliente
    $('#tblIndicadorCategoriaCliente tbody').on('click', 'a[rel="edit"]', function () {
        var tr = tblIndicadorCategoriaCliente.cell($(this).closest('td, li')).index();
        var data = tblIndicadorCategoriaCliente.row(tr.row).data();
        $.each(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstTablaCategoriaCliente, function (pos, value) {
            if(data == value){
                dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstTablaCategoriaCliente.splice(pos, 1);
            }
        });
        $('#slcCategoriaCliente').val(data.intSubset).trigger('change.select2');
        $('#slcIndicadorCategoriaCliente').val(data.intIndicador).trigger('change.select2');
        $('#iptObjetivoCategoriaCliente').val(data.fltObjetivoIndicador);
        $('#rowMetaGeneralCategoriaCliente').attr('hidden', false);
        $('#tblIndicadorCategoriaCliente').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstTablaCategoriaCliente).draw();
        fncRetornarDataGraficoCategoriaCliente();
    });

    // Eliminar indicador de tabla categoría cliente
    $('#tblIndicadorCategoriaCliente tbody').on('click', 'a[rel="delete"]', function (e) {
        e.preventDefault();
        var tr = tblIndicadorCategoriaCliente.cell($(this).closest('td, li')).index();
        var data = tblIndicadorCategoriaCliente.row(tr.row).data();
        fncMensajeAlertamns('Eliminar indicador', '¿Está seguro de eliminar este indicador?', function () {
            $.each(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstTablaCategoriaCliente, function (pos, value) {
                if(data == value){
                    dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstTablaCategoriaCliente.splice(pos, 1);
                }
            });
            $('#tblIndicadorCategoriaCliente').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstTablaCategoriaCliente).draw();    
        })
    });
    
    // Evento cuando collapse de asesor comercial se muestra
    $('#cllAsesor').on('shown.bs.collapse', function () {
        dctPlaneacionComercial.dctIndicadoresAsesorComercial.bolCollapseAsesorComercial = true;
    });
    
    // Evento cuando collapse de asesor comercial se oculta
    $('#cllAsesor').on('hidden.bs.collapse', function () {
        dctPlaneacionComercial.dctIndicadoresAsesorComercial.bolCollapseAsesorComercial = false;
    });

    // Ejecutar consulta para establecer indicadores por asesor comercial
    $('#btnCollapseAsesorComercial').on('click', function (e) {
        e.stopPropagation();
        if (dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales.length >= 1){
            if (dctPlaneacionComercial.dctIndicadoresAsesorComercial.bolCollapseAsesorComercial == false){
                $('#cllAsesor').collapse('show');
                return;
            }
            else{
                $('#cllAsesor').collapse('hide');
                return;
            }
        }
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'btnConsultarAsesoresComercialesjsn');
        $.ajax({
            url: window.location.pathname,
            data: jsnParametros,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                if (request.hasOwnProperty('strError')) {   
                    fncMensajeErrormns(request.strError);
                    return;
                }
                dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales = request.lstSelectAsesorComercial;
                $("#slcAsesorComercial").select2({
                    theme: "bootstrap4",
                    placeholder: "Seleccione un asesor",
                    language: 'es',
                    allowClear: true,
                    data: request.lstSelectAsesorComercial
                });
                $("#slcIndicadorAsesorComercial").select2({
                    theme: "bootstrap4",
                    placeholder: "Seleccione un indicador",
                    language: 'es',
                    allowClear: true,
                });
                $('#slcAsesorComercial').val('').trigger('change.select2');
                $('#slcIndicadorAsesorComercial').val('').trigger('change.select2');
                $('#cllAsesor').collapse('show');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    });

    // Ejecutar consulta de indicador por asesor comercial
    $('#slcIndicadorAsesorComercial').on('select2:select', function (e) {
        e.preventDefault();
        var strIndicadorAsesorComercial = $('#slcIndicadorAsesorComercial').val();
        var strAsesorComercial = $('#slcAsesorComercial :selected').text();
        var intIndicadorAsesorComercial = $('#slcIndicadorAsesorComercial :selected').text();
        if(strIndicadorAsesorComercial == ''){
            fncMensajeErrormns('Seleccione una asesor comercial');
            $('#slcIndicadorAsesorComercial').val('').trigger('change.select2');
            return;
        }
        else if(intIndicadorAsesorComercial == 'Total_Sales_Objetive'){
            if($('#iptVentaTotal').val() == ''){
                fncMensajeErrormns('Para establecer indicador de venta total por asesor comercial, debe establecer indicador general de venta total');
                $('#slcIndicadorAsesorComercial').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorAsesorComercial == 'Customer_Retention_Rate'){
            if($('#iptVentasNuevas').val() == ''){
                fncMensajeErrormns('Para establecer indicador de ventas nuevas por asesor comercial, debe establecer indicador general de ventas nuevas');
                $('#slcIndicadorAsesorComercial').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorAsesorComercial == 'Sales_Deepening'){
            if($('#iptProfundizacionClientes').val() == ''){
                fncMensajeErrormns('Para establecer indicador de profundización de ventas por asesor comercial, debe establecer indicador general de profundización de ventas');
                $('#slcIndicadorAsesorComercial').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorAsesorComercial == 'New_Customers'){
            if($('#iptClientesNuevos').val() == ''){
                fncMensajeErrormns('Para establecer indicador de clientes nuevos por asesor comercial, debe establecer indicador general de clientes nuevos');
                $('#slcIndicadorAsesorComercial').val('').trigger('change.select2');
                return;
            }
        }
        else if(intIndicadorAsesorComercial == 'Margin'){
            if($('#iptMargenVenta').val() == ''){
                fncMensajeErrormns('Para establecer indicador de margén de venta por asesor comercial, debe establecer indicador general de margén de venta');
                $('#slcIndicadorAsesorComercial').val('').trigger('change.select2');
                return;
            }
        }
        if (dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales.length >= 1){
            $.each(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales, function (pos, value) {
                if(strAsesorComercial == value.strSubset && intIndicadorAsesorComercial == value.strIndicador){
                    fncMensajeConfirmacionmns('Alerta', 'Ya se encuentra en la tabla esta asesor comercial con este indicador ¿desea eliminar el actual y establecerlo de nuevo?',
                    function () {
                        dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales.splice(pos, 1);
                        $('#tblIndicadorAsesorComercial').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstAsesoresComerciales).draw();
                        $('#iptObjetivoAsesorComercial').focus();
                        fncRetornarDataGraficoAsesorComercial();
                        return;
                    }, 
                    function () {
                        $('#slcAsesorComercial').val('').trigger('change.select2');
                        $('#slcIndicadorAsesorComercial').val('').trigger('change.select2');
                        $('#iptObjetivoAsesorComercial').val('');
                        $('#iptMetaGeneralAsesorComercial').val('');
                        $('#iptMetaAcumuladaAsesorComercial').val('');
                        $('#iptMetaRestanteAsesorComercial').val('');
                        $('#rowMetaGeneralAsesorComercial').attr('hidden', true);
                        $('#rowGraficoAsesorComercial').attr('hidden', true);
                        return;
                    });
                    return;
                }
                else{
                    fncRetornarDataGraficoAsesorComercial();
                }
            });
            return;
        }
        fncRetornarDataGraficoAsesorComercial();
    });
    
    // Agregar indicador a la tabla de asesores comerciales
    $('#frmAsesorComercial').on('submit', function (e) {
        e.preventDefault();
        var intAsesorComercial = $('#slcAsesorComercial').val();
        var strAsesorComercial = $('#slcAsesorComercial :selected').text();
        var fltObjetivoIndicador = parseFloat($('#iptObjetivoAsesorComercial').val()).toFixed(2);
        var intIndicadorAsesorComercial = $('#slcIndicadorAsesorComercial').val();
        var strIndicadorAsesorComercial = $('#slcIndicadorAsesorComercial :selected').text();
        var fltMetaRestanteAsesorComercial = $('#iptMetaRestanteAsesorComercial').val();
        var strObjetivoIndicador = fltObjetivoIndicador.toString()
        var strMetaRestanteAsesorComercial = fltMetaRestanteAsesorComercial.toString()
        if(strObjetivoIndicador.length >= strMetaRestanteAsesorComercial.length ){
            if(fltObjetivoIndicador > fltMetaRestanteAsesorComercial){
                fncMensajeErrormns('No puede establecer una meta para este indicador mayor que la meta general, por favor valide el recuadro de meta restante');
                return;
            }
        }
        dctNuevoIndicador = {
            'strSet': 'Adviser',
            'intSubset': intAsesorComercial,
            'strSubset': strAsesorComercial,
            'intIndicador': intIndicadorAsesorComercial,
            'strIndicador': strIndicadorAsesorComercial,
            'fltObjetivoIndicador': parseFloat(fltObjetivoIndicador).toFixed(2)
        }
        if(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstTablaAsesorComercial.length >= 1){
            dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstTablaAsesorComercial.push(dctNuevoIndicador);
            $('#slcAsesorComercial').val('').trigger('change.select2');
            $('#slcIndicadorAsesorComercial').val('').trigger('change.select2');
            $('#iptObjetivoAsesorComercial').val('');
            $('#iptMetaGeneralAsesorComercial').val('');
            $('#iptMetaAcumuladaAsesorComercial').val('');
            $('#iptMetaRestanteAsesorComercial').val('');
            $('#rowMetaGeneralAsesorComercial').attr('hidden', true);
            $('#rowGraficoAsesorComercial').attr('hidden', true);
            $('#tblIndicadorAsesorComercial').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstTablaAsesorComercial).draw();
        }
        else{
            dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstTablaAsesorComercial.push(dctNuevoIndicador);
            $('#slcAsesorComercial').val('').trigger('change.select2');
            $('#slcIndicadorAsesorComercial').val('').trigger('change.select2');
            $('#iptObjetivoAsesorComercial').val('');
            $('#iptMetaGeneralAsesorComercial').val('');
            $('#iptMetaAcumuladaAsesorComercial').val('');
            $('#iptMetaRestanteAsesorComercial').val('');
            $('#rowMetaGeneralAsesorComercial').attr('hidden', true);
            $('#rowGraficoAsesorComercial').attr('hidden', true);
            dctPlaneacionComercial.fncIndicadoresAsesorComercialtbl();
        }
        
    });
    
    // Editar indicador de tabla asesor comercial
    $('#tblIndicadorAsesorComercial tbody').on('click', 'a[rel="edit"]', function () {
        var tr = tblIndicadorAsesorComercial.cell($(this).closest('td, li')).index();
        var data = tblIndicadorAsesorComercial.row(tr.row).data();
        $.each(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstTablaAsesorComercial, function (pos, value) {
            if(data == value){
                dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstTablaAsesorComercial.splice(pos, 1);
            }
        });
        $('#slcAsesorComercial').val(data.intSubset).trigger('change.select2');
        $('#slcIndicadorAsesorComercial').val(data.intIndicador).trigger('change.select2');
        $('#iptObjetivoAsesorComercial').val(data.fltObjetivoIndicador);
        $('#rowMetaGeneralAsesorComercial').attr('hidden', false);
        $('#tblIndicadorAsesorComercial').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstTablaAsesorComercial).draw();
        fncRetornarDataGraficoAsesorComercial();
    });

    // Eliminar indicador de tabla asesor comercial
    $('#tblIndicadorAsesorComercial tbody').on('click', 'a[rel="delete"]', function (e) {
        e.preventDefault();
        var tr = tblIndicadorAsesorComercial.cell($(this).closest('td, li')).index();
        var data = tblIndicadorAsesorComercial.row(tr.row).data();
        fncMensajeAlertamns('Eliminar indicador', '¿Está seguro de eliminar este indicador?', function () {
            $.each(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstTablaAsesorComercial, function (pos, value) {
                if(data == value){
                    dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstTablaAsesorComercial.splice(pos, 1);
                }
            });
            $('#tblIndicadorAsesorComercial').DataTable().clear().rows.add(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstTablaAsesorComercial).draw();    
        })
    });

    // Funcíon que valida si se estableció almenos un indicador para ser guardado
    function fncSumarTotal(dctIndicadores) {
        fltTotalIndicadores = 0.00;
        $.each(dctIndicadores, function (pos, dict) {
            if(dict.fltObjetivo != ''){
                fltTotalIndicadores += parseFloat(dict.fltObjetivo);
            }
        });
        return fltTotalIndicadores;
    }
    
    $('#btnGuardarPlaneacion').on('click', function (e) {
        e.preventDefault();
        var fltVentaTotal = $('#iptVentaTotal').val();
        var fltVentasNuevas = $('#iptVentasNuevas').val();
        var fltProfundizacionClientes = $('#iptProfundizacionClientes').val();
        var fltClientesNuevos = $('#iptClientesNuevos').val();
        var fltMargenVenta = $('#iptMargenVenta').val();
        var lstIndicadoresGenerales = [
            {'strIndicador': 'Total_Sales_Objetive', 'fltObjetivo': fltVentaTotal},
            {'strIndicador': 'Customer_Retention_Rate', 'fltObjetivo': fltVentasNuevas},
            {'strIndicador': 'Sales_Deepening', 'fltObjetivo': fltProfundizacionClientes},
            {'strIndicador': 'New_Customers', 'fltObjetivo': fltClientesNuevos},
            {'strIndicador': 'Margin', 'fltObjetivo': fltMargenVenta}
        ]
        fltTotal = fncSumarTotal(lstIndicadoresGenerales);
        if (fltTotal == 0){
            fncMensajeErrormns('No ha establecido indicadores, para guardar su planeación debe establecer almenos un indicador');
            return;
        }
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'btnGuardarPlaneacionComercialjsn');
        jsnParametros.append('lstIndicadoresGenerales', JSON.stringify(lstIndicadoresGenerales));
        jsnParametros.append('lstTablaCiudades', JSON.stringify(dctPlaneacionComercial.dctIndicadoresCiudades.lstTablaCiudades));
        jsnParametros.append('lstTablaZonas', JSON.stringify(dctPlaneacionComercial.dctIndicadoresZonas.lstTablaZonas));
        jsnParametros.append('lstTablaCategoriaCliente', JSON.stringify(dctPlaneacionComercial.dctIndicadoresCategoriaCliente.lstTablaCategoriaCliente));
        jsnParametros.append('lstTablaAsesorComercial', JSON.stringify(dctPlaneacionComercial.dctIndicadoresAsesorComercial.lstTablaAsesorComercial));
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Está seguro de guardar el registro?', parameters, function (response) {
                location.href = '/planeacion/planeacion_comercial_historico/';
        });
    });

});