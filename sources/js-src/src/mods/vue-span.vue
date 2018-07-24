<template>
    <span class="spans">
        <span v-for="(s,i) in spans" :key="s.id">
            <span data-word='{"name":"atp"}' v-if="spans.length>1">{{'（'+(i+1)+'）'}}</span>
            <slot :index="i+1"></slot>
            <span class="span-del" title="删除" @click="delSpan(i)"><i class="fa fa-minus-square"></i></span>
        </span>
        <span class="span-add" title="添加" @click="addNewSpan"><i class="fa fa-plus-square"></i></span>
    </span>
</template>
<script>
import layer from "./layer/layer.js";
export default {
    data:function(){
        return {
            spans:[]
        }
    },
    methods:{
        makeNewSpan:function(){
            return {id:newID};
        },
        addNewSpan:function(){
            this.spans.push(this.makeNewSpan())
        },
        delSpan:function(index){
            if(this.spans.length == 1){
                layer.msg('至少保留一行！');
            }else if(confirm("确定删除吗？")){
                //删除当前span
                this.spans.splice(index,1);
            }
        },
        clearList:function(){
            this.spans = [];
        },
        renderTpl:function(num){
            for(var i=0;i<num;i++)this.addNewSpan();
        }

    },
    created:function(){
        this.addNewSpan();
    },
    mounted:function(){
        this.$root.storeChildVm(this,"spans");
    }
}
</script>
