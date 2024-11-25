const sideBar = document.getElementById('sideBar');
const sideBarButton = document.getElementById('sideBarButton');

sideBarButton.addEventListener('click', function() {
    if (sideBar.classList.contains('max-md:-translate-x-full')) {
        sideBar.classList.remove('max-md:-translate-x-full');
        sideBar.classList.add('max-md:translate-x-0');
    } else {
        sideBar.classList.add('max-md:-translate-x-full');
        sideBar.classList.remove('max-md:translate-x-0');
    };
});