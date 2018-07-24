//js
import "./client.js";
import layer from "./layer/layer.js";

//css 
import "./login.css";

//回车事件
$("body").keydown(function(e){
    e.keyCode == "13" && login();
})

$(".log-btn").hover(function(){
    $(this).css("color","#3f5367");
},function(){
    $(this).css("color","#fff");
})

function login(btn){
    $(btn).css({"background":"#3f5367","color":"#fff"}).prop("disabled",true)
    setTimeout(function(){
        try{
            if(account.value && pwd.value){
                var result = Python.controller.login(account.value,pwd.value);
                if(result == "01"){
                    //跳转到主页面-登录成功        
                    frameElement.src = 'main.html';
                }else if(result == "02"){
                    layer.msg("登录失败，用户名或密码错误！")
                }else if(result == "03"){
                    layer.msg("登录异常！")
                }
            }else{
                layer.msg("请填写完整再登录！");
            }
        }catch(e){
            layer.msg(e.toString());
        }
        $(btn).css("background","#42a5f5").prop("disabled",false);
    },0)
    
}

window.util = {login}