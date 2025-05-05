<?php

use Slim\Factory\AppFactory;
use Slim\Views\Twig;
use Slim\Views\TwigMiddleware;

// Carga liberrías de composer
require __DIR__ . '/../vendor/autoload.php';

// Inicia la app
$app = AppFactory::create();

// Configurar Twig para vistas HTML
$twig = Twig::create(__DIR__ . '/../templates', ['cache' => false]);
$app->add(TwigMiddleware::create($app, $twig));

// Carga Rutas

// Carga sin ejecutarlo como función
require __DIR__ . '/../src/Middleware/AuthProxy.php';

// Carga requerida
(require __DIR__ . '/../src/Routes/web.php')($app);

// Middleware
$app->add(new \App\Middleware\AuthProxy());


// Ejecuta la app
$app->run();