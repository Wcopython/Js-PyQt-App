import Vue from "./vue.js";
import attrUtil from "./attrUtil.js";
import layer from "../mods/layer/layer.js";


//copyfile 是否复制文件
function _dbValue($field,copyfile) {
    var data = {};

    $field.find("[db-val]").each(function () {

        var valInfo = attrUtil.attrInfoAndVal($(this),"db-val");

        //转化为JSON数据
        makeJson(valInfo.valstr.split("."), valInfo.val.trim(), data);

        //复制文件 copy有值为新上传文件,否则为旧有文件
        if(copyfile && valInfo.type=="file"){
            var copy = $(this).attr("copy");
            copy && util.fileUtil.copy(JSON.parse(copy));
        }
    });

    return JSON.stringify(data);

    function makeJson(keys, value, o) {
        var makeKeys = function (i) {
                var attrs = '';
                for (var j = 0; j <= i; j++)
                    attrs += "['" + keys[j] + "']";
                return attrs;
            },
            exec = function (str) {
                return Function("o", str)(o);
            };

        for (var i = 0; i < keys.length; i++) {
            var attrs = makeKeys(i);
            if (i != keys.length - 1) {
                !exec("return o" + attrs) && exec("o" + attrs + " = {}");
            } else {
                // exec("o" + attrs + "?(o" + attrs + "+='," + value + "'):(o" + attrs + "='" + value + "')");
                exec("o" + attrs + "='" + value + "'");
            }
        }
    }

}

function _fillItemValue(field, _dbValue) {

    if(!_dbValue)return;

    $(field).find("[db-val]").each(function () {
        var $this = $(this),
            valInfo = attrUtil.attrInfo($this.attr("db-val")),
            itemVal = parseValTree(JSON.parse(_dbValue), valInfo.valstr),
            isSelect = $this.hasClass("radios") || $this.hasClass("boxs");

        (isSelect ? selectValue : fillValue)($this, itemVal, valInfo.type);

    });

    function fillValue($this, val, info) {
        val = function (_value) {
            return /null/.test(_value) ? "" : _value;
        }(val);
        switch (info) {
            case 'val': $this.val(val); break;
            case 'value': $this.attr("value", val); break;
            case 'text': $this.text(val); break;
        }
    }

    function selectValue($this, val) {
        var arrs = val.split("");
        for (var i = 0; i < arrs.length; i++) {
            $this.find("[value=" + arrs[i] + "]").click();
        }
    }
}

function parseValTree(value, keysStr) {
    try{
        var attrs = '', keys = keysStr.split(".");
        for (var j = 0; j < keys.length; j++)attrs += "['" + keys[j] + "']";
        return Function("o", "return o" + attrs + ";")(value);
    }catch(e){
        return "";
    }
}

//需要根据数据来调整HTML
function _dataMakeHtml(field,value,callback) {

    renderEach(field,getTplTypes(field),0);

    function getTplTypes(field){
        var arr = [];
        $(field).find("[editTpl]").each(function(){
            var type = JSON.parse($(this).attr("editTpl")).type;
            arr.indexOf(type) === -1 && arr[type=="forms"?"unshift":"push"](type);
        });
        return arr;
    }

    function renderEach(field,types,index){
        var type = types[index];
        if(type){
            $(field).find('[editTpl*='+type+']').each(function(){
                var valstr = $(this).attr("editTpl"),
                    info = JSON.parse(valstr);
                renderHtmlTpls(
                    type,
                    parseValTree(JSON.parse(value),info.value),
                    window.mainVue.tpls[info.tplId]
                );
            });
            Vue.nextTick(function(){
                renderEach(field,types,++index);
            });
        }else if(callback){
            callback(field,value);
        }
    }


    function renderHtmlTpls(type,db_value,curVue){
        if(db_value){
            //清空原有数据
            curVue.clearList();

            //渲染可扩展表单
            if(type == "forms"){
                curVue.renderTpl(Object.keys(db_value).length);

            //渲染可扩展span和tr
            }else if(type=="spans" || type=="trs"){
                curVue.renderTpl(Object.keys(db_value).length || 1);

            //渲染可扩展upload
            }else if(type == "ups"){
                var files = db_value.files;

                if(files){
                    Object.keys(files).forEach(function(key){
                        curVue.renderTpl(files[key])
                    });
                }
            }

        }  
    }
}


//回滚数据
function loadData(callback) {
    if(!Apply.applyId)return;
    var message = "",
        result = true,
        loading = layer.load();
    try{
        var tbNames = [],tbs = {};
        $("[db-table]").each(function(){
            var tbName = $(this).attr("db-table");
            tbNames.push(tbName);
            tbs[tbName] = this;
        });

        var results = Python.db.batchFind({apply_id:Apply.applyId,tables:tbNames});
       
        tbNames.forEach(function(tbName){
            $(tbs[tbName]).find("[db-field]").each(function(){
                var field = $(this).attr("db-field"),
                    fieldVal = results[tbName][field];
           
                fieldVal && _dataMakeHtml(this,fieldVal,_fillItemValue);
            });
        })
        
        message = "加载成功！";

    }catch(e){
        result = false;
        message = e.toString();
    }
    layer.close(loading);
    layer.msg(message,{time:2000},function(){
        callback && callback(result);
    });
};

//time 秒
function autoSave(time){
    //3分钟自动保存一次
    setInterval(util.dataUtil.save,time*1000);
}

//保存数据
function save(callback) {
    var loading = layer.load(),
        result = false,
        message = "";
    try{
        var db_data = {};
        $("[db-table]").each(function(){

            var db_table = $(this).attr("db-table");
            db_data[db_table] = {apply_id:Apply.applyId};

            $(this).find("[db-field]").each(function(){
                var db_field = $(this).attr("db-field");
                db_data[db_table][db_field] = _dbValue($(this),true);
            });
        });

        result = !!Python.db.batchSave(db_data);
        message = result?"数据已保存！":"数据保存异常！";

    }catch(e){
        message = e.toString();
    }

    layer.close(loading);
    layer.msg(message,{time:1000},function(){
        callback && callback(result);
    });
};

export default {loadData,save,autoSave}
