const spinnerBox = $('#spinnerBox');

$('#form').on('submit', function (e) {
    e.preventDefault();
    spinnerBox.prop('hidden', false);
    var parameters = new FormData(this);
    parameters.append('action', 'frmCargarArchivojsn');
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: parameters,
        headers: {
            'X-CSRFToken': csrftoken
        },
        dataType: 'json',
        processData: false,
        contentType: false,
    }).done(function(data) {
        if (data.hasOwnProperty('success')){
            spinnerBox.prop('hidden', true);
            $.confirm({
                columnClass: 'col-md-12',
                title: 'Felicidades',
                icon: 'fas fa-clipboard-check',
                content: data.success,
                theme: 'supervan',
                buttons: {
                    Aceptar: function () {
                        location.href = '/configuracion/listar_proveedores/';
                    }
                }
            });
        }
        else if (data.hasOwnProperty('strErrorArchivo')){
            var strErrorArchivo = data.strErrorArchivo;
            var jsnProveedores = data.jsnProveedores;
            var lstValidarImportacion = data.lstValidarImportacion;
            var parameters = new FormData();
            parameters.append('action', 'btnArchivoErroresjsn');
            parameters.append('jsnProveedores', jsnProveedores);
            parameters.append('lstValidarImportacion', JSON.stringify(lstValidarImportacion));
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: parameters,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                processData: false,
                contentType: false,
                xhrFields: {
                    responseType: 'blob'
                },
            }).done(function(data) {
                spinnerBox.prop('hidden', true);
                $.confirm({
                    columnClass: 'col-md-12',
                    title: 'Error en archivo',
                    icon: 'fa fa-warning',
                    content: strErrorArchivo,
                    theme: 'supervan',
                    buttons: {
                        Continuar: function () {
                            var d = new Date();
                            var date_now = d.getFullYear() + "_" + d.getMonth() + "_" + d.getDay();
                            var a = document.createElement("a");
                            document.body.appendChild(a);
                            a.style = "display: none";
                            const blob = new Blob([data], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
                            const url = URL.createObjectURL(blob);
                            a.href = url;
                            a.download = "errores_catalogo_" + date_now + ".xlsx";
                            a.click();
                            window.URL.revokeObjectURL(url);
                            location.reload();
                        },
                        Cancelar: function () {
                                    
                        },
                    }
                }); 
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus +': '+errorThrown);
            }).always(function(data) {                
            });
        }
        else if (data.hasOwnProperty('error')){
            spinnerBox.prop('hidden', true);
            fncMensajeErrormns(data.error);
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus +': '+errorThrown);
    }).always(function(data) {                
    });    
});
