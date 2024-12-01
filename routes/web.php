<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ChatbotController;
use App\Http\Controllers\SocialiteController;

Route::get('/', [ChatbotController::class, 'index'])->name('index');
Route::post('/chat', [ChatbotController::class, 'store'])->name('index.post');

Route::post('refresh-token/', [SocialiteController::class, 'refreshToken'])->name('refresh-token');
Route::get('auth/google/redirect', [SocialiteController::class, 'redirect'])->middleware('guest')->name('google.redirect');
Route::get('auth/google/callback', [SocialiteController::class, 'callback'])->middleware('guest')->name('google.callback');
Route::get('logout', [SocialiteController::class, 'logout'])->middleware('auth')->name('google.logout');