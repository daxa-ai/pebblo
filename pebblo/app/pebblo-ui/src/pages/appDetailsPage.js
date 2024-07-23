import { capitalizeFirstLetter, getFormattedDate } from "../util.js";
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
  LOAD_HISTORY_TABLE_DATA,
  LOAD_HISTORY_TABLE_COL,
  MEDIA_URL,
  TABS_ARR_FOR_APPLICATION_DETAILS,
  TAB_PANEL_ARR_FOR_APPLICATION_DETAILS,
} from "../constants/constant.js";
import { CLICK, LOAD, PATH } from "../constants/enums.js";
import { GET_FILE } from "../services/get.js";
import {
  DASHBOARD_ROUTE,
  DELETE_APP_ROUTE,
  GET_REPORT,
} from "../constants/routesConstant.js";
import {
  CheckIcon,
  CopyIcon,
  DownloadIcon,
  LoadHistoryIcon,
} from "../icons/index.js";
import DeleteIcon from "../icons/deleteIcon.js";
import { DELETE_APP } from "../services/delete.js";

const SUCCESS_CODE = 200;

const DialogBody = () => {
  return /*html*/ `
  <div class="load-history-table pt-6 pb-6 pr-6 pl-6 rounded-md">
    ${Table({
      tableCol: LOAD_HISTORY_TABLE_COL,
      tableData: LOAD_HISTORY_TABLE_DATA,
    })}
  </div>
  `;
};

const DeleteAppDialogBody = () => {
  window.addEventListener(LOAD, function () {
    const delete_icon = document.getElementById("delete_confirm_btn");
    const DIALOG = document.getElementById("delete_app_dialog");
    delete_icon?.addEventListener(CLICK, async function () {
      const res = await DELETE_APP(
        `${DELETE_APP_ROUTE}?app_name=${APP_DATA?.name}`
      );
      if (res.status === SUCCESS_CODE) {
        window.location.href = DASHBOARD_ROUTE;
      } else {
        DIALOG.close();
      }
    });
  });

  return /*html*/ `
   <div>
    <div class="flex flex-col gap-1">
      <div class="font-14 inter">Are you sure you want to delete this app?</div>
    </div>
    <div class="text-right">
      ${Button({
        class: "ml-auto",
        id: `delete_confirm_btn`,
        variant: "contained",
        btnText: "Confirm",
        color: "critical",
      })}
    </div>
   </div>
  `;
};

export function AppDetailsPage() {
  window.addEventListener(LOAD, function () {
    const download_icon = document.getElementById("download_report_btn");
    const copyPath = document.getElementById("copy_path");
    download_icon?.addEventListener(CLICK, function () {
      GET_FILE(`${GET_REPORT}?app_name=${APP_DATA?.name}`);
    });
    copyPath?.addEventListener("click", onCopyText);
  });

  function onCopyText() {
    const pathValue = document.getElementById("path_value");
    const copyIcon = document.getElementById("copy_path");
    const copyTooltip = document.getElementById("copy_tooltip");
    copyIcon.innerHTML = CheckIcon({ color: "success" });
    copyTooltip.style.visibility = "visible";
    navigator.clipboard.writeText(pathValue.textContent);
    const setIcon = setTimeout(() => {
      copyIcon.innerHTML = CopyIcon({ color: "grey", class: "cursor-pointer" });
      copyTooltip.style.visibility = "hidden";
      clearTimeout(setIcon);
    }, 2000);
  }

  return /*html*/ `
    <div class="flex gap-6 flex-col h-full overflow-auto">
      <div class="flex justify-between">
        <div class="flex gap-3">
           <div class="bg-surface-10 pl-2 pr-2 pt-4 pb-4 rounded-lg">
             <img src="${MEDIA_URL}/static/langchain-icon.png" alt="App icon" />
           </div>
           <div class="flex flex-col gap-1 inter surface-10">
             <div class="font-24">${capitalizeFirstLetter(APP_DATA?.name)}</div>
             <div class="font-12 flex gap-3">
          
               ${AccordionSummary({ children: "Instance Details", id: 1 })}
             </div>
           </div>
        </div>
        <div class="flex gap-2 mt-auto h-fit">
          ${Button({
            variant: "text",
            btnText: "Download Report",
            startIcon: DownloadIcon({ color: "primary" }),
            id: "download_report_btn",
            color: "primary",
          })}
          <div class="divider mt-2 mb-2"></div>
          ${Button({
            variant: "text",
            btnText: "Load History",
            startIcon: LoadHistoryIcon({ color: "primary" }),
            id: "load_history_dialog_btn",
            color: "primary",
          })}
          <div class="divider mt-2 mb-2"></div>
          ${Button({
            variant: "text",
            btnText: "Delete App",
            startIcon: DeleteIcon({ color: "critical" }),
            id: "delete_app_btn",
            color: "critical",
          })}
        </div>
      </div>
      ${AccordionDetails({
        children: /*html*/ `<div class="grid grid-cols-4 row-gap-3 col-gap-3 w-full">
           ${APP_DETAILS?.myMap((item) =>
             KeyValue({
               key: item.label,
               value: item?.render ? item.render : item.value,
               className: item?.label === PATH ? "col-3" : "",
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
             APP_DATA?.reportSummary?.owner
           }, ${getFormattedDate(
    APP_DATA?.reportSummary?.createdAt,
    false,
    true
  )} </div>

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
      ${Dialog({
        title: "Delete App",
        maxWidth: "sm",
        dialogBody: DeleteAppDialogBody(),
        dialogId: "delete_app_dialog",
        btnId: "delete_app_btn",
      })}
   </div>
    `;
}
