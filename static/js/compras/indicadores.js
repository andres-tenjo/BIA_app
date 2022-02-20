$(function () {
    Highcharts.chart('fillRateChart', {

        chart: {
            type: 'column'
        },
    
        title: {
            text: 'Entregas a tiempo al cliente'
        },
    
        xAxis: {
            categories: ['Enero', 'Febrero', 'Marzo', 'Abril']
        },
    
        yAxis: {
            allowDecimals: false,
            min: 0,
            title: {
                text: 'Porcentaje cumplimiento'
            }
        },
    
        tooltip: {
            formatter: function () {
                return '<b>' + this.x + '</b><br/>' +
                    this.series.name + ': ' + this.y + '%' + '<br/>' +
                    'Total: ' + this.point.stackTotal + '%';
            }
        },
    
        plotOptions: {
            column: {
                stacking: 'normal'
            }
        },
    
        series: [{
            name: 'Incumplidas',
            data: [51, 48, 52, 50],
            stack: 'male'
        }, {
            name: 'Cumplidas',
            data: [49, 52, 48, 50],
            stack: 'male'
        }]
    });
    
    Highcharts.chart('perfectDelSupp', {

        chart: {
            type: 'column'
        },
    
        title: {
            text: 'Entregas completas al cliente'
        },
    
        xAxis: {
            categories: ['Enero', 'Febrero', 'Marzo', 'Abril']
        },
    
        yAxis: {
            allowDecimals: false,
            min: 0,
            title: {
                text: 'Porcentaje cumplimiento'
            }
        },
    
        tooltip: {
            formatter: function () {
                return '<b>' + this.x + '</b><br/>' +
                    this.series.name + ': ' + this.y + '%' + '<br/>' +
                    'Total: ' + this.point.stackTotal + '%';
            }
        },
    
        plotOptions: {
            column: {
                stacking: 'normal'
            }
        },
    
        series: [{
            name: 'Incumplidas',
            data: [22, 16, 19, 20],
            stack: 'male'
        }, {
            name: 'Cumplidas',
            data: [78, 84, 81, 80],
            stack: 'male'
        }]
    });

    Highcharts.chart('inventoryRotation', {
        chart: {
            type: 'areaspline'
        },
        title: {
            text: 'Rotación de inventario'
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 150,
            y: 100,
            floating: true,
            borderWidth: 1,
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF'
        },
        xAxis: {
            categories: [
                'Enero',
                'Febrero',
                'Marzo',
                'Abril'
            ],
            plotBands: [{ // visualize the weekend
                from: 4.5,
                to: 6.5,
                color: 'rgba(68, 170, 213, .2)'
            }]
        },
        yAxis: {
            title: {
                text: 'Días de rotación'
            }
        },
        tooltip: {
            shared: true,
            valueSuffix: ' Días'
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            areaspline: {
                fillOpacity: 0.5
            }
        },
        series: [{
            name: 'Días de inventario',
            data: [38, 47, 50, ]
        }]
    });

    Highcharts.chart('fullActivities', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Cumplimiento de actividades'
        },
        accessibility: {
            announceNewData: {
                enabled: true
            }
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: 'Porcentaje'
            }
    
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: '{point.y:.1f}%'
                }
            }
        },
    
        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> del total<br/>'
        },
    
        series: [
            {
                name: "Resultado",
                colorByPoint: true,
                data: [
                    {
                        name: "Generar oc",
                        y: 96.21,
                        drilldown: "Visita"
                    },
                    {
                        name: "Evaluar proveedores",
                        y: 91.23,
                        drilldown: "Visita"
                    },
                ]
            }
        ],
        drilldown: {
            series: [
                {
                    name: "Chrome",
                    id: "Chrome",
                    data: [
                        [
                            "v65.0",
                            0.1
                        ],
                        [
                            "v64.0",
                            1.3
                        ],
                        [
                            "v63.0",
                            53.02
                        ],
                        [
                            "v62.0",
                            1.4
                        ],
                        [
                            "v61.0",
                            0.88
                        ],
                        [
                            "v60.0",
                            0.56
                        ],
                        [
                            "v59.0",
                            0.45
                        ],
                        [
                            "v58.0",
                            0.49
                        ],
                        [
                            "v57.0",
                            0.32
                        ],
                        [
                            "v56.0",
                            0.29
                        ],
                        [
                            "v55.0",
                            0.79
                        ],
                        [
                            "v54.0",
                            0.18
                        ],
                        [
                            "v51.0",
                            0.13
                        ],
                        [
                            "v49.0",
                            2.16
                        ],
                        [
                            "v48.0",
                            0.13
                        ],
                        [
                            "v47.0",
                            0.11
                        ],
                        [
                            "v43.0",
                            0.17
                        ],
                        [
                            "v29.0",
                            0.26
                        ]
                    ]
                },
                {
                    name: "Firefox",
                    id: "Firefox",
                    data: [
                        [
                            "v58.0",
                            1.02
                        ],
                        [
                            "v57.0",
                            7.36
                        ],
                        [
                            "v56.0",
                            0.35
                        ],
                        [
                            "v55.0",
                            0.11
                        ],
                        [
                            "v54.0",
                            0.1
                        ],
                        [
                            "v52.0",
                            0.95
                        ],
                        [
                            "v51.0",
                            0.15
                        ],
                        [
                            "v50.0",
                            0.1
                        ],
                        [
                            "v48.0",
                            0.31
                        ],
                        [
                            "v47.0",
                            0.12
                        ]
                    ]
                },
                {
                    name: "Internet Explorer",
                    id: "Internet Explorer",
                    data: [
                        [
                            "v11.0",
                            6.2
                        ],
                        [
                            "v10.0",
                            0.29
                        ],
                        [
                            "v9.0",
                            0.27
                        ],
                        [
                            "v8.0",
                            0.47
                        ]
                    ]
                },
                {
                    name: "Safari",
                    id: "Safari",
                    data: [
                        [
                            "v11.0",
                            3.39
                        ],
                        [
                            "v10.1",
                            0.96
                        ],
                        [
                            "v10.0",
                            0.36
                        ],
                        [
                            "v9.1",
                            0.54
                        ],
                        [
                            "v9.0",
                            0.13
                        ],
                        [
                            "v5.1",
                            0.2
                        ]
                    ]
                },
                {
                    name: "Edge",
                    id: "Edge",
                    data: [
                        [
                            "v16",
                            2.6
                        ],
                        [
                            "v15",
                            0.92
                        ],
                        [
                            "v14",
                            0.4
                        ],
                        [
                            "v13",
                            0.1
                        ]
                    ]
                },
                {
                    name: "Opera",
                    id: "Opera",
                    data: [
                        [
                            "v50.0",
                            0.96
                        ],
                        [
                            "v49.0",
                            0.82
                        ],
                        [
                            "v12.1",
                            0.14
                        ]
                    ]
                }
            ]
        }
    });

});
