$(function () {
    
    Highcharts.chart('storageCapacity', {

        chart: {
            type: 'column'
        },
    
        title: {
            text: 'Capacidad de almacenamiento por bodega'
        },
    
        xAxis: {
            categories: ['Bodega Norte', 'Bodega Sur', 'Bodega Central']
        },
    
        yAxis: {
            allowDecimals: false,
            min: 0,
            title: {
                text: 'Capacidad'
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
            name: 'Disponible',
            data: [22, 16, 19],
            stack: 'male'
        }, {
            name: 'Ocupada',
            data: [90, 84, 78],
            stack: 'male'
        }]
    });

    Highcharts.chart('inventoryError', {

        title: {
            text: 'Error en la precisión de inventario'
        },
    
        yAxis: {
            title: {
                text: 'Porcentaje de error'
            }
        },
    
        xAxis: {
            categories: ['Enero', 'Febrero', 'Marzo', 'Abril']
        },
    
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },
    
        series: [{
            name: 'Bodega Norte',
            data: [6, 5, 7, 6]
        }, {
            name: 'Bodega Sur',
            data: [9, 12, 8, 7]
        }, {
            name: 'Bodega Central',
            data: [14, 10, 12, 11]
        }],
    
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }
    
    });

    Highcharts.chart('inventoryDrops', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Bajas de inventario'
        },
        xAxis: {
            categories: [
                'Enero',
                'Febrero',
                'Marzo',
                'Abril'
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Costo de bajas (mm)'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Bodega Norte',
            data: [49.9, 71.5, 64.4, 92.2]
    
        }, {
            name: 'Bodega Sur',
            data: [32.2, 29.2, 29.5, 31.4]
    
        }, {
            name: 'Bodega Central',
            data: [75.2, 72.8, 69.3, 41.4]
    
        }]
    });

    Highcharts.chart('deliveriesUnfulfilled', {

        chart: {
            type: 'column'
        },
    
        title: {
            text: 'Entregas incumplidas a clientes'
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
            data: [17, 19, 15, 20],
            stack: 'male'
        }, {
            name: 'Cumplidas',
            data: [83, 81, 85, 80],
            stack: 'male'
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
                        name: "Recepción",
                        y: 94.21,
                        drilldown: "Visita"
                    },
                    {
                        name: "Despacho",
                        y: 96.35,
                        drilldown: "Visita"
                    },
                    {
                        name: "Alistamiento",
                        y: 93.45,
                        drilldown: "Visita"
                    },
                    {
                        name: "Inventario",
                        y: 97.32,
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
