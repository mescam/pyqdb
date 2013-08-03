<html>
<head>
    <title>pyqdb</title>
    <link rel="stylesheet" href="http://yui.yahooapis.com/pure/0.2.1/pure-min.css">
    <style>
    .content {
        margin-top: 60px;
        margin-left: 20px;
        margin-right: 20px;
        margin-bottom: 30px;
    }

    * {
        color: gray;
    }

    blockquote {
        background-color: rgb(250, 250, 250);
        padding: 20px 20px 20px 20px;
        border: 1px solid rgb(238, 238, 238);
    }

    p.quote {
        margin-left: 40px;
    }
    </style>
</head>
<body>
    <div class="header">
        <div class="pure-menu pure-menu-open pure-menu-fixed pure-menu-horizontal">
            <a class="pure-menu-heading" href="">PyQDB</a>

            <ul>
                <li <%block name="ahome"></%block>><a href="/">Home</a></li>
                <li <%block name="alist"></%block>><a href="/list">New</a></li>
                <li <%block name="abest"></%block>><a href="/list/best">Best</a></li>
                <li <%block name="asubmit"></%block>><a href="/submit">Submit</a></li>
                <li <%block name="aadmin"></%block>><a href="/admin">Admin</a></li>
            </ul>
        </div>
    </div>


    <div class="content">
        <%block name="content">
        blabla
        </%block>
    </div>

</body>
</html>