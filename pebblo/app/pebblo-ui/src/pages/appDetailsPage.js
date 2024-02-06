import { getFormattedDate } from "../util.js";
import {
  AccordionSummary,
  AccordionDetails,
  Button,
  KeyValue,
  Tabs,
  Application_Details_List_Section,
  SnippetDetails,
} from "../components/index.js";

const MEDIA_URL = document.scripts[0].getAttribute("staticURL");
const APP_DATA = JSON.parse(document.scripts[0].getAttribute("appData"));

const APP_DETAILS_FINDINGS_TABLE = [
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
    align: "end",
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
];

const TABS_ARR_FOR_APPLICATION_DETAILS = [
  {
    label: "Findings",
    critical: 72,
    outOf: 0,
    value: 0,
    isCritical: true,
    tabPanel: Application_Details_List_Section(
      "Findings",
      APP_DETAILS_FINDINGS_TABLE,
      []
    ),
  },
  {
    label: "Files With Findings",
    critical: 8,
    outOf: 24,
    value: 1,
    isCritical: true,
    tabPanel: Application_Details_List_Section(
      "Files With Findngs",
      APP_DETAILS_FINDINGS_TABLE,
      []
    ),
  },
  {
    label: "Data Source",
    critical: 4,
    outOf: 0,
    value: 2,
    isCritical: false,
    tabPanel: Application_Details_List_Section(
      "Data Source",
      APP_DETAILS_FINDINGS_TABLE,
      []
    ),
  },
  {
    label: "Snippets",
    critical: 254,
    outOf: 0,
    value: 3,
    isCritical: false,
    tabPanel: SnippetDetails(APP_DATA?.dataSources[0]?.findingsDetails),
  },
];

const APP_DETAILS = [
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
    value: getFormattedDate(APP_DATA?.instanceDetails?.createdAt),
  },
  {
    label: "Path",
    value:
      "/Users/shreyasdamle/work/cloud_defense/daxa-analyzer-rc1/samples/basic_retrieval",
  },
];

export function AppDetailsPage() {
  return `
    <div class="flex gap-6 flex-col h-full overflow-auto">
      <div class="flex justify-between">
        <div class="flex gap-3">
           <div class="bg-surface-10 pl-2 pr-2 pt-4 pb-4 rounded-lg">
             <img src="${MEDIA_URL}/static/langchain-icon.png" alt="App icon" />
           </div>
           <div class="flex flex-col gap-1 inter surface-10">
             <div class="font-24">${APP_DATA?.name}</div>
             <div class="font-12 flex gap-3">
               <div class="font-thin">Last Updated ${getFormattedDate(
                 APP_DATA?.lastModified
               )}</div>
               <div class="divider"></div>
               ${AccordionSummary("Instance Details", 1)}
             </div>
           </div>
        </div>
        <div class="flex gap-2 mt-auto h-fit">
          ${Button({
            variant: "text",
            btnText: "Download Report",
            startIcon: "/static/download-icon.png",
          })}
          <div class="divider mt-2 mb-2"></div>
          ${Button({
            variant: "text",
            btnText: "Load History",
            startIcon: "/static/pending-icon.png",
          })}
        </div>
      </div>
      ${AccordionDetails(
        `<div class="grid grid-cols-4 row-gap-3 col-gap-3 w-full">
           ${APP_DETAILS?.map((item) =>
             KeyValue(
               item.label,
               item.value,
               item?.label === "Path" ? "col-4" : ""
             )
           ).join("")}
        </div>`,
        "panel-1"
      )}
      <div class="divider-horizontal"></div>
      <div class="flex flex-col gap-4 h-full">
        <div class="flex gap-2 surface-10 inter items-center">
           <div class="font-16">Report Summary</div>
           <div class="font-12">Current Load By ${
             APP_DATA?.reportSummary?.owner
           }, ${getFormattedDate(APP_DATA?.lastModified)} </div>
        </div>
        ${Tabs(
          TABS_ARR_FOR_APPLICATION_DETAILS,
          Application_Details_List_Section(
            "Findings",
            APP_DETAILS_FINDINGS_TABLE,
            []
          )
        )}
      </div>
   </div>
    `;
}
