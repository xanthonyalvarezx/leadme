<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Models\PropertyManager;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::post('/property-managers', function (Request $request) {
    $data = $request->all();

    if (is_array($data) && isset($data[0])) {
        // Bulk insert with duplicate checking
        $saved = 0;
        $skipped = 0;

        foreach ($data as $item) {
            // Check if property manager with same name already exists
            $existing = PropertyManager::where('name', $item['name'])->first();

            if (!$existing) {
                PropertyManager::create($item);
                $saved++;
            } else {
                $skipped++;
            }
        }

        return response()->json([
            'message' => 'Property managers processed successfully',
            'saved' => $saved,
            'skipped' => $skipped,
            'total' => count($data)
        ]);
    } else {
        // Single insert with duplicate checking
        $existing = PropertyManager::where('name', $data['name'])->first();

        if (!$existing) {
            $propertyManager = PropertyManager::create($data);
            return response()->json([
                'message' => 'Property manager saved successfully',
                'id' => $propertyManager->id,
                'saved' => 1,
                'skipped' => 0
            ]);
        } else {
            return response()->json([
                'message' => 'Property manager already exists',
                'id' => $existing->id,
                'saved' => 0,
                'skipped' => 1
            ]);
        }
    }
});

Route::post('/property-managers/check', function (Request $request) {
    $name = $request->input('name');

    if (!$name) {
        return response()->json(['error' => 'Company name is required'], 400);
    }

    $exists = PropertyManager::where('name', $name)->exists();

    return response()->json([
        'exists' => $exists,
        'name' => $name
    ]);
});
