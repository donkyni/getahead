$(document).ready(function(){
    var ShowForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-pays').modal('show');
            },
            success: function(data){
                $('#modal-pays .modal-content').html(data.html_form);
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
                    $('#table-pays tbody').html(data.code);
                    $('#modal-pays').modal('hide');
                } else {
                    $('#modal-pays .modal-content').html(data.html_form)
                }
            }
        })
        return false;
    };

// Create a form
$(".show-form").click(ShowForm);
$('#modal-pays').on("submit", ".create-form", SaveForm);

// Update form
$('#table-pays').on("click", ".show-form-update", ShowForm);
$('#modal-pays').on("submit", ".update-form", SaveForm);

// Delete form
$('#table-pays').on("click", ".show-form-delete", ShowForm);
$('#modal-pays').on("submit", ".delete-form", SaveForm);

});