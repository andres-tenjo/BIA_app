// Evento eliminar grupo en tabla
$(".delGroup").on('click', function (e) {
    e.preventDefault();
    var id = $(this).attr('id');
    var parameters = new FormData();
    parameters.append('action', 'btnEliminarGrupojsn');
    parameters.append('id', id);
    fncGuardarFormularioAjax(window.location.pathname, 'Notificación','¿Estas seguro de eliminar el registro?', parameters, function () {
        location.href = '/usuarios/listar_grupos';
    });
});