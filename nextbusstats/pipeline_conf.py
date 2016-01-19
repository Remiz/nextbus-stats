PIPELINE = {
    #'PIPELINE_ENABLED': True,
    'STYLESHEETS': {
        'global': {
            'source_filenames': (
                'foundation-sites/dist/foundation.min.css',
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
                'moment/min/moment.min.js',
                'Chart.js/Chart.min.js',
            ),
            'output_filename': 'js/global.js',
        }
    }
}
