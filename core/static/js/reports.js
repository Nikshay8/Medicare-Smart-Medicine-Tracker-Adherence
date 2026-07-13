
(function () {
    'use strict';

    var CIRCUMFERENCE = 2 * Math.PI * 45; // r=45

    function drawDonut(svg) {
        var taken  = parseInt(svg.getAttribute('data-taken'),  10) || 0;
        var missed = parseInt(svg.getAttribute('data-missed'), 10) || 0;
        var total  = parseInt(svg.getAttribute('data-total'),  10) || 0;

        var takenPct  = total > 0 ? taken  / total : 0;
        var missedPct = total > 0 ? missed / total : 0;
        var adherePct = total > 0 ? Math.round(takenPct * 100) : 0;

        var takenLen  = takenPct  * CIRCUMFERENCE;
        var missedLen = missedPct * CIRCUMFERENCE;
        var takenOffset  = 0;
        var missedOffset = CIRCUMFERENCE - takenLen;

        var arcTaken  = svg.querySelector('.donut-taken');
        var arcMissed = svg.querySelector('.donut-missed');
        var pctText   = svg.querySelector('.donut-pct');

        if (arcTaken) {
            arcTaken.style.strokeDasharray  = takenLen + ' ' + (CIRCUMFERENCE - takenLen);
            arcTaken.style.strokeDashoffset = 0;
        }

        if (arcMissed) {
            if (missed > 0) {
                arcMissed.style.strokeDasharray  = missedLen + ' ' + (CIRCUMFERENCE - missedLen);
                arcMissed.style.strokeDashoffset = -takenLen;
            } else {
                arcMissed.style.strokeDasharray  = '0 ' + CIRCUMFERENCE;
                arcMissed.style.strokeDashoffset = 0;
            }
        }

        if (pctText) {
            pctText.textContent = adherePct + '%';
        }
    }

    function init() {
        var svgs = document.querySelectorAll('.donut-svg');
        for (var i = 0; i < svgs.length; i++) {
            drawDonut(svgs[i]);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
