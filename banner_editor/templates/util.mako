
<%def name="input_error(renderer, input)">
    % if renderer.is_error(input):
    <div class="form-group col-md-4">  
        <div class="alert alert-danger alert-dismissible show mt-2 fade" role="alert">
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
            ${'\n'.join(renderer.errors_for(input))}
        </div>
    </div>
    % endif
</%def>