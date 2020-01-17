<html>
<head>
    <script src="js/jquery-3.4.1.js"></script>

    <script type="text/javascript">

        function loadContent(selector){
            $("#loadOnClick").html($(selector).html());
        };


        $(document).ready(function(){

            loadContent("#userGuide");

        });
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
        <p> upload</p>
    </div>
    <div id="ansibleSmell" class="displayOnClick">
        <h1>Ansible Smells</h1>
        <p> upload</p>
    </div>
    <footer>Copyright &copy; SODALITE</footer>

</div>

</body>
</html>