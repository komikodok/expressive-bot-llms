<?php

namespace App\Http\Controllers;

use App\Models\User;
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

        $userFromDb = User::updateOrCreate(
            ['google_id' => $userFromGoogle->getId()],
            [
                'name' => $userFromGoogle->getName(),
                'email' => $userFromGoogle->getEmail()
            ]
        );

        auth('web')->login($userFromDb);
        session()->regenerate();

        return redirect()->route('index');
    }

    public function logout(Request $request) {
        auth('web')->logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        
        return redirect()->route('index');
    }
}
