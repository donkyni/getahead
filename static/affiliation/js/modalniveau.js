$(document).ready(function(){
    var ShowForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-niveau').modal('show');
            },
            success: function(data){
                $('#modal-niveau .modal-content').html(data.html_form);
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
                    $('#table-niveau tbody').html(data.niveau);
                    $('#modal-niveau').modal('hide');
                } else {
                    $('#modal-niveau .modal-content').html(data.html_form)
                }
            }
        })
        return false;
    };

// Create a form
$(".show-form").click(ShowForm);
$('#modal-niveau').on("submit", ".create-form", SaveForm);

// Update form
$('#table-niveau').on("click", ".show-form-update", ShowForm);
$('#modal-niveau').on("submit", ".update-form", SaveForm);

// Delete form
$('#table-niveau').on("click", ".show-form-delete", ShowForm);
$('#modal-niveau').on("submit", ".delete-form", SaveForm);

});