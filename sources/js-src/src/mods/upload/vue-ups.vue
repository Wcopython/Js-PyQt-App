<template>
    <!-- @dragover.prevent="dragover" @dragleave.prevent="dragleave" @drop.prevent="addfile" -->
	<div :db-val="'value:'+dbVal+'.path'" :value="fulldir" class="label-upload">
		<div data-word='{"name":"file"}' class="up-item" v-for="(file,i) in files" :db-val="'file:'+dbVal+'.files.'+(i+1)" :value="file.name" :copy="getCopyInfo(file)" :key="file.id">
			<div :class="'upfile '+getFileClass(file.name)" data-word='{"name":"img"}' @dblclick="openLocalFile(file)" :word-src="file.toWord?file.src:null"></div>
			<p data-word='{"name":"title"}'>{{file.name}}</p>
			<i class="fa fa-minus-square up-del" title="删除" @click="delfile(file.id)"></i>
		</div>
		<label title="添加附件">
		+
		<div class="upload-btn" title="添加附件" @click="selectFiles"></div>
		</label>
		<!-- <div v-if="!files.length" class="up-placeholder">可拖拽附件到此处</div> -->
	</div>  
</template>
<script>
var layer = require("../layer/layer.js");

import "./upfiles.css";

function getAffix(filename){
    return filename.match(/\.(\w+)$/)[1] || "";
}

export default {
    props:['dbVal','dir','type'],
    data:function(){
        return {
            files : [],
            fulldir : "",
            // fulldir : "/"+this.dir,
            //需要添加到word中的文件类型
            toWordType:["png","jpg","bmp","jpeg"]
        }
    },
    methods:{
        newfile:function(name,local){
            return {
                id:newID,
                src:this.fulldir+'/'+name,
                name:name,
                local:local,
                toWord:this.toWordType.indexOf(getAffix(name))!=-1
            };
        },
        // dragover(e){
        //     this.$refs.panel.style = "box-shadow:0px 0px 1px 1px #42b983 inset";
        // },
        // dragleave(e){
        //     this.$refs.panel.style = "box-shadow: 0";
        // },
        openLocalFile:function(file){
            var loading = layer.load(),
                filePath = file.local||file.src,
                result = Python.file.open(filePath);
            !result && alert("打开出错，程序未保存该文件！")
            layer.close(loading);
        },
        selectFiles:function(){
            this.addfile(Python.file.select(this.type && this.type.split(",")));
        },
        getFilename:function(local){
            return local && local.split("/").reverse()[0];
        },
        getCopyInfo:function(file){
            return file.local && '{"local":"'+file.local+'","target":"'+file.src+'"}';
        },
        addfile:function(filePaths){
            var vm = this;
            filePaths.forEach(function(path){vm.files.push(vm.newfile(vm.getFilename(path),path))});

            // let vm = this,
            //     //拖拽时需判断是否为文件夹
            //     isfile = (file,callback)=>{
            //         var reader = new FileReader();
            //         reader.readAsBinaryString(file.slice(0,3));
            //         reader.onload=()=>callback(true,file);
            //         reader.onerror=()=>callback(false,file);
            //     };

            // Array.from(e.target.files||e.dataTransfer.files).forEach(file=>{
            //     isfile(file,function(result,file){
            //         !result?
            //             layer.msg('不支持拖拽文件夹！',{time:1500}):
            //             result && vm.files.push(vm.newfile(file.name));
            //     })
            // });
            // e.dataTransfer && e.dataTransfer.files && vm.dragleave(e);
        },
        delfile:function(delId){
            this.files.splice(this.files.findIndex(function(file){
                var equal = file.id == delId;
                //物理删除
                equal && !file.local && Python.file.del(file.src);
                return equal;
            }),1);
        },
        getFileClass:function(filename){
            return "up_"+getAffix(filename);
        },
        clearList:function(){
            this.files = [];
        },
        renderTpl:function(name){
            this.files.push(this.newfile(name,''));
        }
    },
    mounted:function(){
        this.$root.storeChildVm(this,"ups");
        this.fulldir = Apply.upfilesPath+"/"+this.dir;
    }
}
</script>
<style lang="scss">
/*------------上传组件样式--------------*/
.label-upload{
    width:100%;
    display:-webkit-flex;
    margin-bottom: -1px;
    height: 180px;
    border: 1px solid #efefef;
    -webkit-flex-wrap:wrap;
    overflow: auto;
    position: relative;

    label{
        position: relative;
        font-size: 36px;
        color:#9dacbb;
        height:60px;
        width:62px;
        line-height: 32px;
        cursor: pointer;
        padding:10px 15px;
        border-width: 1px;
        border-style: solid;
        border-radius: 2px;
        text-align: center;
        background-color: #fff;
        white-space: nowrap;
        border-color: #e6e6e6;
        margin: 15px 25px 0;
        margin-right: 0;

        &:hover{
            background: #efefef;
        }
    }

    .up-item{
        position: relative;
        text-align: center;
        width: 50px;
        height: 65px;
        margin: 15px 26px 0;
        margin-right: 0;
        display: inline-block;

        p{
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
            font-size:12px;
            margin:0;
            text-align: center;
        }

        .up-del{
            display: none;
            position: absolute;
            right: -12px;
            top: -8px;
            cursor:pointer;
        }

        &:hover .up-del{
            display:block;
        }
    }

    .upload-btn{
        opacity: 0;
        position: absolute;
        top:0;
        left:0;
        width:100%;
        height:100%;
    }
    
}

// .label-upload .up-placeholder{
//     font-size: 30px;
//     position: absolute;
//     left:35%;
//     top:35%;
//     color:#efefef;
// }

</style>

