function listadoLlamadas(){
    $.ajax({
        url: "/comercial/listar_llamadas/",
        type:"get",
        dataType: "json",
        success: function(response){
            $('#tabla_llamadas tbody').html("");
            for(let i = 0; i < response.length;i++){
                let fila = '<tr>';
                fila += '<td>' + (i+1) + '</td>';
                fila += '<td>' + response[i]["fields"]['cod_cliente'] + '</td>';
                fila += '<td>' + response[i]["fields"]['fecha_llamada'] + '</td>';
                fila += '<td>' + response[i]["fields"]['hora_inicio'] + '</td>';
                fila += '<td>' + response[i]["fields"]['estado_llamada'] + '</td>';
                fila += '<td><button> Ver </button><button> Gestionar </button></td>';
                fila += '</tr>';
                $('#tabla_llamadas tbody').append(fila);
            }
            $('#tabla_llamadas').DataTable({
                responsive: true,
                autoWidth: false,
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
            });

            },
        error: function(error){
            console.log(error);
        }
    });
}
$(document).ready(function (){
    listadoLlamadas();
});