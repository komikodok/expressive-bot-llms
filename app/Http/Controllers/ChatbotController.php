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

        try {
            $response = Http::withHeaders([
                'Authorization' => 'Bearer ' . $access_token,
                'Content-Type' => 'application/json'
            ])->post('http://localhost:8001/chat', [
                'message' => $message
            ]);
        } catch (\Exception $e) {
            return response()->json(['error' => 'Bad request'], 400);
        }

        if ($response->status() == 401) {
            Log::info('Sending refresh token.....');
            $refresh_response = Http::timeout(120)->post('http://localhost:8000/refresh-token', [
                'refresh_token' => $refresh_token
            ]);
            Log::info('Refresh token: ', ['refresh_token' => $refresh_response->json('access_token')]);

            if ($refresh_response->status() == 200) {
                $new_access_token = $refresh_response->json('access_token');
                $request->session()->put('access_token', $new_access_token);

                $response = Http::withHeaders([
                    'Authorization' => 'Bearer ' . $new_access_token,
                    'Content-Type' => 'application/json'
                ])->post('http://localhost:8001/chat', [
                    'message' => $message
                ]);
            } else {
                return redirect()->route('google.logout')->with('error', 'Session expired, please log in again.');
            }
        }

        return response()->json([
            'generation' => $response->json('generation'),
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
