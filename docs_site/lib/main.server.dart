/// The entrypoint for the **server** environment.
library;

import 'package:jaspr/server.dart';

import 'package:jaspr_content/components/callout.dart';

import 'package:jaspr_content/components/image.dart';
import 'package:jaspr_content/components/tabs.dart';
import 'package:jaspr_content/components/sidebar.dart';
import 'package:jaspr_content/components/theme_toggle.dart';
import 'package:jaspr_content/jaspr_content.dart';
import 'package:jaspr_content/theme.dart';

import 'components/tab_header.dart';
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
        Tabs(),
      ],
      layouts: [
        DocsLayout(
          header: TabHeader(
            title: 'Cocode Skills',
            logo: '$base/images/logo.svg',
            tabs: [
              TabLink(text: 'Overview', href: '$base/'),
              TabLink(text: '시작하기', href: '$base/getting-started'),
              TabLink(text: 'Plugins', href: '$base/plugins/methodology'),
              TabLink(text: '기여', href: '$base/contributing'),
            ],
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
                title: 'Product & Strategy',
                links: [
                  SidebarLink(
                      text: '방법론 & 워크플로우',
                      href: '$base/plugins/methodology'),
                  SidebarLink(
                      text: 'Product Management',
                      href: '$base/plugins/product-management'),
                ],
              ),
              SidebarGroup(
                title: 'Engineering',
                links: [
                  SidebarLink(
                      text: 'Flutter 개발', href: '$base/plugins/flutter'),
                  SidebarLink(
                      text: '백엔드 & 분석', href: '$base/plugins/backend'),
                  SidebarLink(
                      text: 'UI/UX 엔지니어링', href: '$base/plugins/uiux'),
                  SidebarLink(
                      text: 'Pipeline', href: '$base/plugins/pipeline'),
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
