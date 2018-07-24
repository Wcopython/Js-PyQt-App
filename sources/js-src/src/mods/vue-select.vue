<template>
    <div class="select">
        <input type="text" @click.stop="toggleList()" :db-val="'val:'+dbVal" autocomplete="off" :value="inputVal" readonly="readonly" class="select-input">
        <span class="select-suffix" @click.stop="toggleList()">
            <i v-if="!show" class="fa fa-angle-down"></i>
            <i v-else class="fa fa-angle-up"></i>
        </span>
        <ul v-show="show" class="option-list">
            <li @click="chooseVal(option)" v-for="option in options">{{option}}</li>
        </ul>
    </div>   
</template>
<script>
export default {
    props:{
        options:Array,
        dbVal:String
    },
    data:function(){
        return {
            show : false,
            inputVal : "请选择"
        }
    },
    methods : {
        toggleList : function(){
            this.show = !this.show;
            this.$root.toHide = this;
            
        },
        chooseVal : function(option){
            this.inputVal = option;
            this.toggleList();
        }
    }
}
</script>
<style lang="scss">
.select{
    display: inline-block;
    border:1px solid #dcdfe6;
    width:8em;
    position:relative;
    cursor:pointer;

    .select-input{
        cursor:pointer;
        -webkit-appearance:none;
        outline: none;
        padding:0 15px 0 10px;
        line-height: 25px;
        border:none;
        width:100%;
        color:blue;
    }

    .select-suffix{
        position: absolute;
        height:100%;
        top:0;
        right:8px;
        text-align:center;
        color:#c0c4cc;
        line-height: 24px;
        font-size: 18px;
    }

    .option-list{
        color:blue;
        position: absolute;
        background: #fff;
        width:100%;
        list-style: none;
        border:1px solid #dcdfe6;
        margin: 3px 0;
        padding: 0;
        -webkit-transition:all .3s;
        z-index: 999;

        li{
            padding-left: 10px;
            height:32px;
            line-height: 32px;

            &:hover{
                background: #f2f2f2;
            }
        }
    }

}
</style>

