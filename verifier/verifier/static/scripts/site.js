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
            //if there is a panel body in the form group then add the error
            //text there instead
            var formGroup = element.closest('.form-group')
            var panelBody = formGroup.children('.panel-body')

            if (panelBody.length > 0) {
                panelBody.append(error);
            }
            else {
                formGroup.append(error);
            }



        }
    }
});

