<?php

namespace App\Middleware;

use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;

class AuthProxy
{
    public function __invoke(Request $request, $handler): Response
    {

        if ($request->getMethod() === 'OPTIONS') {
            $response = new \Slim\Psr7\Response();
            return $response
                ->withHeader('Access-Control-Allow-Origin', 'http://127.0.0.1:5000')
                ->withHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
                ->withHeader('Access-Control-Allow-Headers', 'Authorization, Content-Type, X-Requested-With')
                ->withHeader('Access-Control-Allow-Credentials', 'true')
                ->withStatus(200);
        }

        $authHeader = $request->getHeaderLine('Authorization');
        if (!$authHeader) {
            $response = new \Slim\Psr7\Response();
            $response->getBody()->write(json_encode(['error' => 'Authorization header missing']));
            return $response
                ->withHeader('Content-Type', 'application/json')
                ->withStatus(401);
        }

        $client = new Client(['base_uri' => $_ENV['BASE_URL']]);

        try {
            // Validar el token con Flask
            $validateResponse = $client->get('/api/protected', [
                'headers' => ['Authorization' => $authHeader]
            ]);

            if ($validateResponse->getStatusCode() === 200) {
                return $handler->handle($request);
            }
        } catch (RequestException $e) {
            // Manejar errores HTTP específicos
            if ($e->hasResponse()) {
                $statusCode = $e->getResponse()->getStatusCode();
                $message = $e->getResponse()->getReasonPhrase();
                throw new \Exception("Token validation failed: $message", $statusCode);
            }

            throw new \Exception('Token validation failed: ' . $e->getMessage(), 500);
        }

        // Intentar renovar el token si es necesario
        try {
            $refreshToken = $request->getHeaderLine('X-Refresh-Token');
            if (!$refreshToken) {
                throw new \Exception('Refresh token missing', 401);
            }

            $refreshResponse = $client->post('/api/refresh-token', [
                'headers' => ['Authorization' => $authHeader],
                'json' => ['refresh_token' => $refreshToken]
            ]);

            if ($refreshResponse->getStatusCode() === 200) {
                $newToken = json_decode($refreshResponse->getBody(), true)['token'];
                $request = $request->withHeader('Authorization', 'Bearer ' . $newToken);
                return $handler->handle($request);
            }
        } catch (RequestException $refreshException) {
            if ($refreshException->hasResponse()) {
                $statusCode = $refreshException->getResponse()->getStatusCode();
                $message = $refreshException->getResponse()->getReasonPhrase();
                throw new \Exception("Failed to refresh token: $message", $statusCode);
            }

            throw new \Exception('Failed to refresh token: ' . $refreshException->getMessage(), 500);
        }

        throw new \Exception('Unknown error occurred', 500);
    }
}