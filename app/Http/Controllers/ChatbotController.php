<?php

namespace App\Http\Controllers;

use App\Models\Message;
use App\Models\Session;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Http;

class ChatbotController extends Controller
{
    public function index()
    {
        return view('index');
    }

    public function chat(Request $request, ?string $session_id = null)
    {
        $user_id = $request->session()->get('user_id');
        $session = Session::where('id', $session_id)->where('user_id', $user_id)->first();

        if (!$session) {
            $session = Session::create([
                'id' => $session_id,
                'user_id' => $user_id,
                'last_activity' => time()
            ]);

            $request->session()->put('session_id', $session->id);
        }

        return view('chat'); // data = menyimpan message session query database
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
            ])->post('http://localhost:8001/chat/' . $session_id, [
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
            'message_history' => [
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
