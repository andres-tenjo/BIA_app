$(function () {
    
    // Cargar select2
    $('.select').select2({
        theme: "bootstrap4",
        language: 'es',
        placeholder: 'Seleccione una opción'
    });

    // Abrir modal creación dirección
    $('.btnAddAddress').on('click', function () {
        $('#myModalAddress').modal('show');
        $('select[name="addressType"]').focus();
    });

    $('#frmAddress').on('submit', function (e) {
        e.preventDefault();
        addresType = $('select[name="addressType"]').val();
        streetNumber = $('input[name="streetNumber"]').val();
        addressLet = $('select[name="addressLet"]').val();
        addressBis = $('select[name="addressBis"]').val();
        number = $('input[name="number"]').val();
        numberLet = $('select[name="numberLet"]').val();
        numberBis = $('select[name="numberBis"]').val();
        nomStreet = $('input[name="nomStreet"]').val();
        addressSur = $('select[name="addressSur"]').val();
        address = String(addresType) + ' ' + String(streetNumber) + ' ' + String(addressLet) + ' ' + String(addressBis) + ' ' + String(number) + ' ' + String(numberLet) + ' ' + String(numberBis) + ' ' + String(nomStreet) + ' ' + String(addressSur)
        $('input[name="address"]').val(address);
        $('#myModalAddress').modal('hide');
    });
});