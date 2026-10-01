# 3사 기술 변곡점·경쟁 포지셔닝 분석 — Lam Research / Applied Materials / Tokyo Electron

> 용도: 「3사 기업분석·사업전략·기술분석집」의 **기술전략 파트** 원재료. 장비 동작 원리는 별도 장비 심층편이 있으므로 여기서는 1~3줄만 쓰고, "어떤 기술 전환이 오고 → 어떤 공정·장비 수요가 바뀌며 → 3사 중 누가 어디에 서 있는가"에 집중했다.
> 기준일: 2026-10-01
> 일관성: 같은 폴더의 lam.md(4장), amat.md(4장), tel.md(4장)의 제품명·태그를 그대로 따랐다. 충돌 시 이 문서에 [충돌]로 별도 표기.

## 읽는 법 · 태그 · 조사 한계

| 태그 | 의미 |
|---|---|
| [확정] | 회사 공식 보도자료·IR·실적콜 원문 인용이 검색 결과에 직접 나타나고, 2개 이상 출처가 일치 |
| [추정] | 출처 1건, 2차 요약(애널리스트 블로그·뉴스 요약), 또는 수치 원문 미확인 |
| [충돌] | 출처끼리 수치·사실이 다름. 어느 쪽인지 병기 |
| [해석] | 작성자의 분석·전략적 함의. 사실이 아님 |
| 확인 불가 | 이번 조사로 찾지 못함 |

**조사 한계(중요):** WebFetch는 네트워크 정책으로 **전부 차단**됐다(yolegroup.com, fool.com, ir.appliedmaterials.com, tel.com 시도 → EGRESS_BLOCKED). 따라서 이 문서의 모든 사실은 **WebSearch 결과 요약**에 근거한다. 원문 PDF·트랜스크립트를 직접 읽지 못했으므로, 회사 공식 수치라도 단일 요약에만 나온 것은 [추정]으로 낮췄다. 전략집 최종본에 숫자를 넣기 전에 IR 원문 대조를 권장한다.

**용어:** WSPM = 월 웨이퍼 투입(wafer starts per month). SAM = 회사가 공략 가능한 시장(Served Available Market). WFE = 전공정 장비 시장. POR/TOR = 고객 양산 표준 채택(Process/Tool of Record). HVM = 대량 양산.

---

## 0. 한 장 요약 — 8대 기술 변곡점과 3사 포지션

| # | 변곡점 | 장비 수요에서 커지는 것 | 수혜 1순위(주장 기준) | 도전·견제 | 한국 고객 관련성 | HVM 시점 |
|---|---|---|---|---|---|---|
| 1 | GAA(2nm 이하) | 선택적 식각·등방성 식각, ALD(메탈게이트), Epi, eBeam 계측 | AMAT(증착·Epi·계측 폭), Lam(도체식각 Akara·금속증착) | TEL(게이트·등방성 식각 확대 주장) | 삼성 파운드리 SF2 | 2025~2026 진행 중 |
| 2 | 후면전력(BSPDN) | 웨이퍼 본딩·박막화·후면 CMP/식각·나노 TSV·계측 | AMAT(배선·계측), Lam(+$1B SAM/100k 주장) | TEL(본더·레이저 리프트오프), EVG(본더) | 삼성 SF2Z | Intel 18A 2025~, TSMC A16 2026 말, 삼성 2027~ |
| 3 | 3D NAND 고단화 | 채널홀 HAR 식각(극저온), 몰리브덴 워드라인, 웨이퍼 본딩 | Lam(채널홀 사실상 독점, Mo ALD 선점) | **TEL(극저온 식각·Mo 배치 증착으로 정면 도전)** | 삼성 V10(400단대), SK하이닉스 321→375단 | 업그레이드 2026~2027, 400단대 2027~ |
| 4 | DRAM 4F²/3D·HBM | HAR 식각·증착, 신소재(IGZO), TSV·도금·CMP·본딩 | Lam(Akara·TSV·도금), AMAT(패키징 풀셋), TEL(커패시터 식각 POR) | 3사 모두 경쟁 | 삼성 10a(2028 목표), SK 10b | 4F² 2027~2028, 3D DRAM 2030대 |
| 5 | 첨단 패키징 | 하이브리드 본딩, ECD, CMP, 갭필 증착, 프로버 | AMAT(Kinex+Besi), Lam(ECD·TSV), TEL(본더·LLO·프로버) | 한미·ASMPT(TCB), EVG(W2W) | SK하이닉스·삼성 HBM | HB는 HBM5 이후로 지연 [충돌] |
| 6 | 리소 인접 | EUV 트랙·레지스트, 패턴 셰이핑 | TEL(트랙 90%+) | Lam Aether(드라이 레지스트), AMAT Sculpta | SK하이닉스(Aether 채택 보도), 삼성 High-NA | High-NA 2027~ 양산 적용 |
| 7 | 소재 전환 | Mo ALD/CVD, Ru/Co 라이너, low-k | Lam(Mo ALD), AMAT(RuCo·Black Diamond) | TEL(Mo 배치), ASM·Kokusai | SK하이닉스 375단 Mo | NAND 2026~, 로직 2nm~ |
| 8 | 팹 자동화·AI 서비스 | 원격·예측 정비, 코봇, 디지털 트윈 | Lam(Dextro·EI), AMAT(AIx·구독형 AGS) | TEL(Epsira·NVIDIA 협업) | 국내 FSE/CE 업무 변화 | 이미 진행 |

[해석] 한 줄로 요약하면: **Lam은 "3D 수직화(식각·증착 강도)"에, AMAT는 "재료공학+패키징+계측의 폭"에, TEL은 "리소 트랙 독점을 기반으로 식각·본딩에서 점유율 탈환"에 베팅**하고 있다. 2026~2027년의 최대 격전지는 **3D NAND 채널홀 극저온 식각과 Mo 증착(Lam vs TEL)**, 그리고 **HBM 본딩(AMAT·Besi vs TCB 진영)**이다.

---

## 1. GAA(나노시트, 2nm 이하) · 포크시트/CFET 전망

### (a) 기술 변화
- 핀(FinFET) 대신 Si/SiGe 적층 나노시트를 게이트가 사방에서 감싼다. SiGe를 선택적으로 빼내고(측면·등방성 식각) 그 틈에 high-k/메탈게이트를 ALD로 채운다. [해석, 일반 공학]
- 다음 단계: **포크시트**(n/p 시트 사이 유전체 벽) → **CFET**(n/p를 수직 적층). imec은 포크시트를 A10(1nm급)~A7, CFET를 A7부터로 제시했고 A7 시점은 2031→2033으로 늦춰지는 흐름이다. [추정] 출처: [Tom's Hardware imec 2026 로드맵](https://www.tomshardware.com/tech-industry/semiconductors/imecs-2026-roadmap-details-0-3nm-nodes-by-2038-cfet-transistors-become-viable-at-0-7nm-company-redefines-moores-law-as-cell-sizes-gain-importance-for-density), [imec outer wall forksheet](https://www.imec-int.com/en/articles/outer-wall-forksheet-bridge-nanosheet-and-cfet-device-architectures-logic-technology)

### (b) 장비 수요 변화
- **식각·증착 강도 상승**: "GAA를 도입하면 업계가 까는 10만 WSPM당 Lam SAM이 **$1B** 늘어난다(식각·증착 강도 때문)". 금속 증착 SAM/웨이퍼는 약 **3배**. [추정] 출처: [Investing.com – Lam @ Morgan Stanley](https://www.investing.com/news/transcripts/lam-research-at-morgan-stanley-conference-strategic-growth-in-focus-93CH-4539702), [Quartr Lam Investor Day 2025](https://quartr.com/events/lam-research-corporation-lrcx-investor-day-2025_33D7JGMm)
- AMAT도 "선단 GAA 노드 10만 WSPM당 **약 $1B 증분 매출**, 주로 증착·식각"이라고 제시. [추정] 출처: [LongYield – AMAT and the Angstrom Age](https://longyield.substack.com/p/applied-materials-and-the-angstrom), [Investing.com AMAT](https://www.investing.com/news/company-news/applied-materials-advances-chip-performance-with-new-materials-93CH-3509902)
  - [해석] 두 회사가 "10만 WSPM당 $1B"라는 같은 숫자를 쓰지만 **각자의 SAM 기준**이라 합산·비교 불가. "GAA가 식각·증착 장비 수요를 키운다"는 방향성만 인용할 것.
- 수요가 커지는 공정: 선택적/등방성 식각, 도체 식각(게이트), 메탈게이트 ALD, S/D Epi, 저저항 콘택(Mo), eBeam 계측(3D 구조 내부 측정). 상대적으로 리소 단계 비중은 정체. [해석] 근거: AMAT "materials engineering, rather than lithography alone, is becoming the primary lever" (amat.md 4-2 ①, [Converge Digest](https://convergedigest.com/applied-materials-targets-2nm-gaa-nodes-with-new-deposition-systems/))

### (c) 3사 포지션
| 회사 | 제품·주장 | 태그 / 출처 |
|---|---|---|
| **AMAT** | 2026.2 Viva Radical Treatment, Sym3 Z Magnum(도체식각), Spectral ALD(Mo 콘택) / 2026.4 Endura Trillium ALD(메탈게이트), Producer Precision Selective Nitride PECVD / PROVision 10(GAA·BSPDN용 eBeam). "multiple leading foundry-logic manufacturers" 사용 중 | [확정] amat.md 4-1 공통 출처([AMAT IR 2026.2](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-unveils-transistor-and-wiring-innovations/), [StockTitan 2026.4.8](https://www.stocktitan.net/news/AMAT/applied-materials-introduces-deposition-systems-for-angstrom-era-7v0938tplllx.html)) |
| AMAT 목표 | "GAA와 배선(후면전력 포함)에서 served market의 **50% 이상** 확보 궤도" (Q1 FY26 콜) | [추정] 검색 요약. 출처: [AMAT Q1 FY26 실적 8-K](https://www.sec.gov/Archives/edgar/data/6951/000162828026007661/exhibit991q12026earningsre.htm) 및 [fool.com Q1 2026 transcript](https://www.fool.com/earnings/call-transcripts/2026/02/12/applied-materials-amat-q1-2026-earnings-transcript/) |
| AMAT 실적 | Q3 FY26 반도체시스템 매출 $7.04B(+27% YoY), "GAA·FinFET 증설이 파운드리로직 사상 최대 견인" | [확정] [AMAT Q3 FY26 Prepared Remarks](https://ir.appliedmaterials.com/static-files/e9985149-77c2-4cf3-aaad-a579178cbfe4), [Q3 FY26 보도자료](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-third-quarter-2026-results) |
| **Lam** | Akara(도체식각, DirectDrive, 2025.2 출시) → Q4 FY26 콜: "2nm 이하 GAA 로직과 첨단 DRAM에서 여러 전략적 TOR 확보, 출시 후 설치 대수 매년 2배" | [확정] [Yahoo – Lam Q4 call highlights](https://finance.yahoo.com/technology/articles/lam-research-q4-earnings-call-230406093.html), lam.md 4-1 |
| Lam 목표 | 신규 구조(3D NAND·3D DRAM·GAA·BSPDN)가 만드는 **증분 SAM의 50% 이상** 점유, SAM을 WFE의 low-30%→decade 말 high-30%로 | [추정] [Quartr](https://quartr.com/events/lam-research-corporation-lrcx-investor-day-2025_33D7JGMm) |
| **TEL** | "2nm 로직에서 처음 채택된 GAA 구조로 **게이트 식각·등방성(isotropic) 식각** 사업기회 확대". FY2027 식각 매출 +25~30% 전망(고종횡비 콘택·인터커넥트·GAA) | [추정] [Investing.com TEL Q4 FY26 transcript](https://www.investing.com/news/transcripts/earnings-call-transcript-tokyo-electron-q4-2026-beats-estimates-stock-surges-93CH-4654441), [ninescrolls](https://ninescrolls.com/news/tokyo-electron-posts-record-jpy-2-44-trillion-fy2026-guides-first-half-fy2027) |
| TEL 기타 | Certas LEAGA(가스 화학 식각, 등방성) — 제품군 존재만 확인. GAA 전용 POR 공개 수치 확인 불가 | [추정] tel.md 4-2 |

### (d) 한국 고객
- 삼성 파운드리 SF2(2nm GAA): Exynos 2600 양산(2025.9 시작 보도), 수율 약 50~60% 추정 보도, 2세대 SF2P 준비. [추정] 출처: [TrendForce 2025.12.19](https://www.trendforce.com/news/2025/12/19/news-samsung-officially-unveils-exynos-2600-industry-first-2nm-gaa-ap-with-113-ai-performance-uplift), [TechPowerUp](https://www.techpowerup.com/345239/samsung-foundry-supposedly-achieves-50-yields-with-2-nm-gaa-node-process) — 수율 수치는 보도마다 30~60%로 [충돌]
- SK하이닉스는 로직 파운드리가 없어 GAA 직접 수요는 없음. 단 Akara·Sym3 등 도체식각 장비는 DRAM에도 같이 쓰인다(위 Lam·AMAT 발표). [해석]

### (e) 타임라인
- TSMC N2·삼성 SF2·Intel 18A(RibbonFET)가 2025~2026 양산. 포크시트 2030 전후(A10), CFET 2031~2033(A7) 이후. [추정] 위 imec 출처

### (f) [해석] 전략적 함의
- **AMAT**: GAA는 "리소보다 재료공학"이라는 AMAT 정체성에 가장 잘 맞는 전환. Epi·ALD·선택식각·eBeam까지 한 회사에서 묶어 파는 **통합 솔루션(co-optimization)** 이 무기. 리스크는 고객이 소수(TSMC·삼성·Intel)라 특정 고객 투자 지연에 민감.
- **Lam**: 로직은 전통적으로 메모리 대비 약했던 영역. Akara·금속 증착으로 "로직 점유율 확대"가 투자 스토리의 핵심이고, Q4 FY26 TOR 확보 발언이 그 진척 신호.
- **TEL**: GAA에서는 도전자. 다만 리소 트랙(EUV) 점유를 고객 접점으로 활용해 식각 POR을 늘리는 구도. CFET로 가면 웨이퍼 본딩 수요가 생겨(아래 2장) TEL 본더 사업에도 연결.

---

## 2. 후면전력공급(BSPDN / Backside Power Delivery)

### (a) 기술 변화
- 전원 배선을 웨이퍼 뒷면으로 옮겨 앞면을 신호 배선 전용으로 쓴다. 공정 흐름은 앞면 완성 → 캐리어 웨이퍼에 **영구 본딩** → 원래 기판을 수 μm까지 **박막화** → 후면 나노 TSV·배선 형성. [해석, 일반 공학]

### (b) 장비 수요 변화
- Lam: "BSPDN도 10만 WSPM당 **$1B 증분 SAM**". [추정] [Investing.com Morgan Stanley](https://www.investing.com/news/transcripts/lam-research-at-morgan-stanley-conference-strategic-growth-in-focus-93CH-4539702)
- AMAT: "BSPDN 도입으로 배선(wiring) 기회가 10만 WSPM당 $1B 더 늘어 약 **$7B**". [추정] [Investing.com/AMAT 검색 요약](https://www.investing.com/news/company-news/applied-materials-advances-chip-performance-with-new-materials-93CH-3509902), [AMAT Q4 FY24 프레젠테이션](https://ir.appliedmaterials.com/static-files/394e84d2-f6ff-4ffd-a4d7-4b95bfddda22)
- 새로 생기는 장비 수요: W2W 본더, 그라인딩/CMP/선택 식각(박막화), 레이저 리프트오프, 후면 정렬·오버레이 계측, 나노 TSV 식각·충진. 웨이퍼 휨(500μm 이상 가능)과 2~3nm 수준 왜곡 제어가 병목. [추정] 출처: [SEMIVISION substack note](https://substack.com/@semivision/note/c-333551781), [SemiEngineering – BSPDN fab tool barriers](https://semiengineering.com/backside-power-delivery-creates-fab-tool-thermal-dissipation-barriers/)

### (c) 3사 포지션
| 회사 | 포지션 | 태그 / 출처 |
|---|---|---|
| AMAT | PROVision 10 eBeam 계측을 "GAA and Backside Power Delivery architectures"용으로 출시. 배선·후면전력 served market 50%+ 목표(1장) | [확정] [AMAT IR Patterning](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-expands-patterning-solutions-portfolio) |
| Lam | +$1B SAM/100k WSPM 주장. 구체적 BSPDN TOR 공개 확인 불가 | [추정] 위 |
| TEL | **Ulucus LX**(Extreme Laser Lift Off, 2024.12): 영구 본딩 후 백그라인딩·폴리싱·화학식각을 대체, DI water 90%+ 절감 / **Synapse** 본더. tel.md는 Ulucus LX 용도를 "NAND CBA, 후면 전력 공급"으로 정리 | [추정] [TEL 뉴스 Ulucus LX](https://www.tel.com/news/product/2024/20241209_001.html), tel.md 4-5 |
| (기타) EV Group | W2W 본더 선두. "EVG 82%, TEL 17%"(웨이퍼 본딩), "W2W 하이브리드 본더 TEL 약 20%(Synapse Si)" | [추정] [SemiAnalysis – Austria's Silent Monopolies](https://newsletter.semianalysis.com/p/austrias-silent-monopolies-on-advanced) (작성 시점이 2026년 이전일 가능성, 최신 점유율 확인 불가) |

### (d) 한국 고객
- 삼성 SF2Z(2nm+BSPDN): 2027 리스크 생산, 2029 본격 양산이라는 보도. [추정] [Wikipedia/BSPDN 정리](https://en.wikipedia.org/wiki/Backside_power_delivery), [TrendForce 2024.5](https://www.trendforce.com/news/2024/05/09/news-gearing-up-for-backside-power-delivery-heated-tech-war-between-tsmc-intel-and-samsung/) — "2027 양산"으로 쓴 요약도 있어 [충돌]
- 메모리: BSPDN 자체는 로직 기술이지만 **같은 W2W 본딩·박막화 장비**가 NAND(CMOS bonded array)·3D DRAM에도 쓰인다. [추정] 위 SEMIVISION

### (e) 타임라인
- Intel 18A PowerVia: 2026 CES Panther Lake로 상용 / TSMC A16(Super Power Rail): 2026 말 양산 목표 / 삼성 SF2Z: 2027(리스크)~. [추정] 출처: [Wikipedia BSPDN](https://en.wikipedia.org/wiki/Backside_power_delivery), [fiisual](https://fiisual.com/blog/post/2026/bspdn-introduction)

### (f) [해석] 전략적 함의
- **TEL**에게 가장 "새 시장" 성격이 강하다. 본더·레이저·세정을 묶은 후면 공정 패키지를 팔 수 있고, 경쟁자는 EVG(본더)·Disco(그라인딩) 같은 비(非) 빅3 업체다.
- **AMAT**는 계측(eBeam)과 CMP·배선 증착에서 수혜. "BSPDN에서 계측이 새 병목"이라는 서사가 AMAT eBeam 사업에 유리.
- **Lam**은 나노 TSV 식각·금속 충진 쪽 수혜를 주장하지만 공개 TOR은 아직 확인되지 않음 → 전략집에서는 "주장 단계"로 표기.

---

## 3. 3D NAND 고단화 (200→300→400단+), 채널홀 HAR 식각, 극저온 식각, Mo 워드라인

### (a) 기술 변화
- 단수가 늘수록 채널홀이 깊어진다(10μm급). 극저온(cryogenic) 식각은 웨이퍼를 매우 낮은 온도로 유지해 측벽 반응을 억제하고 수직 식각 속도를 높인다. 워드라인 금속은 W→Mo(저항↓, 배리어 불필요)로 바뀐다. 셀·주변회로를 따로 만들어 붙이는 **웨이퍼 본딩(CBA)** 도 확산. [해석] lam.md 4-1, 4-4

### (b) 장비 수요 변화 (정량)
- Lam: **NAND SAM/웨이퍼가 128단 대비 500단+에서 2배**(Investor Day 1.8배에서 상향). **$40B NAND 업그레이드 기회** 유지, 200단 미만→200단 이상 전환이 **2027년 말까지** 완료될 것으로 앞당김. 업계 캐파의 약 2/3가 200단 미만이었다. [추정] 출처: [Globe and Mail – Lam Q4 FY26 transcript](https://www.theglobeandmail.com/investing/markets/stocks/LRCX/pressreleases/3729596/lam-research-lrcx-q4-2026-earnings-call-transcript/), [Yahoo – Lam lifts 2026 WFE outlook](https://finance.yahoo.com/technology/ai/articles/lam-research-lifts-2026-wfe-180229282.html)
- Lam Q4 FY26(6월 분기): 비휘발성 메모리가 시스템 매출의 **23%**(전 분기 12%), NAND 매출이 전 분기 대비 2배 이상, "256단 이상 전환 투자(주로 엔터프라이즈 SSD)". [확정] [TradingView/Zacks](https://www.tradingview.com/news/zacks:c6805a50a094b:0-lrcx-q4-earnings-beat-on-nand-and-customer-support-strength/), [Yahoo](https://finance.yahoo.com/markets/stocks/articles/lrcx-q4-earnings-beat-nand-155400014.html)
- TEL: **채널홀 식각 시장 약 $0.5B(CY2023) → 약 $2B(CY2027)**, 점유율 50% 가정 시 TEL 증분 매출 $1B. [추정] 출처: [Nomad Semi – TEL Deep Dive Part 2](https://www.nomadsemi.com/p/tokyo-electron-deep-dive-part-2), [Yole](https://www.yolegroup.com/industry-news/tokyo-electron-takes-aim-at-nand-etching-leader-lam-research/) (원문 미열람)
- Mo: SemiAnalysis 추정 — NAND용 Mo 증착 장비 매출 **2027년 $1B 초과, 2030년 연 약 $2B**(DRAM·로직 확산 포함), NAND 캐파 중 Mo 비중 2025년 한 자릿수 중반 → 2027년 약 30%. [추정] 출처: [Bitget – SemiAnalysis 요약](https://www.bitget.com/news/detail/12560605717420), [BigGo – Mo 장비 시장 $1B](https://finance.biggo.com/news/132af702-c5dc-4719-8ab2-93b4217e4825)
- 커지는 공정: HAR 유전체 식각(극저온), 몰드 스택 증착(산화막/질화막 PECVD), Mo ALD/CVD, Mo 선택 식각, 슬릿 식각, 웨이퍼 본딩. [해석]

### (c) 3사 포지션 — **Lam vs TEL 정면승부**
| 항목 | Lam | TEL | AMAT |
|---|---|---|---|
| 채널홀 극저온 식각 | 2019년부터 양산 투입된 유일 업체. NAND용 HAR 유전체 식각 챔버 **7,500대+ 중 약 1,000대가 극저온**. Cryo 3.0(2024.7): 10μm 깊이 CD 편차 0.1% 미만, 식각률 2배+, "1,000단 경로" [확정] [Lam Newsroom Cryo 3.0](https://newsroom.lamresearch.com/2024-07-31-Lam-Research-Introduces-Lam-Cryo-TM-3-0-Cryogenic-Etch-Technology-to-Accelerate-Scaling-of-3D-NAND-for-the-AI-Era), [Lam 블로그](https://newsroom.lamresearch.com/introducing-lam-cryogenic-etching?blog=true) | 400단+ 깊이를 **2.5배 빠르게**, 10μm 초과, 전력 40%+ 절감 주장. "400단 극저온 식각기가 **CY2027부터** 고객 양산 라인에 배치 시작"(Q1 FY27 콜) [추정] [Investing.com TEL Q1 FY27](https://www.investing.com/news/transcripts/earnings-call-transcript-tokyo-electron-q1-2026-beats-on-eps-shares-rise-62-93CH-4827853), [dempa](https://aei.dempa.net/archives/16308), [TEL 블로그](https://www.tel.com/blog/all/20241021_001.html) | 채널홀 식각 확인 불가(주력 아님) |
| 점유율 | "초고종횡비 채널홀 식각 사실상 100%" [추정] [SemiAnalysis 2023](https://semianalysis.com/2023/07/16/nand-flash-monopoly-broken-tokyo) | "Lam 독점을 깰 도전자", Lam은 "1.5년 늦게 대응, 고객은 2nd 벤더 도입 유인" [추정] 같은 출처(TEL 측 시각) | — |
| Mo 워드라인 | **ALTUS Halo**(2025.2) 업계 첫 Mo ALD. "선도 고객에서 3개 노드 연속 TOR", 한국·싱가포르 팹을 가진 NAND 업체에서 초기 채택, Micron 양산 [추정] [Lam IR ALTUS Halo](https://investor.lamresearch.com/2025-02-19-Lam-Research-Ushers-in-New-Era-of-Semiconductor-Metallization-with-ALTUS-R-Halo-for-Molybdenum-Atomic-Layer-Deposition), 검색 요약 | **SK하이닉스 375단 Mo 공정에서 Lam과 비교 평가 후 TEL 선택**. Lam은 매엽식, TEL은 약 100매 배치 퍼니스 → 장비가·풋프린트·Mo 소모량 유리 [추정] [디일렉 idxno=11210](https://www.thelec.net/news/articleView.html?idxno=11210), [memorymarket](https://www.memorymarket.com/a/14799) | **Producer Selectra Mo Etch**(2026.6): 워드라인 분리를 위한 Mo 선택 제거, HVM qualified. Centris Spectral SiN ALD [확정] amat.md 4-2 ④ |
| 기타 | VECTOR(몰드 스택 PECVD), Strata·Vector DT 수요 증가 언급 [추정] lam.md 4-2 | TEL Q1 FY27 콜: 추가 기회로 "극저온 식각, 저저항 금속 증착, 하이브리드 본딩" 명시 [추정] [BigGo TEL Q1 FY27](https://finance.biggo.com/news/JP_8035.T_2026-07-30) | — |

- **[충돌] SemiAnalysis의 Mo 수혜 순서**: "Lam이 먼저, TEL이 바로 뒤, AMAT·ASMI·Naura는 이후 DRAM·로직 전환에서 수혜"([Bitget 요약](https://www.bitget.com/news/detail/12560605717420)). 그러나 SK하이닉스 375단 Mo는 TEL 선택 보도(디일렉). Lam의 "한국 팹 보유 NAND 업체 초기 채택"이 삼성인지 SK인지는 **확인 불가**. → 전략집에서는 "Mo 증착은 매엽 ALD(Lam)와 배치 퍼니스(TEL)의 방식 경쟁"으로 서술 권장.

### (d) 한국 고객
- **삼성 V10(약 400~430단)**: 채널홀에 극저온 식각 첫 적용 예정, Lam·TEL 장비를 평가. 수요 불확실성과 신기술 비용으로 양산 투자가 지연됐고, 초기 평가에서 양산 적용이 어려워 **운전 온도를 약간 올리는 방향**으로 Lam·TEL과 공정 재조정. TrendForce(2026.6)는 "공급사 선정 최종 단계". [추정] 출처: [TrendForce 2026.6.12](https://www.trendforce.com/news/2026/06/12/news-the-race-to-400-layer-nand-roadmaps-and-key-technologies-driving-samsung-sk-hynix-and-kioxia/), [SmBom – 430단 지연](https://www.smbom.com/news/40296), [Jukan X 요약(삼성 V10 TEL 도입 보도)](https://x.com/Jukanlosreve/status/1893917099816587452)
  - **[충돌]** SemiAnalysis(2023)·Jukan(2025.2)은 "삼성이 V10에 TEL 극저온 식각 도입"으로 보도, TrendForce(2026.6)는 "아직 선정 최종 단계". 2026.10 현재 최종 벤더 비율은 **확인 불가**.
  - 삼성은 FMS 2026에서 V10 BV-NAND(웨이퍼 본딩, 400단)를 공개. [추정] [Techzine](https://www.techzine.eu/news/infrastructure/143432/samsung-unveils-v10-bv-nand-with-wafer-bonding-and-400-layers/), [technologies.org](https://technologies.org/samsung-unveils-zhbm-and-400-layer-v10-bv-nand-at-fms-2026-and-wafer-bonding-is-the-common-thread/)
- **SK하이닉스**: 청주 M15에서 176/238/321단 라인을 전환 투자 중이고, 375단(내부 명칭 "400단") 양산 검증 완료, **2026년 말 양산**, 워드라인 W 일부를 Mo로 교체. SK도 TEL 극저온 식각기 테스트 중이라는 보도. [추정] [디일렉 11210](https://www.thelec.net/news/articleView.html?idxno=11210), [TrendForce 2026.6.12](https://www.trendforce.com/news/2026/06/12/news-the-race-to-400-layer-nand-roadmaps-and-key-technologies-driving-samsung-sk-hynix-and-kioxia/)

### (e) 타임라인
- 2026~2027: 기존 라인 전환(200단+·300단대) 중심, 신규 그린필드 제한적(Lam). 400단대 극저온 식각 양산 배치 **2027~**(TEL). Kioxia/Sandisk는 VLSI 2026에서 1,000단 관련 기술 발표, Lam·삼성은 2030년 1,000단을 목표로 언급. [추정] [kantenna](https://kantenna.com/topic/kioxia-sandisk-1000-layer-3d-nand-vlsi-2026-world-first), [e4ds](https://www.e4ds.com/sub_view.asp?idx=19495&lang=en)

### (f) [해석] 전략적 함의
- **Lam**: NAND는 Lam의 "홈그라운드"이자 가장 큰 리스크. 업그레이드 사이클(장비 교체·개조) 매출이 Q4 FY26 CSBG 사상 최대를 이끌었다. 설치 기반 7,500챔버는 서비스·업그레이드로 돈이 되는 자산이지만, 400단대 신규 POR을 TEL에 일부 내주면 **2027년 이후 신규 설비 점유율이 하락**할 수 있다. Lam의 방어 논리는 "양산 검증된 유일한 극저온 설치 기반 + 업그레이드 경로".
- **TEL**: 채널홀 식각과 Mo 배치 증착은 TEL이 Lam의 핵심 시장에 들어가는 **양면 공격**. 성공하면 "식각 2위 → NAND에서도 1위 경쟁자"로 위상이 바뀐다. 고객(삼성·SK) 입장에서는 2nd 벤더 확보 유인이 크다.
- **AMAT**: 채널홀 식각에서는 비켜서 있고, Mo 선택식각·SiN ALD 같은 **주변 공정**과 계측으로 수혜. NAND는 AMAT 매출 비중이 상대적으로 작다.
- 한국 취업 관점: 삼성 V10·SK 375단 공정 평가가 진행 중인 2026~2027은 **Lam·TEL 한국 법인의 PE/FPE·FSE가 고객 평가 현장에서 직접 경쟁**하는 시기다.

---

## 4. DRAM 스케일링 (6F²→4F²/VCT, 3D DRAM) · HBM

### (a) 기술 변화
- **4F²/VCT**: 트랜지스터를 수직으로 세워 셀 면적을 6F²→4F²로 줄인다. 채널 소재로 IGZO가 검토되고, 커패시터·비트라인 신소재가 필요. 이후 셀을 옆으로 눕혀 쌓는 **3D DRAM**. [추정] [TrendForce 2026.4.24](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/)
- **HBM**: DRAM 다이를 TSV로 수직 적층. 적층 방식은 TCB(열압착)+MR-MUF/NCF → 하이브리드 본딩(범프리스 Cu-Cu)으로 전환 예정. [해석]

### (b) 장비 수요 변화
- Lam: 4F²·3D로 갈수록 "수직 스케일링, 더 많은 금속 배선층, 고종횡비 void-free 충진과 정밀 식각" 필요. [추정] [Quartr](https://quartr.com/events/lam-research-corporation-lrcx-investor-day-2025_33D7JGMm), [디일렉 – Lam 4F²→3D](https://www.thelec.net/news/articleView.html?idxno=5865)
- AMAT 관련 2차 분석: "6F²·4F²·3D DRAM이 단위 캐파당 장비 가치를 높인다", "DRAM WFE가 2026 WFE 성장의 50% 이상, 2027년 2/3 이상" — 회사 원문인지 애널리스트 해석인지 불분명. [추정] [404k Research](https://404kresearch.substack.com/p/applied-materials-deep-dive-how-the)
- **HBM의 웨이퍼 소모**: Micron(Hot Chips 2026) "같은 용량에 HBM은 DDR5 대비 약 **3배** 웨이퍼 면적, 세대마다 격차 확대". HBM4는 최대 5배라는 요약도 있음. → **같은 비트 수요에 전공정 DRAM 캐파(=WFE)가 더 필요**. [확정: 3배] [추정: 5배] [Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation), [igor'sLAB](https://www.igorslab.de/en/micron-hbm-requires-three-times-wafer-area-ddr5-gap-widens/)
- 커지는 공정: DRAM 커패시터 HAR 식각·증착, 패터닝(EUV 층수 증가, SK 1c DRAM EUV 6층 보도[추정] [TweakTown](https://www.tweaktown.com/news/106957/sk-hynix-ramps-1c-dram-to-6-euv-layers-preps-for-high-na-designs-destroy-samsung-in-hbm)), 주변회로 Epi, HBM용 TSV 식각·라이너·Cu 도금·CMP·박막화·본딩·KGD 테스트.

### (c) 3사 포지션
| 회사 | DRAM 전공정 | HBM/TSV | 태그 / 출처 |
|---|---|---|---|
| **Lam** | Akara: 6F² DRAM TOR, 4F²·3D DRAM 확장 가능, "주요 DRAM 업체에서 여러 신규 애플리케이션 수주"(Q4 FY25). Striker 카바이드(커패시터·비트라인 스페이서 TOR 언급). **Aether 드라이 레지스트: 선도 메모리 업체 최첨단 DRAM TOR**(2025.1) | **TSV 식각(Syndion)·Cu 도금(SABRE 3D) 리더십**으로 HBM4/4E·16단 수혜 주장. SABRE 3D 점유율 CY2025 약 5%p 상승 기대 | [확정] Akara·Aether([Lam IR Akara](https://investor.lamresearch.com/2025-02-19-Lam-Research-Unveils-Industrys-Most-Advanced-Conductor-Etch-Technology-to-Date), [PRNewswire Aether](https://www.prnewswire.com/news-releases/breakthrough-euv-dry-photoresist-technology-from-lam-research-adopted-by-leading-memory-manufacturer-302363785.html)) / [추정] SABRE 3D·Striker([Quartr](https://quartr.com/events/lam-research-corporation-lrcx-investor-day-2025_33D7JGMm), lam.md 4-2) |
| **AMAT** | Centura Prime Epi(로직급 Epi를 DRAM 주변회로에), Producer XP Pioneer CVD 패터닝막("leading memory manufacturers" 채택). Q3 FY26: "DRAM(HBM 패키징 포함) 매출 +52% YoY", 하반기 DRAM·선단 로직 "sizable increase" | Nokota VMax 2 ECD(TSV·마이크로범프 Cu), Opta Quad CMP, Producer Avila 2 PECVD(박막 다이 응력), VeritySEM 7AP·SEMVision G7AP(패키징 eBeam), Kinex | [확정] [GlobeNewswire 2026.6.25](https://www.globenewswire.com/news-release/2026/06/25/3317583/0/en/applied-materials-introduces-new-systems-to-accelerate-dram-and-advanced-packaging-for-ai-chips.html) / [추정] +52%([Futurum Q3](https://futurumgroup.com/insights/applied-materials-q3-fy-2026-advanced-packaging-and-dram-accelerate-growth/)) |
| **TEL** | "**DRAM 커패시터 공정에서 모든 선도 고객 POR**", 유전체 식각 세계 점유율 50% 이상(회사 주장). VCT 4F² DRAM 2027~2028 등장 전망 | "HBM용으로 커지는 **인터커넥트 공정에서 매우 높은 점유율**". 박막화(Ulucus G)·본더/디본더(Synapse)·KGD 프로버(Prexa) | [추정] [Investing.com TEL Q4 FY26](https://www.investing.com/news/transcripts/earnings-call-transcript-tokyo-electron-q4-2026-beats-estimates-stock-surges-93CH-4654441), tel.md 4-5 |

- [충돌] **DRAM 커패시터·HAR 식각 주도권**: TEL은 "커패시터 공정 전 선도 고객 POR"을, Lam은 "DRAM 점유율 확대(Akara·Striker)"를 각각 주장. 공정 단계(커패시터 몰드 식각 vs 게이트·비트라인 도체 식각)가 다를 수 있어 직접 비교 불가.
- [충돌] **HBM TSV/인터커넥트**: Lam은 TSV 식각 리더십, TEL은 HBM 인터커넥트 고점유를 각각 주장. tel.md 7-2의 "Episode UL이 SK하이닉스 HBM TSV 식각 POR"은 내부 자료로 외부 미확인.

### (d) 한국 고객 · HBM4/4E 타이밍
- **4F²/VCT**: 삼성은 10a DRAM을 4F²+VCT로 2026 개발 완료 → 2027 품질 테스트 → **2028 양산 이전** 목표, 10a~10c 3세대 적용 후 10d부터 3D DRAM. SK하이닉스는 10a를 건너뛰고 **10b에서 도입**. [추정] [TrendForce 2026.4.24](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/), [Digitimes 2025.6](https://www.digitimes.com/news/a20250620PD214/dram-samsung-sk-hynix-3d-development.html)
- **HBM4 양산**: 삼성은 2026년 2월 상용 HBM4 출하(1c DRAM + 4nm 로직 베이스 다이, 11.7Gbps) 발표. SK하이닉스 HBM4 양산 개시 시점은 "2026.2"와 "2026 Q2"로 요약마다 다름. [확정: 삼성] [Samsung Newsroom](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4), [TrendForce 2026.1.26](https://www.trendforce.com/news/2026/01/26/news-samsung-reportedly-set-to-begin-official-hbm4-shipments-to-nvidia-and-amd-in-february/) / [충돌: SK 시점] [BigGo](https://finance.biggo.com/news/Tui5V5sBU6SAbxhZ0Sjf) vs [FinancialContent](https://markets.financialcontent.com/stocks/article/tokenring-2026-1-26-the-hbm4-era-begins-samsung-and-sk-hynix-trigger-mass-production-for-next-gen-ai)
- **HBM4E**: 양사 2027년 샘플 출하 진행이라는 요약 [추정, 출처 신뢰도 낮음] [Silicon Analysts](https://siliconanalysts.com/market/hbm4-mass-production-race-accelerates-sk-hynix-leads-samsung-surges-supply-locke-2026-08-03)
- **하이브리드 본딩 시점 [충돌]**:
  - SK하이닉스(Hot Chips 2026, 2026.8): "HBM4E에는 하이브리드 본딩이 준비되지 않는다 → **HBM5가 가장 이른 시점**", Nvidia Rubin까지 MR-MUF 유지. 근거는 JEDEC HBM4 패키지 높이 한도 **775μm**(HBM3E까지 720μm). [확정] [Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/sk-hynix-says-hybrid-bonding-wont-be-ready-for-hbm4e-as-ai-memory-runs-into-a-775-micron-ceiling), [ninescrolls](https://ninescrolls.com/news/sk-hynix-rules-out-hybrid-bonding-for-hbm4e-775-micron-ceiling-keeps-mr-muf/)
  - 삼성: HBM4에 하이브리드 본딩 공개 약속(2025.5), "16단 HBM4E부터 적용"이 공식 방향. 반면 SEMES 연구소장은 Nano Korea 2026에서 "HBM5 이후 본격 사용". [추정] [36kr](https://eu.36kr.com/en/p/3756077063209481), [economy.ac](https://economy.ac/news/2026/02/202602288324)
  - SK하이닉스 12단 하이브리드 본딩 HBM 검증 완료·수율 개선 중(2026.4). [추정] [TrendForce 2026.4.29](https://www.trendforce.com/news/2026/04/29/news-sk-hynix-reportedly-completes-12-high-hybrid-bonding-hbm-validation-works-to-raise-yields-for-mass-production/)
  - → [해석] 2026.10 기준 가장 최신·1차 발언은 SK하이닉스 Hot Chips(=HBM5)다. "HBM4E부터 하이브리드 본딩"이라는 문장은 쓰지 말 것.

### (e) 타임라인 요약
- HBM4 양산 2026 / HBM4E 2027 / 하이브리드 본딩 본격화 HBM5(2028 이후 추정) / 4F²·VCT 2027~2028 / 3D DRAM 2030년대. [추정] 위 출처 종합

### (f) [해석] 전략적 함의
- **DRAM이 2026~2027 WFE 성장의 핵심**이 되면서 3사 모두 DRAM 노출을 키운다. HBM 웨이퍼 3배 효과는 전공정(식각·증착·EUV 트랙) 전체에 순풍.
- **Lam**: 메모리 비중이 원래 높고, Akara·Aether로 DRAM 내 점유율 확대를 노린다. 4F²·3D DRAM은 "NAND에서 쌓은 HAR 식각 역량을 DRAM으로 옮기는" 그림이라 장기적으로 가장 유리한 구조.
- **AMAT**: HBM 공정 체인(Epi→ECD→CMP→증착→eBeam→본딩) 전체를 가진 유일한 회사라는 점이 차별점. 하이브리드 본딩 지연은 Kinex 매출 시점을 늦추지만, TSV·CMP·ECD는 TCB 방식에서도 쓰여 영향이 제한적.
- **TEL**: DRAM 커패시터 식각과 EUV 트랙(DRAM EUV 층 증가)으로 이중 수혜. HBM에서는 박막화·본더·프로버로 "후공정 3종"을 가진 것이 강점.

---

## 5. 첨단 패키징 (하이브리드 본딩, 칩렛, 패널 레벨)

### (a) 기술 변화
- 칩렛·HBM·CoWoS형 2.5D/3D 집적이 늘면서 웨이퍼 팹 공정(증착·식각·CMP·도금·계측)이 패키징으로 내려온다. D2W 하이브리드 본딩은 범프 없이 Cu-Cu를 직접 붙인다. 패널(사각 대형 기판) 레벨 패키징은 원형 웨이퍼의 면적 한계를 넘기 위한 시도. [해석]

### (b) 장비 수요 변화 (정량)
- AMAT: 패키징 매출 **CY2026 +70% 이상** 전망. [추정] [Futurum Q3 FY26](https://futurumgroup.com/insights/applied-materials-q3-fy-2026-advanced-packaging-and-dram-accelerate-growth/), [Yahoo/Zacks](https://finance.yahoo.com/technology/ai/articles/amat-rides-ai-led-wfe-151900886.html)
- Lam: 패키징 매출 CY2026 **+50% 이상**이라는 요약과 **+70% 이상**이라는 요약이 공존. [충돌] [Yahoo – Lam betting on AP 50%](https://finance.yahoo.com/markets/stocks/articles/lam-research-lrcx-betting-advanced-200933179.html) vs 같은 검색의 70% 요약(출처 불명확, AMAT 수치 혼입 가능성)
- TEL: 본딩 관련 매출 FY2026 약 **300억 엔 → 1~2년 내 연 1,000억 엔 이상** 계획, 2026~2030 레이저·본더/디본더 관련 누적 약 **5,000억 엔** 기대. [추정] [Investing.com TEL Q4 FY26](https://www.investing.com/news/transcripts/earnings-call-transcript-tokyo-electron-q4-2026-beats-estimates-stock-surges-93CH-4654441)
- HBM TCB 시장: 한미반도체 2025년 1~3분기 매출 기준 **71.2%**, SEMES·ASMPT·Yamaha·한화세미텍 순. [추정] [introl](https://introl.com/blog/south-korea-hbm4-stargate-memory-supercycle-2026) 등 검색 요약

### (c) 3사 포지션
| 회사 | 포지션·제품 | 실적·채택 | 태그 / 출처 |
|---|---|---|---|
| **AMAT** | **Kinex**(Besi 공동, 통합 D2W 하이브리드 본더) + Opta Quad CMP + Nokota VMax 2 ECD + Avila 2 PECVD + eBeam 계측. 2026.10.1 Besi가 EPIC 센터 Innovation Partner로 합류, 범위를 TCB 스케일링·die-on-panel·광 인터커넥트로 확대 | "로직·메모리·OSAT 고객이 양산 채택", HVM에서 시간당 1,600 다이(최대 2,000) 배치 | [확정] [GlobeNewswire 2026.10.1](https://www.globenewswire.com/news-release/2026/10/01/3372971/0/en/applied-materials-and-besi-expand-strategic-partnership-to-advance-next-generation-packaging-for-ai-scaling.html) / [추정] [EE Times](https://www.eetimes.com/applied-materials-besi-push-die-to-wafer-hybrid-bonding-toward-high-volume-manufacturing/) |
| **Lam** | VECTOR TEOS 3D(2025.9, 칩렛 갭필, 휨 웨이퍼 대응), SABRE 3D(ECD), Syndion(TSV), Striker(TSV 라이너), Coronus DX(베벨 증착). **패널 레벨 패키징 CoE(오스트리아 잘츠부르크, 2026.5)** — 도금·세정·식각 습식 공정을 패널로 확장, Kallisto 패널 ECD 공개. Rapidus가 600mm 각 유리 인터포저에 Lam PLP 시스템 채택 보도 | 패키징 매출 고성장(위 [충돌]) | [확정] [Lam Newsroom PLP CoE](https://newsroom.lamresearch.com/Lam-Research-Establishes-Panel-Level-Packaging-CoE), [디일렉 10758](https://www.thelec.net/news/articleView.html?idxno=10758), lam.md 4-2 / [추정] Rapidus([TrendForce 2026.5.26](https://www.trendforce.com/news/2026/05/26/news-rapidus-reportedly-taps-lam-research-panel-level-packaging-system-for-600mm-square-glass-interposer-push/)) |
| **TEL** | Synapse(본더/디본더), Ulucus G(박막화), Ulucus LX(레이저 리프트오프), **Prexa SDP**(첨단 패키징용 프로버, 2026.4), LITHIUS Pro AP(패키징 트랙). W2W 하이브리드 본딩 1μm·0.5μm 피치, 전기 수율 98% 시연 | 본딩 매출 300억→1,000억 엔 계획(위) | [추정] tel.md 4-5, [TEL Synapse/Ulucus 페이지](https://www.tel.com/product/synapse-ulucus.html), [TEL Prexa SDP](https://www.tel.com/news/product/2026/20260416_001.html) |

### (d) 한국 고객
- **SK하이닉스**: AMAT Kinex로 하이브리드 본딩 파일럿 라인 구축·평가(2026 초~), AMAT(CMP·플라즈마)+Besi(본더) 인라인 시스템 1세트 약 200억 원 첫 양산급 발주 보도. 동시에 HBM4용 TCB는 한미반도체(442억 원, 2026.6)·ASMPT(약 300억 원) 발주. [추정] [디일렉 6246](https://www.thelec.net/news/articleView.html?idxno=6246), [Jukan X](https://x.com/jukan05/status/2038926893785788532?lang=en), [TrendForce 2026.6.9](https://www.trendforce.com/news/2026/06/09/news-sk-hynix-reportedly-places-44-2bn-won-tc-bonder-order-with-hanmi-accelerating-hbm4-ramp-up/), [TrendForce 2025.12.12](https://www.trendforce.com/news/2025/12/12/news-sk-hynix-reportedly-places-hbm4-tc-bonder-order-with-asmpt-as-hanmi-hanwha-patent-clash-heats-up/)
- **삼성**: 개발용으로 Besi 도입, 자회사 SEMES 하이브리드 본더 품질 테스트(성숙도는 Besi보다 낮다는 평가). [추정] [36kr](https://eu.36kr.com/en/p/3407854283296132)
- 삼성·SK 모두 AMAT의 EPIC 센터 참여. [확정] amat.md 4-2 ⑦

### (e) 타임라인
- TCB(+MR-MUF/NCF): HBM4·HBM4E 주력 / D2W 하이브리드 본딩: HBM5 이후 본격(4장 [충돌] 참고), 로직 3D IC(SoIC류)에서는 이미 사용 / PLP: 2026 R&D·파일럿, 대규모 양산은 과제 남음(Digitimes). [추정] [Digitimes 2026.5.22](https://www.digitimes.com/news/a20260522PD223/lam-research-plp-panel-production-process-control-equipment.html)

### (f) [해석] 전략적 함의
- **AMAT**: Besi와의 결합으로 "패키징 = AMAT의 세 번째 성장축"을 가장 분명히 만든 회사. 하이브리드 본딩 지연은 단기 리스크지만, Besi 파트너십을 TCB까지 넓혀(2026.10.1) **본딩 방식이 무엇이 되든 수혜**하는 쪽으로 헤지했다.
- **Lam**: 본더는 없고 **도금·TSV 식각·갭필**이라는 "본딩 전후 공정"에 집중. PLP 선점(잘츠부르크)은 차세대 기판 전환에 대한 옵션.
- **TEL**: 본더·박막화·레이저·프로버로 "후공정 하드웨어"가 가장 많다. 단 본더 시장은 EVG(W2W)·Besi(D2W)·한미(TCB) 같은 전문 업체가 강해 TEL은 도전자.
- 국내 취업 관점: HBM 패키징 장비 경쟁은 **빅3 vs 한국 후공정 장비사(한미·한화·SEMES)** 구도도 함께 본다.

---

## 6. 리소그래피 인접: High-NA EUV, EUV 레지스트(MOR·드라이 레지스트), 패턴 셰이핑

### (a) 기술 변화
- High-NA EUV(ASML EXE:5200B)는 해상도를 높여 멀티패터닝을 줄인다. 레지스트는 화학증폭형(CAR) → 금속산화물 레지스트(MOR, 습식 현상) 또는 **드라이 레지스트**(기상 증착·건식 현상)로 다변화. 패턴 셰이핑(AMAT Sculpta)은 한 번 노광한 패턴을 방향성 식각으로 늘려 더블 패터닝 단계를 없앤다. [해석] amat.md·tel.md 4장

### (b) 장비 수요 변화
- EUV 레지스트·코터·디벨로퍼 시장은 **$5B+** 규모로 Lam·TEL·JSR이 경쟁. [추정] [SemiAnalysis](https://newsletter.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle)
- Sculpta: 대체하는 EUV 더블 패터닝 시퀀스 1개당 **10만 WSPM 기준 설비비 약 $250M 절감, 웨이퍼당 약 $50 절감**. [확정] [GlobeNewswire 2023.2.28](https://www.globenewswire.com/news-release/2023/02/28/2616946/0/en/Applied-Materials-Innovative-Pattern-Shaping-Technology-Reduces-the-Cost-Complexity-and-Environmental-Impact-of-Advanced-Chip-Manufacturing.html), [AMAT IR Patterning](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-expands-patterning-solutions-portfolio)
  - [해석] Sculpta·High-NA는 **EUV 노광 횟수를 줄이는** 방향이라 트랙(TEL) 사용 횟수에는 중립~약한 부정, 식각·증착(패턴 셰이핑, 하드마스크)에는 긍정. 다만 DRAM의 EUV 층수 자체는 늘고 있어(SK 1c 6층 보도) 트랙 수요 총량은 증가 중.
- Lam 드라이 레지스트: 5년 누적 매출 기회 **$1.5B**를 "더 높을 것"이라고 상향 시사(수치 미제시). [추정] [Yahoo – Lam lifts WFE outlook](https://finance.yahoo.com/technology/ai/articles/lam-research-lifts-2026-wfe-180229282.html)

### (c) 3사 포지션
| 회사 | 포지션 | 태그 / 출처 |
|---|---|---|
| **TEL** | 코터/디벨로퍼 점유율 **90% 이상**, EUV용 사실상 100%. LITHIUS Pro DICE(2025.12) 램프로 **C/D 매출 +50% 이상**, "선단 로직·DRAM 여러 공정 POR". MOR용 습식 현상 **ESPERT**: EUV 감도 약 36% 개선, 단일 브리지 결함 2.1배 감소, MOR에서 30% 도즈 저감(별도 요약은 38%) | [확정] 점유율·DICE(tel.md 2-2, 4-1) / [추정] ESPERT 수치([SemiAnalysis](https://newsletter.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle), [TEL EUV 2023 논문](https://euvlitho.com/2023/P44.pdf)) — 도즈 저감 30% vs 38% [충돌] |
| **Lam** | **Aether** 드라이 레지스트: 2025.1 "선도 메모리 제조사 최첨단 DRAM TOR"(SK하이닉스로 보도). 2026.3 IBM과 5년 협력(High-NA EUV로 1nm 이하 로직, 올버니), JSR과도 협력 | [확정] [PRNewswire](https://www.prnewswire.com/news-releases/breakthrough-euv-dry-photoresist-technology-from-lam-research-adopted-by-leading-memory-manufacturer-302363785.html), [IBM Newsroom 2026.3.10](https://newsroom.ibm.com/2026-03-10-ibm-and-lam-research-announce-collaboration-to-advance-sub-1nm-logic-scaling) / [추정] SK 고객명([electronics360](https://electronics360.globalspec.com/article/18254/sk-hynix-to-use-dry-resist-euv-lithography-for-future-dram)) |
| **AMAT** | **Centura Sculpta**: "모든 선단 로직 업체와 Sculpta 적용 확대 중", 팁-투-팁 축소와 브리지 결함 제거. Producer XP Pioneer CVD(패터닝막), Sym3 Y Magnum, Aselta 디자인 기반 계측 | [확정] [AMAT IR Patterning](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-expands-patterning-solutions-portfolio) |
| (TEL 추가) | Acrevia(가스 클러스터 빔, EUV 패턴 CD·형상 저손상 보정, 2024.7) — Sculpta와 개념상 경쟁 | [추정] tel.md 4-1 |
| (기타) ASML | High-NA 스캐너 독점. JSR(Inpria) MOR 소재 | [해석] |

### (d) 한국 고객
- SK하이닉스: High-NA EUV 2025 하반기 도입, 2026 R&D 시작, 차세대 DRAM 개발·양산에 활용 계획. PSM(위상반전 마스크) 도입 보도. [추정] [TrendForce 2026.2.16](https://www.trendforce.com/news/2026/02/16/news-asmls-high-na-euv-for-2027-28-which-giants-are-betting-big-intel-samsung-sk-hynix-or-tsmc/), [Digitimes 2026.8.13](https://www.digitimes.com/news/a20260813PD214/euv-sk-hynix-high-na-high-na-euv-dram.html)
- 삼성: EXE:5200B 1호기 2025 말, 2호기 2026 상반기 입고, 양산 적용은 약 2027로 신중. [추정] [TrendForce 2025.10.16](https://www.trendforce.com/news/2025/10/16/news-samsung-reportedly-purchasing-two-asml-high-na-euv-tools-for-mass-production-by-1h26/), [KuCoin 요약](https://www.kucoin.com/news/flash/high-na-euv-market-divides-as-intel-leads-tsmc-waits-samsung-hesitates)
- [해석] **Aether를 SK가 DRAM에 채택**했다는 보도는 TEL 트랙 독점에 대한 첫 균열이자, Lam 한국 법인이 포토(리소) 영역에 처음 진입하는 사례.

### (e) 타임라인
- Intel: EXE:5200B 인수 테스트 통과(2025.12), 14A 개발. TSMC: 비용 문제로 도입 지연. 2026은 Intel·SK 첫 High-NA 제품 수율 검증의 해, 양산 본격 2027~2028. [추정] [TrendForce 2026.5.20](https://www.trendforce.com/news/2026/05/20/news-asml-expects-first-high-na-euv-memory-logic-products-within-months-amid-tsmcs-cost-driven-delay/), [CNBC 2026.9.8](https://www.cnbc.com/2026/09/08/tsmc-samsung-asml-high-na-euv-machine-ai-chips.html)

### (f) [해석] 전략적 함의
- **TEL**: 트랙은 TEL 수익성의 근간. 방어 전략은 (1) DICE로 High-NA 결함 제어, (2) MOR 습식 현상(ESPERT)으로 "기존 트랙으로도 차세대 레지스트 대응 가능"을 증명해 드라이 레지스트 전환 유인을 낮추는 것.
- **Lam**: Aether는 Lam이 **리소 셀(노광 전후)** 이라는 새 SAM에 들어가는 교두보. DRAM TOR 1건 + IBM High-NA 로직 협력으로 메모리·로직 양쪽 레퍼런스를 만드는 중. 다만 매출 규모($1.5B/5년)는 아직 작다.
- **AMAT**: Sculpta는 "EUV를 덜 쓰게 하는" 장비라 ASML·TEL과 간접 경쟁. 고객의 EUV 비용 압박이 클수록(TSMC High-NA 지연 사례) 설득력이 커진다.
- 같은 이슈를 3사 지원자가 **정반대로 해석**해야 하는 대표 주제(tel.md 4-1 [해석]과 일치).

---

## 7. 소재 전환: W→Mo, Ru/Co, 신규 유전체

### (a) 기술 변화
- 배선·콘택이 가늘어지면 W·Cu는 배리어/라이너 두께 때문에 실효 저항이 커진다. Mo는 배리어 없이 증착 가능하고 미세 선폭에서 저항이 낮다. Cu 배선은 RuCo 라이너로 연장, 장기적으로 Ru 등 "Cu 이후" 금속 검토. low-k 유전체는 기계적 강도와 k값을 동시에 개선해야 한다. [해석] lam.md 4-4, amat.md 4-2 ⑤

### (b) 장비 수요 변화
- Mo: NAND용 Mo 증착 장비 2027 $1B+, 2030 연 ~$2B(3장). Mo 전환마다 **새 증착 장비**가 필요하다는 점이 핵심. [추정] [Bitget/SemiAnalysis](https://www.bitget.com/news/detail/12560605717420)
- Mo 전구체는 상온 고체라 가열·안정 공급 시스템 필요 → 증착 장비 설계 차별화 포인트. [추정] [TrendForce 2026.6.12](https://www.trendforce.com/news/2026/06/12/news-the-race-to-400-layer-nand-roadmaps-and-key-technologies-driving-samsung-sk-hynix-and-kioxia/)
- RuCo 라이너: 2nm에서 선 저항 최대 25% 감소, 라이너 두께 33% 감소(AMAT 주장). [확정] [GlobeNewswire 2024.7.8](https://www.globenewswire.com/news-release/2024/07/08/2909540/0/en/applied-materials-unveils-chip-wiring-innovations-for-more-energy-efficient-computing.html)

### (c) 3사 포지션
| 소재 | Lam | AMAT | TEL |
|---|---|---|---|
| Mo(NAND 워드라인) | ALTUS Halo Mo ALD, 3개 노드 연속 TOR(선도 고객), Micron 양산 [추정] | Selectra Mo Etch(선택 제거) [확정] | 배치 퍼니스 Mo 증착, SK하이닉스 375단 선정 보도 [추정] |
| Mo(로직 콘택·DRAM) | ALTUS Halo 로직 팹 채택 시작, DRAM 개발 중 [추정] [Lam IR](https://investor.lamresearch.com/2025-02-19-Lam-Research-Ushers-in-New-Era-of-Semiconductor-Metallization-with-ALTUS-R-Halo-for-Molybdenum-Atomic-Layer-Deposition) | Spectral ALD로 W 콘택→Mo(2026.2), "선도 파운드리 사용 중" [확정] amat.md | 확인 불가 |
| Ru/Co | 확인 불가 | **RuCo 라이너: 2nm에서 모든 선도 로직 업체 채택**, Endura 플랫폼 [확정] [AMAT IR 2024.7](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-unveils-chip-wiring-innovations-more-energy/) | 확인 불가 |
| low-k·유전체 | Striker ALD(유전막), VECTOR PECVD | **강화 Black Diamond: 모든 선도 로직·DRAM 업체 채택** [확정] 위 / Centris Spectral SiN ALD, Producer Precision Selective Nitride [확정] | EVAROS 배치 열처리(ALD 등), NT333 ALD [추정] tel.md 4-3 |
| (기타) | ASM International: 단일 웨이퍼 ALD 55%+ (전체 ALD 19.4%), Kokusai: 배치 ALD 약 70% [추정] 아래 경쟁지도 |

### (d) 한국 고객
- SK하이닉스 375단 Mo 워드라인 일부 적용(2026 말 양산). 삼성 V10의 Mo 적용 여부 **확인 불가**. [추정] [디일렉 11210](https://www.thelec.net/news/articleView.html?idxno=11210)
- [해석] wccftech는 "SK가 400단+에서는 W를 완전히 버려야 한다"고 보도 → 다음 세대에서 Mo 증착 장비 물량이 더 커질 가능성. [추정] [wccftech](https://wccftech.com/sk-hynix-races-samsung-to-400-layer-nand-must-abandon-tungsten-as-stacking-hits-a-wall/)

### (e) 타임라인
- NAND Mo: 2025(Micron)~2026(SK 375단) → 2027 NAND 캐파 약 30%(추정) / 로직 Mo 콘택: 2nm 세대~ / DRAM Mo: 개발 중 / RuCo: 2nm 세대 적용. [추정]

### (f) [해석] 전략적 함의
- **소재 전환은 "증착 회사"의 시장 점유율 재배분 기회**다. W CVD 강자(Lam ALTUS)가 Mo로 자연 연장하려 하지만, 배치 장비(TEL·Kokusai)와 ALD 전문(ASM)이 경제성으로 파고든다.
- **AMAT**는 Cu 배선 연장(RuCo·Black Diamond)으로 "Cu를 더 오래 쓰게" 만드는 방어 전략과 Mo 콘택·선택식각으로 "새 금속 주변 공정"을 함께 잡는 투트랙.
- 재료·화학 전공자에게 가장 직접적인 자소서 소재(새 금속마다 레시피·분석·균일도 재정립).

---

## 8. 팹 자동화·데이터: Equipment Intelligence, AI 서비스, 코봇, 디지털 트윈

### (a) 기술 변화
- 장비 센서 데이터를 모아 예측 정비·자동 보정하고, 반복 정비 작업은 로봇이 대신하며, 공정·장비를 가상 모델(디지털 트윈)로 먼저 검증한다. [해석]

### (b) 서비스 사업에 미치는 영향 (정량)
- **Lam CSBG**: Q4 FY26(6월 분기) 약 **$2.5B**, 3개 분기 연속 최대, +43% YoY(주로 업그레이드). Q3 FY26 $2.11B로 첫 $2B 돌파. [확정] [Yahoo](https://finance.yahoo.com/technology/articles/lam-research-q4-earnings-call-230406093.html), [Investing.com Q3 slides](https://www.investing.com/news/company-news/lam-research-q3-2026-slides-ai-drives-record-revenue-raises-outlook-93CH-4631007)
- Lam: 한 고객 램프업에서 **Equipment Intelligence Services + Dextro** 병행으로 장비 가용률 **23% 개선**(웨트 클린 품질 15%, first-time-right 정비 8%). [추정] [nikhs substack 3QFY26](https://nikhs.substack.com/p/lam-research-3qfy26-more-than-a-cycle), [Investing.com](https://www.investing.com/news/company-news/lam-research-q3-2026-slides-ai-drives-record-revenue-raises-outlook-93CH-4631007)
- **AMAT AGS**: Q2 FY26 매출 $1.665B(전년 $1.42B). 반복성 부품·서비스·소프트웨어 매출의 약 **60%가 장기 구독 계약**, AGS의 약 2/3가 장기 계약(갱신율 90%+, 평균 약 2.9년). AIx에 **3만~3.5만 챔버 이상** 연결. [추정] 수치 출처 혼재: [AMAT 블로그 – Subscription services](https://www.appliedmaterials.com/us/en/blog/blog-posts/subscription-services-provide-increased-value-to-chipmakers.html), [TradingView/Zacks AGS](https://www.tradingview.com/news/zacks:74395071c094b:0-can-amat-s-ags-business-become-a-long-term-growth-driver/), [tikr](https://www.tikr.com/blog/applied-materials-30-systems-outlook-is-the-headline-the-services-business-may-be-the-better-story)
- **TEL Field Solutions**: FY2026 6,260억 엔(+16.3%). [추정] tel.md 2-3

### (c) 3사 포지션
| 회사 | 자동화·데이터 제품 | 최근 진척 | 태그 / 출처 |
|---|---|---|---|
| **Lam** | Equipment Intelligence(자율 보정·자가적응 정비), **Dextro 코봇**(2024.12 업계 첫 팹 정비 코봇), Semiverse Solutions(시뮬레이션·가상 트레이닝) | Dextro **8개 장비 유형**으로 확대, 첫 증착용 코봇 출하(Q3 FY26), 차세대는 연산 10배·소형화. EI를 선도 고객 R&D(NAND·DRAM 신노드 증착)에 적용 | [확정] Dextro 출시([PRNewswire](https://www.prnewswire.com/news-releases/lam-research-introduces-the-semiconductor-industrys-first-collaborative-robot-for-fab-maintenance-optimization-302327247.html)) / [추정] 8종·10배([nikhs](https://nikhs.substack.com/p/lam-research-3qfy26-more-than-a-cycle)) |
| **AMAT** | **AIx**(Actionable Insight Accelerator: 센서·계측·ML), 구독형 서비스, FabVantage(레거시 팹 컨설팅), EPIC 센터(공동 개발) | 3만~3.5만 챔버 연결, 장기 계약 비중 높음 | [추정] 위 |
| **TEL** | **Epsira**(DX 인프라: AI MTBWC 연장 분석, 로보틱스 정비, AI 트러블슈팅, "자율 장비" 비전), **TELeMetrics**(원격 모니터링), Episode UL "Smart tool" | 2026.7.16 NVIDIA와 협력 확대(Isaac 디지털 트윈, NeMo 에이전트 AI·로보틱스) | [추정] [TEL 뉴스 2026.7.16](https://www.tel.com/news/topics/2026/20260716_001.html), [TEL Field Solutions](https://www.tel.com/sustainability/customer/field-solutions/index.html) |

### (d) 한국 고객·국내 직무 관련성
- 삼성·SK 팹은 3사의 최대 설치 기반 중 하나. 이번 공채에서 Lam은 **Data Analytics FSE**를 신설, AMAT는 MesoVision/Metrology Algorithm Developer·FabVantage PM을 모집. [확정] lam.md 1-2·5-2, amat.md 1-1
- [해석] 서비스가 "고장 수리" → "가용률 보장 계약(구독)·데이터 기반 예측"으로 바뀌면서, 국내 FSE/CE의 성과 지표가 **가동률·first-time-right·MTBC** 중심으로 이동.

### (e) 타임라인
- 이미 상용화(Dextro, AIx, Epsira). 디지털 트윈·AI 에이전트 기반 정비는 2026~2028 확산 단계. [해석]

### (f) [해석] 전략적 함의
- **Lam**: 설치 기반이 가장 큰 NAND·식각 장비를 중심으로 **"하드웨어 자동화(코봇)"까지 직접 만드는** 유일한 회사. 서비스 매출 고성장의 상당 부분이 업그레이드라 NAND 사이클과 연동된다는 점은 리스크.
- **AMAT**: 서비스를 **구독 모델**로 가장 먼저 전환해 매출 안정성이 높다. AIx·EPIC으로 "개발 단계부터 데이터를 쥐는" 전략.
- **TEL**: 트랙 설치 기반(전 세계 노광기 옆)이 데이터 수집의 최대 자산. NVIDIA 협업으로 디지털 트윈·에이전트 AI를 빠르게 끌어오는 중.
- 공통: 코봇·AI가 늘어도 **진단·판단·고객 커뮤니케이션은 사람**이라는 메시지가 면접 답변의 핵심(lam.md 4-3 [해석]과 일치).

---

## 9. 공정 세그먼트별 경쟁 지도

> 표기: ◎ 리더 / ○ 강한 2위·도전자 / △ 참여 / – 사실상 없음. 점유율은 **출처가 있을 때만** 표기, 시장조사기관마다 범위 정의가 달라 **수치끼리 비교 금지**.

| 세그먼트 | Lam | AMAT | TEL | 3사 외 주요 플레이어 | 점유율 근거·충돌 |
|---|---|---|---|---|---|
| **식각 – 도체(conductor)** | ◎ (Kiyo, Akara) | ○ (Sym3, "선단 로직·DRAM 도체식각 리더십 확장" 주장) | ○ (Tactras, Episode UL) | Hitachi High-Tech | [충돌] "Lam 43%·TEL 20%·AMAT 19%"(semiconductorinsight) vs "Lam 26%/22.1%"(GGI·Dataintelo) — lam.md 2-5. AMAT는 Sym3 Z Magnum 발표에서 "conductor etch market leadership in advanced logic and DRAM" 주장 [추정] [AMAT IR](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-unveils-transistor-and-wiring-innovations/) |
| **식각 – 유전체(dielectric)** | ◎ (Flex, Vantex, Cryo; NAND 채널홀 사실상 100%) | △ | ◎/○ (Tactras Vigus, **회사 주장 50%+**) | — | [충돌] TEL은 "유전체 식각 세계 50% 이상"(TEL Q4 FY26 콜), Lam은 NAND HAR 독점. 정의 차이(NAND HAR vs DRAM 커패시터·콘택 등) 가능성 [추정] |
| **식각 – 전체 드라이** | ◎ | ○ | ○ | Hitachi, NAURA, AMEC | [충돌] TEL **23%**(Gartner·TechInsights 인용) / TEL 27%(tel.md, 분석 1건) / "**AMAT 32%·Lam 28%**"(Mordor) / "plasma etch Lam 약 45%" — 기관별 범위 상이. 출처: [Yahoo TEL Q4 FY26](https://finance.yahoo.com/quote/8035.T/earnings/8035.T-Q4-2026-earnings_call-552866.html), [Mordor etch](https://www.mordorintelligence.com/industry-reports/semiconductor-etch-equipment-market), lam.md 2-5 |
| **식각 – 선택적/등방성** | ○ (Argos [충돌], Prevos) | ◎ (Selectra, Mo Etch) | ○ (Certas LEAGA, GAA 등방성 확대 주장) | — | 점유율 확인 불가 |
| **증착 – CVD/PECVD** | ◎ (VECTOR, ALTUS W CVD) | ◎ (Producer, Black Diamond, Pioneer) | △ (Triase+, Episode 1) | ASM, Kokusai(배치 CVD 34%, 2023 Gartner) | Lam·AMAT 공동 리더. 개별 % 확인 불가. Kokusai: [Kokusai IR Day 2024](https://www.kokusai-electric.com/sites/default/files/2024-06/IRDay2024_Part2_textversion_Eng_240626.pdf) [추정] |
| **증착 – ALD** | ○ (Striker, ALTUS Halo Mo) | ○ (Spectral, Trillium, Olympia[내부]) | ○ (NT333, 배치 ALD) | **ASM International**(단일웨이퍼 ALD 55%+, 전체 ALD 19.4%), **Kokusai**(배치 ALD 약 70%) | [추정] [GMInsights ALD](https://www.gminsights.com/industry-analysis/ald-equipment-market), [SemiAnalysis Kokusai](https://newsletter.semianalysis.com/p/going-vertical-gate-all-around-3d). TEL 배치 ALD 약 30%라는 요약도 [추정] |
| **증착 – PVD** | △ | ◎ (Endura) | △ | Ulvac, Evatec | AMAT "Endura PVD 약 85%"는 내부 자료만 → 확인 불가(amat.md 2-4) |
| **증착 – ECD(도금)** | ◎ (SABRE 3D, Kallisto 패널) | ○ (Nokota VMax 2) | – | ACM Research, Ebara | Lam SABRE 3D CY2025 점유율 약 5%p 상승 기대(Quartr) [추정]. 절대 % 확인 불가 |
| **증착 – Epi** | – | ◎ (Centura Epi, Prime Epi) | – | ASM | AMAT "Epi 90%+"는 내부 자료만 → 확인 불가 |
| **CMP** | – | ◎ (Reflexion[내부], Opta Quad) | – (패키징 박막화 Ulucus G는 그라인딩 영역) | **Ebara** | [추정] AMAT 약 42%, Ebara 약 27%(GGI 계열 요약) [CMP 시장](https://www.globalgrowthinsights.com/market-reports/cmp-equipment-market-115415). 내부 자료 "AMAT 약 70%"와 [충돌] |
| **이온주입** | – | ◎ (VIISta[내부]) | – | Axcelis(SiC 70~80%), Sumitomo HI | [충돌] AMAT 62.65%(2024) / 38.2% / 약 30% — 기관별 차이 극심 [Fortune BI 등 검색 요약](https://www.fortunebusinessinsights.com/ion-implanter-market-109422). 내부 "약 70%"도 별개 |
| **세정(clean)** | ○ (Coronus 베벨, 매엽 웻) | △ | ○ (CELLESTA; 21% 한 분석) | **SCREEN**(매엽 38%, 배치 70%, CY2024), SEMES, ACM | [추정] SCREEN 수치: 검색 요약([SCREEN IR](https://www.screen.co.jp/download_file/8ea7bfd9-acb0-494f-852a-7c14f39d901a/1211)). TEL 21%는 tel.md [S22] |
| **트랙(코터/디벨로퍼)** | △ (Aether는 트랙이 아닌 드라이 레지스트 증착·현상) | – | ◎ (**90% 이상**, EUV 사실상 100%) | SCREEN, SEMES | [확정] 90%+ (TEL 실적콜). 세부 90~92% [충돌] tel.md 2-2 |
| **열처리/퍼니스** | – | ○ (RTP·어닐, 매엽) | ◎/○ (배치 퍼니스 TELINDY·EVAROS) | **Kokusai**(배치) | [충돌] TEL "약 40% 1위"(tel.md, 분석 1건) vs "버티컬 퍼니스 약 15%"(검색 요약) [추정] |
| **계측/검사** | – (Semiverse는 SW) | ○ (eBeam: PROVision, VeritySEM, SEMVision; 계측·검사 전체 약 9.8%) | △ (Prexa는 테스트/프로버) | **KLA**(약 56~64%), Hitachi High-Tech, Nova, Onto, Camtek | [충돌] KLA 64.1%(2025) vs 약 56%. AMAT 9.8%·Nova 4.3% [추정] [Castellano substack](https://drrobertcastellano.substack.com/p/kla-camtek-and-nova-three-ways-to), [theindextimes](https://www.theindextimes.com/post/klac-kla-s-58-process-control-stranglehold-tightens-as-ai) |
| **본딩·패키징 장비** | ○ (도금·TSV식각·갭필, 본더 없음) | ○ (Kinex D2W HB with Besi + CMP·ECD·계측) | ○ (Synapse W2W·임시본딩, Ulucus LLO·박막화) | **EVG**(W2W 82%), **Besi**(D2W), **한미**(TCB 71.2%), ASMPT, Disco | [추정] EVG/TEL 82/17([SemiAnalysis](https://newsletter.semianalysis.com/p/austrias-silent-monopolies-on-advanced), 시점 불명), 한미 71.2% |
| **프로버** | – | – | ◎/○ (Prexa) | **Tokyo Seimitsu(Accretech)**, SEMES | [추정] 완전자동 프로버 Accretech·TEL·Semis CR3 약 70%(2024, QYResearch) [QY Research](https://www.qyresearch.com/news/10031/fully-automatic-wafer-test-prober). TEL 단독 % 확인 불가 |
| **노광(참고)** | – | – | – | **ASML** 독점(EUV) | WFE 1위 ASML(약 21.2%, 2025) [추정] amat.md 2-4 |

**[해석] 지도에서 읽히는 구도**
1. **Lam = 식각·증착 "깊이"형**: 도체·유전체 식각과 CVD/ECD에서 리더, 나머지는 거의 없다. 따라서 3D 구조 전환(NAND·GAA·4F²)의 수혜가 가장 직접적이지만, **NAND 사이클과 TEL 도전**에 가장 노출.
2. **AMAT = "폭"형**: PVD·Epi·CMP·이온주입에서 사실상 1위, 식각·ALD·계측에서는 2~3위. 신규 소재·패키징에서 **여러 공정을 묶어 파는 능력**이 차별점.
3. **TEL = "리소 독점+3대 공정 도전자"형**: 트랙 독점과 배치 열처리를 기반으로, 식각(극저온·GAA)·Mo 증착·본딩에서 점유율을 빼앗아 오는 전략.
4. **3사 밖의 강자**에 주의: 계측(KLA), 노광(ASML), ALD(ASM·Kokusai), 세정(SCREEN), 본딩(EVG·Besi·한미), CMP(Ebara). 면접에서 "3사만의 시장"처럼 말하면 감점 요인.

---

## 10. 3사 종합 기술 포지셔닝 (전략집용 요약)

| 관점 | Lam Research | Applied Materials | Tokyo Electron |
|---|---|---|---|
| 핵심 베팅 | 3D 수직화(NAND 고단·4F²/3D DRAM·GAA·BSPDN)로 식각·증착 강도↑ → SAM을 WFE의 high-30%로 [추정] | "재료공학" 통합 솔루션 + 패키징 + eBeam 계측. GAA·배선 served market 50%+ [추정] | 트랙 독점 유지(DICE·MOR) + 식각 점유 확대(극저온·GAA) + 본딩·LLO 신시장 |
| 2026 가장 강한 신호 | NAND 업그레이드 폭증(NVM 23%), Akara TOR, CSBG 사상 최대 [확정] | GAA 증설로 파운드리로직 사상 최대, 패키징 +70% [확정/추정] | C/D +50%, 식각 FY27 +25~30% 전망, 본딩 300억→1,000억 엔 계획 [추정] |
| 최대 리스크 | NAND 채널홀·Mo에서 TEL 2nd 벤더화 | 하이브리드 본딩 지연, 소수 로직 고객 의존 | 드라이 레지스트(Aether)의 트랙 잠식, 식각에서 POR 획득 속도 |
| 한국 고객 키 이슈 | 삼성 V10 극저온 식각 벤더 비율, SK 375단 Mo(TEL 선정 보도), SK Aether 채택 | SK 하이브리드 본딩 파일럿(Kinex), EPIC 공동개발, 삼성 SF2·SF2Z | 삼성 V10 극저온 식각, SK 375단 Mo 배치, DRAM 커패시터 POR, HBM 프로버 |
| 지원자 키워드 [해석] | HAR·극저온 식각, Mo ALD, 업그레이드, Dextro·EI | GAA 재료공학, HBM 공정 체인, eBeam, 구독형 서비스 | EUV 트랙·MOR, 극저온 식각 도전, 배치 퍼니스, 본딩·LLO |

---

## 11. 충돌·확인 불가 목록 (전략집 작성 시 체크)

1. **세그먼트 점유율 전반** [충돌]: 식각(AMAT 32% vs TEL 23% vs Lam 45% 등), 이온주입(AMAT 30~63%), CMP(42% vs 내부 70%), 열처리(TEL 15% vs 40%). → %를 쓰지 말고 ◎/○ 서술 권장.
2. **유전체 식각 리더** [충돌]: TEL "50%+" 주장 vs Lam NAND HAR 독점.
3. **삼성 V10 극저온 식각 벤더** [충돌]: "TEL 도입"(2023~2025 보도) vs "선정 최종 단계"(2026.6). 2026.10 최종 결과 확인 불가.
4. **SK하이닉스 375단 Mo 장비** [추정]: TEL 선정은 디일렉 단독 계열 보도. Lam ALTUS Halo의 "한국 NAND 업체 TOR" 고객 정체 확인 불가.
5. **HBM 하이브리드 본딩 시점** [충돌]: SK Hot Chips 2026 "HBM5 이후" vs 일부 요약 "2026 하반기 양산". → 최신 1차 발언(SK)을 우선.
6. **SK하이닉스 HBM4 양산 개시월** [충돌]: 2026.2 vs 2026 Q2.
7. **Lam 패키징 매출 성장률** [충돌]: +50% vs +70% (CY2026).
8. **ESPERT 도즈 저감** [충돌]: 30% vs 38%.
9. **삼성 SF2Z 양산** [충돌]: 2027 vs 2029.
10. **확인 불가**: Lam의 BSPDN 구체 TOR, TEL GAA POR 수치, TEL 프로버 단독 점유율, Ru 배선(Cu 대체) 양산 시점, 3D DRAM HVM 연도(2030년대 이후로만 추정), "WFE per 10k wafer starts" 형태의 회사 공식 수치(검색된 것은 모두 10만 WSPM 기준 $1B 형태).
11. **원문 미열람**: WebFetch 차단으로 모든 IR 원문(PDF·트랜스크립트)을 직접 읽지 못함. [확정] 표기도 "검색 요약에 회사 원문이 일치해 나타난 경우"임.

---

## 12. 출처 목록 (본문 인용 순서 무관, 주제별)

**Lam Research**
- Investor Day 2025 요약: https://quartr.com/events/lam-research-corporation-lrcx-investor-day-2025_33D7JGMm / 자료 PDF: https://filecache.investorroom.com/mr5ir_lamresearch2/1435/Lam%20Research%202025%20Investor%20Day%20FINAL.pdf
- Morgan Stanley 컨퍼런스(GAA·BSPDN $1B/100k): https://www.investing.com/news/transcripts/lam-research-at-morgan-stanley-conference-strategic-growth-in-focus-93CH-4539702
- Q4 FY26 콜: https://finance.yahoo.com/technology/articles/lam-research-q4-earnings-call-230406093.html / https://www.tradingview.com/news/zacks:c6805a50a094b:0-lrcx-q4-earnings-beat-on-nand-and-customer-support-strength/ / https://www.theglobeandmail.com/investing/markets/stocks/LRCX/pressreleases/3729596/lam-research-lrcx-q4-2026-earnings-call-transcript/ / https://finance.biggo.com/news/US_LRCX_2026-07-29
- WFE 전망·Aether 기회: https://finance.yahoo.com/technology/ai/articles/lam-research-lifts-2026-wfe-180229282.html
- Q3 FY26: https://www.investing.com/news/company-news/lam-research-q3-2026-slides-ai-drives-record-revenue-raises-outlook-93CH-4631007 / https://nikhs.substack.com/p/lam-research-3qfy26-more-than-a-cycle
- Cryo 3.0: https://newsroom.lamresearch.com/2024-07-31-Lam-Research-Introduces-Lam-Cryo-TM-3-0-Cryogenic-Etch-Technology-to-Accelerate-Scaling-of-3D-NAND-for-the-AI-Era / https://newsroom.lamresearch.com/introducing-lam-cryogenic-etching?blog=true / https://www.e4ds.com/sub_view.asp?idx=19495&lang=en
- Akara: https://investor.lamresearch.com/2025-02-19-Lam-Research-Unveils-Industrys-Most-Advanced-Conductor-Etch-Technology-to-Date / https://www.barchart.com/story/news/34425597/lrcx-s-akara-etch-wins-gain-momentum-can-it-expand-dram-share / https://www.thelec.net/news/articleView.html?idxno=5865
- ALTUS Halo: https://investor.lamresearch.com/2025-02-19-Lam-Research-Ushers-in-New-Era-of-Semiconductor-Metallization-with-ALTUS-R-Halo-for-Molybdenum-Atomic-Layer-Deposition
- Aether: https://www.prnewswire.com/news-releases/breakthrough-euv-dry-photoresist-technology-from-lam-research-adopted-by-leading-memory-manufacturer-302363785.html / https://electronics360.globalspec.com/article/18254/sk-hynix-to-use-dry-resist-euv-lithography-for-future-dram / IBM 협력: https://newsroom.ibm.com/2026-03-10-ibm-and-lam-research-announce-collaboration-to-advance-sub-1nm-logic-scaling
- 패키징·PLP: https://finance.yahoo.com/markets/stocks/articles/lam-research-lrcx-betting-advanced-200933179.html / https://newsroom.lamresearch.com/Lam-Research-Establishes-Panel-Level-Packaging-CoE / https://www.thelec.net/news/articleView.html?idxno=10758 / https://www.digitimes.com/news/a20260522PD223/lam-research-plp-panel-production-process-control-equipment.html / https://www.trendforce.com/news/2026/05/26/news-rapidus-reportedly-taps-lam-research-panel-level-packaging-system-for-600mm-square-glass-interposer-push/
- Dextro: https://www.prnewswire.com/news-releases/lam-research-introduces-the-semiconductor-industrys-first-collaborative-robot-for-fab-maintenance-optimization-302327247.html / https://www.therobotreport.com/lam-research-dextro-cobot-boosts-semiconductor-production-efficiency/ / EI: https://newsroom.lamresearch.com/what-is-equipment-intelligence-semi-101?blog=true

**Applied Materials**
- Q3 FY26: https://ir.appliedmaterials.com/static-files/e9985149-77c2-4cf3-aaad-a579178cbfe4 / https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-third-quarter-2026-results / https://futurumgroup.com/insights/applied-materials-q3-fy-2026-advanced-packaging-and-dram-accelerate-growth/ / https://www.investing.com/news/transcripts/earnings-call-transcript-applied-materials-beats-q3-2026-estimates-shares-fall-93CH-4859444
- Q1 FY26(GAA·배선 50%+): https://www.sec.gov/Archives/edgar/data/6951/000162828026007661/exhibit991q12026earningsre.htm / https://www.fool.com/earnings/call-transcripts/2026/02/12/applied-materials-amat-q1-2026-earnings-transcript/
- GAA/BSPDN $1B/100k: https://longyield.substack.com/p/applied-materials-and-the-angstrom / https://www.investing.com/news/company-news/applied-materials-advances-chip-performance-with-new-materials-93CH-3509902 / https://ir.appliedmaterials.com/static-files/394e84d2-f6ff-4ffd-a4d7-4b95bfddda22
- 2026 신제품: https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-unveils-transistor-and-wiring-innovations/ / https://www.stocktitan.net/news/AMAT/applied-materials-introduces-deposition-systems-for-angstrom-era-7v0938tplllx.html / https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-unveils-deposition-and-selective-etch-systems / https://www.globenewswire.com/news-release/2026/06/25/3317583/0/en/applied-materials-introduces-new-systems-to-accelerate-dram-and-advanced-packaging-for-ai-chips.html
- 배선(RuCo·Black Diamond): https://www.globenewswire.com/news-release/2024/07/08/2909540/0/en/applied-materials-unveils-chip-wiring-innovations-for-more-energy-efficient-computing.html
- Sculpta·패터닝: https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-expands-patterning-solutions-portfolio / https://www.globenewswire.com/news-release/2023/02/28/2616946/0/en/Applied-Materials-Innovative-Pattern-Shaping-Technology-Reduces-the-Cost-Complexity-and-Environmental-Impact-of-Advanced-Chip-Manufacturing.html
- Kinex·Besi: https://www.eetimes.com/applied-materials-besi-push-die-to-wafer-hybrid-bonding-toward-high-volume-manufacturing/ / https://www.globenewswire.com/news-release/2026/10/01/3372971/0/en/applied-materials-and-besi-expand-strategic-partnership-to-advance-next-generation-packaging-for-ai-scaling.html
- AGS·AIx: https://www.appliedmaterials.com/us/en/blog/blog-posts/subscription-services-provide-increased-value-to-chipmakers.html / https://www.tradingview.com/news/zacks:74395071c094b:0-can-amat-s-ags-business-become-a-long-term-growth-driver/ / https://www.tikr.com/blog/applied-materials-30-systems-outlook-is-the-headline-the-services-business-may-be-the-better-story
- DRAM 분석: https://404kresearch.substack.com/p/applied-materials-deep-dive-how-the / https://finance.yahoo.com/technology/ai/articles/amat-rides-ai-led-wfe-151900886.html

**Tokyo Electron**
- FY2026 Q4 콜: https://www.investing.com/news/transcripts/earnings-call-transcript-tokyo-electron-q4-2026-beats-estimates-stock-surges-93CH-4654441 / https://finance.yahoo.com/quote/8035.T/earnings/8035.T-Q4-2026-earnings_call-552866.html / https://ninescrolls.com/news/tokyo-electron-posts-record-jpy-2-44-trillion-fy2026-guides-first-half-fy2027 / https://finance.biggo.com/news/JP_8035.T_2026-04-30
- Q1 FY2027: https://www.investing.com/news/transcripts/earnings-call-transcript-tokyo-electron-q1-2026-beats-on-eps-shares-rise-62-93CH-4827853 / https://finance.biggo.com/news/JP_8035.T_2026-07-30 / https://www.investing.com/news/company-news/tokyo-electron-q1-fy2027-slides-ai-boom-drives-record-sales-outlook-93CH-4827886
- FY2026 Q2 transcript(차단, 검색 요약만): https://www.tel.com/ir/library/report/n0n82r00000000hl-att/fy26q2transcript-e.pdf
- 극저온 식각: https://www.nomadsemi.com/p/tokyo-electron-deep-dive-part-2 / https://www.yolegroup.com/industry-news/tokyo-electron-takes-aim-at-nand-etching-leader-lam-research/ / https://aei.dempa.net/archives/16308 / https://www.tel.com/blog/all/20241021_001.html / https://semianalysis.com/2023/07/16/nand-flash-monopoly-broken-tokyo
- 트랙·레지스트: https://newsletter.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle / https://euvlitho.com/2023/P44.pdf
- 본딩·LLO·프로버: https://www.tel.com/news/product/2024/20241209_001.html / https://www.tel.com/product/synapse-ulucus.html / https://www.tel.com/news/product/2026/20260416_001.html
- 자동화: https://www.tel.com/news/topics/2026/20260716_001.html / https://www.tel.com/sustainability/customer/field-solutions/index.html

**고객·기술 동향(한국 포함)**
- NAND: https://www.trendforce.com/news/2026/06/12/news-the-race-to-400-layer-nand-roadmaps-and-key-technologies-driving-samsung-sk-hynix-and-kioxia/ / https://www.thelec.net/news/articleView.html?idxno=11210 / https://www.memorymarket.com/a/14799 / https://www.smbom.com/news/40296 / https://x.com/Jukanlosreve/status/1893917099816587452 / https://www.techzine.eu/news/infrastructure/143432/samsung-unveils-v10-bv-nand-with-wafer-bonding-and-400-layers/ / https://wccftech.com/sk-hynix-races-samsung-to-400-layer-nand-must-abandon-tungsten-as-stacking-hits-a-wall/ / https://kantenna.com/topic/kioxia-sandisk-1000-layer-3d-nand-vlsi-2026-world-first
- Mo 시장: https://www.bitget.com/news/detail/12560605717420 / https://finance.biggo.com/news/132af702-c5dc-4719-8ab2-93b4217e4825
- DRAM 4F²: https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/ / https://www.digitimes.com/news/a20250620PD214/dram-samsung-sk-hynix-3d-development.html
- HBM: https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4 / https://www.trendforce.com/news/2026/01/26/news-samsung-reportedly-set-to-begin-official-hbm4-shipments-to-nvidia-and-amd-in-february/ / https://www.tomshardware.com/tech-industry/semiconductors/sk-hynix-says-hybrid-bonding-wont-be-ready-for-hbm4e-as-ai-memory-runs-into-a-775-micron-ceiling / https://ninescrolls.com/news/sk-hynix-rules-out-hybrid-bonding-for-hbm4e-775-micron-ceiling-keeps-mr-muf/ / https://www.trendforce.com/news/2026/04/29/news-sk-hynix-reportedly-completes-12-high-hybrid-bonding-hbm-validation-works-to-raise-yields-for-mass-production/ / https://eu.36kr.com/en/p/3407854283296132 / https://eu.36kr.com/en/p/3756077063209481 / https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation / https://www.thelec.net/news/articleView.html?idxno=6246 / https://x.com/jukan05/status/2038926893785788532?lang=en / https://www.trendforce.com/news/2026/06/09/news-sk-hynix-reportedly-places-44-2bn-won-tc-bonder-order-with-hanmi-accelerating-hbm4-ramp-up/ / https://www.trendforce.com/news/2025/12/12/news-sk-hynix-reportedly-places-hbm4-tc-bonder-order-with-asmpt-as-hanmi-hanwha-patent-clash-heats-up/ / https://introl.com/blog/south-korea-hbm4-stargate-memory-supercycle-2026
- 로직·BSPDN·High-NA: https://en.wikipedia.org/wiki/Backside_power_delivery / https://fiisual.com/blog/post/2026/bspdn-introduction / https://www.trendforce.com/news/2024/05/09/news-gearing-up-for-backside-power-delivery-heated-tech-war-between-tsmc-intel-and-samsung/ / https://semiengineering.com/backside-power-delivery-creates-fab-tool-thermal-dissipation-barriers/ / https://substack.com/@semivision/note/c-333551781 / https://www.trendforce.com/news/2025/12/19/news-samsung-officially-unveils-exynos-2600-industry-first-2nm-gaa-ap-with-113-ai-performance-uplift / https://www.techpowerup.com/345239/samsung-foundry-supposedly-achieves-50-yields-with-2-nm-gaa-node-process / https://www.trendforce.com/news/2026/02/16/news-asmls-high-na-euv-for-2027-28-which-giants-are-betting-big-intel-samsung-sk-hynix-or-tsmc/ / https://www.trendforce.com/news/2026/05/20/news-asml-expects-first-high-na-euv-memory-logic-products-within-months-amid-tsmcs-cost-driven-delay/ / https://www.digitimes.com/news/a20260813PD214/euv-sk-hynix-high-na-high-na-euv-dram.html / https://www.trendforce.com/news/2025/10/16/news-samsung-reportedly-purchasing-two-asml-high-na-euv-tools-for-mass-production-by-1h26/ / https://www.cnbc.com/2026/09/08/tsmc-samsung-asml-high-na-euv-machine-ai-chips.html / https://www.tweaktown.com/news/106957/sk-hynix-ramps-1c-dram-to-6-euv-layers-preps-for-high-na-designs-destroy-samsung-in-hbm
- CFET/포크시트: https://www.tomshardware.com/tech-industry/semiconductors/imecs-2026-roadmap-details-0-3nm-nodes-by-2038-cfet-transistors-become-viable-at-0-7nm-company-redefines-moores-law-as-cell-sizes-gain-importance-for-density / https://www.imec-int.com/en/articles/outer-wall-forksheet-bridge-nanosheet-and-cfet-device-architectures-logic-technology

**경쟁 지도(점유율)**
- 식각: https://www.mordorintelligence.com/industry-reports/semiconductor-etch-equipment-market / https://semiconductorinsight.com/blog/top-10-semiconductor-etch-equipment-market-companies/
- 계측: https://drrobertcastellano.substack.com/p/kla-camtek-and-nova-three-ways-to / https://www.theindextimes.com/post/klac-kla-s-58-process-control-stranglehold-tightens-as-ai
- CMP: https://www.globalgrowthinsights.com/market-reports/cmp-equipment-market-115415
- 이온주입: https://www.fortunebusinessinsights.com/ion-implanter-market-109422
- 세정: https://www.screen.co.jp/download_file/8ea7bfd9-acb0-494f-852a-7c14f39d901a/1211
- ALD·배치: https://www.gminsights.com/industry-analysis/ald-equipment-market / https://www.kokusai-electric.com/sites/default/files/2024-06/IRDay2024_Part2_textversion_Eng_240626.pdf / https://newsletter.semianalysis.com/p/going-vertical-gate-all-around-3d
- 본딩: https://newsletter.semianalysis.com/p/austrias-silent-monopolies-on-advanced
- 프로버: https://www.qyresearch.com/news/10031/fully-automatic-wafer-test-prober / https://www.mordorintelligence.com/industry-reports/wafer-prober-market
- WFE 구조: https://www.yolegroup.com/press-release/wafer-fab-equipment-wfe-market-to-hit-184-billion-by-2030-for-equipment-and-services-driven-by-specialized-segment-growth-and-global-manufacturing-shifts/
