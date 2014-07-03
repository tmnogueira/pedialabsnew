test('calcSensitivity', function() {
    expect(24);

    function roundCalc(x) {
        var r = plot.calcSensitivity(x);
        // We're just comparing to two decimal places, so round our test result
        return Math.round(r * 100) / 100;
    }

    equal(roundCalc(-5), 1);
    equal(roundCalc(0), 1);
    equal(roundCalc(1), 1);
    equal(roundCalc(2), 1);
    equal(roundCalc(3), 1);
    equal(roundCalc(4), 1);
    equal(roundCalc(5), 1);
    equal(roundCalc(6), 1);
    equal(roundCalc(7), 1);
    equal(roundCalc(8), 1);
    equal(roundCalc(9), .99);
    equal(roundCalc(10), .99);
    equal(roundCalc(11), .96);
    equal(roundCalc(12), .81);
    equal(roundCalc(13), .67);
    equal(roundCalc(14), .67);
    equal(roundCalc(14.5), .5);
    equal(roundCalc(15), .5);
    equal(roundCalc(16), .19);
    equal(roundCalc(17), .19);
    equal(roundCalc(18), .04);
    equal(roundCalc(19), .01);
    equal(roundCalc(20), .01);
    equal(roundCalc(25), .01);
});

test('calcSpecificity', function() {
    expect(24);

    function roundCalc(x) {
        var r = plot.calcSpecificity(x);
        // We're just comparing to two decimal places, so round our test result
        return Math.round(r * 100) / 100;
    }

    equal(roundCalc(-5), 0);
    equal(roundCalc(0), 0);
    equal(roundCalc(1), 0);
    equal(roundCalc(2), .02);
    equal(roundCalc(3), .04);
    equal(roundCalc(4), .1);
    equal(roundCalc(5), .1);
    equal(roundCalc(6), .2);
    equal(roundCalc(7), .34);
    equal(roundCalc(7.5), .5);
    equal(roundCalc(8), .66);
    equal(roundCalc(9), .8);
    equal(roundCalc(10), .9);
    equal(roundCalc(11), .9);
    equal(roundCalc(12), .98);
    equal(roundCalc(13), .98);
    equal(roundCalc(14), .99);
    equal(roundCalc(15), 1);
    equal(roundCalc(16), 1);
    equal(roundCalc(17), 1);
    equal(roundCalc(18), 1);
    equal(roundCalc(19), 1);
    equal(roundCalc(20), 1);
    equal(roundCalc(25), 1);
});

