var datePickers = {};

Vue.directive('datepicker', {
    bind: function(param) {
        var vm = this.vm;
        var key = this.expression;

        datePickers[key] = new Pikaday({
            field: $(this.el)[0],
            position: 'bottom',
            showTime: false,
            use24hour: true,
            maxDate: moment().toDate(),
            onSelect: function(date) {
                vm.$set(key, date);
                if (key == 'dateTimeFrom') {
                    datePickers['dateTimeTo'].setMinDate(date);
                    datePickers['dateTimeTo'].gotoDate(date);
                    datePickers['dateTimeTo'].show();
                }
            }
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