---
created: 2025-12-21T01:41
updated: 2026-01-15T23:30
---

# Video Streaming

Session 영상 호스팅 및 스트리밍을 위해 **Cloudflare Stream**을 사용합니다.

## 서비스 선택 이유

| 기준             | Cloudflare Stream |
| ---------------- | ----------------- |
| 가격 구조        | 단순 (분 단위)    |
| 인코딩 비용      | 무료              |
| 대역폭 비용      | 무료 (포함)       |
| 접근 제어        | Signed URL 지원   |
| 초기/운영 비용   | 낮음              |
| 비용 예측 가능성 | 높음              |

## 가격 구조

| 항목              | 비용               |
| ----------------- | ------------------ |
| 비디오 저장       | $5 / 1,000분 (월)  |
| 비디오 전달(시청) | $1 / 1,000분       |
| 인코딩            | 무료               |
| 업로드            | 무료               |
| 대역폭            | 무료 (가격에 포함) |

### 예상 비용 (초기)

- 100개 강의 × 10분 = 1,000분 저장 → 월 $5
- 월 10,000분 시청 → $10
- **월 총 비용: 약 $15**

## 주요 기능

- **Adaptive Bitrate Streaming**: 네트워크 환경에 따라 품질 자동 조절
- **자동 인코딩**: 업로드 시 여러 품질로 자동 변환
- **Signed URL**: 유료 콘텐츠 접근 제어
- **내장 플레이어**: 별도 플레이어 개발 불필요
- **라이브 스트리밍**: 추후 라이브 강의 지원 가능

## 접근 제어 (Signed URL)

유료 Session 콘텐츠 보호를 위해 Signed URL 방식을 사용합니다.

### 동작 방식

1. 사용자가 Session 접근 요청
2. Backend에서 구독 상태 확인
3. 유효한 경우 Signed URL 생성 (만료 시간 포함)
4. Frontend에서 Signed URL로 영상 재생

### 구현 예시 (Backend)

```python
import cloudflare
from datetime import datetime, timedelta

def generate_signed_url(video_id: str, expires_in_hours: int = 2) -> str:
    expiry = datetime.utcnow() + timedelta(hours=expires_in_hours)
    # Cloudflare Stream API를 통해 서명된 토큰 생성
    return f"https://customer-{subdomain}.cloudflarestream.com/{video_id}/manifest/video.m3u8?token={token}"
```

## 제한 사항

- **DRM 미지원**: 완벽한 복제 방지는 불가 (Signed URL로 제한적 보호)
- **저장 용량 제한**: 초과 시 추가 구매 필요

## 로컬 개발 환경

개발 환경에서는 Cloudflare Stream 대신 **MinIO** (S3 호환 스토리지)를 사용합니다.

### Docker Compose 실행

```bash
cd infra/dev
docker compose up -d
```

### MinIO 접속 정보

| 항목       | 값                    |
| ---------- | --------------------- |
| API        | http://localhost:9000 |
| 웹 콘솔    | http://localhost:9001 |
| Access Key | minioadmin            |
| Secret Key | minioadmin            |
| 버킷       | videos                |

### 환경별 분기

| 환경        | VIDEO_PROVIDER | 스토리지          |
| ----------- | -------------- | ----------------- |
| development | local          | MinIO (Docker)    |
| staging     | cloudflare     | Cloudflare Stream |
| production  | cloudflare     | Cloudflare Stream |

## 대안 (필요 시)

DRM이 반드시 필요한 경우 Bunny Stream + DRM 고려:

- 월 $99 기본 요금 + 라이선스당 비용
- 완전한 콘텐츠 보호 가능
