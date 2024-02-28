import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebars: SidebarsConfig = {
  sidebar: [
    {
      type: "doc",
      id: "introduction", // document ID
      label: "Overview", // sidebar label
    },
    {
      type: "doc",
      id: "installation", // document ID
      label: "Installation", // sidebar label
    },
    {
      type: "doc",
      id: "development", // document ID
      label: "Development Environment", // sidebar label
    },
    {
      type: "doc",
      id: "config", // document ID
      label: "Configuration", // sidebar label
    },
    {
      type: "category",
      label: "Pebblo", // sidebar label
      items: [
        {
          type: "doc",
          label: "Server",
          id: "daemon",
        },
        {
          type: "doc",
          label: "Entity Classifier",
          id: "entityclassifier",
        },
        {
          type: "doc",
          label: "Topic Classifier",
          id: "topicclassifier",
        },
      ],
    },
    {
      type: "doc",
      id: "rag", // document ID
      label: "Safe DataLoader for Langchain", // sidebar label
    },
    {
      type: "doc",
      id: "reports", // document ID
      label: "Reports", // sidebar label
    },
    {
      type: "doc",
      id: "troubleshooting", // document ID
      label: "Troubleshooting Guide", // sidebar label
    },
  ],
};

export default sidebars;
