<?php
namespace App\Http\Middleware;

use Closure;
use Exception;
use Tymon\JWTAuth\Facades\JWTAuth;
use Tymon\JWTAuth\Exceptions\TokenExpiredException;
use Tymon\JWTAuth\Exceptions\TokenInvalidException;

class JwtMiddleware
{
    public function handle($request, Closure $next)
    {
        try {
            $user = JWTAuth::parseToken()->authenticate();
        } catch (Exception $e) {
            if ($e instanceof TokenInvalidException) {
                return response()->json(['message' => 'Token inválido'], 401);
            } elseif ($e instanceof TokenExpiredException) {
                return response()->json(['message' => 'Token expirado'], 401);
            } else {
                return response()->json(['message' => 'Token no encontrado'], 401);
            }
        }

        return $next($request);
    }
}