
import dataUtil from "./dataUtil.js";
import checkUtil from "./check.js";
import layer from "../mods/layer/layer.js";

export default {
    copy:function(copyInfo){
        return copyInfo && Python.file.copy(copyInfo.local, copyInfo.target);
    },
    export:function(callback) {
        if(confirm("确认导出doc文档？")){
            dataUtil.save(function() {
                layer.msg("开始导出word . . .", {time: 1500}, function() {
                    var result = Python.doc.export_word($("body").html());
                    if (result)alert(result === 'ok' ? "导出Word成功！" : result)
                });
            });
        }
    },
    zip:function() {
        if(Apply.mode=="apply" && !checkUtil.must.allInput()){
            alert("请将标记出的内容填写完整且格式正确！");
        }else{
            if(confirm("确认导出申请书数据包？")){
                dataUtil.save(function(){
                    var result = Python.file.zip();
                    if(result=="success"){
                        alert("导出数据包成功！");
                    }else if(result=="failed"){
                        alert("数据包导出格式异常,请勿使用！");
                    }
                });
            }
        }
    },
    loadZip:function(){
        if(confirm("导入的数据包将会覆盖本地数据，是否继续？")){
            var loading = layer.load(),
                result = Python.file.loadZip();
    
            this.checkUnzipResult(result,function(){
                history.go(0);
            })
            layer.close(loading);
        }
    },
    checkUnzipResult : function(result,callback){
        if(result=="success"){
            layer.msg("已解压数据包！");
            callback && callback();
        }else if(result=="failed"){
            alert("解压数据包异常！");
        }else if(result=="noEqual"){
            alert("数据包内容已纂改，导入错误！");
        }else if(result=="wrongPwd"){
            alert("获取项目解码密钥异常！")
        }
    }
};