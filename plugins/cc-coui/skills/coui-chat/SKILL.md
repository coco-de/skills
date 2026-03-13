---
name: coui-chat
description: Activate when creating chat interfaces, message lists, chat bubbles, or messaging UIs using CouiChat/CouiChatBubble/CouiChatInput/ChatMessage/ChatSender (Flutter) or Chat/ChatBubble (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Chat

## Overview

The Chat component is a messaging interface consisting of message lists and input fields. It uses `ChatBubble` and `ChatInput` subcomponents to create a complete conversational UI.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
CouiChat(
  messages: [
    ChatMessage(
      id: '1',
      content: '안녕하세요!',
      sender: ChatSender.other,
      timestamp: DateTime.now(),
    ),
  ],
  onSend: (String text) => handleSendMessage(text),
  placeholder: '메시지를 입력하세요...',
)
```

### CouiChat Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `messages` | `List<ChatMessage>` | required | List of messages to display |
| `onSend` | `void Function(String)` | required | Callback when user sends a message |
| `placeholder` | `String` | `'메시지 입력...'` | Input field hint text |
| `isLoading` | `bool` | `false` | Shows loading indicator while awaiting responses |
| `maxInputLines` | `int` | `4` | Maximum input field height |

### ChatMessage Model

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `String` | Unique message identifier |
| `content` | `String` | Message text content |
| `sender` | `ChatSender` | Sender type (`me` or `other`) |
| `timestamp` | `DateTime?` | Optional timestamp |
| `avatar` | `Widget?` | Optional custom avatar widget |

### Loading State

```dart
CouiChat(
  messages: messages,
  onSend: handleSendMessage,
  isLoading: true,
)
```

### CouiChatBubble (Subcomponent)

```dart
CouiChatBubble(
  message: 'Hello!',
  sender: ChatSender.me,
  timestamp: DateTime.now(),
  avatar: Avatar(initials: 'JD'),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Chat(
  messages: [
    ChatMessage(
      id: '1',
      content: '안녕하세요!',
      sender: ChatSender.other,
      timestamp: DateTime.now(),
    ),
  ],
  onSend: handleSendMessage,
  placeholder: '메시지를 입력하세요...',
)
```

### ChatBubble (Web Subcomponent)

```dart
ChatBubble(
  message: 'Hello!',
  sender: ChatSender.me,
)
```

## Common Patterns

### Bidirectional Chat

Alternate between `ChatSender.me` and `ChatSender.other` to show conversation flow.

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Main widget | `CouiChat` | `Chat` |
| Bubble widget | `CouiChatBubble` | `ChatBubble` |
| Input widget | `CouiChatInput` | Built into `Chat` |
| Loading state | `isLoading` param | `isLoading` param |
| Max input lines | `maxInputLines` param | Not available |

### When to Use

- Messaging and chat applications
- AI/chatbot conversation interfaces
- Customer support chat widgets
- Comment threads with reply functionality
