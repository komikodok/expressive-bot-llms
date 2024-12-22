<?php

namespace App\Models;

use App\Models\User;
use App\Models\Message;
use Illuminate\Support\Str;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class UserSession extends Model
{
    protected $table = 'user_sessions';
    protected $fillable = ['session_uuid', 'user_id', 'last_activity'];
    protected $with = 'messages';
    
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }

    public function messages(): HasMany
    {
        return $this->hasMany(Message::class, 'user_session_id');
    }
}
