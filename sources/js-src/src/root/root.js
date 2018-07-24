//组件ui
import vueHead from "../mods/vue-head.vue"
import vueTrs from "../mods/vue-trs.vue"
import vueUps from "../mods/upload/vue-ups.vue"
import vueFoot from "../mods/vue-foot.vue"
import vueSpan from "../mods/vue-span.vue"
import vueForm from "../mods/vue-form.vue"
import vueSelect from "../mods/vue-select.vue"

//css
import "./css/font-awesome.min.css";
import "./css/iconfont.css"
import "./css/root.scss";

export default {

    el:'#main',
    data:{
        //页面组件的模板实例
        tpls:[],
        // autoTable:{},
        toHide : null,
        mode:"",
        title:""
    },
    methods:{
        doToHide:function(){
            this.toHide && (this.toHide.show=false);
        },
        //存储子组件实例
        storeChildVm:function(childVm,type){
            var tplId = "tpl"+newID,
                $el = $(childVm.$el),
                newArg = {tplId:tplId,type:type},
                oldArg = $el.attr("editTpl");
                
                
            if(oldArg){
                newArg = $.extend(newArg,JSON.parse(oldArg));
            }
            
            this.tpls[tplId] = childVm;
            $el.attr("editTpl",JSON.stringify(newArg));
        }
    },
    components:{
        "vue-head":vueHead,
        "vue-tr":vueTrs,
        "vue-upload":vueUps,
        "vue-spans":vueSpan,
        "vue-foot":vueFoot,
        "vue-form":vueForm,
        "vue-select":vueSelect
    }
}
