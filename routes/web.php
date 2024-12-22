<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ChatbotController;
use App\Http\Controllers\SocialiteController;

Route::get('/', [ChatbotController::class, 'index'])->name('index');
Route::post('/', [ChatbotController::class, 'store'])->name('index.post');

Route::middleware('auth')->group(function () {
    Route::get('/{user_session_id}', [ChatbotController::class, 'chat'])->name('chat');
    Route::post('/new-chat', [ChatbotController::class, 'new_chat'])->name('new.chat');
    Route::get('/logout', [SocialiteController::class, 'logout'])->name('google.logout');
});

Route::middleware('guest')->group(function () {
    Route::get('/auth/google/redirect', [SocialiteController::class, 'redirect'])->name('google.redirect');
    Route::get('/auth/google/callback', [SocialiteController::class, 'callback'])->name('google.callback');
});
