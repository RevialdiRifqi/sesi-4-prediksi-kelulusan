<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Prediksi Kelulusan Tepat Waktu</title>
  <style>
    body{font-family:system-ui,sans-serif;max-width:560px;margin:2rem auto;padding:0 1rem;color:#222}
    label{display:block;margin-top:.8rem;font-weight:600;font-size:.9rem}
    input,select{width:100%;padding:.5rem;margin-top:.25rem;box-sizing:border-box}
    button{margin-top:1.2rem;padding:.7rem 1.2rem;background:#2563eb;color:#fff;border:0;border-radius:6px;cursor:pointer}
    .hasil{margin-top:1.5rem;padding:1rem;border-radius:8px;background:#f1f5f9}
    .RENDAH{border-left:6px solid #16a34a}.SEDANG{border-left:6px solid #f59e0b}.TINGGI{border-left:6px solid #dc2626}
    .err{color:#b91c1c;font-size:.85rem}
  </style>
</head>
<body>
  <h1>Prediksi Kelulusan Tepat Waktu</h1>
  <p>Masukkan data akademik. Data tidak disimpan.</p>

  @foreach ($errors->all() as $e)<p class="err">{{ $e }}</p>@endforeach

  <form method="POST" action="{{ route('prediksi') }}">
    @csrf
    @foreach ([
      'ipk' => 'IPK (0-4)', 'rata_ips_3_semester' => 'Rata-rata IPS 3 semester terakhir',
      'sks_lulus' => 'SKS yang sudah lulus', 'persen_kehadiran' => 'Kehadiran (%)',
      'jumlah_mk_mengulang' => 'Jumlah MK mengulang'] as $name => $label)
      <label>{{ $label }}
        <input type="number" step="any" name="{{ $name }}" value="{{ old($name) }}" required>
      </label>
    @endforeach
    @foreach (['pernah_cuti' => 'Pernah cuti akademik?', 'kerja_paruh_waktu' => 'Bekerja paruh waktu?', 'aktif_organisasi' => 'Aktif organisasi?'] as $name => $label)
      <label>{{ $label }}
        <select name="{{ $name }}"><option value="0">Tidak</option><option value="1" @selected(old($name)==='1')>Ya</option></select>
      </label>
    @endforeach
    <button type="submit">Prediksi</button>
  </form>

  @if ($hasil)
    <div class="hasil {{ $hasil['risiko'] }}">
      <strong>Risiko keterlambatan: {{ $hasil['risiko'] }}</strong><br>
      Peluang lulus tepat waktu: {{ number_format($hasil['peluang_tepat_waktu'] * 100, 1) }}%<br>
      Estimasi lama studi: ±{{ $hasil['estimasi_lama_studi_semester'] }} semester
    </div>
  @endif
</body>
</html>
