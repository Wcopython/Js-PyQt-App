
    var py = window;

    //1.申请基本信息初始化
    window.applyInit = function(apply){
        apply = JSON.parse(apply);
        window.Apply = {
            applyId : apply.id,
            applyKey : apply.password,
            version : apply.version,
            applyLev : apply.apply_level,
            applyUnit : apply.company_name,
            applyType : apply.evalname,
            upfilesPath : apply.upfilesPath,  //上传文件目录
            applyTitle : apply.title,
            mode : apply.mode
        };
    }

    //2.与python通信接口
    window.Python = {
        //数据库接口
        db : {
            //返回单条记录对象
            get : function(sql,data){
                return this.find(sql,data)[0]
            },
            //返回多条记录对象
            find : function(sql){
                 return JSON.parse(py.db.find(Apply.applyKey,sql) || "[]")
            },
            //插入记录
            save : function(tb,data){
                return py.db.insert(Apply.applyKey,tb,JSON.stringify(data)||'');
            },
            //更新记录
            update : function(tb,data,where){
                return py.db.update(Apply.applyKey,tb,JSON.stringify(data)||'',where);
            },
            batchSave : function(data){
                return py.db.batchSave(Apply.applyKey,JSON.stringify(data)||'');
            },
            batchFind : function(data){
                return JSON.parse(py.db.batchFind(Apply.applyKey,JSON.stringify(data))||"{}");
            }
                
        },


        //文件操作接口
        file : {
            //复制文件
            copy : function(source,filename){
                return py.file.copy(source,filename);
            },
            del : function(filePath){
                return py.file.delFile(filePath);
            },
            //压缩文件
            zip : function(){
                return py.file.zip(Apply.applyId,Apply.applyKey);
            },
            select : function(filter){  //array
               //array
                if (Array.isArray(filter)) {
                    filter = filter.map(function (v) {
                        return '*.' + v;
                    }).join(" ");
                } else {
                    filter = filter || "*";
                }
                return JSON.parse(py.file.select(filter));
            },
            open : function(path){
                return py.file.open(path);
            },
            //导入数据包
            loadZip : function(){
                return py.file.loadZip(Apply.applyId,Apply.applyKey);
            }

        },

        //导出word接口
        doc: {
            export_word : function(html_code) {
                return py.doc.export_word(html_code);
            }
        },

        http : {         
            uploadZip : function(tbs){
                return py.java.upload_zip(tbs);
            }
        },

        controller : {
            login : function(account,pwd){
                return py.controller.login(account,pwd);
            },
            toHome(){
                return py.controller.home();
            }
        },
    };

    

