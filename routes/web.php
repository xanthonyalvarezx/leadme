<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\PageController;
use App\Http\Controllers\DashboardController;

Route::get('/', [PageController::class, 'landing']);


Route::group(['prefix' => 'auth'], function () {
    Route::get('/login', [AuthController::class, 'login'])->name('login');
    Route::get('/register', [AuthController::class, 'register'])->name('register');
    Route::post('/submitlogin', [AuthController::class, 'submitLogin'])->name('submit_login');
    Route::post('/submitregister', [AuthController::class, 'submitRegister'])->name('submit_register');
    Route::post('/logout', [AuthController::class, 'logout'])->name('logout');
});

Route::group(['prefix' => 'dashboard'], function () {
    Route::get('/', [PageController::class, 'home'])->name('dashboard.home')->middleware('auth');
    Route::get('/leads', [PageController::class, 'leads'])->name('dashboard.leads')->middleware('auth');
    Route::get('/contacts', [PageController::class, 'contacts'])->name('dashboard.contacts')->middleware('auth');
    Route::post('/saveContact', [DashboardController::class, 'saveContact'])->name('dashboard.saveContact')->middleware('auth');
    Route::get('/removeLead/{id}', [DashboardController::class, 'removeLead'])->name('dashboard.removeLead')->middleware('auth');
});
