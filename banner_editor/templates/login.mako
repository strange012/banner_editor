<%inherit file="home.mako"/>
<%namespace name="util" file="util.mako"/>

<div class="container border mt-3">
    <form class="m-4" action=${request.route_path('login')} method="post" id="form_login">
        ${renderer.csrf_token()}
        <div class="form-row">
            <div class="form-group col-md-6">
                <label for="login">Login:</label>
                ${renderer.text('login', class_='form-control', placeholder_='Login', required_=True)}
            </div>
            ${util.input_error(renderer, 'login')}
        </div>
        <div class="form-row">
            <div class="form-group col-md-6">
                <label for="password">Password:</label>
                ${renderer.password('password', class_='form-control', placeholder_='Password')}
            </div>
            ${util.input_error(renderer, 'password')}
        </div>
        <div class="form-row">
            <div class="form-check col">
                <button type="submit" class="btn btn-primary">Submit</button>
                <button class="btn btn-secondary" type="button" name="showpassword" id="showpassword" value="Show">Show</button> 
            </div>
        </div>
    </form>
</div>

<script>
    $("#showpassword").on('click', function(){	
        var pass = $("#password");
        var fieldtype = pass.attr('type');
        if (fieldtype == 'password') {
            pass.attr('type', 'text');
            $(this).text("Hide");
        }else{
            pass.attr('type', 'password');
            $(this).text("Show");
        }
    });
</script>