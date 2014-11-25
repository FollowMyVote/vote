//Javascript file for ID Verification page

//This is the number of results to show max.  There is a server side limit too, which needs
//to be set heigher than this so we can detect if there are more results than we are showing.
var VOTER_RESULTS_LIMIT = 3

$(function () {
    $('#state').selectize({
        selectOnTab: true
    })

    $('#ballot_id').selectize({
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

    function getVoterName(voter){
        name = '<div class="voter-name">' + voter.last_name + ', ' +  voter.first_name;
        if (voter.middle_name){
            name += ' ' + voter.middle_name;
        }

        if (voter.suffix){
            name += ', ' + voter.suffix;
        }
        name += '</div>'
        return name;
    }

    function getVoterAddress(voter){
        address = '<div class="voter-address row">'
        address += '<div class="col col-sm-12 address">' + voter.address_1 +'</div>';
        if (voter.address_2) {
            '<div class="col col-sm-12 address">' + voter.address_2 +'</div>';
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

    function getVoter(voter, voterIndex){
        return '<div class="voter row" data-voter-index=' + voterIndex + '> ' +
            '<div class="col col-sm-6">' +
            getVoterName(voter) +
            getVoterAddress(voter) + 
            '</div>' + 
            getVoterOther(voter) +
            
            '</div>'

            
    }
    
    function populateVoters(results) {

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
                voters += '<div class="row voter more-results"><div class="col col-sm-12">There are too many results for this search.&nbsp;&nbsp;Please enter more search terms.</div></div>'
            }

            //remove all the clicks on the current voters if there are any
            $('.voter').off();

            $('#search-results').html(voters);
            $('.voter').click(function () {
                alert($(this).data('voter-index'));
            });

        }
        else{
            return $('#search-results').html('<div class="row"><div class="col col-sm-12 no-results">Your search did not return any voters.</div></div>');
        }
    }

    var searchVoterRequest = false;
    
    function doVoterSearch() {
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

            console.log('begin search voter');
            if (searchVoterRequest){
                
                searchVoterRequest.abort()
            }

            searchVoterRequest = $.getJSON(SCRIPT_ROOT + "/search-voters", data)
                .done(function (data) {
                    populateVoters(data.results);
                    searchVoterRequest = null;

                })
                .fail(function (jqXHR, textStatus, errorThrown) {
                    console.log(textStatus, errorThrown, jqXHR);
                })

        }, 200);
    }



    $('#accept').click(accept);

    $('#reject').click(reject)

    $('#voter_search').keyup(doVoterSearch)

})