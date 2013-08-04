<%inherit file="base.mako"/>
<%!
from markupsafe import Markup
def nl2br(s):
    return s.replace("\n", Markup("<br />"))

import time
def int2time(s):
    return str(time.strftime("%d/%m/%Y",time.localtime(int(s))))

%>
<%block name="aadmin">class="pure-menu-selected"</%block>
<%block name="content">
<div class="pure-g">
    <div class="pure-u-3-4">
        <h2>Pending quotes</h2>
        % for quote in quotes:
<div class="pure-g" id="q${quote[0]}">
    <div class="pure-u-1"">
        <p class="quote">${quote[1]|int2time}
        <span>
        <a nohref onClick="approve(${quote[0]})">Approve</a>
        -
        <a nohref onClick="qdelete(${quote[0]})">Delete</a>
        </span>
        </p>
        <blockquote>${quote[2]|h,nl2br}</blockquote>
    </div>
</div>
% endfor
    </div>
    <div class="pure-u-1-4">
        <h2>Change password</h2>
        <p>Later...</p>
    </div>
</div>

<script>
function approve(id) {
    $.ajax({
        url: "/approve/"+id,
        context: document.body
    }).done(function(resp) {
        $("#q"+id).remove()
    });
}

function qdelete(id) {
    $.ajax({
        url: "/delete/"+id,
        context: document.body
    }).done(function(resp) {
        $("#q"+id).remove()
    });
}
</script>


</%block>
