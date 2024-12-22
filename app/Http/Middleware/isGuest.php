<?php

namespace App\Http\Middleware;

use Closure;
use App\Models\UserSession;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

class isGuest
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if (Auth::check()) {
            $user_id = $request->session()->get('user_id');

            if ($user_id) {
                $user_session = UserSession::where('user_id', $user_id)->latest('last_activity')->first();
                $session_uuid = $user_session->session_uuid;
    
                if (session()->has('access_token') && $session_uuid) {
                    return redirect()->route('chat', ['session_uuid' => $session_uuid]);
                }
            }
        }

        return $next($request);
    }
}
