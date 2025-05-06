<?php

use Slim\App;
use App\Controllers\AdminController;

return function (App $app) {
    $app->get('/admin/dashboard', [AdminController::class, 'dashboard']);
    $app->get('/admin/users', [AdminController::class, 'listUsers']);
};
