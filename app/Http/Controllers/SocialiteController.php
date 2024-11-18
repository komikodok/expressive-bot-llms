<?php

namespace App\Http\Controllers;

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
        return redirect('/');
    }
}
