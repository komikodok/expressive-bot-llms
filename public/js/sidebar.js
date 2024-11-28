const sideBar = document.getElementById('sideBar');
const sideBarButton = document.getElementById('sideBarButton');

sideBarButton.addEventListener('click', function() {
    sideBar.classList.toggle('max-md:-translate-x-full');
    sideBar.classList.toggle('max-md:translate-x-0');
});
