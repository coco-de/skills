/// The entrypoint for the **server** environment.
library;

import 'package:jaspr/server.dart';

import 'package:jaspr_content/components/callout.dart';

import 'package:jaspr_content/components/header.dart';
import 'package:jaspr_content/components/image.dart';
import 'package:jaspr_content/components/sidebar.dart';
import 'package:jaspr_content/components/theme_toggle.dart';
import 'package:jaspr_content/jaspr_content.dart';
import 'package:jaspr_content/theme.dart';

import 'main.server.options.dart';

const base = '/skills';

void main() {
  Jaspr.initializeApp(
    options: defaultServerOptions,
  );

  runApp(
    ContentApp(
      templateEngine: MustacheTemplateEngine(),
      parsers: [
        MarkdownParser(),
      ],
      extensions: [
        HeadingAnchorsExtension(),
        TableOfContentsExtension(),
      ],
      components: [
        Callout(),
        Image(zoom: true),
      ],
      layouts: [
        DocsLayout(
          header: Header(
            title: 'Cocode Skills',
            logo: '$base/images/logo.svg',
            items: [
              ThemeToggle(),
            ],
          ),
          sidebar: Sidebar(
            groups: [
              SidebarGroup(
                links: [
                  SidebarLink(text: 'Overview', href: '$base/'),
                  SidebarLink(text: '시작하기', href: '$base/getting-started'),
                ],
              ),
              SidebarGroup(
                title: 'Plugins',
                links: [
                  SidebarLink(
                      text: '방법론 & 워크플로우',
                      href: '$base/plugins/methodology'),
                  SidebarLink(
                      text: '  cc-bmad', href: '$base/plugins/cc-bmad/'),
                  SidebarLink(
                      text: '  cc-workflow',
                      href: '$base/plugins/cc-workflow/'),
                  SidebarLink(
                      text: '  cc-code-quality',
                      href: '$base/plugins/cc-code-quality/'),
                  SidebarLink(
                      text: 'Flutter 개발', href: '$base/plugins/flutter'),
                  SidebarLink(
                      text: '  cc-coui', href: '$base/plugins/cc-coui/'),
                  SidebarLink(
                      text: '  cc-flutter-dev',
                      href: '$base/plugins/cc-flutter-dev/'),
                  SidebarLink(
                      text: '  cc-flutter-inspector',
                      href: '$base/plugins/cc-flutter-inspector/'),
                  SidebarLink(
                      text: '  cc-i18n', href: '$base/plugins/cc-i18n/'),
                  SidebarLink(
                      text: '백엔드 & 분석', href: '$base/plugins/backend'),
                  SidebarLink(
                      text: '  cc-serverpod',
                      href: '$base/plugins/cc-serverpod/'),
                  SidebarLink(
                      text: '  cc-backend',
                      href: '$base/plugins/cc-backend/'),
                  SidebarLink(
                      text: '  cc-clickhouse',
                      href: '$base/plugins/cc-clickhouse/'),
                  SidebarLink(
                      text: 'Product Management',
                      href: '$base/plugins/product-management'),
                  SidebarLink(
                      text: '  cc-pm-discovery',
                      href: '$base/plugins/cc-pm-discovery/'),
                  SidebarLink(
                      text: '  cc-pm-strategy',
                      href: '$base/plugins/cc-pm-strategy/'),
                  SidebarLink(
                      text: '  cc-pm-analytics',
                      href: '$base/plugins/cc-pm-analytics/'),
                  SidebarLink(
                      text: '  cc-pm-gtm',
                      href: '$base/plugins/cc-pm-gtm/'),
                  SidebarLink(text: 'UI/UX', href: '$base/plugins/uiux'),
                  SidebarLink(
                      text: '  cc-uiux-design',
                      href: '$base/plugins/cc-uiux-design/'),
                  SidebarLink(
                      text: '  cc-uiux-accessibility',
                      href: '$base/plugins/cc-uiux-accessibility/'),
                  SidebarLink(
                      text: '  cc-uiux-frontend',
                      href: '$base/plugins/cc-uiux-frontend/'),
                  SidebarLink(
                      text: '  cc-uiux-backend',
                      href: '$base/plugins/cc-uiux-backend/'),
                  SidebarLink(
                      text: '  cc-uiux-testing',
                      href: '$base/plugins/cc-uiux-testing/'),
                  SidebarLink(
                      text: '  cc-uiux-devops',
                      href: '$base/plugins/cc-uiux-devops/'),
                  SidebarLink(
                      text: '  cc-uiux-security',
                      href: '$base/plugins/cc-uiux-security/'),
                  SidebarLink(
                      text: 'Pipeline', href: '$base/plugins/pipeline'),
                  SidebarLink(
                      text: '  cc-pipeline',
                      href: '$base/plugins/cc-pipeline/'),
                ],
              ),
              SidebarGroup(
                title: 'Community',
                links: [
                  SidebarLink(text: '기여 가이드', href: '$base/contributing'),
                ],
              ),
            ],
          ),
        ),
      ],
      theme: ContentTheme(
        primary:
            ThemeColor(ThemeColors.indigo.$500, dark: ThemeColors.indigo.$400),
        background:
            ThemeColor(ThemeColors.slate.$50, dark: ThemeColors.zinc.$950),
        colors: [
          ContentColors.quoteBorders.apply(ThemeColors.indigo.$400),
        ],
      ),
    ),
  );
}
