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
        hideCharts: true,
        showWarning: false,
        stops: [],
    },
    computed: {

    },
    methods: {
        updateCharts: function() {
            // Check that all required parameters are selected
            if ( moment(this.dateTimeFrom).isValid() &&
                 moment(this.dateTimeTo).isValid() &&
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
                vm.stops = response.content.stops;
            });
        },
        updateTimePlotChart: function() {
            // make the dateTimeTo inclusive (add 23 hours 59 minutes and 59 seconds)
            dateTimeTo = moment(this.dateTimeTo).add(86400-1, 's');
            $.ajax({
                method: 'POST',
                url: url_get_chart,
                data: {
                    datetime_from: this.dateTimeFrom.toISOString(),
                    datetime_to: dateTimeTo.toISOString(),
                    stop_selected: this.stopSelected,
                    timezone: moment.tz.guess(),
                }
            }).done(function(response) {
                if (response.status != 200) {
                    console.log(response);
                    return false;
                }
                if (window.time_plot_chart){
                    window.time_plot_chart.destroy();
                }
                predictions = response.content.predictions;
                labels = [];
                data = [];
                for (var i =0; i < predictions.length; i++){
                    labels.push(predictions[i].posted_at);
                    data.push(predictions[i].prediction);
                }
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
                            }]
                        }
                    }
                });
            });
        },
        updateDailyAverageChart: function() {
            $.ajax({
                method: 'POST',
                url: url_get_daily_average_chart,
                data: {
                    stop_selected: this.stopSelected,
                    timezone: moment.tz.guess(),
                }
            }).done(function(response) {
                if (response.status != 200) {
                    console.log(response);
                    return false;
                }
                if (window.daily_average_chart){
                    window.daily_average_chart.destroy();
                }
                avg_weekday = response.content.avg_weekday;
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
            });
        },
        updateHourlyAverageChart: function() {
            $.ajax({
                method: 'POST',
                url: url_get_hourly_average_chart,
                data: {
                    stop_selected: this.stopSelected,
                    timezone: moment.tz.guess(),
                }
            }).done(function(response) {
                if (response.status != 200) {
                    console.log(response);
                    return false;
                }
                if (window.hourly_average_chart){
                    window.hourly_average_chart.destroy();
                }
                avg_hourly = response.content.avg_hourly;
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
            });
        }
    },

});