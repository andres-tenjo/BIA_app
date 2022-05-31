$(function () {
    const strTipoPersona = document.getElementById('person_type');
    const strTipoIdentificacion = document.getElementById('id_type');
    const strDepartamento = $("#department");
    const strCiudad = $('#city');

    // Función para cargar libreria Select2 para los input tipo select
    fncCargarLibreriaSelect2('');

    // Evento que actualiza el tipo de identificación 
    // respecto al tipo de documento seleccionado
    strTipoPersona.addEventListener("change", function() {
        fncFiltrarTipoId(strTipoPersona, strTipoIdentificacion) 
    });
    
    // Evento que filtra la ciudad de ubicación de la empresa
    // respecto al departamento seleccionado
    strDepartamento.on("change", function() {
        fncFiltrarCiudades(strDepartamento, strCiudad);
    });

});