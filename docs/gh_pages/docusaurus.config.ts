import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";

const config: Config = {
  title: "Pebblo",
  tagline: "OpenSource Safe DataLoader for Gen AI applications",
  favicon: "img/pebblo-logo.png",
  // Set the production url of your site here
  url: "https://daxa-ai.github.io/",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "/pebblo/",
  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "/daxa-ai", // Usually your GitHub org/user name.
  projectName: "pebblo", // Usually your repo name.
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          routeBasePath: "/",
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: "https://github.com/daxa-ai/pebblo",
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: "Pebblo",
      logo: {
        alt: "Site Logo",
        src: "img/pebblo-logo.png",
        width: 32,
      },
      items: [
        {
          type: "docSidebar",
          sidebarId: "sidebar",
          position: "left",
          label: "Docs",
        },
        {
          href: "https://github.com/daxa-ai/pebblo",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        //{
        //  title: "Community",
        //  items: [
        //    {
        //      label: "Stack Overflow",
        //      href: "https://stackoverflow.com/questions/tagged/docusaurus",
        //    },
        //    {
        //      label: "Discord",
        //      href: "https://discordapp.com/invite/docusaurus",
        //    },
        //    {
        //      label: "Twitter",
        //      href: "https://twitter.com/docusaurus",
        //    },
        //  ],
        //},
        {
          title: "More",
          items: [
            {
              label: "GitHub",
              href: "https://github.com/daxa-ai/pebblo",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },
};

export default config;
