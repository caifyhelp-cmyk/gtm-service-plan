from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER

FONT = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"

pdfmetrics.registerFont(TTFont("Nanum", FONT))
pdfmetrics.registerFont(TTFont("NanumB", FONT_BOLD))

W, H = A4
M = 20 * mm

def s(name, **kw):
    base = dict(fontName="Nanum", fontSize=10, leading=16, textColor=colors.HexColor("#333333"))
    base.update(kw)
    return ParagraphStyle(name, **base)

ST = {
    "title":  s("title",  fontName="NanumB", fontSize=22, leading=30, textColor=colors.HexColor("#111111"), spaceAfter=4),
    "meta":   s("meta",   fontSize=9, textColor=colors.HexColor("#888888"), spaceAfter=12),
    "h2":     s("h2",     fontName="NanumB", fontSize=14, leading=20, textColor=colors.HexColor("#1a4fc4"), spaceBefore=14, spaceAfter=4),
    "h3":     s("h3",     fontName="NanumB", fontSize=11, leading=16, textColor=colors.HexColor("#222222"), spaceBefore=8, spaceAfter=2),
    "body":   s("body",   spaceAfter=4),
    "code":   s("code",   fontName="Nanum", fontSize=9, leading=14, backColor=colors.HexColor("#f5f5f5"), textColor=colors.HexColor("#222222"), leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=8, borderPad=4),
    "quote":  s("quote",  fontName="NanumB", fontSize=12, leading=20, textColor=colors.HexColor("#1a4fc4"), leftIndent=12, spaceAfter=8),
}

def p(text, style="body"):
    return Paragraph(text.replace("\n", "<br/>"), ST[style])

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"), spaceAfter=8, spaceBefore=4)

def tbl(headers, rows, col_w=None):
    n = len(headers)
    usable = W - 2 * M
    if col_w is None:
        col_w = [usable / n] * n
    data = [headers] + rows
    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ("FONTNAME",    (0,0), (-1,0),  "NanumB"),
        ("FONTNAME",    (0,1), (-1,-1), "Nanum"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("LEADING",     (0,0), (-1,-1), 14),
        ("BACKGROUND",  (0,0), (-1,0),  colors.HexColor("#e6ebff")),
        ("TEXTCOLOR",   (0,0), (-1,-1), colors.HexColor("#222222")),
        ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#bbbbbb")),
        ("TOPPADDING",  (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#fafafa")]),
    ]))
    return t

def sp(h=6):
    return Spacer(1, h)

def make_pdf():
    out = "/root/gtm-service-plan/GTM_서비스기획_카이파이_20260530.pdf"
    doc = SimpleDocTemplate(out, pagesize=A4,
                            leftMargin=M, rightMargin=M,
                            topMargin=M+5*mm, bottomMargin=M)
    story = []
    uw = W - 2 * M  # usable width

    # ── 표지 ─────────────────────────────────────────
    story += [
        p("GTM+GA4 자동화 서비스 기획 로그", "title"),
        p("작성일: 2026-05-30  |  카이파이(Caify) 신규 서비스 기획", "meta"),
        hr(), sp(4),
    ]

    # ── 1. 서비스 개요 ────────────────────────────────
    story += [p("1. 서비스 개요", "h2")]
    story += [p("아이디어", "h3")]
    story += [p("채팅 + AI 에이전트 방식으로 고객이 GTM/GA4 설정을 자연어로 말하면,\n구글 공식 문서를 탐색하고 자동으로 태그/트리거/변수를 생성 및 적용하는 서비스."), sp()]
    story += [p("핵심 가치", "h3")]
    story += [p("• 코드 몰라도 GTM+GA4 세팅 완료\n• 세팅 후 지속적인 성과 리포트 제공\n• 마케팅 실행(카이파이) + 성과 측정 풀사이클 연결"), sp(), hr()]

    # ── 2. 기술 구조 ──────────────────────────────────
    story += [p("2. 기술 구조", "h2")]
    story += [p("전체 파이프라인", "h3")]
    story += [p("[채팅 입력] → [AI 에이전트] → [GTM 설정 JSON] → [GTM API 자동 적용]", "code")]
    story += [p("GTM API v2", "h3")]
    story += [p("공식 Google Tag Manager API v2 존재. 태그/트리거/변수 생성 + publish까지 완전 자동화 가능.\nDOM 자동화(셀레니움) 불필요, 안정적."), sp()]
    story += [p("인증 구조 (부업 모델)", "h3")]
    story += [p("고객이 GTM에 caifyhelp@gmail.com 편집자 추가\n→ 우리 계정 1개로 모든 고객 GTM 접근 가능\n→ GCP OAuth 앱 1회 등록으로 완료", "code")]
    story += [hr()]

    # ── 3. 서비스 로직 ────────────────────────────────
    story += [p("3. 서비스 로직 전체 플로우", "h2")]
    story += [p("의뢰 접수 시 고객에게 받는 것", "h3")]
    story += [p("1. GTM에 편집자 추가 요청\n2. 어떤 이벤트 / 플랫폼(카페24·고도몰·워드프레스) / 발생 시점 / 추적 데이터"), sp()]
    story += [p("서비스 범위", "h3"), sp(2)]
    story += [tbl(
        ["항목", "자동화", "수동"],
        [
            ["GTM 태그/트리거/변수 생성", "✅ API", ""],
            ["GTM publish", "✅ API", ""],
            ["데이터레이어 코드 생성", "✅ AI", ""],
            ["삽입 가이드", "✅ 자동", ""],
            ["실제 코드 삽입", "", "✅ 고객 직접"],
        ],
        [uw*0.5, uw*0.25, uw*0.25]
    ), sp(6), hr()]

    # ── 4. 시장 조사 ──────────────────────────────────
    story += [p("4. 시장 조사 (한국 기준)", "h2")]
    story += [p("국내 GTM AI 자동화 도구: 없음 (블루오션)\n글로벌 MCP 서버: 오픈소스 존재하나 개발자용, 비포장 상태"), sp()]
    story += [p("크몽 실거래 데이터", "h3"), sp(2)]
    story += [tbl(
        ["서비스", "거래 건수", "가격대"],
        [
            ["GA4+GTM 세팅 A", "328건", "3.3~18만원"],
            ["GA4+GTM 세팅 B", "5건", "10~70만원"],
        ],
        [uw*0.5, uw*0.25, uw*0.25]
    ), sp(4)]
    story += [p("→ 수동으로 해줘도 328번 팔림. 수요 검증 완료."), sp()]
    story += [p("기존 경쟁자 대비 차별점", "h3"), sp(2)]
    story += [tbl(
        ["항목", "기존 프리랜서", "우리"],
        [
            ["방식", "수동 세팅", "AI 자동화"],
            ["처리 시간", "2~5시간", "10~20분"],
            ["리포트", "없음", "지속 제공"],
            ["한국 플랫폼 특화", "경험 의존", "학습된 템플릿"],
        ],
        [uw*0.35, uw*0.325, uw*0.325]
    ), sp(6), hr()]

    # ── 5. 카이파이 연계 ──────────────────────────────
    story += [p("5. 카이파이(Caify)와의 연계", "h2")]
    story += [tbl(
        ["서비스", "가격"],
        [
            ["블로그 자동화", "30만원/월"],
            ["홈페이지 제작", "30만원/월"],
            ["숏폼 영상 자동화", "30만원/월"],
        ],
        [uw*0.6, uw*0.4]
    ), sp(4)]
    story += [p("연계 구조", "h3")]
    story += [p("GTM+GA4 세팅 (저가, 1회성)\n    ↓ 신뢰 형성\nGA4 데이터로 '블로그/영상 유입 부족' 확인\n    ↓\n카이파이 제안 → 구독 → 성과 데이터\n    ↓\n루프: 콘텐츠 생산 → 성과 측정 → 콘텐츠 개선", "code")]
    story += [hr()]

    # ── 6. 리포트 구조 ────────────────────────────────
    story += [p("6. 리포트 구조 (A안)", "h2")]
    story += [p("커뮤니케이션 구조", "h3"), sp(2)]
    story += [tbl(
        ["타이밍", "내용", "채널"],
        [
            ["즉시 (GTM Webhook)", "전화/카카오 클릭 알림", "카카오 알림톡"],
            ["매주 월요일", "지난주 3줄 요약", "카카오 알림톡"],
            ["매월 1일", "종합 분석 + 액션", "카카오/이메일"],
            ["이상 감지 시", "트래픽 급변 알림", "즉시"],
        ],
        [uw*0.32, uw*0.4, uw*0.28]
    ), sp(6)]
    story += [p("리포트 샘플", "h3")]
    story += [p(
        "📊 5월 성과 요약\n\n"
        "✅ 이번 달 347명 방문 (지난달+23%)\n"
        "   전화번호 클릭 12번 / 블로그 유입 68%\n\n"
        "📍 유입 채널: 블로그 68% / 인스타 21% / 검색 8%\n\n"
        "🏆 1위 콘텐츠: '강남 냉삼 맛집' → 89명 유입\n\n"
        "⚠️  3주차 방문자 -40% → 블로그 발행 없었던 주\n\n"
        "📌 다음달 액션\n"
        "   1. '강남 회식 장소' 주제 글 작성\n"
        "   2. 모바일 전화버튼 상단 이동 (83%가 모바일)\n"
        "   3. 인스타 화요일 오전 발행 (유입 최다)", "code")]
    story += [hr()]

    # ── 7. A안 vs B안 ─────────────────────────────────
    story += [p("7. 방향성 A vs B", "h2"), sp(2)]
    story += [tbl(
        ["항목", "A안 (범위 축소)", "B안 (완전 추적)"],
        [
            ["출시 기간", "1~2개월", "3~4개월"],
            ["전화 추적", "클릭만", "실제 통화 완료"],
            ["세팅 가격", "3.9만원", "9.9만원"],
            ["리포트 가격", "2.9만원/월", "7.9만원/월"],
            ["경쟁력", "보통", "강함"],
        ],
        [uw*0.32, uw*0.34, uw*0.34]
    ), sp(4)]
    story += [p("추천 전략", "h3")]
    story += [p("A안으로 빠르게 출시 → 고객 50명 확보\n→ 업종별 벤치마크 데이터 구축\n→ B안으로 진화 (콜 트래킹 + 네이버/카카오 API)", "code")]
    story += [hr()]

    # ── 8. 데이터 모트 ────────────────────────────────
    story += [p("8. 장기 차별점 (데이터 모트)", "h2")]
    story += [p("고객이 쌓일수록 업종별 전환율 벤치마크 자동 구축."), sp(2)]
    story += [p(
        "'사장님 전환율이 치킨집 평균보다 2.6배 높아요'\n"
        "→ 이 데이터는 우리만 가능\n"
        "→ ChatGPT, 크몽 프리랜서 불가\n"
        "→ 고객 많을수록 서비스 정확도 향상 → 진입 장벽", "code")]
    story += [p("초기 데이터 없는 시기: Think with Google 공개 업종별 벤치마크 활용"), hr()]

    # ── 9. 포지셔닝 ───────────────────────────────────
    story += [p("9. 최종 포지셔닝", "h2"), sp(4)]
    story += [p(
        '"마케팅 했는데 왜 안 되는지 모르는 소상공인을 위한,<br/>'
        '실행부터 성과까지 자동으로 연결해주는 서비스"', "quote")]

    doc.build(story)
    print(f"PDF 생성 완료: {out}")

if __name__ == "__main__":
    make_pdf()
