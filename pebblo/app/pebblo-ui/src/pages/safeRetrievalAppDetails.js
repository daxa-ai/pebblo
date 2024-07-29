import {
  AccordionDetails,
  AccordionSummary,
  DeleteAppButton,
  KeyValue,
  Tabs,
} from "../components/index.js";
import {
  APP_DATA,
  APP_DETAILS,
  MEDIA_URL,
  TABS_ARR_FOR_APP_DETAILS_RETRIEVAL,
  TAB_PANEL_ARR_APP_DETAILS_RETRIEVAL,
} from "../constants/constant.js";
import { PATH } from "../constants/enums.js";
import { SAFE_RETRIEVAL_ROUTE } from "../constants/routesConstant.js";

export function SafeRetrievalAppDetails(props) {
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
    <div>
      ${DeleteAppButton({
        appName: APP_DATA?.name,
        redirectRoute: SAFE_RETRIEVAL_ROUTE,
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
  <div class="font-18 medium surface-10 inter">Overview</div>
  ${Tabs(
    TABS_ARR_FOR_APP_DETAILS_RETRIEVAL,
    TAB_PANEL_ARR_APP_DETAILS_RETRIEVAL
  )}
  </div>
    `;
}
