$.getJSON("/js/lang.json", function(json){
  $('.translate').click(function(){
    let lang = $(this).attr('id');
    $('.lang').each(function(index, element){
      $(this).text(json[lang][$(this).attr('key')]);
    });
  });

});//Get json AJAX