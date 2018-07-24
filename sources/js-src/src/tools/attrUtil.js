export default {
        attrInfo : function(info){
            var infoArr = info && info.split(":");
            return {type:infoArr[0]||"", valstr:infoArr[1]||""};
        },
        inputVal : function($this,type){
            var handler = function (str) {
                    return /undefined|null/.test(str) ? "" : str;
                };
            switch (type) {
                case 'val': 
                    return handInput($this);
                case 'value':
                case 'file': 
                    return handler($this.attr("value"));
                case 'text': 
                    return handler($this.text());
                default : 
                    return handler($this.attr(type));
            }
    
            function handInput($this){
                var val = $this.val();
                $this.attr("value",val);
                return val;
            }
           
        },
        attrInfoAndVal : function($this,attr){
            var info = this.attrInfo($this.attr(attr));
            return $.extend(info,{val:this.inputVal($this,info.type)});
        }
    };