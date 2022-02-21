var dctOpcionesCrearCliente = {
    dctVariables: {
        lstCategorias: [],
    },

    fncZonaClienteslc: function () {
        $('select[name="customer_zone"]').select2({
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
                        action: 'slcBuscarZonaClientejsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione o cree una nueva',
        });  
    },

    fncZonaCLienteAsesorslc: function () {
        $('select[name="zone"]').select2({
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
                        action: 'slcBuscarZonaClientejsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione o cree una nueva',
        });  
    },

    fncAsesorComercialslc: function () {
        $('select[name="commercial_advisor"]').select2({
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
                        action: 'slcBuscarAsesorComercialjsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione o cree una nueva',
        });  
    },

    fncCategoriaClienteslc: function () {
        $('select[name="customer_cat"]').select2({
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
                        action: 'slcBuscarCategoriaClientejsn'
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Seleccione o cree una nueva',
        });  
    },

    fncMargenCategoriaClientetbl: function () {
        tblMargenCategoriaCliente = $('#tblMargin').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            dom: 'Bfrtip',
            language: {
                "decimal": "",
                "emptyTable": "No existe información creada",
                "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                "infoEmpty": "Mostrando 0 de 0 Entradas",
                "infoFiltered": "(Filtrado de _MAX_ total entradas)",
                "infoPostFix": "",
                "thousands": ",",
                "lengthMenu": "Mostrar _MENU_ Entradas",
                "loadingRecords": "Cargando...",
                "processing": "Procesando...",
                "search": "Buscar:",
                "zeroRecords": "Sin resultados encontrados",
                "paginate": {
                    "first": "Primero",
                    "last": "Ultimo",
                    "next": "Siguiente",
                    "previous": "Anterior"
                },
            },
            data: this.dctVariables.lstCategorias[0],
            columns: [
                { "data": "product_cat"},
                { "data": "margin_max"},
                { "data": "margin_min"}
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input name="margin_min" type="number" min="0" value="0" step=".01" required="true"></input>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input name="margin_max" type="number" min="0" value="0" step=".01" required="true"></input>';
                    }
                }
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="margin_max"]').TouchSpin({
                    min: 0,
                    max: 100,
                    step: 0.01,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 1,
                    postfix: '%'
                }).val(0.00);
                $(row).find('input[name="margin_min"]').TouchSpin({
                    min: 0,
                    max: 100,
                    step: 0.01,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 1,
                    postfix: '%'
                }).val(0.00);

            },
            initComplete: function(settings, json) {
            }
        });
    },
}

$(function () {

    const strMetodoPago = document.getElementById('pay_method');
    const fltCupoCredito = document.getElementById('credit_value');
    const intDiasCredito = document.getElementById('credit_days');
    const strTipoPersona = document.getElementById('person_type');
    const strTipoIdentificacion = document.getElementById('id_type');
    const strDepartamento = $("#department");
    const strCiudad = $('#city');

    // Función para cargar libreria Select2 para los input tipo select
    fncCargarLibreriaSelect2('.select2', 'Seleccione o cree una nueva');
    fncCargarLibreriaSelect2('.select', 'Seleccione una opción');
    
    // Cargar editar método de pago
    if(strMetodoPago.value == 'CR'){
        $('#creditMethod').prop('hidden', false);
        $('#textMethod').prop('hidden', false);
    }

    // Función para cargar libreria TouchSpin para los input tipo número, decimal y moneda
    fncCargarLibreriaTouchSpinFormatoEntero();
    fncCargarLibreriaTouchSpinFormatoMoneda();

    // Evento que filtra la ciudad de ubicación de la empresa
    // respecto al departamento seleccionado
    strDepartamento.on("change", function() {
        fncFiltrarCiudades(strDepartamento, strCiudad);
    });
    
    // Evento que actualiza el tipo de identificación 
    // respecto al tipo de documento seleccionado
    $('#person_type').on('change', function () {
        fncFiltrarTipoId(strTipoPersona, strTipoIdentificacion)
    })

    // Seleccionar método de pago
    $('#pay_method').on('change', function () {
        pay = $('#pay_method').val();
        if(pay == 'CR'){
            $('#creditMethod').prop('hidden', false);
            $('#textMethod').prop('hidden', false);
        }
        else if(pay == 'CO'){
            $('#creditMethod').prop('hidden', true);
            $('#textMethod').prop('hidden', true);
            $('#credit_limit').val('');
            $('#credit_days').val('');
        }
    });

    // Abrir modal creación categoría cliente
    $('.btnAddCat').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: window.location.pathname,
            headers: {
                'X-CSRFToken': csrftoken
            },
            type: 'POST',
            data: {
                'action':'tblMargenCategoriaProductojsn'
            },
            dataType: 'json',
        }).done(function(data) {
            if(data.hasOwnProperty('error')){
                error = data.error;
                $.confirm({
                    columnClass: 'col-md-12',
                    title: 'Error en categoría',
                    icon: 'fa fa-warning',
                    content: error,
                    theme: 'supervan',
                    buttons: {
                        Aceptar: function () {
                            location.href = '/configuracion/opciones_producto/';
                        },
                        Cancelar: function () {
                                    
                        },
                    }
                });
            }
            else{
                dctOpcionesCrearCliente.dctVariables.lstCategorias.push(data);
                dctOpcionesCrearCliente.fncMargenCategoriaClientetbl();
                $('#myModalCategory').modal('show');
                $('input[name="cat_cust"]').focus();

            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus +': '+errorThrown);
        }).always(function(data) {                
        });        
    });

    // Borrar lo digitado en el formulario categoría
    $('#myModalCategory').on('hidden.bs.modal', function (e) {
        $('#frmCatCust').trigger('reset');
        dctOpcionesCrearCliente.dctVariables.lstCategorias = []
    })

    // Guardar el registro de categoría de cliente
    $('#frmCatCust').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData();
        parameters.append('action', 'frmCrearCategoriaClientejsn');
        parameters.append('customer_cat', $('input[name="cat_cust"]').val());
        parameters.append('margin_cat', JSON.stringify(dctOpcionesCrearCliente.dctVariables.lstCategorias));
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                var newOption = new Option(response.customer_cat, response.id, false, true);
                dctOpcionesCrearCliente.fncCategoriaClienteslc();
                $('#customer_cat').append(newOption).trigger('change');
                $('#myModalCategory').modal('hide');
                dctOpcionesCrearCliente.dctVariables.lstCategorias = []
            });
    });

    // Eventos de la tabla categoría productos margén
    $('#tblMargin tbody')
        //Calcular cantidades de la tabla
        .on('change', 'input[name="margin_min"]', function () {
            var margin_min = parseFloat($(this).val());
            var tr = tblMargenCategoriaCliente.cell($(this).closest('td, li')).index();
            dctOpcionesCrearCliente.dctVariables.lstCategorias[0][tr.row].margin_min = margin_min;
        })
        .on('change', 'input[name="margin_max"]', function () {
            var margin_max = parseFloat($(this).val());
            var tr = tblMargenCategoriaCliente.cell($(this).closest('td, li')).index();
            dctOpcionesCrearCliente.dctVariables.lstCategorias[0][tr.row].margin_max = margin_max;
    });

    // Abrir modal creación zona cliente
    $('.btnAddZone').on('click', function () {
        $('#myModalZone').modal('show');
    });

    // Borrar lo digitado en el formulario zona
    $('#myModalZone').on('hidden.bs.modal', function (e) {
        $('#frmCatZone').trigger('reset');
    })

    // Guardar el registro de zona de cliente
    $('#frmCatZone').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'frmCrearZonaClientejsn');
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                var newOption = new Option(response.customer_zone, response.id, false, true);
                dctOpcionesCrearCliente.fncZonaClienteslc();
                $('#customer_zone').append(newOption).trigger('change');
                $('#myModalZone').modal('hide');
            });
    });
    
    // Abrir modal creación asesor comercial
    $('.btnAddAdv').on('click', function () {
        $('#myModalAdvisor').modal('show');
        dctOpcionesCrearCliente.fncZonaCLienteAsesorslc();
    });

    // Borrar lo digitado en el formulario asesor
    $('#myModalAdvisor').on('hidden.bs.modal', function (e) {
        $('#frmAdvisor').trigger('reset');
    })

    // Guardar el registro de zona de cliente
    $('#frmAdvisor').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'frmCrearAsesorComercialjsn');
        fncGuardarFormularioAjax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar el registro?', parameters, function (response) {
                var newOption = new Option(response.advisor, response.id, false, true);
                dctOpcionesCrearCliente.fncAsesorComercialslc();
                $('#commercial_advisor').append(newOption).trigger('change');
                $('#myModalAdvisor').modal('hide');
            });
    });
    
    // Seleccionar método de pago
    $('#pay_method').on('change', function () {
        pay = $('#pay_method').val();
        if(pay == 'CR'){
            $('#creditMethod').prop('hidden', false);
            $('#textMethod').prop('hidden', false);
            $('#credit_value').val(1);
            $('#credit_days').val(1);
        }
        else if(pay == 'CO'){
            $('#creditMethod').prop('hidden', true);
            $('#textMethod').prop('hidden', true);
            $('#credit_value').val('');
            $('#credit_days').val('');
        }
    });

    $('#frm').on('submit', function (e) {
        e.preventDefault();
        if (strMetodoPago.value === 'CR'){
            if (fltCupoCredito.value === ''){
                fncMensajeErrormns('Debe ingresar el cupo de crédito');
                return;
            }
            else if(intDiasCredito.value === ''){
                fncMensajeErrormns('Debe ingresar los días de crédito');
                return;
            }
            else if(fltCupoCredito.value == 0){
                fncMensajeErrormns('El cupo de crédito debe ser diferente de 0');
                return;
            }
            else if(intDiasCredito.value == 0){
                fncMensajeErrormns('Los días de crédito deben ser diferente de 0');
                return;
            }
            else{
                var parameters = new FormData(this);
                fncGuardarFormularioAjax(window.location.pathname, 'Notificación', '¿Está seguro de guardar el registro?', parameters, function () {
                location.href = '/configuracion/listar_clientes/';
                });       
            }
        }else if (strMetodoPago.value === 'CO'){
            var parameters = new FormData(this);
            fncGuardarFormularioAjax(window.location.pathname, 'Notificación', '¿Está seguro de guardar el registro?', parameters, function () {
            location.href = '/configuracion/listar_clientes/';
        });
        }
    });
});