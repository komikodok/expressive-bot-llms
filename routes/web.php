<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\SocialiteController;
use App\Http\Controllers\Welcome\WelcomeController;

Route::get('/', [WelcomeController::class, 'index']);
Route::get('auth/google/redirect', [SocialiteController::class, 'redirect'])->middleware('guest');
Route::get('auth/google/callback', [SocialiteController::class, 'callback'])->middleware('guest');