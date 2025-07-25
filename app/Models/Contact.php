<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Contact extends Model
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
        'notes'
    ];

    protected $casts = [
        'notes' => 'string',
    ];
}
