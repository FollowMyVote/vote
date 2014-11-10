//This is a global javascript file for the entire site.


$.validator.setDefaults({
    highlight: function (element) {
        $(element).closest('.form-group').addClass('has-error');
    },
    unhighlight: function (element) {
        $(element).closest('.form-group').removeClass('has-error');
    },
    errorElement: 'span',
    errorClass: 'help-block',
    errorPlacement: function (error, element) {
        if (element.parent('.input-group').length) {
            error.insertAfter(element.parent());
        } else {
            element.closest('.form-group').append(error);
            //if (element.hasClass('selectized')) {
            //    error.insertAfter(element.parent().children('.selectize-control')[0])
            //}
            //else {
            //    error.insertAfter(element);
            //}
            
        }
    }
});

