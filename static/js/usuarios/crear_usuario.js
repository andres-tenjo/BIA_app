$(function () {
    pwd = $('#password').val();
    
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es',
        placeholder: 'Buscar'
    });

    if(pwd != ''){
        $('#editPassword').prop("hidden", false);
        $('#pwdRow').prop("hidden", true);
        $('#pwdText').prop("hidden", true);
    }

    $('#cbPwd').on('click', function () {
        v = $('#cbPwd').val();
        if(v == 1){
            $('#pwdRow').prop("hidden", true);
            $('#pwdText').prop("hidden", true);
            $('#password').val(pwd);
            $('#cbPwd').val(0);
        }
        else if(v == 0){
            $('#pwdRow').prop("hidden", false);
            $('#pwdText').prop("hidden", false);
            $('#password').val('');
            $('#cbPwd').val(1);
        }
    });
});