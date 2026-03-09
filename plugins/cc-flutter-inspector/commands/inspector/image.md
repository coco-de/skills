---
name: inspector/image
description: "이미지 캐시 및 메모리 런타임 분석"
category: petmedi-development
complexity: simple
mcp-servers: [flutter-inspector]
---

# /inspector/image

> **Context Framework Note**: 이미지 관련 성능 문제 디버깅 시 활성화됩니다.

## Triggers

- 이미지 캐시 문제
- 메모리 사용량 경고
- 이미지 로딩 성능

## MCP Tools

### img_get_cache_stats
이미지 캐시 통계를 반환합니다.

**응답 예시**:
```json
{
  "cache": {
    "currentSize": 52428800,
    "currentSizeFormatted": "50 MB",
    "maximumSize": 104857600,
    "maximumSizeFormatted": "100 MB",
    "usagePercent": 50,
    "liveImageCount": 25
  },
  "memory": {
    "currentUsage": 157286400,
    "currentUsageFormatted": "150 MB"
  }
}
```

### img_analyze_warnings
이미지 관련 경고와 문제점을 분석합니다.

**파라미터**:
- `threshold`: 경고 임계값 (MB)

**응답 예시**:
```json
{
  "warnings": [
    {
      "type": "oversized",
      "severity": "high",
      "message": "이미지가 표시 크기보다 4배 큽니다",
      "image": "banner_home.png",
      "suggestion": "cacheWidth/cacheHeight 사용 권장"
    }
  ],
  "score": 65,
  "grade": "C"
}
```

### img_clear_cache
이미지 캐시를 정리합니다.

**파라미터**:
- `type`: 정리 유형 (all, memory, disk, expired)

## Common Diagnostics

### 메모리 경고
```
1. img_get_cache_stats → 현재 사용량 확인
2. img_analyze_warnings → 문제 이미지 식별
3. img_clear_cache → 캐시 정리
4. cacheWidth/cacheHeight 적용 검토
```

### 이미지 로딩 느림
```
1. img_get_cache_stats → 캐시 히트율 확인
2. /inspector/network → 다운로드 확인
3. 이미지 크기 최적화 검토
```

### 앱 크래시 (OOM)
```
1. img_get_cache_stats → 피크 메모리 확인
2. img_analyze_warnings → 오버사이즈 이미지 찾기
3. 큰 이미지 최적화 적용
4. 캐시 최대 크기 조정 검토
```

## Best Practices

### 이미지 로딩 패턴
```dart
// ✅ CORRECT: 캐시 크기 지정
Image.network(
  imageUrl,
  cacheWidth: 200,
  cacheHeight: 200,
)

// ✅ CORRECT: CachedNetworkImage 사용
CachedNetworkImage(
  imageUrl: imageUrl,
  memCacheWidth: 200,
  placeholder: (context, url) => CircularProgressIndicator(),
)

// ❌ WRONG: 원본 크기 로딩
Image.network(imageUrl)  // 4000x4000 이미지가 100x100에 표시
```

## Examples

### 캐시 상태 확인

```
/inspector/image stats
```

### 이미지 문제점 분석

```
/inspector/image warnings
```

### 캐시 정리

```
/inspector/image clear expired
```

## 참조

- 상세 구현: `.claude/agents/flutter-inspector-image.md`
- 마스터 인스펙터: `.claude/commands/inspector.md`
- 이미지 최적화: `.claude/agents/flutter-image-optimizer.md`
