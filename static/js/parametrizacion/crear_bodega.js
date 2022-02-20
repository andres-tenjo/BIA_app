$(function () {
    const strDepartamento = $("#department");
    const strCiudad = $('#city');

    // Cargar select para opciones preestablecidas
    fncCargarLibreriaSelect2('.select', 'Seleccione una opción');
    
    // Evento que filtra la ciudad de ubicación de la empresa
    // respecto al departamento seleccionado
    strDepartamento.on("change", function() {
        fncFiltrarCiudades(strDepartamento, strCiudad);
    });

});