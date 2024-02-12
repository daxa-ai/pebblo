import { getFormattedDate } from "../util.js";
import {
  AccordionSummary,
  AccordionDetails,
  Button,
  KeyValue,
  Tabs,
  Dialog,
} from "../components/index.js";
import {
  APP_DATA,
  APP_DETAILS,
  MEDIA_URL,
  TABS_ARR_FOR_APPLICATION_DETAILS,
  TAB_PANEL_ARR_FOR_APPLICATION_DETAILS,
} from "../constants/constant.js";

export function AppDetailsPage() {
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
            id: "showDialogBtn",
          })}
        </div>
      </div>
      ${AccordionDetails(
        /*html*/ `<div class="grid grid-cols-4 row-gap-3 col-gap-3 w-full">
           ${APP_DETAILS?.myMap((item) =>
             KeyValue(
               item.label,
               item.value,
               item?.label === "Path" ? "col-4" : ""
             )
           )}
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
          TAB_PANEL_ARR_FOR_APPLICATION_DETAILS
        )}
      </div>
      ${Dialog({ title: "", maxWidth: "md", children: "" })}
   </div>
    `;
}
