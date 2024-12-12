<?php

namespace App\Http\Controllers;

use App\Models\User;
use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
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
            $user_from_google = Socialite::driver('google')->user();
        } catch (\Exception $e) {
            return redirect()->route('index')->with('error', 'Autenticated failed');
        }

        if (!$user_from_google || !$user_from_google->getEmail()) {
            return redirect()->route('index')->with('error', 'Invalid user');
        }

        $user_from_db = User::updateOrCreate(
            ['google_id' => $user_from_google->getId()],
            [
                'name' => $user_from_google->getName(),
                'email' => $user_from_google->getEmail()
            ]
        );

        auth('web')->login($user_from_db);
        session()->regenerate();

        $access_token = $this->generate_token($user_from_db, 30); // 30 minutes expired
        $refresh_token = $this->generate_token($user_from_db, 60 * 5); // 5 hours expired

        session([
            'access_token' => $access_token,
            'refresh_token' => $refresh_token
        ]);

        return redirect()->route('index');
    }

    public function logout(Request $request) 
    {
        auth('web')->logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        
        return redirect()->route('index');
    }

    public function generate_token($user, $minutes)
    {
        $payload = [
            'iss' => 'http://localhost:8000',
            'sub' => (string) $user->name,
            'iat' => time(),
            'exp' => time() + ($minutes * 60)
        ];
        return JWT::encode($payload, env('SECRET_KEY'), 'HS256');
    }

    public function refresh_token(Request $request)
    {
        $refresh_token = $request->input('refresh_token');
    
        try {
            $decoded = JWT::decode($refresh_token, new Key(env('SECRET_KEY'), 'HS256'));
            $user = User::find($decoded->sub);
    
            if (!$user) {
                return response()->json(['error' => 'Invalid token'], 401);
            }
    
            $new_access_token = $this->generate_token($user, 30); // 30 minutes expired
            return response()->json(['access_token' => $new_access_token]);
    
        } catch (\Exception $e) {
            return response()->json(['error' => 'Invalid or expired refresh token'], 401);
        }
    }
    
}
