import { ApplicationsList, SnippetDetails } from "../components/index.js";
import { get_Formatted_Date } from "../util.js";

export const MEDIA_URL = document.scripts[0].getAttribute("staticURL");
export const APP_DATA = JSON.parse(document.scripts[0].getAttribute("appData"));
export const APP_DETAILS_ROUTE = "/appDetails";

export const MONTHS = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

export const APP_DETAILS_FINDINGS_TABLE = [
  {
    label: "Finding type",
    field: "findingsType",
    align: "start",
  },
  {
    label: "Finding",
    field: "labelName",
    align: "start",
  },
  {
    label: "Source Files",
    field: "fileCount",
    align: "end",
  },
  {
    label: "Snippets",
    field: "snippetCount",
    align: "end",
  },
  {
    label: "Data Source",
    field: "findings",
    align: "start",
  },
];

export const APP_DETAILS = [
  {
    label: "IP",
    value: APP_DATA?.instanceDetails?.ip,
  },
  {
    label: "Runtime",
    value: APP_DATA?.instanceDetails?.runtime,
  },
  {
    label: "Language",
    value: APP_DATA?.instanceDetails?.language,
  },
  {
    label: "Host",
    value: APP_DATA?.instanceDetails?.host,
  },
  {
    label: "Created At",
    value: get_Formatted_Date(APP_DATA?.instanceDetails?.createdAt),
  },
  {
    label: "Path",
    value:
      "/Users/shreyasdamle/work/cloud_defense/daxa-analyzer-rc1/samples/basic_retrieval",
  },
];

export const TABLE_DATA_FOR_APPLICATIONS = [
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
    actions: /*html*/ `
        <div class="flex gap-4 justify-end">
          <img id="download_icon" class="cursor-pointer" src="${MEDIA_URL}/static/download-icon.png" alt="Download Icon" />
          <div class="divider"></div>
          <img id="load_history_icon" class="cursor-pointer" src="${MEDIA_URL}/static/pending-icon.png" alt="Download Icon" />
        </div>
      `,
  },
];

export const TABLE_DATA_FOR_FINDINGS = [
  {
    label: "Finding type",
    field: "findingType",
    align: "start",
  },
  {
    label: "Finding",
    field: "label",
    align: "start",
  },
  {
    label: "Source Files",
    field: "sourceFiles",
    align: "end",
  },
  {
    label: "Snippets",
    field: "snippets",
    align: "start",
  },
  {
    label: "Data Source",
    field: "dataSource",
    align: "start",
  },
  {
    label: "Application",
    field: "application",
    align: "start",
  },
];

export const TABLE_DATA_FOR_FILES_WITH_FINDINGS = [
  {
    label: "File Name",
    field: "fileName",
    render: (item) => /*html*/ `
    <div class="flex flex-col inter">
       <div class="surface-10 font-13">${item.fileName || "-"}</div>
       <div class="surface-10-opacity-50 font-12 flex">
         <div>${item?.size || "-"} | ${item?.owner || "-"}</div>
       </div>
    </div>
 `,
    align: "start",
  },
  {
    label: "Findings-Topics",
    field: "topics",
    align: "end",
  },
  {
    label: "Findings-Entities",
    field: "entities",
    align: "end",
  },
  {
    label: "Data Source",
    field: "dataSource",
    align: "start",
  },
  {
    label: "Application",
    field: "application",
    align: "start",
  },
];

export const TABLE_DATA_FOR_DATA_SOURCE = [
  {
    label: "Data Source Name",
    field: "dataSourceName",
    render: (item) => /*html*/ `
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

export const TABS_ARR_FOR_APPLICATIONS = [
  {
    label: "Applications With Findings",
    critical: 2,
    outOf: 4,
    value: 0,
    isCritical: true,
  },
  {
    label: "Findings",
    critical: 72,
    outOf: 0,
    value: 1,
    isCritical: true,
  },
  {
    label: "Files With Findings",
    critical: 8,
    outOf: 24,
    value: 2,
    isCritical: true,
  },
  {
    label: "Data Source",
    critical: 4,
    outOf: 0,
    value: 3,
    isCritical: false,
  },
];

export const TAB_PANEL_ARR_FOR_APPLICATIONS = [
  {
    value: {
      title: "Applications",
      tableCol: TABLE_DATA_FOR_APPLICATIONS,
      tableData: APP_DATA?.appList,
      isDownloadReport: false,
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Findings",
      tableCol: TABLE_DATA_FOR_FINDINGS,
      tableData: APP_DATA?.allFindings,
      isDownloadReport: false,
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Files With Findings",
      tableCol: TABLE_DATA_FOR_FILES_WITH_FINDINGS,
      tableData: APP_DATA?.allFilesWithFindings,
      isDownloadReport: false,
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Data Source",
      tableCol: TABLE_DATA_FOR_DATA_SOURCE,
      tableData: [],
      isDownloadReport: false,
    },
    component: ApplicationsList,
  },
];

export const TABS_ARR_FOR_APPLICATION_DETAILS = [
  {
    label: "Findings",
    critical: 72,
    outOf: 0,
    value: 0,
    isCritical: true,
  },
  {
    label: "Files With Findings",
    critical: 8,
    outOf: 24,
    value: 1,
    isCritical: true,
  },
  {
    label: "Data Source",
    critical: 4,
    outOf: 0,
    value: 2,
    isCritical: false,
  },
  {
    label: "Snippets",
    critical: 254,
    outOf: 0,
    value: 3,
    isCritical: false,
  },
];

export const TAB_PANEL_ARR_FOR_APPLICATION_DETAILS = [
  {
    value: {
      title: "Findings",
      tableCol: APP_DETAILS_FINDINGS_TABLE,
      tableData: APP_DATA?.dataSources[0]?.findingsSummary,
      searchField: ["findingsType"],
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Files With Findngs",
      tableCol: APP_DETAILS_FINDINGS_TABLE,
      tableData: [],
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Data Source",
      tableCol: APP_DETAILS_FINDINGS_TABLE,
      tableData: [],
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Snippets",
      data: APP_DATA?.snippets,
    },
    component: SnippetDetails,
  },
];

export const LOAD_HISTORY_TABLE_COL = [
  {
    label: "Report Name",
    field: "reportName",
    type: "label",
  },
  {
    label: "Findings",
    field: "findings",
  },
  {
    label: "Files With Findings",
    field: "filesWithFindings",
    align: "end",
  },
  {
    label: "Generated On",
    field: "generatedOn",
  },
];

export const LOAD_HISTORY_TABLE = APP_DATA?.loadHistory?.history;
