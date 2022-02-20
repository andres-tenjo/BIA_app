$(function () {

    // Obtener data para meta
    $('#planning_button').on('click', function(e){
        e.preventDefault();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'get_data'
            },
            dataType: 'json',
        }).done(function (data) {
            if (data.hasOwnProperty('return')) {
                location.href = '/configuracion/planeacion_comercial';
            }
            else{
                msg = data.msg;
                $.confirm({
                    columnClass: 'col-md-12',
                    title: 'Alerta!',
                    icon: 'fa fa-warning',
                    content: msg,
                    theme: 'supervan',
                    buttons: {
                        Aceptar: function () {
                            location.href = '/configuracion/importar_pedidos';
                        },
                        Cancelar: function () {
                            title = 'Alerta'
                            content = 'El asistente de prónostico no se ejecutara'
                            alert_action_msg(content, function () {
                                location.href = '/configuracion/planeacion_comercial';  
                            });
                        },
                    }
                }); 
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
        });
    });

});
