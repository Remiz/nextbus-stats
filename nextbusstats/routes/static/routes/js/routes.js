
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
                    datetime_from: this.dateTimeFrom,
                    datetime_to: this.dateTimeTo,
                    stop_selected: this.stopSelected,
                }
            }).done(function(response) {
                console.log(response);
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