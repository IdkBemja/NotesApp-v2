<?php
Route::prefix('admin')->middleware('jwt.auth')->group(function () {
    Route::get('/', [DashboardController::class, 'index'])->name('admin.dashboard');
    Route::resource('users', UserController::class);
    Route::resource('notes', NoteController::class);
});