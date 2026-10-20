<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;

/** Menghubungkan Laravel dengan API Python (model Random Forest). */
class PredictionService
{
    public function predict(array $data): array
    {
        $response = Http::timeout(10)
            ->post(config('services.ml.url') . '/predict', $data);

        if ($response->failed()) {
            throw new \RuntimeException($response->json('error') ?? 'Layanan prediksi tidak tersedia.');
        }
        return $response->json();
    }
}
