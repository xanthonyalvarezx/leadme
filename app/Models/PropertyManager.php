<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class PropertyManager extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'phone',
        'address',
        'website',
        'yellowpages_profile',
        'city',
        'type',
        'active'
    ];

    protected $casts = [
        'active' => 'boolean',
    ];
}
