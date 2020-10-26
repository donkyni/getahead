$(document).ready(function(){
    var ShowForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-parent').modal('show');
            },
            success: function(data){
                $('#modal-parent .modal-content').html(data.html_form);
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
                    $('#table-parent tbody').html(data.parent);
                    $('#modal-parent').modal('hide');
                } else {
                    $('#modal-parent .modal-content').html(data.html_form)
                }
            }
        })
        return false;
    };

// Create a form
$(".show-form").click(ShowForm);
$('#modal-parent').on("submit", ".create-form", SaveForm);

// Update form
$('#table-parent').on("click", ".show-form-update", ShowForm);
$('#modal-parent').on("submit", ".update-form", SaveForm);

// Delete form
$('#table-parent').on("click", ".show-form-delete", ShowForm);
$('#modal-parent').on("submit", ".delete-form", SaveForm);

});