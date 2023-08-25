$(function(e) {
    'use strict';
    var table = $('#file-export').DataTable({
        responsive: true,
        lengthMenu:
            [10, 25, 50, 100]
    });
    table.buttons().container()
        .appendTo('#file-export_wrapper .col-md-6:eq(0)');


    // DATATABLE 1
    $('#datatable1').DataTable({
        responsive: true,
        language: {
            searchPlaceholder: 'Search...',
            sSearch: '',
            lengthMenu: '_MENU_ items/page',
        }
    });

    // DATATABLE 2
    $('#datatable2').DataTable({
        bLengthChange: false,
        searching: false,
        responsive: true
    });
    
    // SELECT2
    $('.dataTables_length select').select2({
        minimumResultsForSearch: Infinity
    });
});