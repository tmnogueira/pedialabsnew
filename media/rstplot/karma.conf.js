module.exports = function(config) {
    config.set({
        basePath: 'js',
        frameworks: ['qunit'],
        files: [
            'lib/jquery.min.js',
            'lib/jquery-ui.min.js',
            'plot.js',
            'test/unit_tests.js',
        ],
        reporters: ['dots'],
        port: 9876,
        colors: true,
        logLevel: config.LOG_INFO,
        autoWatch: true,
        browsers: ['PhantomJS'],
        singleRun: true
    });
};
