<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

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
        $botResponse = 'Dummies response';

        return response()->json(
            [
                'botResponse' => $botResponse
            ]
        );
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
