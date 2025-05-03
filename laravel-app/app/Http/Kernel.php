<?php
protected $routeMiddleware = [
    'jwt.auth' => \App\Http\Middleware\JwtMiddleware::class,
];