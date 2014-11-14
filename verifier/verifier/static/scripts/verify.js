//Javascript file for ID Verification page

$(function () {
    $('#state').selectize({
        selectOnTab: true
       
    })
    $('#rejection_reason').selectize({
        create: true,
        createOnBlur: true,
        selectOnTab: false
        
    })

    if (refreshPage) {
        setTimeout(function () {

            window.location.reload();
        }, 5000);

    }



    $('.image-wrapper').zoom();
    
    var form = $('form');

    var isAccepting = false;

    $.validator.addMethod("checkImageInvalid", function (value, element) {
        return !isAccepting || !$(element).prop('checked');
        }
    , "Photo should not be marked invalid if the id is being accepted.");

    var validator = form.validate({
        onsubmit:false,
        ignore: ':hidden:not([class~=selectized]),:hidden > .selectized, .selectize-control .selectize-input input'
    });

    function accept() {
        $('#result').val('accept');
        isAccepting = true;
        $('.has-error').removeClass('has-error');
        if (form.valid()) {
            form.submit();
        }
    }
    function reject() {
        $('#result').val('reject');
        isAccepting = false;
        validator.resetForm();
        $('.has-error').removeClass('has-error');
        if ($('#rejection_reason').val() == "" &&
            !$('.checkImageInvalid').is(':checked')) {
            validator.showErrors({
                "rejection_reason": "Please enter a rejection reason or select an invalid image."
            });
        }
        else {
            form.submit();
        }
    }

    $('#accept').click(accept);

    $('#reject').click(reject)




})