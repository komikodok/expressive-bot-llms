<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Index\IndexController;

Route::get('/', [IndexController::class, 'index']);