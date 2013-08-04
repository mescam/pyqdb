<%inherit file="base.mako"/>
<%block name="asubmit">class="pure-menu-selected"</%block>
<%block name="content">
<h2>Add new quote:</h2>
<form class="pure-form pure-form-aligned" action="/submit" method="post">
    <fieldset>
        <div class="pure-control-group">
            <textarea name="quote" cols="120" rows="10"></textarea>
        </div>

        <button type="submit" class="pure-button pure-button-primary">Submit</button>

    </fieldset>
</form>
% if sent:
<strong>Thank you! Your comment has been added to our database and now awaits for moderation</strong>
% endif
</%block>
