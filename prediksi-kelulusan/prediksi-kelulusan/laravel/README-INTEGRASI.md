# Integrasi ke proyek Laravel

1. Buat proyek: `composer create-project laravel/laravel web`
2. Salin isi folder ini (`app/`, `resources/`, `routes/web.php`) ke dalam proyek `web/`.
3. Tambahkan di `config/services.php`:
   ```php
   'ml' => ['url' => env('ML_API_URL', 'http://127.0.0.1:5000')],
   ```
4. Tambahkan di `.env`: `ML_API_URL=http://127.0.0.1:5000`
5. Jalankan API Python (`python ml/api.py`) lalu `php artisan serve`, buka http://127.0.0.1:8000
