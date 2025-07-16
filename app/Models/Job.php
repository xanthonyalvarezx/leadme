<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Job extends Model
{
    protected $table = 'job';
    protected $fillable = ['link', 'title', 'details', 'posted_date'];

    public function getPostedDateAttribute($value) {}
}
