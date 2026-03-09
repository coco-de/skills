# Module Refactoring Patterns

모듈 리네이밍 및 리팩토링을 위한 가이드입니다.

## 모듈 리네이밍 절차

### 1. 디렉토리 이동

```bash
# 예: scm_sales_management → publisher_sales_management
mv feature/console/scm_sales_management feature/console/publisher_sales_management
```

### 2. pubspec.yaml 업데이트

```yaml
# feature/console/publisher_sales_management/pubspec.yaml
name: publisher_sales_management  # 패키지명 변경
```

### 3. 파일 리네이밍

| 기존 | 변경 |
|------|------|
| `scm_sales_management.dart` | `publisher_sales_management.dart` |
| `scm_sales_management_bloc.dart` | `publisher_sales_management_bloc.dart` |
| `scm_sales_management_page.dart` | `publisher_sales_management_page.dart` |
| `scm_sales_management_route.dart` | `publisher_sales_management_route.dart` |
| `i_scm_sales_management_repository.dart` | `i_publisher_sales_management_repository.dart` |

### 4. 클래스/타입 리네이밍

```dart
// 기존
class ScmSalesManagementBloc extends Bloc<...>
class ScmSalesManagementState
sealed class ScmSalesManagementEvent
class IScmSalesManagementRepository

// 변경
class PublisherSalesManagementBloc extends Bloc<...>
class PublisherSalesManagementState
sealed class PublisherSalesManagementEvent
class IPublisherSalesManagementRepository
```

### 5. Import 경로 업데이트

```dart
// 기존
import 'package:scm_sales_management/scm_sales_management.dart';

// 변경
import 'package:publisher_sales_management/publisher_sales_management.dart';
```

### 6. 라우터 업데이트

```dart
// console_router/lib/src/route/console_route.dart
import 'package:publisher_sales_management/publisher_sales_management.dart';

// 라우트 정의도 업데이트
TypedGoRoute<PublisherSalesManagementRoute>(
  path: '/publisher-sales',
  // ...
)
```

### 7. Melos Bootstrap

```bash
melos bootstrap
```

## 리네이밍 체크리스트

- [ ] 디렉토리 이동
- [ ] pubspec.yaml name 변경
- [ ] 메인 export 파일 리네이밍
- [ ] BLoC 파일들 리네이밍 (bloc, event, state)
- [ ] Page 파일 리네이밍
- [ ] Route 파일 리네이밍
- [ ] Repository 인터페이스/구현 리네이밍
- [ ] UseCase 내부 참조 업데이트
- [ ] Failure/Exception 클래스 리네이밍
- [ ] 모든 import 경로 업데이트
- [ ] Router 패키지 의존성 업데이트
- [ ] DI injector 업데이트
- [ ] 테스트 파일 업데이트
- [ ] melos bootstrap 실행
- [ ] 빌드 검증

## 일괄 치환 패턴

### VSCode 검색/치환

```
검색: scm_sales_management
치환: publisher_sales_management

검색: ScmSalesManagement
치환: PublisherSalesManagement

검색: scmSalesManagement
치환: publisherSalesManagement
```

### sed 명령어 (주의: 백업 필수)

```bash
# 파일 내용 치환
find feature/console/publisher_sales_management -name "*.dart" \
  -exec sed -i '' 's/ScmSalesManagement/PublisherSalesManagement/g' {} \;

find feature/console/publisher_sales_management -name "*.dart" \
  -exec sed -i '' 's/scm_sales_management/publisher_sales_management/g' {} \;
```

## 의존성 그래프 영향

모듈 리네이밍 시 영향받는 패키지:

```
publisher_sales_management
├── console_router (직접 의존)
├── app_kobic_console (간접 의존)
└── (기타 이 모듈을 참조하는 패키지)
```

## 흔한 실수

1. **Export 파일 누락**: 메인 export 파일의 export 경로 미업데이트
2. **라우터 의존성**: console_router pubspec.yaml에서 의존성명 미변경
3. **DI 등록**: GetIt 등록 코드 미업데이트
4. **테스트 파일**: 테스트 파일 내 import 미업데이트
5. **Generated 파일**: `.g.dart`, `.freezed.dart` 파일 재생성 필요

## 검증 명령어

```bash
# 빌드 검증
cd feature/console/publisher_sales_management
flutter analyze lib

# 전체 프로젝트 검증
melos run analyze --no-select
```
