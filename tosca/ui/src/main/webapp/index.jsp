<html>
<head>
    <script src="js/jquery-3.4.1.js"></script>

    <script type="text/javascript">

        function loadContent(selector){
            $("#loadOnClick").html($(selector).html());
        }
        function detectTOSCABugs () {
            $("#but_upload").click(function() {
                var fd = new FormData();
                var files = $('#file')[0].files[0];
                fd.append('file', files);
                // var filename = $('input[type=file]').val().split('\\').pop();
                // fd.append("name", filename);
                $.ajax({
                    url: 'http://localhost:8080/bug-predictor-api/v0.1/bugs/tosca/file',
                    type: 'post',
                    data: fd,
                    contentType: false,
                    processData: false,
                    dataType:"json",
                    success: function(response){
                        if(response !== 0){
                            alert(response)
                            alert(response.bugs);
                            alert(response.action_id)
                            $("#loadOnClick").html(response.action_id);
                        }
                        else{
                            alert('file not uploaded');
                        }
                    },
                });
            });
        }
    </script>
    <style>
        div.container11 {
            width: 100%;

        }
        section.container1{
            display: -webkit-flex; /* Safari */
            display: flex;
        }

        .displayInline{
            -webkit-flex: 1;  /* Safari 6.1+ */
            -ms-flex: 1;  /* IE 10 */
            flex: auto;
        }

        header, footer {
            padding: 1em;
            color: white;
            background-color: powderblue;
            clear: left;
            text-align: center;
        }

        nav {
            border-right: 2px solid gray;
        }

        nav ul {
            list-style-type: none;
            padding-top: 5px;
        }

        nav ul a {
            text-decoration: none;
            line-height: 30px;
        }

        div#loadOnClick {
            float: right;
        }

        .displayOnClick{
            display: none;
        }
    </style>
</head>
<body>

<div class="container">

    <header>
        <h1>SODALITE Defect Predictor</h1>
    </header>

    <section id="container1">
        <nav class="displayInLine" style="width: 20%; float: left;">
            <ul>
                <li><a href="#toscaSmell" class="quickLinks" onclick='loadContent("#toscaSmell")'>TOSCA Smells</a></li>
                <li><a href="#ansibleSmell" class="quickLinks" onclick='loadContent("#ansibleSmell")'>Ansible Smells</a></li>
            </ul>
        </nav>

        <div class="displayInLine" id="loadOnClick" style="width:75%; float: right;">

        </div>
    </section>

    <div id="toscaSmell" class="displayOnClick">
        <h1>TOSCA Smells</h1>
        <div align="center">
            <form method="post" action="" enctype="multipart/form-data" id="myform">
                <div >
                    <input type="file" id="file" name="file" />
                    <input type="button" class="button" value="Upload" id="but_upload" onclick="detectTOSCABugs()">
                </div>
            </form>
        </div>
    </div>
    <div id="ansibleSmell" class="displayOnClick">
        <h1>Ansible Smells</h1>
        <p> upload</p>
    </div>
    <footer>Copyright &copy; SODALITE</footer>
</div>

</body>
</html>