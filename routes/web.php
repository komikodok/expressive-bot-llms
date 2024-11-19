<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\SocialiteController;
use App\Http\Controllers\Welcome\WelcomeController;

Route::get('/', [WelcomeController::class, 'index'])->name('index');
Route::get('auth/google/redirect', [SocialiteController::class, 'redirect'])->middleware('guest')->name('google.redirect');
Route::get('auth/google/callback', [SocialiteController::class, 'callback'])->middleware('guest')->name('google.callback');