//This is a global javascript file for the entire site.

//is a function to delay a call, it will cancel the previous call if a second call is made while the delay is in process
//usage example:
//delay(function(){alert('test');} , 200)
var delay = (function () {
    var timer = 0;
    return function (callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
})();

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

