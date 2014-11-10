//Javascript file for ID Verification page

$(function () {
    $('#state').selectize({
        selectOnTab: true,
        allowEmptyOption: true
    })
    $('#rejection_reason').selectize({
        create: true,
        createOnBlur: true,
        selectOnTab: true,
        allowEmptyOption: true
    })

    if (refreshPage) {
        setTimeout(function () {

            window.location.reload();
        }, 5000);

    }



    $('#owner>.image-wrapper').zoom();
    $('#id-back>.image-wrapper').zoom();
    $('#id-front>.image-wrapper').zoom();
    $('#voter-reg>.image-wrapper').zoom();
    var validator = $('form').validate({
        ignore: ':hidden:not([class~=selectized]),:hidden > .selectized, .selectize-control .selectize-input input'
    });
    
    $('#accept').click(function () {
        if ($('#owner_photo_invalid').prop('checked')) {
           
            validator.showErrors({
                "owner_photo_invalid": "Photo cannot be marked invalid if id is accepted."
            });
        }

    })

    $('#reject').click(function () {
        if ($('#rejection_reason').val() == "") {
            validator.showErrors({
                "rejection_reason": "This field is required"
            });
        }
    })



})