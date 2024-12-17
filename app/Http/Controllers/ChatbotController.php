<?php

namespace App\Http\Controllers;

use App\Models\Message;
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
        $session_id = $request->session()->get('session_id');

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
            return redirect()->route('google.logout')->with('error', 'Session expired, please log in again.');
        }

        Message::create([
            'session_id' => $session_id,
            'metadata' => [
                ['role' => 'user', 'content' => $message],
                ['role' => 'assistant', 'content' => $response->json('generation')]
            ]
        ]);

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
