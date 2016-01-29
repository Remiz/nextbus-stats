
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
        direction: null,
        stops: [],
        dateTimeFrom: null,
        dateTimeTo: null,
    },
    methods: {
        updateChart: function() {
            $.ajax({
                method: 'POST',
                url: url_get_chart,
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
                vm.stops = response.content.stops;
            });
        }
    },

});