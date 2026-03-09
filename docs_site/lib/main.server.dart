/// The entrypoint for the **server** environment.
library;

import 'package:jaspr/server.dart';

import 'package:jaspr_content/components/callout.dart';

import 'package:jaspr_content/components/github_button.dart';
import 'package:jaspr_content/components/header.dart';
import 'package:jaspr_content/components/image.dart';
import 'package:jaspr_content/components/sidebar.dart';
import 'package:jaspr_content/components/theme_toggle.dart';
import 'package:jaspr_content/jaspr_content.dart';
import 'package:jaspr_content/theme.dart';

import 'main.server.options.dart';

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
            title: 'CoCode Skills',
            logo: 'images/logo.svg',
            items: [
              ThemeToggle(),
              GitHubButton(repo: 'coco-de/skills'),
            ],
          ),
          sidebar: Sidebar(
            groups: [
              SidebarGroup(
                links: [
                  SidebarLink(text: 'Overview', href: '.'),
                  SidebarLink(text: '시작하기', href: 'getting-started'),
                ],
              ),
              SidebarGroup(
                title: 'Plugins',
                links: [
                  SidebarLink(
                      text: '방법론 & 워크플로우',
                      href: 'plugins/methodology'),
                  SidebarLink(
                      text: 'Flutter 개발', href: 'plugins/flutter'),
                  SidebarLink(
                      text: '백엔드 & 분석', href: 'plugins/backend'),
                  SidebarLink(
                      text: 'Product Management',
                      href: 'plugins/product-management'),
                  SidebarLink(text: 'UI/UX', href: 'plugins/uiux'),
                  SidebarLink(
                      text: 'Pipeline', href: 'plugins/pipeline'),
                ],
              ),
              SidebarGroup(
                title: 'Community',
                links: [
                  SidebarLink(text: '기여 가이드', href: 'contributing'),
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
