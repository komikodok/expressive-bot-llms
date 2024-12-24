<?php

namespace App\Http\Controllers;

use App\Models\Message;
use App\Models\UserSession;
use Exception;
use Illuminate\Support\Str;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Http;

class ChatbotController extends Controller
{
    public function index(Request $request)
    {
        return view('index');
    }

    public function chat(Request $request, string $session_uuid)
    {   
        $user_id = $request->session()->get('user_id');

        
        if (!$session_uuid) {
            return redirect()->route('google.logout')->with('error', 'Session uuid is required.');
        }
        
        try {
            $user_session = UserSession::where('session_uuid', $session_uuid)
                ->where('user_id', $user_id)
                ->firstOrFail();
            } catch (Exception $e) {
                Log::info('Exception: ' . $e);
                return redirect()->route('index')->with('error', 'Session invalid.');
            }
            
            $list_session = UserSession::where('user_id', $user_id)->latest()->get(['session_uuid', 'updated_at']);
        $messages = $user_session->messages()->where('id', '>=', 2)->get();
        
        session(['session_uuid' => $session_uuid]);
        Log::info('Session uuid from chat: ' . $session_uuid);

        return view('chat', [
            'messages' => $messages,
            'list_session' => $list_session
        ]);
    }

    public function new_chat(Request $request)
    {
        $user_id = $request->session()->get('user_id');

        $user_session = UserSession::create([
            'session_uuid' => Str::uuid()->toString(),
            'user_id' => $user_id,
            'last_activity' => time()
        ]);

        if (!$user_session) {
            return redirect()->route('index')->with('error', 'Invalid session from new_chat.');
        }

        $session_uuid = $user_session->session_uuid;

        $request->session()->put('session_uuid', $session_uuid);
        Log::info('Session uuid from new_chat: ' . $session_uuid);

        return redirect()->route('chat', ['session_uuid' => $session_uuid]);
    }

    public function store(Request $request)
    {
        $message = $request->input('message', '');

        $access_token = $request->session()->get('access_token');
        $session_uuid = $request->session()->get('session_uuid');
        Log::info('Session uuid from store: ' . $session_uuid);

        try {
            $response = Http::withHeaders([
                'Authorization' => 'Bearer ' . $access_token,
                'Content-Type' => 'application/json'
            ])->post('http://localhost:8001/chat/' . $session_uuid, [
                'message' => $message
            ]);
        } catch (\Exception $e) {
            return response()->json(['error' => 'Bad request'], 400);
        }

        if ($response->status() == 401) {
            return redirect()->route('google.logout')->with('error', 'Session expired, please log in again.');
        }

        $user_session = UserSession::where('session_uuid', $session_uuid)->first();

        Message::create([
            'user_session_id' => $user_session->id,
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
}
