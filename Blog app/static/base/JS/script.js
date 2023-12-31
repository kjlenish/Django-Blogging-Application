$(document).ready(function() {
    $('.dropdown').hover(function() {
        $(this).find('.dropdown-menu').fadeIn('slow');
    }, function() {
        $(this).find('.dropdown-menu').fadeOut('slow');
    });
});

function refreshPage(){
    window.location.reload();
} 