<?php

namespace App\Http\Controllers;

use App\Models\User;
use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use App\Models\UserSession;
use Illuminate\Support\Str;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Laravel\Socialite\Facades\Socialite;

class SocialiteController extends Controller
{
    public function redirect() 
    {
        try {
            return Socialite::driver('google')->redirect();
        } catch (\Exception $e) {
            Log::error('Google OAuth Error: ' . $e->getMessage());
            return response()->json(['error' => 'Unable to authenticate with Google.'], 500);
        }
    }

    public function callback()
    {   
        try {
            $user_from_google = Socialite::driver('google')->user();
        } catch (\Exception $e) {
            Log::error("Google OAuth Error", [
                'message' => $e->getMessage(),
                'trace' => $e->getTraceAsString(),
                'request' => request()->all(),
                'session' => session()->all(),
            ]);
            return redirect()->route('index')->with('error', 'Authentication failed');
        }
        
        if (!$user_from_google || !$user_from_google->getEmail()) {
            Log::error("User: ", ['User_google' => $user_from_google]);
            return redirect()->route('index')->with('error', 'Invalid user');
        }

        $user_from_db = User::updateOrCreate(
            ['google_id' => $user_from_google->getId()],
            [
                'name' => $user_from_google->getName(),
                'email' => $user_from_google->getEmail()
            ]
        );

        $user_session = UserSession::where('user_id', $user_from_db->id)->latest('last_activity')->first();

        if (!$user_session) {
            Log::info('User session not found for user: ' . $user_from_db->id . ' Create new user');
            $user_session = UserSession::create([
                'session_uuid' => Str::uuid()->toString(),
                'user_id' => $user_from_db->id,
                'last_activity' => time()
            ]);
            Log::info('User session id from callback: ' . $user_session);
        }

        auth('web')->login($user_from_db);
        session()->regenerate();

        $access_token = $this->generate_token($user_from_db, 60 * 5); // 5 hours expired

        session([
            'access_token' => $access_token,
            'user_id' => $user_from_db->id
        ]);

        Log::info('Redirecting to chat with user_session_id: ' . $user_session->session_uuid);
        return redirect()->route('chat', ['session_uuid' => $user_session->session_uuid]);
    }

    public function logout(Request $request) 
    {
        auth('web')->logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        
        return redirect()->route('index')->with('error', session('error'));
    }

    public function generate_token($user, $minutes)
    {
        $payload = [
            'iss' => env('LARAVEL_URL'),
            'sub' => (string) $user->name,
            'iat' => time(),
            'exp' => time() + ($minutes * 60)
        ];
        return JWT::encode($payload, env('SECRET_KEY'), 'HS256');
    }
}
