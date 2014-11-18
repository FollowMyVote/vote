
$(function () {

    $('.contest').click(function () {
        
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
                text: 'Approval Vote',
                align:'left'
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
                data: summaryAllOpinions
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
                text: 'Official Vote',
                align:'left'
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
        $('#results').DataTable().search($(this).val()).draw();
    });
    



});