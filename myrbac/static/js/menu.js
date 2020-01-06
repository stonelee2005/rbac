$('.item .title').click(function () {
    // $(this).next().toggle('hide')
   $(this).next().removeClass('hide').parent().siblings().find('.body').addClass('hide');
});