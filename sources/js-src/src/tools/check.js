import attrUtil from "./attrUtil.js";

export default {
    //相关联处校验同一值
    related : {

        init : function(){
            $("[related]").each(function(){
                var $this = $(this),
                    info = attrUtil.attrInfo($this.attr("related"));
                $this.attr({"relatedWho":info.valstr,"relatedHow":info.type});
                $this.attr("oninput","util.checkUtil.related.syncInput(this,'"+info.valstr+"',util.$(this)."+info.type+"())");
            });
        },
        syncInput : function(_this,who,val){
            $("[relatedWho="+who+"]").each(function(){
                var how = $(this).attr("relatedHow");
                // 非本DOM节点
                if(!this.isEqualNode(_this)){
                    Function("o","o."+how+"('"+val+"')")($(this));
                }
            });
        }
    },
    pattern : {
        init : function(){
            $("[check]").blur(function(){
                var info = attrUtil.attrInfoAndVal($(this),"check");
                if(info.val){
                    var check = util.checkUtil.pattern[info.valstr](info.val);
                    $(this).toggleClass("input-error",!check.result);
                    if(!check.result){
                        alert(check.info);
                    }
                }
            });
           
        },
        isNum : function(input){
            return {result:/^\d+(\.\d+)?$/.test(input),info:"请输入正确的数字格式！"}
        },
        isEmail : function(input){
            return {
                result:/^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/.test(input),
                info:"请输入正确的电子邮箱格式！"
            }
        }
    },
    must : {
        allInput : function(){
            $("[must]").each(function(){
                var val = attrUtil.inputVal($(this),$(this).attr("must"));
                $(this).toggleClass("input-error",val.trim()=="");
            });
            return !$(".input-error").length;
       } 
    },
    init : function(){
        this.related.init();
        this.pattern.init();
    }
}