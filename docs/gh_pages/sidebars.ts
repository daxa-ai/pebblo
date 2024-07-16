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
      type: "category",
      label: "Pebblo UI", // sidebar label
      items: [
        { type: "doc", label: "Safe Loader", id: "safe_loader" },
        { type: "doc", label: "Safe Retriever", id: "safe_retriever" },
      ],
    },
    {
      type: "doc",
      id: "rag", // document ID
      label: "Safe DataLoader for Langchain", // sidebar label
    },
    {
      type: "doc",
      id: "retrieval_chain", // document ID
      label: "Safe Retriever for Langchain", // sidebar label
    },
    {
      type: "doc",
      id: "reports", // document ID
      label: "Reports", // sidebar label
    },
    {
        type: "category",
        label: "Samples", // sidebar label
        items: [
            {
              type: "category",
              label: "Safe Loader Samples",
              items: [
                {
                  type: "link",
                  label: "1. Google Drive-Qdrant Safe Loader Sample",
                  href: "https://github.com/daxa-ai/pebblo/tree/main/pebblo_safeloader/langchain/identity-rag",
                },
                {
                  type: "link",
                  label: "2. CSV Loader-Chroma Safe Loader Sample",
                  href: "https://github.com/daxa-ai/pebblo/tree/main/pebblo_safeloader/langchain/acme-corp-rag",
                },
              ],
            },
            {
              type: "doc",
              label: "Safe Retriever Samples",
              id: "safe_retriever_samples",
            }
        ]
    },
    {
      type: "doc",
      id: "troubleshooting", // document ID
      label: "Troubleshooting Guide", // sidebar label
    },
  ],
};

export default sidebars;
