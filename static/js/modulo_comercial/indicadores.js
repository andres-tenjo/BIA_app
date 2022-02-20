$(function () {
    
    Highcharts.chart('salesChart', {
        chart: {
            type: 'areaspline'
        },
        title: {
            text: 'Indicador de cumplimiento en ventas por asesor'
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
                text: 'Ventas'
            }
        },
        tooltip: {
            shared: true,
            valueSuffix: ' Millones'
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
            name: 'Marco',
            data: [3.347, 3.152, 3.209, 3.206]
        }, {
            name: 'Eliecer',
            data: [3.100, 2.855, 2.925, 3.205]
        }]
    });
    Highcharts.chart('margenSales', {
        chart: {
            type: 'line'
        },
        title: {
            text: 'Margen de ventas por categoría de productos'
        },
        xAxis: {
            categories: ['Enero',
            'Febrero',
            'Marzo',
            'Abril']
        },
        yAxis: {
            title: {
                text: 'Margen %'
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
            name: 'Comisionistas',
            data: [7.0, 6.9, 9.5, 14.5]
        }, {
            name: 'Cuentas Claves',
            data: [17.3, 18.6, 17.9, 16.9]
        }, {
            name: 'Empresarial',
            data: [16.2, 17.2, 17.7, 18.3]
        }, {
            name: 'Horecas',
            data: [13.5, 14.1, 13.6, 13.8]
        }, {
            name: 'Lager',
            data: [14.9, 14.4, 15.3, 14.5]
        }, {
            name: 'Mayoristas',
            data: [13.0, 11.2, 11.2, 12.4]
        }]
    });
    
    Highcharts.chart('newClient', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Clientes nuevos por ciudad'
        },
        xAxis: {
            categories: [
                'Enero',
                'Febrero',
                'Marzo',
                'Abril',
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Nuevos clientes'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} clientes</b></td></tr>',
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
            name: 'Bogotá',
            data: [15, 17, 10, 12]
    
        }, {
            name: 'Medellin',
            data: [8, 7, 9, 9]
    
        }, {
            name: 'Cali',
            data: [4, 3, 3, 4]
    
        }, {
            name: 'Barranquilla',
            data: [4, 5, 3, 3]
    
        }]
    });

    Highcharts.chart('lostClient', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Clientes perdidos por ciudad'
        },
        xAxis: {
            categories: [
                'Enero',
                'Febrero',
                'Marzo',
                'Abril',
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Nuevos clientes'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} clientes</b></td></tr>',
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
            name: 'Bogotá',
            data: [7, 5, 5, 6]
    
        }, {
            name: 'Medellin',
            data: [3, 3, 2, 4]
    
        }, {
            name: 'Cali',
            data: [2, 1, 1, 2]
    
        }, {
            name: 'Barranquilla',
            data: [1, 3, 2, 2]
    
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
                        name: "Visita toma pedido",
                        y: 92.74,
                        drilldown: "Visita"
                    },
                    {
                        name: "Llamada toma pedido",
                        y: 87.57,
                        drilldown: "Llamada"
                    },
                    {
                        name: "Visita cliente",
                        y: 80.23,
                        drilldown: "Visita"
                    },
                    {
                        name: "Llamada cliente",
                        y: 89.58,
                        drilldown: "Llamada"
                    }
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

    Highcharts.chart('convRate', {
        chart: {
            zoomType: 'xy'
        },
        title: {
            text: 'Promedio de conversión de prospectos a clientes'
        },
        xAxis: [{
            categories: ['Jan', 'Feb', 'Mar', 'Apr'],
            crosshair: true
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}°%',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: 'Promedio',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            }
        }, { // Secondary yAxis
            title: {
                text: 'Clientes',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                format: '{value}',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true
        }],
        tooltip: {
            shared: true
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 100,
            floating: true,
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || // theme
                'rgba(255,255,255,0.25)'
        },
        series: [{
            name: 'Meses',
            type: 'column',
            yAxis: 1,
            data: [34, 29, 31, 25],
            tooltip: {
                valueSuffix: ''
            }
    
        }, {
            name: 'Promedio',
            type: 'spline',
            data: [30, 30, 30, 30],
            tooltip: {
                valueSuffix: '%'
            }
        }]
    });

});
