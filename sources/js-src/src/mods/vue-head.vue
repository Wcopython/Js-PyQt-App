<template>
    <header id="header">
        <div class="place-left">
            <span>{{title}}</span>
        </div>
        <div v-if="mode=='apply'" class="place-right apply">
            <i title="保存数据" style="font-size:18px;margin-top: 1px;" @click="save" class="fa fa-save"></i> 
            <i title="导出doc" style="font-size:20px;vertical-align:text-bottom" @click="exportDoc" class="fa iconfont icon-daochu1"></i>
            <i title="导出数据包" style="font-size:16px;" @click="exportZip" class="fa iconfont icon-daochu"></i>
            <i title="导入数据包" @click="loadZip" class="fa iconfont icon-daoru"></i>
        </div>
        <div v-else class="place-right check">
            <i title="返回首页" style="font-size:20px;" @click="toHome" class="fa fa-home"></i>
            <i title="保存数据" style="font-size:18px;margin-top: 1px;" @click="save" class="fa fa-save"></i> 
            <i title="上传数据到服务器" @click="uploadZip" style="font-size:24px;vertical-align:text-bottom" class="fa fa-angle-double-up"></i>
            <i title="导出数据包" style="font-size:16px;" @click="exportZip" class="fa iconfont icon-daochu"></i>
            <i title="导出doc" style="font-size:20px;vertical-align:text-bottom" @click="exportDoc" class="fa iconfont icon-daochu1"></i>
        </div>
    </header>
</template>
<script>
import layer from "./layer/layer.js";
export default {
    props:["mode","title"],
    methods:{
        save(){
            util.dataUtil.save();
        },
        exportDoc(){
            util.fileUtil.export();
        },
        exportZip(){
            util.fileUtil.zip();
        },
        loadZip(){
            util.fileUtil.loadZip();
        },
        uploadZip(){
            var tbs = ["apply"];
            $("[db-table]").each(function(){
                tbs.push($(this).attr("db-table"));
            });
            var result = Python.http.uploadZip(JSON.stringify(tbs));
            layer.msg(result?"上传成功！":"上传异常！");
        },
        toHome(){
            Python.controller.toHome();
        }
    }
}
</script>
<style lang="scss">
#header{
    position: fixed;
    width:100%;
    top:0;
    background: #f2f2f2;
    height: 40px;
    z-index: 999;
    box-shadow: 0 0 2px rgba(0,0,0,0.25);
    transition: background-color 0.3s ease-in-out;
    display:-webkit-flex;
    -webkit-justify-content:  space-between;
    color:#8a8a8a;
    line-height: 40px;
    padding:0 3rem;

     .fa{
        cursor: pointer;line-height: 45px;
        &:hover{
            -webkit-transform: scale(1.2)
        }
    }

    .place-right{
        display:-webkit-flex;
        width:18%;
        -webkit-justify-content:space-between;

        &.check{
            width:23%;
        }
    }
}
</style>
