$(function () {

    const flt_valor_minimo_compra = document.getElementById('min_purchase_value');
    const str_metodo_pago = document.getElementById('pay_method');
    const flt_cupo_credito = document.getElementById('credit_limit');
    const int_dias_credito = document.getElementById('credit_days');
    const strTipoPersona = document.getElementById('person_type');
    const strTipoIdentificacion = document.getElementById('id_type');
    const strDepartamento = $("#department");
    const strCiudad = $('#city');

    // Función para cargar libreria Select2 para los input tipo select
    fncCargarLibreriaSelect2('.select2', 'Seleccione o cree una nueva');
    
    // Función para cargar libreria TouchSpin para los input tipo número, decimal y moneda
    fncCargarLibreriaTouchSpinFormatoEntero();
    fncCargarLibreriaTouchSpinFormatoDecimal();
    fncCargarLibreriaTouchSpinFormatoMoneda();
    
    if(flt_valor_minimo_compra.value === ''){
        flt_valor_minimo_compra.value = 0;
    }

    // Cargar editar método de pago
    if(str_metodo_pago.value == 'CR'){
        $('#creditMethod').prop('hidden', false);
        $('#textMethod').prop('hidden', false);
    }

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
            $('#credit_limit').val(1);
            $('#credit_days').val(1);
        }
        else if(pay == 'CO'){
            $('#creditMethod').prop('hidden', true);
            $('#textMethod').prop('hidden', true);
            $('#credit_limit').val('');
            $('#credit_days').val('');
        }
    });

    $('#frm').on('submit', function (e) {
        e.preventDefault();
        if (str_metodo_pago.value === 'CR'){
            if (flt_cupo_credito.value === ''){
                fncMensajeErrormns('Debe ingresar el cupo de crédito');
                return;
            }
            else if(int_dias_credito.value === ''){
                fncMensajeErrormns('Debe ingresar los días de crédito');
                return;
            }
            else if(flt_cupo_credito.value == 0){
                fncMensajeErrormns('El cupo de crédito debe ser diferente de 0');
                return;
            }
            else if(int_dias_credito.value == 0){
                fncMensajeErrormns('Los días de crédito deben ser diferente de 0');
                return;
            }
            else{
                var parameters = new FormData(this);
                fncGuardarFormularioAjax(window.location.pathname, 'Notificación', '¿Está seguro de guardar el registro?', parameters, function () {
                location.href = '/configuracion/listar_proveedores/';
            });       
            }
        }else if (str_metodo_pago.value === 'CO'){
            var parameters = new FormData(this);
            fncGuardarFormularioAjax(window.location.pathname, 'Notificación', '¿Está seguro de guardar el registro?', parameters, function () {
            location.href = '/configuracion/listar_proveedores/';
        });
        }
    });
});