$(document).ready(function(){
    var ShowForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-acheter-espace').modal('show');
            },
            success: function(data){
                $('#modal-acheter-espace .modal-content').html(data.html_form);
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
                    $('#table-liste-acheteur tbody').html(data.utilisateur);
                    $('#modal-acheter-espace').modal('hide');
                } else {
                    $('#modal-acheter-espace .modal-content').html(data.html_form)
                }
            }
        })
        return false;
    };

// Update form
$('#table-liste-acheteur').on("click", ".show-form-update", ShowForm);
$('#modal-acheter-espace').on("submit", ".update-form", SaveForm);

});