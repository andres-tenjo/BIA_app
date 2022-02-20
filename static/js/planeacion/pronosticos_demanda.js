       
var tblProd;
function getData() {
    tblProd = $('#data').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        searching: false,
        paging: false,
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        info: false,
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
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action':'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            { "data": "id"},
            { "data": "sale_proj"},
            { "data": "state"},
        ],
        columnDefs: [
            {
                targets: [0],
                searchable: false,
                orderable: false,
                class: 'text-center',
            },
            {
                targets: [1],
                className: "text-center",
                type: 'numeric-comma',
            },
            {
                targets: [2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="view" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-sign-in-alt"></i></a> ';
                    return buttons;
                }
            },
        ],
        order: [[ 1, 'asc']],
        initComplete: function(settings, json) {
        }
    });
}

function getProd(id) {
    tblPronProd = $('#tabla_pron_prod').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
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
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action':'forecast',
                'id': id,
            },
            dataSrc: ""
        },
        columns: [
            { "data": "id"},
            { "data": "product"},
            { "data": "proj_sale"},
            { "data": "sale_proj"},
            { "data": "purchase_cost"},
            { "data": "purchase_proj"},
        ],
        columnDefs: [
            {
                targets: [0],
                searchable: false,
                orderable: false,
                class: 'text-center',
            },
        ],
        order: [[ 1, 'asc']],
        initComplete: function(settings, json) {
        }
    });
}
var tblPronCli;
function getCli(id) {
    tblPronCli = $('#tabla_pron_cli').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
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
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action':'forecast',
                'id': id,
            },
            dataSrc: ""
        },
        columns: [
            { "data": "id"},
            { "data": "customer"},
            { "data": "proj_sale"},
        ],
        columnDefs: [
            {
                targets: [0],
                searchable: false,
                orderable: false,
                class: 'text-center',
            },
        ],
        order: [[ 1, 'asc']],
        initComplete: function(settings, json) {
        }
    });
}
var tblPronZone;
function getZone(id) {
    tblPronZone = $('#tabla_pron_zone').DataTable({
    dom: 'Bfrtip',
    buttons: [
        'copy', 'csv', 'excel', 'pdf', 'print'
    ],
    responsive: true,
    autoWidth: false,
    destroy: true,
    deferRender: true,
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
    ajax: {
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action':'forecast',
            'id': id,
        },
        dataSrc: ""
    },
    columns: [
        { "data": "id"},
        { "data": "zone"},
        { "data": "proj_sale"},
    ],
    columnDefs: [
        {
            targets: [0],
            searchable: false,
            orderable: false,
            class: 'text-center',
        },
    ],
    order: [[ 1, 'asc']],
    initComplete: function(settings, json) {
    }
});
}
var tblPronAdv;
function getAdvisor(id) {
    tblPronAdv = $('#tabla_pron_advisor').DataTable({
    responsive: true,
    autoWidth: false,
    destroy: true,
    deferRender: true,
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
    ajax: {
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action':'forecast',
            'id': id,
        },
        dataSrc: ""
    },
    columns: [
        { "data": "id"},
        { "data": "advisor"},
        { "data": "proj_sale"},
    ],
    columnDefs: [
        {
            targets: [0],
            searchable: false,
            orderable: false,
            class: 'text-center',
        },
    ],
    order: [[ 1, 'asc']],
    initComplete: function(settings, json) {
    }
});
}

function tblName(tblName) {
    tblName.on( 'order.dt search.dt', function () {
        tblName.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
}
$(function () {
    
    modal_title = $('.modal-title');
    
    getData();
    
    tblName(tblProd);

    $('#data tbody').on('click', 'a[rel="view"]', function () {
        modal_title.find('span').html('Ponósticos de venta por producto, cliente, zona y asesor');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        var tr = tblProd.cell($(this).closest('td, li')).index();
        var data = tblProd.row(tr.row).data();
        var id = data.id;
        getProd(id);
        getCli(id);
        getZone(id);
        getAdvisor(id);
        tblName(tblPronProd);
        tblName(tblPronCli);
        tblName(tblPronZone);
        tblName(tblPronAdv);
        $('#ModalForecast1').modal('show');
    });
    $('.btnSelection').on('click', function () {
        $.confirm({
            theme: 'material',
            title: 'Notificación',
            icon: 'fa fa-info',
            content: '¿Desea seleccionar el escenario?',
            columnClass: 'small',
            typeAnimated: true,
            cancelButtonClass: 'btn-primary',
            draggable: true,
            dragWindowBorder: false,
            buttons: {
                info: {
                    text: "Si",
                    btnClass: 'btn-primary',
                    action: function () {
        
                    }
                },
                danger: {
                    text: "No",
                    btnClass: 'btn-red',
                    action: function () {
                        
                    }
                },
            }
        })
    });
});
