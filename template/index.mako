<%inherit file="base.mako"/>
<%block name="ahome">class="pure-menu-selected"</%block>
<%block name="content">
<div class="pure-g">
    <div class="pure-u-1">
        <h2>Statistics</h2>
        <p>Approved quotes: ${approved1}</p>
        <p>Pending quotes: ${approved0}</p>
    </div>
</div>
</%block>
