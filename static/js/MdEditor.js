var testEditor;
        $(function() {    
            // You can custom @link base url.
            
            testEditor = editormd("test-editormd", {
                width     : "90%",
                path : "{% static 'mdeditor/js/lib/' %}",
                height    : 720,
                toc       : true,

                // //atLink    : false,    // disable @link
                // //emailLink : false,    // disable email address auto link
                syncScrolling       : false,
                todoList  : true,
                // theme : "dark",
                // previewTheme : "dark",
                // editorTheme : "pastel-on-dark",
                // markdown : md,
                codeFold : true,
                // //syncScrolling : false,
                saveHTMLToTextarea : true,    // 保存 HTML 到 Textarea
                searchReplace : true,
                // //watch : false,                // 关闭实时预览
                // htmlDecode : "style,script,iframe|on*",            // 开启 HTML 标签解析，为了安全性，默认不开启    
                // //toolbar  : false,             //关闭工具栏
                // //previewCodeHighlight : false, // 关闭预览 HTML 的代码块高亮，默认开启
                emoji : true,
                taskList : true,
                tocm            : true,         // Using [TOCM]
                tex : true,                   // 开启科学公式TeX语言支持，默认关闭
                flowChart : true,             // 开启流程图支持，默认关闭
                sequenceDiagram : true,       // 开启时序/序列图支持，默认关闭,
            });

            
        });