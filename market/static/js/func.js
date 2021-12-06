$(document).ready(function(){
    $('#item-tab').on('change', 'input', function () {
        var cummul = 0;
        row = $(this).closest('tr');
        total = $('#amount',row).val()*$('#price',row).text();
        $('#calc', row).text(total);
        $('#item-tab > tbody  > tr').each(function(){
            cummul += parseInt($('#calc',$(this)).text());
        });
        $('#cummulative').text(cummul);
    });
});