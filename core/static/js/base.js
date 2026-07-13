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
