# Flutter Widget Testing (Flutter 위젯 테스트)

## 트리거
- CoUI 컴포넌트의 렌더링과 인터랙션을 테스트할 때
- 새로운 화면이나 위젯의 동작을 검증할 때
- Golden 테스트(스크린샷 비교)를 작성할 때
- BLoC과 연동된 UI 동작을 테스트할 때

## 동작
1. 위젯 테스트 환경을 설정한다
   - `testWidgets()`로 테스트 케이스 작성
   - 필요한 상위 위젯(MaterialApp, BlocProvider 등)을 래핑
   - CoUI 테마 및 디자인 토큰 주입
2. 위젯 렌더링을 검증한다
   - `find.byType()`, `find.byKey()`, `find.text()`로 위젯 검색
   - `expect()`로 위젯 존재 여부 및 속성 검증
3. 사용자 인터랙션을 시뮬레이션한다
   - `tester.tap()`, `tester.enterText()`, `tester.drag()` 활용
   - `tester.pump()`, `tester.pumpAndSettle()`로 프레임 진행
4. Golden 테스트를 작성한다
   - `matchesGoldenFile()`로 스크린샷 비교
   - 다양한 화면 크기에서 Golden 이미지 생성
5. BLoC 연동 테스트를 작성한다
   - MockBloc으로 BLoC을 모킹
   - 특정 State에서의 UI 렌더링 검증

## 출력
- 위젯 테스트 코드 (`*_test.dart`)
- Golden 테스트 이미지 파일
- Mock BLoC 클래스 정의
- 테스트 유틸리티/헬퍼 함수

## 참고
- CoUI 컴포넌트 테스트 시 `CoTheme`을 반드시 주입하여 디자인 토큰이 적용된 상태에서 테스트한다
- `bloc_test` 패키지의 `MockBloc`과 `whenListen`을 활용하여 BLoC 상태를 제어한다
- Golden 테스트는 CI에서 플랫폼 간 폰트 렌더링 차이를 고려하여 Linux 환경에서 실행한다
- CoUI 컴포넌트의 반응형 동작을 테스트하려면 `MediaQuery`를 오버라이드하여 다양한 화면 크기를 시뮬레이션한다
