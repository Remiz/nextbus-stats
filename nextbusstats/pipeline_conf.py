PIPELINE = {
    #'PIPELINE_ENABLED': True,
    'STYLESHEETS': {
        'global': {
            'source_filenames': (
                'foundation-sites/dist/foundation.min.css',
                'foundation-datepicker/css/foundation-datepicker.min.css',
                'foundation-icon-fonts/foundation-icons.css',
                'routes/css/routes.css',
            ),
            'output_filename': 'css/global.css',
            'extra_context': {
                'media': 'screen,projection',
            },
        },
    },
    'JAVASCRIPT': {
        'global': {
            'source_filenames': (
                'jquery/dist/jquery.min.js',
                'foundation-sites/dist/foundation.min.js',
                'foundation-datepicker/js/foundation-datepicker.min.js',
                'moment/min/moment.min.js',
                'Chart.js/Chart.min.js',
                'vue/dist/vue.min.js',
                'common/js/csrf.js',
                'routes/js/routes.js',
            ),
            'output_filename': 'js/global.js',
        }
    }
}
