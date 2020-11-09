$(document).ready(function(){
    var ShowForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-payement').modal('show');
            },
            success: function(data){
                $('#modal-payement .modal-content').html(data.html_form);
            }
        });
    };
    var SaveForm = function() {
        var form = $(this);
        $.ajax({
            url: form.attr('data-url'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data) {
                if(data.form_is_valid) {
                    $('#table-payement tbody').html(data.payement);
                    $('#modal-payement').modal('hide');
                } else {
                    $('#modal-payement .modal-content').html(data.html_form);
                }
            }
        })
        return false;
    };

// Update form
$('#table-payement').on("click", ".show-form-update", ShowForm);
$('#modal-payement').on("submit", ".update-form", SaveForm);

});