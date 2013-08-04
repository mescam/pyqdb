<%inherit file="base.mako"/>
<%!
from markupsafe import Markup
def nl2br(s):
    return s.replace("\n", Markup("<br />"))

import time
def int2time(s):
    return str(time.strftime("%d/%m/%Y",time.localtime(int(s))))

%>

<%block name="alist">
% if mode == 'new':
class="pure-menu-selected"
% endif
</%block>

<%block name="abest">
% if mode == 'best':
class="pure-menu-selected"
% endif
</%block>

<%block name="content">
% for quote in quotes:
<div class="pure-g">
    <div class="pure-u-1">
        <p class="quote">${quote[1]|int2time}
        <span id="vote${quote[0]}">
        <a onClick="voteup(${quote[0]})" href="#">+</a> / <a href="#" onClick="votedown(${quote[0]})">-</a> (rate: ${quote[4]})
        </span>
        </p>
        <blockquote>${quote[2]|h,nl2br}</blockquote>
    </div>
</div>
% endfor


<script>
function voteup(id) {
    $.ajax({
        url: "/voteup/"+id,
        context: document.body
    }).done(function(resp) {
        $("#vote"+id).html(resp)
    });
}

function votedown(id) {
    $.ajax({
        url: "/votedown/"+id,
        context: document.body
    }).done(function(resp) {
        $("#vote"+id).html(resp)
    });
}
</script>
</%block>
