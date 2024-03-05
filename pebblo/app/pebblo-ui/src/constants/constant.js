import { ApplicationsList, SnippetDetails } from "../components/index.js";
import { Tooltip } from "../components/tooltip.js";
import { get_Formatted_Date } from "../util.js";
import { APP_DETAILS_ROUTE } from "./routesConstant.js";

export const MEDIA_URL = document.scripts[0].getAttribute("staticURL");
export const APP_DATA = JSON.parse(document.scripts[0].getAttribute("appData"));
export const PORT = window.location.port;

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
    render:() => APP_DATA?.dataSources[0]?.name
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
    value: APP_DATA?.instanceDetails?.path,
  },
];

export const FILES_WITH_FINDINGS_TABLE = [
  {
    label: "File Name",
    field: "fileName",
    render: (item) => /*html*/ `
    <div class="flex flex-col inter">
       <div class="surface-10 font-13">${item.fileName || "-"}</div>
       <div class="surface-10-opacity-50 font-12 flex">
         <div>${item?.sourceSize || "-"} | ${item?.fileOwner || "-"}</div>
       </div>
    </div>
 `,
    align: "start",
  },
  {
    label: "Findings-Topics",
    field: "findingsTopics",
    align: "end",
  },
  {
    label: "Findings-Entities",
    field: "findingsEntities",
    align: "end",
  },
  {
    label: "Data Source",
    render:() => APP_DATA?.dataSources[0]?.name
  },
];

export const DATA_SOURCE_TABLE = [
  {
    label: "Finding Type",
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
];

export const TABLE_DATA_FOR_APPLICATIONS = [
  {
    label: "Application",
    field: "name",
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
    render: (item) =>
      Tooltip({
        children: /*html*/ `<div class="flex gap-4 justify-end">
      <img id="${item?.name}" class="download-icon" class="cursor-pointer" src="${MEDIA_URL}/static/download-icon.png" alt="Download Icon" />
    </div>`,
        title: "Download Icon",
        variant: "right",
      }),
    align: "start",
    //   render: /*html*/ `
    //   <div class="flex gap-4 justify-end">
    //     <img id="download_icon" class="cursor-pointer" src="${MEDIA_URL}/static/download-icon.png" alt="Download Icon" />
    //     <div class="divider"></div>
    //     <img id="load_history_icon" class="cursor-pointer" src="${MEDIA_URL}/static/pending-icon.png" alt="Download Icon" />
    //   </div>
    // `
  },
];

export const TABLE_DATA_FOR_FINDINGS = [
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
    label: "Application",
    field: "appName",
    align: "start",
  },
];

export const TABLE_DATA_FOR_FILES_WITH_FINDINGS = [
  {
    label: "File Name",
    field: "sourceFilePath",
    align: "start",
    render: (item) => /*html*/ `
     <div>${item?.sourceFilePath}</div>
     <div>By ${item?.owner}</div>
    `,
    isTooltip: true,
    tooltipTitle: (item) => item.sourceFilePath,
  },
  {
    label: "Findings-Topics",
    field: "findingsTopics",
    align: "end",
  },
  {
    label: "Findings-Entities",
    field: "findingsEntities",
    align: "end",
  },
  {
    label: "Data Source",
    field: "sourceName",
    align: "start",
  },
  {
    label: "Application",
    field: "appName",
    align: "start",
  },
];

export const TABLE_DATA_FOR_DATA_SOURCE = [
  {
    label: "Data Source Name",
    field: "name",
    render: (item) => /*html*/ `
      <div class="flex flex-col inter">
         <div class="surface-10 font-13">${item.name || "-"}</div>
         <div class="surface-10-opacity-50 font-12">${item.sourceSize} | ${
      item.sourcePath
    }</div>
      </div>
   `,
    align: "start",
  },
  {
    label: "Findings-Topics",
    field: "findingsTopics",
    align: "end",
  },
  {
    label: "Findings-Entities",
    field: "findingsEntities",
    align: "end",
  },
  {
    label: "Application",
    field: "appName",
    align: "start",
  },
];

export const TABLE_DATA_FOR_DATA_SOURCE_APP_DETAILS = [
  {
    label: "Data Source Name",
    field: "name",
    render: (item) => /*html*/ `
      <div class="flex flex-col inter">
         <div class="surface-10 font-13">${item.name || "-"}</div>
         <div class="surface-10-opacity-50 font-12">${item.sourceSize} | ${
      item.sourcePath
    }</div>
      </div>
   `,
    align: "start",
  },
  {
    label: "Findings-Topics",
    render:()=>APP_DATA?.reportSummary?.findingsTopics,
    align: "end",
  },
  {
    label: "Findings-Entities",
    render:()=> APP_DATA?.reportSummary?.findingsEntities,
    align: "end",
  },
  {
    label: "Application",
    field:"appName",
    render:()=> APP_DATA?.name,
    align: "start",
  },
];

export const TABS_ARR_FOR_APPLICATIONS = [
  {
    label: "Applications With Findings",
    critical: APP_DATA?.applicationsAtRiskCount || 0,
    outOf: APP_DATA?.appList?.length || 0,
    value: 0,
    isCritical: true,
  },
  {
    label: "Findings",
    critical: APP_DATA?.findingsCount || 0,
    value: 1,
    isCritical: true,
  },
  {
    label: "Documents With Findings",
    critical: APP_DATA?.documentsWithFindingsCount || 0,
    value: 2,
    isCritical: true,
  },
  {
    label: "Data Source",
    critical: APP_DATA?.dataSourceCount || 0,
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
      searchField: ["name", "owner"],
      isSorting: true,
      link: APP_DETAILS_ROUTE,
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Findings",
      tableCol: TABLE_DATA_FOR_FINDINGS,
      tableData: APP_DATA?.findings,
      isDownloadReport: false,
      searchField: ["findingsType", "labelName","appName"],
      isSorting: true,
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Documents With Findings",
      tableCol: TABLE_DATA_FOR_FILES_WITH_FINDINGS,
      tableData: APP_DATA?.documentsWithFindings,
      isDownloadReport: false,
      searchField: ["sourceFilePath", "appName"],
      isSorting: true,
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Data Source",
      tableCol: TABLE_DATA_FOR_DATA_SOURCE,
      tableData: APP_DATA?.dataSource,
      isDownloadReport: false,
      searchField: ["name", "appName"],
      isSorting: true,
    },
    component: ApplicationsList,
  },
];

export const TABS_ARR_FOR_APPLICATION_DETAILS = [
  {
    label: "Findings",
    critical: APP_DATA?.reportSummary?.findings || 0,
    value: 0,
    isCritical: true,
  },
  {
    label: "Documents With Findings",
    critical: APP_DATA?.reportSummary?.filesWithFindings || 0,
    outOf: APP_DATA?.reportSummary?.totalFiles || 0,
    value: 1,
    isCritical: true,
  },
  {
    label: "Data Source",
    critical: APP_DATA?.reportSummary?.dataSources || 0,
    value: 2,
    isCritical: false,
  },
  {
    label: "Snippets",
    critical: APP_DATA?.dataSources
      ? APP_DATA?.dataSources[0]?.displayedSnippetCount
      : 0,
    outOf: APP_DATA?.dataSources
    ? APP_DATA?.dataSources[0]?.totalSnippetCount
    : 0,
    value: 3,
    isCritical: false,
  },
];

export const TAB_PANEL_ARR_FOR_APPLICATION_DETAILS = [
  {
    value: {
      title: "Findings",
      tableCol: APP_DETAILS_FINDINGS_TABLE,
      tableData: APP_DATA?.dataSources
        ? APP_DATA?.dataSources[0]?.findingsSummary
        : [],
      searchField: ["labelName", "findingsType"],
      isSorting: true,
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Documents With Findings",
      tableCol: FILES_WITH_FINDINGS_TABLE,
      tableData: APP_DATA?.topFindings,
      searchField: ["fileName"],
      isSorting: true,
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Data Source",
      tableCol: TABLE_DATA_FOR_DATA_SOURCE_APP_DETAILS,
      tableData: APP_DATA?.dataSources ? APP_DATA?.dataSources : [],
      searchField: ["name"],
      isSorting: true,
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Snippets",
      data: APP_DATA?.dataSources
        ? APP_DATA?.dataSources[0]?.findingsDetails
        : [],
      searchField: ["labelName", "findingsType"],
    },
    component: SnippetDetails,
  },
];

export const LOAD_HISTORY_TABLE_COL = [
  {
    label: "Report Name",
    field: "reportName",
    isTooltip: true,
    tooltipTitle: (item) => item.reportName,
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
