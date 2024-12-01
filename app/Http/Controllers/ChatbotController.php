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

        $accesToken = $request->session()->get('accesToken');
        $refreshToken = $request->session()->get('refreshToken');

        $response = Http::withToken($accesToken)->post('http://fastapi:8001/chat', [
            'message' => $message
        ]);

        if ($response->status() == 401) {
            $refresh_response = Http::post('http://laravel:8000/refresh-token', [
                'refreshToken' => $refreshToken
            ]);

            if ($refresh_response->status() == 200) {
                $newAccesToken = $refresh_response->json('accesToken');
                $request->session()->put('accesToken', $newAccesToken);

                $response = Http::withToken($newAccesToken)->post('http://fastapi:8001/chat', [
                    'message' => $message
                ]);
            } else {
                return redirect()->route('google.logout')->with('error', 'Session expired, please log in again.');
            }
        }

        return response()->json([
            'botResponse' => $response->json('botResponse')
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
