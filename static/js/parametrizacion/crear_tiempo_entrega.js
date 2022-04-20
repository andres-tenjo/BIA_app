$(function () {
    
    // Función para cargar libreria Select2 para los input tipo select
    fncCargarLibreriaSelect2('.select2', 'Seleccione una opción');
    
    function fncCalcularTotalTiempoflt() {

        fltTiempoTotal = 0.0;
        let iptEstimadoAlistamiento = document.getElementById("enlistment_time");
        let iptEstimadoRecorrido = document.getElementById("travel_time");
        let iptEstimadoDescarga = document.getElementById("download_time");
        let fltEstimadoAlistamiento = parseFloat(iptEstimadoAlistamiento.value)
        let fltEstimadoRecorrido = parseFloat(iptEstimadoRecorrido.value)
        let fltEstimadoDescarga = parseFloat(iptEstimadoDescarga.value)
        
        if(!isNaN(fltEstimadoAlistamiento)){
            fltTiempoTotal += fltEstimadoAlistamiento;
        }
        if(!isNaN(fltEstimadoRecorrido)){
            fltTiempoTotal += fltEstimadoRecorrido;
        }
        if(!isNaN(fltEstimadoDescarga)){
            fltTiempoTotal += fltEstimadoDescarga;
        }
        $('#total_time').val(parseFloat(fltTiempoTotal).toFixed(1));
    }

    function fncBuscarCiudadesslc() {
        const strCiudad = $("#city").val();
        var jsnParametros = new FormData();
        jsnParametros.append('action', 'slcBuscarCiudadesjsn');
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
                    $.confirm({
                        columnClass: 'col-md-12',
                        title: 'Error',
                        icon: 'fas fa-warning',
                        content: request.strError,
                        theme: 'supervan',
                        buttons: {
                            Aceptar: function () {
                                location.href = '/configuracion/crear_cliente/';
                            }
                        }
                    });
                }
                $("#city").html('').select2({
                    theme: "bootstrap4",
                    placeholder: "Seleccione una ciudad",
                    language: 'es',
                    allowClear: true,
                    data: request.lstCiudades
                });
                if(strCiudad === ''){
                    $('#city').val('').trigger('change.select2');
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fncMensajeErrormns(errorThrown + ' ' + textStatus);
            }
        });
    }

    fncBuscarCiudadesslc();

    $('#enlistment_time').on('change', function () {
        fncCalcularTotalTiempoflt();
    });

    $('#travel_time').on('change', function () {
        fncCalcularTotalTiempoflt();
    });

    $('#download_time').on('change', function () {
        fncCalcularTotalTiempoflt();
    });

});