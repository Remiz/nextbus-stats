
Vue.directive('datepicker', {
    bind: function(param) {
        var vm = this.vm;
        var key = this.expression;
        $(this.el).fdatepicker({
            pickTime: true,
            format: 'mm/dd/yyyy hh:ii',
            onRender: function(date) {
                if (key == 'dateTimeFrom') {
                    return date.valueOf() > moment().valueOf() ? 'disabled'  : '';
                } else {
                    if (date < vm.$get('dateTimeFrom') ||
                        date.valueOf() > moment().valueOf()) {
                        return 'disabled';
                    } else {
                        return '';
                    }
                }
            }
        }).on('changeDate', function(ev) {
            vm.$set(key, ev.date);
        });
    },
});

new Vue({
    el: '#routeApp',
    data: {
        stopSelected: null,
        dateTimeFrom: null,
        dateTimeTo: null,
        direction: null,
        stops: [],
    },
    methods: {
        updateChart: function() {
            $.ajax({
                method: 'POST',
                url: url_get_chart,
                data: {
                    datetime_from: this.dateTimeFrom.toISOString(),
                    datetime_to: this.dateTimeTo.toISOString(),
                    stop_selected: this.stopSelected,
                }
            }).done(function(response) {
                if (window.myChart){
                    window.myChart.destroy();
                }
                predictions = response.content.predictions;
                labels = [];
                data = [];
                for (var i =0; i < predictions.length; i++){
                    labels.push(predictions[i].posted_at);
                    data.push(predictions[i].prediction);
                }
                window.myChart = new Chart($(routeChart), {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'seconds',
                            data: data
                        }]
                    },
                    options:{
                        scales:{
                            yAxes:[{
                                ticks:{
                                    beginAtZero:true
                                }
                            }],
                            xAxes: [{
                                type: 'time',
                            }]
                        }
                    }
                });
            });
        },
        updateStops: function() {
            var vm = this;
            $.ajax({
                method: 'POST',
                url: url_get_stops_from_direction,
                data: { direction: this.direction },
            }).done(function(response) {
                vm.stopSelected = "";
                vm.stops = response.content.stops;
            });
        }
    },

});