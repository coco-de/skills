import 'package:jaspr/dom.dart';
import 'package:jaspr/jaspr.dart';
import 'package:jaspr_content/components/sidebar_toggle_button.dart';
import 'package:jaspr_content/theme.dart';

class TabLink {
  const TabLink({required this.text, required this.href});

  final String text;
  final String href;
}

/// A header component with a logo, title, tab navigation, and additional items.
///
/// Designed to replace the default [Header] in [DocsLayout] to provide
/// a tab-style navigation bar similar to docs.jaspr.site.
class TabHeader extends StatelessComponent {
  const TabHeader({
    required this.logo,
    required this.title,
    required this.tabs,
    this.items = const [],
    super.key,
  });

  final String logo;
  final String title;
  final List<TabLink> tabs;
  final List<Component> items;

  @override
  Component build(BuildContext context) {
    return Component.fragment([
      Document.head(children: [Style(styles: _styles)]),
      header(classes: 'tab-header', [
        div(classes: 'tab-header-top', [
          SidebarToggleButton(),
          a(classes: 'tab-header-title', href: '/', [
            img(src: logo, alt: 'Logo'),
            span([Component.text(title)]),
          ]),
          div(classes: 'tab-header-items', items),
        ]),
        nav(classes: 'tab-header-tabs', [
          for (final tab in tabs)
            a(classes: 'tab-link', href: tab.href, [
              Component.text(tab.text),
            ]),
        ]),
      ]),
    ]);
  }

  static List<StyleRule> get _styles => [
    css('.tab-header', [
      css('&').styles(
        display: Display.flex,
        raw: {'flex-direction': 'column'},
      ),
      // Top bar: logo + title + items
      css('.tab-header-top', [
        css('&').styles(
          height: 4.rem,
          display: Display.flex,
          alignItems: AlignItems.center,
          gap: Gap.column(1.rem),
          padding: Padding.symmetric(horizontal: 1.rem, vertical: .25.rem),
          margin: Margin.symmetric(horizontal: Unit.auto),
          width: 100.percent,
          raw: {'box-sizing': 'border-box'},
        ),
        css.media(MediaQuery.all(minWidth: 768.px), [
          css('&').styles(
              padding: Padding.symmetric(horizontal: 2.5.rem)),
        ]),
      ]),
      css('.tab-header-title', [
        css('&').styles(
          display: Display.inlineFlex,
          flex: Flex(basis: 17.rem),
          alignItems: AlignItems.center,
          gap: Gap.column(.75.rem),
        ),
        css('img').styles(height: 1.5.rem, width: Unit.auto),
        css('span').styles(fontWeight: FontWeight.w700),
      ]),
      css('.tab-header-items', [
        css('&').styles(
          display: Display.flex,
          flex: Flex(grow: 1),
          justifyContent: JustifyContent.end,
          gap: Gap.column(0.25.rem),
        ),
      ]),
      // Tab bar
      css('.tab-header-tabs', [
        css('&').styles(
          display: Display.flex,
          gap: Gap.column(0.25.rem),
          padding: Padding.symmetric(horizontal: 1.rem),
          border: Border.only(
            top: BorderSide(color: Color('#0000000d'), width: 1.px),
          ),
          raw: {'box-sizing': 'border-box'},
        ),
        css.media(MediaQuery.all(minWidth: 768.px), [
          css('&').styles(
              padding: Padding.symmetric(horizontal: 2.5.rem)),
        ]),
      ]),
      // Hide tab bar on small screens, show scrollable on mobile
      css.media(MediaQuery.all(maxWidth: 640.px), [
        css('.tab-header-tabs').styles(
          raw: {'overflow-x': 'auto', 'white-space': 'nowrap', '-webkit-overflow-scrolling': 'touch'},
        ),
      ]),
      css('.tab-link', [
        css('&').styles(
          display: Display.inlineFlex,
          alignItems: AlignItems.center,
          padding: Padding.symmetric(horizontal: .75.rem, vertical: .5.rem),
          fontSize: .875.rem,
          fontWeight: FontWeight.w500,
          color: ContentColors.text,
          opacity: 0.65,
          border: Border.only(
            bottom: BorderSide(color: Color('transparent'), width: 2.px),
          ),
          raw: {
            'text-decoration': 'none',
            'transition': 'color 150ms ease, opacity 150ms ease, border-color 150ms ease',
          },
        ),
        css('&:hover').styles(
          opacity: 1,
          color: ContentColors.primary,
        ),
      ]),
    ]),
    // Override DocsLayout offsets to account for the taller header (4rem top + ~2.25rem tabs)
    css('.docs', [
      css('.sidebar-container').styles(
        raw: {'top': '6.25rem'},
      ),
      css.media(MediaQuery.all(maxWidth: 1023.px), [
        css('.sidebar-container').styles(
          raw: {'top': '0'},
        ),
      ]),
      css('main').styles(
        padding: Padding.only(top: 6.25.rem),
      ),
    ]),
  ];
}
