
$(function () {

    $('.contest').click(function () {
        $('.contest').removeClass('selected');
        $(this).addClass('selected');
        $('#contest_id').val($(this).attr('id'));
        $('#contest_form').submit();
        


    });


    function plotApprovalChart() {

        // Build the chart
        $('#chart').highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: ''
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            series: [{
                type: 'pie',
                name: 'candidates',
                data: [
                    ['Candidate A', 53],
                    ['Candidate B', 37],
                    ['Candidate C', 7],
                    ['Other', 3]
                ]
            }]
        });
    }

    function plotOfficialChart() {
        $('#chart').highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: ''
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            series: [{
                type: 'pie',
                name: 'candidates',
                data: [
                    ['Candidate A', 46],
                    ['Candidate B', 51],
                    ['Candidate C', 2],
                    ['Other', 1]
                ]
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



});