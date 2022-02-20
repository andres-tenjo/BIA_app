var app = new Vue({
    el: '#app',
    data: {
        customer: '',
        category_cust: '',
        name: '',
        nit: '',
        cel: '',
        pay_method: '',
        estado_cartera: '',
        order_date: '',
        order_city:'',
        order_address: '',
        deliver_date: '',
        del_schedule: '',
        observation:'',
        subtotal: 0.00,
        iva: 00,
        dcto: 0.00,
        total: 0.00,
        products: [],
        salesHelper: []
    },
    computed:{

    },
    methods: {
        get_ids: function () {
            var ids = [];
            $.each(this.items.products, function (key, value) {
                ids.push(value.id);
            });
            return ids;
        },
        view_state_cartera: function () {
            
        },
        add: function (item) {
            this.items.products.push(item);
            this.list();
        },
        calculate_invoice: function () {
            var subtotal = 0.00;
            var iva = 0.00;
            var dcto = 0.00;
            var total = 0.00;
            cbDesc = $('.cbDesc').val();
            $.each(this.items.products, function (pos, dict) {
                subtotal += dict.subtotal;
                iva += (dict.cant * dict.price_udv) * dict.iva
                dcto += (dict.cant * dict.price_udv) * dict.desc
            });
            this.items.subtotal = subtotal;
            this.items.iva = iva;
            this.items.dcto = dcto;
            total = subtotal + iva - dcto
            this.items.total = total;
    
            $('input[name="subtotal"]').val('$ ' + this.items.subtotal.toFixed(2));
            $('input[name="iva"]').val('$ ' + this.items.iva.toFixed(2));
            $('input[name="dcto"]').val('$ ' + this.items.dcto);
            $('input[name="total"]').val('$ ' + this.items.total.toFixed(2));
        },
        list: function () {
            this.calculate_invoice();
            tblProducts = $('#tblProducts').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
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
                data: this.items.products,
                columns: [
                    { "data": "id"},
                    { "data": "name"},
                    { "data": "udv.name"},
                    { "data": "price_udv"},
                    { "data": "cant"},
                    { "data": "subtotal"},
                    { "data": "iva"},
                    { "data": "desc"},
                    { "data": "id"},
                ],
                columnDefs: [
                    {
                        targets: [-1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                        }
                    },
                    {
                        targets: [-4, -6],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '$ '+parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-2, -3],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return (parseFloat(data).toFixed(2) * 100) + ' %';
                        }
                    },
                    {
                        targets: [-5],
                        class: 'text-center',
                    },
                ],
                rowCallback(row, data, displayNum, displayIndex, dataIndex) {
    
                    $(row).find('input[name="cant"]').TouchSpin({
                        min: 1,
                        max: 1000000000,
                        step: 1
                    });
    
                },
                initComplete: function(settings, json) {
                }
            });
        },
        helperList: function () {
            tblHelper = $('#tblHelp').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
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
                data: this.items.salesHelper,
                columns: [
                    { "data": "id"},
                    { "data": "name"},
                    { "data": "udv.name"},
                    { "data": "price_udv"},
                    { "data": "cant"},
                    { "data": "subtotal"},
                    { "data": "iva"},
                    { "data": "desc"},
                    { "data": "id"},
                ],
                columnDefs: [
                    {
    
                    }
                ],
                initComplete: function(settings, json) {
                }
            });
        },
    }
  })