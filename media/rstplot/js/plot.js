var plot = (function() {
    var easelShape, easelStage;
    var purpleColor = 'rgba(152,58,178,1)';
    var redColor = 'rgba(171,38,52,1)';
    var overlayColor = 'rgba(178,31,43,0.5)';


    var filterCanvas = function(can, ctx, filter) {
        if (can.width > 0 && can.height > 0) {
            var imageData = ctx.getImageData(0, 0, can.width, can.height);
            filter(imageData);
            ctx.putImageData(imageData, 0, 0);
        }
    };

    /*
     * Draw the legend canvases
     */
    var drawLegend = function($container, can, ctx) {
        var items = ['fp', 'tp', 'tn', 'fn'];
        $.each(items, function(k, v) {
            var can = $container.find('#plot-legend-' + v)[0];
            var ctx = can.getContext('2d');

            if (v == 'fp' || v == 'tn') {
                var imageObj = new Image();

                imageObj.onload = function() {
                    ctx.drawImage(imageObj, -140, -40);
                    if (v == 'tn') {
                        ctx.fillStyle = overlayColor;
                        ctx.rect(0, 0, can.width, can.height);
                        ctx.fill();
                    }
                };
                imageObj.src = '/media/rstplot/img/rst-green.png';
            } else {
                ctx.fillStyle = purpleColor;
                ctx.rect(0, 0, can.width, can.height);
                ctx.fill();
                if (v == 'fn') {
                    ctx.fillStyle = overlayColor;
                    ctx.rect(0, 0, can.width, can.height);
                    ctx.fill();
                }
            }
        });
    };

    /*
     * Draw the plot's lines and text
     */
    var drawPlot = function(can, ctx) {
        var numSamples = 20;
        var rowHead = 25;
        var margin = 12;
        var plotLineHeight = 15;
        var horizLinePos = can.height - margin - (margin/2) - 2;
        var header = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
            16, 17, 18, 19, 20];

        ctx.fillStyle = 'black';
        ctx.font = '10pt Helvetica';

        // set horizontal scalar to available width / number of samples
        var xScalar = (can.width - rowHead) / numSamples;

        ctx.strokeStyle = 'black';
        ctx.strokeWidth = 1;
        var translate = (ctx.strokeWidth % 2) / 2;
        ctx.translate(translate, 0);
        ctx.beginPath();
        ctx.textAlign = 'center';
        // print  column header and draw vertical grid lines
        for (i = 1; i <= numSamples; i++) {
            var x = Math.round(i * xScalar);

            ctx.fillText(header[i], x, can.height);
            ctx.moveTo(x, can.height - margin);
            ctx.lineTo(x, can.height - plotLineHeight - margin);
        }
        ctx.stroke();
        ctx.translate(-translate, 0);

        // Draw horiz line
        ctx.translate(0, translate);
        ctx.beginPath();
        ctx.moveTo(0, horizLinePos);
        ctx.lineTo(can.width, horizLinePos);
        ctx.stroke();
        ctx.translate(0, -translate);
    };

    /*
     * Draw the plot's text
     */
    var drawPlotText = function(can, ctx) {
        ctx.font = '9pt Helvetica';
        ctx.textAlign = 'center';

        var txt = 'True Distribution of Disease';
        var x = can.width / 2 + 10;
        var y = 10;
        ctx.fillText(txt, x, y);

        ctx.fillText('True D-', can.width / 2 - 160, 40);
        ctx.fillText('True D+', can.width / 2 + 110, 60);
    };

    /*
     * Draw an image to a canvas.
     * Returns a promise.
     */
    var drawImage = function(ctx, imgUrl, x, y) {
        return new RSVP.Promise(function(resolve, reject) {
            var imageObj = new Image();
            imageObj.onload = function() {
                ctx.drawImage(imageObj, x, y);
                resolve();
            };
            imageObj.src = imgUrl;
        });
    }

    /*
     * Draw the plot's background images.
     * Returns a promise.
     */
    var drawPlotBg = function(can, ctx) {
        easelStage = new createjs.Stage(
            document.getElementById('easel-canvas'));
        easelShape = new createjs.Shape();
        easelShape.graphics.beginFill(overlayColor)
            .drawRect(-can.width, 0, can.width, can.height - 19, 10);
        easelStage.addChild(easelShape);
        easelStage.update();

        return drawImage(ctx, '/media/rstplot/img/purple-path.png', 200, 0)
            .then(function() {
                drawImage(ctx, '/media/rstplot/img/rst-green.png', 0, 0);
            });
    };

    var updateCalcValues = function($container, x) {
        var sensitivity = plot.calcSensitivity(x);
        var specificity = plot.calcSpecificity(x);

        $container.find('#plot-sensitivity').html(sensitivity);
        $container.find('#plot-specificity').html(specificity);
    };

    var moveEaselShape = function(x) {
        easelShape.x = x;
        easelStage.update();
    };

    return {
        calcSensitivity: function(x) {
            var r;
            if (x < 9) {
                r = 1;
            } else if (x < 11) {
                r = .99;
            } else if (x < 12) {
                r = .96;
            } else if (x < 13) {
                r = .81;
            } else if (x < 14.5) {
                r = .67;
            } else if (x < 16) {
                r = .5;
            } else if (x < 18) {
                r = .19;
            } else if (x < 19) {
                r = .04;
            } else {
                r = .01;
            }
            return r;
        },

        calcSpecificity: function (x) {
            var r;
            if (x < 2) {
                r = 0;
            } else if (x < 3) {
                r = .02;
            } else if (x < 4) {
                r = .04;
            } else if (x < 6) {
                r = .1;
            } else if (x < 7) {
                r = .2;
            } else if (x < 7.5) {
                r = .34;
            } else if (x < 8) {
                r = .5;
            } else if (x < 9) {
                r = .66;
            } else if (x < 10) {
                r = .8;
            } else if (x < 12) {
                r = .9;
            } else if (x < 14) {
                r = .98;
            } else if (x < 15) {
                r = .99;
            } else {
                r = 1;
            }
            return r;
        },

        initPlot: function(container) {
            var $container = $rstplotJquery(container);

            drawLegend($container);

            var can = $container.find('#plot-canvas')[0];
            var ctx = can.getContext('2d');
            drawPlotBg(can, ctx)
                .then(function() {
                    drawPlot(can, ctx);
                    drawPlotText(can, ctx);
                });

            var $slider = $container.find('#plot-slider');
            $slider.slider({
                slide: function(e, ui) {
                    var val = ui.value * .21;
                    updateCalcValues($container, val);

                    var width = $container.find('#easel-canvas').width();
                    var xPos = width * (ui.value / 100);
                    moveEaselShape(xPos);
                },
                step: 0.01
            });
            $slider.find('.ui-slider-handle').append(
                '<div class="plot-hint">Screening Test</div>' +
                '<div class="plot-hint">Cutpoint</div>' +
                '<div class="plot-cutpoint-tri"></div>'
            );
        }
    };
}());
