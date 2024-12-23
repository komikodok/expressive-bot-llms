<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ChatbotController;
use App\Http\Controllers\SocialiteController;


Route::middleware('is_auth')->group(function () {
    Route::post('/', [ChatbotController::class, 'store'])->name('index.post');
    Route::get('/{session_uuid}', [ChatbotController::class, 'chat'])->name('chat');
    Route::post('/new-chat', [ChatbotController::class, 'new_chat'])->name('new.chat');
    Route::post('/logout', [SocialiteController::class, 'logout'])->name('google.logout');
});

Route::middleware('is_guest')->group(function () {
    Route::get('/', [ChatbotController::class, 'index'])->name('index');
    Route::get('/auth/google/redirect', [SocialiteController::class, 'redirect'])->name('google.redirect');
    Route::get('/auth/google/callback', [SocialiteController::class, 'callback'])->name('google.callback');
});
