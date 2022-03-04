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

}



$(function () {
    
    // Ejecutar consulta de histórico  para gráficar indicadores generales
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
        },
        error: function (jqXHR, textStatus, errorThrown) {
            fncMensajeErrormns(errorThrown + ' ' + textStatus);
        }
    });

    fncCargarLibreriaTouchSpinFormatoEntero();
    fncCargarLibreriaTouchSpinFormatoDecimal();
    fncCargarLibreriaTouchSpinFormatoMoneda();
    
    // Consultar si existe 1 o más ciudades para la base de datos de clientes
    $('#btnCollapseCiudad').on('click', function () {
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
                
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    });
});