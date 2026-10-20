<?php

namespace App\Http\Controllers;

use App\Services\PredictionService;
use Illuminate\Http\Request;

class PredictionController extends Controller
{
    public function index()
    {
        return view('predict', ['hasil' => null]);
    }

    public function store(Request $request, PredictionService $service)
    {
        // Validasi di sisi Laravel (lapis pertama), Python memvalidasi lagi (lapis kedua)
        $data = $request->validate([
            'ipk'                 => 'required|numeric|between:0,4',
            'rata_ips_3_semester' => 'required|numeric|between:0,4',
            'sks_lulus'           => 'required|integer|between:0,160',
            'persen_kehadiran'    => 'required|numeric|between:0,100',
            'jumlah_mk_mengulang' => 'required|integer|between:0,30',
            'pernah_cuti'         => 'required|in:0,1',
            'kerja_paruh_waktu'   => 'required|in:0,1',
            'aktif_organisasi'    => 'required|in:0,1',
        ]);

        try {
            $hasil = $service->predict($data);
        } catch (\Throwable $e) {
            return back()->withInput()->withErrors(['api' => $e->getMessage()]);
        }

        // Privasi: hasil TIDAK disimpan ke database & tidak memuat identitas.
        return view('predict', ['hasil' => $hasil]);
    }
}
