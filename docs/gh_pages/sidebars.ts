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
      id: "daemon", // document ID
      label: "Pebblo Daemon", // sidebar label
    },
    {
      type: "doc",
      id: "rag", // document ID
      label: "Pebblo Safe DataLoader for Langchain", // sidebar label
    },
    {
      type: "doc",
      id: "config", // document ID
      label: "Pebblo Configuration File", // sidebar label
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
    {
      type: "doc",
      id: "entityclassifier", // document ID
      label: "Pebblo Entity Classifier", // sidebar label
    },
    {
      type: "doc",
      id: "topicclassifier", // document ID
      label: "Pebblo Topic Classifier", // sidebar label
    },
  ],
};

export default sidebars;
