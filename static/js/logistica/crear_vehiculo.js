$(function () {
    
    // Cargar select2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // Guardar el registro de producto
    $('#formVehicle').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', $('input[name="action"]').val());
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación', '¿Está seguro de guardar el registro?', parameters, function () {
        location.href = '/logistica/listar_vehiculos';
        });
    });
});