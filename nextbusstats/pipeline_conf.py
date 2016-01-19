PIPELINE = {
    #'PIPELINE_ENABLED': True,
    'STYLESHEETS': {
        'global': {
            'source_filenames': (
              'css/core.css',
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
              'js/jquery.js',
            ),
            'output_filename': 'js/global.js',
        }
    }
}
