$(document).ready(function(){
    var ShowForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-poste').modal('show');
            },
            success: function(data){
                $('#modal-poste .modal-content').html(data.html_form);
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
                    $('#table-poste tbody').html(data.poste);
                    $('#modal-poste').modal('hide');
                } else {
                    $('#modal-poste .modal-content').html(data.html_form)
                }
            }
        })
        return false;
    };

// Create a form
$(".show-form").click(ShowForm);
$('#modal-poste').on("submit", ".create-form", SaveForm);

// Update form
$('#table-poste').on("click", ".show-form-update", ShowForm);
$('#modal-poste').on("submit", ".update-form", SaveForm);

// Delete form
$('#table-poste').on("click", ".show-form-delete", ShowForm);
$('#modal-poste').on("submit", ".delete-form", SaveForm);

});