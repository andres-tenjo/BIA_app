///////////////////////////////////////////////////////////////////////////////////////////
///////////////////// FUNCIONES JS PARA EVENTOS GENERALES DE BIA //////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////


// Función para cumplir mecanismo de protección CSRF token de django para peticiones Ajax
function fncObtenerCsrfAjax(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = fncObtenerCsrfAjax('csrftoken');

// Función para cargar libreria select2
// strClase: Clase html del widget que recibe la librería
// strPlaceholder: Cadena de texto para el placeholder del widget
function fncCargarLibreriaSelect2(strClase, strPlaceholder) {
    $(strClase).select2({
        theme: "bootstrap4",
        language: 'es',
        placeholder: strPlaceholder,
    });    
}

// Función para cargar libreria datetimepicker
function fncCargarLibreriaDateTimePicker() {
    $('.timePicker').datetimepicker({
        format: 'LT'
    });
}

// Función para cargar libreria TouchSpin tipo entero
function fncCargarLibreriaTouchSpinFormatoEntero() {
    $(".touchNumber").TouchSpin({
        min: 0,
        max: 10000000,
        step: 1,
    });
}

// Función para cargar libreria TouchSpin tipo decimal 
function fncCargarLibreriaTouchSpinFormatoDecimal() {
    $(".touchPerc").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    });
}

// Función para cargar libreria TouchSpin tipo moneda
function fncCargarLibreriaTouchSpinFormatoMoneda() {
    $(".touchPrice").TouchSpin({
        min: 0,
        max: 100000000000000,
        decimals: 2,
        step: 0.01,
        prefix: '$',
    });
}

// Función que muestra un mensaje de error en ventana
// strMensaje: Cadena de texto del mesnaje que se desea visualizar
function fncMensajeErrormns(strMensaje) {
    var html = '';
    if (typeof (strMensaje) === 'object') {
        var html = '<ul style="text-align: left;">';
        $.each(strMensaje, function (key, value) {
            html+='<li>'+key+': '+value+'</li>';
        });
        html+='</ul>';
    }
    else{
        html = '<p>'+strMensaje+'</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}

// Función que muestra un mensaje de información en ventana
// strMensaje: Cadena de texto del mesnaje que se desea visualizar
function fncMensajeInformacionmns(strMensaje) {
    var html = '';
    if (typeof (strMensaje) === 'object') {
        var html = '<ul style="text-align: left;">';
        $.each(strMensaje, function (key, value) {
            html+='<li>'+key+': '+value+'</li>';
        });
        html+='</ul>';
    }
    else{
        html = '<p>'+strMensaje+'</p>';
    }
    Swal.fire({
        html: html,
        icon: 'info',
    });
}

// Función que ejecuta el envío de un formulario a través de petición Ajax por medio de un mensaje de confirmación
// url: Url de la vista que ejecutara la acción
// strTituloMensaje: Titulo del mensaje para la confirmación del envío del formulario
// strContenidoMensaje: Contenido del mensaje para la confirmación del envío del formulario
// jsnParametros: Diccionario jsn con los parametros que serán enviado al servidor para ejecutar la acción
// fncRetorno: Función que se ejecutara una vez se haya confirmado la acción
function fncGuardarFormularioAjax(url, strTituloMensaje, strContenidoMensaje, jsnParametros, fncRetorno) {
    $.confirm({
        theme: 'material',
        title: strTituloMensaje,
        icon: 'fa fa-info',
        content: strContenidoMensaje,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Aceptar",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url,
                        data: jsnParametros,
                        type: 'POST',
                        dataType: 'json',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        processData: false,
                        contentType: false,
                        success: function (request) {
                            if (!request.hasOwnProperty('error')) {
                                fncRetorno(request);
                                return false;
                            }
                            fncMensajeErrormns(request.error);
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            fncMensajeErrormns(errorThrown + ' ' + textStatus);
                        }
                    });
                }
            },
            danger: {
                text: "Cancelar",
                btnClass: 'btn-red',
                action: function () {
                    
                }
            },
        }
    })
}

// Función para eliminar un item que tiene relación con otras tablas
// jsnParametros: Diccionario jsn con los parametros que serán enviado al servidor para ejecutar la acción
// fncRetorno: Función que se ejecutara una vez se haya confirmado la acción
function delete_action_foreign_key(url, jsnParametros, fncRetorno) {
    $.confirm({
        columnClass: 'col-md-12',
        title: 'Alerta',
        icon: 'fa fa-warning',
        content: '¿Está seguro de cambiar el estado del registro?',
        theme: 'supervan',
        buttons: {
            Continuar: function () {
                $.ajax({
                    url: url,
                    data: jsnParametros,
                    type: 'POST',
                    dataType: 'json',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    processData: false,
                    contentType: false,
                    success: function (request) {
                        if (!request.hasOwnProperty('error')) {
                            fncRetorno(request);
                            return false;
                        }
                        fncMensajeErrormns(request.error);
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        fncMensajeErrormns(errorThrown + ' ' + textStatus);
                    }
                });
            },
            Cancelar: function () {
            },
        }
    });
}

// Eliminar una fila de una tabla
function delete_action(url, parameters, callback) {
    $.confirm({
        columnClass: 'col-md-12',
        title: 'Alerta',
        icon: 'fa fa-warning',
        content: '¿Está seguro de cambiar el estado del registro?',
        theme: 'supervan',
        buttons: {
            Continuar: function () {
                $.ajax({
                    url: url,
                    data: parameters,
                    type: 'POST',
                    dataType: 'json',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    processData: false,
                    contentType: false,
                    success: function (request) {
                        if (!request.hasOwnProperty('error')) {
                            callback(request);
                            return false;
                        }
                        fncMensajeErrormns(request.error);
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        fncMensajeErrormns(errorThrown + ' ' + textStatus);
                    }
                });
            },
            Cancelar: function () {
            },
        }
    });
}

// Mensaje de información para formularios
function message_form(title) {
    Swal.fire({
        position: 'top-end',
        icon: 'warning',
        title: title,
        showConfirmButton: false,
        timer: 1500
  })
}

// Mensaje de alerta
function alert_action(title, content, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    
                }
            },
        }
    })
}

// Mensaje de alerta 2
function alert_action_msg(content, callback) {
    $.confirm({
        columnClass: 'col-md-12',
        title: 'Alerta!',
        icon: 'fa fa-warning',
        content: content,
        theme: 'supervan',
        buttons: {
            Continuar: function () {
                callback();
            },
            Cancelar: function () {
            },
        }
    });
}

// Buscador de producto
function formatRepoProd(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-12 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.product_desc + '<br>' +
        '<b>Código producto:</b> ' + repo.id + '<br>' +
        '<b>Presentación:</b> ' + repo.presentation + '<br>' +
        '<b>Precio:</b> <span class="badge badge-warning">$'+repo.cost_pu+'</span>'+
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

// Cargar repo de proveedores
function formatRepoSupplier(repo) {
    if (repo.loading) {
        return repo.text;
    }
    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-12 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.supplier_name + '<br>' +
        '<b>Id:</b> ' + repo.identification + '<br>' +
        '<b>Contacto:</b> ' + repo.contact_name + '<br>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

// Cargar repo de clientes
function formatRepoCustomer(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-12 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Proveedor:</b> ' + repo.business_name + '<br>' +
        '<b>Identificación: </b>' + repo.identification + '<br>' +
        '<b>Celular: </b> OC000' + repo.cel_number + '<br>' +
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