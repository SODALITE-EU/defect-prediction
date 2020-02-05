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
                            var bugtable = "<h2>TOSCA Defects</h2>\n";
                            bugtable = bugtable+ "<table>\n" +
                                "  <tr>\n" +
                                "    <th>Defect Id</th>\n" +
                                "    <th>Defect Type</th>\n" +
                                "    <th>Location</th>\n" +
                                "    <th>Defect Description</th>\n" +
                                "  </tr>";
                            response.bugs.forEach(function(entry, index) {
                                bugtable = bugtable +"<tr>\n" +
                                    "    <td>"+ index +"</td>\n" +
                                    "    <td>"+entry.bug_name+"</td>\n" +
                                    "    <td>"+entry.element_type + " " + entry.element_name+ " in " + entry.context+"</td>\n" +
                                    "    <td>"+entry.description+"</td>\n" +
                                    "  </tr>";
                            });
                            bugtable = bugtable+ "</table>";
                            $("#loadOnClick").html(bugtable);
                        }
                        else{
                            alert('file not uploaded');
                        }
                    },
                });
            });
        }
        function detectAnsibleBugs () {
            $("#but_upload_ansible").click(function() {
                var fd = new FormData();
                var files = $('#file_ansible')[0].files[0];
                fd.append('file', files);
                // var filename = $('input[type=file]').val().split('\\').pop();
                // fd.append("name", filename);
                $.ajax({
                    url: 'http://35.188.199.162:5000/bugs/ansible/file',
                    type: 'post',
                    data: fd,
                    contentType: false,
                    processData: false,
                    dataType:"json",
                    success: function(response){
                        if(response !== 0){
                            var bugtable = "<h2>Ansible Defects</h2>\n";
                            bugtable = bugtable+ "<table>\n" +
                                "  <tr>\n" +
                                "    <th>Defect Id</th>\n" +
                                "    <th>Defect Type</th>\n" +
                                "    <th>Location</th>\n" +
                                "  </tr>";
                            response.bugs.forEach(function(entry, index) {
                                bugtable = bugtable +"<tr>\n" +
                                    "    <td>"+ index +"</td>\n" +
                                    "    <td>"+entry.bug_name+"</td>\n" +
                                    "    <td>"+entry.bug_info.uri+"</td>\n" +
                                    "  </tr>";
                            });
                            bugtable = bugtable+ "</table>";
                            $("#loadOnClick").html(bugtable);
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
        table {
            border-collapse: collapse;
            width: 100%;
            table-layout: fixed;
        }

        th, td {
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even){background-color: #f2f2f2}

        th {
            background-color: #4CAF50;
            color: white;
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
                <li><a href="#toscaSmell" class="quickLinks" onclick='loadContent("#toscaSmell")'>TOSCA Defects</a></li>
                <li><a href="#ansibleSmell" class="quickLinks" onclick='loadContent("#ansibleSmell")'>Ansible Defects</a></li>
            </ul>
        </nav>

        <div class="displayInLine" id="loadOnClick" style="width:75%; float: right;">

        </div>
    </section>

    <div id="toscaSmell" class="displayOnClick">
        <h1>Upload TOSCA Files</h1>
        <div align="center">
            <form method="post" action="" enctype="multipart/form-data" id="myform">
                <div style="background-color:lavender">
                    <table>
                        <tr>
                            <td><input type="file" id="file" name="file"/></td>
                            <td><input type="button" class="button" value="Upload" id="but_upload" onclick="detectTOSCABugs()"></td>
                        </tr>

                    </table>


                </div>
            </form>
        </div>
    </div>
    <div id="ansibleSmell" class="displayOnClick">
        <h1>Upload Ansible Files</h1>
        <div align="center">
            <form method="post" action="" enctype="multipart/form-data" id="myform2">
                <div style="background-color:lavender">
                    <table>
                        <tr>
                            <td><input type="file" id="file_ansible" name="file"/></td>
                            <td><input type="button" class="button" value="Upload" id="but_upload_ansible" onclick="detectAnsibleBugs()"></td>
                        </tr>

                    </table>

                </div>
            </form>
        </div>
    </div>
    <footer>Copyright &copy; SODALITE</footer>
</div>

</body>
</html>