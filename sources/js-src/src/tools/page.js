var num = 0,
    $chapters = {},
    chapterShow = function(chapter){
        $('.chapter').eq(chapter).show().siblings(".chapter").hide()
    };

export default {
    next:function(){
        $(window).scrollTop(0);
        chapterShow(++num);
        // dataUtil.save(num+1,function(){$(window).scrollTop(0);chapterShow(++num);});
    },
    last:function(){
        $(window).scrollTop(0);
        chapterShow(--num);
        // dataUtil.save(num+1,function(){$(window).scrollTop(0);chapterShow(--num);});
    },
    chapter:function(chapter){
        chapterShow(num = --chapter);
    },
    title:function(chapter){
        var toTitle = this.chapter;
        return title => {
            toTitle(chapter);
            $("#"+title)[0].scrollIntoView();
        }
    },
    init:function(){
        $('.chapter').eq(num).show();
    }
}

