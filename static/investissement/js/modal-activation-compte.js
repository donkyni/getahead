$(document).ready(function(){
    var ShowForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-activation-compte').modal('show');
            },
            success: function(data){
                $('#modal-activation-compte .modal-content').html(data.html_form);
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
                    $('#liste_compte_a_activer tbody').html(data.activation);
                    $('#modal-activation-compte').modal('hide');
                } else {
                    $('#modal-activation-compte .modal-content').html(data.html_form)
                }
            }
        })
        return false;
    };

// Update form
$('#liste_compte_a_activer').on("click", ".show-form-update", ShowForm);
$('#modal-activation-compte').on("submit", ".update-form", SaveForm);

});