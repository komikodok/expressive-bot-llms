<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ChatbotController;
use App\Http\Controllers\SocialiteController;

Route::get('/', [ChatbotController::class, 'index'])->name('index');
Route::get('auth/google/redirect', [SocialiteController::class, 'redirect'])->middleware('guest')->name('google.redirect');
Route::get('auth/google/callback', [SocialiteController::class, 'callback'])->middleware('guest')->name('google.callback');