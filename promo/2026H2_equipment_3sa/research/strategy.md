# 3사 사업전략·재무 분석 팩 — Lam Research / Applied Materials / Tokyo Electron

> 용도: 「3사 기업분석·사업전략·기술분석집」의 사업전략·재무 파트 원자료. 직무 팁이 아니라 **에쿼티 리서치·전략 리포트** 관점으로 작성했습니다.
> 기준일: 2026-10-01. 작성 범위: 5개년 실적, 고객 집중도, 지역 믹스, 중장기 전략, 자본배분, 서비스 사업, WFE 시장, 한국 전략.
> 기존 팩(lam.md / amat.md / tel.md)의 2~3장과 겹치는 분기 실적·한국 법인 세부는 **요약만 하고 해당 팩을 참조**합니다. 이 문서는 "연간 추세"와 "3사 비교"에 집중합니다.

## 0. 읽기 전에: 표기 규칙과 한계

**태그**
- [확정]: 독립 출처 2곳 이상(예: SEC 공시 + 보도자료/전문 매체)
- [추정]: 출처 1곳 또는 2차 가공 수치
- [충돌]: 출처 간 수치가 다름. 양쪽을 모두 적음
- [해석]: 전략적 의미에 대한 분석. 사실 아님
- [계산]: 공개 수치로 직접 나눈 값(반올림)
- 확인 불가: 검색으로 찾지 못함. 수치를 만들어 넣지 않음

**수집 방법의 한계(중요)**
- WebFetch를 다시 시도했지만 sec.gov, macrotrends.net 모두 `EGRESS_BLOCKED`(네트워크 정책 차단)였습니다. 그래서 **모든 수치는 WebSearch 결과 요약을 거친 값**이고, 공시 원문 표를 직접 대조하지 못했습니다. 원문 링크는 그대로 적었으니 최종 원고 전에 핵심 숫자(특히 5개년 표)는 원문 대조를 권장합니다.
- 검색 요약기가 질의문에 넣은 숫자를 그대로 "확인"해 주는 경향이 있었습니다. 그래서 질의에 넣은 값과 다르게 돌아온 수치(예: Lam FY2021~22 영업이익률, TEL FY2025 매출 성장률)를 우선 채택했고, 질의값만 반복된 경우는 [추정]으로 낮췄습니다.

**회계연도(반드시 구분)**

| 회사 | 회계연도 종료 | "FY2026"이 뜻하는 기간 | 비고 |
|---|---|---|---|
| Lam Research | 6월 마지막 일요일 | 2025.7 ~ 2026.6 (2026-06-28 종료) | 10-K FY2026 제출 완료 |
| Applied Materials | 10월 마지막 일요일 | 2025.10 ~ 2026.10 (2026-10-25 전후 종료) | **FY2026은 아직 끝나지 않음.** Q1~Q3 실적 + Q4 가이던스만 있음 |
| Tokyo Electron | 3월 31일 | 2025.4 ~ 2026.3 | TEL은 FY 앞 숫자가 "종료 연도". FY2027 = 2026.4~2027.3(진행 중) |

- [해석] 같은 "FY2025"라도 Lam은 2024년 하반기~2025년 상반기, AMAT은 2024년 11월~2025년 10월, TEL은 2024년 4월~2025년 3월입니다. **업황 사이클의 위상이 최대 9개월 어긋납니다.** 3사 성장률을 같은 줄에 놓고 "누가 더 잘했다"를 말할 때는 이 차이를 반드시 각주로 달아야 합니다. 예를 들어 2023~24년 메모리 다운턴은 Lam FY2024(−14.5%)와 TEL FY2024(−17%)에 고스란히 들어가지만, AMAT FY2024는 성장(+2.5%)으로 나타납니다.

---

## 1. 5개년 실적 추세 (대략 FY2021~FY2026)

### 1-1. Lam Research (FY = 6월 결산, 단위: 10억 달러)

| FY | 매출 | YoY | GAAP GM | GAAP OPM | R&D | R&D/매출 [계산] | Systems | CSBG(고객지원 등) | CSBG 비중 [계산] |
|---|---|---|---|---|---|---|---|---|---|
| FY2021 | 14.63 | — | 46.5% | 30.6% [추정] | 1.493 | 10.2% | 9.76 | 4.86 | 33% |
| FY2022 | 17.23 | +18% | 45.7% | 31.2% [추정] | 1.604 | 9.3% | 11.32 | 5.90 | 34% |
| FY2023 | 17.43 | +1% | 44.6% | 29.7% | 1.727 | 9.9% | 10.70 | 6.73 | 39% |
| FY2024 | 14.91 | −14.5% | 47.3% [추정] | 28.6% | 1.902 | 12.8% | 8.92 | 5.98 | 40% |
| FY2025 | 18.44 | +23.7% | 48.7% | 32.0% | 2.096 | 11.4% | 11.49 | 6.94 | 38% |
| FY2026 | 23.23 | +26% | 약 50.5% [추정] | 35.3% | 2.376 | 10.2% | 14.89 | 8.35 | 36% |

- 태그: 매출·Systems/CSBG·R&D 금액은 [확정](10-K 각 연도 + stockanalysis/TradingView 요약 일치). FY2021~22 OPM은 질의값(30.3%/30.0%)과 다르게 돌아온 2차 집계(alphaquery) 값이라 [추정]. FY2026 GM 50.5%는 "48.7%에서 180bp 상승"이라는 요약 1건 [추정].
- 출처: 10-K FY2021 https://www.sec.gov/Archives/edgar/data/707549/000070754921000136/lrcx-20210627.htm · FY2022 https://www.sec.gov/Archives/edgar/data/707549/000070754922000107/lrcx-20220626.htm · FY2023 https://www.sec.gov/Archives/edgar/data/707549/000070754923000102/lrcx-20230625.htm · FY2024 https://www.sec.gov/Archives/edgar/data/707549/000070754924000106/lrcx-20240630.htm · FY2025 https://www.sec.gov/Archives/edgar/data/707549/000070754925000075/lrcx-20250629.htm · FY2026 https://www.sec.gov/Archives/edgar/data/0000707549/000070754926000037/lrcx-20260628.htm · 8-K Q4 FY2026 https://www.sec.gov/Archives/edgar/data/0000707549/000070754926000033/lrcx_exhibitx991xq4x2026.htm · TradingView FY2026 요약 https://es.tradingview.com/news/tradingview:c4d83c9b16623:0-lam-research-corp-fy-2026-revenue-23-23b-eps-5-76-10-k-summary/ · stockanalysis https://stockanalysis.com/stocks/lrcx/financials/ · alphaquery OPM https://www.alphaquery.com/stock/LRCX/fundamentals/annual/operating-profit-margin
- FY2026 R&D 증가 $279M, R&D 비중 11.4% → 10.2% [추정]: 10-K FY2026 검색 요약.
- 분기 최신(FQ4'26 매출 $6.72B, GM 51.7%, CSBG 약 $2.5B, FQ1'27 가이던스 $8.1B±0.4B, OPM 39.5%±1%p)은 lam.md 2-2 참조.

**Systems 매출의 응용처 믹스(Lam, % of systems revenue)**

| 기간 | Memory | Foundry | Logic/IDM·기타 | 태그 / 출처 |
|---|---|---|---|---|
| FY2022 | 60% | 26% | 14% | [추정] 10-K FY2024 표 요약 https://www.sec.gov/Archives/edgar/data/707549/000070754924000106/lrcx-20240630.htm , ycharts https://ycharts.com/indicators/lam_research_corp_lrcx_memory_revenue_total_systems_revenue |
| FY2023 | 42% | 38% | 20% | 위와 같음 |
| FY2024 | 42% | 40% | 18% | 위와 같음 |
| FY2025 연간 | 확인 불가 | 확인 불가 | 확인 불가 | — |
| FQ4'26(2026.4~6) | 46%(NAND 23% + DRAM 23%) | 44% | 10% | [확정] Investing.com 콜 트랜스크립트 https://www.investing.com/news/transcripts/earnings-call-transcript-lam-research-posts-record-q4-2026-results-stock-rebounds-93CH-4821978 , Yahoo 하이라이트 https://finance.yahoo.com/markets/stocks/articles/lam-research-corp-lrcx-q4-050153347.html |

- [해석] Lam은 전통적으로 "메모리(특히 NAND) 장비사"였지만 FY2022 60% → FY2024 42%로 메모리 의존을 크게 줄였습니다. 이는 전략적 다각화라기보다 **NAND 투자 붕괴(2023~24)의 결과**에 가깝습니다. 2026년 들어 NAND 매출이 분기 만에 2배가 되며 메모리 46%로 반등했습니다. Lam 실적은 여전히 **NAND 업그레이드 사이클의 레버리지**를 가장 크게 받는 구조입니다.

### 1-2. Applied Materials (FY = 10월 결산, 단위: 10억 달러)

| FY | 매출 | YoY [계산] | GAAP GM | GAAP OPM | RD&E | R&D/매출 [계산] | SSG(반도체 시스템) | AGS(서비스) | Display(→Other) |
|---|---|---|---|---|---|---|---|---|---|
| FY2021 | 23.06 | — | 47.3% | 29.9% | 2.485 | 10.8% | 16.29 (71%) | 5.01 (22%) | 1.63 (7%) |
| FY2022 | 25.79 | +12% | 46.5% | 30.2% | 2.771 | 10.7% | 18.80 (73%) | 5.54 (21%) | 1.33 (5%) |
| FY2023 | 26.52 | +3% | 46.7% | 28.9% | 3.102 | 11.7% | 19.70 (74%) | 5.73 (22%) | 0.87 (3%) |
| FY2024 | 27.18 | +2.5% | 47.5% | 28.9% | 3.233 | 11.9% | 19.91 (73%) | 6.23 (23%) | 0.885 (3%) |
| FY2025 | 28.37 | +4% | 48.7% | 29.2% | 3.570 | 12.6% | 20.80 (73%) | 6.39 (23%) | 약 1.06 [계산: FY24 × 1.20] |
| FY2026(진행 중) | Q1 7.01 + Q2 7.91 + Q3 9.12 = 24.04(9개월) / Q4 가이던스 10.25±0.5 포함 시 약 34.3 [계산] | 약 +21% [계산, 가이던스 기준] | Q3 비GAAP 50.4% | Q3 비GAAP 34% | 확인 불가 | — | Q3 약 7.0 | Q3 1.8(+22%) | Other로 보고 |

- 태그: FY2021~FY2025 매출·GM·OPM은 [확정](각 연도 8-K/IR 보도자료 + 10-K 검색 요약). RD&E FY2021~2025 [확정](10-K FY2022·FY2023·FY2025 + stockanalysis). 세그먼트 FY2021~23 [확정](8-K + stockanalysis), FY2024 AGS/Display [확정](8-K FY2024 + ARS), FY2025 [확정](amat.md 2-1·2-2와 일치).
- 출처: FY2021 8-K https://www.sec.gov/Archives/edgar/data/6951/000000695121000038/exhibit991q42021earningsre.htm · FY2022 8-K https://www.sec.gov/Archives/edgar/data/6951/000000695122000037/exhibit991q42022earningsre.htm · FY2023 8-K https://www.sec.gov/Archives/edgar/data/6951/000000695123000035/exhibit991q42023earningsre.htm · FY2024 8-K https://www.sec.gov/Archives/edgar/data/6951/000000695124000037/exhibit991q42024earningsre.htm · FY2025 IR https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-fourth-quarter-and-fiscal-year-2025/ · 10-K FY2025 https://www.sec.gov/Archives/edgar/data/6951/000162828025056742/amat-20251026.htm · 10-K FY2023 https://www.sec.gov/Archives/edgar/data/6951/000000695123000041/amat-20231029.htm · 세그먼트 https://stockanalysis.com/stocks/amat/metrics/revenue-by-segment/ · RD&E https://stockanalysis.com/stocks/amat/metrics/operating-expense-breakdown/ · FY2026 분기: amat.md 2-1(SEC 8-K Q1~Q3 FY26)
- Display 보고 변경: FY2026부터 Display는 별도 보고 세그먼트가 아니라 "Other"에 포함 [확정] (amat.md 2-2, 10-K FY2025).

**SSG(반도체 시스템) 응용처 믹스(AMAT)**

| FY | Foundry·Logic·기타 | DRAM | Flash(NAND) | 태그 / 출처 |
|---|---|---|---|---|
| FY2021 | 60% | 19% | 21% | [추정] 10-K FY2023 검색 요약 https://www.sec.gov/Archives/edgar/data/6951/000000695123000041/amat-20231029.htm |
| FY2022 | 66% | 19% | 15% | 위와 같음 |
| FY2023 | 77% | 17% | 6% | 위와 같음 |
| FY2024 | 68% | 28% | 4% | [추정] 10-K FY2025 검색 요약 https://www.sec.gov/Archives/edgar/data/6951/000162828025056742/amat-20251026.htm |
| FY2025 | 67% | 26% | 7% | 위와 같음 |
| FQ3'26 | 확인 불가(DRAM 26%만 확인) | 26% | — | [확정] amat.md 2-1(GlobeNewswire + SEC 8-K) |

- [해석] AMAT은 3사 중 **로직/파운드리 노출이 가장 큰 회사**입니다(FY2023 77%). 2023년 메모리 다운턴을 상대적으로 덜 맞은 이유가 여기 있습니다. 반대로 NAND는 4~7%까지 줄어 NAND 회복의 수혜는 Lam·TEL보다 작습니다. FY2024 DRAM 28%는 중국 DRAM 투자와 HBM 영향으로 보이나, 원인 분해는 확인 불가입니다.

### 1-3. Tokyo Electron (FY = 3월 결산, 단위: 10억 엔)

| FY(종료월) | 매출 | YoY [계산] | GM | OPM | R&D | R&D/매출 [계산] | Field Solutions(FS) | FS 비중 [계산] |
|---|---|---|---|---|---|---|---|---|
| FY2021(2021.3) | 1,399.1 | — | 40.4% [추정] | 22.9% [계산: 영업이익 320.7] | 136.6 [추정] | 9.8% | 확인 불가 | — |
| FY2022(2022.3) | 2,003.8 | +43% | 45.5% [추정] | 29.9% | 158.2 | 7.9% | 확인 불가 | — |
| FY2023(2023.3) | 2,209.0 | +10% | 44.6% [추정] | 28.0% [계산: 617.7] | 191.1~191.2 | 8.7% | 474.0 [추정] | 21% |
| FY2024(2024.3) | 1,830.5 | −17% | 45.4% [계산: FY25 47.1% − 1.7%p] | 24.9% | 202.9 | 11.1% | **[충돌]** 약 500 vs 약 428.6 | 23~27% |
| FY2025(2025.3) | 2,431.5 | **+32.8%** | 47.1%(사상 최고) | 28.7% | 250.0 | 10.3% | 538.3(+25.6%) | 22% |
| FY2026(2026.3) | 2,443.5 | +0.5% | 45.3% | 25.6% | 277.8(+11.1%) | 11.4% | 626.0(+16.3%) | 26% |
| Q1 FY2027(2026.4~6) | 732.3(분기 최대) | +33.3% | 46.8% | 28.9% | — | — | — | — |

- 태그: 매출·OPM FY2022~FY2026 [확정](TEL 결산 PDF + japanir/ninescrolls/BigGo 요약). FY2025 GM 47.1%·R&D 250.0 [확정](TEL FY25 발표 + Integrated Report 2025). FY2026 GM 45.3%·R&D 277.8 [확정](Investing.com 슬라이드 + BigGo). FY2021 GM·R&D, FY2022 GM, FY2023 GM은 각 1건 [추정].
- **[충돌] FY2024 Field Solutions**: 검색 요약 하나는 "약 5,000억 엔"이라고 했지만, FY2025 FS 5,383억 엔이 "+25.6%"라는 TEL 발표를 역산하면 약 4,286억 엔입니다. **TEL 공식 성장률과 맞는 4,286억 엔 쪽이 더 신뢰할 만**합니다. 이 경우 FS는 FY2023 4,740억 → FY2024 4,286억(감소) → FY2025 5,383억으로, 다운턴에 서비스도 줄었다는 뜻이 됩니다.
- **기존 팩 정정**: tel.md 2-3은 FY2025 매출 성장률을 "+30.0%"(내부 Notion)로 적었으나, 1,830.5 → 2,431.5는 **+32.8%**이고 TEL 자료 요약도 32.8%입니다. FY2025 순이익은 5,441억 엔(+49.5%)으로, tel.md의 [충돌](내부 5,390억 vs 역산 5,440억)은 **5,441억 쪽으로 해소**됩니다.
- 출처: FY2024 연결재무제표 https://www.tel.com/ir/library/consolidated-financial-statements/hbu2s80000000099-att/Consolidated_Financial_Statements_FY2024.pdf · FY2024 결산단신 https://www.tel.com/ir/library/report/ll4pka00000000l9-att/fy24q4tanshin-e.pdf · FY2023 결산 https://www.tel.com/ir/library/report/a4fd9v000000004h-att/fy23q4tanshin-e.pdf · FY2022 발표자료 https://www.tel.com/ir/library/report/hq95qj00000007nc-att/fy22q4presentations-e.pdf · FY2025 발표 https://www.tel.com/ir/library/report/l8gqgo00000000gl-att/fy25q4presentations-e.pdf · Integrated Report 2025 재무 https://www.tel.com/ir/library/ar/pjsoh100000000rc-att/ir2025_data_section_en.pdf · FY2026 https://www.tel.com/ir/library/report/pjuomj00000000tf-att/fy26q4transcript-e.pdf · japanir https://japanir.jp/en/company/company-8035/ir/8035-20260430-01_wp_financial_summary/ · Investing.com FY2026 슬라이드 https://www.investing.com/news/company-news/tokyo-electron-fy2026-slides-q4-beats-fuel-40-growth-outlook-93CH-4654520 · BigGo Q1 FY2027 https://finance.biggo.com/news/JP_8035.T_2026-07-30 · companiesmarketcap https://companiesmarketcap.com/tokyo-electron/revenue/
- 세그먼트: TEL은 SPE(반도체 제조장비)와 FPD(평판디스플레이 제조장비)를 보고하고, SPE 안에서 신규장비와 Field Solutions를 나눠 공시합니다. **FPD 매출 금액은 이번 검색에서 확인 불가**입니다. "FPD 약 8%"라는 2차 블로그(matrixbcg) 수치는 출처 신뢰도가 낮아 쓰지 않습니다.

**SPE 신규장비 응용처 믹스(TEL)**

| 기간 | Logic/Foundry(비메모리) | DRAM | 비휘발성 메모리(NAND) | 태그 / 출처 |
|---|---|---|---|---|
| FY2024 | 62% | 31% | 7% | [추정] 검색 요약 1건(FY2025와 같은 값으로 나와 혼동 가능성 있음) |
| FY2025 | 62% | 31% | 7% | [추정] TEL 발표자료 요약 https://www.marketscreener.com/news/tokyo-electron-presentationsi-979kbi--ce7f58dbda8ffe23 |
| FY2026 | 59% | 31% | 10% | [추정] Investing.com FY2026 슬라이드 요약 |
| Q1 FY2027 | 57% | 32% | 11% | [확정] tel.md 2-3 + Investing.com Q1 FY2027 https://www.investing.com/news/company-news/tokyo-electron-q1-fy2027-slides-ai-boom-drives-record-sales-outlook-93CH-4827886 |

### 1-4. 3사 비교표 ① 수익성·R&D 추세

| 지표 | Lam (6월 결산) | AMAT (10월 결산) | TEL (3월 결산) |
|---|---|---|---|
| 최근 확정 연도 매출 | FY2026 $23.2B | FY2025 $28.4B | FY2026 ¥2.44T(약 $16B 수준, 환율 가정 필요) |
| 5년 매출 CAGR [계산] | FY2021→FY2026 약 9.7% | FY2021→FY2025 약 5.3% | FY2021→FY2026 약 11.8%(FY2021 저점 효과) |
| 다운턴 연도 매출 | FY2024 −14.5% | 역성장 없음(FY2023~24 +2~3%) | FY2024 −17% |
| GM 범위 | 44.6% → 50%대 | 46.5% → 48.7% | 40.4% → 47.1%(정점) → 45.3% |
| OPM 범위 | 28.6% → 35.3% | 28.9% → 30.2% | 22.9% → 29.9% → 25.6% |
| R&D/매출 | 9.3~12.8% | 10.7~12.6% | 7.9~11.4% |
| R&D 절대액 최근 | $2.38B(FY26) | $3.57B(FY25) | ¥277.8B(FY26) |
| 서비스 비중 | CSBG 33~40% | AGS 21~23% | FS 21~26% |
| 메모리 비중(시스템/신규장비) | 42~60%(가장 높음) | 23~40%(가장 낮음) | 38~43% |

- [해석] **세 회사의 수익성 궤적이 갈립니다.**
  - **Lam**: GM이 5년 동안 약 6%p, OPM이 약 6%p 올랐습니다. 3사 중 유일하게 "매출 회복 + 마진 구조 개선"이 동시에 확인됩니다. 원인으로 회사는 공장 효율과 제품 믹스를 들었고, 말레이시아 생산 이전(아래 5장)도 원가 측면에서 기여했을 가능성이 큽니다(인과는 [해석]).
  - **AMAT**: 가장 덜 변동적입니다. 매출이 매년 플러스였고 OPM은 29~30%에 고정돼 있습니다. 넓은 포트폴리오와 로직 노출이 **완충재** 역할을 했다는 뜻이지만, 동시에 업사이클에서 레버리지가 약하다는 뜻이기도 합니다. FY2026에 비GAAP OPM 34%로 올라선 것이 이 정체를 깨는 첫 신호입니다.
  - **TEL**: GM 정점이 FY2025 47.1%였고 FY2026은 45.3%로 후퇴했습니다. 중기계획 목표(OPM 35%)와의 간극(약 9%p)이 3사 중 가장 큽니다. 회사가 "2년 안에 GM 50% 이상"을 별도 목표로 내건 이유가 여기 있습니다.
- [해석] **R&D 강도**: AMAT은 R&D 절대액이 가장 크고 비중도 꾸준히 올라 FY2025 12.6%입니다. Lam은 FY2026에 R&D 비중이 오히려 낮아졌는데(매출이 더 빨리 늘어서), 그 직후 "$3B+ 랩 네트워크 투자"를 발표했습니다. 즉 **비용 비중은 낮게 유지하면서 설비형 R&D(랩·클린룸)로 투자 형태를 바꾸는 중**으로 읽힙니다. TEL은 5년 R&D ¥1.5조 계획으로 R&D/매출이 10%를 넘어 일본 기업 치고는 공격적입니다.

---

## 2. 고객 집중도

### 2-1. 회사별 공시

**Lam Research (10-K, 10% 이상 고객)**

| FY | 10% 이상 고객 수와 비중 | 이름 공시 | 태그 / 출처 |
|---|---|---|---|
| FY2024 | 1곳, 약 17% (다른 고객은 모두 10% 미만) | 이름은 표에서 확인 불가. 10-K는 주요 고객으로 Micron, Samsung, SK hynix, TSMC를 명시 | [추정] 10-K FY2024 https://www.sec.gov/Archives/edgar/data/707549/000070754924000106/lrcx-20240630.htm |
| FY2025 | 2곳, 약 17%·15% | 위와 같음 | [추정] 10-K FY2025 https://www.sec.gov/Archives/edgar/data/707549/000070754925000075/lrcx-20250629.htm |
| FY2026 | **4곳, 약 16%·15%·12%·12%** (합 약 55% [계산]) | 위와 같음(FY2024~26 주요 고객: Micron, Samsung, SK hynix, TSMC) | [추정] 10-K FY2026 https://www.sec.gov/Archives/edgar/data/0000707549/000070754926000037/lrcx-20260628.htm |

- "Samsung 단독 약 20%", "상위 5개사 70%+"라는 2차 블로그 서술이 있으나 공시 근거가 확인되지 않아 **쓰지 않습니다** (출처: https://www.deepresearchglobal.com/p/lam-research-swot-analysis-report).

**Applied Materials (10-K)**

| FY | 10% 이상 고객 | 태그 / 출처 |
|---|---|---|
| FY2023 | Samsung 15% (TSMC 등 다른 고객 비중 확인 불가) | [추정] 10-K FY2025 검색 요약(비교연도) |
| FY2024 | Samsung 12%, TSMC 11%, Intel 10% 미만 | [추정] 10-K FY2024 https://www.sec.gov/Archives/edgar/data/6951/000000695124000044/amat-20241027.htm |
| FY2025 | 2곳, 약 19%·15% (이름은 요약에서 확인 불가) | [추정] 10-K FY2025 https://www.sec.gov/Archives/edgar/data/6951/000162828025056742/amat-20251026.htm |
| 참고: FY2025 상반기(6개월) | TSMC 18%, Samsung 17% | [추정] 10-Q(2025-04-27) https://www.sec.gov/Archives/edgar/data/6951/000000695125000024/amat-20250427.htm |

- [해석] FY2025 상반기 수치로 미뤄 보면 FY2025 연간 19%·15%는 TSMC·Samsung일 가능성이 높지만, **이름 매칭은 확인 불가**입니다. 원고에는 "상위 2개 고객이 각각 약 19%, 15%(10-K FY2025)"로만 쓰는 것을 권장합니다.

**Tokyo Electron (유가증권보고서, 10% 이상 고객)**

| FY | 고객 | 비중 | 태그 / 출처 |
|---|---|---|---|
| FY2026(2026.3) | Samsung Electronics | 15.1%(약 3,681억 엔) | [추정] 검색 요약 1건, 유가증권보고서 근거로 표기 https://www.postation.jp/news/tsmc-japan-chip-equipment-customers |
| FY2026 | TSMC | 12.9%(약 3,158억 엔) | [추정] 위와 같음 |
| 일반 | 일본 회계기준 상장사는 매출 10% 이상 고객명을 유가증권보고서에 기재. TEL 포함 일본 장비·소재 8개사가 TSMC를 10% 이상 고객으로 공시 | [추정] 같은 출처 |

- "TSMC·Intel·Samsung 합계 50%"라는 2차 블로그 서술(matrixbcg)은 공시 근거가 없어 쓰지 않습니다.

### 2-2. 3사 비교표 ② 고객 집중도

| 항목 | Lam | AMAT | TEL |
|---|---|---|---|
| 10% 이상 고객 수(최근) | 4곳(FY2026) | 2곳(FY2025) | 2곳 이상(FY2026, Samsung·TSMC 확인) |
| 최대 고객 비중 | 약 16% | 약 19% | 약 15%(Samsung) |
| 10% 이상 고객 합계 [계산] | 약 55% | 약 34% | 약 28%+ |
| 추세 | 1곳(FY24) → 2곳(FY25) → 4곳(FY26): 집중 심화 | 2곳 유지, 상위 비중 상승(12/11% → 19/15%) | 시계열 확인 불가 |
| 공시상 Samsung 위상 | 이름은 주요 고객 목록에만 | FY2023 15% → FY2024 12% | FY2026 최대 고객(15.1%) |

- [해석] **Lam의 고객 집중이 가장 빠르게 심해지고 있습니다.** FY2026에 4개 고객이 각각 12% 이상이라는 것은, 메모리 3사(Samsung·SK hynix·Micron)와 TSMC가 동시에 큰손이 됐다는 뜻입니다. 중국 고객(분산된 다수 고객)이 줄고 글로벌 대형 고객이 늘어난 지역 믹스 변화(3장)와 같은 현상의 다른 면입니다. 협상력 측면에서는 **고객 1곳의 투자 연기가 실적에 주는 충격이 커졌습니다.**
- [해석] **한국 고객의 비중**: 세 회사 모두 Samsung이 10% 이상 고객입니다. TEL은 Samsung이 TSMC보다 큰 최대 고객이고, AMAT도 FY2023~24에는 Samsung이 최대 고객이었습니다. 한국 법인이 "지사"가 아니라 **최대 고객 계정을 관리하는 핵심 조직**이라는 근거로 쓸 수 있습니다.

---

## 3. 지역 매출 믹스와 수출규제

### 3-1. 회사별 연간 지역 비중

**Lam Research (FY = 6월 결산, % of revenue)**

| FY | 중국 | 한국 | 대만 | 일본 | 미국 | 동남아 | 유럽 | 태그 |
|---|---|---|---|---|---|---|---|---|
| FY2021 | 35% | 27% | 확인 불가 | 확인 불가 | 확인 불가 | 확인 불가 | 확인 불가 | [추정] |
| FY2022 | 31% | 23% | 17% | 9% | 8% | 8% | 4% | [추정] |
| FY2023 | 26% | 20% | 20% | 10% | 9% | 8% | 7% | [추정] |
| FY2024 | **42%** | 19% | 11% | 10% | 7% | 6% | 5% | [추정] |
| FY2025 | 34% | 22% | 19% | 10% | 7% | 5% | 3% | [추정] |
| FY2026 | 34% | 19% | 22% | 9% | 7% | 6% | 3% | [추정] |
| 분기 추이 | 26Q1 43% → 26Q2 35% → 26Q3 34% → 26Q4 26% | 26Q3 23% → 26Q4 20% | 26Q4 27% | | | | | [확정] lam.md 2-3 |

- 출처: 10-K FY2022~FY2026(위 1-1 링크), 검색 요약 https://www.stock-analysis-on.net/NASDAQ/Company/Lam-Research-Corp/Ratios/Geographic-Areas , https://bullfincher.io/companies/lam-research-corporation/revenue-by-geography
- 수출규제 언급: ① 2022년 10월 규제 직후 "최대 $2.5B 매출 손실" 경고 [추정] (SCMP https://www.scmp.com/tech/tech-war/article/3196597/tech-war-us-chip-equipment-makers-calculate-revenue-losses-billions-after-washingtons-curbs-china). ② BIS 50% 계열사 규칙(Affiliates Rule)으로 2026년 매출 약 $600M 감소, 중국 비중 30% 미만 전망 [확정] (Seeking Alpha https://seekingalpha.com/news/4507247-lam-research-anticipates-china-revenue-below-30-percent-in-2026-as-ai-drives-record-5b , Yahoo/Zacks https://finance.yahoo.com/news/lrcxs-china-revenue-drop-below-132200026.html).

**Applied Materials (FY = 10월 결산, % of revenue)**

| FY | 중국 | 한국 | 대만 | 일본 | 미국 | 태그 |
|---|---|---|---|---|---|---|
| FY2021 | 33% ($7.54B) | 22% ($5.01B) | 20% ($4.74B) | 확인 불가 | 확인 불가 | [추정] |
| FY2022 | 28% ($7.25B) | 17% ($4.40B) | 24% ($6.26B) | 확인 불가 | 확인 불가 | [추정] |
| FY2023 | 27% ($7.25B) | 18% ($4.61B) | 21% ($5.67B) | 확인 불가 | 확인 불가 | [추정] |
| FY2024 | **37%** ($10.12B) | 17% ($4.49B) | 15% ($4.01B) | 확인 불가 | 확인 불가 | [추정] |
| FY2025 | 30.1% ($8.53B) | 19.8% ($5.61B) | 24.2% ($6.86B) | 8.0% | 10.8% | [확정] amat.md 2-2 + 이번 검색 일치 |
| FY2026 분기 | Q2 24%, Q3 26% | 확인 불가 | 확인 불가 | | | [확정] amat.md 2-1 |

- 출처: 10-K FY2022 https://www.sec.gov/Archives/edgar/data/6951/000000695122000043/amat-20221030.htm · 10-K FY2024 https://www.sec.gov/Archives/edgar/data/6951/000000695124000044/amat-20241027.htm · 10-K FY2025(위) · bullfincher https://bullfincher.io/companies/applied-materials/revenue-by-geography
- 수출규제 언급: Affiliates Rule로 FY2025 Q4 약 $110M, FY2026 약 $600M 매출 감소 예상(2025-09-29 8-K). 이후 보도에서는 $600~710M 범위 [확정] (8-K https://www.sec.gov/Archives/edgar/data/6951/000162828025043753/amat-20250929.htm , MarketScreener https://www.marketscreener.com/news/applied-materials-expects-new-export-rule-to-hit-2026-revenue-by-600-million-ce7d5bded188f024 ). 2026-02 미 상무부 조사 관련 $252.5M 합의는 amat.md 9-5 참조.

**Tokyo Electron (FY = 3월 결산, % of net sales)**

| FY | 중국 | 한국 | 대만 | 태그 / 출처 |
|---|---|---|---|---|
| FY2022 | 약 26% | 확인 불가 | 확인 불가 | [추정] 검색 요약 1건 |
| FY2023 | 약 24% | 확인 불가 | 확인 불가 | [추정] 위와 같음 |
| FY2024 | **약 44%**(8,130억 엔+) | 2위 시장(비중 확인 불가) | 3위 | [추정] Statista https://www.statista.com/statistics/208590/worldwide-sales-of-tokyo-electron-in-2011-by-region/ |
| FY2025 | 41.7%~42% | 약 17%(4,090억 엔) [계산 16.8%] | 약 17% | [확정] 중국: ashu-chinastatistics + 일본 요약 2건 / 한국: 금액 요약 + 비율 요약 일치 |
| FY2026 | 34.1% | 22.3% | 20.4% | [확정] global-net https://global-net.co.jp/archives/12822 + tel.md 2-3 |
| Q4 FY2026 / Q1 FY2027 | 26.8% / 30.4% | 24.3% / 20.8% | 22.0% / 25.4% | [확정] tel.md 2-3 |

- 출처 추가: https://ashu-chinastatistics.com/news/309927-931870818430 , TrendForce(2025.6.30, 중국 30%대로 하락 전망) https://www.trendforce.com/news/2025/06/30/news-tokyo-electron-reportedly-sees-china-sales-dropping-to-30-in-2025-amid-tightening-u-s-export-curbs/
- 수출규제 언급: 일본 정부의 2023년 7월 23개 품목 수출관리 강화. TEL은 "규제 영향 제품은 일부(well below 50%)"이며 AI·첨단 공정용 장비가 FY2026 매출의 약 40%에 이를 것이라고 설명 [추정] (TrendForce 2025.12.8 https://www.trendforce.com/news/2025/12/08/news-tokyo-electron-sees-ai-driven-sales-hitting-40-by-2026-offsetting-china-slowdown/ , Startup Fortune https://startupfortune.com/japans-chip-equipment-giants-are-losing-china-and-betting-on-ai-to-fill-the-gap/ ). TEL이 미국 Affiliates Rule에 대해 따로 정량 영향을 밝힌 자료는 확인 불가.

### 3-2. 3사 비교표 ③ 지역 믹스(각 사 최근 회계연도)

| 지역 | Lam FY2026(~2026.6) | AMAT FY2025(~2025.10) | TEL FY2026(~2026.3) |
|---|---|---|---|
| 중국 | 34% (정점 FY24 42%) | 30.1% (정점 FY24 37%) | 34.1% (정점 FY24 약 44%) |
| 한국 | 19% (FY21 27%) | 19.8% (FY21 22%) | 22.3% (FY25 약 17%) |
| 대만 | 22% | 24.2% | 20.4% |
| 일본 | 9% | 8.0% | 확인 불가 |
| 미국 | 7% | 10.8% | 확인 불가 |
| 수출규제 정량 영향 | 2026년 약 $600M | FY2026 약 $600~710M | 비공개(확인 불가) |

- [해석] **세 회사 모두 FY2024 전후에 중국 비중 정점(37~44%)을 찍고 내려오는 같은 궤적**입니다. 2023~24년 중국 고객의 선제적 "규제 전 사재기" 수요가 다운턴을 메웠고, 그 기저가 빠지는 2025~26년에 AI 관련 대만·한국·미국 투자가 자리를 대신했습니다. TEL의 중국 정점이 가장 높았던 것은 일본 규제가 미국보다 늦고 범위가 좁았기 때문이라는 해석이 일반적입니다(인과는 [해석]).
- [해석] **한국 비중은 3사 모두 20% 안팎에서 수렴**합니다. 다만 방향이 다릅니다. Lam은 27%(FY21) → 19%(FY26)로 장기 하락했고(NAND 투자 위축, TSMC 비중 상승), TEL은 17% → 22%로 상승했습니다(HBM·DRAM 투자에서 코터/디벨로퍼·식각 수요). **한국 메모리 투자 사이클에 가장 민감한 회사가 Lam에서 TEL로 옮겨가는 중**이라는 가설을 세울 수 있습니다(검증 필요).
- [해석] **규제 리스크 일정**: BIS Affiliates Rule은 2025-11-10부터 1년간 시행 유예됐고 유예 만료가 **2026-11-09**입니다(Federal Register https://www.federalregister.gov/documents/2025/11/12/2025-19846/one-year-suspension-of-expansion-of-end-user-controls-for-affiliates-of-certain-listed-entities , Skadden https://www.skadden.com/insights/publications/2025/11/bis-suspends-affiliates-rule-for-one-year-as-part-of-the-us-china-trade-deal ). 기준일(2026-10-01)로부터 약 6주 뒤입니다. 연장 여부가 Lam·AMAT의 2027년 중국 매출 가이던스를 좌우하는 단기 변수입니다. 미국 규칙이라 TEL은 직접 대상이 아니지만, 미국 하원이 일본·네덜란드 공조 강화를 압박하고 있다는 점(tel.md 2-4)은 TEL에도 꼬리 리스크입니다.

---

## 4. 중장기 전략

### 4-1. Lam Research: Investor Day 2025(2025-02) 목표

| 항목 | 내용 | 태그 / 출처 |
|---|---|---|
| 2028 재무 목표 | 매출 $25~27B, GM 약 50%, OPM 34~35%, EPS $6~7 | [확정] Investor Day 자료 https://filecache.investorroom.com/mr5ir_lamresearch2/1435/Lam%20Research%202025%20Investor%20Day%20FINAL.pdf , Quartr https://quartr.com/events/lam-research-corporation-lrcx-investor-day-2025_33D7JGMm , X 요약 https://x.com/TheAmericanCEO/status/1894133373943046243 |
| 장기("$1조 반도체 시대") | 매출 $30B+, GM 50%+, EPS $8+ | [추정] Quartr 요약 |
| SAM 확대 | WFE 대비 SAM을 "low 30%"에서 decade 말 "high 30%"로. 신규 구조가 만드는 증분 SAM의 50% 이상 점유 | [추정] Quartr 요약 |
| 핵심 변곡점 | 3D NAND(고층화), 3D DRAM, GAA, 후면전력공급(BSPDN), 첨단 패키징. 첨단 웨이퍼당 WFE 강도 50% 이상 증가 전망 | [추정] Quartr 요약 |
| 제품 목표 | ALD 몰리브덴 3~5년 누적 출하 $2B+, Aether(EUV 건식 레지스트) 5년 $1.5B | [추정] Quartr 요약 |
| CSBG | 설치기반보다 빠르게 성장. "2028년까지 2배 이상" 언급은 2차 요약 1건 | [추정, 검증 필요] Investing.com 콜 요약 https://www.investing.com/news/transcripts/earnings-call-transcript-lam-research-q4-2025-beats-expectations-stock-rises-93CH-4161532 |
| Morningstar 평가 | 2028 목표는 "optimistic" | [추정] https://www.morningstar.com/company-reports/1265715-lam-research-we-raise-our-valuation-after-upbeat-investor-day-but-see-2028-targets-as-optimistic |

**진척도(2026-10 기준)**
- FY2026 실적이 이미 **매출 $23.2B, OPM 35.3%**로, 2028 목표의 OPM 하단(34%)을 2년 앞당겨 넘었습니다. FQ1'27 가이던스($8.1B, 연환산 약 $32B [계산])대로면 매출 목표($25~27B)도 FY2027에 넘을 수 있습니다 [해석].
- Q4 FY26 콜: conductor etch·deposition 수주로 SAM 확대가 "Investor Day 목표보다 빠르게 high-30%로" 진행 중. Conductor etch 설치기반 4만 챔버 돌파, Akara 설치기반이 2027년에도 2배 성장 전망. NAND에서 128단 → 500단+로 가면 웨이퍼당 Lam SAM 2배 [확정] (Yahoo 하이라이트, Investing.com 트랜스크립트, Motley Fool https://www.fool.com/earnings/call-transcripts/2026/08/07/lam-research-lrcx-q4-2026-earnings-call-transcript/ ).
- 2026년을 "WFE 대비 3년 연속 아웃퍼폼"으로 전망 [추정] (Yahoo 하이라이트).
- [해석] 2028 목표가 사실상 조기 달성 국면이라, 시장의 관심은 **다음 Investor Day에서 목표를 얼마나 올리느냐**로 옮겨갈 것입니다. 단, 이번 업사이클의 상당 부분이 NAND 업그레이드(설치기반 전환)여서, 신규 팹 사이클이 꺾일 때 CSBG가 완충해 줄 수 있느냐가 목표의 지속성을 가릅니다.

### 4-2. Applied Materials: 전략 진술과 목표

| 항목 | 내용 | 태그 / 출처 |
|---|---|---|
| 2021 Investor Meeting(2021-04-06) 목표 | FY2024까지 FY2020 대비 매출 +55% 이상, 비GAAP EPS +100% 이상, SSG 매출 +60% 이상 | [추정] AMAT IR https://investor.appliedmaterials.com/news-releases/news-release-details/applied-materials-showcases-unique-capabilities-accelerate |
| 결과(FY2024) | 매출 $27.18B, 비GAAP EPS $8.65(사상 최대) | [확정] 8-K FY2024 + IR |
| 2021 목표 달성 여부 [계산] | FY2020 매출 $17.2B(확인 불가, 일반 공개값)로 가정하면 +58% 수준. 원문 대조 전까지 "대체로 달성"으로만 표현 | [해석] |
| 정체성 | "materials engineering" 회사. 여러 공정(증착·식각·CMP·이온주입·계측)을 묶은 **통합 솔루션(co-optimized)**과 PPACt(전력·성능·면적·비용·출시시간) 프레임 | [추정] amat.md 2-4, 4-1 |
| 2026 시장 전략 | 선단 파운드리·로직, DRAM(HBM 포함), 첨단 패키징이 2026~27년 WFE 성장의 약 80%. 이 세 분야 리더십으로 다년 성장. DRAM 다음 구조 변곡점에서 점유율 추가 확보 기대 | [확정] Futurum Q2·Q3 https://futurumgroup.com/insights/applied-materials-q2-fy-2026-ai-capacity-expansion-fuels-equipment-demand/ , Q2 FY2026 prepared remarks https://ir.appliedmaterials.com/static-files/28ef7eff-8b4d-418e-999a-dbfa403ce6f3 , Seeking Alpha https://seekingalpha.com/news/4522053-applied-materials-projects-2026-growth-led-by-ai-driven-foundry-logic-and-dram |
| 2026 성장 가이드 | 반도체 장비 사업 CY2026 성장률 2월 "20%+" → 5월·8월 "30%+". 회사 전체 "40%에 근접" 언급도 있음 | [확정] amat.md 2-1 / [추정] 24/7 Wall St https://247wallst.com/investing/2026/09/10/applied-materials-ceo-says-the-ai-boom-is-nowhere-near-over-his-order-book-is-the-proof/ |
| AGS 목표 | CY2026 AGS +20% 이상, **장기 지속 성장률 연 mid-teens(10%대 중반)** | [확정] Q3 FY2026 콜 요약 https://finance.yahoo.com/markets/stocks/articles/applied-materials-q3-earnings-call-220405111.html , Investing.com https://www.investing.com/news/transcripts/earnings-call-transcript-applied-materials-beats-q3-2026-estimates-shares-fall-93CH-4859444 |
| EPIC Center | 실리콘밸리(서니베일) $5B, 클린룸 18만 sq ft 이상, 2023년 발표·2026년 가동 목표. Samsung(2026.2), SK hynix(2026.3), TSMC(2026.5), Micron, Kioxia(2026.9) 등 참여 | [확정] amat.md 3-3·9-6, GlobeNewswire TSMC https://www.globenewswire.com/news-release/2026/05/11/3291946/0/en/Applied-Materials-and-TSMC-Partner-at-the-EPIC-Center-to-Accelerate-AI-Scaling.html , Semiecosystem https://marklapedus.substack.com/p/two-semiconductor-r-and-d-centers |

- 공식 "2028 재무 모델" 같은 수치 목표를 AMAT이 최근(2024~2026) 투자자 행사에서 새로 냈는지는 **확인 불가**입니다. Lam·TEL과 달리 AMAT의 최근 전략은 **"재무 목표"보다 "구조적 성장 동력(AI 3대 분야)과 AGS 장기 성장률"로 소통**하는 방식입니다.
- [해석] AMAT의 전략 축은 두 개입니다. ① **EPIC로 고객의 연구 단계부터 들어가 공정 레시피와 장비 선정(POR)을 선점**하는 것. 메모리 4사(Samsung·SK hynix·Micron·Kioxia)와 TSMC가 모두 들어온 것은 "공동개발 플랫폼"으로서 사실상 업계 표준 위치를 노린다는 뜻입니다. ② **AGS를 구독형으로 전환해 사이클 방어**. 장기 mid-teens 성장 가이드는 장비 매출(사이클성)과 서비스 매출(구조성)을 분리해 밸류에이션을 받겠다는 메시지로 읽힙니다.

### 4-3. Tokyo Electron: 중기경영계획(2022-06-08 발표)

| 항목 | 목표 | 진척(FY2026 실적·FY2027 진행) | 태그 / 출처 |
|---|---|---|---|
| 매출 | FY2027(2027.3)까지 ¥3조 이상 | FY2026 ¥2.44조. Q1 FY2027 ¥7,323억, 상반기 가이던스 ¥1.62조. 회사 "¥3조 이상 달성에 자신감 커짐" | [확정] TEL 2022.6 https://www.tel.com/news/ir/2022/20220608_001.html , BigGo https://finance.biggo.com/news/JP_8035.T_2026-07-30 , tel.md 2-1·2-3 |
| 영업이익률 | 35% 이상 | FY2026 25.6%, Q1 FY2027 28.9%. 회사는 "이번 회계연도 내 달성 의지" 재확인 | [확정] 위와 같음 |
| ROE | 30% 이상 | 매출·ROE는 목표 궤도라는 평가 | [추정] tel.md 2-1 [S23] |
| 매출총이익률 | (추가 목표) 2년 안에 50% 이상 | FY2025 47.1% 정점, FY2026 45.3%, Q1 FY2027 46.8% | [확정] Investing.com Q1 FY2027, BigGo |
| R&D | 5년(FY2023~27) ¥1조 이상 → IR Day(2025-02-26)에서 **FY2025부터 5년 ¥1.5조 이상**으로 확대 | FY2025 ¥250.0B, FY2026 ¥277.8B | [확정] IR Day https://www.tel.com/ir/policy/mplan/i9nanv00000000ga-att/20250226_TELIRDay_E_rev.1_slide_r3.pdf , Integrated Report 2025 |
| 설비투자 | FY2025부터 5년 ¥7,000억 이상 | FY2026 설비투자 전년 대비 +48%로 사상 최대(보도) | [확정] IR Day / [추정] TrendForce 2026.1.9 https://www.trendforce.com/news/2026/01/09/news-tokyo-electron-reportedly-raises-fy26-capex-48-to-record-high-bets-on-dram-etching-demand/ |
| 가이던스 방식 | FY2027부터 연간 가이던스 중단, 반기만 제시 | — | [추정] tel.md 2-3 |

- **주의(혼동 방지)**: 검색에 나오는 "VISION2030(FY2026~FY2030)"은 **자회사/관계사 도쿄일렉트론디바이스(TED, 2760)**의 중기계획입니다. TEL(8035)의 차기 중기계획은 기준일 현재 **확인 불가**입니다. FY2027이 현 계획의 마지막 해이므로 2027년 상반기에 새 계획이 나올 가능성이 높습니다([해석]). 출처: https://www.teldevice.co.jp/eng/ir/management_plan.html
- [해석] **진척 평가**: 매출 ¥3조는 반기 가이던스(¥1.62조) × 하반기 성장 가정이면 도달 가능한 거리입니다. 그러나 OPM 35%는 Q1 28.9%에서 남은 3개 분기 평균 약 37%가 필요해 **4개 목표 중 가장 어렵습니다**([계산]: 연 매출 ¥3조·OPM 35%면 영업이익 ¥1.05조, Q1 ¥2,114억을 빼면 잔여 3개 분기 ¥8,386억 ÷ 매출 약 ¥2.27조 ≈ 37%). 비용 측면에서 R&D(¥1.5조/5년)와 설비투자(+48%)를 동시에 늘리는 중이라, 이익률보다 **점유율·기술 투자를 우선하는 선택**을 했다고 볼 수 있습니다.

### 4-4. 3사 비교표 ④ 중장기 목표

| 항목 | Lam | AMAT | TEL |
|---|---|---|---|
| 최신 공식 목표 발표 | Investor Day 2025-02 | Investor Meeting 2021-04(이후 수치 목표 갱신 확인 불가) | 중기계획 2022-06 + IR Day 2025-02 |
| 목표 연도 | CY2028(장기 "$1조 시대") | FY2024(완료) | FY2027(2027.3) |
| 매출 목표 | $25~27B | FY2020 대비 +55% | ¥3조+ |
| 이익률 목표 | GM 약 50%, OPM 34~35% | 비GAAP EPS +100% | OPM 35%+, ROE 30%+, (GM 50%+ 2년 내) |
| 진척 | 사실상 조기 달성 국면 | 달성(FY2024 EPS $8.65) | 매출 근접, OPM 간극 큼 |
| SAM·점유율 주장 | SAM WFE의 low→high 30%, 증분 SAM 50%+ | AI 3대 분야(WFE 성장의 80%) 리더십 | 코터/디벨로퍼 90%+, EUV용 100% (tel.md 2-2) |
| 서비스 목표 | CSBG 설치기반보다 빠른 성장 | AGS 장기 mid-teens 성장 | FS 정량 목표 확인 불가 |

---

## 5. 자본배분: 주주환원·M&A·설비/R&D 투자

### 5-1. 회사별

**Lam Research**
| 항목 | 내용 | 태그 / 출처 |
|---|---|---|
| 자사주 매입 승인 | 2024-05 $10B 추가 승인(만기 없음), 같은 시기 10:1 액면분할 발표(2024-10 시행) | [확정] PRNewswire https://www.prnewswire.com/news-releases/lam-research-corporation-announces-10-billion-share-repurchase-authorization-and-a-10-for-1-stock-split-302150679.html , 10-K FY2026 |
| FY2026 주주환원 | 총 $5.12B 이상(자사주 $3.85B + 배당 $1.27B). FY2025 자사주 $3.42B | [추정] Yahoo https://uk.finance.yahoo.com/news/lam-research-returns-5b-shareholders-134200568.html |
| 배당 | 분기 배당 $0.26 → $0.33(+27%), 2026-10-14 지급 | [확정] PRNewswire https://www.prnewswire.com/news-releases/lam-research-corporation-announces-a-27-increase-in-quarterly-dividend-302862122.html , Yahoo |
| M&A | 소규모·기술 보강형. Coventor(2017-08, $137.6M, 공정 시뮬레이션), Esgee Technologies(2022, 플라즈마 시뮬레이션), SEMSYSCO(2022-11, 오스트리아 습식장비, 첨단 패키징) | [확정] BusinessToday https://www.businesstoday.in/latest/corporate/story/lam-research-acquires-semsysco-adds-advanced-packaging-capabilities-353059-2022-11-16 , electronics360 https://electronics360.globalspec.com/article/18921/lam-research-acquires-wet-chip-equipment-vendor-semsysco , 10-K FY2018 |
| R&D 설비 | 향후 5년 $3B+ 글로벌 랩 네트워크 확장(2026-08-13 발표), 실험 처리량 50% 이상 증가 목표. 첫 단계로 오리건 Tualatin 랩 착공(2026-08-26) | [확정] Lam IR https://newsroom.lamresearch.com/2026-08-13-Lam-Research-Announces-Plans-to-Invest-More-than-3B-to-Expand-Global-Lab-Network,-Increase-Innovation-Velocity-in-the-AI-Era , Oregon https://newsroom.lamresearch.com/2026-08-26-Lam-Research-Breaks-Ground-on-New-Oregon-Lab-to-Accelerate-AI-Era-Semiconductor-Research-Development-Locally,-Globally , eeNews https://www.eenewseurope.com/en/lam-research-to-invest-3bn-in-global-rd-lab-expansion/ |
| 생산 설비 | 말레이시아 바투카완(페낭) 최대 생산기지 2021-08 개소(80만 sq ft 이상) | [확정] MIDA https://www.mida.gov.my/media-release/lam-research-to-expand-global-footprint/ , AmCham https://amcham.com.my/lam-research-strengthens-global-manufacturing-network-with-largest-manufacturing-facility-in-malaysia/ |
| 인도 | 카르나타카에 ₹10,000 crore(약 $1.2B) 이상 투자 약정(2025-02) | [확정] Deccan Herald https://www.deccanherald.com/business/us-firm-lam-research-commits-investment-worth-over-rs-10000-cr-in-karnataka-3401948 , Benzinga https://www.benzinga.com/government/regulations/25/02/43664402/lam-research-commits-1-2-billion-investment-in-india-eyes-63-billion-semiconductor-growth-market |

**Applied Materials**
| 항목 | 내용 | 태그 / 출처 |
|---|---|---|
| 자사주 매입 승인 | 2025-03 $10B 신규 승인(기존 잔여 약 $7.6B에 추가) | [확정] Investing.com https://www.investing.com/news/company-news/applied-materials-raises-dividend-adds-10-billion-buyback-93CH-3917462 , Seeking Alpha https://seekingalpha.com/news/4418852-applied-materials-raises-dividend-by-15-to-effect-10b-share-repurchase-program |
| 배당 | 2025-03 분기 배당 +15%($0.46), 8년 연속 인상 | [확정] 위와 같음 |
| FY2025 주주환원 | 약 $6.3B. 10년간 배당 CAGR 16%, FCF의 약 90% 환원 | [추정] AMAT 보도자료 요약 |
| 실패한 M&A | **Kokusai Electric 인수 무산**: 중국 규제당국 승인 지연으로 2021-03-19 계약 종료(2021-03-29 발표). KKR에 해지 수수료 $154M 현금 지급. 대만·일본·한국·아일랜드·이스라엘 승인은 받았음 | [확정] AMAT IR https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-termination-kokusai-electric/ , 8-K https://www.sec.gov/Archives/edgar/data/6951/000119312521097484/d165560dex991.htm , Caixin https://www.caixinglobal.com/2021-03-23/china-hurdle-threatens-applied-materials-bid-for-kokusai-electric-101678995.html |
| R&D 설비 | EPIC Center $5B(4-2 참조) | [확정] |
| 생산 설비 | 싱가포르 $500M 투자, 생산능력 2배·1,000명 고용(2026-06 발표) | [추정] AMAT IR https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-expands-singapore-manufacturing-support-ai |
| 인도 | 10년간 $5B 투자(140에이커 리서치파크, 공급망 10배 확대), SEMICON India 2026(2026-09) 발표 | [확정] TechNode https://technode.global/2026/09/18/applied-materials-5b-india-semiconductor-investment/ , Business Standard https://www.business-standard.com/amp/companies/news/applied-materials-to-invest-5-billion-in-india-over-next-decade-126091700558_1.html |
| 한국 | 오산 Applied Collaboration Center(건설 중), 용인 필드오피스(2026-07 협약) | [확정] amat.md 3-2 |

**Tokyo Electron**
| 항목 | 내용 | 태그 / 출처 |
|---|---|---|
| 배당 정책 | 배당성향 약 50%. FY2026 기말배당 364엔, 배당성향 50.1% | [추정] japanir https://japanir.jp/en/company/company-8035/ir/8035-20260430-01_wp_financial_summary/ |
| 자사주 매입 | 최대 750만 주(1.64%) / ¥1,500억, 2026-06 ~ 2027-03. 주식분할과 연계 보도 | [추정] MarketScreener https://www.marketscreener.com/news/tokyo-electron-limited-announces-an-equity-buyback-for-7-500-000-shares-representing-1-64-for-150-ce7f5ddbdf8df027 , TipRanks https://www.tipranks.com/news/company-announcements/tokyo-electron-sets-up-150-billion-share-buyback-facility-ahead-of-stock-split . 결의일 [충돌]: 2026-05-29 vs "2월 6일" 표기 혼재 |
| M&A | 대형 M&A 확인 불가. (참고: 2013~15 AMAT–TEL 합병 시도는 미국 법무부 반대로 2015년 무산. 이번 검색에서 원문 재확인 못함 → 확인 불가로 둠) | 확인 불가 |
| R&D·설비 계획 | FY2025부터 5년 R&D ¥1.5조+, 설비투자 ¥7,000억+ | [확정] IR Day 2025 |
| 신규 거점 | 미야기 신생산동(연면적 약 88,600㎡, 공사비 약 ¥1,040억, 2027년 여름 준공 예정), 구마모토 신개발동, 이와테 도호쿠 생산·물류센터(2025-11 준공), 미야기 개발동 3호(스마트팩토리) | [확정] IR Day 2025 + TEL 뉴스 https://www.tel.com/news/ir/2025/20251121_001.html , TEL 블로그 https://www.tel.com/blog/all/20251125_001.html |
| 한국 | TTCK-2(화성, 2024-10 준공, 2,000~2,500억 원), TTCK-Y(용인, 2027-01 준공 목표) | [확정] tel.md 3-3 |

### 5-2. 3사 비교표 ⑤ 자본배분

| 항목 | Lam | AMAT | TEL |
|---|---|---|---|
| 최근 연간 주주환원 | FY2026 $5.1B+ | FY2025 약 $6.3B | 배당성향 50% + ¥1,500억 매입(2026~27) |
| 매입 승인 잔액 성격 | $10B(2024-05) | $10B(2025-03) + 잔여 | 기간 한정 프로그램 |
| 배당 인상 | +27%(2026-09) | +15%(2025-03) | 실적 연동(배당성향 기준) |
| M&A 성향 | 소형 기술 인수(시뮬레이션·습식·패키징) | 대형 시도(Kokusai, 2021 무산·해지수수료 $154M. 인수가는 이번 검색에서 확인 불가) 후 내부 성장 | 대형 M&A 확인 불가 |
| 대표 R&D 투자 | 글로벌 랩 $3B+/5년 | EPIC $5B | R&D ¥1.5조/5년 |
| 생산 거점 다변화 | 말레이시아, 인도 | 싱가포르, 인도 | 일본 국내(미야기·구마모토·이와테) 집중 |

- [해석] **생산 전략이 정반대**입니다. 미국 2사는 말레이시아·싱가포르·인도로 생산과 공급망을 옮기며(원가·지정학 분산), TEL은 일본 도호쿠·규슈에 신공장을 짓는 **국내 집중** 전략입니다. TEL은 일본 내 엔지니어링·공급망 밀착을 품질 경쟁력으로 보는 반면, 엔저가 원가 측면에서 국내 생산을 정당화합니다(엔저 효과는 [해석]).
- [해석] **R&D 투자의 형태가 "랩·클린룸"으로 수렴**합니다. AMAT EPIC($5B), Lam 랩 네트워크($3B+), TEL 개발동·TTCK 계열이 모두 "고객 웨이퍼를 받아 장비사 사내 팹에서 먼저 공정을 개발"하는 구조입니다. 공정 난도가 올라가면서 **R&D의 무게중심이 고객 팹에서 장비사 팹으로 이동**하고 있고, 이는 장비사의 POR 선점력을 키우는 방향입니다.
- [해석] AMAT–Kokusai 무산(2021)은 **중국 규제당국이 글로벌 장비 M&A의 사실상 거부권**을 가진다는 것을 보여 준 사례입니다. 이후 3사 모두 대형 수평 통합보다 소형 기술 인수·내부 투자로 방향을 잡은 배경으로 읽을 수 있습니다.

---

## 6. 서비스 사업의 경제학

### 6-1. 회사별

| 항목 | Lam CSBG | AMAT AGS | TEL Field Solutions |
|---|---|---|---|
| 포함 범위 | 서비스, 스페어, 업그레이드, Reliant(비선단 신품·리퍼비시 장비) | 스페어, 서비스, 200mm 레거시 장비, 공정 최적화·원격진단 | 부품·서비스, 개조(modification), 중고장비 |
| 최근 연간 매출 | FY2026 $8.35B(+20% [계산]) | FY2025 $6.39B(+3%) | FY2026 ¥626.0B(+16.3%) |
| 최근 분기 | FQ4'26 약 $2.5B(+43% YoY) | FQ3'26 $1.8B(+22% YoY) | 확인 불가 |
| 매출 비중 | 36~40% | 21~23% | 21~26% |
| 설치기반 | **[충돌]** "100,000 챔버 초과"(lam.md) vs "약 100,000 챔버"(FY2025 콜 요약). Conductor etch만 4만 챔버+ | **[충돌]** 약 42,500 시스템(amat.md) vs "55,000 툴 초과, 연 5%+ 성장"(TIKR, FY26 Q2 기준). AIx 연결 챔버 3만7천+ | 92,000대 초과, 연 4,000~6,000대 증가 [추정] |
| 계약 모델 | Equipment Intelligence, Dextro(협동로봇 유지보수) 등 고도화 서비스. NAND에서 검증 후 DRAM으로 확장 | AGS 매출의 2/3 이상이 다년 구독 계약, 갱신률 90%+, 평균 2.9년 | 정량 공개 확인 불가 |
| 성장 동력 | **업그레이드**(NAND 200단+ 전환, "record upgrade revenue") | 구독 서비스 + 거래형 부품 수요 | 고객 팹 가동률 상승, 개조·중고장비 |
| 목표 | 설치기반보다 빠른 성장 | CY2026 +20%+, 장기 mid-teens | 확인 불가 |

- 출처: Lam — lam.md 2-1·2-2, Q4 FY26 콜(Yahoo https://finance.yahoo.com/markets/stocks/articles/lam-research-corp-lrcx-q4-050153347.html ), FY2025 콜 요약(Investing.com https://www.investing.com/news/transcripts/earnings-call-transcript-lam-research-q4-2025-beats-expectations-stock-rises-93CH-4161532 ). AMAT — TIKR https://www.tikr.com/blog/applied-materials-30-systems-outlook-is-the-headline-the-services-business-may-be-the-better-story , AMAT 블로그 https://www.appliedmaterials.com/us/en/blog/blog-posts/subscription-services-provide-increased-value-to-chipmakers.html , Q3 FY26 콜 요약(Yahoo https://finance.yahoo.com/markets/stocks/articles/applied-materials-q3-earnings-call-220405111.html ). TEL — FY2025·FY2026 발표(1-3), 설치기반 matrixbcg https://matrixbcg.com/blogs/how-it-works/tel (2차 블로그, 신뢰도 낮음).
- AMAT AGS 분기 영업이익률 29.2%(Q2), 전년 대비 300bp+ 상승 [추정] (TIKR 요약). Lam·TEL의 서비스 부문 이익률은 별도 공시가 없어 확인 불가.

### 6-2. 왜 서비스가 중요한가 [해석]

1. **사이클 완충**: Lam FY2024(매출 −14.5%)에 Systems는 −17% [계산: 10.70→8.92]였지만 CSBG는 −11% [계산: 6.73→5.98]에 그쳤습니다. TEL FY2024는 매출 −17%였는데 FS는 약 −10%(4,740→4,286억 엔, [충돌] 반영)였습니다. 서비스는 다운턴의 하락폭을 절반 가까이 줄입니다.
2. **설치기반 = 미래 매출의 담보**: 장비 1대를 팔면 10년 이상 부품·서비스·업그레이드가 따라옵니다. 그래서 "출하 대수(설치기반 증가 속도)"가 서비스 매출의 선행지표입니다. 3사 설치기반이 모두 수만~10만 단위로 커져 있어, 이제 **신규 장비 매출의 변동성보다 서비스의 안정성이 밸류에이션을 지지**하는 단계입니다.
3. **업그레이드는 서비스와 장비의 중간**: Lam CSBG 성장의 핵심이 업그레이드라는 점은 중요합니다. 고객이 새 팹을 짓지 않고도 기존 장비를 개조해 200단+ NAND로 전환하면, 그 매출은 Systems가 아니라 CSBG로 잡힙니다. 즉 Lam CSBG의 일부는 **경기 민감형**입니다. 반대로 AMAT은 다년 구독이 2/3 이상이라 **계약형 비중**이 높습니다. 같은 "서비스"라도 질이 다릅니다.
4. **데이터·AI 서비스로의 진화**: AMAT AIx(연결 챔버 3만7천+), Lam Equipment Intelligence·Dextro는 서비스의 단가를 "사람 시간"에서 "수율·가동률 개선 가치"로 옮기려는 시도입니다. 이것이 성공하면 서비스 마진이 구조적으로 오릅니다.
5. **중국 리스크와의 관계**: 수출규제는 신규 장비뿐 아니라 일부 **부품·서비스 제공**까지 막습니다(AMAT 8-K 2025-09-29: "certain parts and services"). 중국에 깔린 대규모 설치기반의 서비스 매출이 규제 범위에 들어가면, 서비스 사업의 "안정성" 논리도 지역별로 다르게 봐야 합니다.

### 6-3. 3사 비교표 ⑥ 서비스

| 항목 | Lam | AMAT | TEL |
|---|---|---|---|
| 서비스 비중 | 가장 높음(36~40%) | 중간(약 23%) | 중간(약 22~26%) |
| 성장 질 | 업그레이드 주도(경기 연동 성분 큼) | 구독 주도(계약형) | 가동률·개조 주도 |
| 공시 투명성 | 분기 CSBG 금액 공개 | 세그먼트 보고(AGS 이익 포함) | FS 금액 공개, 이익 미공개 |
| 장기 목표 | 정성(설치기반 대비 초과 성장) | 정량(mid-teens) | 확인 불가 |

---

## 7. WFE 시장 맥락

### 7-1. 시장 규모(정의 차이에 주의)

| 연도 | 수치 | 정의 | 태그 / 출처 |
|---|---|---|---|
| 2024 | $117.1B | SEMI, **전체 반도체 장비**(WFE + 테스트 + 조립·패키징) 실적 | [확정] SEMI https://www.prnewswire.com/news-releases/semi-reports-global-semiconductor-equipment-billings-reached-135-billion-in-2025-up-15-year-on-year-302735003.html , Semiconductor Digest |
| 2025 | **$135.1B**(+15%) | SEMI 전체 장비 실적. 중국 $49.3B(−0.5%), 대만 $31.5B(+90%) | [확정] SEMI(PRNewswire), I-Connect007 https://iconnect007.com/article/149534/semi-reports-global-semiconductor-equipment-billings-reached-135-billion-in-2025-up-15-yoy/149531/ein |
| 2025 | $115.7B(+11%) | SEMI **WFE 세그먼트 전망**(2025년 중 발표) | [추정] SEMI https://www.semi.org/en/semi-press-release/semi-reports-global-total-semiconductor-equipment-sales-forecast-to-reach-125.5-billion-dollars-in-2025 |
| 2025 | $143B(+12%) | Counterpoint, **WFE 벤더 매출(시스템+서비스 포함)**. 상위 5사 $114B(+14%) | [추정] Counterpoint https://counterpointresearch.com/en/insights/WFE-Revenue-Up-12-percentage-YoY-in-2025-Driven-by-Increased-Memory-Advanced-Node-Foundry-Investments , Electronics Weekly https://www.electronicsweekly.com/news/business/2025-wafer-fab-equipment-vendor-revenue-up-12-2026-04/ |
| 2026 | **[충돌]** SEMI 전망 $139B / $145B / $165.9B(발표 시점별) | SEMI 전체 장비 | [충돌] SEMI https://www.semi.org/en/semi-press-release/global-total-semiconductor-equipment-sales-forecast-to-reach-a-record-of-dollar-139-billion-in-2026-semi-reports , everythingpe https://www.everythingpe.com/news/details/10720-semi-forecasts-record-165-9-billion-semiconductor-equipment-market-in-2026 |
| 2026 | Lam: WFE "low-$150B"(2026-07, 기존 $135~140B에서 상향) | 회사 정의 WFE | [확정] Seeking Alpha https://seekingalpha.com/news/4621252-lam-research-projects-8_1b-september-quarter-revenue-with-wfe-seen-in-low-150b-range , Yahoo https://finance.yahoo.com/technology/ai/articles/lam-research-lifts-2026-wfe-180229282.html |
| 2026 | TEL: WFE $150B 초과, 2027년 $190B 초과 가능성 언급 | 회사 정의 | [추정] Alpha Spread 요약 https://www.alphaspread.com/security/tse/8035/investor-relations/earnings-call/q4-2026 |
| 2026 | AMAT: 반도체 장비 사업 CY2026 +30% 이상 | 성장률만 제시 | [확정] amat.md 2-1 |
| 2026 | Goldman Sachs $150B, BofA $156B | 증권사 WFE | [추정] KuCoin 요약 https://www.kucoin.com/news/flash/goldman-sachs-upgrades-wfe-forecast-to-1-5-trillion-by-2026-dram-and-foundry-drive-growth |
| 2027 | SEMI 전체 장비 $156B 전망(이전 발표) | SEMI | [추정] https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports |

- [해석] **"WFE 규모"는 정의에 따라 $115B~$143B(2025)로 30% 가까이 차이**납니다. SEMI WFE는 장비 출하만, Counterpoint는 벤더 매출(서비스 포함), 회사 가이던스는 각자 정의입니다. 원고에서는 반드시 "누구의 어떤 정의인지"를 같이 써야 합니다. 2026년은 정의와 무관하게 **20~30% 성장, $150B 안팎이 업계 합의**입니다.

### 7-2. 상위 5개 벤더 순위와 점유율

| 순위(2025) | 회사 | 근거 | 태그 |
|---|---|---|---|
| 1 | ASML | Counterpoint·Castellano·CINNO 모두 1위 | [확정] |
| 2 | Applied Materials | 같음. 국내 보도도 "세계 2위" | [확정] |
| 3 | Lam Research | Counterpoint 순서(ASML, AMAT, Lam, TEL, KLA) | [확정] Counterpoint + Castellano |
| 4 | Tokyo Electron | 같음 | [확정] |
| 5 | KLA | 같음 | [확정] |

**점유율 수치는 출처마다 다름 [충돌]**
- Castellano: ASML이 2025년 **WFE의 21.2%** (같은 저자 헤드라인은 "거의 25%"). 2025년 Lam·KLA·ASML은 점유율 확대, **AMAT·TEL은 각자 SAM 내 점유율 하락** [추정] https://drrobertcastellano.substack.com/p/asml-maintains-1-semiconductor-equipment , https://drrobertcastellano.substack.com/p/applied-materials-lost-share-across
- Counterpoint(2025 상반기): 매출 성장률 ASML +35%, Lam +29%, KLA +26%, TEL +12%, AMAT +7% [추정] https://counterpointresearch.com/en/insights/top-five-wfe--manufacturers-q2-2025-performance
- CINNO(2025 상반기): 상위 10사 반도체 장비 매출 $64B+(+24%), ASML 약 $17B(+38%), AMAT $13.7B(+7%) [추정] https://www.webull.com/news/13521455135785984
- TEL 점유율 "약 15%(매출 약 200억 달러)" 같은 추정치는 tel.md 2-2 참조(신뢰도 중간). Lam "WFE의 9.9%(2024)"라는 블로그 수치(patentpc)는 Lam 매출 규모와 맞지 않아 **사용하지 않음**.
- 공정별 점유율(식각 Lam 45~50%, 증착 AMAT 약 40% 등)은 리서치 회사마다 범주가 달라 수치 인용을 권하지 않습니다(lam.md 2-5, tel.md 2-2와 같은 결론).

### 7-3. 회사별 SAM 주장

| 회사 | 주장 | 태그 / 출처 |
|---|---|---|
| Lam | SAM이 WFE의 low-30% → high-30%(decade 말), Investor Day 목표보다 빠르게 진행. NAND 웨이퍼당 SAM 128단 대비 500단+에서 2배 | [확정] 4-1 |
| AMAT | 선단 로직·DRAM·첨단 패키징이 2026~27 WFE 성장의 약 80%이고 이 분야 리더. 정량 SAM 비중 공시는 확인 불가 | [확정] 4-2 |
| TEL | 코터/디벨로퍼 90%+(EUV용 100%), 4대 제품(코터/디벨로퍼·식각·증착·세정)이 제품 매출의 95%. FY2027 코터/디벨로퍼 +50%, 식각 +30%, 첨단 패키징 +60% 전망 | [확정/추정 혼재] tel.md 2-2·2-3 |

- [해석] **2025년 점유율 승자는 "리소그래피 연관(ASML·TEL 트랙)"과 "식각·증착 중 메모리 고단화(Lam)"**였고, AMAT은 중국 비중 하락과 로직 편중으로 상대적 부진이었습니다. 2026년에는 DRAM·HBM·패키징이 AMAT의 강점 분야라 반전 여지가 있습니다(AMAT DRAM 비중 26%, 패키징 +70% 전망).

### 7-4. 3사 비교표 ⑦ 시장 포지션

| 항목 | Lam | AMAT | TEL |
|---|---|---|---|
| 2025 순위 | 3위 | 2위 | 4위 |
| 2025 점유율 방향(Castellano) | 확대 | 하락 | 하락 |
| 2025 상반기 성장률(Counterpoint) | +29% | +7% | +12% |
| 2026 WFE 견해 | low-$150B | 장비 +30%+ | $150B+ |
| 강점 SAM | 식각(특히 NAND 고종횡비, conductor etch), 증착(ALD Mo) | 증착·CMP·이온주입·계측의 통합, 패키징 | 코터/디벨로퍼 독점, 열처리, 세정, 식각 추격 |

---

## 8. 한국 전략

### 8-1. 회사별

| 항목 | Lam | AMAT | TEL |
|---|---|---|---|
| 본사 기준 한국 매출(최근 연도) | FY2026 약 19% → 약 $4.4B [계산: 23.23 × 0.19] | FY2025 $5.61B(19.8%) | FY2026 22.3% → 약 ¥545B [계산: 2,443.5 × 0.223] |
| 한국 매출 추세 | 27%(FY21) → 19%(FY26) 하락 | 22%(FY21) → 17%(FY22~24) → 19.8%(FY25) | 약 17%(FY25) → 22.3%(FY26) 상승 |
| 한국 법인 매출(2025, 국내 기준) | 램리서치코리아 1조 4,643억 원 / 매뉴팩춰링코리아 1조 9,775억 원 / 코리아테크놀로지 1,563억 원 [추정] | 1조 5,564억 원(+17.1%), 영업이익 2,817억 원 [추정] | 1조 5,288억 원 [추정] |
| 한국 인력 | 약 1,720명(2024-09, 전자신문) [추정] | **[충돌]** 약 2,200명(공식 페이지) vs 약 1,450명 | **[충돌]** 약 1,722명(내부) vs 2,173명(사람인) |
| 한국 R&D | 용인 KTC(2022-04 개관, 약 3만㎡, 증착·식각 클린룸) | 오산 Applied Collaboration Center(건설 중, 장비 20대+, 연구인력 100명+ 계획), EPIC 연계 | TTCK(2012), TTCK-2(화성, 2024-10), TTCK-Y(용인, 2027-01 목표) |
| 한국 제조 | **있음**: 램리서치매뉴팩춰링코리아(용인), 코리아테크놀로지 | 확인 불가(지원·서비스 중심) | **있음**: 발안 공장(화성) |
| 용인 클러스터 | 기흥 지곡 일반산단(KTC·본사). 원삼 클러스터 직접 입주는 확인 불가 | 원삼 협력화단지 13,305㎡ 필드오피스(2026-07-06 협약) | 원삼 일반산단 TTCK-Y + 제2용인테크노밸리 부지 5만3,292㎡ 매입 |
| 현지 공급망 | 2025년 국내 협력사 조달 1조 원 돌파(2026-02 발표) | 확인 불가(정성 서술만) | 국내 협력사 약 160곳 활용(니케이) |
| 한국 고객 R&D 협력 | 확인 불가(공개된 공동 R&D 프로그램 없음) | Samsung(2026-02), SK hynix(2026-03) EPIC 파트너 | 확인 불가 |
| 한국 대표 | 박준홍(2024-01~) | 박광선 | 노태우(2025-04~) |

- 출처: 각 팩 3장(lam.md 3-1~3-4, amat.md 3-1~3-3, tel.md 3-1~3-4). 용인 4대 장비사 정리: 이투데이 https://www.etoday.co.kr/news/view/2600799 , 블로터 https://www.bloter.net/news/articleView.html?idxno=667425 , 글로벌이코노믹 https://www.g-enews.com/article/General-News/2026/07/202607071107265946d6b0ab7f1c_1 , 네이트 https://m.news.nate.com/view/20260706n31755 . ASML 원삼 사무소(2024-12) 전자신문 https://www.etnews.com/20241212000003
- **[충돌] Lam 용인 R&D 시점**: 2026-07 용인시 관련 보도는 "램리서치는 지난해 8월 지곡 일반산단에 한국 R&D센터를 이전했다"고 썼으나, 다수 보도는 KTC 개관을 2022-04-26로 기록합니다(lam.md 3-2). 2025-08은 본사 이전 등 다른 사건일 수 있어 원문 확인이 필요합니다.
- [해석] **한국 법인 매출(원화) ≠ 본사의 한국 매출(달러/엔)**입니다. 본사 한국 매출은 고객 소재지 기준이고, 한국 법인 매출은 법인 간 거래·서비스 수수료 등 구조에 따라 달라집니다. Lam은 한국에 제조 법인이 있어 법인 매출 합계(약 3.6조 원 [계산])가 본사 한국 매출(약 $4.4B)과 비슷한 규모로 나오지만, 이는 제조 법인이 **수출용 부품·모듈을 만드는 매출**을 포함하기 때문으로 보입니다(추론).

### 8-2. 3사 한국 전략 비교 [해석]

| 축 | Lam | AMAT | TEL |
|---|---|---|---|
| 전략 유형 | **"제조·R&D 현지화형"**: 한국을 고객지원 거점이자 생산 거점으로 활용, 국내 조달 1조 원 | **"고객 공동개발형"**: 한국 고객을 실리콘밸리 EPIC로 끌어들이고, 한국에는 연계 R&D 허브(오산) | **"고객 밀착 R&D·데모 팹형"**: 고객 양산 팹과 같은 구조의 TTCK-Y를 클러스터 안에 짓는 방식 |
| 강점 | 공급망 깊이, 메모리(NAND) 레거시 관계 | 최고경영진 단위 파트너십(Samsung·SK hynix EPIC 창립 파트너) | 클러스터 내 물리적 근접, 한국 매출 비중 상승 |
| 약점/리스크 | 한국 매출 비중 장기 하락 | 국내 제조 기반 확인 불가 | TSMC 2nm 영업비밀 사건(tel.md) 등 컴플라이언스 평판 |

- [해석] **용인 클러스터는 3사 모두의 2027~2030년 핵심 전장**입니다. SK hynix 용인 Y1·Y2 및 청주 M17(2027~2029 클린룸 오픈, lam.md 3-3)에 장비가 들어가는 시점에, TEL은 TTCK-Y(2027-01)로 가장 가까이 R&D를 붙이고, AMAT은 필드오피스로 서비스 거점을 확보했습니다. Lam은 기흥 지곡의 기존 KTC·제조 거점으로 대응합니다. **"누가 가장 먼저, 가장 가까이"의 경쟁**이라는 점에서 TEL이 물리적으로 앞서 있습니다.

---

## 9. 종합: 전략적 함의 요약 [해석]

1. **사이클 국면**: 3사 모두 2026년 사상 최대 실적 구간이지만 동력이 다릅니다. Lam은 NAND 업그레이드와 식각 점유율, AMAT은 DRAM·패키징·서비스, TEL은 EUV 코터/디벨로퍼와 식각 추격입니다.
2. **마진의 갈림**: Lam은 2028 목표를 조기 달성 중(OPM 35%), AMAT은 29~30% 정체를 막 벗어나는 중, TEL은 35% 목표와 약 9%p 간극이 남았습니다.
3. **중국 → AI 전환**: 3사 모두 FY2024 전후 중국 정점(37~44%) 이후 30%대 중반으로 내려왔고, 대만·한국이 대체했습니다. 2026-11-09 Affiliates Rule 유예 만료가 다음 변수입니다.
4. **고객 집중 심화**: 특히 Lam(10% 이상 고객 4곳, 합계 약 55%). 한국 고객(Samsung)은 3사 모두에서 10% 이상 고객입니다.
5. **서비스의 질**: Lam(업그레이드형) vs AMAT(구독형) vs TEL(가동률형). 같은 "서비스 매출"도 경기 민감도가 다릅니다.
6. **R&D의 팹화**: EPIC $5B, Lam 랩 $3B+, TEL TTCK/개발동. 장비사가 "고객보다 먼저 공정을 개발"하는 구조로 바뀌고 있습니다.
7. **한국**: 매출 비중은 3사 모두 약 20%로 수렴했지만, 전략 유형은 제조 현지화(Lam) / 공동개발(AMAT) / 클러스터 밀착 R&D(TEL)로 갈립니다.

## 10. 확인 불가·후속 확인 목록

- 모든 SEC/TEL 원문 표 대조(WebFetch 차단). 특히 Lam FY2021~22 OPM, FY2024 GM, TEL FY2021~23 GM.
- Lam FY2025 연간 Memory/Foundry/Logic 비중, FY2021 지역 비중(대만 이하).
- AMAT FY2025 10% 고객 이름 매칭(19%·15%), FY2023 TSMC 비중, FY2021~24 일본·미국 비중.
- TEL FY2022~24 한국·대만 비중, FPD 세그먼트 매출, 10% 이상 고객의 연도별 추이, FY2024 FS 금액([충돌]), 자사주 결의일([충돌]).
- AMAT의 최근(2024~26) 공식 재무 목표 모델 존재 여부.
- TEL 차기 중기경영계획(FY2028~) 발표 여부. "VISION2030"은 TEL이 아니라 TED의 계획임.
- Lam CSBG "2028년까지 2배 이상" 발언의 원문 확인.
- AMAT 한국 공급망 조달 규모, AMAT 한국 내 제조 여부.
- 3사 서비스 부문 이익률(AMAT AGS 외 미공시).

## 11. 출처 목록(본문 링크 외 핵심 묶음)

**Lam Research**
- 10-K FY2021~FY2026: 1-1 표 아래 링크
- Investor Day 2025: https://filecache.investorroom.com/mr5ir_lamresearch2/1435/Lam%20Research%202025%20Investor%20Day%20FINAL.pdf · https://quartr.com/events/lam-research-corporation-lrcx-investor-day-2025_33D7JGMm
- Q4 FY2026: https://www.fool.com/earnings/call-transcripts/2026/08/07/lam-research-lrcx-q4-2026-earnings-call-transcript/ · https://www.investing.com/news/transcripts/earnings-call-transcript-lam-research-posts-record-q4-2026-results-stock-rebounds-93CH-4821978 · https://finance.yahoo.com/markets/stocks/articles/lam-research-corp-lrcx-q4-050153347.html
- 자본배분: https://www.prnewswire.com/news-releases/lam-research-corporation-announces-a-27-increase-in-quarterly-dividend-302862122.html · https://uk.finance.yahoo.com/news/lam-research-returns-5b-shareholders-134200568.html
- 랩 투자: https://newsroom.lamresearch.com/2026-08-13-Lam-Research-Announces-Plans-to-Invest-More-than-3B-to-Expand-Global-Lab-Network,-Increase-Innovation-Velocity-in-the-AI-Era

**Applied Materials**
- 8-K FY2021~FY2024, 10-K FY2022~FY2025: 1-2·2-1·3-1 링크
- Kokusai: https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-termination-kokusai-electric/
- 2021 Investor Meeting: https://investor.appliedmaterials.com/news-releases/news-release-details/applied-materials-showcases-unique-capabilities-accelerate
- Q3 FY2026: https://www.investing.com/news/transcripts/earnings-call-transcript-applied-materials-beats-q3-2026-estimates-shares-fall-93CH-4859444 · https://ir.appliedmaterials.com/static-files/9d5d182d-f060-4b22-a32c-4582257fdc9b
- 투자: https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-expands-singapore-manufacturing-support-ai · https://technode.global/2026/09/18/applied-materials-5b-india-semiconductor-investment/

**Tokyo Electron**
- 중기계획: https://www.tel.com/news/ir/2022/20220608_001.html · Q&A https://www.tel.com/ir/policy/mplan/qa_2022.html
- IR Day 2025: https://www.tel.com/ir/policy/mplan/i9nanv00000000ga-att/20250226_TELIRDay_E_rev.1_slide_r3.pdf
- 결산: 1-3 표 아래 링크
- 고객: https://www.postation.jp/news/tsmc-japan-chip-equipment-customers
- 자사주: https://www.marketscreener.com/news/tokyo-electron-limited-announces-an-equity-buyback-for-7-500-000-shares-representing-1-64-for-150-ce7f5ddbdf8df027

**시장**
- SEMI 2025 실적: https://www.prnewswire.com/news-releases/semi-reports-global-semiconductor-equipment-billings-reached-135-billion-in-2025-up-15-year-on-year-302735003.html
- Counterpoint 2025: https://counterpointresearch.com/en/insights/WFE-Revenue-Up-12-percentage-YoY-in-2025-Driven-by-Increased-Memory-Advanced-Node-Foundry-Investments
- Castellano: https://drrobertcastellano.substack.com/p/asml-maintains-1-semiconductor-equipment
- BIS Affiliates Rule 유예: https://www.federalregister.gov/documents/2025/11/12/2025-19846/one-year-suspension-of-expansion-of-end-user-controls-for-affiliates-of-certain-listed-entities
