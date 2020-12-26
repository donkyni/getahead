$(document).ready(function(){
    var ShowForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-palier').modal('show');
            },
            success: function(data){
                $('#modal-palier .modal-content').html(data.html_form);
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
                    $('#table-palier tbody').html(data.palier);
                    $('#modal-palier').modal('hide');
                } else {
                    $('#modal-palier .modal-content').html(data.html_form)
                }
            }
        })
        return false;
    };

// Create a form
$(".show-form").click(ShowForm);
$('#modal-palier').on("submit", ".create-form", SaveForm);

// Update form
$('#table-palier').on("click", ".show-form-update", ShowForm);
$('#modal-palier').on("submit", ".update-form", SaveForm);

// Delete form
$('#table-palier').on("click", ".show-form-delete", ShowForm);
$('#modal-palier').on("submit", ".delete-form", SaveForm);

});