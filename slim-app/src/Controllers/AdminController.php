<?php

namespace App\Controllers;

use GuzzleHttp\Client;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Slim\Views\Twig;

class AdminController
{
    public function dashboard(Request $request, Response $response, $args): Response
    {
        try {
            $client = new Client(['base_uri' => $_ENV['BASE_URL']]);
            $authHeader = $request->getHeaderLine('Authorization');

            $flaskResponse = $client->get('/api/protected', [
                'headers' => [
                    'Authorization' => $authHeader
                ]
            ]);

            $data = json_decode($flaskResponse->getBody(), true);

            $view = Twig::fromRequest($request);
            return $view->render($response, 'admin-panel.twig', [
                'data' => json_encode($data, JSON_PRETTY_PRINT)
            ]);
        } catch (\Exception $e) {
            // Capturar cualquier excepción lanzada por el middleware o el controlador
            return $this->handleError($request, $response, $e);
        }
    }

    private function handleError(Request $request, Response $response, \Exception $e): Response
    {
        $statusCode = $e->getCode() ?: 500;
        $message = $e->getMessage();

        $view = Twig::fromRequest($request);
        return $view->render($response->withStatus($statusCode), 'error.twig', [
            'status_code' => $statusCode,
            'message' => $message
        ]);
    }

    public function listUsers(Request $request, Response $response, $args): Response
    {
        try {
            // Aquí iría la lógica para listar usuarios
            $response->getBody()->write("List of users goes here.");
            return $response;
        } catch (\Exception $e) {
            return $this->handleError($request, $response, $e);
        }
    }
}