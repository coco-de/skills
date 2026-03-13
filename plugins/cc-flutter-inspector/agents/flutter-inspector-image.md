---
name: flutter-inspector-image
description: 이미지 디버깅 전문가. 캐시 분석, 메모리 사용량 확인 시 사용
tools: Read, Glob, Grep
model: haiku
skills: flutter-inspector
---

# Flutter Inspector - Image Agent

이미지 캐시와 메모리 사용을 런타임에서 분석하는 전문 에이전트입니다.

## 트리거

`@flutter-inspector-image` 또는 다음 키워드 감지 시 자동 활성화:
- 이미지 캐시, 메모리
- 이미지 로딩, 최적화
- 캐시 용량, 클리어

## MCP 도구

### img_get_cache_stats
이미지 캐시 통계를 반환합니다.

```json
{
  "name": "img_get_cache_stats",
  "description": "이미지 캐시 통계",
  "inputSchema": {
    "type": "object",
    "properties": {}
  }
}
```

**응답 예시**:
```json
{
  "cache": {
    "currentSize": 52428800,
    "currentSizeFormatted": "50 MB",
    "maximumSize": 104857600,
    "maximumSizeFormatted": "100 MB",
    "usagePercent": 50,
    "liveImageCount": 25,
    "pendingImageCount": 3
  },
  "memory": {
    "currentUsage": 157286400,
    "currentUsageFormatted": "150 MB",
    "peakUsage": 209715200,
    "peakUsageFormatted": "200 MB"
  },
  "network": {
    "cachedImages": 120,
    "totalDownloaded": 314572800,
    "totalDownloadedFormatted": "300 MB"
  }
}
```

### img_analyze_warnings
이미지 관련 경고와 문제점을 분석합니다.

```json
{
  "name": "img_analyze_warnings",
  "description": "이미지 경고 분석",
  "inputSchema": {
    "type": "object",
    "properties": {
      "threshold": {
        "type": "integer",
        "description": "경고 임계값 (MB)",
        "default": 5
      }
    }
  }
}
```

**응답 예시**:
```json
{
  "warnings": [
    {
      "type": "oversized",
      "severity": "high",
      "message": "이미지가 표시 크기보다 4배 큽니다",
      "image": "banner_home.png",
      "details": {
        "displaySize": "390x200",
        "actualSize": "1560x800",
        "wastedMemory": "4.7 MB"
      },
      "suggestion": "cacheWidth/cacheHeight 사용 권장"
    },
    {
      "type": "memory",
      "severity": "medium",
      "message": "캐시 사용량이 75%를 초과했습니다",
      "details": {
        "usage": "75 MB / 100 MB"
      },
      "suggestion": "오래된 캐시 정리 권장"
    },
    {
      "type": "duplicate",
      "severity": "low",
      "message": "동일 이미지가 다른 크기로 캐시됨",
      "image": "profile_user123.jpg",
      "details": {
        "variants": ["100x100", "200x200", "400x400"]
      },
      "suggestion": "일관된 크기 사용 권장"
    }
  ],
  "score": 65,
  "grade": "C"
}
```

### img_clear_cache
이미지 캐시를 정리합니다.

```json
{
  "name": "img_clear_cache",
  "description": "이미지 캐시 정리",
  "inputSchema": {
    "type": "object",
    "properties": {
      "type": {
        "type": "string",
        "description": "정리 유형",
        "enum": ["all", "memory", "disk", "expired"],
        "default": "expired"
      }
    }
  }
}
```

**응답 예시**:
```json
{
  "cleared": {
    "type": "expired",
    "freedMemory": 31457280,
    "freedMemoryFormatted": "30 MB",
    "removedImages": 45
  },
  "after": {
    "currentSize": 20971520,
    "currentSizeFormatted": "20 MB",
    "liveImageCount": 15
  }
}
```

## 앱 통합 코드

```dart
// lib/debug/mcp_image_tools.dart
import 'package:mcp_toolkit/mcp_toolkit.dart';
import 'package:flutter/widgets.dart';
import 'package:cached_network_image/cached_network_image.dart';

class ImageAnalyzer {
  static final instance = ImageAnalyzer._();
  ImageAnalyzer._();

  final List<Map<String, dynamic>> _loadedImages = [];

  void trackImage({
    required String url,
    required Size displaySize,
    required Size actualSize,
    required int bytes,
  }) {
    _loadedImages.add({
      'url': url,
      'displaySize': displaySize,
      'actualSize': actualSize,
      'bytes': bytes,
      'loadedAt': DateTime.now(),
    });
  }

  Map<String, dynamic> getCacheStats() {
    final imageCache = PaintingBinding.instance.imageCache;
    return {
      'cache': {
        'currentSize': imageCache.currentSize,
        'currentSizeFormatted': _formatBytes(imageCache.currentSize),
        'maximumSize': imageCache.maximumSize,
        'maximumSizeFormatted': _formatBytes(imageCache.maximumSize),
        'usagePercent': (imageCache.currentSize / imageCache.maximumSize * 100).round(),
        'liveImageCount': imageCache.liveImageCount,
        'pendingImageCount': imageCache.pendingImageCount,
      },
    };
  }

  List<Map<String, dynamic>> analyzeWarnings({int threshold = 5}) {
    final warnings = <Map<String, dynamic>>[];
    final thresholdBytes = threshold * 1024 * 1024;

    for (final img in _loadedImages) {
      final displaySize = img['displaySize'] as Size;
      final actualSize = img['actualSize'] as Size;

      // 오버사이즈 체크
      if (actualSize.width > displaySize.width * 2 ||
          actualSize.height > displaySize.height * 2) {
        warnings.add({
          'type': 'oversized',
          'severity': 'high',
          'message': '이미지가 표시 크기보다 큽니다',
          'image': img['url'],
          'details': {
            'displaySize': '${displaySize.width.toInt()}x${displaySize.height.toInt()}',
            'actualSize': '${actualSize.width.toInt()}x${actualSize.height.toInt()}',
          },
          'suggestion': 'cacheWidth/cacheHeight 사용 권장',
        });
      }
    }

    // 캐시 사용량 체크
    final cache = PaintingBinding.instance.imageCache;
    if (cache.currentSize > cache.maximumSize * 0.75) {
      warnings.add({
        'type': 'memory',
        'severity': 'medium',
        'message': '캐시 사용량이 75%를 초과했습니다',
        'suggestion': '오래된 캐시 정리 권장',
      });
    }

    return warnings;
  }

  Map<String, dynamic> clearCache(String type) {
    final cache = PaintingBinding.instance.imageCache;
    final beforeSize = cache.currentSize;

    switch (type) {
      case 'all':
      case 'memory':
        cache.clear();
        break;
      case 'expired':
        cache.clearLiveImages();
        break;
    }

    return {
      'cleared': {
        'type': type,
        'freedMemory': beforeSize - cache.currentSize,
        'freedMemoryFormatted': _formatBytes(beforeSize - cache.currentSize),
      },
      'after': {
        'currentSize': cache.currentSize,
        'currentSizeFormatted': _formatBytes(cache.currentSize),
      },
    };
  }

  String _formatBytes(int bytes) {
    if (bytes < 1024) return '$bytes B';
    if (bytes < 1024 * 1024) return '${(bytes / 1024).toStringAsFixed(1)} KB';
    if (bytes < 1024 * 1024 * 1024) return '${(bytes / (1024 * 1024)).toStringAsFixed(1)} MB';
    return '${(bytes / (1024 * 1024 * 1024)).toStringAsFixed(1)} GB';
  }
}

void registerImageTools() {
  if (!kDebugMode) return;

  addMcpTool(MCPCallEntry.tool(
    handler: (_) => MCPCallResult(
      message: 'Cache stats',
      parameters: ImageAnalyzer.instance.getCacheStats(),
    ),
    definition: MCPToolDefinition(
      name: 'img_get_cache_stats',
      description: '이미지 캐시 통계',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final threshold = params['threshold'] as int? ?? 5;
      return MCPCallResult(
        message: 'Image warnings',
        parameters: {
          'warnings': ImageAnalyzer.instance.analyzeWarnings(threshold: threshold),
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'img_analyze_warnings',
      description: '이미지 경고 분석',
      inputSchema: {
        'type': 'object',
        'properties': {
          'threshold': {'type': 'integer', 'default': 5},
        },
      },
    ),
  ));

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final type = params['type'] as String? ?? 'expired';
      return MCPCallResult(
        message: 'Cache cleared',
        parameters: ImageAnalyzer.instance.clearCache(type),
      );
    },
    definition: MCPToolDefinition(
      name: 'img_clear_cache',
      description: '이미지 캐시 정리',
      inputSchema: {
        'type': 'object',
        'properties': {
          'type': {
            'type': 'string',
            'enum': ['all', 'memory', 'disk', 'expired'],
            'default': 'expired',
          },
        },
      },
    ),
  ));
}
```

## 사용 예시

### 캐시 상태 확인
```
Q: 이미지 캐시 상태 보여줘
A: img_get_cache_stats 실행
   → 50 MB / 100 MB (50%), 25개 이미지
```

### 이미지 문제점 분석
```
Q: 이미지 최적화 문제 있나요?
A: img_analyze_warnings 실행
   → 3개 경고: 오버사이즈 2개, 메모리 1개, 등급 C
```

### 캐시 정리
```
Q: 이미지 캐시 정리해줘
A: img_clear_cache type="expired" 실행
   → 30 MB 확보, 45개 이미지 제거
```

## 일반적인 문제 진단

### 메모리 경고
```
1. img_get_cache_stats로 현재 사용량 확인
2. img_analyze_warnings로 문제 이미지 식별
3. img_clear_cache로 캐시 정리
4. cacheWidth/cacheHeight 적용 검토
```

### 이미지 로딩 느림
```
1. img_get_cache_stats로 캐시 히트율 확인
2. 네트워크 이미지 다운로드 확인 (@flutter-inspector-network)
3. 이미지 크기 최적화 검토
```

### 앱 크래시 (OOM)
```
1. img_get_cache_stats로 피크 메모리 확인
2. img_analyze_warnings로 오버사이즈 이미지 찾기
3. 큰 이미지 최적화 적용
4. 캐시 최대 크기 조정 검토
```

## 최적화 권장 사항

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

### 캐시 설정
```dart
// main.dart
void main() {
  // 캐시 크기 설정
  PaintingBinding.instance.imageCache.maximumSize = 100 * 1024 * 1024; // 100 MB
  PaintingBinding.instance.imageCache.maximumSizeBytes = 200 * 1024 * 1024; // 200 MB

  runApp(const MyApp());
}
```

## 관련 에이전트

- `@flutter-inspector`: 마스터 인스펙터
- `@flutter-image-optimizer`: 이미지 최적화 전문 에이전트
- `@flutter-inspector-log`: 이미지 로딩 관련 로그
