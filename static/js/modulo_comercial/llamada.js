$(function(){
    $('#visit_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD"),
    });
    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación', '¿Está seguro de guardar el registro?', parameters, function () {
            location.href = '/comercial/listar_llamadas';
        });
    });
});