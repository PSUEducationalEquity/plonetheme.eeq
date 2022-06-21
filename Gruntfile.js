module.exports = function (grunt) {
    'use strict';
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        // we could just concatenate everything, really
        // but we like to have it the complex way.
        // also, in this way we do not have to worry
        // about putting files in the correct order
        // (the dependency tree is walked by r.js)
        less: {
            dist: {
                options: {
                    paths: [],
                    math: "always",
                    strictMath: false,
                    sourceMap: true,
                    outputSourceFiles: true,
                    sourceMapFileInline: false,
                    sourceMapURL: '../less/theme-compiled.less.map',
                    sourceMapFilename: '../less/theme-compiled.less.map',
                    modifyVars: {
                        "isPlone": "false"
                    }
                },
                files: {
                    '../build/theme-compiled.css': '../less/theme.local.less',
                }
            }
        },
        cssmin: {
            options: {
                sourceMap: true
            },
            target: {
                files: [{
                    expand: false,
                    dest: 'theme-compiled.min.css',
                    src: ['../node_modules/bootstrap/dist/css/bootstrap.css',
                          '../styles/open-iconic-bootstrap.css',
                          '../build/theme-compiled.css']
                }]
            }
        },
        uglify: {
            options: {
                mergeIntoShorthands: false,
                sourceMap: true
            },
            my_target: {
                files: {
                    'eeq-loader.min.js': ['../scripts/loader.js'],
                    'eeq-scripts.min.js': ['../scripts/bootstrap.bundle.js', '../scripts/main.js']
                }
            }
        },
        watch: {
            scripts: {
                files: [
                    '../less/*.less',
                    '../scripts/main.js',
                ],
                tasks: ['compile'],
                options: {
                    spawn: false,
                },
            }
        },
        browserSync: {
            html: {
                bsFiles: {
                    src: [
                        '../less/*.less',
                        '../scripts/main.js',
                        '../*.html'
                    ]
                },
                options: {
                    watchTask: true,
                    debugInfo: true,
                    online: true,
                    server: {
                        baseDir: "../"
                    },
                }
            },
            plone: {
                bsFiles: {
                    src: [
                        '../less/*.less',
                        '../scripts/main.js',
                        '../*.html',
                        '../*.xml'
                    ]
                },
                options: {
                    watchTask: true,
                    debugInfo: true,
                    proxy: "localhost:8080",
                    reloadDelay: 3000,
                    // reloadDebounce: 2000,
                    online: true,
                    open: false
                }
            }
        }
    });


    // grunt.loadTasks('tasks');
    grunt.loadNpmTasks('grunt-browser-sync');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-uglify');

    // CWD to theme folder
    grunt.file.setBase('./src/plonetheme/eeq/theme/build');

    grunt.registerTask('compile', ['less', 'cssmin', 'uglify']);
    grunt.registerTask('default', ['compile']);
    grunt.registerTask('bsync', ["browserSync:html", "watch"]);
    grunt.registerTask('plone-bsync', ["browserSync:plone", "watch"]);
};
