<%inherit file="base.mako"/>
<%!
from markupsafe import Markup
def nl2br(s):
    return s.replace("\n", Markup("<br />"))

import time
def int2time(s):
    return str(time.strftime("%d/%m/%Y",time.localtime(int(s))))

%>

<%block name="alist">class="pure-menu-selected"</%block>
<%block name="content">
% for quote in quotes:
<div class="pure-g">
    <div class="pure-u-1">
        <p class="quote">${quote[1]|int2time} <a href="/voteup/${quote[0]}">+</a> / <a href="/votedown/${quote[0]}">-</a> (rating: ${quote[4]})</p>
        <blockquote>${quote[2]|h,nl2br}</blockquote>
    </div>
</div>
% endfor
</%block>
