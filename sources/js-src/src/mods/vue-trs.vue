<template>
    <tbody>
        <!--表格行-->
        <tr data-word='{"name":"tr"}' class="tr-edit" v-for="(tr,i) in trs" :key="tr.id">
            <td>
                <div @click="addNewTr(tr,i)" class="tr-util add-tr">
                    <i title="添加行" class="fa fa-plus-square"></i>
                </div>
                <div @click="delTr(tr,i)" class="tr-util del-tr">
                    <i title="删除行" class="fa fa-minus-square"></i>
                </div>
                <span data-word='{"name":"td"}' v-html="i+1"></span>
            </td>
            <template v-if="tr.useTpl">
                <slot :name="tr.tpl" :index="i+2">
                    <td data-word='{"name":"td"}' contenteditable v-for="j in tdsNum" :db-val="'text:'+dbVal+'.row'+(i+2)+'.col'+(j+1)"></td>
                </slot>
            </template>
            <template v-else>
                <td data-word='{"name":"td"}' contenteditable v-for="j in tdsNum" :db-val="'text:'+dbVal+'.row'+(i+2)+'.col'+(j+1)"></td>
            </template>
        </tr>
    </tbody>
</template>
<script>
import layer from "./layer/layer.js";

export default {
    props:{
        trsNum:{
            type:Number,
            default:1
        },
        tdsNum:{
            type:Number
        },
        tbName:{
            type:String
        },
        dbVal:{
            type:String
        }
    },
    data:function(){
        return {
            //表格新行，可编辑
            trs:[]
        }
    },
    methods:{
        //是否使用默认的模板数据
        makeNewTr:function(useTpl,tplRow){
            return {id:newID,useTpl:useTpl,tpl:tplRow};
        },
        //显示序号
        getIndex:function(tr){
           return this.trs.findIndex(function(_tr){return tr==_tr})+1;
        },
        delTr:function(tr,index){
           
            //只留一行时不删除
            if(this.trs.length == 1){
                layer.msg('至少保留一行！');
            }else if(confirm("确定删除吗？")){
                //删除当前行
                this.trs.splice(index,1);
            }
            
        },
        //向下插入新行 
        addNewTr:function(tr,index){
            this.trs.splice(index+1,0,this.makeNewTr(false));

        },
        clearList:function(){
            this.trs = [];
        },
        renderTpl:function(num){
            for(var i=0;i<num;i++)
                this.trs.push(this.makeNewTr(false));
        }
    },
    created:function(){
        var row = 2;
        for(var i=0; i<this.trsNum; i++){
            this.trs.push(this.makeNewTr(true,"row"+(row++)));
        }
    },
    mounted:function(){
        this.$root.storeChildVm(this,"trs");
    }
}
</script>
<style lang="scss">
.tr-edit .tr-util{
    position: absolute;
    &.add-tr{
        left:-30px;
    }
    &.del-tr{
        right:-26px;
    }
 }
 
//  .tr-edit .add-tr-panel{
//     position:absolute;
//     list-style:none;
//     margin:0;
//     background:#fff;
//     border: 1px solid #ddd;
//     padding:0;
//     z-index: 9999;
//  }
//  .tr-edit .add-tr-panel li{
//      padding: 7px 20px;
//  }
//  .tr-edit .add-tr-panel li:nth-of-type(2){
//     border-bottom:1px solid #ddd;
//  }
//  .tr-edit .add-tr-panel li:hover{
//      background: #0e90d2;
//      color:#fff;
//      cursor: default;
//  }

</style>

