<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Log;
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

        $access_token = $request->session()->get('access_token');
        $refresh_token = $request->session()->get('refresh_token');

        $response = Http::withToken($access_token)->post('http://localhost:8001/chat', [
            'message' => $message
        ]);

        if ($response->status() == 401) {
            $refresh_response = Http::post('http://localhost:8000/refresh-token', [
                'refresh_token' => $refresh_token
            ]);

            if ($refresh_response->status() == 200) {
                $new_access_token = $refresh_response->json('access_token');
                $request->session()->put('access_token', $new_access_token);

                $response = Http::withToken($new_access_token)->post('http://localhost:8001/chat', [
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
