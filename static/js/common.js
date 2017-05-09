/**
 * Created by Echo on 2017/5/2.
 */


function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function scrollup(){
    var e = $("#scrollUp");
    e.fadeOut(0);
    $(window).scroll(function(){  //只要窗口滚动,就触发下面代码
        var scrollt = document.documentElement.scrollTop + document.body.scrollTop; //获取滚动后的高度
        if( scrollt > 100 ){  //判断滚动后高度超过100px,就显示
            e.fadeIn(400); //淡出
        }else{
            e.stop().fadeOut(400); //如果返回或者没有超过,就淡入.必须加上stop()停止之前动画,否则会出现闪动
        }
    });
//    e.click(function(){ //当点击标签的时候,使用animate在300毫秒的时间内,滚到顶部
//        $("html,body").animate({scrollTop:"0px"},100);
//    });
}