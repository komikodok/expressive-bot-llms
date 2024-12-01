<?php

namespace App\Http\Controllers;

use App\Models\User;
use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use Illuminate\Http\Request;
use Laravel\Socialite\Facades\Socialite;

class SocialiteController extends Controller
{
    public function redirect() 
    {
        return Socialite::driver('google')->redirect();
    }

    public function callback()
    {   
        try {
            $userFromGoogle = Socialite::driver('google')->user();
        } catch (\Exception $e) {
            return redirect()->route('index')->with('error', 'Autenticated failed');
        }

        if (!$userFromGoogle || !$userFromGoogle->getEmail()) {
            return redirect()->route('index')->with('error', 'Invalid user');
        }

        $userFromDb = User::updateOrCreate(
            ['google_id' => $userFromGoogle->getId()],
            [
                'name' => $userFromGoogle->getName(),
                'email' => $userFromGoogle->getEmail()
            ]
        );

        auth('web')->login($userFromDb);
        session()->regenerate();

        $accesToken = $this->generateToken($userFromDb, 30); // 30 minutes expired
        $refreshToken = $this->generateToken($userFromDb, 60 * 5); // 5 hours expired

        return redirect()->route('index')->with([
            'acces_token' => $accesToken,
            'refresh_token' => $refreshToken
        ]);
    }

    public function logout(Request $request) 
    {
        auth('web')->logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        
        return redirect()->route('index');
    }

    public function generateToken($user, $minutes)
    {
        $payload = [
            'iss' => env('APP_URL'),
            'sub' => $user->name,
            'iat' => time(),
            'exp' => time() + ($minutes * 60)
        ];
        return JWT::encode($payload, env('JWT_SECRET'), 'HS256');
    }

    public function refreshToken(Request $request)
    {
        $refreshToken = $request->input('refresh_token');
    
        try {
            $decoded = JWT::decode($refreshToken, new Key(env('JWT_SECRET'), 'HS256'));
            $user = User::find($decoded->sub);
    
            if (!$user) {
                return response()->json(['error' => 'Invalid token'], 401);
            }
    
            $newAccessToken = $this->generateToken($user, 30); // 30 minutes expired
            return response()->json(['access_token' => $newAccessToken]);
    
        } catch (\Exception $e) {
            return response()->json(['error' => 'Invalid or expired refresh token'], 401);
        }
    }
    
}
