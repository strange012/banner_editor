<%inherit file="home.mako"/>
<%namespace name="util" file="util.mako"/>

<div class="container border mt-3">
    <form class="m-4" action=${request.route_path('banner_add') if 'id' not in request.matchdict else request.route_path('banner_edit', id=request.matchdict['id'])} method="post" id="form_edit" enctype="multipart/form-data">
        ${renderer.csrf_token()}
        <div class="form-row">
            <div class="form-group col-md-6">
                <label for="name">Name:</label>
                ${renderer.text('name', class_='form-control', value_='banner')}
            </div>
            ${util.input_error(renderer, 'name')}
        </div>
        <div class="form-row">
            <div class="form-group col-md-6">
                <label for="url">URL:</label>
                ${renderer.text('url', class_='form-control', value_='https://wwww.google.com')}
            </div>
            ${util.input_error(renderer, 'url')}
        </div>
        <div class="form-row">
            <div class="form-group col-md-8">
                <label for="image">Image:</label>
                ${renderer.file('image', accept_='image/*', class_='form-control-file')}
                <img src="${path if path else '.'}" class="img-fluid" id="preview">
            </div>

            % if 'id' in request.matchdict:
            <div class="form-group col-md-4">
                <label for="pos">Position:</label>
                ${renderer.text('pos', type='number', step_=0.0000000001, class_='form-control')}
            </div>
            % endif
        </div>
        <div class="form-group">
            <div class="form-check">
                ${renderer.checkbox('enabled', class_='form-control-input', checked_=True)}
                <label class="form-check-label" for="enabled">
                    Is enabled
                </label>
            </div>
        </div>
        <button type="submit" class="btn btn-primary" value="submit">Submit</button>
    </form>
</div>

<script>
    function readURL(input) {
        if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $('#preview').attr('src', e.target.result);
                }
                reader.readAsDataURL(input.files[0]);
            }
        }
        $("#image").change(function(){
            readURL(this);
        });
</script>