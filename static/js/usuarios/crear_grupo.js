function groups_edit() {
    t = $('#all').is(':checked');
    c = $('#commercial').is(':checked');
    p = $('#purchase').is(':checked');
    l = $('#logistics').is(':checked');
    a = $('#admin').is(':checked');
    if (t == true){
        $('#com_permission').prop("disabled", true);
        $('#pur_permission').prop("disabled", true);
        $('#log_permission').prop("disabled", true);
        $('#adm_permission').prop("disabled", true);
        $('#commercial').prop("disabled", true);
        $('#purchase').prop("disabled", true);
        $('#logistics').prop("disabled", true);
        $('#admin').prop("disabled", true);
        $('#commercial').val(0);
        $('#purchase').val(0);
        $('#logistics').val(0);
        $('#admin').val(0);
        $('#all').val(1);
    }
    if (c == true){
        $('#com_permission').val('').trigger('change');
        $('#com_permission').prop("disabled", true);
        $('#commercial').val(1);
    }
    if (p == true){
        $('#pur_permission').val('').trigger('change');
        $('#pur_permission').prop("disabled", true);
        $('#purchase').val(1);
    }
    if (l == true){
        $('#log_permission').val('').trigger('change');
        $('#log_permission').prop("disabled", true);
        $('#logistics').val(1);
    }
    if (a == true){
        $('#adm_permission').val('').trigger('change');
        $('#adm_permission').prop("disabled", true);
        $('#admin').val(1);
    }
}

$(function () {

    groups_edit()

    // Cargar permisos para el input del modulo comercial
    $('#collapseOne').on('shown.bs.collapse', function () {
        $('#com_permission').select2({
            theme: "bootstrap4",
            language: 'es',
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                url: window.location.pathname,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: function (params) {
                    var queryParameters = {
                        action: 'slcBuscarPermisosComercialjsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione uno o más permisos',
        });    
    });

    // Cargar permisos para el input del modulo compras
    $('#collapseTwo').on('shown.bs.collapse', function () {
        $('#pur_permission').select2({
            theme: "bootstrap4",
            language: 'es',
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                url: window.location.pathname,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: function (params) {
                    var queryParameters = {
                        action: 'slcBuscarPermisosComprasjsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione uno o más permisos',
        });
    });

    // Cargar permisos para el input del modulo almacen
    $('#collapseThree').on('shown.bs.collapse', function () {
        $('#log_permission').select2({
            theme: "bootstrap4",
            language: 'es',
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                url: window.location.pathname,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: function (params) {
                    var queryParameters = {
                        action: 'slcBuscarPermisosLogisticajsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione uno o más permisos',
        });
    });

    // Cargar permisos para el input del modulo planeación
    $('#collapseFour').on('shown.bs.collapse', function () {
        $('#adm_permission').select2({
            theme: "bootstrap4",
            language: 'es',
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                url: window.location.pathname,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: function (params) {
                    var queryParameters = {
                        action: 'slcBuscarPermisosAdministradorjsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione uno o más permisos',
        });
    }); 

    // Función para seleccionar los permisos del modulo comercial
    $('#commercial').on('click', function () {
        v = $('#commercial').val();
        if(v == 1){
            $('#com_permission').prop("disabled", false);
            $('#commercial').val(0);
        }
        else if(v == 0){
            $('#com_permission').prop("disabled", true);
            $('#com_permission').val('').trigger('change');
            $('#commercial').val(1);
        }
    });
    
    // Función para seleccionar los permisos del modulo compras
    $('#purchase').on('click', function () {
        v = $('#purchase').val();
        if(v == 1){
            $('#pur_permission').prop("disabled", false);
            $('#purchase').val(0);
        }
        else if(v == 0){
            $('#pur_permission').prop("disabled", true);
            $('#pur_permission').val('').trigger('change');
            $('#purchase').val(1);
        }
    });
    
    // Función para seleccionar los permisos del modulo almacen
    $('#logistics').on('click', function () {
        v = $('#logistics').val();
        if(v == 1){
            $('#log_permission').prop("disabled", false);
            $('#logistics').val(0);
        }
        else if(v == 0){
            $('#log_permission').prop("disabled", true);
            $('#log_permission').val('').trigger('change');
            $('#logistics').val(1);
        }
    });
    
    // Función para seleccionar los permisos del modulo planeación
    $('#admin').on('click', function () {
        v = $('#admin').val();
        if(v == 1){
            $('#adm_permission').prop("disabled", false);
            $('#admin').val(0);
        }
        else if(v == 0){
            $('#adm_permission').prop("disabled", true);
            $('#adm_permission').val('').trigger('change');
            $('#admin').val(1);
        }
    });

    // Función para seleccionar todos los permisos
    $('#all').on('click', function () {
        v = $('#all').val();
        if(v == 1){
            $('#com_permission').prop("disabled", false);
            $('#pur_permission').prop("disabled", false);
            $('#log_permission').prop("disabled", false);
            $('#adm_permission').prop("disabled", false);
            $('#commercial').prop("disabled", false);
            $('#purchase').prop("disabled", false);
            $('#logistics').prop("disabled", false);
            $('#admin').prop("disabled", false);
            $('#commercial').val(0);
            $('#purchase').val(0);
            $('#logistics').val(0);
            $('#admin').val(0);
            $('#all').val(0);
        }
        else if(v == 0){
            $('#com_permission').val('').trigger('change');
            $('#com_permission').prop("disabled", true);
            $('#pur_permission').val('').trigger('change');
            $('#pur_permission').prop("disabled", true);
            $('#log_permission').val('').trigger('change');
            $('#log_permission').prop("disabled", true);
            $('#adm_permission').val('').trigger('change');
            $('#adm_permission').prop("disabled", true);
            $('#commercial').prop('checked', false);
            $('#commercial').prop("disabled", true);
            $('#purchase').prop('checked', false);
            $('#purchase').prop("disabled", true);
            $('#logistics').prop('checked', false);
            $('#logistics').prop("disabled", true);
            $('#admin').prop('checked', false);
            $('#admin').prop("disabled", true);
            $('#commercial').val(0);
            $('#purchase').val(0);
            $('#logistics').val(0);
            $('#admin').val(0);
            $('#all').val(1);
        }
    });

});