import { FindingsPanel } from "../components/findingsPanel.js";
import {
  ApplicationsList,
  ViewMore,
  SnippetDetails,
  RetrievalDetails,
  ProgressBar,
} from "../components/index.js";
import { Tooltip } from "../components/tooltip.js";
import { CopyIcon } from "../icons/index.js";
import { DownloadIcon } from "../icons/index.js";
import {
  extractTimezone,
  getDifferenceInDays,
  getFileSize,
  getFormattedDate,
  getMaxValue,
  getStringOfNItems,
  sortByDate,
} from "../util.js";
import { KEYWORD_MAPPING } from "./keywordMapping.js";
import {
  APP_DETAILS_ROUTE,
  DASHBOARD_ROUTE,
  SAFE_RETRIEVAL_APP_ROUTE,
  SAFE_RETRIEVAL_ROUTE,
} from "./routesConstant.js";

const SCRIPT_ELEMENT = document.getElementById("main_script");
export const DOCUMENTATION_URL = "https://daxa-ai.github.io/pebblo";

export const MEDIA_URL = SCRIPT_ELEMENT.dataset["static"];
const APP_DATA_RESP = JSON.parse(SCRIPT_ELEMENT.dataset["appdata"] || "");

export const LOADER_STR = "loaderApps";
export const RETRIEVER_STR = "retrievalApps";

export const CURRENT_TAB = window.location.pathname?.includes(
  SAFE_RETRIEVAL_ROUTE
)
  ? RETRIEVER_STR
  : LOADER_STR;
export const APP_DATA =
  window.location.pathname.includes(APP_DETAILS_ROUTE) ||
  window.location.pathname.includes(SAFE_RETRIEVAL_APP_ROUTE)
    ? APP_DATA_RESP
    : APP_DATA_RESP[CURRENT_TAB] || {};

export const PORT = window.location.port;

export const SERVER_VERSION = APP_DATA_RESP?.pebbloServerVersion || "";
export const CLIENT_VERSION = APP_DATA?.clientVersion?.version || "";
const CLIENT_NAME = APP_DATA?.clientVersion?.name || "";

const langchainVersion = APP_DATA?.framework?.version
  ? `${APP_DATA?.framework?.name}: ${APP_DATA?.framework?.version}`
  : "";

const PEBBLO_CLIENT_VERSION = CLIENT_VERSION
  ? `${CLIENT_NAME} ${CLIENT_VERSION}`
  : `Client Version: ${APP_DATA?.pebbloClientVersion}`;

export const NO_APPLICATIONS_FOUND = APP_DATA
  ? Object.keys(APP_DATA)?.length === 0
  : true;
export const NO_FINDINGS_FOR_APP =
  APP_DATA && APP_DATA?.reportSummary
    ? APP_DATA.reportSummary?.findings === 0
    : true;

export const EMPTY_STATES = {
  ENABLE_PEBBLO_EMPTY_STATE: {
    image: `${MEDIA_URL}/static/pebblo-image.png`,
    heading: "Enable Pebblo to unlock insights in your Gen-AI apps",
    subHeading:
      "Check out our installation guide or watch the video tutorial to enable Pebblo",
    buttonNodes: [
      {
        variant: "contained",
        btnText: "View Installation Guide",
        href: `${DOCUMENTATION_URL}/installation`,
      },
    ],
  },
  NO_FINDINGS_EMPTY_STATE: {
    image: `${MEDIA_URL}/static/no-findings.png`,
    heading: "",
    subHeading:
      "We scanned all your documents and didn’t discover any documents with findings",
  },
};

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
    render: (item) => KEYWORD_MAPPING[item?.labelName] || item?.labelName,
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
    render: () => APP_DATA?.dataSources[0]?.name,
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
    value: getFormattedDate(APP_DATA?.instanceDetails?.createdAt, false, false),
  },
  {
    label: "Pebblo Client",
    value: `<div class="flex flex-col">
      <div>${PEBBLO_CLIENT_VERSION}</div>
      <div>${langchainVersion}</div>
    </div>`,
  },
  {
    label: "Path",
    render: /*html*/ `
     <div class="flex items-center gap-2">
         <div id="path_value">${APP_DATA?.instanceDetails?.path}</div>
         <div class="relative flex items-center">
          <div id="copy_tooltip" class="copy-text-tooltip">Copied!</div>
          <div id="copy_path">
           ${CopyIcon({ color: "grey", class: "cursor-pointer" })}
          </div>
         </div>
     </div>
    `,
  },
];

export const FILES_WITH_FINDINGS_TABLE = [
  {
    label: "File Name",
    field: "fileName",
    render: (item) => /*html*/ `
    <div class="flex flex-col inter text-none">
       <div class="surface-10 font-13">${item.fileName || "-"}</div>
       <div class="surface-10-opacity-50 font-12 flex">
         <div>${item?.fileOwner || "-"}</div>
       </div>
    </div>
 `,
    align: "start",
    isTooltip: true,
    tooltipTitle: (item) => item.fileName,
  },
  {
    label: "Size",
    field: "sourceSize",
    align: "end",
    render: (item) => getFileSize(item?.sourceSize),
  },
  {
    label: "Findings",
    field: "findingsTopics",
    render: (item) => item.findingsEntities + item.findingsTopics,
    isTooltip: true,
    tooltipTitle: (item) => `
      <div class="surface-main flex flex-col gap-1 inter font-12 font-300 w-10">
        <div class="flex justify-between">
        <div>Topics</div>
        <div>${item.findingsTopics}</div>
        </div>
        <div class="flex justify-between">
        <div>Entities</div>
        <div>${item.findingsEntities}</div>
        </div>
      </div>`,
    tooltipWidth: "fit",
    align: "end",
  },
  {
    label: "Identities",
    field: "authorizedIdentities",
    render: (item) =>
      ViewMore({
        list: item?.authorizedIdentities,
        showCount: 1,
        fileName: item?.fileName,
        id: item.id,
        tableCol: IDENTITY_TABLE_COL,
        tableData: item?.authorizedIdentities?.map((identityName) => ({
          identity: identityName,
        })),
        dialogTitle: `<div class="flex gap-4 items-center">
          <div>Identities (${item?.authorizedIdentities?.length})</div>
          <div class="text-none font-12 surface-10-opacity-50 overflow-ellipsis w-400px overflow-hidden" title="${item.fileName}">Document: ${item?.fileName}</div>     
        </div>`,
      }),
    align: "start",
  },
  {
    label: "Data Source",
    render: () => APP_DATA?.dataSources[0]?.name,
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
    render: (item) => `<span class="text-none">${item?.name}</span>`,
  },
  {
    label: "Findings - Total",
    field: "total",
    render: (item) => {
      return item.topics + item.entities;
    },
    align: "end",
  },
  {
    label: "Topics",
    field: "topics",
    align: "end",
  },
  {
    label: "Entities",
    field: "entities",
    align: "end",
  },
  {
    label: "Owner",
    field: "owner",
    align: "start",
    render: (item) => `<div class="text-none">${item?.owner || "-"}</div>`,
  },
  {
    label: "",
    field: "actions",
    render: (item) =>
      Tooltip({
        children: /*html*/ `<div class="flex gap-4 justify-end">
      ${DownloadIcon({
        color: "primary",
        class: "download-icon",
        id: `${item?.name}`,
      })}
    </div>`,
        title: "Download Icon",
        variant: "right",
      }),
    align: "start",
    //   render: /*html*/ `
    //   <div class="flex gap-4 justify-end">
    //       ${DownloadIcon({ color: "primary", class: 'download-icon', id: `${item?.name}` })}
    //     <div class="divider"></div>
    //       ${LoadHistoryIcon({ color: "primary" })}
    //   </div>
    // `
  },
];

export const TABLE_DATA_FOR_APPLICATIONS_SAFE_RETRIEVAL = [
  {
    label: "Application Name",
    field: "name",
    align: "start",
    render: (item) => {
      return /*html*/ `<div class="flex flex-col gap-1">
        <div class="font-13 text-none">${item?.name}</div>
        <div class="surface-60 font-11">Owner: ${item?.owner}</div>
      </div>`;
    },
  },
  {
    label: "Retrievals",
    field: "retrievals",
    render: (item) => item?.retrievals?.length,
    align: "end",
  },
  {
    label: "Active Users",
    field: "active_users",
    render: (item) => item?.active_users?.length,
    isTooltip: false,
    tooltipTitle: (item) =>
      item?.active_users ? getStringOfNItems(item?.active_users, 3) : "",
    tooltipWidth: "fit",
    align: "center",
  },
  {
    label: "Documents",
    field: "documents",
    render: (item) => item?.documents?.length,
    isTooltip: false,
    tooltipTitle: (item) =>
      item?.documents ? getStringOfNItems(item?.documents, 3) : "",
    tooltipWidth: "fit",
    align: "center",
  },
  {
    label: "VectorDB",
    field: "vector_dbs",
    render: (item) =>
      ViewMore({
        list: item?.vector_dbs,
        showCount: 1,
        fileName: item?.name,
        id: item?.name,
        tableCol: VECTOR_DB_TABLE_COL,
        tableData: item?.vector_dbs?.map((identityName) => ({
          vector_db: identityName,
        })),
        dialogTitle: "Vector DB",
        showTooltip: true,
      }),
    align: "start",
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
    render: (item) => KEYWORD_MAPPING[item?.labelName] || item?.labelName,
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
    render: (item) => `<span class="text-none">${item?.appName}</span>`,
  },
];

export const TABLE_DATA_FOR_FILES_WITH_FINDINGS = [
  {
    label: "File Name",
    field: "sourceFilePath",
    align: "start",
    render: (item) => /*html*/ `
     <div class="text-none">${item?.sourceFilePath}</div>
     <div class="inter font-12 surface-10-opacity-50 text-none">By ${item?.owner}</div>
    `,
    isTooltip: true,
    tooltipTitle: (item) => item.sourceFilePath,
  },
  {
    label: "Size",
    field: "sourceSize",
    align: "end",
    render: (item) => getFileSize(item?.sourceSize),
  },
  {
    label: "Findings",
    field: "findingsTopics",
    render: (item) => item.findingsEntities + item.findingsTopics,
    isTooltip: true,
    tooltipTitle: (item) => `
      <div class="surface-main flex flex-col gap-1 inter font-12 font-300 w-10">
        <div class="flex justify-between">
        <div>Topics</div>
        <div>${item.findingsTopics}</div>
        </div>
        <div class="flex justify-between">
        <div>Entities</div>
        <div>${item.findingsEntities}</div>
        </div>
      </div>`,
    tooltipWidth: "fit",
    align: "end",
  },
  {
    label: "Identities",
    field: "authorizedIdentities ",
    render: (item) =>
      ViewMore({
        list: item?.authorizedIdentities,
        showCount: 1,
        fileName: item?.sourceFilePath,
        id: item.id,
        tableCol: IDENTITY_TABLE_COL,
        tableData: item?.authorizedIdentities?.map((identityName) => ({
          identity: identityName,
        })),
        dialogTitle: `<div class="flex gap-4 items-center">
      <div>Identities (${item?.authorizedIdentities?.length})</div>
      <div class="font-12 surface-10-opacity-50">Document: ${item?.sourceFilePath}</div>
    </div>`,
      }),
    align: "start",
  },
  {
    label: "Application",
    field: "appName",
    align: "start",
    render: (item) => `<span class="text-none">${item?.appName}</span>`,
  },
  {
    label: "Data Source",
    field: "sourceName",
    align: "start",
  },
];

export const TABLE_DATA_FOR_DATA_SOURCE = [
  {
    label: "Data Source Name",
    field: "name",
    render: (item) => /*html*/ `
      <div class="flex flex-col inter text-none">
         <div class="surface-10 font-13">${item.name || "-"}</div>
         <div class="surface-10-opacity-50 font-12">${
           item?.sourceSize ? getFileSize(item.sourceSize) : "-"
         } | ${item.sourcePath}</div>
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
    render: (item) => `<span class="text-none">${item?.appName}</span>`,
  },
];

export const TABLE_DATA_FOR_DATA_SOURCE_APP_DETAILS = [
  {
    label: "Data Source Name",
    field: "name",
    render: (item) => /*html*/ `
      <div class="flex flex-col inter text-none">
         <div class="surface-10 font-13">${item.name || "-"}</div>
         <div class="surface-10-opacity-50 font-12">${
           item.sourceSize ? getFileSize(item.sourceSize) : ""
         } | ${item.sourcePath}</div>
      </div>
   `,
    align: "start",
  },
  {
    label: "Findings-Topics",
    render: () => APP_DATA?.reportSummary?.findingsTopics,
    align: "end",
  },
  {
    label: "Findings-Entities",
    render: () => APP_DATA?.reportSummary?.findingsEntities,
    align: "end",
  },
  {
    label: "Application",
    field: "appName",
    render: () => `<span class="text-none">${APP_DATA?.name}</span>`,
    align: "start",
  },
];

const promptsWithFindingsArr = APP_DATA?.promptDetails
  ? APP_DATA?.promptDetails?.map((prompt, index) => ({
      id: index,
      name: prompt?.entity_name,
      prompts: prompt?.total_prompts,
      users: prompt?.users,
      app: prompt?.app_name,
    }))
  : [];

const IS_CRITICAL_DATA =
  NO_APPLICATIONS_FOUND || APP_DATA?.applicationsAtRiskCount?.length === 0
    ? false
    : true;

export const TABS_ARR_FOR_APPLICATIONS_SAFE_LOADER = [
  {
    label: "Applications With Findings",
    critical: NO_APPLICATIONS_FOUND
      ? "-"
      : APP_DATA?.applicationsAtRiskCount || 0,
    outOf: APP_DATA?.appList?.length || 0,
    value: 0,
    isCritical: IS_CRITICAL_DATA,
  },
  {
    label: "Findings",
    critical: NO_APPLICATIONS_FOUND ? "-" : APP_DATA?.findingsCount || 0,
    value: 1,
    isCritical: IS_CRITICAL_DATA,
  },
  {
    label: "Documents With Findings",
    critical: NO_APPLICATIONS_FOUND
      ? "-"
      : APP_DATA?.documentsWithFindingsCount || 0,
    value: 2,
    isCritical: IS_CRITICAL_DATA,
  },
  {
    label: "Data Source",
    critical: NO_APPLICATIONS_FOUND ? "-" : APP_DATA?.dataSourceCount || 0,
    value: 3,
    isCritical: IS_CRITICAL_DATA,
  },
];

export const TABS_ARR_FOR_APPLICATIONS_SAFE_RETRIEVAL = [
  {
    label: "Applications",
    critical: APP_DATA?.appList?.length || 0,
    value: 0,
    isCritical: false,
  },
  {
    label: "Retrievals",
    critical: APP_DATA?.retrievals?.length || 0,
    value: 1,
    isCritical: false,
    disable: true,
  },
  {
    label: "Prompts with Findings",
    critical: APP_DATA?.total_prompt_with_findings || 0,
    value: 2,
    isCritical: false,
  },
  {
    label: "Active Users",
    critical: APP_DATA?.activeUsers
      ? Object.keys(APP_DATA?.activeUsers)?.length
      : 0,
    value: 2,
    isCritical: false,
    disable: true,
  },
  {
    label: "Violations",
    critical: APP_DATA?.violations?.length || 0,
    value: 3,
    isCritical: false,
    disable: true,
  },
];

const aggregatedFindingsForAllApps = APP_DATA?.findings
  ? APP_DATA?.findings?.reduce((findings, currentFinding, i) => {
      const item =
        i > 0 &&
        findings.find(
          ({ labelName }) => labelName === currentFinding.labelName
        );
      if (item) item.snippetCount += currentFinding.snippetCount;
      else
        findings.push({
          label:
            KEYWORD_MAPPING[currentFinding?.labelName] ||
            currentFinding?.labelName,
          value: currentFinding.snippetCount,
          type: currentFinding.findingsType,
        });
      return findings;
    }, [])
  : [];

const topicsCountAllApps = APP_DATA?.findings
  ? APP_DATA?.findings?.filter((finding) => finding.findingsType === "topics")
      ?.length
  : 0;

const entitiesCountAllApps = APP_DATA?.findings
  ? APP_DATA?.findings?.length - topicsCountAllApps
  : 0;

export const TABLE_DATA_FOR_PROMPTS_WITH_FINDINGS_SAFE_RETRIEVAL = [
  {
    label: "Entity Name",
    field: "name",
    render: (item) => /*html*/ `
      <div class="flex flex-col inter text-none">
         <div class="surface-10 font-13">${KEYWORD_MAPPING[item?.name]}</div>
         <div class="surface-10-opacity-50 font-12"></div>
      </div>
   `,
    align: "start",
  },
  {
    label: "Prompts",
    field: "prompts",
    align: "end",
  },
  {
    label: "Users",
    field: "users",
    render: (item) =>
      ViewMore({
        list: item?.users,
        showCount: 1,
        id: item.id + "user",
        tableCol: [
          {
            label: "Users",
            field: "user",
            align: "start",
            render: (item) =>
              `<div class="text-none">${item?.user || "-"}</div>`,
          },
        ],
        tableData: item?.users?.map((user) => ({
          user,
        })),
        dialogTitle: `<div class="flex gap-4 items-center">
          <div>Users (${item?.users?.length})</div>
        </div>`,
      }),
    align: "start",
  },
  {
    label: "Apps",
    field: "app",
    render: (item) => `<div class="text-none">${item?.app || "-"}</div>`,
    align: "start",
  },
];

export const TAB_PANEL_ARR_FOR_APPLICATIONS_SAFE_LOADER = [
  {
    value: {
      title: "Applications",
      tableCol: TABLE_DATA_FOR_APPLICATIONS,
      tableData: APP_DATA?.appList,
      isDownloadReport: false,
      searchField: ["name", "owner"],
      isSorting: true,
      error: NO_APPLICATIONS_FOUND ? "ENABLE_PEBBLO_EMPTY_STATE" : null,
      link: APP_DETAILS_ROUTE,
      inputPlaceholder: "Search by Application & Owner",
    },
    component: ApplicationsList,
  },
  {
    value: {
      findingsMap: {
        title: "Findings Map",
        chartData: aggregatedFindingsForAllApps,
        chartLegends: [
          {
            label: "Topics",
            value: topicsCountAllApps,
            color: "#A8B7FF",
          },
          {
            label: "Entities",
            value: entitiesCountAllApps,
            color: "#96D7FC",
          },
        ],
        error: NO_APPLICATIONS_FOUND ? "ENABLE_PEBBLO_EMPTY_STATE" : null,
      },
      findingsTable: {
        title: "Findings",
        tableCol: TABLE_DATA_FOR_FINDINGS,
        tableData: APP_DATA?.findings,
        isDownloadReport: false,
        error: NO_APPLICATIONS_FOUND ? "ENABLE_PEBBLO_EMPTY_STATE" : null,
        searchField: ["findingsType", "labelName", "appName"],
        isSorting: true,
        inputPlaceholder: "Search by Finding, Type & Application",
      },
      title: "Findings",
      error: NO_APPLICATIONS_FOUND ? "ENABLE_PEBBLO_EMPTY_STATE" : null,
    },
    component: FindingsPanel,
  },
  {
    value: {
      title: "Documents With Findings",
      tableCol: TABLE_DATA_FOR_FILES_WITH_FINDINGS,
      tableData: APP_DATA?.documentsWithFindings?.map((finding, index) => ({
        ...finding,
        id: index,
      })),
      isDownloadReport: false,
      error: NO_APPLICATIONS_FOUND ? "ENABLE_PEBBLO_EMPTY_STATE" : null,
      searchField: ["sourceFilePath", "appName"],
      isSorting: true,
      inputPlaceholder: "Search by File, Data Source & Application",
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Data Source",
      tableCol: TABLE_DATA_FOR_DATA_SOURCE,
      tableData: APP_DATA?.dataSource,
      isDownloadReport: false,
      error: NO_APPLICATIONS_FOUND ? "ENABLE_PEBBLO_EMPTY_STATE" : null,
      searchField: ["name", "appName"],
      isSorting: true,
      inputPlaceholder: "Search by Data Source & Application",
    },
    component: ApplicationsList,
  },
];

export const TAB_PANEL_ARR_FOR_APPLICATIONS_SAFE_RETRIEVAL = [
  {
    value: {
      title: "Applications",
      tableCol: TABLE_DATA_FOR_APPLICATIONS_SAFE_RETRIEVAL,
      tableData: APP_DATA?.appList,
      isDownloadReport: false,
      searchField: ["name"],
      isSorting: false,
      error: NO_APPLICATIONS_FOUND ? "ENABLE_PEBBLO_EMPTY_STATE" : null,
      link: SAFE_RETRIEVAL_APP_ROUTE,
      inputPlaceholder: "Search By Application Name",
    },
    component: ApplicationsList,
  },
  {},
  {
    value: {
      title: "Prompts with Findings",
      tableCol: TABLE_DATA_FOR_PROMPTS_WITH_FINDINGS_SAFE_RETRIEVAL,
      tableData: promptsWithFindingsArr,
      isDownloadReport: false,
      searchField: ["name"],
      isSorting: false,
      error:
        APP_DATA?.total_prompt_with_findings === 0
          ? "NO_FINDINGS_EMPTY_STATE"
          : null,
    },
    component: ApplicationsList,
  },
];

const IS_CRITICAL_COUNT = NO_FINDINGS_FOR_APP ? false : true;

const dataSourceObject =
  APP_DATA?.dataSources && APP_DATA?.dataSources?.length
    ? APP_DATA?.dataSources[0]
    : null;

const aggregatedFindings = dataSourceObject
  ? dataSourceObject?.findingsSummary?.reduce((findings, currentFinding, i) => {
      const item =
        i > 0 &&
        findings.find(
          ({ labelName }) => labelName === currentFinding.labelName
        );
      if (item) item.snippetCount += currentFinding.snippetCount;
      else
        findings.push({
          label:
            KEYWORD_MAPPING[currentFinding?.labelName] ||
            currentFinding?.labelName,
          value: currentFinding.snippetCount,
          type: currentFinding.findingsType,
        });
      return findings;
    }, [])
  : [];

const topicsCount = dataSourceObject
  ? dataSourceObject?.findingsSummary?.filter(
      (finding) => finding.findingsType === "topics"
    )?.length
  : 0;

const entitiesCount = dataSourceObject
  ? dataSourceObject?.findingsSummary?.length - topicsCount
  : 0;

export const TABS_ARR_FOR_APPLICATION_DETAILS = [
  {
    label: "Findings",
    critical: NO_FINDINGS_FOR_APP
      ? "-"
      : APP_DATA?.reportSummary?.findings || 0,
    value: 0,
    isCritical: IS_CRITICAL_COUNT,
  },
  {
    label: "Documents With Findings",
    critical: NO_FINDINGS_FOR_APP
      ? "-"
      : APP_DATA?.reportSummary?.filesWithFindings || 0,
    outOf: NO_FINDINGS_FOR_APP ? "" : APP_DATA?.reportSummary?.totalFiles || 0,
    value: 1,
    isCritical: IS_CRITICAL_COUNT,
  },
  {
    label: "Data Source",
    critical: APP_DATA?.reportSummary?.dataSources || 0,
    value: 2,
    isCritical: false,
  },
  {
    label: "Snippets",
    critical: NO_FINDINGS_FOR_APP
      ? "-"
      : APP_DATA?.dataSources
      ? APP_DATA?.dataSources[0]?.totalSnippetCount
      : 0,
    value: 3,
    isCritical: false,
  },
];

export const TAB_PANEL_ARR_FOR_APPLICATION_DETAILS = [
  {
    value: {
      findingsMap: {
        title: "Snippet Distribution By Topics & Entities",
        chartData: aggregatedFindings,
        chartLegends: [
          {
            label: "Topics",
            value: topicsCount,
            color: "#A8B7FF",
          },
          {
            label: "Entities",
            value: entitiesCount,
            color: "#96D7FC",
          },
        ],
        error: NO_FINDINGS_FOR_APP ? "NO_FINDINGS_EMPTY_STATE" : null,
      },
      findingsTable: {
        title: "Findings",
        tableCol: APP_DETAILS_FINDINGS_TABLE,
        tableData: APP_DATA?.dataSources
          ? APP_DATA?.dataSources[0]?.findingsSummary
          : [],
        searchField: ["labelName", "findingsType"],
        isSorting: true,
        inputPlaceholder: "Search by Finding & Type",
        error: NO_FINDINGS_FOR_APP ? "NO_FINDINGS_EMPTY_STATE" : null,
      },
      title: "Findings",
      error: NO_FINDINGS_FOR_APP ? "NO_FINDINGS_EMPTY_STATE" : null,
    },
    component: FindingsPanel,
  },
  {
    value: {
      title: "Documents With Findings",
      tableCol: FILES_WITH_FINDINGS_TABLE,
      tableData: APP_DATA?.topFindings?.map((finding, index) => ({
        ...finding,
        id: index,
      })),
      searchField: ["fileName"],
      isSorting: true,
      inputPlaceholder: "Search by File",
      error: NO_FINDINGS_FOR_APP ? "NO_FINDINGS_EMPTY_STATE" : null,
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
      inputPlaceholder: "Search by Data Source",
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: "Snippets",
      data: {
        snippetCount: dataSourceObject
          ? dataSourceObject?.displayedSnippetCount
          : 0,
        totalSnippetCount: dataSourceObject
          ? dataSourceObject?.totalSnippetCount
          : 0,
        snippets: dataSourceObject ? dataSourceObject?.findingsDetails : [],
      },
      searchField: ["labelName"],
      inputPlaceholder: "Search",
      error: NO_FINDINGS_FOR_APP ? "NO_FINDINGS_EMPTY_STATE" : null,
    },
    component: SnippetDetails,
  },
];

export const TABS_ARR_FOR_APP_DETAILS_RETRIEVAL = [
  {
    label: "Retrievals",
    critical: APP_DATA?.retrievals?.length || 0,
    value: 0,
    isCritical: true,
  },
  {
    label: "Prompts with Findings",
    critical: APP_DATA?.total_prompt_with_findings || 0,
    value: 1,
    isCritical: true,
    disable: true,
  },
  {
    label: "Active Users",
    critical: APP_DATA?.activeUsers
      ? Object.keys(APP_DATA?.activeUsers)?.length
      : 0,
    value: 2,
    isCritical: true,
  },
  {
    label: "Documents",
    critical: APP_DATA?.documents
      ? Object.keys(APP_DATA?.documents)?.length
      : 0,
    value: 3,
    isCritical: true,
  },
  {
    label: "Vector Database",
    critical: APP_DATA?.vectorDbs ? Object.keys(APP_DATA.vectorDbs)?.length : 0,
    value: 4,
    isCritical: true,
    disable: true,
  },
];

let retrievalAppUserBasedRetrievalTotal = 0;
let retrievalAppDocumentRetrievalTotal = 0;

const retrievalAppActiveUsersData = APP_DATA?.activeUsers
  ? sortByDate(
      Object.keys(APP_DATA?.activeUsers)?.map((activeUser, index) => {
        const data = APP_DATA?.activeUsers[activeUser];
        retrievalAppUserBasedRetrievalTotal += data?.retrievals?.length || 0;
        return {
          ...data,
          id: index + 1,
          name: activeUser,
          retrievalCount: data?.retrievals?.length,
        };
      }),
      "last_accessed_time",
      "desc"
    )
  : [];

const retrievalAppDocumentData = APP_DATA?.documents
  ? sortByDate(
      Object.keys(APP_DATA?.documents)?.map((document, index) => {
        const data = APP_DATA?.documents[document];
        retrievalAppDocumentRetrievalTotal += data?.retrievals?.length || 0;
        return {
          ...data,
          id: index + 1,
          name: document,
          retrievalCount: data?.retrievals?.length,
        };
      }),
      "last_accessed_time",
      "desc"
    )
  : [];

export const TAB_PANEL_FOR_APP_ACTIVE_USERS = [
  {
    label: "User",
    field: "user",
    align: "start",
    render: (item) => {
      return /*html*/ `<div class="flex flex-col gap-1 w-300px">
        <div class="font-13 text-none">${item?.name}</div>
      </div>`;
    },
  },
  {
    label: "Retrievals",
    field: "retrievals",
    align: "start",
    render: (item) =>
      ProgressBar({
        value: item?.retrievalCount,
        progress:
          (item?.retrievalCount / retrievalAppUserBasedRetrievalTotal) * 100,
        color: "#526FF3",
        id: item?.id,
      }),
  },
  {
    label: "Last Accessed",
    field: "documents",
    render: (item) =>
      item?.last_accessed_time
        ? getDifferenceInDays(new Date(), new Date(item?.last_accessed_time))
        : "-",
    align: "start",
  },
  {
    label: "Linked Groups",
    field: "linkedGroups",
    render: (item) =>
      ViewMore({
        list: item?.linked_groups,
        showCount: 2,
        fileName: "",
        id: item?.id,
        tableCol: GROUP_TABLE_COL,
        tableData: item?.linked_groups?.map((group) => ({
          group,
        })),
        dialogTitle: `<div class="flex gap-4 items-center">
        <div>Groups (${item?.linked_groups?.length})</div>
      </div>`,
      }),
    align: "start",
  },
];

export const TAB_PANEL_FOR_APP_DOCUMENTS = [
  {
    label: "Document Name",
    field: "name",
    align: "start",
    isTooltip: true,
    tooltipTitle: (item) => item.name,
    tooltipWidth: "fit",
    render: (item) => {
      return /*html*/ `<div class="flex flex-col gap-1 w-400px">
        <div class="font-13 text-none">${item?.name}</div>
      </div>`;
    },
  },
  {
    label: "Retrievals",
    field: "retrievals",
    align: "start",
    render: (item) =>
      ProgressBar({
        value: item?.retrievalCount,
        progress:
          (item?.retrievalCount / retrievalAppDocumentRetrievalTotal) * 100,
        color: "#526FF3",
        id: item?.id,
      }),
  },
  {
    label: "Last Accessed",
    field: "lastAccessed",
    render: (item) =>
      item?.last_accessed_time
        ? getDifferenceInDays(new Date(), new Date(item?.last_accessed_time))
        : "-",
    align: "start",
  },
];

export const TAB_PANEL_ARR_APP_DETAILS_RETRIEVAL = [
  {
    value: {
      title: "",
      data: APP_DATA?.retrievals?.reverse(),
      searchField: ["labelName"],
      inputPlaceholder: "Search",
      error: !APP_DATA?.retrievals?.length ? "NO_FINDINGS_EMPTY_STATE" : null,
    },
    component: RetrievalDetails,
  },
  {},
  {
    value: {
      title: `Users (${
        APP_DATA?.activeUsers ? Object.keys(APP_DATA?.activeUsers)?.length : 0
      })`,
      tableCol: TAB_PANEL_FOR_APP_ACTIVE_USERS,
      tableData: APP_DATA?.activeUsers ? retrievalAppActiveUsersData : [],
      searchField: ["labelName"],
      inputPlaceholder: "Search",
      error: !APP_DATA?.retrievals?.length ? "NO_FINDINGS_EMPTY_STATE" : null,
    },
    component: ApplicationsList,
  },
  {
    value: {
      title: `Documents (${
        APP_DATA?.documents ? Object.keys(APP_DATA?.documents)?.length : 0
      })`,
      tableCol: TAB_PANEL_FOR_APP_DOCUMENTS,
      tableData: APP_DATA?.documents ? retrievalAppDocumentData : [],
      searchField: ["labelName"],
      inputPlaceholder: "Search",
      error: !APP_DATA?.retrievals?.length ? "NO_FINDINGS_EMPTY_STATE" : null,
    },
    component: ApplicationsList,
  },
];

export const TIMEZONE_FOR_LOAD_HISTORY = extractTimezone(
  getFormattedDate(
    APP_DATA?.loadHistory?.history?.length
      ? APP_DATA?.loadHistory?.history[0]?.generatedOn
      : null,
    true,
    true
  )
);

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
    align: "end",
  },
  {
    label: "Files With Findings",
    field: "filesWithFindings",
    align: "end",
  },
  {
    label: `Generated On (${TIMEZONE_FOR_LOAD_HISTORY})`,
    field: "generatedOn",
  },
];

/**
 * Iterated over LOAD_HISTORY_TABLE_DATA and modified date to match format (DD MM YYYY HH:MM, A)
 * 2024-03-14 16:24:06.797429 => Mar 14, 2024, 4:24 PM India Standard Time
 */
export const LOAD_HISTORY_TABLE_DATA = APP_DATA?.loadHistory?.history?.map(
  (loadHistoryItem) => ({
    ...loadHistoryItem,
    generatedOn: getFormattedDate(loadHistoryItem?.generatedOn, true, false),
  })
);

export const IDENTITY_TABLE_COL = [
  {
    label: "Identity",
    field: "identity",
    align: "start",
    render: (item) => `<div class="text-none">${item?.identity || "-"}</div>`,
  },
];

export const VECTOR_DB_TABLE_COL = [
  {
    label: "Vector DB",
    field: "vector_db",
    align: "start",
  },
];

export const GROUP_TABLE_COL = [
  {
    label: "Group",
    field: "group",
    align: "start",
    render: (item) => `<div class="text-none">${item?.group || "-"}</div>`,
  },
];

export const PEBBLO_TABS = [
  {
    name: "Safe Loader",
    link: DASHBOARD_ROUTE,
  },
  {
    name: "Safe Retriever",
    link: SAFE_RETRIEVAL_ROUTE,
  },
];
