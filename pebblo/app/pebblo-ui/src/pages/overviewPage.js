import { ApplicationsList, Tabs } from "../components/index.js";

const MEDIA_URL = document.scripts[0].getAttribute("staticURL");
const APP_DATA = JSON.parse(document.scripts[0].getAttribute("appData"));

const TABLE_DATA_FOR_APPLICATIONS = [
  {
    label: "Application",
    field: "application",
    align: "start",
  },
  {
    label: "Findings - Topics",
    field: "topics",
    align: "end",
  },
  {
    label: "Findings - Entities",
    field: "entities",
    align: "end",
  },
  {
    label: "Owner",
    field: "owner",
    align: "start",
  },
  {
    label: "",
    field: "actions",
    actions: `
      <div class="flex gap-4 justify-end">
      <img class="cursor-pointer" src="${MEDIA_URL}/static/download-icon.png" alt="Download Icon" />
      <div class="divider"></div>
      <img class="cursor-pointer" src="${MEDIA_URL}/static/pending-icon.png" alt="Download Icon" />
      </div>
    `,
  },
];

const TABLE_DATA_FOR_FINDINGS = [
  {
    label: "Finding type",
    field: "type",
    type: APP_DATA?.name,
    align: "start",
  },
  {
    label: "Finding",
    field: "finding",
    finding: APP_DATA?.reportSummary.findingsTopics,
    align: "start",
  },
  {
    label: "Source Files",
    field: "sourceFiles",
    sourceFiles: APP_DATA?.reportSummary.findingsEntities,
    align: "end",
  },
  {
    label: "Snippets",
    field: "snippets",
    snippets: APP_DATA?.reportSummary.owner,
    align: "start",
  },
  {
    label: "Data Source",
    field: "dataSource",
    dataSource: APP_DATA?.reportSummary.owner,
    align: "start",
  },
  {
    label: "Application",
    field: "application",
    application: "",
    align: "start",
  },
];

const TABLE_DATA_FOR_FILES_WITH_FINDINGS = [
  {
    label: "File Name",
    field: "fileName",
    fileName: "",
    align: "start",
  },
  {
    label: "Findings-Topics",
    field: "findingsTopics",
    findingsTopics: "",
    align: "end",
  },
  {
    label: "Findings-Entities",
    field: "findingsEntities",
    findingsEntities: "",
    align: "end",
  },
  {
    label: "Data Source",
    field: "datasource",
    datasource: "",
    align: "start",
  },
  {
    label: "Application",
    field: "application",
    application: "",
    align: "start",
  },
];

const TABLE_DATA_FOR_DATA_SOURCE = [
  {
    label: "Data Source Name",
    field: "dataSourceName",
    render: (item) => `
    <div class="flex flex-col inter">
       <div class="surface-10 font-13">${item.dataSourceName || "-"}</div>
       <div class="surface-10-opacity-50 font-12">-</div>
    </div>
 `,
    align: "start",
  },
  {
    label: "Findings-Topics",
    field: "findingsTopics",
    findingsTopics: "",
    align: "end",
  },
  {
    label: "Findings-Entities",
    field: "findingsEntities",
    findingsEntities: "",
    align: "end",
  },
  {
    label: "Application",
    field: "application",
    application: "",
    align: "start",
  },
];

const TABS_ARR_FOR_APPLICATIONS = [
  {
    label: "Applications With Findings",
    critical: 2,
    outOf: 4,
    value: 0,
    isCritical: true,
    tabPanel: ApplicationsList(
      "Applications",
      TABLE_DATA_FOR_APPLICATIONS,
      APP_DATA?.appList
    ),
  },
  {
    label: "Findings",
    critical: 72,
    outOf: 0,
    value: 1,
    isCritical: true,
    tabPanel: ApplicationsList("Findings", TABLE_DATA_FOR_FINDINGS, []),
  },
  {
    label: "Files With Findings",
    critical: 8,
    outOf: 24,
    value: 2,
    isCritical: true,
    tabPanel: ApplicationsList(
      "Files With Findings",
      TABLE_DATA_FOR_FILES_WITH_FINDINGS,
      []
    ),
  },
  {
    label: "Data Source",
    critical: 4,
    outOf: 0,
    value: 3,
    isCritical: false,
    tabPanel: ApplicationsList("Data Source", TABLE_DATA_FOR_DATA_SOURCE, []),
  },
];

export function OverviewPage(APP_DATA) {
  return `
       <div class="flex gap-5 flex-col h-full overflow-auto">
        <div class="surface-10 inter font-14 medium">Overview</div>
         ${Tabs(
           TABS_ARR_FOR_APPLICATIONS,
           ApplicationsList(
             "Applications",
             TABLE_DATA_FOR_APPLICATIONS,
             APP_DATA?.appList
           )
         )}
       </div>
      `;
}
