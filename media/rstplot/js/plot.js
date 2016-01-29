var plot = (function() {
    var palegreenColor = 'rgba(70,254,185,1)';
    var purpleColor = 'rgba(152,58,178,1)';
    var redColor = 'rgba(171,38,52,1)';

    // The plot bounds, independent of the canvas dimensions.
    var plotHeight = 125;
    var plotWidth = 550;

    /*
     * Draw the legend canvases
     */
    var drawLegend = function($container, can, ctx) {
        var items = ['fp', 'tp', 'tn', 'fn'];
        $rstplotJquery.each(items, function(k, v) {
            var can = $container.find('#plot-legend-' + v)[0];
            var ctx = can.getContext('2d');

            if (v == 'fp' || v == 'tn') {
                var imageObj = new Image();

                imageObj.onload = function() {
                    if (v == 'tn') {
                        ctx.fillStyle = palegreenColor;
                        ctx.rect(0, 0, can.width, can.height);
                        ctx.fill();
                    }
                    ctx.drawImage(imageObj, -140, -40);
                };
                imageObj.src = window.STATIC_URL + 'rstplot/img/rst-green.png';
            } else {
                ctx.fillStyle = purpleColor;
                ctx.rect(0, 0, can.width, can.height);
                ctx.fill();
                if (v == 'fn') {
                    ctx.fillStyle = redColor;
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
        var horizLinePos = plotHeight - margin - (margin/2) - 2;
        var header = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
            16, 17, 18, 19, 20];

        ctx.fillStyle = 'black';
        ctx.font = '10pt Helvetica';

        // set horizontal scalar to available width / number of samples
        var xScalar = (plotWidth - rowHead) / numSamples;

        ctx.strokeStyle = 'black';
        ctx.strokeWidth = 1;
        var translate = (ctx.strokeWidth % 2) / 2;
        ctx.translate(translate, 0);
        ctx.beginPath();
        ctx.textAlign = 'center';
        // print  column header and draw vertical grid lines
        for (i = 1; i <= numSamples; i++) {
            var x = Math.round(i * xScalar);

            ctx.fillText(header[i], x, plotHeight);
            ctx.moveTo(x, plotHeight - margin);
            ctx.lineTo(x, plotHeight - plotLineHeight - margin);
        }
        ctx.stroke();
        ctx.translate(-translate, 0);

        // Draw horiz line
        ctx.translate(0, translate);
        ctx.beginPath();
        ctx.moveTo(0, horizLinePos);
        ctx.lineTo(plotWidth, horizLinePos);
        ctx.stroke();
        ctx.translate(0, -translate);
    };

    /*
     * Draws the given text over a backdrop.
     */
    var drawTextWithBackdrop = function(ctx, txt, x, y) {
        ctx.save();
        var width = ctx.measureText(txt).width + 10;
        var height = 22;

        ctx.font = 'bold 9pt Helvetica';

        var oldFillStyle = ctx.fillStyle;
        ctx.fillStyle = 'rgba(255,255,255,0.8)';

        ctx.fillRect(x - (width/2), y - (height/2) - 5, width, height);

        ctx.fillStyle = oldFillStyle;
        ctx.fillText(txt, x, y);

        ctx.restore();
    };

    /*
     * Draw X and Y axis labels.
     *
     * FIXME: Right now Y axis labels are not drawn from here. The width of
     * plot is difficult to change, because of the tricky way it's been
     * implemented. 'overflow: hidden;' in the CSS prevents us from easily
     * adding extra width here, and it was simpler to add the Y axis label in a
     * seperate HTML element.
     */
    var drawAxisLabelText = function(can, ctx) {
        ctx.font = '9pt Helvetica';
        ctx.textAlign = 'center';
        var xAxisLabel = 'Test Result (continuous scale)';
        ctx.fillText(xAxisLabel, plotWidth / 2, can.height - 10);
    };

    /*
     * Draw the plot's text
     */
    var drawPlotText = function(can, ctx) {
        ctx.font = '9pt Helvetica';
        ctx.textAlign = 'center';

        var txt = 'True Distribution of Disease';
        var x = plotWidth / 2 + 10;
        var y = 10;
        ctx.fillText(txt, x, y);

        drawTextWithBackdrop(ctx, 'True D-', plotWidth / 2 - 90, 60);
        drawTextWithBackdrop(ctx, 'True D+', plotWidth / 2 + 110, 60);
        drawAxisLabelText(can, ctx);
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
    var drawPlotBg = function(can, ctx, side) {
        if (typeof side == 'undefined') {
            side = 'right';
        }

        if (side == 'right') {
            return drawImage(ctx, window.STATIC_URL + 'rstplot/img/purple-path.png', 200, 0)
                .then(function() {
                    return drawImage(ctx,
                                     window.STATIC_URL + 'rstplot/img/white-path.png',
                                     0, 0);
                })
                .then(function() {
                    return drawImage(ctx,
                                     window.STATIC_URL + 'rstplot/img/rst-green.png', 0, 0);
                });
        } else {
            return drawImage(ctx,
                             window.STATIC_URL + 'rstplot/img/palegreen-path.png', 0, 0)
                .then(function () {
                    return drawImage(ctx,
                                     window.STATIC_URL + 'rstplot/img/rst-green.png', 0, 0);
                })
                .then(function() {
                    return drawImage(ctx,
                                     window.STATIC_URL + 'rstplot/img/red-path.png',
                                     200, 0);
                });
        }


    };

    var updateCalcValues = function($container, x) {
        var sensitivity = plot.calcSensitivity(x);
        var specificity = plot.calcSpecificity(x);

        $container.find('#plot-sensitivity').html(sensitivity);
        $container.find('#plot-specificity').html(specificity);
    };

    var updateGraphsAndValues = function($container, ui) {
        var val = ui.value * .21;
        updateCalcValues($container, val);

        $container.find('.plot-left').width(ui.value + '%');
        $container.find('.plot-right').width((100-ui.value) + '%');
        $container.find('#plot-right-canvas').css('left',
                                                  (-ui.value * 5.5) + 'px');
    };

    return {
        calcSensitivity: function(x) {
            var r;
            if (x < 9) {
                r = 1;
            } else if (x < 10.1) {
                r = .99;
            } else if (x < 11.1) {
                r = .96;
            } else if (x < 12) {
                r = .9;
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
            } else if (x < 11.1) {
                r = .9;
            } else if (x < 12) {
                r = .96;
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

            var can1 = $container.find('#plot-left-canvas')[0];
            var ctx1 = can1.getContext('2d');
            drawPlotBg(can1, ctx1, 'left').then(function() {
                drawPlot(can1, ctx1);
                drawPlotText(can1, ctx1);
            });

            var can2 = $container.find('#plot-right-canvas')[0];
            var ctx2 = can2.getContext('2d');
            drawPlotBg(can2, ctx2, 'right').then(function() {
                drawPlot(can2, ctx2);
                drawPlotText(can2, ctx2);
            });

            var $slider = $container.find('#plot-slider');
            $slider
                .slider({
                    value: 51,
                    step: 0.01,
                    change: function(e, ui) {
                        updateGraphsAndValues($container, ui);
                    },
                    slide: function(e, ui) {
                        updateGraphsAndValues($container, ui);
                    }
                })
                // Needed to trigger the 'change' event on init
                .slider('value', 51);

            $slider.find('.ui-slider-handle').append(
                '<div class="plot-hint">Screening Test</div>' +
                '<div class="plot-hint">Cutpoint</div>' +
                '<div class="plot-cutpoint-tri"></div>'
            );
        }
    };
}());
