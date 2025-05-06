<?php

use Slim\Factory\AppFactory;
use Slim\Views\Twig;
use Slim\Views\TwigMiddleware;

use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;

// Carga librerías de composer
require __DIR__ . '/../vendor/autoload.php';

// Cargar archivo .env
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . '/../');
$dotenv->load();

// Inicia la app
$app = AppFactory::create();

// 1) Ruta para servir assets estáticos (antes de CORS/Auth)
$app->get('/assets/{path:.*}', function (Request $request, Response $response, array $args) {
    $file = __DIR__ . '/assets/' . $args['path'];
    if (!file_exists($file) || !is_readable($file)) {
        return $response->withStatus(404);
    }
    $stream = new \Slim\Psr7\Stream(fopen($file, 'rb'));
    $mimeType = mime_content_type($file) ?: 'application/octet-stream';
    return $response
        ->withBody($stream)
        ->withHeader('Content-Type', $mimeType);
});

// Middleware para habilitar CORS
$allowedOrigins = [ $_ENV['BASE_URL'] ];

// 1) Middleware global de CORS
$app->add(function ($request, $handler) use ($allowedOrigins) {
    $response = $handler->handle($request);
    $origin = $request->getHeaderLine('Origin');
    if (in_array($origin, $allowedOrigins, true)) {
        $response = $response
            ->withHeader('Access-Control-Allow-Origin', $origin)
            ->withHeader('Vary', 'Origin')
            ->withHeader('Access-Control-Allow-Credentials', 'true')
            ->withHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
            ->withHeader('Access-Control-Allow-Headers', 'Authorization,Content-Type');
    }
    return $response;
});

// Preflight OPTIONS
$app->options('/{routes:.+}', function ($request, $response) use ($allowedOrigins) {
    $origin = $request->getHeaderLine('Origin');
    if (in_array($origin, $allowedOrigins, true)) {
        $response = $response
            ->withHeader('Access-Control-Allow-Origin', $origin)
            ->withHeader('Vary', 'Origin')
            ->withHeader('Access-Control-Allow-Credentials', 'true')
            ->withHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
            ->withHeader('Access-Control-Allow-Headers', 'Authorization,Content-Type');
    }
    return $response->withStatus(200);
});


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