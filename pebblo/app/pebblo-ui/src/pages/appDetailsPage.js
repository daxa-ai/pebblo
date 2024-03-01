import { get_Formatted_Date } from "../util.js";
import {
  AccordionSummary,
  AccordionDetails,
  Button,
  KeyValue,
  Tabs,
  Dialog,
  Table,
} from "../components/index.js";
import {
  APP_DATA,
  APP_DETAILS,
  LOAD_HISTORY_TABLE,
  LOAD_HISTORY_TABLE_COL,
  MEDIA_URL,
  TABS_ARR_FOR_APPLICATION_DETAILS,
  TAB_PANEL_ARR_FOR_APPLICATION_DETAILS,
} from "../constants/constant.js";
import { CLICK, LOAD, PATH } from "../constants/enums.js";
import { GET_FILE } from "../services/get.js";
import { GET_REPORT } from "../constants/routesConstant.js";

const DialogBody = () => {
  return /*html*/ `
  <div class="load-history-table pt-6 pb-6 pr-6 pl-6 rounded-md">
    ${Table({
      tableCol: LOAD_HISTORY_TABLE_COL,
      tableData: LOAD_HISTORY_TABLE,
    })}
  </div>
  `;
};

export function AppDetailsPage() {
  window.addEventListener(LOAD, function () {
    const download_icon = document.getElementById("download_report_btn");
    download_icon.addEventListener(CLICK, function () {
      GET_FILE(`${GET_REPORT}?app_name=${APP_DATA?.name}`);
    });
  });

  // last updated date
  // <div class="font-thin">Last Updated 13 Feb 2024
  // </div>
  // <div class="divider"></div>

  return /*html*/ `
    <div class="flex gap-6 flex-col h-full overflow-auto">
      <div class="flex justify-between">
        <div class="flex gap-3">
           <div class="bg-surface-10 pl-2 pr-2 pt-4 pb-4 rounded-lg">
             <img src="${MEDIA_URL}/static/langchain-icon.png" alt="App icon" />
           </div>
           <div class="flex flex-col gap-1 inter surface-10">
             <div class="font-24">${APP_DATA?.name}</div>
             <div class="font-12 flex gap-3">
          
               ${AccordionSummary({ children: "Instance Details", id: 1 })}
             </div>
           </div>
        </div>
        <div class="flex gap-2 mt-auto h-fit">
          ${Button({
            variant: "text",
            btnText: "Download Report",
            startIcon: "/static/download-icon.png",
            id: "download_report_btn",
          })}
          <div class="divider mt-2 mb-2"></div>
          ${Button({
            variant: "text",
            btnText: "Load History",
            startIcon: "/static/pending-icon.png",
            id: "load_history_dialog_btn",
          })}
        </div>
      </div>
      ${AccordionDetails({
        children: /*html*/ `<div class="grid grid-cols-4 row-gap-3 col-gap-3 w-full">
           ${APP_DETAILS?.myMap((item) =>
             KeyValue({
               key: item.label,
               value: item.value,
               className: item?.label === PATH ? "col-4" : "",
             })
           )}
        </div>`,
        id: "panel-1",
      })}
      <div class="divider-horizontal"></div>
      <div class="flex flex-col gap-4 h-full">
        <div class="flex gap-2 surface-10 inter items-center">
           <div class="font-16">Report Summary</div>
           <div class="font-12">Current Load By ${
             APP_DATA?.reportSummary.owner
           }, ${get_Formatted_Date(APP_DATA?.reportSummary.createdAt)} </div>

        </div>
        ${Tabs(
          TABS_ARR_FOR_APPLICATION_DETAILS,
          TAB_PANEL_ARR_FOR_APPLICATION_DETAILS
        )}
      </div>

      ${Dialog({
        title: "Load History",
        maxWidth: "md",
        dialogBody: DialogBody(),
        dialogId: "load_history_dialog",
        btnId: "load_history_dialog_btn",
      })}
   </div>
    `;
}
