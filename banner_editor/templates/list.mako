<%inherit file="home.mako"/>

<div class="ml-4 mr-4">
    <table class="table table-bordered table-hover">
        <thead class="thead-light">
            <tr>
                <th scope="col" class="text-center">#</th> 
                <th scope="col" class="text-center">Enabled</th>
                <th scope="col" class="text-center">Move</th>
                <th scope="col" class="text-center">Image</th>
                <th scope="col" class="text-center">Name</th>
                <th scope="col" class="text-center">Timestamp</th>
                <th scope="col" class="text-center">Edit</th>
                <th scope="col" class="text-center">Delete</th>
            </tr>
        </thead>
        <tbody>
            % for idx, banner in enumerate(sorted(banners, key=lambda x: x.pos)):
            <tr>
                <th scope="row"><p class="text-center">${idx + 1}</p></th>
                <td>
                    <div class="form-check text-center">
                        <input type="checkbox" class="form-check-input" name="include" ${"checked" if banner.enabled else ""} disabled="disabled">
                    </div>
                </td> 
                <td class="text-center">
                    <div class="btn-group-vertical">
                        <form method="post" action=${request.route_path('banner_move', id=banner.id)}>
                            <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
                            <input name="upwards" value="True" hidden>
                            <button class="btn btn-light">&#8593</button>
                        </form>
                        <form method="post" action=${request.route_path('banner_move', id=banner.id)}>
                            <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
                            <input name="upwards" value="False" hidden>
                            <button class="btn btn-light">&#8595</button>
                        </form>
                    </div>
                </td>
                <td class="text-center">
                    <img src=${banner.static_path("list_icon")} class="img-fluid" alt="icon" onerror="this.style.display='none'">
                </td>  
                <td>
                    <a href = ${banner.url}><p class="text-center">${banner.name}</p></a>
                </td>
                <td>
                    <p class="text-center">Created: ${banner.date_created.strftime('%H:%M %Y-%m-%d')}</span>
                    <p class="text-center">Edited: ${banner.date_edited.strftime('%H:%M %Y-%m-%d')}</span>
                </td>
                <td>
                    <p class="text-center"><a href= ${request.route_path('banner_edit', id=banner.id)} class="btn btn-light">&#9998</a></p>
                </td> 
                <td>
                    <form method="post" action=${request.route_path('banner_delete', id=banner.id)}>
                        <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
                        <p class="text-center"><button type="submit" class="btn btn-light">&#128465</button></p>
                    </form>
                </td>
            <tr>
            % endfor
        </tbody>
    </table>
    <a href=${request.route_path('banner_add')} class="btn btn-primary">Add banner</a>
</div>
