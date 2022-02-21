$(function () {
    Highcharts.chart('containerSale', {
        chart: {
            type: 'line'
        },
        title: {
            text: 'Monthly Average Temperature'
        },
        subtitle: {
            text: 'Source: WorldClimate.com'
        },
        xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
            title: {
                text: 'Temperature (°C)'
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: false
            }
        },
        series: [{
            name: 'Tokyo',
            data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
        }, {
            name: 'London',
            data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
        }]
    });
});





/*var cityDataTable;
var forecastChart;
var seriesOptions = [],
    seriesCounter = 0,
    names = ['MSFT', 'AAPL', 'GOOG'];

var comercial_planning = {
    var: {
        perc_act: 0,
        perc_goal: 0,
        monet_goal: 0.00,
        monet_real: 0.00,
        
        deepClientIndex: 0,
        newClientIndex: 0,

        forecastTable: [],
        forecastGraph: [],

        dataActTable: [],
        dataStaTable: [],

        cityTable: [],
        zoneoneTable: [],
        advisorTable: [],
        custCatTable: [],
        customerTable: []
    },

    getGeneralGraph: function () {
        Highcharts.chart('containerSale', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Proyección de ventas Diciembre'
            },
            xAxis: {
                categories: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            },
            yAxis: {
                title: {
                    text: 'Ventas Millones de $'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: false
                }
            },
            series: [{
                name: 'Pronóstico',
                data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
            }, {
                name: 'Real',
                data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
            }]
        });
    }, 

    getIndicatorGraph: function () {
        Highcharts.chart('containerIndicator', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Proyección de ventas Diciembre'
            },
            xAxis: {
                categories: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            },
            yAxis: {
                title: {
                    text: 'Ventas Millones de $'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: false
                }
            },
            series: [{
                name: 'Pronóstico',
                data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
            }, {
                name: 'Real',
                data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
            }]
        });
    },

    getIndicator2Graph: function () {
        Highcharts.chart('containerIndicator2', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Proyección de ventas Diciembre'
            },
            xAxis: {
                categories: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            },
            yAxis: {
                title: {
                    text: 'Ventas Millones de $'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: false
                }
            },
            series: [{
                name: 'Pronóstico',
                data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
            }, {
                name: 'Real',
                data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
            }]
        });
    },

    calc_perc_inc: function () {
        if(this.var.perc_act == 1){
        goal = $('input[name="monetary_goal"]').val()
        inc_calc = parseFloat(((goal - this.var.monet_real)/this.var.monet_real) * 100).toFixed(2);
        this.var.perc_goal = inc_calc;
        $('input[name="perc_goal"]').val(inc_calc + ' %');
        }
    },

    // Cargar pronóstico
    getForecastTable: function () {
        forecastTableDT = $('#dataForecast').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ],
            searching: false,
            paging: false,
            data: this.var.forecastTable,
            columns: [
                { "data": "month"},
                { "data": "week"},
                { "data": "sale_proj"},
            ],
            columnDefs: [
                {
                    targets: [-1, -2, -3],
                    class: 'text-center',
                },
            ],
            initComplete: function(settings, json) {
            }
        });
    },

    getForecastGraph: function () {
        Highcharts.chart('containerForecast', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Pronóstico de ventas'
            },
            subtitle: {
                text: 'Gráfico'
            },
            xAxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            },
            yAxis: {
                title: {
                    text: 'Venta ($)'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: false
                }
            },
            series: [{
                name: 'Historico',
                data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
            }, {
                name: 'Pronóstico',
                data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 10.3, 6.6, 4.8]
            }]
        });
    },

    // Agregar actividad
    add_activity: function (item) {
        this.var.dataActTable.push(item);
        this.get_act_table();
    },

    // Calcular % de actividades vs meta
    calculate_activity: function () {
        var deepInd = 0.00;
        var newCustInd = 0.00;
        $.each(this.var.dataActTable, function (pos, dict) {
            deepInd += parseFloat(dict.deepInd);
            newCustInd += parseFloat(dict.newInd);
        $('input[name="actAcumDeep"]').val(deepInd.toFixed(2));
        $('input[name="actAcumNew"]').val(newCustInd.toFixed(2));
        });
    },

    // Cargar tabla de actividades
    get_act_table: function () {
        actTable = $('#actTable').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            dom: 'Bfrtip',
            buttons: [
                'copy', 'excel', 'pdf', 'print'
            ],
            searching: false,
            paging: false,
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
            data: this.var.dataActTable,
            columns: [
                { "data": "name"},
                { "data": "desc"},
                { "data": "deepInd"},
                { "data": "newInd"},
                { "data": "dateInit"},
                { "data": "dateEnd"},
            ],
            columnDefs: [
                {
                    targets: [-1, -2, -3],
                    class: 'text-center',
                },
            ],
            initComplete: function(settings, json) {
            }
        });
    },
    
    // Cargar tabla de estacionalidades
    get_sta_table: function () {
        staTable = $('#staTable').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ],
            searching: false,
            paging: false,
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
            data: this.var.dataStaTable,
            columns: [
                { "data": "name"},
                { "data": "desc"},
                { "data": "growth"},
                { "data": "decrease"},
                { "data": "dateInit"},
                { "data": "dateEnd"},
            ],
            columnDefs: [
                {
                    targets: [-1, -2, -3],
                    class: 'text-center',
                },
            ],
            initComplete: function(settings, json) {
            }
        }); 
    },

    // Agregar estacionalidad
    add_seasonality: function (item) {
        this.var.dataStaTable.push(item);
        this.get_sta_table();
    },

    // Cargar tabla de ciudades    
    getCityTable: function () {
        cityDataTable = $('#cityDataTable').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ],
            searching: false,
            paging: false,
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
            data: this.var.cityTable,
            columns: [
                { 'data': "city"},
                { 'data': "hist"},
                { 'data': "sale_proj"},
                { 'data': "goal_mon"},
                { 'data': "goal_per"},
            ],
            columnDefs: [
                {
                    targets: [1, 2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$ '+parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="goalMonCity" class="form-control form-control-sm input-sm" autocomplete="off" value=" ">';
                    }
                },
                {
                    targets: [4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="goalPercCity" class="form-control form-control-sm input-sm" autocomplete="off" value=" ">';
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="goalMonCity"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1,
                    prefix: '$',
                });

                $(row).find('input[name="goalPercCity"]').TouchSpin({
                    min: 1,
                    max: 1000,
                    step: 1,
                    postfix: '%',
                });
            
            },
            initComplete: function(settings, json) {
            }
        });
    },

    calculate_city: function () {
        var goalCityMon = 0.00;
        //var goalCityPer = 0.00;
        $.each(this.var.cityTable, function (pos, dict) {
            dict.goal_per = parseFloat(((dict.goal_mon - dict.hist)/dict.hist) * 100).toFixed(2);
            //goalCityMon += parseFloat(dict.goal_mon);
            //goalCityPer += parseFloat(dict.goal_per);
        //$('input[name="goalMonCity"]').val(goalCityMon.toFixed(2));
        //$('input[name="goalPercCity"]').val(goalCityPer.toFixed(2));
        }); 
        console.log(this.var.cityTable);
    },

    getCityGraph: function () {
        Highcharts.chart('containerCity', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Browser market shares in January, 2018'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            accessibility: {
                point: {
                    valueSuffix: '%'
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            series: [{
                name: 'Brands',
                colorByPoint: true,
                data: [{
                    name: 'Chrome',
                    y: 61.41,
                    sliced: true,
                    selected: true
                }, {
                    name: 'Internet Explorer',
                    y: 11.84
                }, {
                    name: 'Firefox',
                    y: 10.85
                }, {
                    name: 'Edge',
                    y: 4.67
                }, {
                    name: 'Safari',
                    y: 4.18
                }, {
                    name: 'Sogou Explorer',
                    y: 1.64
                }, {
                    name: 'Opera',
                    y: 1.6
                }, {
                    name: 'QQ',
                    y: 1.2
                }, {
                    name: 'Other',
                    y: 2.61
                }]
            }]
        });        
    },

    get_zone_data: function () {
        zoneTable = $('#dataZone').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ],
            searching: false,
            paging: false,
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
            columns: [
                { title: "Zona"},
                { title: "Real"},
                { title: "Pronóstico"},
                { title: "Meta"},
            ],
            columnDefs: [
                {
                    targets: [-1, -2, -3],
                    class: 'text-center',
                },
            ],
            initComplete: function(settings, json) {
            }
        });
        Highcharts.chart('containerZone', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Browser market shares in January, 2018'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            accessibility: {
                point: {
                    valueSuffix: '%'
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            series: [{
                name: 'Brands',
                colorByPoint: true,
                data: [{
                    name: 'Chrome',
                    y: 61.41,
                    sliced: true,
                    selected: true
                }, {
                    name: 'Internet Explorer',
                    y: 11.84
                }, {
                    name: 'Firefox',
                    y: 10.85
                }, {
                    name: 'Edge',
                    y: 4.67
                }, {
                    name: 'Safari',
                    y: 4.18
                }, {
                    name: 'Sogou Explorer',
                    y: 1.64
                }, {
                    name: 'Opera',
                    y: 1.6
                }, {
                    name: 'QQ',
                    y: 1.2
                }, {
                    name: 'Other',
                    y: 2.61
                }]
            }]
        });        
    },
    
    get_advisor_data: function () {
        advTable = $('#dataAdvisor').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ],
            searching: false,
            paging: false,
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
            columns: [
                { title: "Asesor"},
                { title: "Real"},
                { title: "Pronóstico"},
                { title: "Meta"},
            ],
            columnDefs: [
                {
                    targets: [-1, -2, -3],
                    class: 'text-center',
                },
            ],
            initComplete: function(settings, json) {
            }
        });
        Highcharts.chart('containerAdvisor', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Browser market shares in January, 2018'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            accessibility: {
                point: {
                    valueSuffix: '%'
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            series: [{
                name: 'Brands',
                colorByPoint: true,
                data: [{
                    name: 'Chrome',
                    y: 61.41,
                    sliced: true,
                    selected: true
                }, {
                    name: 'Internet Explorer',
                    y: 11.84
                }, {
                    name: 'Firefox',
                    y: 10.85
                }, {
                    name: 'Edge',
                    y: 4.67
                }, {
                    name: 'Safari',
                    y: 4.18
                }, {
                    name: 'Sogou Explorer',
                    y: 1.64
                }, {
                    name: 'Opera',
                    y: 1.6
                }, {
                    name: 'QQ',
                    y: 1.2
                }, {
                    name: 'Other',
                    y: 2.61
                }]
            }]
        });        
    },

    get_cust_cat_data: function () {
        custCatTable = $('#dataCustCat').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ],
            searching: false,
            paging: false,
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
            columns: [
                { title: "Categoría cliente"},
                { title: "Real"},
                { title: "Pronóstico"},
                { title: "Meta"},
            ],
            columnDefs: [
                {
                    targets: [-1, -2, -3],
                    class: 'text-center',
                },
            ],
            initComplete: function(settings, json) {
            }
        });
        Highcharts.chart('containerCustCat', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Browser market shares in January, 2018'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            accessibility: {
                point: {
                    valueSuffix: '%'
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            series: [{
                name: 'Brands',
                colorByPoint: true,
                data: [{
                    name: 'Chrome',
                    y: 61.41,
                    sliced: true,
                    selected: true
                }, {
                    name: 'Internet Explorer',
                    y: 11.84
                }, {
                    name: 'Firefox',
                    y: 10.85
                }, {
                    name: 'Edge',
                    y: 4.67
                }, {
                    name: 'Safari',
                    y: 4.18
                }, {
                    name: 'Sogou Explorer',
                    y: 1.64
                }, {
                    name: 'Opera',
                    y: 1.6
                }, {
                    name: 'QQ',
                    y: 1.2
                }, {
                    name: 'Other',
                    y: 2.61
                }]
            }]
        });        
    },

    get_cust_data: function () {
        custTable = $('#dataCust').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ],
            searching: false,
            paging: false,
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
            columns: [
                { title: "Cliente"},
                { title: "Real"},
                { title: "Pronóstico"},
                { title: "Meta"},
            ],
            columnDefs: [
                {
                    targets: [-1, -2, -3],
                    class: 'text-center',
                },
            ],
            initComplete: function(settings, json) {
            }
        });
        Highcharts.chart('containerCust', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Browser market shares in January, 2018'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            accessibility: {
                point: {
                    valueSuffix: '%'
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            series: [{
                name: 'Brands',
                colorByPoint: true,
                data: [{
                    name: 'Chrome',
                    y: 61.41,
                    sliced: true,
                    selected: true
                }, {
                    name: 'Internet Explorer',
                    y: 11.84
                }, {
                    name: 'Firefox',
                    y: 10.85
                }, {
                    name: 'Edge',
                    y: 4.67
                }, {
                    name: 'Safari',
                    y: 4.18
                }, {
                    name: 'Sogou Explorer',
                    y: 1.64
                }, {
                    name: 'Opera',
                    y: 1.6
                }, {
                    name: 'QQ',
                    y: 1.2
                }, {
                    name: 'Other',
                    y: 2.61
                }]
            }]
        });        
    },
};

$(function () {

    comercial_planning.getGeneralGraph();
    comercial_planning.getIndicatorGraph();
    comercial_planning.getIndicator2Graph();



    // Obtener data para meta
    /*$(function get_data() {
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'get_data'
            },
            dataType: 'json',
        }).done(function (data) {
            week = data.total_week;
            msg = data.msg;
            if (!data.hasOwnProperty('last_planning')) {
                if(week == 0){
                    fncMensajeInformacionmns(msg);
                    comercial_planning.var.perc_goal = "";
                    return false;
                }else if(week > 0){
                    fncMensajeInformacionmns(msg);
                    $('input[name="perc_goal"]').removeAttr('type');
                    $('label[name="percLabelGoal"]').removeAttr('hidden');
                    $("input[name='perc_goal']").TouchSpin({
                        min: 0,
                        max: 100,
                        step: 1,
                        decimals: 1,
                        boostat: 5,
                        maxboostedstep: 10,
                        postfix: '%',
                    })
                    return false;
                }
            }
            inc_calc = parseFloat(((data.last_planning - data.last_sale)/data.last_sale) * 100).toFixed(2);
            comercial_planning.var.perc_goal = inc_calc;
            comercial_planning.var.monet_real = data.last_sale;
            comercial_planning.var.perc_act = 1;
            fncMensajeInformacionmns(msg);
            $('input[name="perc_goal"]').removeAttr('type');
            $('label[name="percLabelGoal"]').removeAttr('hidden');
            $('input[name="monetary_goal"]').val(data.last_planning);
            $("input[name='perc_goal']").val(inc_calc + ' %');
            $("input[name='perc_goal']").attr('readonly', true);

        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    });

    // Cargar touchspin para meta y función para calcular % de crecimiento
    $("input[name='monetary_goal']").TouchSpin({        
        min: 0,
        max: 10000000000000,
        stepinterval: 10000,
        maxboostedstep: 10000000,
        prefix: '$',
    }).on('change', function (){
        comercial_planning.calc_perc_inc();
    })
    
    // Función para establecer meta checkbutton
    $('.cbGoal').on('click', function () {
        cbValue = parseFloat($('.cbGoal').val());
        perc_goal = $('input[name="perc_goal"]').val();
        monetary_goal = $('input[name="monetary_goal"]').val();
        if(cbValue == 0){
        $('.cbGoal').val(1);
        $('input[name="perc_goal"]').attr('readonly', true);
        $('input[name="monetary_goal"]').attr('readonly', true);
        $('input[name="perc_deep_clients"]').focus();
        fncMensajeInformacionmns('Ingrese el valor total de la meta en los indicadores')
        } else if(cbValue == 1){
        $('.cbGoal').val(0);
        $('input[name="perc_goal"]').attr('readonly', false);
        $('input[name="monetary_goal"]').attr('readonly', false);
        }
    });

    // Cargar touchspin para indicador de clientes nuevos
    $("input[name='perc_new_clients']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
    })
    
    // Cargar touchspin para indicador de profundización de clientes
    $("input[name='perc_deep_clients']").TouchSpin({
        min: 0,
        max: 100,
        step: 1,
        decimals: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
    })

    // Función para establecer indicadores checkbutton
    $('.cbIndex').on('click', function () {
        cbValue = parseFloat($('.cbGoal').val());
        if(cbValue == 0){
            fncMensajeInformacionmns('Seleccione la opción "Establecer meta" antes de establecer indicadores')
            return false;
        }
        cbIndex = parseFloat($('.cbIndex').val());
        console.log(cbIndex);
        newCli = parseFloat($('input[name="perc_new_clients"]').val());
        profCli = parseFloat($('input[name="perc_deep_clients"]').val());
        indTotal = newCli + profCli;
        if(cbIndex == 0){
            if(comercial_planning.var.perc_goal === ''){
                $('.cbIndex').val(1);
                $('input[name="perc_deep_clients"]').attr('readonly', true);
                $('input[name="perc_new_clients"]').attr('readonly', true);
                comercial_planning.var.deepClientIndex = $('input[name="perc_deep_clients"]').val();
                comercial_planning.var.newClientIndex = $('input[name="perc_new_clients"]').val();
                fncMensajeInformacionmns('Ingrese las actividades para cumplimiento de meta y el % que representa en cada indicador')
                $('input[name="perc_new_clients"]').focus();
            }
            else if(indTotal < comercial_planning.var.perc_goal){
                fncMensajeInformacionmns('Los valores ingresados son menores que la meta')
                return false;
            }else if(indTotal > comercial_planning.var.perc_goal){
                fncMensajeInformacionmns('Los valores ingresados son mayores que la meta')
                return false;
            }
            $('.cbIndex').val(1);
            $('input[name="perc_deep_clients"]').attr('readonly', true);
            $('input[name="perc_new_clients"]').attr('readonly', true);
            comercial_planning.var.deepClientIndex = $('input[name="perc_deep_clients"]').val();
            comercial_planning.var.newClientIndex = $('input[name="perc_new_clients"]').val();
            fncMensajeInformacionmns('Ingrese las actividades para cumplimiento de meta y el % que representa en cada indicador')
            $('input[name="perc_new_clients"]').focus();
        } else if(cbIndex == 1){
            $('.cbIndex').val(0);
            $('input[name="perc_deep_clients"]').attr('readonly', false);
            $('input[name="perc_new_clients"]').attr('readonly', false);
        }
    });

    // Función para visualizar el pronóstico
    $('.btnForecast').on('click', function (e) {
        e.preventDefault();
        msgFalse = '';
        msgTrue = '';
        if (msgTrue === '' & msgFalse === '' ){
            if (comercial_planning.var.forecastTable.length === 0 ){
                $(function get_forecast() {
                    $.ajax({
                        url: window.location.pathname,
                        type: 'POST',
                        data: {
                            'action': 'get_forecast'
                        },
                        dataType: 'json',
                    }).done(function (data) {
                        if (!data.hasOwnProperty('forecast_table')) {
                            fncMensajeInformacionmns(data.msg);
                            msgFalse = data.msg;
                            // pendiente cerrar collapse de pronostico
                            return false;
                        }
                        comercial_planning.var.forecastTable = data.forecast_table;
                        //comercial_planning.var.forecastGraph = data.forecast_graph;
                        comercial_planning.getForecastTable();
                        comercial_planning.getForecastGraph();
                        fncMensajeInformacionmns(data.msg);
                        msgTrue = data.msg;
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {
            
                    });
                });    
            }
        }else if (msgFalse != '' ){
            fncMensajeInformacionmns(msgFalse)
            return false;
        }else if (msgTrue != '' ){
            comercial_planning.getForecastTable();
            comercial_planning.getForecastGraph();
        }
        
    });

    // Cargar touchspin para indicador de profundización en actividades
    $("input[name='indDeepCliAct']").TouchSpin({
        min: 0,
        max: 100,
        step: 1,
        decimals: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
    }).on('change', function (){
        
    }).val(0.00)
    
    // Cargar touchspin para indicador de clientes nuevos en actividades
    $("input[name='indNewCliAct']").TouchSpin({
        min: 0,
        max: 100,
        step: 1,
        decimals: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
    }).on('change', function (){
        
    }).val(0.00)

    // Cargar datetimepicker para fecha inicio de actividades
    $('#init_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD"),
    });
    
    // Cargar datetimepicker para fecha fin de actividades
    $('#end_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD"),
    });

    // Cargar touchspin para crecimiento de estacionalidades
    $("input[name='staCrec']").TouchSpin({
        min: 0,
        max: 100,
        step: 1,
        decimals: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
    }).on('change', function (){
        
    }).val(0.00)

    // Cargar touchspin para decrecimiento de estacionalidades
    $("input[name='staDec']").TouchSpin({
        min: 0,
        max: 100,
        step: 1,
        decimals: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
    }).on('change', function (){
        
    }).val(0.00)

    // Cargar datetimepicker para fecha inicio de estacionalidades
    $('#initDateSta').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD"),
    });
    
    // Cargar datetimepicker para fecha fin de estacionalidades
    $('#endDateSta').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD"),
    });

    // Función en boton ajustar manualmente meta
    $('.btnManual').on('click', function () {
        /*cbGoal = parseFloat($('.cbGoal').val());
        cbIndex = parseFloat($('.cbIndex').val());
        cbTotal = cbGoal + cbIndex;
        $('input[name="realDeep"]').val(comercial_planning.var.deepClientIndex);
        $('input[name="realNew"]').val(comercial_planning.var.newClientIndex);
        $('input[name="actAcumDeep"]').val(0);
        $('input[name="actAcumNew"]').val(0);
        if(cbTotal <= 1){
            fncMensajeInformacionmns('Debe establecer meta e indicadores antes de realizar el ajuste manual')
            return false;
        }
    });    

    // Función para visualizar la tabla de actividades creadas
    $('.btnActTable').on('click', function () {
        comercial_planning.get_act_table();
    });    
    
    // Función en boton agregar actividad
    $('.addAct').on('click', function () {
        nameAct = $('input[name="nameAct"]').val();
        descAct = $('input[name="descAct"]').val();
        indDeep = $('input[name="indDeepCliAct"]').val();
        indNew = $('input[name="indNewCliAct"]').val();
        initDate = $('input[name="initAct"]').val();
        endDate = $('input[name="endAct"]').val();
        item = {name: nameAct, desc: descAct, deepInd: indDeep, newInd: indNew, dateInit: initDate, dateEnd: endDate};
        comercial_planning.add_activity(item);
        $('input[name="nameAct"]').val('');
        $('input[name="descAct"]').val('');
        $('input[name="indDeepCliAct"]').val(0);
        $('input[name="indNewCliAct"]').val(0);
        $('input[name="initAct"]').val('');
        $('input[name="endAct"]').val('');
        comercial_planning.calculate_activity();
    });

    // Función para establecer actividades checkbutton
    $('.cbAct').on('click', function () {
        // cbValue = parseFloat($('.cbAct').val());
        realDeep = parseInt($('input[name="realDeep"]').val());
        realNew = parseInt($('input[name="realNew"]').val());
        acumDeep = parseInt($('input[name="actAcumDeep"]').val());
        acumNew = parseInt($('input[name="actAcumNew"]').val());
        if(comercial_planning.var.dataActTable.length === 0 ){
            fncMensajeInformacionmns('Debe agregar al menos una actividad ')
            return false;
        }else if(realDeep != acumDeep){
            fncMensajeInformacionmns('El porcentaje en el indicador de profundización debe ser igual al acumulado de sus actividades para este indicador')
            return false;
        }else if(realNew != acumNew){
            fncMensajeInformacionmns('El porcentaje en el indicador de clientes nuevos debe ser igual al acumulado de sus actividades para este indicador')
            return false;
        }
    });

    // Función para eliminar actividades creadas en la tabla
    $('.removeAct').on('click', function () {
        if(comercial_planning.var.dataActTable.length === 0 ) return false;
        fncMensajeAlertamns('Notificación', '¿Está seguro de eliminar todo?', function () {
            comercial_planning.var.dataActTable = [];
            $('input[name="actAcumDeep"]').val(0);
            $('input[name="actAcumNew"]').val(0);
            comercial_planning.get_act_table();
        });
    });
    
    // Función para visualizar la tabla de estacionalidades creadas
    $('.btnStaTable').on('click', function () {
        comercial_planning.get_sta_table();
    });

    // Función en boton agregar estacionalidad
    $('.addSta').on('click', function () {
        nameSta = $('input[name="staName"]').val();
        descSta = $('input[name="staDesc"]').val();
        crecSta = $('input[name="staCrec"]').val();
        decSta = $('input[name="staDec"]').val();
        initDate = $('input[name="initDateSta"]').val();
        endDate = $('input[name="endDateSta"]').val();
        item = {name: nameSta, desc: descSta, growth: crecSta, decrease: decSta, dateInit: initDate, dateEnd: endDate};
        comercial_planning.add_seasonality(item);
        $('input[name="staName"]').val('');
        $('input[name="staDesc"]').val('');
        $('input[name="staCrec"]').val(0);
        $('input[name="staDec"]').val(0);
        $('input[name="initDateSta"]').val('');
        $('input[name="endDateSta"]').val('');
    });

    // Función para eliminar estacionalidades creadas en la tabla
    $('.removeSta').on('click', function () {
        if(comercial_planning.var.dataStaTable.length === 0 ) return false;
        fncMensajeAlertamns('Notificación', '¿Está seguro de eliminar todo?', function () {
            comercial_planning.var.dataStaTable = [];
            comercial_planning.get_sta_table();
        });
    });

    // Función para establecer estacionalidades checkbutton
    $('.cbSta').on('click', function () {
        if(comercial_planning.var.dataStaTable.length === 0 ){
            fncMensajeInformacionmns('Debe agregar al menos una estacionalidad')
            return false;
        }
    });

    // Función para cargar pronóstico por ciudades y establecer meta por ciudad
    $('.cityRun').on('click', function (e) {
        e.preventDefault();
        msgFalse = '';
        msgTrue = '';
        if (msgTrue === '' & msgFalse === '' ){
            if (comercial_planning.var.cityTable.length === 0 ){
                $.ajax({
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'get_forecast_city'
                    },
                    dataType: 'json',
                }).done(function (data) {
                    if (!data.hasOwnProperty('table_city')) {
                        fncMensajeInformacionmns(data.msg);
                        msgFalse = data.msg;
                        return false;
                    }
                    comercial_planning.var.cityTable = data.table_city;
                    //comercial_planning.var.forecastGraph = data.forecast_graph;
                    comercial_planning.getCityTable();
                    comercial_planning.getCityGraph();
                    fncMensajeInformacionmns(data.msg);
                    msgTrue = data.msg;
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    alert(textStatus + ': ' + errorThrown);
                }).always(function (data) {
        
                });
            }

        }else if (msgFalse != '' ){
            fncMensajeInformacionmns(msgFalse)
            return false;
        }else if (msgTrue != '' ){
            comercial_planning.getCityTable();
            comercial_planning.getCityGraph();
        }
    });

    $('#cityDataTable tbody')
        /*.on('click', 'a[rel="remove"]', function () {
            var tr = tblProd.cell($(this).closest('td, li')).index();
            fncMensajeAlertamns('Notificación', '¿Está seguro de eliminar el producto?', function () {
                sales.items.products.splice(tr.row, 1);
                sales.list();
            });
        })
        .on('change', 'input[name="goalMonCity"]', function () {
            var goalMon = parseInt($(this).val());
            var tr = cityDataTable.cell($(this).closest('td, li')).index();
            comercial_planning.var.cityTable[tr.row].goal_mon = goalMon;
            comercial_planning.calculate_city();
            comercial_planning.getCityTable();
            //$('td:eq(4)', cityDataTable.row(tr.row).node()).html('$' + comercial_planning.var.cityTable[tr.row].goal_per.toFixed(2));
    });

    $('.zoneRun').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'forecast_zone',
            },
            dataType: 'json',
        }).done(function (data) {
            if(data.msj === 'No puede ejecutar este filtro'){
                fncMensajeErrormns(data)
                return false;
            }
            comercial_planning.get_zone_data();
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    });

    $('.advisorRun').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'forecast_advisor',
            },
            dataType: 'json',
        }).done(function (data) {
            if(data.msj === 'No puede ejecutar este filtro'){
                fncMensajeErrormns(data)
                return false;
            }
            comercial_planning.get_advisor_data();
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    });

    $('.catCustRun').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'forecast_cust_cat',
            },
            dataType: 'json',
        }).done(function (data) {
            if(data.msj === 'No puede ejecutar este filtro'){
                fncMensajeErrormns(data)
                return false;
            }
            comercial_planning.get_cust_cat_data();
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    });

    $('.custRun').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'forecast_cust',
            },
            dataType: 'json',
        }).done(function (data) {
            if(data.msj === 'No puede ejecutar este filtro'){
                fncMensajeErrormns(data)
                return false;
            }
            comercial_planning.get_cust_data();
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    });

    $('.purchasePlan').on('click', function (e) {
        e.preventDefault();
        $('#myModal').modal('show');
    });    

});*/