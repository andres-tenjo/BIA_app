dctHistoricoIndicadores = {
    
    dctHistoricoIndicadorGeneral:{
        lstCategorias: [],
        lstSeries: []
    },
    
    dctHistoricoIndicadorDetallado:{
        lstCategorias: [],
        lstSeries: []
    },

    // Función que carga el gráfico para el histórico del indicador general
    fncIndicadorGeneralHistorico: function () {
        Highcharts.chart('grfHistoricoGeneral', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Indicador general'
            },
            xAxis: {
                categories: dctHistoricoIndicadores.dctHistoricoIndicadorGeneral.lstCategorias
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
            series: dctHistoricoIndicadores.dctHistoricoIndicadorGeneral.lstSeries
        });
    },
    
    // Función que carga el gráfico para el histórico de indicador detallado
    fncIndicadorDetalladoHistorico: function () {
        Highcharts.chart('grfHistoricoGeneral', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Indicador detallado'
            },
            xAxis: {
                categories: dctHistoricoIndicadores.dctHistoricoIndicadorDetallado.lstCategorias
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
            series: dctHistoricoIndicadores.dctHistoricoIndicadorDetallado.lstSeries
        });
    },

}

$(function () {

    // Cargar librería select2 para select de indicadores
    fncCargarLibreriaSelect2('.slcIndicador', "Seleccione un indicador");
    
    // Cargar librería select2 para select de categorías
    fncCargarLibreriaSelect2('.selectCategoria', "Seleccione una categoría");
    
    // Función que ejecuta una consulta por categoría y retorna la data para el select de indicador detallado actual
    function fncConsultarCategoriaslc(jsnParametrosCategoria) {
        $('#slcCategoriaIndicadorDetalleActual').html('').select2({data: [{id: '', text: ''}]});
        $.ajax({
            url: window.location.pathname,
            data: jsnParametrosCategoria,
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
                $("#slcCategoriaIndicadorDetalleActual").select2({  
                    theme: "bootstrap4",
                    placeholder: "Seleccione una categoría",
                    language: 'es',
                    allowClear: true,
                    data: request.lstSelect
                });
                $("#slcCategoriaIndicadorDetalleActual").val('').trigger('change');
                $('#colDetalleCategoriaActual').attr('hidden', false);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    }

    // Función que ejecuta la consulta de un indicador detallado actual
    function fncConsultarIndicadorDetalladoActual(jsnParametrosDetalle, strCategoria) {
        $.ajax({
            url: window.location.pathname,
            data: jsnParametrosDetalle,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                if(request != false){
                    $('#colDetalleCategoriaActual').attr('hidden', false);
                    $('#colIndicadorDetalleActual').attr('hidden', false);
                    $('#rowMetaIndicadorDetalleActual').attr('hidden', false);
                    $('#iptObjetivoIndicadorDetalleActual').val('$ ' + request.fltObjetivo);
                    $('#iptRealIndicadorDetalleActual').val('$ ' + request.fltReal);
                    $('#lblCumplimientoDetalleActual').attr('hidden', false);
                    $('#rowBarCumplimientoIndicadorDetalleActual').attr('hidden', false);
                    $('#prgBarCumplimientoDetalleActual').css('width', request.strCumplimientoIndicador);
                    $('#txtProgressBarDetallado').text(request.strCumplimientoIndicador);
                }
                else if(request == false){
                    fncMensajeErrormns('El indicador en '+ strCategoria +'no se estableció en su planeación actual')
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });    
    }

    // Función que consulta el histórico de un indicador general
    function fncConsultarHistoricoIndicadorGeneralgrf(jsnParametrosHistoricoIndicador, strIndicador) {
        $.ajax({
            url: window.location.pathname,
            data: jsnParametrosHistoricoIndicador,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                dctHistoricoIndicadores.dctHistoricoIndicadorGeneral.lstCategorias = [];
                dctHistoricoIndicadores.dctHistoricoIndicadorGeneral.lstSeries = [];
                if(request != false){
                    dctHistoricoIndicadores.dctHistoricoIndicadorGeneral.lstCategorias = request[0];
                    dctHistoricoIndicadores.dctHistoricoIndicadorGeneral.lstSeries = request[1]
                    dctHistoricoIndicadores.fncIndicadorGeneralHistorico();
                    $('#rowGraficoHistoricoGeneral').attr('hidden', false);
                }
                else if(request == false){
                    fncMensajeErrormns('El indicador de '+ strIndicador + 'no tiene histórico')
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });    
    }

    // Función que ejecuta una consulta por categoría y retorna el detalle para el select de histórico detallado
    function fncConsultarCategoriasHistoricoslc(jsnParametrosCategoria) {
        $('#slcDetalleCategoriaIndicadorHistorico').html('').select2({data: [{id: '', text: ''}]});
        $.ajax({
            url: window.location.pathname,
            data: jsnParametrosCategoria,
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
                $("#slcDetalleCategoriaIndicadorHistorico").select2({
                    theme: "bootstrap4",
                    placeholder: "Seleccione una categoría",
                    language: 'es',
                    allowClear: true,
                    data: request.lstSelect
                });
                $("#slcDetalleCategoriaIndicadorHistorico").val('').trigger('change');
                $('#colDetalleCategoriaHistorico').attr('hidden', false);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    }

    // Función que ejecuta la consulta del histórico de un indicador detallado
    function fncConsultarIndicadorDetalladoHistorico(jsnParametrosDetalle, strCategoria) {
        $.ajax({
            url: window.location.pathname,
            data: jsnParametrosDetalle,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {
                dctHistoricoIndicadores.dctHistoricoIndicadorDetallado.lstCategorias = [];
                dctHistoricoIndicadores.dctHistoricoIndicadorDetallado.lstSeries = [];
                if(request != false){
                    dctHistoricoIndicadores.dctHistoricoIndicadorDetallado.lstCategorias = request[0];
                    dctHistoricoIndicadores.dctHistoricoIndicadorDetallado.lstSeries = request[1]
                    dctHistoricoIndicadores.fncIndicadorDetalladoHistorico();
                    $('#rowGraficoHistoricoDetallado').attr('hidden', false);
                }
                else if(request == false){
                    fncMensajeErrormns('El indicador en '+ strCategoria +'no se estableció en su planeación actual')
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });    
    }
    
    // Ejecutar consulta para indicador general actual
    $('#slcIndicadorGeneralActual').on('select2:select', function (e) { 
        e.preventDefault();
        var intIndicadorGeneralActual = $('#slcIndicadorGeneralActual').val();
        var strIndicadorGeneralActual = $('#slcIndicadorGeneralActual :selected').text();
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'jsnConsultarIndicadorGeneralActual');
        jsnParametros.append('intIndicadorGeneralActual', intIndicadorGeneralActual);
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
                if(request != false){
                    $('#colObjetivoGeneralActual').attr('hidden', false);
                    $('#iptObjetivoIndicadorGeneralActual').val('$ '+ request.fltObjetivoGeneralActual);
                    $('#colRealGeneralActual').attr('hidden', false);
                    $('#iptRealIndicadorGeneralActual').val('$ '+ request.fltRealGeneralActual);
                    $('#lblCumplimientoGeneral').attr('hidden', false);
                    $('#prgBarCumplimientoGeneral').attr('hidden', false);
                    $('#prgBarIndicadorGeneralActual').css('width', request.strCumplimientoIndicador);
                    $('#txtProgressBar').text(request.strCumplimientoIndicador);
                }
                else if(request == false){
                    fncMensajeErrormns('El indicador de' + strIndicadorGeneralActual + 'no se estableció en su planeación actual')    
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    }).on('select2:unselect', function () {
        $('#colObjetivoGeneralActual').attr('hidden', true);
        $('#iptObjetivoIndicadorGeneralActual').val('');
        $('#colRealGeneralActual').attr('hidden', true);
        $('#iptRealIndicadorGeneralActual').val('');
        $('#lblCumplimientoGeneral').attr('hidden', true);
        $('#prgBarCumplimientoGeneral').attr('hidden', true);
        $('#prgBarIndicadorGeneralActual').css('width', '0%');
        $('#txtProgressBar').text('');
    });
    
    // Ejecutar consulta para obtener la data de la categoría seleccionada para indicador actual detallado
    $('#slcCategoriaIndicadorActual').on('select2:select', function (e) { 
        e.preventDefault();
        var jsnParametros = new FormData();
        var strCategoriaDetalle = $('#slcCategoriaIndicadorActual :selected').text();
        if (strCategoriaDetalle == 'Ciudad'){
            jsnParametros.append('action', 'btnConsultarCiudadesjsn');
            fncConsultarCategoriaslc(jsnParametros);
            return;
        }
        else if(strCategoriaDetalle == 'Zona'){
            jsnParametros.append('action', 'btnConsultarZonasjsn');
            fncConsultarCategoriaslc(jsnParametros);
            return;
        }
        else if(strCategoriaDetalle == 'Categoría clientes'){
            jsnParametros.append('action', 'btnConsultarCategoriaClientejsn');
            fncConsultarCategoriaslc(jsnParametros);
            return;
        }
        else if(strCategoriaDetalle == 'Asesor comercial'){
            jsnParametros.append('action', 'btnConsultarAsesorComercialjsn');
            fncConsultarCategoriaslc(jsnParametros);
            return;
        }
    }).on('select2:unselect', function () {
        $('#colDetalleCategoriaActual').attr('hidden', true);
        $('#slcCategoriaIndicadorDetalleActual').html('').select2({data: [{id: '', text: ''}]});
        $('#colIndicadorDetalleActual').attr('hidden', true);
        $('#slcIndicadorDetalladoActual').val('').trigger('change');
        $('#rowMetaIndicadorDetalleActual').attr('hidden', true);
        $('#iptObjetivoIndicadorDetalleActual').val('');
        $('#iptRealIndicadorDetalleActual').val('');
        $('#lblCumplimientoDetalleActual').attr('hidden', true);
        $('#rowBarCumplimientoIndicadorDetalleActual').attr('hidden', true);
        $('#prgBarCumplimientoDetalleActual').css('width', '0%');
        $('#txtProgressBarDetallado').text('');
    });
    
    $('#slcCategoriaIndicadorDetalleActual').on('select2:select', function (e) {
        e.preventDefault();
        var strCategoriaIndicadorActual = $('#slcCategoriaIndicadorDetalleActual :selected').text();
        if(strCategoriaIndicadorActual =! ''){
            $('#colIndicadorDetalleActual').attr('hidden', false);
            return;
        }
    }).on('select2:unselect', function () {
        $('#colIndicadorDetalleActual').attr('hidden', true);
        $('#slcIndicadorDetalladoActual').val('').trigger('change');
        $('#rowMetaIndicadorDetalleActual').attr('hidden', true);
        $('#iptObjetivoIndicadorDetalleActual').val('');
        $('#iptRealIndicadorDetalleActual').val('');
        $('#lblCumplimientoDetalleActual').attr('hidden', true);
        $('#rowBarCumplimientoIndicadorDetalleActual').attr('hidden', true);
        $('#prgBarCumplimientoDetalleActual').css('width', '0%');
        $('#txtProgressBarDetallado').text('');
    });
    
    // Ejecutar consulta para indicador deatallado actual
    $('#slcIndicadorDetalladoActual').on('select2:select', function (e) {
        e.preventDefault();
        var strIndicadorDetalladoActual = $('#slcIndicadorDetalladoActual :selected').text();
        var strCategoriaDetalle = $('#slcCategoriaIndicadorActual :selected').text();
        var intDetalleCategoriaActual = $('#slcCategoriaIndicadorDetalleActual').val();
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'jsnConsultarIndicadorDetalladoActual');
        jsnParametros.append('strIndicadorDetalladoActual', strIndicadorDetalladoActual);
        jsnParametros.append('intDetalleCategoriaActual', intDetalleCategoriaActual);
        if(strCategoriaDetalle == 'Ciudad'){
            jsnParametros.append('strSet', 'City');
            fncConsultarIndicadorDetalladoActual(jsnParametros, strCategoriaDetalle);
            return;
        }
        else if(strCategoriaDetalle == 'Zona'){
            jsnParametros.append('strSet', 'Zones');
            fncConsultarIndicadorDetalladoActual(jsnParametros, strCategoriaDetalle);
            return;
        }
        else if(strCategoriaDetalle == 'Categoría cliente'){
            jsnParametros.append('strSet', 'Customer_Category');
            fncConsultarIndicadorDetalladoActual(jsnParametros, strCategoriaDetalle);
            return;
        }
        else if(strCategoriaDetalle == 'Asesor comercial'){
            jsnParametros.append('strSet', 'Adviser');
            fncConsultarIndicadorDetalladoActual(jsnParametros, strCategoriaDetalle);
            return;
        }
    }).on('select2:unselect', function () {
        $('#rowMetaIndicadorDetalleActual').attr('hidden', true);
        $('#iptObjetivoIndicadorDetalleActual').val('');
        $('#iptRealIndicadorDetalleActual').val('');
        $('#lblCumplimientoDetalleActual').attr('hidden', true);
        $('#rowBarCumplimientoIndicadorDetalleActual').attr('hidden', true);
        $('#prgBarCumplimientoDetalleActual').css('width', '0%');
        $('#txtProgressBarDetallado').text('');
    });

    // Ejecutar consulta para histórico de indicador general
    $('#slcIndicadorGeneralHistorico').on('select2:select', function (e) { 
        e.preventDefault();
        var intIndicadorGeneral = $('#slcIndicadorGeneralHistorico').val();
        var strIndicadorGeneral = $('#slcIndicadorGeneralHistorico :selected').text();
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'jsnConsultarHistoricoIndicadorGeneral');
        jsnParametros.append('intIndicadorGeneral', intIndicadorGeneral);
        fncConsultarHistoricoIndicadorGeneralgrf(jsnParametros, strIndicadorGeneral);
    }).on('select2:unselect', function () {
        dctHistoricoIndicadores.dctHistoricoIndicadorGeneral.lstCategorias = [];
        dctHistoricoIndicadores.dctHistoricoIndicadorGeneral.lstSeries = [];
        dctHistoricoIndicadores.fncIndicadorGeneralHistorico();
        $('#rowGraficoHistoricoGeneral').attr('hidden', true);
    });

    // Ejecutar consulta para obtener la data de la categoría seleccionada para histórico de indicador detallado
    $('#slcCategoriaIndicadorHistorico').on('select2:select', function (e) { 
        var jsnParametros = new FormData();
        var strCategoriaDetalle = $('#slcCategoriaIndicadorHistorico :selected').text();
        if (strCategoriaDetalle == 'Ciudad'){
            jsnParametros.append('action', 'btnConsultarCiudadesjsn');
            fncConsultarCategoriasHistoricoslc(jsnParametros);
            return;
        }
        else if(strCategoriaDetalle == 'Zona'){
            jsnParametros.append('action', 'btnConsultarZonasjsn');
            fncConsultarCategoriasHistoricoslc(jsnParametros);
            return;
        }
        else if(strCategoriaDetalle == 'Categoría clientes'){
            jsnParametros.append('action', 'btnConsultarCategoriaClientejsn');
            fncConsultarCategoriasHistoricoslc(jsnParametros);
            return;
        }
        else if(strCategoriaDetalle == 'Asesor comercial'){
            jsnParametros.append('action', 'btnConsultarAsesorComercialjsn');
            fncConsultarCategoriasHistoricoslc(jsnParametros);
            return;
        }
    }).on('select2:unselect', function () {
        $('#slcDetalleCategoriaIndicadorHistorico').html('').select2({data: [{id: '', text: ''}]});
        $('#colDetalleCategoriaHistorico').attr('hidden', true);
        $("#slcIndicadorHistoricoDetallado").val('').trigger('change');
        $('#colIndicadorDetalleHistorico').attr('hidden', true);
        $('#rowGraficoHistoricoDetallado').attr('hidden', true);
        dctHistoricoIndicadores.dctHistoricoIndicadorDetallado.lstCategorias = [];
        dctHistoricoIndicadores.dctHistoricoIndicadorDetallado.lstSeries = [];
        dctHistoricoIndicadores.fncIndicadorDetalladoHistorico();
    });

    // 
    $('#slcDetalleCategoriaIndicadorHistorico').on('select2:select', function (e) {
        e.preventDefault();
        var strCategoriaIndicadorHistorico = $('#slcDetalleCategoriaIndicadorHistorico :selected').text();
        if(strCategoriaIndicadorHistorico =! ''){
            $('#colIndicadorDetalleHistorico').attr('hidden', false);
            return;
        }
    }).on('select2:unselect', function () {
        $("#slcIndicadorHistoricoDetallado").val('').trigger('change');
        $('#colIndicadorDetalleHistorico').attr('hidden', true);
        $('#rowGraficoHistoricoDetallado').attr('hidden', true);
        dctHistoricoIndicadores.dctHistoricoIndicadorDetallado.lstCategorias = [];
        dctHistoricoIndicadores.dctHistoricoIndicadorDetallado.lstSeries = [];
        dctHistoricoIndicadores.fncIndicadorDetalladoHistorico();
    });

    // Ejecutar consulta para histórico de indicador detallado
    $('#slcIndicadorHistoricoDetallado').on('select2:select', function (e) { 
        e.preventDefault();
        var intIndicadorDetalladoHistorico = $('#slcIndicadorHistoricoDetallado').val();
        var strCategoriaDetalle = $('#slcCategoriaIndicadorHistorico :selected').text();
        var intDetalleCategoriaActual = $('#slcDetalleCategoriaIndicadorHistorico').val();
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'jsnConsultarIndicadorDetalladoHistorico');
        jsnParametros.append('intIndicadorDetalladoHistorico', intIndicadorDetalladoHistorico);
        jsnParametros.append('intDetalleCategoriaActual', intDetalleCategoriaActual);
        if(strCategoriaDetalle == 'Ciudad'){
            jsnParametros.append('strSet', 'City');
            fncConsultarIndicadorDetalladoHistorico(jsnParametros, strCategoriaDetalle);
            return;
        }
        else if(strCategoriaDetalle == 'Zona'){
            jsnParametros.append('strSet', 'Zones');
            fncConsultarIndicadorDetalladoHistorico(jsnParametros, strCategoriaDetalle);
            return;
        }
        else if(strCategoriaDetalle == 'Categoría cliente'){
            jsnParametros.append('strSet', 'Customer_Category');
            fncConsultarIndicadorDetalladoHistorico(jsnParametros, strCategoriaDetalle);
            return;
        }
        else if(strCategoriaDetalle == 'Asesor comercial'){
            jsnParametros.append('strSet', 'Adviser');
            fncConsultarIndicadorDetalladoHistorico(jsnParametros, strCategoriaDetalle);
            return;
        }
    }).on('select2:unselect', function () {
        $('#rowGraficoHistoricoDetallado').attr('hidden', false);
        dctHistoricoIndicadores.dctHistoricoIndicadorDetallado.lstCategorias = [];
        dctHistoricoIndicadores.dctHistoricoIndicadorDetallado.lstSeries = [];
        dctHistoricoIndicadores.fncIndicadorDetalladoHistorico();
    });

});