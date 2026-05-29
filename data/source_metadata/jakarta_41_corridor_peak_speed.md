# Jakarta 41 Corridor Peak-Hour Speed Dataset

## Source

- Title: Kecepatan Rata-rata di 41 (empat puluh satu) Koridor Jalan Utama pada Jam Sibuk
- Publisher/organization: Provinsi DKI Jakarta / Dinas Perhubungan
- Catalog URL: https://data.go.id/dataset/dataset/kecepatan-rata-rata-di-41-empat-puluh-satu-koridor-jalan-utama-pada-jam-sibuk
- Original source URL: https://satudata.jakarta.go.id/open-data/detail/kecepatan-rata-rata-di-41-empat-puluh-satu-koridor-jalan-utama-pada-jam-sibuk
- CSV URL: https://satudata.jakarta.go.id/backend/restapi/v1/datasets/export/fcf9fe69226f3e6ebcd4ad9b0b9a81dc/kecepatan-rata-rata-di-41-empat-puluh-satu-koridor-jalan-utama-pada-jam-sibuk.csv

## Catalog Metadata Observed

- Dataset ID: `f37b826d-639d-4b8a-8636-0e1d5557b6f8`
- Published: 02-12-2025
- Modified: 02-12-2025
- Description: average speed on main road corridors with travel direction,
  measured in kilometers per hour.
- Status: open catalog page.

## Local Files

- Raw CSV: `data/raw/jakarta_41_corridor_peak_speed.csv`
- Clean CSV: `data/processed/jakarta_corridor_peak_speed_clean.csv`
- Corridor ranking: `data/processed/jakarta_corridor_bottleneck_ranking.csv`
- Monthly summary: `data/processed/jakarta_corridor_monthly_speed_summary.csv`

## Initial Inspection

The downloaded CSV contains `576` rows for year `2023`, covering all 12 months.
Although the dataset title mentions 41 corridors, the `nama_jalan` field contains
48 unique corridor names in the downloaded file. This should be noted in any
analysis.
