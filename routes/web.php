<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\PageController;
use App\Http\Controllers\DashboardController;

Route::get('/', [PageController::class, 'landing']);


Route::group(['prefix' => 'auth'], function () {
    Route::get('/login', [AuthController::class, 'login'])->name('login');
    Route::get('/register', [AuthController::class, 'register'])->name('register');
});

Route::group(['prefix' => 'dashboard'], function () {
    Route::get('/', [PageController::class, 'home'])->name('dashboard.home');
    Route::get('/leads', [PageController::class, 'leads'])->name('dashboard.leads');
});
