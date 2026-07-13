/* Sidebar toggle */
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
    document.getElementById('sidebarOverlay').style.display =
        document.getElementById('sidebar').classList.contains('open') ? 'block' : 'none';
}
function closeSidebar() {
    document.getElementById('sidebar').classList.remove('open');
    document.getElementById('sidebarOverlay').style.display = 'none';
}

/* Profile dropdown */
function toggleProfileDropdown(e) {
    e.stopPropagation();
    var avatar   = document.getElementById('headerAvatar');
    var dropdown = document.getElementById('profileDropdown');
    var isOpen   = dropdown.classList.contains('open');
    dropdown.classList.toggle('open', !isOpen);
    avatar.classList.toggle('open', !isOpen);
}

/* Close dropdown when clicking anywhere else */
document.addEventListener('click', function(e) {
    var wrap = document.getElementById('avatarWrap');
    if (wrap && !wrap.contains(e.target)) {
        document.getElementById('profileDropdown').classList.remove('open');
        document.getElementById('headerAvatar').classList.remove('open');
    }
});


/* SVG icon strings*/
var ICONS = {
    check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    cross:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    clock:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    heart:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    warn:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    star:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    smile:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>',
    info:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
};


function parseTime(str) {
    var p = (str || '').trim().split(' ');
    if (p.length !== 2) return null;
    var t = p[0].split(':');
    if (t.length !== 2) return null;
    var h = parseInt(t[0], 10), m = parseInt(t[1], 10);
    var per = p[1].toUpperCase();
    if (per === 'PM' && h !== 12) h += 12;
    if (per === 'AM' && h === 12) h = 0;
    return h * 60 + m;
}

//Dose Reminder
function checkReminders() {
    if (!window.MEDICINE_DATA || !MEDICINE_DATA.length) return;
    var now = new Date();
    var cur = now.getHours() * 60 + now.getMinutes();
    MEDICINE_DATA.forEach(function(m) {
        var t = parseTime(m.time);
        if (t !== null && t === cur) {
            alert('Reminder: Time to take ' + m.name + '!');
        }
    });
}
checkReminders();
setInterval(checkReminders, 60000);

//Countdown for next dose
function updateCountdown() {
    if (!window.MEDICINE_DATA || !MEDICINE_DATA.length) return;

    var now     = new Date();
    var nowMins = now.getHours() * 60 + now.getMinutes();
    var best    = null, bestDelta = Infinity;

    MEDICINE_DATA.forEach(function(m) {
        var t = parseTime(m.time);
        if (t === null) return;
        var d = t - nowMins;
        if (d < 0) d += 1440;
        if (d < bestDelta) { bestDelta = d; best = m; }
    });

    var nameEl  = document.getElementById('cdName');
    var schedEl = document.getElementById('cdSched');
    var areaEl  = document.getElementById('cdTimerArea');
    var timerEl = document.getElementById('cdTimer');

    if (!best || !nameEl) return;

    nameEl.textContent  = best.name;
    schedEl.textContent = 'Scheduled at ' + best.time;

    if (bestDelta === 0) {
        areaEl.innerHTML =
            '<div class="cd-due-now">' +
            '<span class="pulse-dot"></span>Take it now!' +
            '</div>';
    } else {
        var h = Math.floor(bestDelta / 60);
        var m = bestDelta % 60;
        var txt = (h > 0 ? h + 'h ' : '') + m + 'm';
        if (timerEl) {
            timerEl.textContent = txt;
        } else {
            areaEl.innerHTML =
                '<div class="cd-timer-row">' +
                '<span class="cd-timer">' + txt + '</span>' +
                '<span class="cd-suffix">remaining</span>' +
                '</div>';
        }
    }
}

updateCountdown();
setInterval(updateCountdown, 30000);

//Dose Timeline
function buildTimeline() {
    var track = document.getElementById('timelineTrack');
    if (!track || !window.MEDICINE_DATA || !MEDICINE_DATA.length) return;

    var now     = new Date();
    var nowMins = now.getHours() * 60 + now.getMinutes();

    // Sort by scheduled time
    var sorted = MEDICINE_DATA.slice().sort(function(a, b) {
        return (parseTime(a.time) || 0) - (parseTime(b.time) || 0);
    });

    // Find first upcoming index
    var nextIdx = -1;
    sorted.forEach(function(m, i) {
        var t = parseTime(m.time);
        if (t !== null && t > nowMins && nextIdx === -1) nextIdx = i;
    });

    track.innerHTML = '';

    sorted.forEach(function(m, idx) {
        var t    = parseTime(m.time);
        var past = t !== null && t <= nowMins;
        var st   = (m.latestStatus || '').toLowerCase();

        var isTaken  = past && st === 'taken';
        var isMissed = past && st === 'missed';
        var isNext   = idx === nextIdx;
        var isUpcoming = !past && !isNext;

        // CSS class
        var cls = 'tl-item ';
        if (isTaken)  cls += 'tl-taken';
        else if (isMissed) cls += 'tl-missed';
        else if (isNext)   cls += 'tl-upcoming tl-next';
        else               cls += 'tl-upcoming';

        // Node icon
        var nodeIcon;
        if (isTaken)       nodeIcon = ICONS.check;
        else if (isMissed) nodeIcon = ICONS.cross;
        else if (isNext)   nodeIcon = ICONS.clock;
        else               nodeIcon = ICONS.clock;

        // Badge
        var badge;
        if (isTaken)       badge = 'Taken';
        else if (isMissed) badge = 'Missed';
        else if (isNext)   badge = 'Next';
        else               badge = 'Later';

        var el = document.createElement('div');
        el.className = cls;
        el.innerHTML =
            '<div class="tl-node">' + nodeIcon + '</div>' +
            '<div class="tl-meta">' +
                '<div class="tl-meta-name">' + m.name + '</div>' +
                '<div class="tl-meta-time">' + m.time + '</div>' +
                '<span class="tl-meta-badge">' + badge + '</span>' +
            '</div>';
        track.appendChild(el);
    });
}

buildTimeline();

//Banner - Motivation
function buildStreakBanner() {
    var banner  = document.getElementById('streakBanner');
    var iconWrap = document.getElementById('streakIconWrap');
    var titleEl = document.getElementById('streakTitle');
    var subEl   = document.getElementById('streakSub');

    if (!banner || !iconWrap) return;

    var total     = TAKEN_COUNT + MISSED_COUNT;
    var adherence = total > 0 ? Math.round((TAKEN_COUNT / total) * 100) : -1;
    var maxMissed = 0;

    if (window.MEDICINE_DATA) {
        MEDICINE_DATA.forEach(function(m) {
            if (m.missedStreak > maxMissed) maxMissed = m.missedStreak;
        });
    }

    var icon, title, sub, cls;

    if (!window.MEDICINE_DATA || MEDICINE_DATA.length === 0) {
        icon  = ICONS.info;
        title = 'Welcome to MediCare Companion';
        sub   = 'Add your first medicine to start tracking your doses.';
        cls   = 'sb-neutral';
    } else if (total === 0) {
        icon  = ICONS.info;
        title = 'Start your medication journey today';
        sub   = 'Mark your doses as Taken or Missed to track your progress.';
        cls   = 'sb-neutral';
    } else if (maxMissed >= 3) {
        icon  = ICONS.warn;
        title = 'You missed ' + maxMissed + ' doses in a row — time to get back on track';
        sub   = 'Your health depends on consistency. Take your next dose on time.';
        cls   = 'sb-warn';
    } else if (maxMissed === 2) {
        icon  = ICONS.warn;
        title = 'You missed 2 doses in a row — do not miss today';
        sub   = 'Consistency is key. Your caregiver may have been notified.';
        cls   = 'sb-warn';
    } else if (adherence === 100 && total >= 5) {
        icon  = ICONS.star;
        title = 'Perfect score — ' + total + ' doses logged, none missed';
        sub   = 'Outstanding consistency. Keep up the excellent work!';
        cls   = 'sb-great';
    } else if (adherence >= 80) {
        icon  = ICONS.smile;
        title = adherence + '% adherence — you are doing great';
        sub   = 'Stay consistent and your health outcomes will continue to improve.';
        cls   = 'sb-good';
    } else if (adherence >= 50) {
        icon  = ICONS.warn;
        title = 'Adherence at ' + adherence + '% — room to improve';
        sub   = 'Try to take every dose on time. Small steps make a big difference.';
        cls   = 'sb-warn';
    } else {
        icon  = ICONS.warn;
        title = 'Adherence is low at ' + adherence + '% — let\'s improve together';
        sub   = 'Set a daily reminder and ask your caregiver for support.';
        cls   = 'sb-warn';
    }

    banner.className  = 'streak-banner ' + cls;
    iconWrap.innerHTML = icon;
    titleEl.textContent = title;
    subEl.textContent   = sub;
    banner.style.display = 'flex';
}

buildStreakBanner();
