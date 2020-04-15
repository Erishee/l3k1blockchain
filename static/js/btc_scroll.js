/* Custom filtering function which will search data in column Solde Final between two values */
$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var min = parseInt( $('#min').val(), 10 );
        var max = parseInt( $('#max').val(), 10 );
        var solde_final = parseFloat( data[4] ) || 0; // use data for the solde final column

        if ( ( isNaN( min ) && isNaN( max ) ) ||
             ( isNaN( min ) && solde_final <= max ) ||
             ( min <= solde_final   && isNaN( max ) ) ||
             ( min <= solde_final   && solde_final <= max ) )
        {
            return true;
        }
        return false;
    }
);

$(document).ready(function() {
    var table = $('#btc_table').DataTable( {
        "scrollX": true,
        "info":false,
        "ordering":false,
    } );

    // Event listener to the two range filtering inputs to redraw on input
    $('#min, #max').keyup( function() {
        table.draw();
    } );
} );