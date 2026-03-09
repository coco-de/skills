# Serverpod Database 심화

Serverpod ORM과 PostgreSQL을 활용한 심화 데이터베이스 패턴. 필터, 관계, 트랜잭션, 잠금, 마이그레이션 전략을 다룹니다.

## 트리거

- ORM 쿼리 최적화, 복잡한 필터링
- 관계 로딩 (include, includeList)
- 트랜잭션, 잠금, 동시성 제어
- 마이그레이션 전략, repair migration

## CRUD 기본

```dart
var company = Company(name: 'Serverpod Inc.', foundedDate: DateTime.now());
company = await Company.db.insertRow(session, company);
var stored = await Company.db.findById(session, company.id);
company = company.copyWith(name: 'New Name');
await Company.db.updateRow(session, company);
await Company.db.deleteRow(session, company);
```

## 필터 API

`where` 콜백에서 테이블 디스크립터 `t`를 사용한 Fluent API:

```dart
var activeCompanies = await Company.db.find(session,
  where: (t) => t.name.ilike('a%') & (t.foundedDate > DateTime(2020)));
```

### 연산자

| 연산 | 예시 |
|------|------|
| 동등 | `t.column.equals(value)`, `t.column.notEquals(value)` |
| 비교 | `>`, `>=`, `<`, `<=` (int/double/Duration/DateTime) |
| 범위 | `t.column.between(a, b)`, `notBetween` |
| 집합 | `t.column.inSet(set)`, `notInSet` |
| 문자열 | `t.column.like('A%')` (대소문자 구분), `ilike` (무시) |
| 조합 | `&` (AND), `\|` (OR), `~` (NOT) |

### 관계 필터

```dart
// 1:1 관계 필터
where: (t) => t.address.street.like('%road%')

// 1:N 관계 필터
where: (t) => t.orders.count() > 3
where: (t) => t.orders.count((o) => o.itemType.equals('book')) > 3
where: (t) => t.orders.none()
where: (t) => t.orders.any()
where: (t) => t.orders.any((o) => o.status.equals('active'))
where: (t) => t.orders.every((o) => o.isPaid.equals(true))
```

## 정렬 & 페이지네이션

```dart
// 단일 정렬
orderBy: (t) => t.column
orderDescending: true

// 복합 정렬
orderByList: (t) => [
  Order(column: t.name, orderDescending: true),
  Order(column: t.id),
]

// 관계 기준 정렬
orderBy: (t) => t.ceo.name
orderBy: (t) => t.employees.count()
```

### 페이지네이션 전략

```dart
// Offset 기반 (간단, 대규모 데이터셋에서 느림)
limit: pageSize, offset: page * pageSize

// Cursor 기반 (대규모 데이터셋에 적합)
where: (t) => t.id > lastId
orderBy: (t) => t.id
limit: pageSize
```

## 관계 로딩 (Include)

```dart
// 1:1 include
var employee = await Employee.db.findById(session, id,
  include: Employee.include(address: Address.include()));

// 1:N includeList (필터, 정렬, 페이지네이션 지원)
var company = await Company.db.findById(session, id,
  include: Company.include(
    employees: Employee.includeList(
      where: (t) => t.name.ilike('a%'),
      orderBy: (t) => t.name,
      limit: 10,
      includes: Employee.include(address: Address.include()),
    ),
  ));
```

### Attach / Detach

```dart
// 관계 연결
await Company.db.attachRow.employees(session, company, employee);
await Company.db.attach.employees(session, company, [e1, e2]);

// 관계 해제
await Company.db.detachRow.employees(session, employee);
```

## 트랜잭션

```dart
await session.transaction((tx) async {
  await Company.db.insertRow(tx, company);
  await OtherModel.db.updateRow(tx, other);
  // tx 사용 (session 아님)
});
```

## Row 잠금

트랜잭션 내에서만 사용. `lockMode` + `transaction` 파라미터:

```dart
await session.transaction((tx) async {
  // 배타적 잠금
  var rows = await Company.db.find(session,
    where: (t) => t.id.equals(companyId),
    lockMode: LockMode.forUpdate,
    transaction: tx,
  );

  // 작업 수행
  rows[0] = rows[0].copyWith(balance: rows[0].balance - amount);
  await Company.db.updateRow(tx, rows[0]);
});
```

| LockMode | 설명 |
|----------|------|
| `forUpdate` | 배타적 잠금 |
| `forNoKeyUpdate` | 키 외 컬럼만 잠금 |
| `forShare` | 공유 잠금 |
| `forKeyShare` | 키 공유 잠금 |

| LockBehavior | 설명 |
|--------------|------|
| `wait` | 대기 (기본) |
| `noWait` | 즉시 실패 |
| `skipLocked` | 잠긴 행 건너뜀 (Job Queue에 적합) |

## 런타임 파라미터

```dart
// 전역 설정 (Serverpod 초기화 시)
runtimeParametersBuilder: (params) => [
  params.searchPaths(['my_schema', 'public'])
]

// 트랜잭션별 설정
await tx.setRuntimeParameters(...)
```

## 마이그레이션

```bash
# 마이그레이션 생성
serverpod create-migration
serverpod create-migration --force --tag "v1"

# 마이그레이션 적용
dart run bin/main.dart --apply-migrations

# 스크립트에서 적용 (성공 시 exit 0)
dart run bin/main.dart --role maintenance --apply-migrations
```

### Repair Migration

DB가 마이그레이션 외부에서 변경된 경우:

```bash
serverpod create-repair-migration
serverpod create-repair-migration --mode production --version <name>
dart run bin/main.dart --apply-repair-migration
```

## 체크리스트

- [ ] 쿼리에 적절한 인덱스 활용
- [ ] N+1 문제 방지 (include 사용)
- [ ] 트랜잭션으로 원자적 작업 보장
- [ ] 대규모 데이터셋에 cursor 기반 페이지네이션
- [ ] 동시성 제어가 필요한 곳에 row 잠금
- [ ] 마이그레이션 생성 후 반드시 적용
