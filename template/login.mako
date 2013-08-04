<%inherit file="base.mako"/>
<%block name="aadmin">class="pure-menu-selected"</%block>
<%block name="content">
<div class="pure-g">
    <div class="pure-u-1">
        <h2>Admin login</h2>
        <form class="pure-form pure-form-stacked" method="post">
        <fieldset>

        <input id="login" name="username" type="text" placeholder="Username">
        <input id="password" name="password" type="password" placeholder="Password">

        <button type="submit" class="pure-button pure-button-primary">Sign in</button>
    </fieldset>
</form>
    </div>
</div>
</%block>
