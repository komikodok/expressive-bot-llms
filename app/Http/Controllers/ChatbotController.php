<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ChatbotController extends Controller
{
    public function index()
    {
        return view('chatbot');
    }

    public function create()
    {
        
    }

    public function store(Request $request)
    {
        $message = $request->input('message', '');

        $acces_token = $request->session()->get('acces_token');
        $refresh_token = $request->session()->get('refresh_token');

        $response = Http::withToken($acces_token)->post('http://fastapi:8001/chat', [
            'message' => $message
        ]);

        if ($response->status() == 401) {
            $refresh_response = Http::post('http://laravel:8000/refresh-token', [
                'refresh_token' => $refresh_token
            ]);

            if ($refresh_response->status() == 200) {
                $new_acces_token = $refresh_response->json('acces_token');
                $request->session()->put('acces_token', $new_acces_token);

                $response = Http::withToken($new_acces_token)->post('http://fastapi:8001/chat', [
                    'message' => $message
                ]);
            } else {
                return redirect()->route('google.logout')->with('error', 'Session expired, please log in again.');
            }
        }

        return response()->json([
            'response' => $response->json('response'),
            'mood' => $response->json('mood')
        ]);
    }

    public function show(string $id)
    {
        
    }

    public function edit(string $id)
    {
        
    }

    public function update(Request $request, string $id)
    {
        
    }

    public function destroy(string $id)
    {
        
    }
}
