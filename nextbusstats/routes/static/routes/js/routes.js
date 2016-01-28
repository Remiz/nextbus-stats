
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
        dateTimeFrom: null,
        dateTimeTo: null,
    },
    methods: {
        UpdateChart: function() {
            $.ajax({
                method: 'POST',
                url: url_get_chart,
            }).done(function(response) {
                console.log(response);
            });
        }
    },

});