<%inherit file="home.mako"/>

<div class="container">
    <div class="flexslider">
        <ul class="slides">
        % for banner in sorted((x for x in banners if x.enabled), key=lambda x: x.pos):
            <li>
                <a href=${banner.url}><img src=${banner.static_path("rotator_banner")}></a>
            </li>
        % endfor  
        </ul>
    </div>
</div>
    

   
