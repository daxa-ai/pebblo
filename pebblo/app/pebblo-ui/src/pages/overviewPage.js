import { TabPanel } from "../components/Tab.js";
import { ApplicationsList, Tabs } from "../components/index.js";
import {
  TABS_ARR_FOR_APPLICATIONS,
  TAB_PANEL_ARR_FOR_APPLICATIONS,
} from "../constants/constant.js";

export function OverviewPage() {
  return /*html*/ `
       <div class="flex gap-5 flex-col h-full overflow-auto">
        <div class="surface-10 inter font-14 medium">Overview</div>
         ${Tabs(TABS_ARR_FOR_APPLICATIONS, TAB_PANEL_ARR_FOR_APPLICATIONS)}
       </div>
      `;
}
