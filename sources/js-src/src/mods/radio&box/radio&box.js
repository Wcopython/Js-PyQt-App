
import "./radio&box.scss"

export default {
    init(){
        $("body").on("click","label.radio",function(e){
            var $this = $(this),
                value = $this.attr("value"),
                $parent = $this.parents(".radios:eq(0)");
            //将选择项的值写到父项内
            $parent.attr("value", value).find(".radio").removeClass("checked");
            $this.addClass("checked");
        }).on("click","label.checkbox",function(e){
            var $this = $(this),
                $parents = $this.parents(".boxs"),
                $subBox = $this.siblings(".boxs");
    
            //勾选/取消当前复选框
            $this.toggleClass("checked",
                $subBox.length ? !!$subBox.find(".checked").length : !$this.hasClass("checked"));
    
            $parents.each(function (index, parent) {
                var $parent = $(this);
                //勾选/取消当前复选框的父复选框
                $parent.siblings(".checkbox").toggleClass("checked", !!$parent.find(".checked").length);
    
                //将所有勾选项的值写到父项内
                $parent.attr("value", $parent.find(".checked").filter(function () {
                    var $checked = $(this);
                    return !$.contains(parent, $checked.parents(".boxs:eq(0)")[0]);
                }).map(function () {
                    var $checked = $(this);
                    return $checked.attr("value");
                }).get().join(""));
            });
        });
    }
}