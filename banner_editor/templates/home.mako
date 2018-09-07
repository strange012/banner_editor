<!DOCTYPE html>
<html lang="en">
	<head>
		<title>Banner Rotator</title>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="stylesheet" href="/static/modules/bootstrap.min.css">
		<link rel="stylesheet" href="/static/modules/flexslider.css">
		<script src="/static/modules/jquery-3.3.1.js"></script>
		<script src="/static/modules/bootstrap.min.js"></script>
		<script src="/static/modules/jquery.flexslider-min.js"></script>
		<script type="text/javascript" charset="utf-8">
			$(window).on('load', function() {
				$('.flexslider').flexslider({
					animation: "slide"
				});
			});
		</script>
	</head>

	<body>
		<nav class="navbar navbar-expand-sm bg-dark navbar-dark">
			<ul class="navbar-nav">
				<li class="nav-item">
					<a class="nav-link" href=${request.route_path('home')}>Home</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href=${request.route_path('admin')}>Admin</a>
				</li>
			</ul>
			<ul class="navbar-nav ml-auto">
				%if request.authenticated_userid:
				<li class="nav-item">
					<span class="nav-link text-success">${request.authenticated_userid}</span>
				</li>
				<li class="nav-item">
					<a class="nav-link" href=${request.route_path('logout')}>Logout</a>
				</li>
				% else:
				<li class="nav-item">
					<a class="nav-link" href=${request.route_path('login')}>Login</a>
				</li>
				% endif
			</ul>
		</nav>

		% if request.session.peek_flash():
			% for msg in request.session.pop_flash():
			<div class="alert alert-danger alert-dismissible show mt-2 fade" role="alert">
				<button type="button" class="close" data-dismiss="alert" aria-label="Close">
					<span aria-hidden="true">&times;</span>
				</button>
				${msg}
			</div>
			% endfor
		% endif

		${self.body()}

	</body>
	
</html>