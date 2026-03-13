---
name: coui-switch-field
description: Activate when creating switch fields, labeled toggles, settings toggles, or on/off switches with descriptions using SwitchField, SwitchField, SwitchSize in CoUI Flutter or CoUI Web.
---

# CoUI SwitchField

## Overview

The SwitchField is a form-friendly switch component with integrated label and optional secondary description. It combines toggle functionality with form field semantics. Flutter uses `SwitchField` while Web uses `SwitchField`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
SwitchField(
  value: isNotificationEnabled,
  onChanged: handleNotificationToggled,
  label: '알림 수신',
)
```

### With Description

```dart
SwitchField(
  value: isDarkMode,
  onChanged: handleDarkModeToggled,
  label: '다크 모드',
  description: '어두운 테마를 사용합니다',
  activeColor: Colors.indigo,
)
```

### Large Size

```dart
SwitchField(
  value: isAutoSave,
  onChanged: handleAutoSaveToggled,
  label: '자동 저장',
  description: '변경 사항을 자동으로 저장합니다',
  size: SwitchSize.lg,
)
```

### Settings Pattern

```dart
Column(
  children: [
    SwitchField(
      value: emailMarketing,
      onChanged: handleEmailMarketingToggled,
      label: '마케팅 이메일 수신',
    ),
    SwitchField(
      value: biometricLogin,
      onChanged: handleBiometricToggled,
      label: '생체 인증 로그인',
      description: '지문 또는 얼굴 인식으로 로그인합니다',
      activeColor: Colors.green,
    ),
  ],
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `bool` | required | Current switch state |
| `onChanged` | `ValueChanged<bool>?` | `null` | State change callback |
| `label` | `String` | required | Switch label text |
| `description` | `String?` | `null` | Secondary description text |
| `activeColor` | `Color?` | `null` | Activation color |
| `size` | `SwitchSize` | `SwitchSize.md` | Switch size (sm/md/lg) |
| `enabled` | `bool` | `true` | Enable/disable state |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
SwitchField(
  value: isNotificationEnabled,
  onChanged: handleNotificationToggled,
  label: '알림 수신',
)
```

### With Description

```dart
SwitchField(
  value: isDarkMode,
  onChanged: handleDarkModeToggled,
  label: '다크 모드',
  description: '어두운 테마를 사용합니다',
)
```

### Settings Form

```dart
Card(
  children: [
    CardHeader(
      child: CardTitle(titleChild: Component.text('Settings')),
    ),
    CardContent(
      children: [
        SwitchField(
          label: 'Dark mode',
          checked: isDarkMode,
          onChanged: (v) => setState(() => isDarkMode = v),
        ),
        SwitchField(
          label: 'Push notifications',
          description: 'Receive push notifications on your device.',
          checked: pushEnabled,
          onChanged: (v) => setState(() => pushEnabled = v),
        ),
      ],
    ),
  ],
)
```

## Common Patterns

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `SwitchField` | `SwitchField` |
| State prop | `value` | `checked` |
| Sizes | `SwitchSize.sm/md/lg` | Not specified |
| Active color | `activeColor` | Not supported |
