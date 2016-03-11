var datePickers = {};
var timePickers = {};

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
                if (key == 'dateFrom') {
                    datePickers['dateTo'].setMinDate(date);
                    datePickers['dateTo'].gotoDate(date);
                    datePickers['dateTo'].show();
                }
            }
        });
    },
});

Vue.directive('timepicker', {
    bind: function(param) {
        var vm = this.vm;
        var key = this.expression;

        timePickers[key] = $(this.el).timepicker({
            step: 15,
            timeFormat: 'H:i',
        });

        $(this.el).on('changeTime', function(e) {
            vm.$set(key, timePickers[key].val());
            /*
            if (key == 'timeStart') {
                timePickers['timeEnd'].timepicker('option', 'minTime', timePickers['timeStart'].val());
            } else {
                timePickers['timeStart'].timepicker('option', 'maxTime', timePickers['timeEnd'].val());
            }
            */
        });
    }
});

new Vue({
    el: '#routeApp',
    data: {
        stopSelected: null,
        dateFrom: null,
        dateTo: null,
        timeStart: null,
        timeEnd: null,
        direction: null,
        hideCharts: true,
        showWarning: false,
        stops: [],
    },
    computed: {

    },
    methods: {
        updateCharts: function() {
            // Check that all required parameters are selected
            if ( moment(this.dateFrom).isValid() &&
                 moment(this.dateTo).isValid() &&
                 $.isNumeric(this.stopSelected))
            {
                this.updateTimePlotChart();
                this.updateDailyAverageChart();
                this.updateHourlyAverageChart();
                this.hideCharts = false;
                this.showWarning = false;
            } else {
                this.hideCharts = true;
                this.showWarning = true;
            }
        },
        updateStops: function() {
            var vm = this;
            $.ajax({
                method: 'POST',
                url: url_get_stops_from_direction,
                data: { direction: this.direction },
            }).done(function(response) {
                vm.stopSelected = "";
                vm.stops = response.stops;
            });
        },
        updateTimePlotChart: function() {
            if (window.time_plot_chart){
                window.time_plot_chart.destroy();
            }
            // make the dateTo inclusive (add 23 hours 59 minutes and 59 seconds)
            dateTo = moment(this.dateTo).add(86400-1, 's');
            $.ajax({
                method: 'POST',
                url: url_get_chart,
                data: {
                    date_from: this.dateFrom.toISOString(),
                    date_to: dateTo.toISOString(),
                    time_start: this.timeStart,
                    time_end: this.timeEnd,
                    stop_id: this.stopSelected,
                    timezone: moment.tz.guess(),
                }
            }).done(function(response) {
                predictions = response.predictions;
                labels = [];
                data = [];
                for (var i =0; i < predictions.length; i++){
                    labels.push(predictions[i].posted_at);
                    data.push(predictions[i].prediction);
                }
                var timeFormat = 'MM/DD/YYYY HH:mm';
                window.time_plot_chart = new Chart($("#timePlotChart"), {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'seconds',
                            fill: true,
                            backgroundColor: "rgba(116,169,207,0.2)",
                            borderColor: "rgba(5,112,176,1)",
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
                                time: {
                                    //format: timeFormat,
                                    tooltipFormat: 'll HH:mm'
                                }
                            }]
                        }
                    }
                });
            })
            .fail(function(response) {
                console.log(response);
                return false;
            });
        },
        updateDailyAverageChart: function() {
            if (window.daily_average_chart){
                window.daily_average_chart.destroy();
            }
            $.ajax({
                method: 'POST',
                url: url_get_daily_average_chart,
                data: {
                    stop_id: this.stopSelected,
                    timezone: moment.tz.guess(),
                }
            }).done(function(response) {
                avg_weekday = response.avg_weekday;
                labels = [];
                data = [];
                days_of_week = {  // Django starts weekday on Sunday
                    1: 'Sunday',
                    2: 'Monday',
                    3: 'Tuesday',
                    4: 'Wednesday',
                    5: 'Thursday',
                    6: 'Friday',
                    7: 'Saturday',
                };
                for (var key in avg_weekday){
                    weekday = days_of_week[key];
                    labels.push(weekday);
                    data.push(Math.round(avg_weekday[key]));
                }
                window.daily_average_chart = new Chart($("#dailyAverageChart"), {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'seconds',
                            backgroundColor: "rgba(5,112,176,1)",
                            //borderColor: "rgba(5,112,176,1)",
                            data: data
                        }]
                    },
                    options:{
                        scales:{
                            yAxes:[{

                            }],
                            xAxes: [{

                            }]
                        }
                    }
                });
            })
            .fail(function(response) {
                console.log(response);
                return false;
            });
        },
        updateHourlyAverageChart: function() {
            if (window.hourly_average_chart){
                window.hourly_average_chart.destroy();
            }
            $.ajax({
                method: 'POST',
                url: url_get_hourly_average_chart,
                data: {
                    stop_id: this.stopSelected,
                    timezone: moment.tz.guess(),
                }
            }).done(function(response) {
                avg_hourly = response.avg_hourly;
                labels = [];
                data = [];
                for (var key in avg_hourly){
                    labels.push(key);
                    data.push(Math.round(avg_hourly[key]));
                }
                window.hourly_average_chart = new Chart($("#hourlyAverageChart"), {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'seconds',
                            backgroundColor: "rgba(5,112,176,1)",
                            //borderColor: "rgba(5,112,176,1)",
                            data: data
                        }]
                    },
                    options:{
                        scales:{
                            yAxes:[{

                            }],
                            xAxes: [{

                            }]
                        }
                    }
                });
            })
            .fail(function(response) {
                console.log(response);
                return false;
            });
        }
    },

});