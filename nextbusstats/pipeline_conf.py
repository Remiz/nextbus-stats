PIPELINE = {
    #'PIPELINE_ENABLED': True,
    'STYLESHEETS': {
        'global': {
            'source_filenames': (
                'foundation-sites/dist/foundation.min.css',
                'pikaday-time/css/pikaday.css',
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
                'pikaday-time/pikaday.js',
                'pikaday-time/plugins/pikaday.jquery.js',
                'moment/min/moment.min.js',
                'moment-timezone/builds/moment-timezone-with-data.min.js',
                'Chart.js/Chart.min.js',
                'vue/dist/vue.min.js',
                'common/js/csrf.js',
                'routes/js/routes.js',
            ),
            'output_filename': 'js/global.js',
        }
    }
}
