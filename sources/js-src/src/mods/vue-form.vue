<template>
    <div class="editForm">
        <div style="position: relative;" v-for="(form,index) in forms" :key="form.id">
            <div>
                <div v-if="order && forms.length>1" style="text-align:center;padding:1em;">{{'（'+(index+1)+'）'}}</div>
                <div class="form-utils">
                    <div class="form-util add" title="添加" @click="addForm(index+1)"><i class="fa fa-plus-square"></i></div>
                    <div class="form-util del" title="删除" @click="delForm(index)"><i class="fa fa-minus-square"></i></div>
                </div>
                <slot name="form" :index="index+1"></slot>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props:{
        order:{
            type:Boolean,
            default:true
        },

    },
    data:function(){
        return {
            forms : []
        }
    },
    methods:{
        newForm:function(){
            return {id:newID}
        },
        addForm:function(i){
            this.forms.splice(i,0,this.newForm());
        },
        delForm:function(i){
            if(this.forms.length == 1){
                layer.msg('至少保留一行！');
            }else if(confirm("确定删除吗？")){
                this.forms.splice(i,1);
            }
        },
        clearList:function(){
            this.forms = [];
        },
        renderTpl:function(num){
            for(var i=0;i<num;i++)this.addForm(num);
        }
    },
    created:function(){
        this.addForm(0);
    },
    mounted:function(){
        this.$root.storeChildVm(this,"forms");
    }
}
</script>
<style lang="scss">
.form-utils .form-util{
    position: absolute;
    top:48%;

    &.add{
        left:-30px;
    }
    &.del{
        right:-30px;
    } 
 }
</style>


