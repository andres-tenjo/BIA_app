// Función que filtra el tipo de identificación de un cliente o proveedor
// de acuerdo al tipo de documento seleccionado
// tipoPersonaId = Id del widget tipo de persona que selecciona el usuario
// tipoIdentificacionId = Id del widget tipo de identificación que selecciona el usuario
function fncFiltrarTipoId(tipoPersonaId, tipoIdentificacionId) {
    tipoIdentificacionId.innerHTML = '';
    if(tipoPersonaId.value == 'NT'){
        tipoIdentificacionId.append(new Option("Cédula", "CC"));
        tipoIdentificacionId.append(new Option("Rut", "RU"));
    }else if(tipoPersonaId.value == 'JU'){
        tipoIdentificacionId.append(new Option("Nit", "NI"));
        tipoIdentificacionId.append(new Option("Rut", "RU"));
    }
}

// Función que filtra el tipo la ciudad de acuerdo al departamento seleccionado
// departmentId = Id del widget departamento que selecciona el usuario
// cityId = Id del widget ciudad que seleeciona el usuario
function fncFiltrarCiudades(strDepartamento, strCiudad) {
    var intDepartamentoId = strDepartamento.val();
    var strOptions = '<option value="">--------------------</option>';
    if (intDepartamentoId === '') {
        strCiudad.html(strOptions);
        return false;
    }
    $.ajax({
        url: window.location.pathname,
        data: {
            'action': 'slcFiltrarCiudadesjsn',
            'intId': intDepartamentoId
        },
        type: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (request) {
            if (!request.hasOwnProperty('error')) {
                strCiudad.html('').select2({
                    theme: "bootstrap4",
                    language: 'es',
                    data: request
                });
                return false;
            }
            fncMensajeErrormns(request.error);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            fncMensajeErrormns(errorThrown + ' ' + textStatus);
        }
    });
}

