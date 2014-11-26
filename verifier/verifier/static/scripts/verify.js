//Javascript file for ID Verification page

//This is the number of results to show max.  There is a server side limit too, which needs
//to be set heigher than this so we can detect if there are more results than we are showing.
var VOTER_RESULTS_LIMIT = 3

$(function () {
    $('#state_select').selectize({
        selectOnTab: true
    })

    $('#ballot_id_select').selectize({
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

    $.validator.addMethod("dateFormat", function (value, element) {
        return value.match(/^(?:[1-9]|1[012])\/([1-9]|[12][0-9]|3[01])\/(19|20)\d\d$/);
    }
    , "This field is not a valid date Format: MM/DD/YYYY");

    var validator = form.validate({
        onsubmit: false,
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

    function getVoterName(voter) {
        name = '<div class="voter-name">' + voter.last_name + ', ' + voter.first_name;
        if (voter.middle_name) {
            name += ' ' + voter.middle_name;
        }

        if (voter.suffix) {
            name += ', ' + voter.suffix;
        }
        name += '</div>'
        return name;
    }

    function getVoterAddress(voter) {
        address = '<div class="voter-address row">'
        address += '<div class="col col-sm-12 address">' + voter.address_1 + '</div>';
        if (voter.address_2) {
            '<div class="col col-sm-12 address">' + voter.address_2 + '</div>';
        }
        address += '<div class="col col-sm-12 city-state-zip">' + voter.city + ', ' + voter.state + ' ' + voter.zip + '</div>'

        address += '</div>'
        return address;
    }

    function getVoterOther(voter) {
        other = '<div class="other col col-sm-6">'
        other += '<div class="row"><div class="col col-sm-12 birth-date"><label>Birth Date:</label> ' + voter.birth_date + '</div></div>'
        other += '<div class="row"><div class="col col-sm-12 voter-id"><label>Voter ID:</label> ' + voter.voter_id + '</div></div>'
        other += '<div class="row"><div class="col col-sm-12 precinct"><label>Precinct:</label> ' + voter.precinct + '</div></div>'
        other += '</div>'
        return other;
    }

    function getVoter(voter, voterIndex) {
        return '<div class="voter row" data-voter-index=' + voterIndex + '> ' +
            '<div class="col col-sm-6">' +
            getVoterName(voter) +
            getVoterAddress(voter) +
            '</div>' +
            getVoterOther(voter) +

            '</div>'


    }

    function selectVoter($voter) {

        $('.voter').removeClass('selected');

        moveCaretToEnd($('#voter_search')[0])
        if ($voter.length == 0) {
            //no voter selected
            return;
        }

        $voter.addClass('selected')

        voter = results[parseInt($voter.data('voter-index'))]

        $.each(voter, function (key, value) {
            $element = $('#' + key);
            if ($element.length > 0) {
                //This requires for the form ids to match the voter property names

                if ($element.hasClass('selectized')) {
                    $element[0].selectize.addItem(value);
                }
                else {
                    $element.val(value);
                }

                if (key == 'state' || key == 'ballot_id') {
                    //there is no way to make them a dropdown read only, you can only disable
                    //which prevents it from submitting.  so we have hidden field to submit the value
                    //and the dropdown is just for looks but we still need to update it so it reflects the hidden field value
                    //the name of the dropdown will be the same as the hidden field with _selecte at the end
                    $select = $('#' + key + "_select")
                    if ($select.length > 0 && $select.hasClass('selectized')) {
                        $select[0].selectize.addItem(value);
                    }

                }


            }
            else {

            }
        });
    }

    function populateVoters() {

        if (results && results.length > 0) {

            var result_count = results.length;
            var show_more_results_msg = false;

            if (result_count > VOTER_RESULTS_LIMIT) {
                result_count = VOTER_RESULTS_LIMIT;
                show_more_results_msg = true;
            }

            voters = ''
            for (i = 0; i < result_count; i++) {
                voters += getVoter(results[i], i);
            }
            if (show_more_results_msg) {
                voters += '<div class="row more-results"><div class="col col-sm-12">There are too many results for this search.&nbsp;&nbsp;Please enter more search terms.</div></div>'
            }

            //remove all the clicks on the current voters if there are any
            $('.voter').off();

            $('#search-results').html(voters);
            $('.voter').click(function () {
                selectVoter($(this))
            });

        }
        else {
            return $('#search-results').html('<div class="row"><div class="col col-sm-12 no-results">Your search did not return any voters.</div></div>');
        }
    }

    var searchVoterRequest = false;
    var results = []
    function moveCaretToEnd(input) {
        try {
            if (!input) {
                return;
            }
            var len = input.value.length;
            input.setSelectionRange(len, len);
        } catch (ex) {
        }
    };

    function processKeyUpDown(e) {
        //processes key up or down returns true if up or down key was pressed
        //this changes the voter selection

        function selectVoterByKeypress(down) {
            $all_voters = $('.voter');
            $selected_voter = $('.voter.selected');


            if ($selected_voter.length == 0 && down) {
                $selected_voter = $($all_voters[0]);
            }
            else if ($selected_voter.length > 0) {                
                
                if (down) {
                    i = parseInt($selected_voter.data('voter-index')) + 1
                    if (i >= $all_voters.length) {
                        i = 0;
                    }
                    $selected_voter = $($all_voters[i]);
                }
                else {
                    i = parseInt($selected_voter.data('voter-index')) - 1
                    if (i < 0) {
                        i = ($all_voters.length - 1);
                    }

                    $selected_voter = $($all_voters[i]);
                }
                
            }
            
            selectVoter($selected_voter)
        }
        
        if (e.which == 38) {
            //up key
            selectVoterByKeypress(false)
            e.preventDefault();
            return true;
        }
        else if (e.which == 40) {
            //down key
            selectVoterByKeypress(true)
            e.preventDefault();
            return true;
        }
        else {
            return false;
        }
    }

    function doVoterSearch(e) {

        if (processKeyUpDown(e)) {
            return;
        }

        delay(function () {
            query = $('#voter_search').val()
            if (query.length < 3) {
                //to short will return too many responses
                $('#search-results').html('<div class="row "><div class="col col-sm-12">&nbsp;</div></div>');
                return;
            }

            data = {
                'query': $('#voter_search').val()
            }


            if (searchVoterRequest) {

                searchVoterRequest.abort()
            }

            searchVoterRequest = $.getJSON(SCRIPT_ROOT + "/search-voters", data)
                .done(function (data) {
                    results = data.results;
                    populateVoters();
                    searchVoterRequest = null;

                })
                .fail(function (jqXHR, textStatus, errorThrown) {
                    results = [];
                    console.log(textStatus, errorThrown, jqXHR);
                })

        }, 200);
    }



    $('#accept').click(accept);
    $('#reject').click(reject);
    $('#voter_search').keyup(doVoterSearch);
    $('#voter_search').focus();


})