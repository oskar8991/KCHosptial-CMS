$(document).on('click', '.hamburger', function() {
  $('.menubar')
    .removeClass('hamburger')
    .addClass('cross');
});

$(document).on('click', '.cross', function() {
  $('.menubar')
    .removeClass('cross')
    .addClass('hamburger');
});