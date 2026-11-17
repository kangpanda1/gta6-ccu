# Notes

- Initial `makefun bundle --dry-run` could not run because `/data/home/gta6/entry/` did not exist. This is recorded; no session log has been provided by the runtime, so transcript/bundle eligibility remains unverified.
- Extracted kit contains practice inputs and starter code but no scorer entrypoint or practice scoring command. Practice comparison is performed locally with the published log-pinball formula.
- Model is deterministic and uses only case data and Python standard library; no network or model calls.

## Verifikasi akhir

Dua run pada empat kasus menghasilkan output byte-identik. Scorer dan jawaban practice tidak tersedia di kit lokal, sehingga perbandingan terhadap baseline belum bisa diverifikasi secara lokal.

- Uji dua-run selesai: `p00.out`–`p03.out` byte-identik antar `out1` dan `out2`; direktori sementara dihapus.
