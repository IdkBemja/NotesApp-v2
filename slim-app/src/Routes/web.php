<?php

use Slim\App;

return function (App $app) {
    $app->get("/admin/adashboard", \App\Controllers\DashboardController::class . ":dashboard");
    $app->get('/admin/users', \App\Controllers\AdminController::class . ':listUsers');
};
