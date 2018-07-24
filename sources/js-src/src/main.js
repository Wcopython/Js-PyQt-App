
//tools
import "./tools/client.js";
import "./tools/polyfill.js";
import dataUtil from "./tools/dataUtil.js";
import fileUtil from "./tools/fileUtil.js";
import page from "./tools/page.js";
import checkUtil from "./tools/check.js";
import Vue from "./tools/vue.js";

//引入组件
import layer from "./mods/layer/layer.js";
import laydate from "./mods/laydate/laydate.js";
import sidebarUtil from "./mods/sidebar/sidebar.js";
import radioBox from "./mods/radio&box/radio&box.js"

//引入根实例
import root from "./root/root.js"

//ID生成器，可用newID直接获取新ID
Object.defineProperty(window,'newID',{
    get:function(){return +String(Math.random()).substr(2, 8); }
});

//python调用
window.__allLoaded__ = function(apply){

    applyInit(apply);  //申请书信息初始化
    window.mainVue = new Vue(root);   //页面初始化
    mainVue.mode = Apply.mode || "apply";
    mainVue.title = Apply.applyTitle;  //申请书标题
 
    page.init();          //页面导航初始化
    sidebarUtil.init(".sidebar-menu");
    radioBox.init();    //单选.多选功能组件
    datePickerInit();     //日期组件初始化

    //回滚数据
    dataUtil.loadData(function(){
        //数据回滚之后
        infoTipInit();     //提示信息初始化
        checkUtil.init();    //检测功能初始化
        dataUtil.autoSave(180);    //自动保存，秒单位  180秒=3分钟
    });

}

function infoTipInit(){
    $("[info]").mouseenter(function(){
        this.layerId = layer.tips($(this).attr("info"), this, {
          tips: [1, '#3595CC'],
          time: 0
        }); 
    }).mouseleave(function(){
        layer.close(this.layerId);
    })
}

function datePickerInit(){
    $("span.date-ymd").each(function(){
        laydate.render({elem: this});//指定元素
    });
}

window.util = {page,fileUtil,sidebarUtil,dataUtil,checkUtil,$}


