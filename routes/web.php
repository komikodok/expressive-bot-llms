<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Welcome\WelcomeController;

Route::get('/', [WelcomeController::class, 'index']);