
$(function () {

    $('.contest').click(function () {
        if ($(this).attr('id')) {
        
            $('#contest_id').val($(this).attr('id'));
            $('#contest-form').submit();
        }

    });


    function resultSearch(){

        $('#results').DataTable().search($('#search_results').val()).draw();
    }


    function getElementsByDataValue($elements, dataKey, value){
        results = [];
        if ($elements){
            for(i = 0; i< $elements.length; i++){

                if ( $($elements[i]).data(dataKey) == value){
                    results.push($elements[i]);
                }
            }
        }
        return $(results);
    }


    function searchCandidate(candidate){



        $candidateRows = $('#candidate-table tbody tr');

        $candidateRow = getElementsByDataValue($('#candidate-table tbody tr'), 'candidate-name', candidate)

        if ($candidateRow.length){

            if ($candidateRow.hasClass('selected')){
                $candidateRow.removeClass('selected');
                candidate = "";
            }
            else{
                $candidateRows.removeClass('selected');
                $candidateRow.addClass('selected');
            }

        }





        chart =  $('#chart').highcharts();
        points = chart.series[0].points;
        for (i = 0 ; i < points.length; i++){
            points[i].slice(points[i].name == candidate, false);
        }
        chart.redraw();


        $('#search_results').val(candidate);
        resultSearch();




    }

    function getChart(){

    }

    function plotApprovalChart() {

        // Build the chart
        $('#chart').highcharts({
            credits:{
                enabled:false
            },
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'Approval Vote',
                align:'left'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    events: {
                        click: function(e){
                                searchCandidate(e.point.name);
                                }

                    },
                    point: {
                        events: {
                          legendItemClick: function () {
                                   return false; // <== returning false will cancel the default action
                                }
                        }
                    },
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [{
                type: 'pie',
                name: 'candidates',
                data: summaryAllOpinions
            }]
        });
    }

    function plotOfficialChart() {
        $('#chart').highcharts({
            credits:{
                enabled:false
            },
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'Official Vote',
                align:'left'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    events: {
                        click: function(e){
                                searchCandidate(e.point.name);
                                }

                    },
                    point: {
                        events: {
                          legendItemClick: function () {
                                   return false; // <== returning false will cancel the default action
                                }
                        }
                    },

                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [{
                type: 'pie',
                name: 'candidates',
                data: summaryOfficialOpinions
            }]
        });
    }

    plotOfficialChart();


    $('#btn-official, .official').click(function () {
        if (!$('.official').hasClass('selected')) {
            $('.approval').removeClass('selected');
            $('.official').addClass('selected');
            plotOfficialChart();

        }
    });

    $('#btn-approval, .approval').click(function () {
        if (!$('.approval').hasClass('selected')) {
            $('.official').removeClass('selected');
            $('.approval').addClass('selected');
            plotApprovalChart();

        }
    });

    
    $('#results').dataTable({
        "order": [3, 'asc'],
        "pageLength": 25,
        "dom": 'rtip'

    });

    $('#search_results').on('keyup', function () {
        resultSearch();
    });


    if ($('#search_results').val()){

        resultSearch();
    }

    $('#candidate-table tbody tr').click(function(){


        searchCandidate($(this).data('candidate-name'));

    });

    $('.contest-group-heading').click(function(){
        $(this).parent().children('.contest-group-inner').slideToggle( function(){

            $group = $(this).parent()

            if ($(this).is(":visible")){
                $group.addClass('expanded');
                $group.children('input.group_expanded').val('True');
            }
            else{
                $group.removeClass('expanded');
                $group.children('input.group_expanded').val('False');
            }

        });
    });

});